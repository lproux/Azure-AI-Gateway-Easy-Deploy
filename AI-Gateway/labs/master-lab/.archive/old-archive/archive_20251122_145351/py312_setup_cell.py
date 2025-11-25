#!/usr/bin/env python3
"""
Add Python 3.12 setup cell to notebook
"""
import json
from pathlib import Path

notebook_path = Path('master-ai-gateway-fix-MCP-clean.ipynb')

# Cell source for Python 3.12 virtual environment setup
py312_setup_cell = """# Python 3.12 Virtual Environment Setup
# ============================================================================
# Run this cell ONCE to create a Python 3.12 virtual environment
# Then install this as your Jupyter kernel
# ============================================================================

import sys
import subprocess
import os
from pathlib import Path

print("=" * 80)
print("Python 3.12 Virtual Environment Setup")
print("=" * 80)
print()

# Check Python version
python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
print(f"Current Python: {python_version}")
print(f"Python path: {sys.executable}")
print()

# Check if running in WSL
is_wsl = os.path.exists('/proc/version') and 'microsoft' in open('/proc/version').read().lower()
if is_wsl:
    print("✅ Running in WSL")
    print()

# Virtual environment path
venv_path = Path('.venv-py312')

# Step 1: Create virtual environment if it doesn't exist
if not venv_path.exists():
    print("[1/4] Creating Python 3.12 virtual environment...")
    try:
        subprocess.run([
            'python3.12', '-m', 'venv', str(venv_path)
        ], check=True)
        print(f"✅ Virtual environment created: {venv_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment")
        print(f"   Error: {e}")
        print()
        print("💡 Make sure Python 3.12 is installed:")
        print("   sudo apt update")
        print("   sudo apt install python3.12 python3.12-venv python3-full")
        raise
else:
    print(f"[1/4] ✅ Virtual environment already exists: {venv_path}")

print()

# Step 2: Upgrade pip in virtual environment
print("[2/4] Upgrading pip...")
pip_path = venv_path / 'bin' / 'pip'
try:
    subprocess.run([
        str(pip_path), 'install', '--upgrade', 'pip'
    ], check=True, capture_output=True)
    print("✅ pip upgraded")
except subprocess.CalledProcessError as e:
    print(f"⚠️  pip upgrade warning (non-critical)")

print()

# Step 3: Install requirements
print("[3/4] Installing dependencies...")
requirements_file = 'requirements-py312.txt'

if not Path(requirements_file).exists():
    print(f"⚠️  {requirements_file} not found, using requirements.txt")
    requirements_file = 'requirements.txt'

try:
    result = subprocess.run([
        str(pip_path), 'install', '-r', requirements_file
    ], check=True, capture_output=True, text=True)
    print(f"✅ Dependencies installed from {requirements_file}")
except subprocess.CalledProcessError as e:
    print(f"❌ Failed to install dependencies")
    print(f"   Error: {e.stderr[:200]}")
    raise

print()

# Step 4: Install Jupyter kernel
print("[4/4] Installing Jupyter kernel...")
python_path = venv_path / 'bin' / 'python'
try:
    subprocess.run([
        str(python_path), '-m', 'ipykernel', 'install',
        '--user',
        '--name=py312-ai-gateway',
        '--display-name=Python 3.12 (AI Gateway)'
    ], check=True, capture_output=True)
    print("✅ Jupyter kernel installed: Python 3.12 (AI Gateway)")
except subprocess.CalledProcessError as e:
    print(f"⚠️  Kernel installation warning: {e.stderr.decode()[:100]}")

print()
print("=" * 80)
print("✅ Setup Complete!")
print("=" * 80)
print()
print("Next steps:")
print("  1. Kernel → Change Kernel → Python 3.12 (AI Gateway)")
print("  2. Kernel → Restart Kernel")
print("  3. Continue with the labs!")
print()
print("⚠️  Note: Skip cells 8, 105, 111 (AutoGen install - not needed)")
print()
"""

# Read notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Check if setup cell already exists
cells = notebook['cells']
setup_exists = False
for cell in cells:
    if cell.get('cell_type') == 'code':
        source = ''.join(cell.get('source', []))
        if 'Python 3.12 Virtual Environment Setup' in source:
            setup_exists = True
            print("Setup cell already exists in notebook")
            break

if not setup_exists:
    # Create new cell
    new_cell = {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': py312_setup_cell.split('\n')
    }

    # Insert at position 1 (after the first cell)
    cells.insert(1, new_cell)

    # Save notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)

    print("✅ Added Python 3.12 setup cell to notebook (Cell 2)")
    print()
    print("What this cell does:")
    print("  1. Creates .venv-py312 virtual environment")
    print("  2. Upgrades pip")
    print("  3. Installs all dependencies from requirements-py312.txt")
    print("  4. Registers Python 3.12 (AI Gateway) kernel in Jupyter")
    print()
    print("Next steps:")
    print("  1. Open the notebook in Jupyter")
    print("  2. Run Cell 2 (the new setup cell)")
    print("  3. Change kernel to: Python 3.12 (AI Gateway)")
    print("  4. Restart kernel and continue!")
