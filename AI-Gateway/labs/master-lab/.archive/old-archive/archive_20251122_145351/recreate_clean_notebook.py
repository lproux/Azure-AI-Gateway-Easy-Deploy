#!/usr/bin/env python3
"""
Recreate the clean notebook following the MANUAL_COPY_GUIDE.md specifications.
This automates the manual copy process described in the guides.
"""

import json
from pathlib import Path
from datetime import datetime

# Paths
SOURCE_NB = Path('master-ai-gateway-fix-MCP.ipynb')
TARGET_NB = Path('master-ai-gateway-fix-MCP-clean.ipynb')

def load_notebook(path):
    """Load a Jupyter notebook."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_markdown_cell(source):
    """Create a markdown cell."""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source if isinstance(source, list) else [source]
    }

def create_code_cell(source):
    """Create a code cell."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source if isinstance(source, list) else [source]
    }

def get_source_cell(source_nb, cell_index):
    """Get a cell from the source notebook by index."""
    if cell_index < len(source_nb['cells']):
        return source_nb['cells'][cell_index].copy()
    return None

def consolidate_cells(source_nb, cell_indices):
    """Consolidate multiple source cells into one."""
    sources = []
    for idx in cell_indices:
        cell = get_source_cell(source_nb, idx)
        if cell:
            sources.extend(cell['source'])
            sources.append('\n\n')
    return sources

# Load source notebook
print(f"Loading source notebook: {SOURCE_NB}")
source_nb = load_notebook(SOURCE_NB)
print(f"Source notebook has {len(source_nb['cells'])} cells")

# Create clean notebook structure
clean_nb = {
    "cells": [],
    "metadata": source_nb.get('metadata', {}),
    "nbformat": source_nb.get('nbformat', 4),
    "nbformat_minor": source_nb.get('nbformat_minor', 5)
}

# PART 0: Bootstrap & Initial Setup (Cells 001-012)
print("\nCreating PART 0: Bootstrap & Initial Setup")

# Cell 001: Title
clean_nb['cells'].append(create_markdown_cell([
    "# Master AI Gateway Workshop\n",
    "\n",
    "**One-Click Deployment for Azure AI Gateway with MCP Integration**\n",
    "\n",
    "## Deployment Flow\n",
    "1. **Bootstrap** - Minimal configuration (no master-lab.env needed)\n",
    "2. **Deploy** - Azure resources via Bicep\n",
    "3. **Generate** - Create master-lab.env from deployment outputs\n",
    "4. **Configure** - Load complete configuration\n",
    "5. **Run** - MCP servers, policies, exercises\n"
]))

# Cell 002: Part 0 Header
clean_nb['cells'].append(create_markdown_cell([
    "## Part 0: Bootstrap & Initial Setup\n",
    "\n",
    "**Important**: These cells run WITHOUT master-lab.env (it doesn't exist yet!)\n"
]))

# Cell 003: Environment Detection Header
clean_nb['cells'].append(create_markdown_cell([
    "### Cell 003: Environment Detection\n"
]))

# Cell 004: Environment Detection Code
clean_nb['cells'].append(create_code_cell([
    "# Cell 003: Environment Detection\n",
    "import os\n",
    "import sys\n",
    "from pathlib import Path\n",
    "\n",
    "# Detect environment\n",
    "IS_CODESPACE = bool(os.getenv('CODESPACE_NAME'))\n",
    "WORKSPACE_ROOT = Path.cwd()\n",
    "\n",
    "print(f\"Environment: {'GitHub Codespace' if IS_CODESPACE else 'Local'}\")\n",
    "print(f\"Workspace: {WORKSPACE_ROOT}\")\n",
    "print(f\"Python: {sys.version.split()[0]}\")\n"
]))

# Cell 005: Bootstrap Config Header
clean_nb['cells'].append(create_markdown_cell([
    "### Cell 005: Bootstrap Configuration (Minimal)\n",
    "Load ONLY subscription, resource group, location from bootstrap.env\n"
]))

