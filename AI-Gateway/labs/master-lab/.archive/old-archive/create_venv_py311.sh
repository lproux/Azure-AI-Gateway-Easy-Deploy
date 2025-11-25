#!/bin/bash
# Create new Python 3.11 venv for AutoGen 0.2.x compatibility

echo "🔧 Creating new Python 3.11 virtual environment..."

# Check if Python 3.11 is available
if command -v python3.11 &> /dev/null; then
    python3.11 -m venv .venv-py311
    echo "✅ Created .venv-py311 with Python 3.11"
elif command -v py -3.11 &> /dev/null; then
    py -3.11 -m venv .venv-py311
    echo "✅ Created .venv-py311 with Python 3.11"
else
    echo "❌ Python 3.11 not found. Please install Python 3.11 first."
    echo "   Download from: https://www.python.org/downloads/"
    exit 1
fi

echo ""
echo "📦 Installing dependencies..."
.venv-py311/Scripts/python.exe -m pip install --upgrade pip
.venv-py311/Scripts/python.exe -m pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. In VS Code, select the new kernel:"
echo "   - Press Ctrl+Shift+P"
echo "   - Type 'Python: Select Interpreter'"
echo "   - Choose: .venv-py311\\Scripts\\python.exe"
echo "2. Restart the kernel"
echo "3. Run your notebook cells"
