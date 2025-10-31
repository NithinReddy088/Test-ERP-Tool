#!/bin/bash

echo "🏥 Starting Healthcare Manufacturing ERP System..."

# Install Flask if not installed
pip3 install flask 2>/dev/null || echo "Flask already installed"

# Start the ERP server
python3 run-local.py