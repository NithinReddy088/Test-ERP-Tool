#!/bin/bash

echo "Setting up Healthcare Manufacturing ERP..."

# Stop any existing containers
docker-compose down 2>/dev/null || true

# Start with simple configuration
docker-compose -f docker-compose.simple.yml up -d postgres redis

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Start web container
docker-compose -f docker-compose.simple.yml up -d web

# Wait for web container to be ready
echo "Waiting for web container to be ready..."
sleep 20

# Create new site
echo "Creating new site..."
docker-compose -f docker-compose.simple.yml exec web bench new-site healthcare-erp.local --admin-password admin --mariadb-root-password admin --install-app erpnext

# Install healthcare manufacturing app
echo "Installing healthcare manufacturing app..."
docker-compose -f docker-compose.simple.yml exec web bench get-app healthcare_manufacturing /home/frappe/frappe-bench/apps/healthcare_manufacturing
docker-compose -f docker-compose.simple.yml exec web bench --site healthcare-erp.local install-app healthcare_manufacturing

# Load seed data
echo "Loading seed data..."
docker-compose -f docker-compose.simple.yml exec web python /home/frappe/frappe-bench/apps/healthcare_manufacturing/scripts/seed_data.py

echo "Setup complete!"
echo "Access the application at: http://localhost:8000"
echo "Username: Administrator"
echo "Password: admin"