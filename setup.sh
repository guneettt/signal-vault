#!/bin/bash

# SignalVault Setup Script
# This script sets up the Python environment and installs dependencies

echo "🚀 Setting up SignalVault Emergency Information Hub"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "✅ Found Python $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete! 🎉"
echo ""
echo "To run SignalVault:"
echo "  1. Activate the virtual environment: source .venv/bin/activate"
echo "  2. Run the application: python app.py"
echo "  3. Open your browser to: http://127.0.0.1:5000"
echo ""
echo "For CLI interface: python main.py"
echo ""
echo "Need help? Check the README.md file for detailed instructions."
