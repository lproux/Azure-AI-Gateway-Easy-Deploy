#!/bin/bash
# Install all requirements for master AI Gateway lab
# Run this after changing kernels or creating a new virtual environment

echo "=========================================="
echo "Installing Master AI Gateway Requirements"
echo "=========================================="
echo ""

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: No virtual environment detected"
    echo "   Consider activating .venv-py311 first:"
    echo "   source .venv-py311/bin/activate"
    echo ""
fi

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
echo "Python version: $python_version"
echo ""

# Install requirements
echo "Installing dependencies from requirements.txt..."
echo ""

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo ""
echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Restart your Jupyter kernel"
echo "  2. Run your notebook cells"
echo ""
