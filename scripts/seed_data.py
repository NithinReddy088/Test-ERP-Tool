#!/usr/bin/env python3
"""
Seed data script for Healthcare Manufacturing ERP
Creates sample data for testing and demonstration
"""

import frappe
from frappe.utils import now_datetime, add_days, random_string

def create_seed_data():
    """Create comprehensive seed data for the healthcare manufacturing system"""
    
    print("Creating seed data for Healthcare Manufacturing ERP...")
    
    # Create Items
    create_items()
    
    # Create Suppliers and Customers
    create_suppliers()
    create_customers()
    
    # Create Employees
    create_employees()
    
    # Create Accounts
    create_accounts()
    
    # Create BOMs
    create_boms()
    
    # Create Work Orders
    create_work_orders()
    
    # Create Quality Inspection Plans
    create_quality_inspection_plans()
    
    # Create Sample Quality Inspections
    create_quality_inspections()
    
    # Create KPIs
    create_kpis()
    
    print("Seed data creation completed!")

def create_items():
    """Create sample medical equipment items"""
    items = [
        {
            "item_code": "MED-DEV-001",
            "item_name": "Digital Blood Pressure Monitor",
            "item_group": "Medical Devices",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "has_serial_no": 1,
            "inspection_required_before_purchase": 1,
            "inspection_required_before_delivery": 1
        },
        {
            "item_code": "MED-DEV-002", 
            "item_name": "Pulse Oximeter",
            "item_group": "Medical Devices",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "has_batch_no": 1,
            "inspection_required_before_purchase": 1
        },
        {
            "item_code": "MED-DEV-003",
            "item_name": "Digital Thermometer",
            "item_group": "Medical Devices", 
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "has_serial_no": 1
        },
        {
            "item_code": "RAW-MAT-001",
            "item_name": "Medical Grade Plastic",
            "item_group": "Raw Materials",
            "stock_uom": "Kg",
            "is_stock_item": 1,
            "has_batch_no": 1
        },
        {
            "item_code": "RAW-MAT-002",
            "item_name": "Electronic Components",
            "item_group": "Raw Materials",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "has_batch_no": 1
        }
    ]
    
    for item_data in items:
        if not frappe.db.exists("Item", item_data["item_code"]):
            item = frappe.get_doc({
                "doctype": "Item",
                **item_data
            })
            item.insert()
            print(f"Created item: {item_data['item_code']}")

def create_suppliers():
    """Create sample suppliers"""
    suppliers = [
        {
            "supplier_name": "MedTech Components Ltd",
            "supplier_type": "Company",
            "country": "United States"
        },
        {
            "supplier_name": "Healthcare Materials Inc",
            "supplier_type": "Company", 
            "country": "Germany"
        },
        {
            "supplier_name": "Precision Electronics Co",
            "supplier_type": "Company",
            "country": "Japan"
        }
    ]
    
    for supplier_data in suppliers:
        if not frappe.db.exists("Supplier", supplier_data["supplier_name"]):
            supplier = frappe.get_doc({
                "doctype": "Supplier",
                **supplier_data
            })
            supplier.insert()
            print(f"Created supplier: {supplier_data['supplier_name']}")

def create_customers():
    """Create sample customers"""
    customers = [
        {
            "customer_name": "City General Hospital",
            "customer_type": "Company",
            "customer_group": "Healthcare"
        },
        {
            "customer_name": "Regional Medical Center", 
            "customer_type": "Company",
            "customer_group": "Healthcare"
        },
        {
            "customer_name": "Community Health Clinic",
            "customer_type": "Company",
            "customer_group": "Healthcare"
        }
    ]
    
    for customer_data in customers:
        if not frappe.db.exists("Customer", customer_data["customer_name"]):
            customer = frappe.get_doc({
                "doctype": "Customer",
                **customer_data
            })
            customer.insert()
            print(f"Created customer: {customer_data['customer_name']}")
    
    # Update customers with additional fields
    for customer_data in customers:
        customer_name = customer_data["customer_name"]
        if frappe.db.exists("Customer", customer_name):
            customer = frappe.get_doc("Customer", customer_name)
            customer.territory = "North America"
            customer.credit_limit = 100000
            customer.payment_terms = "Net 30"
            customer.save()
            print(f"Updated customer: {customer_name}")

