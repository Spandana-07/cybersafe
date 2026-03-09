#!/bin/bash
# Quick Start Script for CyberSafe Website (Windows/PowerShell)

echo "==============================================="
echo "CyberSafe - Cybersecurity Awareness Platform"
echo "==============================================="
echo ""

# Check if Python is installed
echo "Checking Python installation..."
python --version
if [ $? -ne 0 ]; then
    echo "Python is not installed or not in PATH"
    exit 1
fi

echo "✓ Python found"
echo ""

# Install dependencies
echo "Installing Python packages..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Packages installed successfully"
else
    echo "✗ Failed to install packages"
    exit 1
fi
echo ""

# Setup database
echo "Setting up MySQL database..."
python setup_database.py
if [ $? -eq 0 ]; then
    echo "✓ Database setup completed"
else
    echo "✗ Database setup failed - check MySQL connection"
fi
echo ""

# Run application
echo "Starting CyberSafe application..."
echo "Application will be available at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
