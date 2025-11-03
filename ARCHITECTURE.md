# Healthcare Equipment ERP - System Architecture

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Web UI     │  │   Mobile     │  │   API        │          │
│  │   (Browser)  │  │   (PWA)      │  │   Clients    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Application Layer                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Frappe Framework (Python)                   │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐│   │
│  │  │  HR    │ │Account │ │Manufac │ │Inventor│ │ Sales  ││   │
│  │  │ Module │ │ Module │ │ Module │ │ Module │ │ Module ││   │
│  │  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘│   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │         Healthcare Manufacturing Custom App              │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐          │   │
│  │  │  Quality   │ │Traceability│ │ Compliance │          │   │
│  │  │  Control   │ │  System    │ │  Manager   │          │   │
│  │  └────────────┘ └────────────┘ └────────────┘          │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Service Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Gunicorn   │  │   SocketIO   │  │   Workers    │          │
│  │   (WSGI)     │  │   (Realtime) │  │  (Background)│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Data Layer                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   MariaDB/   │  │    Redis     │  │   File       │          │
│  │  PostgreSQL  │  │ (Cache/Queue)│  │   Storage    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Module Architecture

### 1. Accounting & Finance Module

**Components:**
- Chart of Accounts
- General Ledger
- Accounts Payable/Receivable
- Payment Processing
- Financial Reports

**Data Flow:**
```
Sales Order → Sales Invoice → Payment Entry → GL Entry
Purchase Order → Purchase Invoice → Payment Entry → GL Entry
```

**Key Tables:**
- `tabAccount`
- `tabJournal Entry`
- `tabPayment Entry`
- `tabGL Entry`

### 2. HR & Payroll Module

**Components:**
- Employee Management
- Attendance System
- Leave Management
- Payroll Processing
- Compliance Tracking

**Data Flow:**
```
Employee → Attendance → Salary Structure → Salary Slip → Payment
```

**Key Tables:**
- `tabEmployee`
- `tabAttendance`
- `tabSalary Slip`
- `tabPayroll Entry`

### 3. Inventory & Supply Chain Module

**Components:**
- Item Master
- Warehouse Management
- Stock Ledger
- Batch/Serial Tracking
- Material Request

**Data Flow:**
```
Purchase Order → Purchase Receipt → Stock Entry → Delivery Note
Material Request → Purchase Order → Stock Entry
```

**Key Tables:**
- `tabItem`
- `tabWarehouse`
- `tabStock Ledger Entry`
- `tabBatch`
- `tabSerial No`

### 4. Sales & CRM Module

**Components:**
- Customer Management
- Lead Tracking
- Opportunity Management
- Quotation System
- Sales Order Processing

**Data Flow:**
```
Lead → Opportunity → Quotation → Sales Order → Delivery Note → Sales Invoice
```

**Key Tables:**
- `tabCustomer`
- `tabLead`
- `tabOpportunity`
- `tabQuotation`
- `tabSales Order`

### 5. Manufacturing Module

**Components:**
- BOM Management
- Work Order System
- Production Planning
- Job Cards
- Maintenance Scheduling

**Data Flow:**
```
Sales Order → Production Plan → Work Order → Job Card → Stock Entry
BOM → Work Order → Material Transfer → Production → Quality Check
```

**Key Tables:**
- `tabBOM`
- `tabWork Order`
- `tabProduction Plan`
- `tabJob Card`
- `tabMaintenance Schedule`

### 6. Quality Control Module

**Components:**
- Quality Inspection
- Inspection Plans
- NCR/CAPA Management
- Compliance Certificates
- Quality Control Logs

**Data Flow:**
```
Purchase Receipt → Quality Inspection → Acceptance/Rejection
Work Order → Quality Inspection → Batch Release
```

**Key Tables:**
- `tabQuality Inspection`
- `tabQuality Control Log`
- `tabEquipment Compliance Certificate`
- `tabCAPA`
- `tabNCR`

---

## 🔄 Workflow Architecture

### Sales to Production Workflow

```
┌──────────────┐
│ Sales Order  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Production   │
│    Plan      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Work Order   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Material     │
│ Transfer     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Production   │
│ Execution    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Quality      │
│ Inspection   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Stock Entry  │
│ (Finished)   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Delivery     │
│    Note      │
└──────────────┘
```

### Purchase to Stock Workflow

```
┌──────────────┐
│ Material     │
│  Request     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Purchase     │
│   Order      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Purchase     │
│  Receipt     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Quality      │
│ Inspection   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Stock Entry  │
└──────────────┘
```

---

## 🔐 Security Architecture

### Authentication & Authorization

```
┌─────────────────────────────────────────┐
│         Authentication Layer            │
│  ┌────────────┐  ┌────────────┐        │
│  │   Login    │  │    OAuth   │        │
│  │   (Local)  │  │   (SSO)    │        │
│  └────────────┘  └────────────┘        │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│        Authorization Layer              │
│  ┌────────────┐  ┌────────────┐        │
│  │   Role     │  │Permission  │        │
│  │   Based    │  │   Rules    │        │
│  └────────────┘  └────────────┘        │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│          Data Access Layer              │
│  ┌────────────┐  ┌────────────┐        │
│  │   User     │  │   Field    │        │
│  │ Permissions│  │   Level    │        │
│  └────────────┘  └────────────┘        │
└─────────────────────────────────────────┘
```

### Role Hierarchy

