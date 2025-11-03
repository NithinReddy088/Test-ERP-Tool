# Healthcare Equipment ERP - Complete Deployment Guide

## 🎯 Project Overview

**Implementation of an Integrated ERP System for Healthcare Equipment Production and Distribution**

This ERP system integrates HR, Accounting, Manufacturing, Inventory, Sales, and Analytics for healthcare equipment companies with focus on quality control, compliance, and traceability.

---

## 📋 Prerequisites

### System Requirements
- Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- 4GB+ RAM (8GB recommended)
- 20GB+ disk space
- Python 3.10+
- Node.js 18+
- MariaDB 10.6+ or PostgreSQL 13+
- Redis 6+

### Install System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y \
    python3-dev \
    python3.10 \
    python3-pip \
    python3-setuptools \
    python3-distutils \
    python3-venv \
    nodejs \
    npm \
    redis-server \
    mariadb-server \
    xvfb \
    libfontconfig \
    wkhtmltopdf \
    git \
    nginx \
    curl \
    build-essential

# Start services
sudo systemctl start redis-server
sudo systemctl enable redis-server
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

---

## 🚀 Installation Steps

### Step 1: Install Frappe Bench

```bash
# Install frappe-bench
sudo pip3 install frappe-bench

# Verify installation
bench --version
```

### Step 2: Initialize Frappe Environment

```bash
# Initialize bench with Frappe version 15
bench init healthcare_erp --frappe-branch version-15

# Navigate to bench directory
cd healthcare_erp
```

### Step 3: Create New Site

```bash
# Create site with MariaDB
bench new-site healthcare.localhost --admin-password admin

# Set site as default
bench use healthcare.localhost
```

### Step 4: Get ERPNext App

```bash
# Get ERPNext version 15
bench get-app erpnext --branch version-15

# Install ERPNext on site
bench --site healthcare.localhost install-app erpnext
```

### Step 5: Install Healthcare Manufacturing App

```bash
# Get the custom healthcare manufacturing app
bench get-app /path/to/Test-ERP-Tool/healthcare_manufacturing

# Install on site
bench --site healthcare.localhost install-app healthcare_manufacturing
```

### Step 6: Start Development Server

```bash
# Start bench
bench start
```

Access the application at: **http://localhost:8000**

Login credentials:
- Username: `Administrator`
- Password: `admin`

---

## 🏗️ Module Configuration

### 1. 🧾 Accounting & Finance Module

**Features:**
- General Ledger management
- Accounts Payable/Receivable
- Multi-currency support
- Tax handling
- Financial reports

**Setup:**
1. Navigate to **Accounting > Chart of Accounts**
2. Create account structure for healthcare equipment business
3. Set up tax templates
4. Configure payment terms

**Key DocTypes:**
- Account
- Journal Entry
- Payment Entry
- Sales Invoice
- Purchase Invoice

### 2. 👥 HR & Payroll Module

**Features:**
- Employee management
- Attendance tracking
- Leave management
- Payroll processing
- Compliance reports

**Setup:**
1. Go to **HR > Employee**
2. Create employee records
3. Set up **Payroll Structure**
4. Configure **Salary Components**
5. Create **Attendance** records

**Key DocTypes:**
- Employee
- Attendance
- Leave Application
- Salary Slip
- Payroll Entry

### 3. 📦 Inventory & Supply Chain Module

**Features:**
- Stock management
- Batch/Serial tracking
- Warehouse management
- Purchase orders
- Material requests

**Setup:**
1. Navigate to **Stock > Item**
2. Create item masters for raw materials and finished goods
3. Set up **Warehouses**
4. Enable batch tracking for items requiring traceability
5. Configure **Stock Settings**

**Key DocTypes:**
- Item
- Warehouse
- Stock Entry
- Purchase Receipt
- Delivery Note
- Batch
- Serial No

### 4. 🛒 Sales & CRM Module

