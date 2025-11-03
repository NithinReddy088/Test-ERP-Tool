# Healthcare Equipment ERP - Quick Reference Guide

## 🚀 Installation (One Command)

```bash
./quick-start.sh
```

Then access: **http://localhost:8000** (Administrator / admin)

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| [README.md](README.md) | Quick start & overview |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Complete setup guide |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture |
| [PRESENTATION.md](PRESENTATION.md) | Project presentation |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Complete summary |
| [DELIVERABLES_CHECKLIST.md](DELIVERABLES_CHECKLIST.md) | All deliverables |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | This file |

---

## 🎯 Key Features

### 6 Core Modules
1. **Accounting & Finance** - GL, AP/AR, Multi-currency
2. **HR & Payroll** - Employees, Attendance, Payroll
3. **Inventory** - Stock, Batch/Serial tracking
4. **Sales & CRM** - Customers, Orders, Delivery
5. **Manufacturing** - BOM, Work Orders, Production
6. **Analytics** - Dashboards, Reports, KPIs

### 4 Custom DocTypes
1. **Quality Control Log** - Inspection tracking
2. **Equipment Compliance Certificate** - ISO/FDA/CE
3. **Maintenance Schedule** - Equipment maintenance
4. **Production Batch Tracking** - Complete traceability

---

## ⚡ Common Commands

### Start/Stop
```bash
cd healthcare_erp_bench
bench start                    # Start server
bench restart                  # Restart server
```

### Site Management
```bash
bench use healthcare.localhost              # Set default site
bench --site healthcare.localhost migrate   # Run migrations
bench --site healthcare.localhost clear-cache  # Clear cache
```

### Backup/Restore
```bash
bench --site healthcare.localhost backup --with-files
bench --site healthcare.localhost restore /path/to/backup.sql.gz
```

### Testing
```bash
bench --site healthcare.localhost run-tests --app healthcare_manufacturing
```

### Logs
```bash
bench --site healthcare.localhost logs
bench doctor  # Check system status
```

---

## 🔑 Default Credentials

- **URL:** http://localhost:8000
- **Username:** Administrator
- **Password:** admin

---

## 📂 Project Structure

```
Test-ERP-Tool/
├── healthcare_manufacturing/          # Main app
│   ├── accounting/                   # Accounting module
│   ├── hr/                           # HR module
│   ├── inventory/                    # Inventory module
│   ├── sales/                        # Sales module
│   ├── manufacturing/                # Manufacturing module
│   │   ├── maintenance_schedule/     # Custom
│   │   └── production_batch_tracking/# Custom
│   ├── quality_control/              # Quality module
│   │   ├── quality_control_log/      # Custom
│   │   └── equipment_compliance_certificate/ # Custom
│   └── analytics/                    # Analytics module
├── quick-start.sh                    # Automated setup
├── README.md                         # Main docs
└── DEPLOYMENT_GUIDE.md               # Full guide
```

---

## 🔄 Workflows

### Sales → Production
```
Sales Order → Production Plan → Work Order → 
Production → Quality Check → Delivery
```

### Purchase → Stock
```
Material Request → Purchase Order → 
Purchase Receipt → Quality Inspection → Stock Entry
```

---

## 🌐 API Examples

### Create Work Order
```bash
curl -X POST http://localhost:8000/api/method/healthcare_manufacturing.api.manufacturing.create_work_order \
  -H "Authorization: token <key>:<secret>" \
  -H "Content-Type: application/json" \
  -d '{"sales_order": "SO-2024-00001"}'
```

### Trace Batch
```bash
curl http://localhost:8000/api/method/healthcare_manufacturing.api.traceability.trace_batch?batch_no=BATCH001 \
  -H "Authorization: token <key>:<secret>"
```

---

## 🛠️ Troubleshooting

### Server won't start
```bash
bench doctor
bench setup requirements
```

### Database issues
```bash
bench mariadb  # Access database
bench migrate  # Run migrations
```

### Cache issues
```bash
bench --site healthcare.localhost clear-cache
bench restart
```

### Permission errors
```bash
sudo chown -R $USER:$USER ~/healthcare_erp_bench
```

---

## 📊 Access Modules

After login, navigate to:

- **Accounting:** Home → Accounting
- **HR:** Home → HR
- **Inventory:** Home → Stock
- **Sales:** Home → Selling
- **Manufacturing:** Home → Manufacturing
- **Quality Control:** Home → Quality
- **Analytics:** Home → Dashboard

---

## 🎓 Learning Path

1. **Start Here:** [README.md](README.md)
2. **Install:** Run `./quick-start.sh`
3. **Learn Setup:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
4. **Understand Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)
5. **See Full Picture:** [PRESENTATION.md](PRESENTATION.md)

---

## 📞 Getting Help

### Check Logs
```bash
bench --site healthcare.localhost logs
```

### System Status
```bash
bench doctor
```

### Community
- Frappe Forum: https://discuss.frappe.io
- ERPNext Docs: https://docs.erpnext.com

---

## ✅ Quick Checklist

Before going live:

- [ ] Run `bench doctor` - all checks pass
- [ ] Test all modules
- [ ] Configure backups
- [ ] Set up SSL (production)
- [ ] Train users
- [ ] Load production data
- [ ] Test workflows
- [ ] Configure email
- [ ] Set up monitoring

---

## 🚀 Production Deployment

```bash
# Setup production
sudo bench setup production $USER

# Enable SSL
sudo bench setup lets-encrypt healthcare.localhost

# Configure workers
bench set-config -g workers 4
bench set-config -g background_workers 2

# Restart
sudo supervisorctl restart all
```

---

## 📈 Key Metrics to Monitor

- Production efficiency
- Quality pass rate
- Inventory accuracy
- Order fulfillment time
- System uptime
- User adoption

---

## 🎯 Success Indicators

✅ All 6 modules operational
✅ Custom DocTypes working
✅ Workflows automated
✅ Dashboards showing data
✅ Users trained
✅ Backups configured
✅ System stable

---

**Quick Reference Version:** 1.0.0
**Last Updated:** 2024
