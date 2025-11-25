#!/usr/bin/env python3
"""Fix cell 4 to work with WSL paths"""

import json

# Load notebook
with open('master-ai-gateway-fix-MCP-clean.ipynb', 'r') as f:
    nb = json.load(f)

# Cell 4 is at index 5
cell_idx = 5

# New source with WSL-aware path detection
new_source = r"""# Cell 005: Load Bootstrap Configuration (minimal)
from pathlib import Path
from dataclasses import dataclass
import os
import sys

# Get notebook directory (works in WSL and Windows)
NOTEBOOK_DIR = None

print("[*] Detecting notebook directory...")
print(f"    Current working directory: {Path.cwd()}")
print(f"    Platform: {sys.platform}")

# Detect if running in WSL
IS_WSL = 'microsoft' in str(Path('/proc/version').read_text()).lower() if Path('/proc/version').exists() else False
if IS_WSL:
    print("    Environment: WSL (Windows Subsystem for Linux)")
else:
    print(f"    Environment: Native {sys.platform}")

# Method 1: Check if we're in the right directory already
if (Path.cwd() / 'bootstrap.env').exists() or (Path.cwd() / 'bootstrap.env.template').exists():
    NOTEBOOK_DIR = Path.cwd()
    print(f"[OK] Method 1: Found in current directory")

# Method 2: Use known absolute path (WSL-aware)
if NOTEBOOK_DIR is None:
    if IS_WSL:
        # WSL path format
        known_path = Path('/mnt/c/Users/lproux/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab')
    else:
        # Windows path format
        known_path = Path(r'C:\Users\lproux\Documents\GitHub\MCP-servers-internalMSFT-and-external\AI-Gateway\labs\master-lab')

    print(f"[*] Method 2: Checking known path: {known_path}")

    if known_path.exists():
        NOTEBOOK_DIR = known_path
        print(f"[OK] Method 2: Using known path")
    else:
        print(f"    Path does not exist")

# Method 3: Search parent directories
if NOTEBOOK_DIR is None:
    print(f"[*] Method 3: Searching parent directories...")
    current = Path.cwd()
    for level in range(5):
        print(f"    Checking: {current}")
        if (current / 'bootstrap.env').exists() or (current / 'bootstrap.env.template').exists():
            NOTEBOOK_DIR = current
            print(f"[OK] Method 3: Found at level {level}")
            break
        current = current.parent

# Method 4: Navigate from current directory if we see AI-Gateway
if NOTEBOOK_DIR is None:
    print(f"[*] Method 4: Looking for AI-Gateway in current directory...")
    current = Path.cwd()

    # Check if AI-Gateway exists in current dir
    ai_gateway = current / 'AI-Gateway'
    if ai_gateway.exists() and ai_gateway.is_dir():
        master_lab = ai_gateway / 'labs' / 'master-lab'
        print(f"    Found AI-Gateway, checking: {master_lab}")
        if master_lab.exists() and ((master_lab / 'bootstrap.env').exists() or (master_lab / 'bootstrap.env.template').exists()):
            NOTEBOOK_DIR = master_lab
            print(f"[OK] Method 4: Found via AI-Gateway navigation")

# Method 5: Search for master-lab folder in tree
if NOTEBOOK_DIR is None:
    print(f"[*] Method 5: Searching for master-lab folder...")
    current = Path.cwd()

    # Check current and all parents
    for parent in [current] + list(current.parents)[:5]:
        if parent.name == 'master-lab':
            if (parent / 'bootstrap.env').exists() or (parent / 'bootstrap.env.template').exists():
                NOTEBOOK_DIR = parent
                print(f"[OK] Method 5: Found master-lab folder: {parent}")
                break

        # Also check if master-lab exists as subdirectory
        master_lab_candidates = list(parent.glob('**/master-lab'))
        for candidate in master_lab_candidates[:3]:  # Check first 3 matches
            if (candidate / 'bootstrap.env').exists() or (candidate / 'bootstrap.env.template').exists():
                NOTEBOOK_DIR = candidate
                print(f"[OK] Method 5: Found master-lab via glob: {candidate}")
                break

        if NOTEBOOK_DIR:
            break

if NOTEBOOK_DIR is None:
    # Last resort: Show what's available
    print("\n[!] DEBUG: Current directory contents:")
    try:
        items = list(Path.cwd().iterdir())
        for item in items[:20]:
            marker = "DIR" if item.is_dir() else "   "
            print(f"    [{marker}] {item.name}")
    except Exception as e:
        print(f"    Error listing: {e}")

    raise ValueError(
        "Cannot locate notebook directory.\n"
        f"Current directory: {Path.cwd()}\n"
        f"Platform: {sys.platform} ({'WSL' if IS_WSL else 'Native'})\n"
        "Expected to find: bootstrap.env or bootstrap.env.template\n"
        "\n"
        "Possible solutions:\n"
        "1. Change to the notebook directory first:\n"
        "   import os\n"
        "   os.chdir(r'C:\\Users\\lproux\\Documents\\GitHub\\MCP-servers-internalMSFT-and-external\\AI-Gateway\\labs\\master-lab')\n"
        "   # or in WSL:\n"
        "   os.chdir('/mnt/c/Users/lproux/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab')\n"
        "\n"
        "2. Or create bootstrap.env.template in the current directory"
    )

# Change to notebook directory
os.chdir(NOTEBOOK_DIR)
print(f"\n[OK] Notebook directory: {NOTEBOOK_DIR}")
print(f"[OK] Changed working directory to: {Path.cwd()}")

@dataclass
class BootstrapConfig:
    subscription_id: str = ""
    resource_group: str = "ai-gateway-workshop"
    location: str = "eastus2"
    deploy_suffix: str = ""

# Use absolute path for bootstrap.env
bootstrap_file = NOTEBOOK_DIR / 'bootstrap.env'
if not bootstrap_file.exists():
    print(f"[WARN] bootstrap.env not found at: {bootstrap_file}")
    bootstrap_file = NOTEBOOK_DIR / 'bootstrap.env.template'
    print(f"[INFO] Using template: {bootstrap_file}")

# Load ONLY bootstrap values
bootstrap = BootstrapConfig()
if bootstrap_file.exists():
    print(f"[OK] Loading from: {bootstrap_file}")
    for line in bootstrap_file.read_text().splitlines():
        if '=' in line and not line.strip().startswith('#'):
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            if hasattr(bootstrap, key.lower()):
                setattr(bootstrap, key.lower(), value)
else:
    raise FileNotFoundError(
        f"Bootstrap file not found at: {bootstrap_file}\n"
        f"Please create bootstrap.env"
    )

print(f"\nBootstrap Configuration:")
print(f"  Subscription: {bootstrap.subscription_id or 'NOT SET'}")
print(f"  Resource Group: {bootstrap.resource_group}")
print(f"  Location: {bootstrap.location}")

# Validate
if not bootstrap.subscription_id:
    raise ValueError(
        "SUBSCRIPTION_ID must be set in bootstrap.env\n"
        f"File location: {bootstrap_file}\n"
        "Please edit the file and add your Azure subscription ID."
    )

print(f"\n[OK] Bootstrap configuration loaded successfully")
"""

# Update cell
nb['cells'][cell_idx]['source'] = [new_source]

# Save
with open('master-ai-gateway-fix-MCP-clean.ipynb', 'w') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("✓ Updated Cell 004 with WSL-aware path detection")
print("\nNew features:")
print("  1. Detects WSL environment automatically")
print("  2. Uses correct path format for WSL (/mnt/c/) or Windows (C:\\)")
print("  3. Method 4: Navigates from current dir if AI-Gateway exists")
print("  4. Method 5: Searches for master-lab in subdirectories")
print("  5. Shows [DIR] markers for directories in debug output")
