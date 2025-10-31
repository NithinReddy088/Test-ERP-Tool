import frappe
from frappe import _

@frappe.whitelist()
def trace_serial(serial_no):
    """Trace serial number through production and quality records"""
    if not serial_no:
        frappe.throw(_("Serial number is required"))
    
    # Get serial number details
    serial_doc = frappe.get_doc("Serial No", serial_no)
    
    trace_data = {
        "serial_no": serial_no,
        "item_code": serial_doc.item_code,
        "status": serial_doc.status,
        "warehouse": serial_doc.warehouse,
        "purchase_history": [],
        "production_history": [],
        "quality_inspections": [],
        "delivery_history": []
    }
    
    # Get purchase history
    purchase_receipts = frappe.get_all("Purchase Receipt Item",
        filters={"serial_no": ["like", f"%{serial_no}%"]},
        fields=["parent", "supplier", "received_qty", "batch_no"])
    
    for pr in purchase_receipts:
        pr_doc = frappe.get_doc("Purchase Receipt", pr.parent)
        trace_data["purchase_history"].append({
            "document": pr.parent,
            "date": pr_doc.posting_date,
            "supplier": pr.supplier,
            "batch_no": pr.batch_no
        })
    
    # Get production history
    stock_entries = frappe.get_all("Stock Entry Detail",
        filters={"serial_no": ["like", f"%{serial_no}%"]},
        fields=["parent", "item_code", "qty", "s_warehouse", "t_warehouse"])
    
    for se in stock_entries:
        se_doc = frappe.get_doc("Stock Entry", se.parent)
        if se_doc.stock_entry_type == "Manufacture":
            trace_data["production_history"].append({
                "document": se.parent,
                "date": se_doc.posting_date,
                "work_order": se_doc.work_order,
                "from_warehouse": se.s_warehouse,
                "to_warehouse": se.t_warehouse
            })
    
    # Get quality inspections
    quality_inspections = frappe.get_all("Quality Inspection",
        filters={"serial_no": serial_no},
        fields=["name", "inspection_date", "status", "inspected_by"])
    
    trace_data["quality_inspections"] = quality_inspections
    
    # Get delivery history
    delivery_notes = frappe.get_all("Delivery Note Item",
        filters={"serial_no": ["like", f"%{serial_no}%"]},
        fields=["parent", "customer", "qty"])
    
    for dn in delivery_notes:
        dn_doc = frappe.get_doc("Delivery Note", dn.parent)
        trace_data["delivery_history"].append({
            "document": dn.parent,
            "date": dn_doc.posting_date,
            "customer": dn.customer
        })
    
    return trace_data

@frappe.whitelist()
def trace_batch(batch_no):
    """Trace batch number through production and quality records"""
    if not batch_no:
        frappe.throw(_("Batch number is required"))
    
    batch_doc = frappe.get_doc("Batch", batch_no)
    
    trace_data = {
        "batch_no": batch_no,
        "item_code": batch_doc.item,
        "manufacturing_date": batch_doc.manufacturing_date,
        "expiry_date": batch_doc.expiry_date,
        "supplier_batch": batch_doc.supplier_batch_id,
        "quality_inspections": [],
        "stock_movements": []
    }
    
    # Get quality inspections for this batch
    quality_inspections = frappe.get_all("Quality Inspection",
        filters={"batch_no": batch_no},
        fields=["name", "inspection_date", "status", "inspected_by", "reference_type", "reference_name"])
    
    trace_data["quality_inspections"] = quality_inspections
    
    # Get stock movements
    stock_ledger = frappe.get_all("Stock Ledger Entry",
        filters={"batch_no": batch_no},
        fields=["posting_date", "voucher_type", "voucher_no", "actual_qty", "warehouse"],
        order_by="posting_date")
    
    trace_data["stock_movements"] = stock_ledger
    
    return trace_data

@frappe.whitelist()
def get_traceability_report(item_code=None, from_date=None, to_date=None):
    """Generate traceability report for items"""
    filters = {}
    if item_code:
        filters["item_code"] = item_code
    if from_date and to_date:
        filters["posting_date"] = ["between", [from_date, to_date]]
    
    # Get all stock movements
    stock_entries = frappe.get_all("Stock Ledger Entry",
        filters=filters,
        fields=["item_code", "batch_no", "serial_no", "voucher_type", "voucher_no", 
                "posting_date", "actual_qty", "warehouse"])
    
    # Group by item and batch/serial
    traceability_data = {}
    for entry in stock_entries:
        key = f"{entry.item_code}_{entry.batch_no or entry.serial_no}"
        if key not in traceability_data:
            traceability_data[key] = {
                "item_code": entry.item_code,
                "batch_no": entry.batch_no,
                "serial_no": entry.serial_no,
                "movements": []
            }
        traceability_data[key]["movements"].append(entry)
    
    return list(traceability_data.values())