# Cell 006: Bootstrap Config Code
clean_nb['cells'].append(create_code_cell([
    "# Cell 005: Load Bootstrap Configuration (minimal)\n",
    "from pathlib import Path\n",
    "from dataclasses import dataclass\n",
    "\n",
    "@dataclass\n",
    "class BootstrapConfig:\n",
    "    subscription_id: str = \"\"\n",
    "    resource_group: str = \"ai-gateway-workshop\"\n",
    "    location: str = \"eastus2\"\n",
    "    deploy_suffix: str = \"\"\n",
    "\n",
    "bootstrap_file = Path('bootstrap.env')\n",
    "if not bootstrap_file.exists():\n",
    "    print(\"⚠️  bootstrap.env not found, using template\")\n",
    "    bootstrap_file = Path('bootstrap.env.template')\n",
    "\n",
    "# Load ONLY bootstrap values (not full master-lab.env)\n",
    "bootstrap = BootstrapConfig()\n",
    "if bootstrap_file.exists():\n",
    "    for line in bootstrap_file.read_text().splitlines():\n",
    "        if '=' in line and not line.strip().startswith('#'):\n",
    "            key, value = line.split('=', 1)\n",
    "            key = key.strip()\n",
    "            value = value.strip()\n",
    "            if hasattr(bootstrap, key.lower()):\n",
    "                setattr(bootstrap, key.lower(), value)\n",
    "\n",
    "print(f\"Subscription: {bootstrap.subscription_id or 'NOT SET'}\")\n",
    "print(f\"Resource Group: {bootstrap.resource_group}\")\n",
    "print(f\"Location: {bootstrap.location}\")\n",
    "\n",
    "# Validate\n",
    "if not bootstrap.subscription_id:\n",
    "    raise ValueError(\"SUBSCRIPTION_ID must be set in bootstrap.env\")\n"
]))

# Cell 007: Dependencies Header
clean_nb['cells'].append(create_markdown_cell([
    "### Cell 007: Dependencies Installation\n"
]))

# Cell 008: Dependencies - COPY FROM SOURCE CELL 3
print("  Copying Cell 008 from source cell 3...")
source_cell_3 = get_source_cell(source_nb, 3)
if source_cell_3:
    source_cell_3['execution_count'] = None
    source_cell_3['outputs'] = []
    clean_nb['cells'].append(source_cell_3)

# Cell 009: Azure Auth Header
clean_nb['cells'].append(create_markdown_cell([
    "### Cell 009: Azure Authentication & Service Principal\n"
]))

# Cell 010: Azure Auth - CONSOLIDATE SOURCE CELLS 5-7
print("  Consolidating Cell 010 from source cells 5-7...")
auth_sources = consolidate_cells(source_nb, [5, 6, 7])
clean_nb['cells'].append(create_code_cell(auth_sources))

# Cell 011: Helper Functions Header
clean_nb['cells'].append(create_markdown_cell([
    "### Cell 011: Core Helper Functions\n"
]))

# Cell 012: Helpers - CONSOLIDATE SOURCE CELLS 8-12
print("  Consolidating Cell 012 from source cells 8-12...")
helper_sources = consolidate_cells(source_nb, [8, 9, 10, 11, 12])
clean_nb['cells'].append(create_code_cell(helper_sources))

# PART 1: Deployment & Environment Generation (Cells 013-023)
print("\nCreating PART 1: Deployment & Environment Generation")

# Cell 013: Part 1 Header
clean_nb['cells'].append(create_markdown_cell([
    "## Part 1: Deployment & Environment Generation\n",
    "\n",
    "Deploy Azure resources and generate master-lab.env from outputs.\n"
]))

# Cell 014: Deployment Config Header
clean_nb['cells'].append(create_markdown_cell([
    "### Cell 014: Deployment Configuration\n"
]))

# Cell 015: Deployment Config - MODIFIED FROM SOURCE CELL 24
print("  Copying Cell 015 from source cell 24 (removing hardcoded subscription)...")
source_cell_24 = get_source_cell(source_nb, 24)
if source_cell_24:
    # Replace hardcoded subscription with bootstrap.subscription_id
    modified_source = []
    for line in source_cell_24['source']:
        if 'subscription_id' in line and '=' in line and 'd334f2cd' in line:
            modified_source.append('subscription_id = bootstrap.subscription_id\n')
        else:
            modified_source.append(line)
    source_cell_24['source'] = modified_source
    source_cell_24['execution_count'] = None
    source_cell_24['outputs'] = []
    clean_nb['cells'].append(source_cell_24)

