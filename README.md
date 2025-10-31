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

### Prerequisites
- Docker and Docker Compose
- 4GB+ RAM
- 20GB+ disk space

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Test-ERP-Tool
```

2. Copy environment file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the services:
```bash
docker-compose up -d
```

4. Initialize the site:
```bash
docker-compose exec web bench new-site healthcare-erp.local --admin-password admin
docker-compose exec web bench --site healthcare-erp.local install-app healthcare_manufacturing
```

5. Load seed data:
```bash
docker-compose exec web python scripts/seed_data.py
```

6. Access the application:
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
docker-compose exec web bench --site healthcare-erp.local run-tests --app healthcare_manufacturing
```

Run specific test:
```bash
docker-compose exec web bench --site healthcare-erp.local run-tests healthcare_manufacturing.tests.test_work_order
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx         │    │   Frappe Web    │    │   Workers       │
│   (Reverse      │────│   Application   │────│   (Background   │
│   Proxy)        │    │                 │    │   Jobs)         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐    ┌─────────────────┐
                       │   PostgreSQL    │    │   Redis         │
                       │   (Database)    │    │   (Cache/Queue) │
                       └─────────────────┘    └─────────────────┘
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
# Database backup
docker-compose exec backup /backup.sh

# File backup
docker-compose exec web tar -czf /backups/files-$(date +%Y%m%d).tar.gz /home/frappe/frappe-bench/sites
```

### Restore Process
```bash
# Restore database
docker-compose exec postgres psql -U postgres -d healthcare_erp < /backups/backup.sql

# Restore files
docker-compose exec web tar -xzf /backups/files-20240101.tar.gz -C /
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
# Start in development mode
docker-compose -f docker-compose.dev.yml up

# Enable developer mode
docker-compose exec web bench --site healthcare-erp.local set-config developer_mode 1
```

## Production Deployment

### Kubernetes Deployment
See `k8s/` directory for Helm charts and deployment manifests.

### Performance Tuning
- Configure PostgreSQL for production workloads
- Set up Redis clustering for high availability
- Enable Nginx caching and compression
- Configure worker scaling based on load

### Monitoring Setup
- Deploy Prometheus and Grafana
- Configure alerting rules
- Set up log aggregation
- Monitor key business metrics

## Support

### Documentation
- API Documentation: `/api/method/frappe.desk.query_report.run`
- User Manual: Available in the application help section
- Developer Guide: See `docs/` directory

### Troubleshooting
- Check application logs: `docker-compose logs web`
- Database connectivity: `docker-compose exec postgres pg_isready`
- Redis status: `docker-compose exec redis redis-cli ping`

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