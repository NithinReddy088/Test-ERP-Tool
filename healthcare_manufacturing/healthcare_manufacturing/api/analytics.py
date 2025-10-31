import frappe
from frappe import _
from frappe.utils import flt

@frappe.whitelist()
def get_production_metrics():
    """Get production dashboard metrics"""
    
    # Work order metrics
    open_work_orders = frappe.db.count("Work Order", 
        {"status": ["in", ["Not Started", "In Process"]]})
    
    completed_today = frappe.db.count("Work Order", {
        "status": "Completed",
        "actual_end_date": [">=", frappe.utils.today()]
    })
    
    overdue_orders = frappe.db.count("Work Order", {
        "status": ["in", ["Not Started", "In Process"]],
        "planned_end_date": ["<", frappe.utils.today()]
    })
    
    # Calculate OEE (Overall Equipment Effectiveness)
    oee_percentage = calculate_oee()
    
    # Production trend data
    production_trend = get_production_trend_data()
    
    # Work order status distribution
    work_order_status = get_work_order_status_distribution()
    
    return {
        "open_work_orders": open_work_orders,
        "completed_today": completed_today,
        "overdue_orders": overdue_orders,
        "oee_percentage": oee_percentage,
        "production_trend": production_trend,
        "work_order_status": work_order_status
    }

@frappe.whitelist()
def get_quality_metrics():
    """Get quality control dashboard metrics"""
    
    # Quality inspection metrics
    pending_inspections = frappe.db.count("Quality Inspection", 
        {"status": "Draft"})
    
    open_ncrs = frappe.db.count("NCR", 
        {"status": "Open"})
    
    # Calculate pass rate for current month
    pass_rate = calculate_quality_pass_rate()
    
    capa_actions = frappe.db.count("CAPA", 
        {"status": ["in", ["Open", "In Progress"]]})
    
    # Quality trend data
    quality_trend = get_quality_trend_data()
    
    # Defect categories
    defect_categories = get_defect_categories_data()
    
    return {
        "pending_inspections": pending_inspections,
        "open_ncrs": open_ncrs,
        "pass_rate": pass_rate,
        "capa_actions": capa_actions,
        "quality_trend": quality_trend,
        "defect_categories": defect_categories
    }

@frappe.whitelist()
def get_finance_metrics():
    """Get finance dashboard metrics"""
    
    # Revenue metrics
    monthly_revenue = get_monthly_revenue()
    
    # Account balances
    accounts_receivable = frappe.db.get_value("Account", 
        {"account_name": "Accounts Receivable"}, "balance") or 0
    
    accounts_payable = frappe.db.get_value("Account", 
        {"account_name": "Accounts Payable"}, "balance") or 0
    
    # Calculate profit margin
    profit_margin = calculate_profit_margin()
    
    # Revenue trend data
    revenue_trend = get_revenue_trend_data()
    
    return {
        "monthly_revenue": monthly_revenue,
        "accounts_receivable": accounts_receivable,
        "accounts_payable": accounts_payable,
        "profit_margin": profit_margin,
        "revenue_trend": revenue_trend
    }

@frappe.whitelist()
def get_inventory_metrics():
    """Get inventory dashboard metrics"""
    
    # Stock levels
    total_items = frappe.db.count("Item", {"is_stock_item": 1})
    
    low_stock_items = frappe.db.sql("""
        SELECT COUNT(*) 
        FROM `tabItem` i
        LEFT JOIN `tabBin` b ON i.name = b.item_code
        WHERE i.is_stock_item = 1 
        AND (b.actual_qty <= i.reorder_level OR b.actual_qty IS NULL)
    """)[0][0] or 0
    
    # Inventory value
    inventory_value = calculate_inventory_value()
    
    # Inventory turnover
    inventory_turnover = calculate_inventory_turnover()
    
    return {
        "total_items": total_items,
        "low_stock_items": low_stock_items,
        "inventory_value": inventory_value,
        "inventory_turnover": inventory_turnover
    }

def calculate_oee():
    """Calculate Overall Equipment Effectiveness"""
    # OEE = Availability × Performance × Quality
    # This is a simplified calculation
    
    # Availability: Planned production time vs actual production time
    availability = 85  # Mock value
    
    # Performance: Actual production rate vs ideal production rate  
    performance = 90  # Mock value
    
    # Quality: Good units produced vs total units produced
    quality = 96  # Mock value
    
    oee = (availability * performance * quality) / 10000
    return round(oee, 1)