**Features:**
- Customer database
- Lead management
- Quotations
- Sales orders
- Delivery tracking

**Setup:**
1. Go to **CRM > Customer**
2. Create customer records
3. Set up **Sales Taxes and Charges**
4. Configure **Terms and Conditions**

**Key DocTypes:**
- Customer
- Lead
- Opportunity
- Quotation
- Sales Order
- Delivery Note

### 5. 🏭 Manufacturing/Production Module

**Features:**
- Bill of Materials (BOM)
- Work Orders
- Production Planning
- Routing
- Maintenance scheduling

**Setup:**
1. Navigate to **Manufacturing > BOM**
2. Create BOMs for finished products
3. Set up **Workstations**
4. Create **Operations** for routing
5. Configure **Manufacturing Settings**

**Key DocTypes:**
- BOM
- Work Order
- Production Plan
- Job Card
- Workstation
- Maintenance Schedule
- Production Batch Tracking

### 6. 📊 Analytics & Reporting Module

**Features:**
- Real-time dashboards
- KPI tracking
- Production efficiency metrics
- Financial analytics
- Custom reports

**Setup:**
1. Go to **Home > Workspace**
2. Create custom dashboards
3. Add charts using **Frappe Charts**
4. Configure **Report Builder**

**Available Reports:**
- Production Efficiency Report
- Stock Movement Analysis
- Sales Trends
- HR Attendance Summary
- Quality Control Metrics

---

## 🔧 Custom DocTypes

### Quality Control Log
Tracks all quality inspections with parameters, results, and corrective actions.

**Fields:**
- Reference Type/Name
- Inspection Date
- Inspector
- Status (Pending/In Progress/Passed/Failed)
- Inspection Parameters
- Observations
- Corrective Actions

### Equipment Compliance Certificate
Manages compliance certificates for healthcare equipment (ISO 13485, FDA, CE Mark).

**Fields:**
- Equipment Item
- Certificate Number
- Compliance Standard
- Issue/Expiry Date
- Certification Body
- Test Results
- Certificate File

### Maintenance Schedule
Schedules preventive and corrective maintenance for production equipment.

**Fields:**
- Equipment Item
- Schedule Type (Preventive/Predictive/Corrective)
- Frequency
- Next Maintenance Date
- Assigned To
- Maintenance Tasks
- History

### Production Batch Tracking
Complete traceability from raw materials to finished products.

**Fields:**
- Batch Number
- Item Code
- Production Date
- Raw Materials Used
- Quality Inspections
- Operator/Shift/Machine
- Traceability Code
- Supplier Batch Mapping

---

## 🌐 Production Deployment

### Setup Production Environment

```bash
# Setup production with supervisor and nginx
sudo bench setup production <your-username>

# Enable site for production
sudo bench setup nginx
sudo supervisorctl reload
```

### Configure Nginx

```bash
# Edit nginx config
sudo nano /etc/nginx/sites-available/healthcare.localhost

# Add SSL (optional)
sudo bench setup lets-encrypt healthcare.localhost
```

### Performance Tuning

```bash
# Adjust Gunicorn workers
bench set-config -g workers 4

# Enable background workers
bench set-config -g background_workers 2

# Configure Redis
bench set-config -g redis_cache "redis://localhost:6379"
bench set-config -g redis_queue "redis://localhost:6379"
```

### Database Optimization

```bash
# For MariaDB
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```

Add:
```ini
[mysqld]
innodb_buffer_pool_size = 2G
innodb_log_file_size = 512M
max_connections = 200
```

Restart MariaDB:
```bash
sudo systemctl restart mariadb
```

---

## 📊 Dashboard Setup

### Create Management Dashboard

1. Navigate to **Home > Workspace > New Workspace**
2. Name: "Healthcare ERP Dashboard"
3. Add charts:

