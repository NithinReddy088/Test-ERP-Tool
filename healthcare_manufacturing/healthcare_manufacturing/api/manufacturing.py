import frappe
from frappe import _

@frappe.whitelist()
def create_work_order_from_sales_order(sales_order):
    """Create work orders from sales order"""
    so_doc = frappe.get_doc("Sales Order", sales_order)
    work_orders = []
    
    for item in so_doc.items:
        # Check if item has BOM
        bom = frappe.db.get_value("BOM", {"item": item.item_code, "is_active": 1, "is_default": 1})
        if bom:
            wo = frappe.get_doc({
                "doctype": "Work Order",
                "production_item": item.item_code,
                "bom_no": bom,
                "qty": item.qty,
                "sales_order": sales_order,
                "planned_start_date": so_doc.delivery_date
            })
            wo.insert()
            work_orders.append(wo.name)
    
    return work_orders

@frappe.whitelist()
def get_work_orders(status=None, production_item=None):
    """Get work orders with filters"""
    filters = {}
    if status:
        filters["status"] = status
    if production_item:
        filters["production_item"] = production_item
    
    return frappe.get_all("Work Order", 
        filters=filters,
        fields=["name", "production_item", "qty", "status", "planned_start_date", "planned_end_date"])

@frappe.whitelist()
def update_work_order_status(work_order, status):
    """Update work order status"""
    doc = frappe.get_doc("Work Order", work_order)
    doc.status = status
    doc.save()
    return {"status": "success", "message": f"Work Order {work_order} updated to {status}"}

@frappe.whitelist()
def get_production_schedule():
    """Get production schedule for Gantt view"""
    work_orders = frappe.get_all("Work Order",
        filters={"status": ["in", ["Not Started", "In Process"]]},
        fields=["name", "production_item", "planned_start_date", "planned_end_date", "status"])
    
    schedule = []
    for wo in work_orders:
        schedule.append({
            "id": wo.name,
            "name": f"{wo.production_item} - {wo.name}",
            "start": wo.planned_start_date,
            "end": wo.planned_end_date,
            "progress": 50 if wo.status == "In Process" else 0
        })
    
    return schedule