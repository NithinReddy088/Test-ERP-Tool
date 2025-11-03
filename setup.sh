#!/bin/bash

set -e

echo "Healthcare Manufacturing ERP - Native Setup"
echo "==========================================="

# Check prerequisites
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required but not installed."; exit 1; }
command -v node >/dev/null 2>&1 || { echo "Node.js is required but not installed."; exit 1; }
command -v redis-cli >/dev/null 2>&1 || { echo "Redis is required but not installed."; exit 1; }

# Install frappe-bench if not already installed
if ! command -v bench >/dev/null 2>&1; then
    echo "Installing frappe-bench..."
    pip3 install frappe-bench
fi

# Initialize bench if not exists
if [ ! -d "frappe-bench" ]; then
    echo "Initializing Frappe bench..."
    bench init frappe-bench --frappe-branch version-15
fi

cd frappe-bench

# Create site
SITE_NAME="healthcare-erp.local"
if [ ! -d "sites/$SITE_NAME" ]; then
    echo "Creating site: $SITE_NAME"
    bench new-site $SITE_NAME --admin-password admin
else
    echo "Site $SITE_NAME already exists"
fi

# Get app
APP_PATH="$(dirname $(pwd))/healthcare_manufacturing"
if [ ! -d "apps/healthcare_manufacturing" ]; then
    echo "Getting healthcare_manufacturing app..."
    bench get-app $APP_PATH
else
    echo "App already exists"
fi

# Install app
echo "Installing healthcare_manufacturing app..."
bench --site $SITE_NAME install-app healthcare_manufacturing

# Load seed data
echo "Loading seed data..."
bench --site $SITE_NAME execute healthcare_manufacturing.setup.seed_data.load_seed_data || echo "Seed data loading skipped"

echo ""
echo "Setup complete!"
echo "Start the application with: cd frappe-bench && bench start"
echo "Access at: http://localhost:8000"
echo "Login: Administrator / admin"
