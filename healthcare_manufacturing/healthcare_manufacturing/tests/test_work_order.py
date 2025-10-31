import frappe
import unittest
from frappe.utils import now_datetime, add_days

class TestWorkOrder(unittest.TestCase):
    def setUp(self):
        # Create test item
        if not frappe.db.exists("Item", "TEST-ITEM-001"):
            item = frappe.get_doc({
                "doctype": "Item",
                "item_code": "TEST-ITEM-001",
                "item_name": "Test Medical Device",
                "item_group": "Medical Equipment",
                "stock_uom": "Nos",
                "is_stock_item": 1
            })
            item.insert()
        
        # Create test BOM
        if not frappe.db.exists("BOM", {"item": "TEST-ITEM-001"}):
            bom = frappe.get_doc({
                "doctype": "BOM",
                "item": "TEST-ITEM-001",
                "quantity": 1,
                "uom": "Nos",
                "is_active": 1,
                "is_default": 1,
                "items": [{
                    "item_code": "RAW-MAT-001",
                    "qty": 2,
                    "uom": "Kg"
                }]
            })
            bom.insert()
            bom.submit()
            self.bom_name = bom.name

    def test_work_order_creation(self):
        """Test work order creation with BOM validation"""
        work_order = frappe.get_doc({
            "doctype": "Work Order",
            "production_item": "TEST-ITEM-001",
            "bom_no": self.bom_name,
            "qty": 10,
            "planned_start_date": now_datetime(),
            "planned_end_date": add_days(now_datetime(), 5)
        })
        work_order.insert()
        
        # Validate required items are set
        self.assertTrue(len(work_order.required_items) > 0)
        self.assertEqual(work_order.required_items[0].item_code, "RAW-MAT-001")
        self.assertEqual(work_order.required_items[0].required_qty, 20)  # 2 * 10

    def test_work_order_material_reservation(self):
        """Test material reservation on work order submission"""
        # Create stock entry for raw material
        stock_entry = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Receipt",
            "to_warehouse": "Stores - HC",
            "items": [{
                "item_code": "RAW-MAT-001",
                "qty": 100,
                "basic_rate": 10,
                "t_warehouse": "Stores - HC"
            }]
        })
        stock_entry.insert()
        stock_entry.submit()
        
        # Create and submit work order
        work_order = frappe.get_doc({
            "doctype": "Work Order",
            "production_item": "TEST-ITEM-001",
            "bom_no": self.bom_name,
            "qty": 5
        })
        work_order.insert()
        work_order.submit()
        
        # Check if materials are reserved
        reservations = frappe.get_all("Stock Reservation",
            filters={"voucher_no": work_order.name})
        self.assertTrue(len(reservations) > 0)

    def test_production_completion_flow(self):
        """Test complete production flow from work order to finished goods"""
        from healthcare_manufacturing.manufacturing.doctype.work_order.work_order import complete_work_order
        
        # Create work order
        work_order = frappe.get_doc({
            "doctype": "Work Order",
            "production_item": "TEST-ITEM-001",
            "bom_no": self.bom_name,
            "qty": 1
        })
        work_order.insert()
        work_order.submit()
        
        # Complete work order
        completed_wo = complete_work_order(work_order.name)
        
        # Verify status change
        self.assertEqual(completed_wo.status, "Completed")
        self.assertIsNotNone(completed_wo.actual_end_date)
        
        # Verify stock entry creation
        stock_entries = frappe.get_all("Stock Entry",
            filters={"work_order": work_order.name})
        self.assertTrue(len(stock_entries) > 0)

    def tearDown(self):
        # Clean up test data
        frappe.db.rollback()