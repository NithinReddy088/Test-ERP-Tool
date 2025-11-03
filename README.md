# Healthcare Manufacturing ERP System

A production-ready ERP application built on ERPNext/Frappe for healthcare equipment production and distribution, focusing on quality control, traceability, and regulatory compliance.

## Features

### Core Modules
- **Manufacturing**: BOM management, Work Orders, Production Planning
- **Quality Control**: Inspection Plans, Quality Inspections, NCR/CAPA workflows
- **Inventory**: Batch/Serial tracking, Stock management, Traceability
- **Sales & CRM**: Customer management, Sales Orders, Delivery tracking
- **Accounting**: GL integration, Multi-currency, Tax handling
- **HR & Payroll**: Employee management, Attendance, Payroll processing

### Key Capabilities
- Complete traceability from supplier batch to finished product
- Automated quality inspection workflows
- Real-time production scheduling with Gantt views
- Regulatory compliance with audit trails
- Multi-level BOM support
- Material reservation and allocation

## Quick Start

### Automated Installation (Recommended)

Run the automated setup script:
```bash
./quick-start.sh
```

This script will:
- Check prerequisites
- Install Frappe Bench
- Initialize bench environment
- Create site and install ERPNext
- Install Healthcare Manufacturing app
- Configure the system

### Manual Installation

#### Prerequisites
- Python 3.10+
- Node.js 18+
- MariaDB 10.6+ or PostgreSQL 13+
- Redis 6+
- wkhtmltopdf (for PDF generation)
- 4GB+ RAM
- 20GB+ disk space

#### Installation Steps

1. Install Frappe Bench:
```bash
pip3 install frappe-bench
```

2. Initialize bench:
```bash
bench init frappe-bench --frappe-branch version-15
cd frappe-bench
```

3. Create a new site:
```bash
bench new-site healthcare-erp.local --admin-password admin
```

4. Clone and install the app:
```bash
bench get-app /path/to/Test-ERP-Tool/healthcare_manufacturing
bench --site healthcare-erp.local install-app healthcare_manufacturing
```

5. Load seed data:
```bash
bench --site healthcare-erp.local execute healthcare_manufacturing.setup.seed_data.load_seed_data
```

6. Start the application:
```bash
bench start
```

7. Access the application:
- Web UI: http://localhost:8000
- Admin credentials: Administrator / admin

## API Documentation

### Manufacturing APIs

#### Create Work Order from Sales Order
```bash
POST /api/method/healthcare_manufacturing.api.manufacturing.create_work_order_from_sales_order
{
  "sales_order": "SO-2024-00001"
}
```

#### Get Work Orders
```bash
GET /api/method/healthcare_manufacturing.api.manufacturing.get_work_orders?status=Open
```

### Traceability APIs

#### Trace Serial Number
```bash
GET /api/method/healthcare_manufacturing.api.traceability.trace_serial?serial_no=SER001
```

#### Trace Batch Number
```bash
GET /api/method/healthcare_manufacturing.api.traceability.trace_batch?batch_no=BATCH001
```

## Testing

Run unit tests:
```bash
bench --site healthcare-erp.local run-tests --app healthcare_manufacturing
```

Run specific test:
```bash
bench --site healthcare-erp.local run-tests healthcare_manufacturing.tests.test_work_order
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Frappe Web    │    │   Workers       │
│   Application   │────│   (Background   │
│   (Gunicorn)    │    │   Jobs)         │
└─────────────────┘    └─────────────────┘
         │
         ├─────────────────┬─────────────────┐
         │                 │                 │
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   MariaDB/      │ │   Redis         │ │   SocketIO      │
│   PostgreSQL    │ │   (Cache/Queue) │ │   (Realtime)    │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

## Security & Compliance

### Audit Trails
- All critical DocTypes have change tracking enabled
- User actions are logged with timestamps
- Document attachments are versioned

### Data Encryption
- Database connections use SSL/TLS
- File uploads are scanned for malware
- Sensitive data fields are encrypted at rest

### Access Control
- Role-based permissions with least privilege
- Multi-factor authentication support
- Session management and timeout controls

## Monitoring

### Metrics (Prometheus + Grafana)
- System performance metrics
- Application-specific KPIs
- Quality control failure rates
- Production efficiency metrics

Access Grafana: http://localhost:3000 (admin/admin)

### Logging
- Centralized application logs
- Audit trail preservation
- Error tracking and alerting

## Backup & Recovery

### Automated Backups
```bash
# Database and files backup
bench --site healthcare-erp.local backup --with-files

# Backups are stored in sites/healthcare-erp.local/private/backups/
```

### Restore Process
```bash
# Restore database and files
bench --site healthcare-erp.local restore /path/to/backup.sql.gz --with-private-files /path/to/files.tar --with-public-files /path/to/public-files.tar
```

## Development

### Adding New DocTypes
1. Create DocType JSON in appropriate module
2. Add Python controller with business logic
3. Create tests for validation
4. Update permissions and workflows

### Custom API Endpoints
```python
# healthcare_manufacturing/api/custom.py
import frappe

@frappe.whitelist()
def custom_endpoint():
    return {"status": "success"}
```

### Running in Development Mode
```bash
# Enable developer mode
bench --site healthcare-erp.local set-config developer_mode 1

# Start in development mode
bench start
```

## Production Deployment

### Setup Production
```bash
# Setup production environment
sudo bench setup production <username>

# Enable SSL
sudo bench setup lets-encrypt healthcare-erp.local
```

### Performance Tuning
- Configure MariaDB/PostgreSQL for production workloads
- Set up Redis persistence and memory limits
- Configure Nginx caching and compression
- Adjust Gunicorn workers: `bench set-config -g workers 4`
- Enable background workers: `bench set-config -g background_workers 2`

### Monitoring Setup
- Monitor logs: `bench --site healthcare-erp.local logs`
- Check processes: `bench doctor`
- Monitor key business metrics via custom reports

## Documentation

### Comprehensive Guides
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Complete setup and deployment instructions
- **[Architecture Documentation](ARCHITECTURE.md)** - System architecture and design
- **[Presentation](PRESENTATION.md)** - Project overview and implementation details

### Additional Resources
- API Documentation: `/api/method/frappe.desk.query_report.run`
- User Manual: Available in the application help section
- Developer Guide: See `docs/` directory

## Custom DocTypes

This ERP includes healthcare-specific custom DocTypes:

1. **Quality Control Log** - Comprehensive quality inspection tracking
2. **Equipment Compliance Certificate** - ISO 13485, FDA, CE Mark management
3. **Maintenance Schedule** - Preventive and corrective maintenance planning
4. **Production Batch Tracking** - Complete traceability from raw materials to finished products

## Support

### Troubleshooting
- Check application logs: `bench --site healthcare-erp.local logs`
- Check bench status: `bench doctor`
- Database connectivity: `bench mariadb` or `bench postgres`
- Redis status: `redis-cli ping`
- Clear cache: `bench --site healthcare-erp.local clear-cache`

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

---

For detailed technical documentation, see the `docs/` directory.