```
Administrator
    │
    ├── System Manager
    │   ├── HR Manager
    │   ├── Accounts Manager
    │   ├── Manufacturing Manager
    │   └── Quality Manager
    │
    ├── Sales Manager
    │   └── Sales User
    │
    ├── Purchase Manager
    │   └── Purchase User
    │
    └── Stock Manager
        └── Stock User
```

---

## 📊 Database Schema

### Core Tables

**Item Master:**
```sql
tabItem
├── item_code (PK)
├── item_name
├── item_group
├── stock_uom
├── has_batch_no
├── has_serial_no
└── is_stock_item
```

**BOM:**
```sql
tabBOM
├── name (PK)
├── item
├── quantity
├── is_active
└── is_default

tabBOM Item
├── parent (FK → tabBOM)
├── item_code
├── qty
└── rate
```

**Work Order:**
```sql
tabWork Order
├── name (PK)
├── production_item
├── bom_no
├── qty
├── planned_start_date
├── status
└── actual_start_date
```

**Quality Inspection:**
```sql
tabQuality Inspection
├── name (PK)
├── inspection_type
├── reference_type
├── reference_name
├── item_code
├── batch_no
└── status
```

---

## 🔌 API Architecture

### REST API Endpoints

**Manufacturing APIs:**
```
POST   /api/method/healthcare_manufacturing.api.manufacturing.create_work_order
GET    /api/method/healthcare_manufacturing.api.manufacturing.get_work_orders
PUT    /api/method/healthcare_manufacturing.api.manufacturing.update_work_order
DELETE /api/method/healthcare_manufacturing.api.manufacturing.cancel_work_order
```

**Traceability APIs:**
```
GET    /api/method/healthcare_manufacturing.api.traceability.trace_serial
GET    /api/method/healthcare_manufacturing.api.traceability.trace_batch
GET    /api/method/healthcare_manufacturing.api.traceability.get_full_trace
```

**Quality Control APIs:**
```
POST   /api/method/healthcare_manufacturing.api.quality.create_inspection
GET    /api/method/healthcare_manufacturing.api.quality.get_inspections
PUT    /api/method/healthcare_manufacturing.api.quality.update_inspection
```

### API Authentication

```python
# Token-based authentication
headers = {
    "Authorization": "token <api_key>:<api_secret>",
    "Content-Type": "application/json"
}
```

---

## 🚀 Deployment Architecture

### Development Environment

```
┌─────────────────────────────────────┐
│      Development Machine            │
│  ┌───────────────────────────────┐  │
│  │   Frappe Bench                │  │
│  │   - Web Server (Port 8000)    │  │
│  │   - SocketIO (Port 9000)      │  │
│  │   - Redis (Port 6379)         │  │
│  │   - MariaDB (Port 3306)       │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Production Environment

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                        │
│                    (Nginx/HAProxy)                      │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼────────┐       ┌───────▼────────┐
│  App Server 1  │       │  App Server 2  │
│  - Gunicorn    │       │  - Gunicorn    │
│  - Workers     │       │  - Workers     │
└───────┬────────┘       └───────┬────────┘
        │                         │
        └────────────┬────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼────────┐       ┌───────▼────────┐
│   Database     │       │     Redis      │
│   (MariaDB)    │       │   (Cache)      │
│   - Master     │       │   - Cluster    │
│   - Replica    │       │                │
└────────────────┘       └────────────────┘
```

---

## 📈 Scalability Considerations

### Horizontal Scaling

- Multiple Gunicorn workers
- Redis clustering for cache
- Database read replicas
- Load balancing across app servers

### Vertical Scaling

- Increase server resources (CPU, RAM)
- Optimize database queries
- Enable query caching
- Use connection pooling

### Performance Optimization

```python
# Enable query caching
frappe.cache().set_value("key", value, expires_in_sec=3600)

# Use background jobs for heavy tasks
frappe.enqueue(
    method="healthcare_manufacturing.tasks.process_batch",
    queue="long",
    timeout=3600
)

# Database indexing
frappe.db.add_index("Work Order", ["status", "planned_start_date"])
```

---

## 🔍 Monitoring & Logging

### Application Monitoring

- Request/Response logging
- Error tracking
- Performance metrics
- User activity logs

### System Monitoring

- CPU/Memory usage
- Disk I/O
- Network traffic
- Database performance

### Log Files

```
logs/
├── web.log          # Web server logs
├── worker.log       # Background worker logs
├── redis.log        # Redis logs
└── mariadb.log      # Database logs
```

---

## 🔄 Backup & Recovery

### Backup Strategy

```
Daily Backups:
├── Database dump (SQL)
├── File attachments
└── Configuration files

Weekly Backups:
├── Full system backup
└── Offsite storage

Monthly Backups:
└── Archive storage
```

### Recovery Procedures

```bash
# Restore database
bench --site healthcare.localhost restore /path/to/backup.sql.gz

# Restore files
bench --site healthcare.localhost restore --with-private-files /path/to/files.tar
```

---

## 📚 Technology Stack Summary

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, JavaScript, Vue.js |
| Backend | Python 3.10, Frappe Framework |
| Database | MariaDB 10.6 / PostgreSQL 13 |
| Cache | Redis 6+ |
| Web Server | Nginx |
| App Server | Gunicorn |
| Task Queue | RQ (Redis Queue) |
| Real-time | SocketIO |
| Charts | Frappe Charts |
| PDF | wkhtmltopdf |

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**Maintained By:** Healthcare ERP Team
