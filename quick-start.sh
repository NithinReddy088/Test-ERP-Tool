#!/bin/bash

set -e

echo "=========================================="
echo "Healthcare Equipment ERP - Quick Start"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}Please do not run as root${NC}"
    exit 1
fi

# Function to check command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command_exists python3; then
    echo -e "${RED}Python 3 is not installed${NC}"
    exit 1
fi

if ! command_exists node; then
    echo -e "${RED}Node.js is not installed${NC}"
    exit 1
fi

if ! command_exists redis-cli; then
    echo -e "${RED}Redis is not installed${NC}"
    exit 1
fi

if ! command_exists mysql || ! command_exists mariadb; then
    echo -e "${RED}MariaDB/MySQL is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites met${NC}"
echo ""

# Install frappe-bench if not exists
if ! command_exists bench; then
    echo -e "${YELLOW}Installing frappe-bench...${NC}"
    pip3 install frappe-bench
    echo -e "${GREEN}✓ Frappe bench installed${NC}"
else
    echo -e "${GREEN}✓ Frappe bench already installed${NC}"
fi

# Set variables
BENCH_DIR="healthcare_erp_bench"
SITE_NAME="healthcare.localhost"
ADMIN_PASSWORD="admin"

# Initialize bench
if [ ! -d "$BENCH_DIR" ]; then
    echo -e "${YELLOW}Initializing Frappe bench...${NC}"
    bench init $BENCH_DIR --frappe-branch version-15
    echo -e "${GREEN}✓ Bench initialized${NC}"
else
    echo -e "${GREEN}✓ Bench directory already exists${NC}"
fi

cd $BENCH_DIR

# Create site
if [ ! -d "sites/$SITE_NAME" ]; then
    echo -e "${YELLOW}Creating site: $SITE_NAME${NC}"
    bench new-site $SITE_NAME --admin-password $ADMIN_PASSWORD --no-mariadb-socket
    echo -e "${GREEN}✓ Site created${NC}"
else
    echo -e "${GREEN}✓ Site already exists${NC}"
fi

# Get ERPNext
if [ ! -d "apps/erpnext" ]; then
    echo -e "${YELLOW}Getting ERPNext app...${NC}"
    bench get-app erpnext --branch version-15
    echo -e "${GREEN}✓ ERPNext downloaded${NC}"
else
    echo -e "${GREEN}✓ ERPNext already exists${NC}"
fi

# Install ERPNext
echo -e "${YELLOW}Installing ERPNext on site...${NC}"
bench --site $SITE_NAME install-app erpnext || echo "ERPNext may already be installed"
echo -e "${GREEN}✓ ERPNext installed${NC}"

# Get healthcare_manufacturing app
APP_PATH="$(dirname $(pwd))/healthcare_manufacturing"
if [ ! -d "apps/healthcare_manufacturing" ]; then
    echo -e "${YELLOW}Getting healthcare_manufacturing app...${NC}"
    if [ -d "$APP_PATH" ]; then
        bench get-app $APP_PATH
        echo -e "${GREEN}✓ Healthcare Manufacturing app added${NC}"
    else
        echo -e "${RED}Healthcare Manufacturing app not found at $APP_PATH${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ Healthcare Manufacturing app already exists${NC}"
fi

# Install healthcare_manufacturing
echo -e "${YELLOW}Installing healthcare_manufacturing on site...${NC}"
bench --site $SITE_NAME install-app healthcare_manufacturing || echo "App may already be installed"
echo -e "${GREEN}✓ Healthcare Manufacturing installed${NC}"

# Set site as default
bench use $SITE_NAME

# Enable developer mode (optional)
echo -e "${YELLOW}Enabling developer mode...${NC}"
bench --site $SITE_NAME set-config developer_mode 1
echo -e "${GREEN}✓ Developer mode enabled${NC}"

# Clear cache
echo -e "${YELLOW}Clearing cache...${NC}"
bench --site $SITE_NAME clear-cache
echo -e "${GREEN}✓ Cache cleared${NC}"

echo ""
echo "=========================================="
echo -e "${GREEN}Installation Complete!${NC}"
echo "=========================================="
echo ""
echo "To start the application:"
echo -e "${YELLOW}cd $BENCH_DIR && bench start${NC}"
echo ""
echo "Access the application at:"
echo -e "${GREEN}http://localhost:8000${NC}"
echo ""
echo "Login credentials:"
echo "  Username: Administrator"
echo "  Password: $ADMIN_PASSWORD"
echo ""
echo "To load seed data:"
echo -e "${YELLOW}bench --site $SITE_NAME execute healthcare_manufacturing.setup.seed_data.load_seed_data${NC}"
echo ""
echo "For production setup:"
echo -e "${YELLOW}sudo bench setup production \$USER${NC}"
echo ""
