#!/usr/bin/env python3
"""
Simple Flask-based ERP Demo Server
Demonstrates the Healthcare Manufacturing ERP features without Docker
"""

from flask import Flask, render_template_string, jsonify, request
import json
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)

# Sample data
items = [
    {"item_code": "MED-DEV-001", "item_name": "Digital Blood Pressure Monitor", "stock_qty": 50},
    {"item_code": "MED-DEV-002", "item_name": "Pulse Oximeter", "stock_qty": 75},
    {"item_code": "RAW-MAT-001", "item_name": "Medical Grade Plastic", "stock_qty": 200}
]

work_orders = [
    {
        "name": "WO-2024-001",
        "production_item": "MED-DEV-001",
        "qty": 10,
        "status": "In Process",
        "planned_start_date": "2024-11-01",
        "planned_end_date": "2024-11-07"
    },
    {
        "name": "WO-2024-002", 
        "production_item": "MED-DEV-002",
        "qty": 25,
        "status": "Not Started",
        "planned_start_date": "2024-11-05",
        "planned_end_date": "2024-11-12"
    }
]

quality_inspections = [
    {
        "name": "QI-2024-001",
        "item_code": "MED-DEV-001",
        "batch_no": "BATCH-001",
        "status": "Accepted",
        "inspection_date": "2024-10-30"
    }
]