**Production Efficiency Chart:**
```javascript
frappe.chart = new frappe.Chart("#production-chart", {
    data: {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        datasets: [{
            name: "Production Output",
            values: [120, 145, 160, 155, 180, 195]
        }]
    },
    type: 'line',
    height: 250
});
```

**Sales Trends Chart:**
```javascript
frappe.chart = new frappe.Chart("#sales-chart", {
    data: {
        labels: ["Q1", "Q2", "Q3", "Q4"],
        datasets: [{
            name: "Sales Revenue",
            values: [450000, 520000, 580000, 650000]
        }]
    },
    type: 'bar',
    height: 250
});
```

---

## 🔐 Security Configuration

### Enable SSL

```bash
sudo bench setup lets-encrypt healthcare.localhost
```

### Configure Firewall

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

### Backup Configuration

```bash
# Enable automatic backups
bench --site healthcare.localhost set-config backup_frequency "Daily"

# Manual backup
bench --site healthcare.localhost backup --with-files
```

Backups stored in: `sites/healthcare.localhost/private/backups/`

---

## 📝 Seed Data

### Load Initial Data

```bash
# Execute seed data script
bench --site healthcare.localhost execute healthcare_manufacturing.setup.seed_data.load_seed_data
```

This creates:
- Sample employees
- Sample items (raw materials and finished goods)
- Sample customers and suppliers
- Sample BOMs
- Sample work orders

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
bench --site healthcare.localhost run-tests --app healthcare_manufacturing

# Run specific test
bench --site healthcare.localhost run-tests healthcare_manufacturing.tests.test_work_order

# Run with coverage
bench --site healthcare.localhost run-tests --app healthcare_manufacturing --coverage
```

---

## 📈 Monitoring

### Check System Status

```bash
# Check bench status
bench doctor

# View logs
bench --site healthcare.localhost logs

# Monitor processes
bench --site healthcare.localhost console
```

### Performance Monitoring

```bash
# Enable query logging
bench --site healthcare.localhost set-config enable_query_comments 1

# Monitor slow queries
bench --site healthcare.localhost mariadb
> SELECT * FROM information_schema.processlist WHERE time > 5;
```

---

## 🔄 Maintenance

### Update System

```bash
# Update bench
bench update

# Update specific app
bench update --app healthcare_manufacturing

# Migrate database
bench --site healthcare.localhost migrate
```

### Clear Cache

```bash
# Clear all cache
bench --site healthcare.localhost clear-cache

# Clear website cache
bench --site healthcare.localhost clear-website-cache
```

---

## 📚 Documentation

### Access API Documentation

Navigate to: `http://healthcare.localhost/api/method/frappe.desk.query_report.run`

### User Manual

Available in application: **Help > User Manual**

### Developer Documentation

See `docs/` directory for:
- API reference
- Custom script examples
- Workflow configurations
- Integration guides

---

## 🆘 Troubleshooting

### Common Issues

**Issue: Bench won't start**
```bash
bench doctor
bench setup requirements
```

**Issue: Database connection error**
```bash
bench mariadb
# Check if database is accessible
```

**Issue: Redis connection error**
```bash
redis-cli ping
sudo systemctl restart redis-server
```

**Issue: Permission errors**
```bash
sudo chown -R $USER:$USER ~/healthcare_erp
```

### Get Help

- Check logs: `bench --site healthcare.localhost logs`
- Frappe Forum: https://discuss.frappe.io
- GitHub Issues: https://github.com/frappe/frappe/issues

---

## 📦 Final Deliverables

✅ Working ERP system accessible via browser  
✅ Six integrated business modules  
✅ Custom DocTypes for healthcare compliance  
✅ Real-time dashboards with Frappe Charts  
✅ Complete traceability system  
✅ Automated workflows  
✅ Production-ready deployment  
✅ Comprehensive documentation  

---

## 📞 Support

For technical support or questions:
- Email: admin@healthcare-erp.com
- Documentation: See `docs/` directory
- Community: Frappe Forum

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**License:** MIT
