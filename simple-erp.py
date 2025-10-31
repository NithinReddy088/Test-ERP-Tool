#!/usr/bin/env python3
"""
Simple Healthcare Manufacturing ERP Demo - No Dependencies
"""

import http.server
import socketserver
import json
import urllib.parse
from datetime import datetime

PORT = 5000

class ERPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_dashboard()
        elif self.path == '/api/work-orders':
            self.send_json(work_orders)
        elif self.path == '/api/items':
            self.send_json(items)
        elif self.path == '/api/employees':
            self.send_json(employees)
        elif self.path == '/api/customers':
            self.send_json(customers)
        elif self.path == '/api/accounts':
            self.send_json(accounts)
        elif self.path == '/api/kpis':
            self.send_json(kpis)
        elif self.path == '/dashboard/production':
            self.send_production_dashboard()
        elif self.path == '/dashboard/quality':
            self.send_quality_dashboard()
        elif self.path == '/dashboard/finance':
            self.send_finance_dashboard()
        elif self.path.startswith('/api/trace/'):
            self.send_trace_data()
        else:
            self.send_404()
    
    def send_dashboard(self):
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Healthcare Manufacturing ERP</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .header {{ background: #2196F3; color: white; padding: 20px; border-radius: 5px; }}
        .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .stats {{ display: flex; gap: 20px; }}
        .stat {{ flex: 1; text-align: center; }}
        .stat h3 {{ margin: 0; color: #2196F3; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f2f2f2; }}
        .api-link {{ background: #4CAF50; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px; margin: 5px; display: inline-block; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏥 Healthcare Manufacturing ERP System</h1>
        <p>Production-ready ERP for Healthcare Equipment Manufacturing & Distribution</p>
    </div>
    
    <div class="stats">
        <div class="card stat">
            <h3>{len(work_orders)}</h3>
            <p>Active Work Orders</p>
        </div>
        <div class="card stat">
            <h3>{len(items)}</h3>
            <p>Items in Catalog</p>
        </div>
        <div class="card stat">
            <h3>{len(kpis)}</h3>
            <p>KPI Metrics</p>
        </div>
    </div>

    <div class="card">
        <h2>Role-Based Dashboards</h2>
        <a href="/dashboard/production" class="api-link">Production Manager Dashboard</a>
        <a href="/dashboard/quality" class="api-link">Quality Control Dashboard</a>
        <a href="/dashboard/finance" class="api-link">Finance Dashboard</a>
    </div>

    <div class="card">
        <h2>API Endpoints</h2>
        <a href="/api/work-orders" class="api-link">GET /api/work-orders</a>
        <a href="/api/items" class="api-link">GET /api/items</a>
        <a href="/api/employees" class="api-link">GET /api/employees</a>
        <a href="/api/customers" class="api-link">GET /api/customers</a>
        <a href="/api/accounts" class="api-link">GET /api/accounts</a>
        <a href="/api/kpis" class="api-link">GET /api/kpis</a>
        <a href="/api/trace/serial/SER001" class="api-link">GET /api/trace/serial/SER001</a>
        <a href="/api/trace/batch/BATCH001" class="api-link">GET /api/trace/batch/BATCH001</a>
    </div>

    <div class="card">
        <h2>Work Orders</h2>
        <table>
            <tr><th>Work Order</th><th>Item</th><th>Qty</th><th>Status</th><th>Start Date</th></tr>
            {''.join([f'<tr><td>{wo["name"]}</td><td>{wo["production_item"]}</td><td>{wo["qty"]}</td><td>{wo["status"]}</td><td>{wo["planned_start_date"]}</td></tr>' for wo in work_orders])}
        </table>
    </div>

    <div class="card">
        <h2>Inventory</h2>
        <table>
            <tr><th>Item Code</th><th>Item Name</th><th>Stock Qty</th></tr>
            {''.join([f'<tr><td>{item["item_code"]}</td><td>{item["item_name"]}</td><td>{item["stock_qty"]}</td></tr>' for item in items])}
        </table>
    </div>
</body>
</html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def send_trace_data(self):
        if 'serial' in self.path:
            data = {
                "serial_no": "SER001",
                "item_code": "MED-DEV-001",
                "status": "In Stock",
                "production_history": [{"work_order": "WO-2024-001", "date": "2024-10-25"}],
                "quality_inspections": [{"inspection": "QI-2024-001", "status": "Accepted"}]
            }
        else:
            data = {
                "batch_no": "BATCH001",
                "item_code": "RAW-MAT-001",
                "manufacturing_date": "2024-10-20",
                "quality_inspections": [{"inspection": "QI-2024-001", "status": "Accepted"}]
            }
        self.send_json(data)
    
    def send_production_dashboard(self):
        dashboard_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Production Manager Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .dashboard-header {{ background: #2196F3; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .metrics {{ display: flex; gap: 20px; margin-bottom: 20px; }}
        .metric {{ background: white; padding: 20px; border-radius: 5px; flex: 1; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .metric h3 {{ margin: 0; font-size: 2em; color: #2196F3; }}
        .chart-container {{ background: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .back-link {{ background: #4CAF50; color: white; padding: 10px 15px; text-decoration: none; border-radius: 3px; }}
    </style>
</head>
<body>
    <div class="dashboard-header">
        <h1>🏭 Production Manager Dashboard</h1>
        <p>Real-time production metrics and work order management</p>
    </div>
    
    <a href="/" class="back-link">← Back to Main Dashboard</a>
    
    <div class="metrics">
        <div class="metric">
            <h3>{len([wo for wo in work_orders if wo['status'] in ['Not Started', 'In Process']])}</h3>
            <p>Open Work Orders</p>
        </div>
        <div class="metric">
            <h3>{len([wo for wo in work_orders if wo['status'] == 'Completed'])}</h3>
            <p>Completed Orders</p>
        </div>
        <div class="metric">
            <h3>85%</h3>
            <p>OEE This Month</p>
        </div>
        <div class="metric">
            <h3>2</h3>
            <p>Overdue Orders</p>
        </div>
    </div>
    
    <div class="chart-container">
        <h3>Work Order Status Distribution</h3>
        <p>In Process: {len([wo for wo in work_orders if wo['status'] == 'In Process'])} orders</p>
        <p>Not Started: {len([wo for wo in work_orders if wo['status'] == 'Not Started'])} orders</p>
        <p>Completed: {len([wo for wo in work_orders if wo['status'] == 'Completed'])} orders</p>
    </div>
    
    <div class="chart-container">
        <h3>Production Schedule (Gantt View)</h3>
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background: #f2f2f2;"><th style="padding: 10px; border: 1px solid #ddd;">Work Order</th><th style="padding: 10px; border: 1px solid #ddd;">Item</th><th style="padding: 10px; border: 1px solid #ddd;">Status</th><th style="padding: 10px; border: 1px solid #ddd;">Timeline</th></tr>
            {''.join([f'<tr><td style="padding: 10px; border: 1px solid #ddd;">{wo["name"]}</td><td style="padding: 10px; border: 1px solid #ddd;">{wo["production_item"]}</td><td style="padding: 10px; border: 1px solid #ddd;">{wo["status"]}</td><td style="padding: 10px; border: 1px solid #ddd;">{wo["planned_start_date"]}</td></tr>' for wo in work_orders])}
        </table>
    </div>
</body>
</html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(dashboard_html.encode())
    
    def send_quality_dashboard(self):
        dashboard_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Quality Control Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .dashboard-header { background: #e91e63; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        .metrics { display: flex; gap: 20px; margin-bottom: 20px; }
        .metric { background: white; padding: 20px; border-radius: 5px; flex: 1; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric h3 { margin: 0; font-size: 2em; color: #e91e63; }
        .chart-container { background: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        .back-link { background: #4CAF50; color: white; padding: 10px 15px; text-decoration: none; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="dashboard-header">
        <h1>🔍 Quality Control Dashboard</h1>
        <p>Quality metrics, inspections, and compliance tracking</p>
    </div>
    
    <a href="/" class="back-link">← Back to Main Dashboard</a>
    
    <div class="metrics">
        <div class="metric">
            <h3>5</h3>
            <p>Pending Inspections</p>
        </div>
        <div class="metric">
            <h3>2</h3>
            <p>Open NCRs</p>
        </div>
        <div class="metric">
            <h3>96%</h3>
            <p>Pass Rate (This Month)</p>
        </div>
        <div class="metric">
            <h3>3</h3>
            <p>CAPA Actions</p>
        </div>
    </div>
    
    <div class="chart-container">
        <h3>Quality Inspection Results</h3>
        <p>✅ Passed: 48 inspections</p>
        <p>❌ Failed: 2 inspections</p>
        <p>⏳ Pending: 5 inspections</p>
    </div>
    
    <div class="chart-container">
        <h3>Non-Conformance Trends</h3>
        <p>Dimensional Issues: 1 NCR</p>
        <p>Visual Defects: 1 NCR</p>
        <p>Functional Issues: 0 NCRs</p>
    </div>
</body>
</html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(dashboard_html.encode())
    
    def send_finance_dashboard(self):
        dashboard_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Finance Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .dashboard-header { background: #4caf50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        .metrics { display: flex; gap: 20px; margin-bottom: 20px; }
        .metric { background: white; padding: 20px; border-radius: 5px; flex: 1; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric h3 { margin: 0; font-size: 2em; color: #4caf50; }
        .chart-container { background: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        .back-link { background: #4CAF50; color: white; padding: 10px 15px; text-decoration: none; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="dashboard-header">
        <h1>💰 Finance Dashboard</h1>
        <p>Financial metrics, P&L, and accounts management</p>
    </div>
    
    <a href="/" class="back-link">← Back to Main Dashboard</a>
    
    <div class="metrics">
        <div class="metric">
            <h3>$850K</h3>
            <p>Monthly Revenue</p>
        </div>
        <div class="metric">
            <h3>$180K</h3>
            <p>Accounts Receivable</p>
        </div>
        <div class="metric">
            <h3>$120K</h3>
            <p>Accounts Payable</p>
        </div>
        <div class="metric">
            <h3>18%</h3>
            <p>Profit Margin</p>
        </div>
    </div>
    
    <div class="chart-container">
        <h3>Account Balances</h3>
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background: #f2f2f2;"><th style="padding: 10px; border: 1px solid #ddd;">Account</th><th style="padding: 10px; border: 1px solid #ddd;">Type</th><th style="padding: 10px; border: 1px solid #ddd;">Balance</th></tr>
            <tr><td style="padding: 10px; border: 1px solid #ddd;">Cash</td><td style="padding: 10px; border: 1px solid #ddd;">Asset</td><td style="padding: 10px; border: 1px solid #ddd;">$250,000</td></tr>
            <tr><td style="padding: 10px; border: 1px solid #ddd;">Accounts Receivable</td><td style="padding: 10px; border: 1px solid #ddd;">Asset</td><td style="padding: 10px; border: 1px solid #ddd;">$180,000</td></tr>
            <tr><td style="padding: 10px; border: 1px solid #ddd;">Inventory</td><td style="padding: 10px; border: 1px solid #ddd;">Asset</td><td style="padding: 10px; border: 1px solid #ddd;">$320,000</td></tr>
            <tr><td style="padding: 10px; border: 1px solid #ddd;">Sales Revenue</td><td style="padding: 10px; border: 1px solid #ddd;">Income</td><td style="padding: 10px; border: 1px solid #ddd;">$850,000</td></tr>
        </table>
    </div>
</body>
</html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(dashboard_html.encode())
    
    def send_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h1>404 Not Found</h1>')

# Sample data
work_orders = [
    {"name": "WO-2024-001", "production_item": "MED-DEV-001", "qty": 10, "status": "In Process", "planned_start_date": "2024-11-01"},
    {"name": "WO-2024-002", "production_item": "MED-DEV-002", "qty": 25, "status": "Not Started", "planned_start_date": "2024-11-05"},
    {"name": "WO-2024-003", "production_item": "MED-DEV-003", "qty": 15, "status": "Completed", "planned_start_date": "2024-10-25"}
]

items = [
    {"item_code": "MED-DEV-001", "item_name": "Digital Blood Pressure Monitor", "stock_qty": 50},
    {"item_code": "MED-DEV-002", "item_name": "Pulse Oximeter", "stock_qty": 75},
    {"item_code": "MED-DEV-003", "item_name": "Digital Thermometer", "stock_qty": 30},
    {"item_code": "RAW-MAT-001", "item_name": "Medical Grade Plastic", "stock_qty": 200}
]

employees = [
    {"name": "EMP-001", "employee_name": "John Smith", "department": "Manufacturing", "designation": "Production Manager"},
    {"name": "EMP-002", "employee_name": "Sarah Johnson", "department": "Quality Control", "designation": "QC Manager"},
    {"name": "EMP-003", "employee_name": "Mike Wilson", "department": "Finance", "designation": "Finance Manager"}
]

customers = [
    {"name": "City General Hospital", "customer_type": "Company", "customer_group": "Healthcare", "credit_limit": 100000},
    {"name": "Regional Medical Center", "customer_type": "Company", "customer_group": "Healthcare", "credit_limit": 150000},
    {"name": "Community Health Clinic", "customer_type": "Company", "customer_group": "Healthcare", "credit_limit": 50000}
]

accounts = [
    {"account_name": "Cash", "account_type": "Asset", "balance": 250000},
    {"account_name": "Accounts Receivable", "account_type": "Asset", "balance": 180000},
    {"account_name": "Inventory", "account_type": "Asset", "balance": 320000},
    {"account_name": "Sales Revenue", "account_type": "Income", "balance": 850000}
]

kpis = [
    {"kpi_name": "Production Efficiency", "kpi_type": "Production", "target_value": 85, "current_value": 82},
    {"kpi_name": "Quality Pass Rate", "kpi_type": "Quality", "target_value": 98, "current_value": 96},
    {"kpi_name": "On-Time Delivery", "kpi_type": "Sales", "target_value": 95, "current_value": 93},
    {"kpi_name": "Inventory Turnover", "kpi_type": "Inventory", "target_value": 12, "current_value": 10}
]

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), ERPHandler) as httpd:
        print(f"🏥 Healthcare Manufacturing ERP Server")
        print(f"📊 Dashboard: http://localhost:{PORT}")
        print(f"🔌 APIs: http://localhost:{PORT}/api/work-orders")
        print(f"🛑 Press Ctrl+C to stop")
        httpd.serve_forever()