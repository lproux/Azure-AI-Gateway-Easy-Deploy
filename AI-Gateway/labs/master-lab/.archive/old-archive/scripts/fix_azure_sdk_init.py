#!/usr/bin/env python3
"""
Fix Azure SDK initialization in Cell 13
Remove subprocess calls to 'az' command
"""

import json

print('[*] Reading notebook...')
with open('master-ai-gateway.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f'[*] Total cells: {len(nb["cells"])}')

# Find Cell 13 (Helper Functions code)
print('[*] Updating Cell 13 (Helper Functions)...')

# New helper functions that don't use subprocess for az commands
new_helper_functions = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "import subprocess\n",
        "import json\n",
        "import time\n",
        "from azure.mgmt.resource import ResourceManagementClient\n",
        "from azure.identity import AzureCliCredential\n",
        "from azure.cli.core import get_default_cli\n",
        "\n",
        "# Initialize Azure CLI credential\n",
        "print('[*] Initializing Azure credentials...')\n",
        "credential = AzureCliCredential()\n",
        "\n",
        "# Get subscription ID from Azure CLI profile\n",
        "print('[*] Getting subscription from Azure CLI profile...')\n",
        "cli = get_default_cli()\n",
        "cli.invoke(['account', 'show', '--query', 'id', '-o', 'tsv'])\n",
        "subscription_id = cli.result.result.strip()\n",
        "\n",
        "if not subscription_id:\n",
        "    raise Exception('Could not get subscription ID. Please run: az login')\n",
        "\n",
        "print(f'[OK] Subscription ID: {subscription_id}')\n",
        "\n",
        "# Create Resource Management Client\n",
        "print('[*] Creating Azure Resource Management client...')\n",
        "resource_client = ResourceManagementClient(credential, subscription_id)\n",
        "print('[OK] Azure SDK initialized')\n",
        "print()\n",
        "\n",
        "def compile_bicep(bicep_file):\n",
        "    \"\"\"Compile Bicep to JSON using Azure CLI\"\"\"\n",
        "    print(f'[*] Compiling {bicep_file}...')\n",
        "    \n",
        "    cli = get_default_cli()\n",
        "    cli.invoke(['bicep', 'build', '--file', bicep_file])\n",
        "    \n",
        "    if cli.result.exit_code != 0:\n",
        "        print(f'[ERROR] Compilation failed')\n",
        "        return False\n",
        "    \n",
        "    json_file = bicep_file.replace('.bicep', '.json')\n",
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
        "    with open(template_file, 'r') as f:\n",
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
        "    print('[*] Deployment started. Polling status...')\n",
        "    start_time = time.time()\n",
        "    last_update = start_time\n",
        "    \n",
        "    while not deployment_async.done():\n",
        "        time.sleep(30)\n",
        "        elapsed = time.time() - start_time\n",
        "        if time.time() - last_update >= 60:\n",
        "            print(f'[*] Still deploying... {int(elapsed/60)}m {int(elapsed%60)}s elapsed')\n",
        "            last_update = time.time()\n",
        "    \n",
        "    # Get result\n",
        "    deployment_result = deployment_async.result()\n",
        "    elapsed = time.time() - start_time\n",
        "    \n",
        "    if deployment_result.properties.provisioning_state == 'Succeeded':\n",
        "        print(f'[OK] Deployment succeeded in {int(elapsed/60)}m {int(elapsed%60)}s')\n",
        "        return True, deployment_result\n",
        "    else:\n",
        "        print(f'[ERROR] Deployment failed: {deployment_result.properties.provisioning_state}')\n",
        "        if deployment_result.properties.error:\n",
        "            print(f'[ERROR] Error details: {deployment_result.properties.error.message}')\n",
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

# Replace Cell 13
nb['cells'][13] = new_helper_functions

print('[*] Saving notebook...')
with open('master-ai-gateway.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print('[OK] Cell 13 updated!')
print()
print('[OK] Changes:')
print('  - Removed subprocess calls to az command')
print('  - Uses Azure CLI Core library instead')
print('  - Gets subscription ID from Azure CLI profile')
print('  - Compiles Bicep using Azure CLI Core')
print()
print('[OK] Please re-run Cell 13 in the notebook')
