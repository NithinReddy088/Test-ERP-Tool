import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, add_days

class ProductionPlan(Document):
    def validate(self):
        self.validate_items()
        self.calculate_material_requirements()

    def validate_items(self):
        if not self.po_items:
            frappe.throw("Production Plan must have at least one item")

    def calculate_material_requirements(self):
        """Calculate material requirements based on BOMs"""
        self.mr_items = []
        
        for item in self.po_items:
            bom = frappe.db.get_value("BOM", {"item": item.item_code, "is_default": 1})
            if bom:
                bom_items = frappe.get_all("BOM Item",
                    filters={"parent": bom},
                    fields=["item_code", "qty"])
                
                for bom_item in bom_items:
                    required_qty = bom_item.qty * item.planned_qty
                    
                    # Check if item already exists in material requirements
                    existing_item = None
                    for mr_item in self.mr_items:
                        if mr_item.item_code == bom_item.item_code:
                            existing_item = mr_item
                            break
                    
                    if existing_item:
                        existing_item.quantity += required_qty
                    else:
                        self.append("mr_items", {
                            "item_code": bom_item.item_code,
                            "quantity": required_qty,
                            "warehouse": "Stores - HC"
                        })

    def on_submit(self):
        self.create_work_orders()

    def create_work_orders(self):
        """Create work orders for all items in the production plan"""
        for item in self.po_items:
            bom = frappe.db.get_value("BOM", {"item": item.item_code, "is_default": 1})
            if bom:
                work_order = frappe.get_doc({
                    "doctype": "Work Order",
                    "production_item": item.item_code,
                    "bom_no": bom,
                    "qty": item.planned_qty,
                    "production_plan": self.name,
                    "planned_start_date": item.planned_start_date or self.posting_date,
                    "planned_end_date": add_days(item.planned_start_date or self.posting_date, 7)
                })
                work_order.insert()
                frappe.msgprint(f"Work Order {work_order.name} created for {item.item_code}")

@frappe.whitelist()
def create_production_plan_from_sales_order(doc, method):
    """Auto-create production plan from sales order"""
    if doc.doctype == "Sales Order" and doc.docstatus == 1:
        # Check if production plan already exists
        existing_plan = frappe.db.get_value("Production Plan", 
            {"sales_order": doc.name})
        
        if not existing_plan:
            production_plan = frappe.get_doc({
                "doctype": "Production Plan",
                "company": doc.company,
                "posting_date": now_datetime(),
                "sales_order": doc.name,
                "po_items": []
            })
            
            for item in doc.items:
                # Check if item has BOM
                bom = frappe.db.get_value("BOM", {"item": item.item_code, "is_default": 1})
                if bom:
                    production_plan.append("po_items", {
                        "item_code": item.item_code,
                        "bom_no": bom,
                        "planned_qty": item.qty,
                        "planned_start_date": doc.delivery_date,
                        "sales_order": doc.name,
                        "sales_order_item": item.name
                    })
            
            if production_plan.po_items:
                production_plan.insert()
                frappe.msgprint(f"Production Plan {production_plan.name} created from Sales Order {doc.name}")

@frappe.whitelist()
def update_production_schedules():
    """Scheduled task to update production schedules"""
    # Get all open work orders
    work_orders = frappe.get_all("Work Order",
        filters={"status": ["in", ["Not Started", "In Process"]]},
        fields=["name", "planned_start_date", "planned_end_date"])
    
    for wo in work_orders:
        # Update schedules based on capacity and dependencies
        # This is a simplified version - real implementation would be more complex
        pass