# Cell 016: Deploy Infrastructure Header
clean_nb['cells'].append(create_markdown_cell([
    "### Cell 016: Deploy Infrastructure\n",
    "Run all 4 deployment steps\n"
]))

# Cells 017-018: Deployment Steps - FROM SOURCE CELLS 26-29
print("  Copying deployment cells 017-018 from source cells 26-29...")
for source_idx in [26, 27, 28, 29]:
    source_cell = get_source_cell(source_nb, source_idx)
    if source_cell:
        source_cell['execution_count'] = None
        source_cell['outputs'] = []
        clean_nb['cells'].append(source_cell)

# Cell 019: Deployment Complete Header
clean_nb['cells'].append(create_markdown_cell([
    "### Cell 019: Deployment Complete\n",
    "\n",
    "All Azure resources deployed. Outputs captured in `deployment_outputs`.\n"
]))

# Cell 020: Generate Env Header (CRITICAL)
clean_nb['cells'].append(create_markdown_cell([
    "### Cell 020: **CRITICAL** - Generate master-lab.env\n",
    "\n",
    "This cell creates the master-lab.env file from deployment outputs.\n",
    "DO NOT SKIP THIS CELL!\n"
]))

# Cell 021: Generate master-lab.env (ENHANCED FROM SOURCE CELLS 30-31)
print("  Creating CRITICAL Cell 021 (generate master-lab.env)...")
clean_nb['cells'].append(create_code_cell([
    "# Cell 021: Generate master-lab.env from deployment outputs\n",
    "from pathlib import Path\n",
    "from datetime import datetime\n",
    "\n",
    "def generate_master_env(outputs: dict) -> None:\n",
    "    \"\"\"Generate master-lab.env from deployment outputs\"\"\"\n",
    "    env_file = Path('master-lab.env')\n",
    "    \n",
    "    lines = [\n",
    "        \"# Master AI Gateway Lab Environment\",\n",
    "        f\"# Generated: {datetime.now().isoformat()}\",\n",
    "        \"\",\n",
    "        \"# Bootstrap Configuration\",\n",
    "        f\"SUBSCRIPTION_ID={bootstrap.subscription_id}\",\n",
    "        f\"RESOURCE_GROUP={bootstrap.resource_group}\",\n",
    "        f\"LOCATION={bootstrap.location}\",\n",
    "        \"\",\n",
    "    ]\n",
    "    \n",
    "    # Add all deployment outputs\n",
    "    lines.append(\"# Deployment Outputs\")\n",
    "    for key, value in outputs.items():\n",
    "        lines.append(f\"{key.upper()}={value}\")\n",
    "    \n",
    "    # Write file\n",
    "    env_file.write_text('\\n'.join(lines))\n",
    "    print(f\"✓ Generated: {env_file}\")\n",
    "    print(f\"  Total variables: {len(outputs) + 3}\")\n",
    "\n",
    "# Get deployment outputs (from previous cells)\n",
    "# deployment_outputs should be populated by Cell 017\n",
    "if 'deployment_outputs' in globals():\n",
    "    generate_master_env(deployment_outputs)\n",
    "    print(\"✓ master-lab.env created successfully!\")\n",
    "else:\n",
    "    print(\"⚠️  No deployment outputs found. Run Cell 017 first.\")\n"
]))

# Cell 022: Reload Config Header
clean_nb['cells'].append(create_markdown_cell([
    "### Cell 022: Reload Complete Configuration\n",
    "\n",
    "NOW we can load the complete master-lab.env\n"
]))

# Cell 023: Reload Config - MODIFIED FROM SOURCE CELL 32
print("  Copying Cell 023 from source cell 32...")
source_cell_32 = get_source_cell(source_nb, 32)
if source_cell_32:
    source_cell_32['execution_count'] = None
    source_cell_32['outputs'] = []
    clean_nb['cells'].append(source_cell_32)

