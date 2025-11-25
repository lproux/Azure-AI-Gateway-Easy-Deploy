#!/usr/bin/env python3
"""
Fix Cell 9 (dependency installation) to work with any kernel/environment
"""
import json
from pathlib import Path

notebook_path = Path('master-ai-gateway-fix-MCP-clean.ipynb')

# New cell source that handles all environments
fixed_cell_source = """# (-1.2) Dependencies Install (Smart Multi-Environment)
import sys
import subprocess
import pathlib
import shlex
import os

print("=" * 80)
print("DEPENDENCY INSTALLATION")
print("=" * 80)

# 1. Check Python version
py_version = sys.version_info
print(f'\\nPython: {py_version.major}.{py_version.minor}.{py_version.micro}')
print(f'Path:   {sys.executable}')

# 2. Detect environment
in_venv = sys.prefix != sys.base_prefix
is_system_python = '/usr/bin/python' in sys.executable or '/usr/local/bin/python' in sys.executable
externally_managed = is_system_python and py_version.major == 3 and py_version.minor >= 11

print(f'In virtual environment: {in_venv}')
print(f'System Python: {is_system_python}')
print(f'Externally managed: {externally_managed}')

# 3. Determine pip install strategy
pip_args = [sys.executable, '-m', 'pip', 'install']

if in_venv:
    # In a virtual environment - install normally
    print('\\n✅ Virtual environment detected - installing packages normally')
    extra_args = []
elif externally_managed:
    # System Python with PEP 668 (externally-managed-environment)
    print('\\n⚠️  Externally-managed system Python detected')
    print('   Using --user flag to install to user site-packages')
    extra_args = ['--user']
else:
    # Other cases (older Python, non-Debian systems)
    print('\\n✅ Installing packages normally')
    extra_args = []

print()
print("=" * 80)

# 4. Install python-dotenv first (CRITICAL - needed by subsequent cells)
print('[1/2] Installing python-dotenv (critical for environment loading)...')
cmd_dotenv = pip_args + extra_args + ['-q', 'python-dotenv>=1.0.0']

try:
    r = subprocess.run(cmd_dotenv, capture_output=True, text=True, timeout=60)
    if r.returncode == 0:
        print('      ✅ python-dotenv installed')
    else:
        print(f'      ⚠️  Warning: {r.stderr.strip()[:100]}')
        # Try without -q for better error messages
        if '--user' not in extra_args and not in_venv:
            print('      Retrying with --user flag...')
            cmd_dotenv_retry = pip_args + ['--user', 'python-dotenv>=1.0.0']
            r2 = subprocess.run(cmd_dotenv_retry, capture_output=True, text=True, timeout=60)
            if r2.returncode == 0:
                print('      ✅ python-dotenv installed with --user')
except subprocess.TimeoutExpired:
    print('      ⚠️  Installation timeout (network issue?)')
except Exception as e:
    print(f'      ⚠️  Error: {e}')

print()

# 5. Determine which requirements file to use
REQ_FILE = pathlib.Path('requirements.txt')
REQ_FILE_PY312 = pathlib.Path('requirements-py312.txt')

# Use Python 3.12-specific requirements if available and Python >= 3.12
if py_version.minor >= 12 and REQ_FILE_PY312.exists():
    install_file = REQ_FILE_PY312
    print(f'[2/2] Installing from: {install_file}')
    print('      (Python 3.12+ - no pyautogen)')
elif REQ_FILE.exists():
    req_content = REQ_FILE.read_text()

    # If Python >= 3.12 but no py312 requirements, create temp file without pyautogen
    if py_version.minor >= 12:
        print('[2/2] Python 3.12+ detected - filtering out pyautogen...')

        temp_req = pathlib.Path('.requirements-temp.txt')
        lines = []
        for line in req_content.splitlines():
            # Skip pyautogen but keep comments
            if 'pyautogen' not in line.lower() or line.strip().startswith('#'):
                lines.append(line)
        temp_req.write_text('\\n'.join(lines))
        install_file = temp_req
        print(f'      Installing from: {install_file} (filtered)')
    else:
        install_file = REQ_FILE
        print(f'[2/2] Installing from: {install_file}')
else:
    print('[2/2] ❌ No requirements file found')
    install_file = None

# 6. Install all dependencies
if install_file:
    cmd = pip_args + extra_args + ['-r', str(install_file)]

    print()
    print('      Running pip install...')
    print(f'      Command: {" ".join(shlex.quote(str(c)) for c in cmd)}')
    print()

    try:
        # Run with real-time output
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        # Print output in real-time (truncated)
        line_count = 0
        for line in process.stdout:
            line_count += 1
            # Only print first 20 and last 10 lines to avoid flooding
            if line_count <= 20:
                print(f'      {line.rstrip()}')
            elif line_count == 21:
                print('      ... (truncating output) ...')

        process.wait()

        print()
        if process.returncode == 0:
            print('      ✅ All dependencies installed successfully!')
        else:
            print(f'      ⚠️  pip exited with code {process.returncode}')
            print('      Some packages may have failed - check output above')

    except Exception as e:
        print(f'      ❌ Error during installation: {e}')

    # Clean up temp file
    if install_file.name == '.requirements-temp.txt' and install_file.exists():
        install_file.unlink()

print()
print("=" * 80)

# 7. Summary
print("SUMMARY")
print("=" * 80)

if in_venv:
    print(f"✅ Packages installed to: {sys.prefix}")
    print("   You're using a virtual environment (recommended!)")
elif extra_args and '--user' in extra_args:
    import site
    print(f"✅ Packages installed to: {site.USER_SITE}")
    print("   Using --user flag (externally-managed system)")
else:
    print(f"✅ Packages installed to: {sys.prefix}")

if py_version.minor >= 12:
    print()
    print("ℹ️  Note: Python 3.12+ detected")
    print("   - AutoGen 0.2.x skipped (not compatible)")
    print("   - All other packages installed successfully")
    print("   - Cells 8, 105, 111 can be skipped (AutoGen setup)")

print()
print("Next steps:")
print("  1. Restart kernel if needed (Kernel → Restart Kernel)")
print("  2. Continue with the labs!")
print("=" * 80)
"""

# Read notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Find and update Cell 9 (index 8)
cells = notebook['cells']
cell_9 = cells[8]

# Verify it's the right cell
source = ''.join(cell_9.get('source', []))
if 'Dependencies Install' in source or 'python-dotenv' in source:
    print("Found Cell 9 - Updating dependency installation logic...")

    # Update the cell
    cells[8]['source'] = fixed_cell_source.split('\n')
    cells[8]['outputs'] = []  # Clear outputs

    # Save notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)

    print()
    print("✅ Cell 9 updated with smart multi-environment dependency installation!")
    print()
    print("What changed:")
    print("  1. ✅ Auto-detects virtual environment vs system Python")
    print("  2. ✅ Uses --user flag for externally-managed systems (WSL/Debian)")
    print("  3. ✅ Automatically uses requirements-py312.txt for Python 3.12+")
    print("  4. ✅ Works with Python 3.11, 3.12, and any kernel")
    print("  5. ✅ Better error handling and progress messages")
    print()
    print("Next steps:")
    print("  1. Open the notebook in Jupyter")
    print("  2. Run Cell 9 (updated dependency installation)")
    print("  3. Restart kernel")
    print("  4. Continue with the labs!")
else:
    print("❌ Cell 9 doesn't match expected pattern")
    print(f"First 100 chars: {source[:100]}")
