#!/bin/bash
# Auto-install script for Image2STL dependencies
# This script sets up a virtual environment and installs all required packages

echo "========================================"
echo "Image2STL - Dependency Auto-Installer"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    echo "Please install Python 3.8+ using your package manager:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-venv python3-dev"
    echo "  macOS: brew install python3"
    exit 1
fi

echo "Python found:"
python3 --version
echo ""

# Check if virtual environment already exists
if [ -d ".venv" ]; then
    echo "Virtual environment already exists."
    echo "Activating virtual environment..."
else
    echo "Creating virtual environment..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
fi

echo ""
echo "Activating virtual environment..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment"
    exit 1
fi

echo ""
echo "Upgrading pip..."
python -m pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "Warning: Failed to upgrade pip, continuing anyway..."
fi

echo ""
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo ""
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "Virtual environment is located in: .venv/"
echo ""
echo "To activate the environment in the future, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To run the GUI app:"
echo "  python gui.py"
echo ""
echo "To run the CLI:"
echo "  python -m src.cli.main --help"
echo ""