# HTML Templates
dashboard_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Healthcare Manufacturing ERP</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .header { background: #2196F3; color: white; padding: 20px; border-radius: 5px; }
        .nav { margin: 20px 0; }
        .nav a { margin-right: 20px; padding: 10px 15px; background: #4CAF50; color: white; text-decoration: none; border-radius: 3px; }
        .nav a:hover { background: #45a049; }
        .card { background: white; padding: 20px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stats { display: flex; gap: 20px; }
        .stat { flex: 1; text-align: center; }
        .stat h3 { margin: 0; color: #2196F3; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f2f2f2; }
        .status-in-process { color: #ff9800; font-weight: bold; }
        .status-not-started { color: #f44336; font-weight: bold; }
        .status-accepted { color: #4caf50; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏥 Healthcare Manufacturing ERP System</h1>
        <p>Production-ready ERP for Healthcare Equipment Manufacturing & Distribution</p>
    </div>
    
    <div class="nav">
        <a href="/">Dashboard</a>
        <a href="/manufacturing">Manufacturing</a>
        <a href="/quality">Quality Control</a>
        <a href="/inventory">Inventory</a>
        <a href="/api/docs">API Docs</a>
    </div>

    <div class="stats">
        <div class="card stat">
            <h3>{{ work_orders|length }}</h3>
            <p>Active Work Orders</p>
        </div>
        <div class="card stat">
            <h3>{{ items|length }}</h3>
            <p>Items in Catalog</p>
        </div>
        <div class="card stat">
            <h3>{{ quality_inspections|length }}</h3>
            <p>Quality Inspections</p>
        </div>
    </div>

    <div class="card">
        <h2>Recent Work Orders</h2>
        <table>
            <tr><th>Work Order</th><th>Item</th><th>Qty</th><th>Status</th><th>Start Date</th></tr>
            {% for wo in work_orders %}
            <tr>
                <td>{{ wo.name }}</td>
                <td>{{ wo.production_item }}</td>
                <td>{{ wo.qty }}</td>
                <td class="status-{{ wo.status.lower().replace(' ', '-') }}">{{ wo.status }}</td>
                <td>{{ wo.planned_start_date }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>

    <div class="card">
        <h2>Inventory Status</h2>
        <table>
            <tr><th>Item Code</th><th>Item Name</th><th>Stock Qty</th></tr>
            {% for item in items %}
            <tr>
                <td>{{ item.item_code }}</td>
                <td>{{ item.item_name }}</td>
                <td>{{ item.stock_qty }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

api_docs_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Healthcare Manufacturing ERP - API Documentation</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .header { background: #2196F3; color: white; padding: 20px; border-radius: 5px; }
        .card { background: white; padding: 20px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .endpoint { background: #e8f5e8; padding: 10px; border-left: 4px solid #4caf50; margin: 10px 0; }
        .method { background: #4caf50; color: white; padding: 2px 8px; border-radius: 3px; font-size: 12px; }
        pre { background: #f4f4f4; padding: 10px; border-radius: 3px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔌 API Documentation</h1>
        <p>Healthcare Manufacturing ERP REST API Endpoints</p>
    </div>

    <div class="card">
        <h2>Manufacturing APIs</h2>
        
        <div class="endpoint">
            <h3><span class="method">GET</span> /api/work-orders</h3>
            <p>Get all work orders with optional status filter</p>
            <pre>curl "http://localhost:5000/api/work-orders?status=In Process"</pre>
        </div>

        <div class="endpoint">
            <h3><span class="method">POST</span> /api/work-orders</h3>
            <p>Create a new work order</p>
            <pre>curl -X POST "http://localhost:5000/api/work-orders" \\
  -H "Content-Type: application/json" \\
  -d '{"production_item": "MED-DEV-001", "qty": 5}'</pre>
        </div>
    </div>

    <div class="card">
        <h2>Quality Control APIs</h2>
        
        <div class="endpoint">
            <h3><span class="method">GET</span> /api/quality-inspections</h3>
            <p>Get all quality inspection records</p>
            <pre>curl "http://localhost:5000/api/quality-inspections"</pre>
        </div>
    </div>

    <div class="card">
        <h2>Traceability APIs</h2>
        
        <div class="endpoint">
            <h3><span class="method">GET</span> /api/trace/serial/{serial_no}</h3>
            <p>Trace a serial number through production history</p>
            <pre>curl "http://localhost:5000/api/trace/serial/SER001"</pre>
        </div>

        <div class="endpoint">
            <h3><span class="method">GET</span> /api/trace/batch/{batch_no}</h3>
            <p>Trace a batch number through quality records</p>
            <pre>curl "http://localhost:5000/api/trace/batch/BATCH001"</pre>
        </div>
    </div>

    <div class="card">
        <h2>Inventory APIs</h2>
        
        <div class="endpoint">
            <h3><span class="method">GET</span> /api/items</h3>
            <p>Get all items in inventory</p>
            <pre>curl "http://localhost:5000/api/items"</pre>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(dashboard_html, 
                                work_orders=work_orders, 
                                items=items, 
                                quality_inspections=quality_inspections)

@app.route('/manufacturing')
def manufacturing():
    return render_template_string("""
    <h1>Manufacturing Module</h1>
    <p>Work Orders, BOMs, and Production Planning</p>
    <a href="/">← Back to Dashboard</a>
    """)

@app.route('/quality')
def quality():
    return render_template_string("""
    <h1>Quality Control Module</h1>
    <p>Quality Inspections, NCR, and CAPA workflows</p>
    <a href="/">← Back to Dashboard</a>
    """)

@app.route('/inventory')
def inventory():
    return render_template_string("""
    <h1>Inventory Module</h1>
    <p>Stock management, Batch/Serial tracking, Traceability</p>
    <a href="/">← Back to Dashboard</a>
    """)

@app.route('/api/docs')
def api_docs():
    return render_template_string(api_docs_html)

# API Endpoints
@app.route('/api/work-orders', methods=['GET', 'POST'])
def api_work_orders():
    if request.method == 'GET':
        status_filter = request.args.get('status')
        if status_filter:
            filtered_orders = [wo for wo in work_orders if wo['status'] == status_filter]
            return jsonify(filtered_orders)
        return jsonify(work_orders)
    
    elif request.method == 'POST':
        data = request.json
        new_wo = {
            "name": f"WO-2024-{str(uuid.uuid4())[:3]}",
            "production_item": data.get('production_item'),
            "qty": data.get('qty'),
            "status": "Not Started",
            "planned_start_date": datetime.now().strftime('%Y-%m-%d'),
            "planned_end_date": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        }
        work_orders.append(new_wo)
        return jsonify(new_wo), 201

@app.route('/api/quality-inspections')
def api_quality_inspections():
    return jsonify(quality_inspections)

@app.route('/api/items')
def api_items():
    return jsonify(items)

@app.route('/api/trace/serial/<serial_no>')
def api_trace_serial(serial_no):
    return jsonify({
        "serial_no": serial_no,
        "item_code": "MED-DEV-001",
        "status": "In Stock",
        "production_history": [
            {"work_order": "WO-2024-001", "date": "2024-10-25"},
        ],
        "quality_inspections": [
            {"inspection": "QI-2024-001", "status": "Accepted", "date": "2024-10-30"}
        ]
    })

@app.route('/api/trace/batch/<batch_no>')
def api_trace_batch(batch_no):
    return jsonify({
        "batch_no": batch_no,
        "item_code": "RAW-MAT-001",
        "manufacturing_date": "2024-10-20",
        "quality_inspections": quality_inspections,
        "stock_movements": [
            {"date": "2024-10-20", "type": "Receipt", "qty": 100},
            {"date": "2024-10-25", "type": "Issue", "qty": 50}
        ]
    })

if __name__ == '__main__':
    print("🏥 Healthcare Manufacturing ERP Server Starting...")
    print("📊 Dashboard: http://localhost:5000")
    print("🔌 API Docs: http://localhost:5000/api/docs")
    print("🛑 Press Ctrl+C to stop")
    app.run(host='0.0.0.0', port=5000, debug=True)