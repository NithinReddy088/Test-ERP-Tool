import frappe
from frappe.model.document import Document
from frappe.utils import now

class ProductionBatchTracking(Document):
    def validate(self):
        if not self.traceability_code:
            self.traceability_code = self.generate_traceability_code()
    
    def generate_traceability_code(self):
        return f"{self.item_code}-{self.batch_no}-{frappe.utils.now_datetime().strftime('%Y%m%d%H%M%S')}"
    
    def on_submit(self):
        self.update_batch_details()
    
    def update_batch_details(self):
        if self.batch_no:
            batch = frappe.get_doc("Batch", self.batch_no)
            batch.production_date = self.production_date
            batch.expiry_date = self.expiry_date
            batch.save()
    
    def get_full_traceability(self):
        traceability = {
            "batch_no": self.batch_no,
            "item": self.item_code,
            "production_date": self.production_date,
            "operator": self.operator,
            "raw_materials": []
        }
        
        for rm in self.raw_materials:
            traceability["raw_materials"].append({
                "item": rm.item_code,
                "batch": rm.batch_no,
                "supplier": rm.supplier
            })
        
        return traceability