# PART 2: MCP Server Configuration (Cells 024-035)
print("\nCreating PART 2: MCP Server Configuration")

# Cell 024: Part 2 Header
clean_nb['cells'].append(create_markdown_cell([
    "## Part 2: MCP Server Configuration\n"
]))

# Cells 025-035: MCP Setup - FROM SOURCE CELLS 79-89
print("  Copying MCP cells 025-035 from source cells 79-89...")
for source_idx in range(79, 90):
    source_cell = get_source_cell(source_nb, source_idx)
    if source_cell:
        source_cell['execution_count'] = None
        source_cell['outputs'] = []
        clean_nb['cells'].append(source_cell)

# PART 3: Security & Access Control (Cells 036-042)
print("\nCreating PART 3: Security & Access Control")

# Cell 036: Part 3 Header
clean_nb['cells'].append(create_markdown_cell([
    "## Part 3: Security & Access Control\n"
]))

# Cells 037-042: Access Control - FROM SOURCE CELLS 56-61 (PRESERVE EXACTLY)
print("  Copying Access Control cells 037-042 from source cells 56-61 (CRITICAL - preserving exactly)...")
for source_idx in range(56, 62):
    source_cell = get_source_cell(source_nb, source_idx)
    if source_cell:
        source_cell['execution_count'] = None
        source_cell['outputs'] = []
        clean_nb['cells'].append(source_cell)

# PART 4: Labs & Exercises (Cells 043-075)
print("\nCreating PART 4: Labs & Exercises")

# Cell 043: Part 4 Header
clean_nb['cells'].append(create_markdown_cell([
    "## Part 4: Labs & Exercises\n"
]))

# Cells 044-060: Basic Labs - FROM SOURCE CELLS 33-55
print("  Copying Labs cells 044-060 from source cells 33-55...")
for source_idx in range(33, 56):
    source_cell = get_source_cell(source_nb, source_idx)
    if source_cell:
        source_cell['execution_count'] = None
        source_cell['outputs'] = []
        clean_nb['cells'].append(source_cell)

# Cells 061-075: Advanced Labs - FROM SOURCE CELLS 62-77
print("  Copying Advanced Labs cells 061-075 from source cells 62-77...")
for source_idx in range(62, 78):
    source_cell = get_source_cell(source_nb, source_idx)
    if source_cell:
        source_cell['execution_count'] = None
        source_cell['outputs'] = []
        clean_nb['cells'].append(source_cell)

# PART 5: Framework Integration (Cells 076-089)
print("\nCreating PART 5: Framework Integration")

# Cell 076: Part 5 Header
clean_nb['cells'].append(create_markdown_cell([
    "## Part 5: Semantic Kernel & AutoGen\n"
]))

# Cell 077: SK & AutoGen Header - FROM SOURCE CELL 93
print("  Copying cell 077 from source cell 93...")
source_cell_93 = get_source_cell(source_nb, 93)
if source_cell_93:
    source_cell_93['execution_count'] = None
    source_cell_93['outputs'] = []
    clean_nb['cells'].append(source_cell_93)

# Cells 078-089: Framework Examples - FROM SOURCE CELLS 133-144
print("  Copying Framework cells 078-089 from source cells 133-144...")
for source_idx in range(133, 145):
    source_cell = get_source_cell(source_nb, source_idx)
    if source_cell:
        source_cell['execution_count'] = None
        source_cell['outputs'] = []
        clean_nb['cells'].append(source_cell)

# Save clean notebook
print(f"\nSaving clean notebook: {TARGET_NB}")
print(f"Total cells: {len(clean_nb['cells'])}")

with open(TARGET_NB, 'w', encoding='utf-8') as f:
    json.dump(clean_nb, f, indent=1, ensure_ascii=False)

print(f"\n✓ Clean notebook created successfully!")
print(f"  Source: {SOURCE_NB} ({len(source_nb['cells'])} cells)")
print(f"  Target: {TARGET_NB} ({len(clean_nb['cells'])} cells)")
print(f"  Reduction: {len(source_nb['cells']) - len(clean_nb['cells'])} cells ({100 * (len(source_nb['cells']) - len(clean_nb['cells'])) / len(source_nb['cells']):.1f}%)")