def create_boms():
    """Create sample BOMs for medical devices"""
    boms = [
        {
            "item": "MED-DEV-001",
            "quantity": 1,
            "uom": "Nos",
            "is_active": 1,
            "is_default": 1,
            "items": [
                {"item_code": "RAW-MAT-001", "qty": 0.5, "uom": "Kg"},
                {"item_code": "RAW-MAT-002", "qty": 1, "uom": "Nos"}
            ],
            "operations": [
                {"operation": "Molding", "time_in_mins": 30, "workstation": "Molding Station"},
                {"operation": "Assembly", "time_in_mins": 45, "workstation": "Assembly Line"},
                {"operation": "Testing", "time_in_mins": 15, "workstation": "QC Station"}
            ]
        },
        {
            "item": "MED-DEV-002",
            "quantity": 1,
            "uom": "Nos", 
            "is_active": 1,
            "is_default": 1,
            "items": [
                {"item_code": "RAW-MAT-001", "qty": 0.2, "uom": "Kg"},
                {"item_code": "RAW-MAT-002", "qty": 1, "uom": "Nos"}
            ],
            "operations": [
                {"operation": "Assembly", "time_in_mins": 20, "workstation": "Assembly Line"},
                {"operation": "Calibration", "time_in_mins": 10, "workstation": "Calibration Station"}
            ]
        }
    ]
    
    for bom_data in boms:
        existing_bom = frappe.db.get_value("BOM", {"item": bom_data["item"], "is_default": 1})
        if not existing_bom:
            bom = frappe.get_doc({
                "doctype": "BOM",
                **bom_data
            })
            bom.insert()
            bom.submit()
            print(f"Created BOM for: {bom_data['item']}")

def create_work_orders():
    """Create sample work orders"""
    work_orders = [
        {
            "production_item": "MED-DEV-001",
            "qty": 50,
            "planned_start_date": now_datetime(),
            "planned_end_date": add_days(now_datetime(), 7),
            "status": "Not Started"
        },
        {
            "production_item": "MED-DEV-002", 
            "qty": 100,
            "planned_start_date": add_days(now_datetime(), 2),
            "planned_end_date": add_days(now_datetime(), 10),
            "status": "In Process"
        }
    ]
    
    for wo_data in work_orders:
        bom = frappe.db.get_value("BOM", {"item": wo_data["production_item"], "is_default": 1})
        if bom:
            wo = frappe.get_doc({
                "doctype": "Work Order",
                "bom_no": bom,
                **wo_data
            })
            wo.insert()
            print(f"Created work order for: {wo_data['production_item']}")

def create_quality_inspection_plans():
    """Create quality inspection templates"""
    templates = [
        {
            "item_code": "MED-DEV-001",
            "parameters": [
                {"specification": "Accuracy Test", "acceptance_criteria": "±3 mmHg", "value": "Pass"},
                {"specification": "Display Function", "acceptance_criteria": "Clear readable display", "value": "Pass"},
                {"specification": "Cuff Pressure", "acceptance_criteria": "0-300 mmHg", "value": "Pass"}
            ]
        },
        {
            "item_code": "MED-DEV-002",
            "parameters": [
                {"specification": "SpO2 Accuracy", "acceptance_criteria": "±2%", "value": "Pass"},
                {"specification": "Pulse Rate Accuracy", "acceptance_criteria": "±3 bpm", "value": "Pass"},
                {"specification": "Response Time", "acceptance_criteria": "<30 seconds", "value": "Pass"}
            ]
        }
    ]
    
    for template in templates:
        # Create quality inspection template (this would be a custom DocType)
        print(f"Quality inspection template for {template['item_code']} would be created here")

def create_employees():
    """Create sample employees"""
    employees = [
        {
            "employee_name": "John Smith",
            "department": "Manufacturing",
            "designation": "Production Manager",
            "date_of_joining": "2020-01-15",
            "company_email": "john.smith@healthcare-erp.com",
            "ctc": 75000
        },
        {
            "employee_name": "Sarah Johnson",
            "department": "Quality Control",
            "designation": "QC Manager", 
            "date_of_joining": "2019-03-10",
            "company_email": "sarah.johnson@healthcare-erp.com",
            "ctc": 70000
        },
        {
            "employee_name": "Mike Wilson",
            "department": "Finance",
            "designation": "Finance Manager",
            "date_of_joining": "2018-06-20",
            "company_email": "mike.wilson@healthcare-erp.com",
            "ctc": 80000
        },
        {
            "employee_name": "Lisa Chen",
            "department": "Sales",
            "designation": "Sales Manager",
            "date_of_joining": "2021-02-01",
            "company_email": "lisa.chen@healthcare-erp.com",
            "ctc": 65000
        }
    ]
    
    for emp_data in employees:
        if not frappe.db.exists("Employee", {"employee_name": emp_data["employee_name"]}):
            emp = frappe.get_doc({
                "doctype": "Employee",
                **emp_data
            })
            emp.insert()
            print(f"Created employee: {emp_data['employee_name']}")

