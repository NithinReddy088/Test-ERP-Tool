# Healthcare Manufacturing ERP Setup Guide

## Quick Setup (Recommended)

### Step 1: Start Database Services
```bash
cd /home/nithin/pro/Test-ERP-Tool
docker-compose -f docker-compose.simple.yml up -d postgres redis
```

### Step 2: Wait and Start Web Service
```bash
# Wait 10 seconds for database to initialize
sleep 10
docker-compose -f docker-compose.simple.yml up -d web
```

### Step 3: Create Site (Wait for web container to be ready)
```bash
# Wait 30 seconds for web container to fully start
sleep 30

# Create new site
docker-compose -f docker-compose.simple.yml exec web bench new-site healthcare-erp.local --admin-password admin --install-app erpnext
```

### Step 4: Install Healthcare Manufacturing App
```bash
# Get the app
docker-compose -f docker-compose.simple.yml exec web bench get-app healthcare_manufacturing /home/frappe/frappe-bench/apps/healthcare_manufacturing

# Install the app
docker-compose -f docker-compose.simple.yml exec web bench --site healthcare-erp.local install-app healthcare_manufacturing
```

### Step 5: Load Sample Data
```bash
docker-compose -f docker-compose.simple.yml exec web python /home/frappe/frappe-bench/apps/healthcare_manufacturing/scripts/seed_data.py
```

## Alternative: Manual Frappe Setup

If Docker setup fails, you can set up Frappe manually:

### Install Frappe Bench
```bash
# Install dependencies
sudo apt update
sudo apt install -y python3-dev python3-pip python3-venv redis-server postgresql postgresql-contrib

# Install bench
pip3 install frappe-bench

# Initialize bench
bench init --frappe-branch version-14 frappe-bench
cd frappe-bench

# Create site
bench new-site healthcare-erp.local --admin-password admin

# Get ERPNext
bench get-app erpnext
bench --site healthcare-erp.local install-app erpnext

# Get Healthcare Manufacturing app
bench get-app healthcare_manufacturing /home/nithin/pro/Test-ERP-Tool/healthcare_manufacturing
bench --site healthcare-erp.local install-app healthcare_manufacturing

# Start development server
bench start
```

## Access the Application

Once setup is complete:
- **URL**: http://localhost:8000
- **Username**: Administrator  
- **Password**: admin

## Key Features to Test

1. **Manufacturing Module**
   - Navigate to Manufacturing > BOM
   - Create a new BOM for medical devices
   - Navigate to Manufacturing > Work Order
   - Create work orders from BOMs

2. **Quality Control**
   - Navigate to Quality > Quality Inspection
   - Create quality inspections
   - Test pass/fail workflows

3. **Traceability**
   - Use API endpoints:
     - `GET /api/method/healthcare_manufacturing.api.traceability.trace_serial?serial_no=SER001`
     - `GET /api/method/healthcare_manufacturing.api.traceability.trace_batch?batch_no=BATCH001`

4. **Manufacturing APIs**
   - `POST /api/method/healthcare_manufacturing.api.manufacturing.create_work_order_from_sales_order`
   - `GET /api/method/healthcare_manufacturing.api.manufacturing.get_work_orders`

## Troubleshooting

### Container Issues
```bash
# Check container status
docker-compose -f docker-compose.simple.yml ps

# View logs
docker-compose -f docker-compose.simple.yml logs web

# Restart services
docker-compose -f docker-compose.simple.yml restart
```

### Database Connection Issues
```bash
# Check PostgreSQL
docker-compose -f docker-compose.simple.yml exec postgres pg_isready

# Check Redis
docker-compose -f docker-compose.simple.yml exec redis redis-cli ping
```

### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER /home/nithin/pro/Test-ERP-Tool
```