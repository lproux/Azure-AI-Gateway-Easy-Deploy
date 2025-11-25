#!/usr/bin/env python3
"""Update cell 4 with fixed path detection"""

import json

# Load notebook
with open('master-ai-gateway-fix-MCP-clean.ipynb', 'r') as f:
    nb = json.load(f)

# Cell 4 is at index 5
cell_idx = 5

# New source with fixed path detection and debugging
new_source = r"""# Cell 005: Load Bootstrap Configuration (minimal)
from pathlib import Path
from dataclasses import dataclass
import os

# Get notebook directory (works regardless of kernel working directory)
NOTEBOOK_DIR = None

print("[*] Detecting notebook directory...")
print(f"    Current working directory: {Path.cwd()}")

# Method 1: Check if we're in the right directory already
if Path('bootstrap.env').exists() or Path('bootstrap.env.template').exists():
    NOTEBOOK_DIR = Path.cwd()
    print(f"[OK] Method 1: Found in current directory")

# Method 2: Use known absolute path
if NOTEBOOK_DIR is None:
    # Fixed: Use raw string properly (single backslashes with r prefix)
    known_path = Path(r'C:\Users\lproux\Documents\GitHub\MCP-servers-internalMSFT-and-external\AI-Gateway\labs\master-lab')
    print(f"[*] Method 2: Checking known path: {known_path}")
    print(f"    Path exists: {known_path.exists()}")

    if known_path.exists():
        NOTEBOOK_DIR = known_path
        print(f"[OK] Method 2: Using known path")

# Method 3: Search parent directories
if NOTEBOOK_DIR is None:
    print(f"[*] Method 3: Searching parent directories...")
    current = Path.cwd()
    for level in range(5):  # Check up to 5 parent levels
        print(f"    Checking: {current}")
        if (current / 'bootstrap.env').exists() or (current / 'bootstrap.env.template').exists():
            NOTEBOOK_DIR = current
            print(f"[OK] Method 3: Found at level {level}")
            break
        current = current.parent

# Method 4: Try to find by looking for master-lab folder
if NOTEBOOK_DIR is None:
    print(f"[*] Method 4: Searching for master-lab folder...")
    current = Path.cwd()
    # Check if we're inside master-lab somewhere
    for parent in [current] + list(current.parents):
        if parent.name == 'master-lab' and (parent / 'bootstrap.env.template').exists():
            NOTEBOOK_DIR = parent
            print(f"[OK] Method 4: Found master-lab folder: {parent}")
            break

if NOTEBOOK_DIR is None:
    # Last resort: List what's in current directory to help debug
    print("\n[!] DEBUG: Files in current directory:")
    try:
        for item in list(Path.cwd().iterdir())[:20]:  # Show first 20
            print(f"    - {item.name}")
    except Exception as e:
        print(f"    Error listing: {e}")

    raise ValueError(
        "Cannot locate notebook directory.\n"
        f"Current directory: {Path.cwd()}\n"
        "Expected to find: bootstrap.env or bootstrap.env.template\n"
        "\n"
        "Please either:\n"
        "1. Run from: C:\\Users\\lproux\\Documents\\GitHub\\MCP-servers-internalMSFT-and-external\\AI-Gateway\\labs\\master-lab\n"
        "2. Or ensure bootstrap.env.template exists in the notebook directory"
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

# Load ONLY bootstrap values (not full master-lab.env)
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
        f"Please create bootstrap.env with:\n"
        f"  SUBSCRIPTION_ID=your-subscription-id\n"
        f"  RESOURCE_GROUP=ai-gateway-workshop\n"
        f"  LOCATION=eastus2"
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

print("✓ Updated Cell 004 with:")
print("  1. Fixed path escaping (raw string with single backslashes)")
print("  2. Added 4th detection method (search for master-lab folder)")
print("  3. Added debug output to show what's being checked")
print("  4. Shows files in current directory if all methods fail")
print("  5. Better error messages with actual paths")
print("\nRun Cell 004 and you'll see detailed detection progress!")
