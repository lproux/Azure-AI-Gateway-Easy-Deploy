#!/usr/bin/env python3
"""
Add a cell to the notebook for creating Service Principal
This way users never have to leave Jupyter!
"""

import json

print('[*] Reading notebook...')
with open('master-ai-gateway.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f'[*] Total cells: {len(nb["cells"])}')

# Create new cells for Service Principal creation
# Insert after Cell 9 (Azure Authentication)

sp_creation_cells = []

# Markdown header
sp_creation_cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Create Service Principal (One-Time Setup)\n",
        "\n",
        "**Run this cell ONCE to create a Service Principal for deployment.**\n",
        "\n",
        "This will:\n",
        "1. Create a Service Principal with Contributor role\n",
        "2. Save credentials to `.azure-credentials.env`\n",
        "3. Add the file to `.gitignore` (safe from git commits)\n",
        "\n",
        "**Skip this cell if you already have `.azure-credentials.env` file.**"
    ]
})

# Code cell
sp_creation_cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "import os\n",
        "import json\n",
        "import subprocess\n",
        "from datetime import datetime\n",
        "\n",
        "# Check if already exists\n",
        "if os.path.exists('.azure-credentials.env'):\n",
        "    print('[OK] .azure-credentials.env already exists!')\n",
        "    print('[OK] Skipping Service Principal creation')\n",
        "    print('[INFO] Delete .azure-credentials.env if you want to create a new one')\n",
        "else:\n",
        "    print('[*] Creating Service Principal...')\n",
        "    print()\n",
        "    \n",
        "    # Get subscription\n",
        "    result = subprocess.run(\n",
        "        'az account show --output json',\n",
        "        shell=True,\n",
        "        capture_output=True,\n",
        "        text=True\n",
        "    )\n",
        "    \n",
        "    if result.returncode != 0:\n",
        "        print('[ERROR] Failed to get subscription. Make sure you are logged in:')\n",
        "        print('        az login')\n",
        "    else:\n",
        "        sub_info = json.loads(result.stdout)\n",
        "        subscription_id = sub_info['id']\n",
        "        \n",
        "        print(f'[OK] Using subscription: {sub_info[\"name\"]}')\n",
        "        print()\n",
        "        \n",
        "        # Create Service Principal\n",
        "        sp_name = f'master-lab-sp-{datetime.now().strftime(\"%Y%m%d-%H%M%S\")}'\n",
        "        print(f'[*] Creating Service Principal: {sp_name}')\n",
        "        print('[*] Role: Contributor')\n",
        "        print()\n",
        "        \n",
        "        result = subprocess.run(\n",
        "            f'az ad sp create-for-rbac '\n",
        "            f'--name \"{sp_name}\" '\n",
        "            f'--role Contributor '\n",
        "            f'--scopes \"/subscriptions/{subscription_id}\" '\n",
        "            f'--output json',\n",
        "            shell=True,\n",
        "            capture_output=True,\n",
        "            text=True\n",
        "        )\n",
        "        \n",
        "        if result.returncode != 0:\n",
        "            print('[ERROR] Failed to create Service Principal')\n",
        "            print(f'[ERROR] {result.stderr}')\n",
        "            print('[INFO] You need permissions to create App Registrations')\n",
        "        else:\n",
        "            sp_output = json.loads(result.stdout)\n",
        "            \n",
        "            tenant_id = sp_output['tenant']\n",
        "            client_id = sp_output['appId']\n",
        "            client_secret = sp_output['password']\n",
        "            \n",
        "            print('[OK] Service Principal created successfully!')\n",
        "            print()\n",
        "            print('Credentials:')\n",
        "            print(f'  Tenant ID:     {tenant_id}')\n",
        "            print(f'  Client ID:     {client_id}')\n",
        "            print(f'  Client Secret: {client_secret[:8]}...')\n",
        "            print()\n",
        "            \n",
        "            # Create .azure-credentials.env\n",
        "            env_content = f'''# Azure Service Principal Credentials\n",
        "# Created: {datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")}\n",
        "# Service Principal: {sp_name}\n",
        "\n",
        "AZURE_TENANT_ID={tenant_id}\n",
        "AZURE_CLIENT_ID={client_id}\n",
        "AZURE_CLIENT_SECRET={client_secret}\n",
        "AZURE_SUBSCRIPTION_ID={subscription_id}\n",
        "'''\n",
        "            \n",
        "            with open('.azure-credentials.env', 'w') as f:\n",
        "                f.write(env_content)\n",
        "            \n",
        "            print('[OK] Created .azure-credentials.env')\n",
        "            print('[OK] This file is in .gitignore (safe from commits)')\n",
        "            print()\n",
        "            print('[OK] Next: Run Cell 11 (Configuration), then Cell 13 (Helper Functions)')\n",
        "            print()\n",
        "            print('To delete this Service Principal later:')\n",
        "            print(f'  az ad sp delete --id {client_id}')\n"
    ]
})

# Insert after Cell 9
print('[*] Inserting Service Principal creation cells after Cell 9...')
for i, cell in enumerate(sp_creation_cells):
    nb['cells'].insert(10 + i, cell)

print(f'[*] Total cells after insertion: {len(nb["cells"])}')

# Save notebook
print('[*] Saving notebook...')
with open('master-ai-gateway.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print('[OK] Notebook updated!')
print()
print('[OK] New cells added at positions 10-11:')
print('  Cell 10: Service Principal creation header')
print('  Cell 11: Service Principal creation code')
print()
print('[OK] Previous cells renumbered:')
print('  Old Cell 10 (Config) is now Cell 12')
print('  Old Cell 11 (Config code) is now Cell 13')
print('  Old Cell 13 (Helper Functions) is now Cell 15')
print('  Old Cell 15 (Main Deployment) is now Cell 17')
print()
print('[OK] Workflow:')
print('  1. Run Cell 10-11: Create Service Principal (one-time)')
print('  2. Run Cell 12-13: Configuration')
print('  3. Run Cell 14-15: Helper Functions')
print('  4. Run Cell 16-17: Main Deployment')
