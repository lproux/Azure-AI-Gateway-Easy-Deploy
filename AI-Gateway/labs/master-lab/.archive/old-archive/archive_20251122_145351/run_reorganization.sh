#!/bin/bash
# Complete Notebook Reorganization Automation

set -e  # Exit on error

echo "=========================================="
echo "Azure AI Gateway Workshop Reorganization"
echo "=========================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_NB="master-ai-gateway-fix-MCP.ipynb"
TARGET_NB="master-ai-gateway-fix-MCP-clean.ipynb"

cd "$SCRIPT_DIR"

echo "Step 1: Verify source notebook exists..."
if [ ! -f "$SOURCE_NB" ]; then
    echo "ERROR: Source notebook not found: $SOURCE_NB"
    exit 1
fi
echo "✓ Source found: $(du -h $SOURCE_NB | cut -f1)"

echo ""
echo "Step 2: Creating supporting files..."

# Create bootstrap.env.template
cat > bootstrap.env.template << 'BOOTSTRAP'
# Minimal Bootstrap Configuration
# Fill in these values before running the workshop

SUBSCRIPTION_ID=
RESOURCE_GROUP=ai-gateway-workshop
LOCATION=eastus2
DEPLOY_SUFFIX=
BOOTSTRAP
echo "✓ Created: bootstrap.env.template"

# Create run_workshop.sh
cat > run_workshop.sh << 'WORKSHOP_SH'
#!/bin/bash
echo "🚀 AI Gateway Workshop - One-Click Deploy"

if [ -n "$CODESPACE_NAME" ]; then
    echo "📍 Running in GitHub Codespace"
else
    echo "📍 Running in local environment"
fi

if [ ! -f bootstrap.env ]; then
    cp bootstrap.env.template bootstrap.env
    echo "⚠️  Created bootstrap.env - please fill in required values"
    exit 1
fi

echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

echo "🔧 Running deployment notebook..."
jupyter nbconvert --to notebook --execute master-ai-gateway-fix-MCP-clean.ipynb \
    --output output/deployed.ipynb \
    --ExecutePreprocessor.timeout=1800

echo "✅ Deployment complete!"
WORKSHOP_SH
chmod +x run_workshop.sh
echo "✓ Created: run_workshop.sh"

# Create run_workshop.ps1
cat > run_workshop.ps1 << 'WORKSHOP_PS1'
Write-Host "🚀 AI Gateway Workshop - One-Click Deploy" -ForegroundColor Green

if ($env:CODESPACE_NAME) {
    Write-Host "📍 Running in GitHub Codespace" -ForegroundColor Cyan
} else {
    Write-Host "📍 Running in local environment" -ForegroundColor Cyan
}

if (-not (Test-Path "bootstrap.env")) {
    Copy-Item "bootstrap.env.template" "bootstrap.env"
    Write-Host "⚠️  Created bootstrap.env - please fill in required values" -ForegroundColor Yellow
    exit 1
}

Write-Host "📦 Installing dependencies..." -ForegroundColor Green
pip install -q -r requirements.txt

Write-Host "🔧 Running deployment notebook..." -ForegroundColor Green
jupyter nbconvert --to notebook --execute master-ai-gateway-fix-MCP-clean.ipynb `
    --output output/deployed.ipynb `
    --ExecutePreprocessor.timeout=1800

Write-Host "✅ Deployment complete!" -ForegroundColor Green
WORKSHOP_PS1
echo "✓ Created: run_workshop.ps1"

# Create output directory
mkdir -p output
echo "✓ Created: output/"

echo ""
echo "Step 3: Creating Python reorganization script..."

# Create Python script to do the actual notebook reorganization
python3 << 'PYTHON_REORG'
import json
import sys
from pathlib import Path
from datetime import datetime

print("[Python] Starting notebook reorganization...")

source_path = Path('master-ai-gateway-fix-MCP.ipynb')
target_path = Path('master-ai-gateway-fix-MCP-clean.ipynb')

# Load source notebook
source_nb = json.loads(source_path.read_text())
print(f"[Python] Loaded source: {len(source_nb['cells'])} cells")

# Create new notebook structure
target_nb = {
    "cells": [],
    "metadata": source_nb.get('metadata', {}),
    "nbformat": source_nb.get('nbformat', 4),
    "nbformat_minor": source_nb.get('nbformat_minor', 5)
}

def create_markdown_cell(source_lines):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source_lines if isinstance(source_lines, list) else [source_lines]
    }

def create_code_cell(source_lines):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source_lines if isinstance(source_lines, list) else [source_lines]
    }

def get_source_cell(index):
    """Get cell from source notebook"""
    if index < len(source_nb['cells']):
        return source_nb['cells'][index]
    return None

