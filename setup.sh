#!/bin/bash

# GTO Wizard Scraper Setup Script
# This script sets up the entire environment and runs the scraper

set -e  # Exit on any error

echo "=========================================="
echo "GTO WIZARD SCRAPER SETUP"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✓ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

echo "✓ pip3 found"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo "✓ Python packages installed"

# Install Playwright browsers
echo ""
echo "Installing Playwright browsers..."
python3 -m playwright install chromium

echo "✓ Playwright browsers installed"

# Check if we can run the token grabber
echo ""
echo "Testing token grabber..."
if python3 token_grabber.py --help &> /dev/null; then
    echo "✓ Token grabber is working"
else
    echo "❌ Token grabber test failed"
    exit 1
fi

echo ""
echo "=========================================="
echo "SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Run: python3 token_grabber_selenium.py --update-scraper"
echo "2. Run: python3 scraper.py"
echo ""