def calculate_quality_pass_rate():
    """Calculate quality inspection pass rate for current month"""
    from frappe.utils import get_first_day, get_last_day, today
    
    first_day = get_first_day(today())
    last_day = get_last_day(today())
    
    total_inspections = frappe.db.count("Quality Inspection", {
        "inspection_date": ["between", [first_day, last_day]],
        "status": ["in", ["Accepted", "Rejected"]]
    })
    
    passed_inspections = frappe.db.count("Quality Inspection", {
        "inspection_date": ["between", [first_day, last_day]],
        "status": "Accepted"
    })
    
    if total_inspections > 0:
        return round((passed_inspections / total_inspections) * 100, 1)
    
    return 0

def get_monthly_revenue():
    """Get current month revenue"""
    from frappe.utils import get_first_day, get_last_day, today
    
    first_day = get_first_day(today())
    last_day = get_last_day(today())
    
    revenue = frappe.db.sql("""
        SELECT SUM(grand_total)
        FROM `tabSales Invoice`
        WHERE posting_date BETWEEN %s AND %s
        AND docstatus = 1
    """, (first_day, last_day))[0][0] or 0
    
    return flt(revenue)

def calculate_profit_margin():
    """Calculate profit margin percentage"""
    # This would need cost of goods sold data
    # For now, return a mock value
    return 18.5

def calculate_inventory_value():
    """Calculate total inventory value"""
    inventory_value = frappe.db.sql("""
        SELECT SUM(b.actual_qty * b.valuation_rate)
        FROM `tabBin` b
        WHERE b.actual_qty > 0
    """)[0][0] or 0
    
    return flt(inventory_value)

def calculate_inventory_turnover():
    """Calculate inventory turnover ratio"""
    # Inventory Turnover = Cost of Goods Sold / Average Inventory
    # For now, return a mock value
    return 8.5

def get_production_trend_data():
    """Get production trend data for charts"""
    # Mock data for demonstration
    return {
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "datasets": [{
            "name": "Units Produced",
            "values": [12, 15, 8, 20, 18, 10, 14]
        }]
    }

def get_work_order_status_distribution():
    """Get work order status distribution"""
    statuses = frappe.db.sql("""
        SELECT status, COUNT(*) as count
        FROM `tabWork Order`
        GROUP BY status
    """, as_dict=True)
    
    labels = [s.status for s in statuses]
    values = [s.count for s in statuses]
    
    return {
        "labels": labels,
        "datasets": [{"values": values}]
    }

def get_quality_trend_data():
    """Get quality trend data for charts"""
    # Mock data for demonstration
    return {
        "labels": ["Week 1", "Week 2", "Week 3", "Week 4"],
        "datasets": [{
            "name": "Pass Rate %",
            "values": [95, 97, 94, 98]
        }]
    }

def get_defect_categories_data():
    """Get defect categories data"""
    # Mock data for demonstration
    return {
        "labels": ["Dimensional", "Visual", "Functional", "Other"],
        "datasets": [{"values": [3, 2, 1, 1]}]
    }

def get_revenue_trend_data():
    """Get revenue trend data for charts"""
    # Mock data for demonstration
    return {
        "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "datasets": [{
            "name": "Revenue",
            "values": [120000, 135000, 148000, 162000, 155000, 170000]
        }]
    }

@frappe.whitelist()
def get_executive_summary():
    """Get executive summary for top management"""
    
    summary = {
        "production": {
            "total_work_orders": frappe.db.count("Work Order"),
            "completion_rate": 85,
            "oee": calculate_oee()
        },
        "quality": {
            "pass_rate": calculate_quality_pass_rate(),
            "open_ncrs": frappe.db.count("NCR", {"status": "Open"}),
            "customer_complaints": 2  # Mock value
        },
        "finance": {
            "monthly_revenue": get_monthly_revenue(),
            "profit_margin": calculate_profit_margin(),
            "cash_flow": "Positive"  # Mock value
        },
        "inventory": {
            "inventory_value": calculate_inventory_value(),
            "turnover_ratio": calculate_inventory_turnover(),
            "stock_outs": 3  # Mock value
        }
    }
    
    return summary