def create_accounts():
    """Create sample chart of accounts"""
    accounts = [
        {
            "account_name": "Assets",
            "account_type": "Asset",
            "is_group": 1,
            "company": "Healthcare Manufacturing Corp"
        },
        {
            "account_name": "Cash",
            "account_type": "Asset",
            "parent_account": "Assets",
            "opening_balance": 250000,
            "company": "Healthcare Manufacturing Corp"
        },
        {
            "account_name": "Accounts Receivable",
            "account_type": "Asset",
            "parent_account": "Assets",
            "opening_balance": 180000,
            "company": "Healthcare Manufacturing Corp"
        },
        {
            "account_name": "Inventory",
            "account_type": "Asset",
            "parent_account": "Assets",
            "opening_balance": 320000,
            "company": "Healthcare Manufacturing Corp"
        },
        {
            "account_name": "Income",
            "account_type": "Income",
            "is_group": 1,
            "company": "Healthcare Manufacturing Corp"
        },
        {
            "account_name": "Sales Revenue",
            "account_type": "Income",
            "parent_account": "Income",
            "company": "Healthcare Manufacturing Corp"
        }
    ]
    
    for acc_data in accounts:
        if not frappe.db.exists("Account", {"account_name": acc_data["account_name"]}):
            acc = frappe.get_doc({
                "doctype": "Account",
                **acc_data
            })
            acc.insert()
            print(f"Created account: {acc_data['account_name']}")

def create_kpis():
    """Create sample KPIs"""
    kpis = [
        {
            "kpi_name": "Production Efficiency",
            "kpi_type": "Production",
            "module": "Manufacturing",
            "frequency": "Daily",
            "target_value": 85,
            "calculation_method": "Percentage",
            "chart_type": "Gauge",
            "color": "#2196F3"
        },
        {
            "kpi_name": "Quality Pass Rate",
            "kpi_type": "Quality",
            "module": "Quality Control",
            "frequency": "Daily",
            "target_value": 98,
            "calculation_method": "Percentage",
            "chart_type": "Line",
            "color": "#4CAF50"
        },
        {
            "kpi_name": "On-Time Delivery",
            "kpi_type": "Sales",
            "module": "Sales",
            "frequency": "Weekly",
            "target_value": 95,
            "calculation_method": "Percentage",
            "chart_type": "Bar",
            "color": "#FF9800"
        },
        {
            "kpi_name": "Inventory Turnover",
            "kpi_type": "Inventory",
            "module": "Inventory",
            "frequency": "Monthly",
            "target_value": 12,
            "calculation_method": "Count",
            "chart_type": "Number",
            "color": "#9C27B0"
        }
    ]
    
    for kpi_data in kpis:
        if not frappe.db.exists("KPI", kpi_data["kpi_name"]):
            kpi = frappe.get_doc({
                "doctype": "KPI",
                **kpi_data
            })
            kpi.insert()
            print(f"Created KPI: {kpi_data['kpi_name']}")

def create_quality_inspections():
    """Create sample quality inspection records"""
    inspections = [
        {
            "inspection_type": "Incoming",
            "item_code": "RAW-MAT-001",
            "batch_no": f"BATCH-{random_string(6)}",
            "sample_size": 5,
            "status": "Accepted",
            "readings": [
                {"specification": "Material Grade", "value": "Medical Grade", "status": "Accepted"},
                {"specification": "Color", "value": "White", "status": "Accepted"}
            ]
        },
        {
            "inspection_type": "In Process",
            "item_code": "MED-DEV-001", 
            "sample_size": 3,
            "status": "Accepted",
            "readings": [
                {"specification": "Assembly Check", "value": "Complete", "status": "Accepted"},
                {"specification": "Function Test", "value": "Pass", "status": "Accepted"}
            ]
        }
    ]
    
    for qi_data in inspections:
        qi = frappe.get_doc({
            "doctype": "Quality Inspection",
            **qi_data
        })
        qi.insert()
        qi.submit()
        print(f"Created quality inspection: {qi.name}")

if __name__ == "__main__":
    frappe.init(site="healthcare-erp.local")
    frappe.connect()
    create_seed_data()
    frappe.db.commit()