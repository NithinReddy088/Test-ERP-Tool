import frappe
from frappe.model.document import Document
from frappe.utils import getdate, add_days, add_months

class MaintenanceSchedule(Document):
    def validate(self):
        self.check_overdue()
    
    def check_overdue(self):
        if getdate(self.next_maintenance_date) < getdate():
            self.status = "Overdue"
    
    def on_submit(self):
        self.create_maintenance_task()
    
    def create_maintenance_task(self):
        task = frappe.get_doc({
            "doctype": "Task",
            "subject": f"Maintenance: {self.equipment_name}",
            "description": f"Scheduled maintenance for {self.equipment_name}",
            "exp_start_date": self.next_maintenance_date,
            "priority": self.priority,
            "assigned_to": self.assigned_to
        })
        task.insert()
    
    def complete_maintenance(self):
        self.status = "Completed"
        self.last_maintenance_date = getdate()
        self.calculate_next_maintenance_date()
        self.save()
    
    def calculate_next_maintenance_date(self):
        frequency_map = {
            "Daily": 1,
            "Weekly": 7,
            "Monthly": 30,
            "Quarterly": 90,
            "Half-Yearly": 180,
            "Yearly": 365
        }
        
        if self.frequency in frequency_map:
            days = frequency_map[self.frequency]
            self.next_maintenance_date = add_days(self.last_maintenance_date, days)
