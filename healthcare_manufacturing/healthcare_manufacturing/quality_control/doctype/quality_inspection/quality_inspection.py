import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

class QualityInspection(Document):
    def validate(self):
        self.validate_readings()
        self.set_inspection_status()

    def validate_readings(self):
        if not self.readings:
            # Get inspection plan readings
            inspection_plan = self.get_inspection_plan()
            if inspection_plan:
                for reading in inspection_plan.quality_inspection_template:
                    self.append("readings", {
                        "specification": reading.specification,
                        "value": reading.value,
                        "acceptance_criteria": reading.acceptance_criteria,
                        "status": "Accepted"
                    })

    def get_inspection_plan(self):
        if self.reference_type == "Purchase Receipt":
            return frappe.db.get_value("Item", self.item_code, "quality_inspection_template")
        return None

    def set_inspection_status(self):
        if self.readings:
            failed_readings = [r for r in self.readings if r.status == "Rejected"]
            if failed_readings:
                self.status = "Rejected"
            else:
                self.status = "Accepted"

    def on_submit(self):
        self.inspected_by = frappe.session.user
        self.inspection_date = now_datetime()
        
        if self.status == "Rejected":
            self.create_ncr()
        
        self.update_reference_document()

    def create_ncr(self):
        ncr = frappe.get_doc({
            "doctype": "NCR",
            "quality_inspection": self.name,
            "item_code": self.item_code,
            "batch_no": self.batch_no,
            "serial_no": self.serial_no,
            "non_conformance_type": "Quality Failure",
            "description": f"Quality inspection failed for {self.item_code}",
            "status": "Open"
        })
        ncr.insert()
        frappe.msgprint(f"NCR {ncr.name} created for failed inspection")

    def update_reference_document(self):
        if self.reference_type and self.reference_name:
            ref_doc = frappe.get_doc(self.reference_type, self.reference_name)
            ref_doc.add_comment("Comment", f"Quality Inspection {self.name}: {self.status}")

@frappe.whitelist()
def create_quality_inspection(doc, method):
    """Auto-create quality inspection for Purchase Receipt"""
    if doc.doctype == "Purchase Receipt":
        for item in doc.items:
            item_doc = frappe.get_doc("Item", item.item_code)
            if item_doc.inspection_required_before_purchase:
                qi = frappe.get_doc({
                    "doctype": "Quality Inspection",
                    "inspection_type": "Incoming",
                    "reference_type": "Purchase Receipt",
                    "reference_name": doc.name,
                    "item_code": item.item_code,
                    "batch_no": item.batch_no,
                    "sample_size": 1
                })
                qi.insert()

@frappe.whitelist()
def get_quality_inspection_template(item_code):
    return frappe.get_all("Quality Inspection Parameter",
        filters={"parent": item_code},
        fields=["specification", "value", "acceptance_criteria"])