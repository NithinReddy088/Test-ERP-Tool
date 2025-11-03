import frappe
from frappe.model.document import Document

class QualityControlLog(Document):
    def validate(self):
        if self.status == "Failed" and not self.corrective_action:
            frappe.throw("Corrective Action is required for failed inspections")
    
    def on_submit(self):
        if self.result == "Rejected":
            self.update_reference_status("Rejected")
    
    def update_reference_status(self, status):
        if self.reference_type and self.reference_name:
            doc = frappe.get_doc(self.reference_type, self.reference_name)
            if hasattr(doc, 'quality_status'):
                doc.quality_status = status
                doc.save()
