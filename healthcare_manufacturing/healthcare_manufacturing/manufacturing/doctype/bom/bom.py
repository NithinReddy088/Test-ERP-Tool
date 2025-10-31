import frappe
from frappe.model.document import Document

class BOM(Document):
    def validate(self):
        self.validate_main_item()
        self.validate_bom_items()
        self.set_bom_material_details()

    def validate_main_item(self):
        if not frappe.db.exists("Item", self.item):
            frappe.throw(f"Item {self.item} does not exist")

    def validate_bom_items(self):
        if not self.items:
            frappe.throw("BOM must have at least one item")
        
        for item in self.items:
            if not frappe.db.exists("Item", item.item_code):
                frappe.throw(f"Item {item.item_code} does not exist")

    def set_bom_material_details(self):
        for item in self.items:
            item_doc = frappe.get_doc("Item", item.item_code)
            item.uom = item_doc.stock_uom
            item.rate = frappe.db.get_value("Item Price", 
                {"item_code": item.item_code}, "price_list_rate") or 0

    def on_submit(self):
        if self.is_default:
            self.set_as_default_bom()

    def set_as_default_bom(self):
        frappe.db.sql("""
            UPDATE `tabBOM` 
            SET is_default = 0 
            WHERE item = %s AND name != %s
        """, (self.item, self.name))

@frappe.whitelist()
def get_bom_items(bom):
    return frappe.get_all("BOM Item", 
        filters={"parent": bom},
        fields=["item_code", "qty", "rate", "amount"])