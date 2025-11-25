#!/bin/bash
# Setup Python 3.12 Virtual Environment for Master AI Gateway Lab
# Creates .venv-py312 with all compatible dependencies

set -e  # Exit on error

echo "=========================================="
echo "Python 3.12 Setup for Master AI Gateway"
echo "=========================================="
echo ""

# Check Python 3.12 is available
if ! command -v python3.12 &> /dev/null; then
    echo "❌ Python 3.12 not found"
    echo ""
    echo "Please install Python 3.12:"
    echo "  sudo apt update"
    echo "  sudo apt install python3.12 python3.12-venv python3-full"
    exit 1
fi

echo "✅ Found Python 3.12: $(python3.12 --version)"
echo ""

# Create virtual environment
VENV_DIR=".venv-py312"

if [ -d "$VENV_DIR" ]; then
    echo "⚠️  Virtual environment $VENV_DIR already exists"
    read -p "Remove and recreate? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing old virtual environment..."
        rm -rf "$VENV_DIR"
    else
        echo "Using existing virtual environment..."
    fi
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python 3.12 virtual environment..."
    python3.12 -m venv "$VENV_DIR"
    echo "✅ Virtual environment created: $VENV_DIR"
fi

echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "✅ Virtual environment activated"
echo "   Python: $(which python)"
echo "   Version: $(python --version)"
echo ""

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip
echo ""

# Install dependencies
echo "Installing dependencies from requirements-py312.txt..."
echo ""
python -m pip install -r requirements-py312.txt

echo ""
echo "=========================================="
echo "✅ Python 3.12 Setup Complete!"
echo "=========================================="
echo ""
echo "Virtual environment: $VENV_DIR"
echo "Python version: $(python --version)"
echo ""
echo "⚠️  IMPORTANT NOTES:"
echo "   - AutoGen 0.2.x cells will NOT work (Python 3.12 incompatible)"
echo "   - All other labs (1-13) will work perfectly"
echo "   - For full AutoGen support, use Python 3.11 (.venv-py311)"
echo ""
echo "To activate this environment:"
echo "  source $VENV_DIR/bin/activate"
echo ""
echo "To use in Jupyter:"
echo "  python -m ipykernel install --user --name=py312-ai-gateway --display-name='Python 3.12 (AI Gateway)'"
echo ""
echo "Next steps:"
echo "  1. Activate: source $VENV_DIR/bin/activate"
echo "  2. Install kernel: python -m ipykernel install --user --name=py312-ai-gateway"
echo "  3. Restart Jupyter"
echo "  4. Select kernel: Python 3.12 (AI Gateway)"
echo ""
