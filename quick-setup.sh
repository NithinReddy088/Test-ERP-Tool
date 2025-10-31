#!/bin/bash

echo "🏥 Healthcare Manufacturing ERP - Quick Setup"

# Clean up existing containers
echo "Cleaning up existing containers..."
sudo docker-compose down --remove-orphans 2>/dev/null || true
sudo docker-compose -f docker-compose.simple.yml down --remove-orphans 2>/dev/null || true

# Start database services
echo "Starting database services..."
sudo docker-compose -f docker-compose.working.yml up -d postgres redis

# Wait for database
echo "Waiting for database to initialize..."
sleep 15

# Start web service
echo "Starting web service..."
sudo docker-compose -f docker-compose.working.yml up -d web

# Wait for web service
echo "Waiting for web service to start..."
sleep 30

# Check if web is running
if sudo docker-compose -f docker-compose.working.yml ps | grep -q "healthcare_erp_web.*Up"; then
    echo "✅ Web service is running"
    
    # Create site
    echo "Creating Frappe site..."
    sudo docker-compose -f docker-compose.working.yml exec web bench new-site healthcare-erp.local --admin-password admin --install-app erpnext
    
    # Install healthcare app
    echo "Installing healthcare manufacturing app..."
    sudo docker-compose -f docker-compose.working.yml exec web bench get-app healthcare_manufacturing /home/frappe/frappe-bench/apps/healthcare_manufacturing
    sudo docker-compose -f docker-compose.working.yml exec web bench --site healthcare-erp.local install-app healthcare_manufacturing
    
    echo "🎉 Setup complete!"
    echo "Access: http://localhost:8000"
    echo "Username: Administrator"
    echo "Password: admin"
else
    echo "❌ Web service failed to start. Check logs:"
    sudo docker-compose -f docker-compose.working.yml logs web
fi