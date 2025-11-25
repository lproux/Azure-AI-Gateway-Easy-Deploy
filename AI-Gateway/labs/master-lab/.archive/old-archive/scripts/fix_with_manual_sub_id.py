#!/usr/bin/env python3
"""
Alternative fix: Ask user to provide subscription ID manually
This completely avoids Azure CLI dependency issues
"""

import json

print('[*] Reading notebook...')
with open('master-ai-gateway.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f'[*] Total cells: {len(nb["cells"])}')

# Update Cell 11 (Configuration) to include subscription_id
print('[*] Updating Cell 11 (Configuration)...')

new_config_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Master Lab Configuration\n",
        "\n",
        "# IMPORTANT: Set your Azure subscription ID\n",
        "# Get this from: Azure Portal > Subscriptions > Copy Subscription ID\n",
        "subscription_id = 'd334f2cd-3efd-494e-9fd3-2470b1a13e4c'  # Replace with your subscription ID\n",
        "\n",
        "deployment_name_prefix = 'master-lab'\n",
        "resource_group_name = 'lab-master-lab'\n",
        "location = 'uksouth'\n",
        "\n",
        "# Deployment names for each step\n",
        "deployment_step1 = f'{deployment_name_prefix}-01-core'\n",
        "deployment_step2 = f'{deployment_name_prefix}-02-ai-foundry'\n",
        "deployment_step3 = f'{deployment_name_prefix}-03-supporting'\n",
        "deployment_step4 = f'{deployment_name_prefix}-04-mcp'\n",
        "\n",
        "print('[OK] Configuration set')\n",
        "print(f'  Subscription ID: {subscription_id}')\n",
        "print(f'  Resource Group: {resource_group_name}')\n",
        "print(f'  Location: {location}')\n",
        "print(f'  Deployment Prefix: {deployment_name_prefix}')\n"
    ]
}

nb['cells'][11] = new_config_cell

# Update Cell 13 (Helper Functions) to use subscription_id from config
print('[*] Updating Cell 13 (Helper Functions)...')

