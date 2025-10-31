import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, add_days

class WorkOrder(Document):
    def validate(self):
        self.validate_bom()
        self.set_required_items()
        self.set_operations()

    def validate_bom(self):
        if not frappe.db.exists("BOM", self.bom_no):
            frappe.throw(f"BOM {self.bom_no} does not exist")
        
        bom_item = frappe.db.get_value("BOM", self.bom_no, "item")
        if bom_item != self.production_item:
            frappe.throw("BOM item does not match production item")

    def set_required_items(self):
        if not self.required_items:
            bom_items = frappe.get_all("BOM Item",
                filters={"parent": self.bom_no},
                fields=["item_code", "qty", "uom"])
            
            for item in bom_items:
                self.append("required_items", {
                    "item_code": item.item_code,
                    "required_qty": item.qty * self.qty,
                    "uom": item.uom,
                    "available_qty": self.get_available_qty(item.item_code)
                })

    def set_operations(self):
        if not self.operations:
            bom_operations = frappe.get_all("BOM Operation",
                filters={"parent": self.bom_no},
                fields=["operation", "time_in_mins", "workstation"])
            
            for op in bom_operations:
                self.append("operations", {
                    "operation": op.operation,
                    "time_in_mins": op.time_in_mins,
                    "workstation": op.workstation,
                    "status": "Pending"
                })

    def get_available_qty(self, item_code):
        return frappe.db.sql("""
            SELECT SUM(actual_qty) 
            FROM `tabStock Ledger Entry` 
            WHERE item_code = %s AND is_cancelled = 0
        """, item_code)[0][0] or 0

    def on_submit(self):
        self.status = "Not Started"
        self.reserve_materials()

    def reserve_materials(self):
        for item in self.required_items:
            if item.available_qty < item.required_qty:
                frappe.throw(f"Insufficient stock for {item.item_code}")
            
            # Create stock reservation
            frappe.get_doc({
                "doctype": "Stock Reservation",
                "item_code": item.item_code,
                "warehouse": "Stores - HC",  # Default warehouse
                "qty": item.required_qty,
                "voucher_type": "Work Order",
                "voucher_no": self.name
            }).insert()

@frappe.whitelist()
def start_work_order(work_order):
    doc = frappe.get_doc("Work Order", work_order)
    doc.status = "In Process"
    doc.actual_start_date = now_datetime()
    doc.save()
    return doc

@frappe.whitelist()
def complete_work_order(work_order):
    doc = frappe.get_doc("Work Order", work_order)
    doc.status = "Completed"
    doc.actual_end_date = now_datetime()
    doc.save()
    
    # Create stock entry for finished goods
    create_production_entry(doc)
    return doc

def create_production_entry(work_order):
    stock_entry = frappe.get_doc({
        "doctype": "Stock Entry",
        "stock_entry_type": "Manufacture",
        "work_order": work_order.name,
        "to_warehouse": "Finished Goods - HC",
        "items": [{
            "item_code": work_order.production_item,
            "qty": work_order.qty,
            "basic_rate": 0,  # Will be calculated
            "t_warehouse": "Finished Goods - HC"
        }]
    })
    
    # Add raw material consumption
    for item in work_order.required_items:
        stock_entry.append("items", {
            "item_code": item.item_code,
            "qty": item.required_qty,
            "s_warehouse": "Stores - HC"
        })
    
    stock_entry.insert()
    stock_entry.submit()
    return stock_entry