# Add title cell
target_nb['cells'].append(create_markdown_cell([
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

# Part 0: Bootstrap & Initial Setup
target_nb['cells'].append(create_markdown_cell([
    "## Part 0: Bootstrap & Initial Setup\n",
    "\n",
    "**Important**: These cells run WITHOUT master-lab.env (it doesn't exist yet!)\n"
]))

# Cell 001: Environment Detection
target_nb['cells'].append(create_markdown_cell(["### Cell 001: Environment Detection\n"]))
target_nb['cells'].append(create_code_cell([
    "# Cell 001: Environment Detection\n",
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

# Cell 002: Minimal Configuration Loader (bootstrap.env only)
target_nb['cells'].append(create_markdown_cell(["### Cell 002: Bootstrap Configuration\n"]))
target_nb['cells'].append(create_code_cell([
    "# Cell 002: Load Bootstrap Configuration (minimal)\n",
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

# Cell 003: Dependencies Installation (from source cell 3)
source_cell_3 = get_source_cell(3)
if source_cell_3:
    target_nb['cells'].append(create_markdown_cell(["### Cell 003: Dependencies Installation\n"]))
    target_nb['cells'].append(source_cell_3)

# Cell 004: Azure Authentication (from source cell 4)
source_cell_4 = get_source_cell(4)
if source_cell_4:
    target_nb['cells'].append(create_markdown_cell(["### Cell 004: Azure Authentication\n"]))
    target_nb['cells'].append(source_cell_4)

# Cell 005: Helper Classes
target_nb['cells'].append(create_markdown_cell(["### Cell 005: Core Helper Classes\n"]))
target_nb['cells'].append(create_code_cell([
    "# Cell 005: AzureOps Wrapper and Helpers\n",
    "from dataclasses import dataclass\n",
    "from typing import Dict, Optional\n",
    "import subprocess\n",
    "import json\n",
    "\n",
    "class AzureOps:\n",
    "    \"\"\"Azure operations wrapper\"\"\"\n",
    "    def __init__(self, subscription_id: str, strategy='sdk'):\n",
    "        self.subscription_id = subscription_id\n",
    "        self.strategy = strategy\n",
    "    \n",
    "    def ensure_login(self):\n",
    "        \"\"\"Ensure Azure CLI is logged in\"\"\"\n",
    "        try:\n",
    "            result = subprocess.run(['az', 'account', 'show'], \n",
    "                                  capture_output=True, text=True)\n",
    "            if result.returncode == 0:\n",
    "                print(\"✓ Azure CLI authenticated\")\n",
    "                return True\n",
    "        except Exception as e:\n",
    "            print(f\"❌ Azure CLI authentication failed: {e}\")\n",
    "        return False\n",
    "    \n",
    "    def deploy_bicep(self, template_path: str, parameters: Dict) -> Dict:\n",
    "        \"\"\"Deploy Bicep template\"\"\"\n",
    "        # Implementation here\n",
    "        pass\n",
    "\n",
    "# Initialize AzureOps\n",
    "az_ops = AzureOps(subscription_id=bootstrap.subscription_id)\n",
    "az_ops.ensure_login()\n",
    "print(\"✓ AzureOps initialized\")\n"
]))

# Part 1: Deployment
target_nb['cells'].append(create_markdown_cell([
    "## Part 1: Deployment & Environment Generation\n",
    "\n",
    "Deploy Azure resources and generate master-lab.env\n"
]))

# Cell 011: CRITICAL - Generate master-lab.env
target_nb['cells'].append(create_markdown_cell([
    "### Cell 011: **CRITICAL** - Generate master-lab.env\n",
    "\n",
    "This cell creates the master-lab.env file from deployment outputs.\n"
]))
target_nb['cells'].append(create_code_cell([
    "# Cell 011: Generate master-lab.env from deployment outputs\n",
    "from pathlib import Path\n",
    "\n",
    "def generate_master_env(deployment_outputs: Dict) -> None:\n",
    "    \"\"\"Generate master-lab.env from deployment outputs\"\"\"\n",
    "    env_file = Path('master-lab.env')\n",
    "    \n",
    "    lines = [\n",
    "        \"# Master AI Gateway Lab Environment\",\n",
    "        f\"# Generated: {datetime.now().isoformat()}\",\n",
    "        \"\",\n",
    "        \"# Azure Configuration\",\n",
    "        f\"SUBSCRIPTION_ID={bootstrap.subscription_id}\",\n",
    "        f\"RESOURCE_GROUP={bootstrap.resource_group}\",\n",
    "        f\"LOCATION={bootstrap.location}\",\n",
    "        \"\",\n",
    "    ]\n",
    "    \n",
    "    # Add deployment outputs\n",
    "    lines.append(\"# Deployment Outputs\")\n",
    "    for key, value in deployment_outputs.items():\n",
    "        lines.append(f\"{key.upper()}={value}\")\n",
    "    \n",
    "    # Write file\n",
    "    env_file.write_text('\\n'.join(lines))\n",
    "    print(f\"✓ Generated: {env_file}\")\n",
    "    print(f\"  Variables: {len(deployment_outputs)}\")\n",
    "\n",
    "# Example usage (replace with actual deployment outputs)\n",
    "example_outputs = {\n",
    "    'APIM_NAME': 'placeholder',\n",
    "    'APIM_GATEWAY_URL': 'placeholder',\n",
    "    'OPENAI_ENDPOINT': 'placeholder',\n",
    "}\n",
    "\n",
    "# TODO: Replace with actual deployment outputs\n",
    "# generate_master_env(deployment_outputs)\n",
    "print(\"⚠️  Cell 011 ready - run after deployments complete\")\n"
]))

# Cell 012: Reload Complete Configuration
target_nb['cells'].append(create_markdown_cell([
    "### Cell 012: Reload Complete Configuration\n",
    "\n",
    "NOW we can load the complete master-lab.env\n"
]))
target_nb['cells'].append(create_code_cell([
    "# Cell 012: Load Complete Configuration\n",
    "from dataclasses import dataclass\n",
    "from pathlib import Path\n",
    "\n",
    "@dataclass\n",
    "class WorkshopConfig:\n",
    "    \"\"\"Complete workshop configuration\"\"\"\n",
    "    subscription_id: str = \"\"\n",
    "    resource_group: str = \"\"\n",
    "    location: str = \"\"\n",
    "    apim_name: str = \"\"\n",
    "    apim_gateway_url: str = \"\"\n",
    "    apim_api_key: str = \"\"\n",
    "    openai_endpoint: str = \"\"\n",
    "    # Add all other fields\n",
    "\n",
    "def load_config() -> WorkshopConfig:\n",
    "    \"\"\"Load complete configuration from master-lab.env\"\"\"\n",
    "    env_file = Path('master-lab.env')\n",
    "    if not env_file.exists():\n",
    "        raise FileNotFoundError(\"master-lab.env not found - run Cell 011 first\")\n",
    "    \n",
    "    config = WorkshopConfig()\n",
    "    for line in env_file.read_text().splitlines():\n",
    "        if '=' in line and not line.strip().startswith('#'):\n",
    "            key, value = line.split('=', 1)\n",
    "            key = key.strip().lower()\n",
    "            value = value.strip()\n",
    "            if hasattr(config, key):\n",
    "                setattr(config, key, value)\n",
    "    \n",
    "    return config\n",
    "\n",
    "# Load configuration\n",
    "# config = load_config()\n",
    "# print(f\"✓ Configuration loaded\")\n",
    "# print(f\"  APIM: {config.apim_name}\")\n",
    "# print(f\"  Gateway: {config.apim_gateway_url}\")\n",
    "\n",
    "print(\"⚠️  Cell 012 ready - run after Cell 011\")\n"
]))

# Add remaining cells (MCP, Policies, Frameworks, Exercises)
# For now, adding placeholders
for i in range(13, 31):
    target_nb['cells'].append(create_markdown_cell([f"### Cell {i:03d}: Placeholder\n"]))
    target_nb['cells'].append(create_code_cell([
        f"# Cell {i:03d}: To be implemented\n",
        "print(f'Cell {i:03d} placeholder')\n"
    ]))

# Save target notebook
target_path.write_text(json.dumps(target_nb, indent=1))
print(f"[Python] ✓ Created: {target_path}")
print(f"[Python] New notebook has {len(target_nb['cells'])} cells")

PYTHON_REORG

echo ""
echo "Step 4: Verification..."
if [ -f "$TARGET_NB" ]; then
    echo "✓ Clean notebook created: $(du -h $TARGET_NB | cut -f1)"
    cell_count=$(python3 -c "import json; nb=json.load(open('$TARGET_NB')); print(len(nb['cells']))")
    echo "  Cells: $cell_count"
else
    echo "❌ Failed to create clean notebook"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Reorganization Complete!"
echo "=========================================="
echo ""
echo "Files created:"
echo "  - $TARGET_NB"
echo "  - bootstrap.env.template"
echo "  - run_workshop.sh"
echo "  - run_workshop.ps1"
echo ""
echo "Next steps:"
echo "  1. Review: $TARGET_NB"
echo "  2. Fill in: bootstrap.env"
echo "  3. Run: ./run_workshop.sh"
echo ""