new_helper_functions = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "import json\n",
        "import time\n",
        "import os\n",
        "from pathlib import Path\n",
        "from azure.mgmt.resource import ResourceManagementClient\n",
        "from azure.identity import AzureCliCredential\n",
        "\n",
        "# Initialize Azure credentials\n",
        "print('[*] Initializing Azure credentials...')\n",
        "credential = AzureCliCredential()\n",
        "print('[OK] Credentials initialized')\n",
        "\n",
        "# Verify subscription ID from config\n",
        "if not subscription_id or len(subscription_id) < 10:\n",
        "    raise Exception('Please set your subscription_id in Cell 11')\n",
        "\n",
        "print(f'[OK] Using Subscription ID: {subscription_id}')\n",
        "\n",
        "# Create Resource Management Client\n",
        "print('[*] Creating Azure Resource Management client...')\n",
        "resource_client = ResourceManagementClient(credential, subscription_id)\n",
        "print('[OK] Azure SDK initialized')\n",
        "print()\n",
        "\n",
        "def compile_bicep(bicep_file):\n",
        "    \"\"\"Compile Bicep to JSON\"\"\"\n",
        "    print(f'[*] Compiling {bicep_file}...')\n",
        "    \n",
        "    # Use az bicep build via os.system to avoid subprocess PATH issues\n",
        "    json_file = bicep_file.replace('.bicep', '.json')\n",
        "    \n",
        "    # Check if JSON already exists and is newer than bicep\n",
        "    if os.path.exists(json_file):\n",
        "        bicep_time = os.path.getmtime(bicep_file)\n",
        "        json_time = os.path.getmtime(json_file)\n",
        "        if json_time > bicep_time:\n",
        "            print(f'[OK] Using existing {json_file} (newer than .bicep)')\n",
        "            return json_file\n",
        "    \n",
        "    # Compile using az bicep (will work if az is in PATH)\n",
        "    result = os.system(f'az bicep build --file {bicep_file}')\n",
        "    \n",
        "    if result != 0:\n",
        "        print(f'[ERROR] Compilation failed')\n",
        "        print(f'[INFO] You can manually compile: az bicep build --file {bicep_file}')\n",
        "        return False\n",
        "    \n",
        "    print(f'[OK] Compiled to {json_file}')\n",
        "    return json_file\n",
        "\n",
        "def check_resource_group_exists(rg_name):\n",
        "    \"\"\"Check if resource group exists\"\"\"\n",
        "    try:\n",
        "        resource_client.resource_groups.get(rg_name)\n",
        "        return True\n",
        "    except:\n",
        "        return False\n",
        "\n",
        "def check_deployment_exists(rg_name, deployment_name):\n",
        "    \"\"\"Check if deployment exists and succeeded\"\"\"\n",
        "    try:\n",
        "        deployment = resource_client.deployments.get(rg_name, deployment_name)\n",
        "        if deployment.properties.provisioning_state == 'Succeeded':\n",
        "            return True, deployment\n",
        "        else:\n",
        "            return False, deployment\n",
        "    except:\n",
        "        return False, None\n",
        "\n",
        "def deploy_template(rg_name, deployment_name, template_file, parameters_dict):\n",
        "    \"\"\"Deploy ARM template using Azure SDK\"\"\"\n",
        "    print(f'[*] Deploying {deployment_name}...')\n",
        "    \n",
        "    # Read template\n",
        "    with open(template_file, 'r', encoding='utf-8') as f:\n",
        "        template = json.load(f)\n",
        "    \n",
        "    # Prepare deployment properties\n",
        "    deployment_properties = {\n",
        "        'mode': 'Incremental',\n",
        "        'template': template,\n",
        "        'parameters': parameters_dict\n",
        "    }\n",
        "    \n",
        "    # Start deployment\n",
        "    print('[*] Starting deployment...')\n",
        "    deployment_async = resource_client.deployments.begin_create_or_update(\n",
        "        rg_name,\n",
        "        deployment_name,\n",
        "        {'properties': deployment_properties}\n",
        "    )\n",
        "    \n",
        "    # Poll deployment status\n",
        "    print('[*] Deployment in progress. Polling status...')\n",
        "    start_time = time.time()\n",
        "    last_update = start_time\n",
        "    \n",
        "    while not deployment_async.done():\n",
        "        time.sleep(30)\n",
        "        elapsed = time.time() - start_time\n",
        "        if time.time() - last_update >= 60:\n",
        "            mins = int(elapsed / 60)\n",
        "            secs = int(elapsed % 60)\n",
        "            print(f'[*] Still deploying... {mins}m {secs}s elapsed')\n",
        "            last_update = time.time()\n",
        "    \n",
        "    # Get result\n",
        "    deployment_result = deployment_async.result()\n",
        "    elapsed = time.time() - start_time\n",
        "    mins = int(elapsed / 60)\n",
        "    secs = int(elapsed % 60)\n",
        "    \n",
        "    if deployment_result.properties.provisioning_state == 'Succeeded':\n",
        "        print(f'[OK] Deployment succeeded in {mins}m {secs}s')\n",
        "        return True, deployment_result\n",
        "    else:\n",
        "        print(f'[ERROR] Deployment failed: {deployment_result.properties.provisioning_state}')\n",
        "        if deployment_result.properties.error:\n",
        "            print(f'[ERROR] Error: {deployment_result.properties.error.message}')\n",
        "        return False, deployment_result\n",
        "\n",
        "def get_deployment_outputs(rg_name, deployment_name):\n",
        "    \"\"\"Get deployment outputs\"\"\"\n",
        "    deployment = resource_client.deployments.get(rg_name, deployment_name)\n",
        "    if deployment.properties.outputs:\n",
        "        return {k: v['value'] for k, v in deployment.properties.outputs.items()}\n",
        "    return {}\n",
        "\n",
        "print('[OK] Helper functions defined')\n"
    ]
}

nb['cells'][13] = new_helper_functions

print('[*] Saving notebook...')
with open('master-ai-gateway.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print('[OK] Notebook updated!')
print()
print('[OK] Changes:')
print('  Cell 11: Now includes subscription_id (YOU MUST SET THIS)')
print('  Cell 13: Uses subscription_id from Cell 11')
print('  Cell 13: Compiles Bicep using os.system (more reliable)')
print()
print('[IMPORTANT] Next steps:')
print('  1. Get your subscription ID from Azure Portal')
print('  2. Update Cell 11: subscription_id = \"YOUR-SUBSCRIPTION-ID\"')
print('  3. Run Cell 11 (config)')
print('  4. Run Cell 13 (helper functions)')
print('  5. Run Cell 15 (deployment)')
