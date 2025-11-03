import frappe
from frappe.model.document import Document
from frappe.utils import getdate, add_days

class EquipmentComplianceCertificate(Document):
    def validate(self):
        if getdate(self.expiry_date) <= getdate(self.issue_date):
            frappe.throw("Expiry Date must be after Issue Date")
        
        self.update_status()
    
    def update_status(self):
        today = getdate()
        expiry = getdate(self.expiry_date)
        
        if expiry < today:
            self.status = "Expired"
        elif expiry <= add_days(today, 30):
            self.status = "Pending Renewal"
        else:
            self.status = "Valid"
