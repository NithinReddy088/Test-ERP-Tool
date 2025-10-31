import frappe
import unittest
from frappe.utils import now_datetime

class TestQualityInspection(unittest.TestCase):
    def setUp(self):
        # Create test item with inspection required
        if not frappe.db.exists("Item", "QC-TEST-001"):
            item = frappe.get_doc({
                "doctype": "Item",
                "item_code": "QC-TEST-001",
                "item_name": "QC Test Item",
                "item_group": "Medical Equipment",
                "stock_uom": "Nos",
                "is_stock_item": 1,
                "inspection_required_before_purchase": 1
            })
            item.insert()

    def test_quality_inspection_creation(self):
        """Test quality inspection creation and validation"""
        qi = frappe.get_doc({
            "doctype": "Quality Inspection",
            "inspection_type": "Incoming",
            "item_code": "QC-TEST-001",
            "sample_size": 5,
            "readings": [{
                "specification": "Dimension Check",
                "value": "Pass",
                "acceptance_criteria": "Within tolerance",
                "status": "Accepted"
            }]
        })
        qi.insert()
        
        # Validate status is set correctly
        self.assertEqual(qi.status, "Accepted")

    def test_quality_inspection_failure_ncr_creation(self):
        """Test NCR creation when quality inspection fails"""
        qi = frappe.get_doc({
            "doctype": "Quality Inspection",
            "inspection_type": "Incoming",
            "item_code": "QC-TEST-001",
            "sample_size": 5,
            "readings": [{
                "specification": "Dimension Check",
                "value": "Fail",
                "acceptance_criteria": "Within tolerance",
                "status": "Rejected"
            }]
        })
        qi.insert()
        qi.submit()
        
        # Check if NCR is created
        ncrs = frappe.get_all("NCR", filters={"quality_inspection": qi.name})
        self.assertTrue(len(ncrs) > 0)

    def test_auto_quality_inspection_from_purchase_receipt(self):
        """Test automatic quality inspection creation from purchase receipt"""
        # Create supplier
        if not frappe.db.exists("Supplier", "TEST-SUPPLIER"):
            supplier = frappe.get_doc({
                "doctype": "Supplier",
                "supplier_name": "Test Supplier",
                "supplier_type": "Company"
            })
            supplier.insert()
        
        # Create purchase receipt
        pr = frappe.get_doc({
            "doctype": "Purchase Receipt",
            "supplier": "TEST-SUPPLIER",
            "items": [{
                "item_code": "QC-TEST-001",
                "qty": 10,
                "rate": 100,
                "warehouse": "Stores - HC"
            }]
        })
        pr.insert()
        pr.submit()
        
        # Check if quality inspection is auto-created
        qis = frappe.get_all("Quality Inspection",
            filters={"reference_name": pr.name, "item_code": "QC-TEST-001"})
        self.assertTrue(len(qis) > 0)

    def test_traceability_link(self):
        """Test traceability linking between quality inspection and batch/serial"""
        # Create batch
        batch = frappe.get_doc({
            "doctype": "Batch",
            "batch_id": "BATCH-001",
            "item": "QC-TEST-001"
        })
        batch.insert()
        
        # Create quality inspection with batch
        qi = frappe.get_doc({
            "doctype": "Quality Inspection",
            "inspection_type": "Incoming",
            "item_code": "QC-TEST-001",
            "batch_no": "BATCH-001",
            "readings": [{
                "specification": "Visual Check",
                "value": "Pass",
                "acceptance_criteria": "No defects",
                "status": "Accepted"
            }]
        })
        qi.insert()
        qi.submit()
        
        # Verify traceability
        from healthcare_manufacturing.api.traceability import trace_batch
        trace_data = trace_batch("BATCH-001")
        
        self.assertEqual(trace_data["batch_no"], "BATCH-001")
        self.assertTrue(len(trace_data["quality_inspections"]) > 0)

    def tearDown(self):
        frappe.db.rollback()