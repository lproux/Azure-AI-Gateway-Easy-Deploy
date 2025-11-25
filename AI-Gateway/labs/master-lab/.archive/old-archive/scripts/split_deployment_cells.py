#!/usr/bin/env python3
"""Split the deployment cell into multiple debuggable cells"""

import json

# Read notebook
with open('master-ai-gateway.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"[*] Total cells before: {len(nb['cells'])}")

# Remove Cell 13 (the comprehensive deployment cell)
print("[*] Removing Cell 13 (comprehensive deployment)")
del nb['cells'][13]

print(f"[*] Total cells after removal: {len(nb['cells'])}")

# Create multiple cells for better debugging
cells_to_insert = []

# Cell 1: Markdown header
cells_to_insert.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Step 1: Check Deployment Status\n",
        "\n",
        "Check if the deployment already exists in Azure."
    ]
})

# Cell 2: Check deployment status
cells_to_insert.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Check if deployment exists\n",
        "print('[*] Checking if deployment exists...')\n",
        "\n",
        "check_output = utils.run(\n",
        "    f'az deployment group show --name {deployment_name} -g {resource_group_name}',\n",
        "    '', ''\n",
        ")\n",
        "\n",
        "deployment_exists = check_output.success and check_output.json_data\n",
        "\n",
        "if deployment_exists:\n",
        "    print('[OK] Deployment already exists!')\n",
        "    print('[OK] You can skip to Step 4 (Retrieve Outputs)')\n",
        "    print('')\n",
        "    print('TIP: If you want to redeploy, delete the resource group first:')\n",
        "    print(f'     az group delete --name {resource_group_name} --yes')\n",
        "else:\n",
        "    print('[!] Deployment not found')\n",
        "    print('[*] Continue to Step 2 to create it')\n"
    ]
})

# Cell 3: Markdown - Create RG
cells_to_insert.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Step 2: Create Resource Group\n",
        "\n",
        "**Run this only if deployment doesn't exist (Step 1 said \"not found\")**"
    ]
})

# Cell 4: Create resource group
cells_to_insert.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Create resource group (only if deployment doesn't exist)\n",
        "if deployment_exists:\n",
        "    print('[OK] Deployment exists. Skipping resource group creation.')\n",
        "else:\n",
        "    print(f'[*] Creating resource group: {resource_group_name}')\n",
        "    print(f'[*] Location: UK South')\n",
        "    \n",
        "    rg_output = utils.run(\n",
        "        f'az group create --name {resource_group_name} --location uksouth',\n",
        "        'Resource group created',\n",
        "        'Failed to create resource group'\n",
        "    )\n",
        "    \n",
        "    if not rg_output.success:\n",
        "        raise Exception('Failed to create resource group. Check permissions and quota.')\n",
        "    \n",
        "    print('[OK] Resource group created successfully!')\n",
        "    print('[OK] Continue to Step 3')\n"
    ]
})

# Cell 5: Markdown - Deploy Bicep
cells_to_insert.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Step 3: Deploy Infrastructure (Bicep)\n",
        "\n",
        "**Run this only if deployment doesn't exist**\n",
        "\n",
        "This will take **30-45 minutes**. You can monitor progress in Azure Portal:\n",
        "- Resource Group: `lab-master-lab`\n",
        "- Deployments: `master-lab-deployment`\n",
        "\n",
        "**What's being deployed:**\n",
        "- API Management (StandardV2)\n",
        "- 3 AI Foundry hubs + projects (UK South, Sweden Central, West Europe)\n",
        "- 14 AI models in UK South + gpt-4o-mini in secondary regions\n",
        "- Redis Enterprise (semantic caching)\n",
        "- Azure Cognitive Search\n",
        "- Cosmos DB\n",
        "- 7 MCP servers in Container Apps\n",
        "- Content Safety\n",
        "\n",
        "**Total resources**: ~60 Azure resources"
    ]
})

# Cell 6: Deploy Bicep
cells_to_insert.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Deploy Bicep (only if deployment doesn't exist)\n",
        "if deployment_exists:\n",
        "    print('[OK] Deployment exists. Skipping Bicep deployment.')\n",
        "else:\n",
        "    print('[*] Starting Bicep deployment...')\n",
        "    print('[*] This will take 30-45 minutes')\n",
        "    print('')\n",
        "    print('[*] Deploying:')\n",
        "    print('    - API Management (StandardV2)')\n",
        "    print('    - 3 AI Foundry hubs + projects')\n",
        "    print('      * UK South: ALL 14 models (priority 1)')\n",
        "    print('      * Sweden Central: gpt-4o-mini only (priority 2)')\n",
        "    print('      * West Europe: gpt-4o-mini only (priority 2)')\n",
        "    print('    - Redis Enterprise (semantic caching)')\n",
        "    print('    - Azure Cognitive Search')\n",
        "    print('    - Cosmos DB')\n",
        "    print('    - 7 MCP servers in Container Apps')\n",
        "    print('    - Content Safety')\n",
        "    print('')\n",
        "    print('[*] Monitor progress:')\n",
        "    print(f'    https://portal.azure.com/#view/HubsExtension/DeploymentDetailsBlade/overview')\n",
        "    print('')\n",
        "    print('[*] Deployment started...')\n",
        "    \n",
        "    deploy_output = utils.run(\n",
        "        f'az deployment group create --name {deployment_name} '\n",
        "        f'--resource-group {resource_group_name} '\n",
        "        f'--template-file master-deployment.bicep '\n",
        "        f'--parameters @params.template.json',\n",
        "        '',\n",
        "        'Deployment failed'\n",
        "    )\n",
        "    \n",
        "    if not deploy_output.success:\n",
        "        print('[!] Deployment failed!')\n",
        "        print('[!] Check Azure Portal for error details:')\n",
        "        print(f'[!] Resource Group: {resource_group_name}')\n",
        "        print(f'[!] Deployment: {deployment_name}')\n",
        "        print('')\n",
        "        print('Common issues:')\n",
        "        print('  - Quota limits (especially for AI models)')\n",
        "        print('  - Region capacity')\n",
        "        print('  - Permissions (need Contributor role)')\n",
        "        print('')\n",
        "        print('You can re-run this cell after fixing the issue.')\n",
        "        raise Exception('Deployment failed. Check Azure Portal for details.')\n",
        "    \n",
        "    print('')\n",
        "    print('[OK] Deployment completed successfully!')\n",
        "    print('[OK] Continue to Step 4')\n",
        "    \n",
        "    # Update deployment_exists flag\n",
        "    deployment_exists = True\n"
    ]
})

# Cell 7: Markdown - Retrieve Outputs
cells_to_insert.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Step 4: Retrieve Deployment Outputs\n",
        "\n",
        "**Always run this cell** - it retrieves all deployment outputs and defines variables.\n",
        "\n",
        "This works whether you just deployed (Step 3) or loaded existing deployment (Step 1)."
    ]
})

# Cell 8: Retrieve outputs
cells_to_insert.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Retrieve deployment outputs\n",
        "print('[*] Retrieving deployment outputs...')\n",
        "\n",
        "output = utils.run(\n",
        "    f'az deployment group show --name {deployment_name} -g {resource_group_name}',\n",
        "    '',\n",
        "    ''\n",
        ")\n",
        "\n",
        "if not output.success or not output.json_data:\n",
        "    print('[!] Failed to retrieve deployment outputs')\n",
        "    print('[!] Make sure deployment completed successfully (Step 3)')\n",
        "    print('')\n",
        "    print('Debug commands:')\n",
        "    print(f'  az deployment group show --name {deployment_name} -g {resource_group_name}')\n",
        "    print(f'  az group exists --name {resource_group_name}')\n",
        "    raise Exception('Failed to retrieve deployment outputs')\n",
        "\n",
        "outs = output.json_data['properties']['outputs']\n",
        "\n",
        "# APIM\n",
        "apim_gateway_url = outs['apimResourceGatewayURL']['value']\n",
        "apim_service_id = outs['apimServiceId']['value']\n",
        "apim_subscriptions = outs['apimSubscriptions']['value']\n",
        "api_key = apim_subscriptions[0]['key']\n",
        "\n",
        "# AI Foundry\n",
        "foundry_endpoint = outs['foundryProjectEndpoint']['value']\n",
        "\n",
        "# Redis\n",
        "redis_host = outs['redisCacheHost']['value']\n",
        "redis_port = outs['redisCachePort']['value']\n",
        "redis_key = outs['redisCacheKey']['value']\n",
        "\n",
        "# Search\n",
        "search_name = outs['searchServiceName']['value']\n",
        "search_endpoint = outs['searchServiceEndpoint']['value']\n",
        "search_key = outs['searchServiceAdminKey']['value']\n",
        "\n",
        "# Cosmos\n",
        "cosmos_account = outs['cosmosDbAccountName']['value']\n",
        "cosmos_endpoint = outs['cosmosDbEndpoint']['value']\n",
        "\n",
        "# MCP Servers\n",
        "mcp_servers = outs['mcpServerUrls']['value']\n",
        "\n",
        "print('')\n",
        "print('[OK] All outputs retrieved successfully!')\n",
        "print('')\n",
        "print(f'[OK] APIM Gateway: {apim_gateway_url}')\n",
        "print(f'[OK] AI Foundry: {foundry_endpoint}')\n",
        "print(f'[OK] Redis: {redis_host}:{redis_port}')\n",
        "print(f'[OK] Search: {search_endpoint}')\n",
        "print(f'[OK] Cosmos: {cosmos_endpoint}')\n",
        "print(f'[OK] MCP Servers: {len(mcp_servers)} deployed')\n",
        "print('')\n",
        "print('[OK] All variables are now defined!')\n",
        "print('[OK] Continue to Step 5')\n"
    ]
})

# Cell 9: Markdown - Export .env
cells_to_insert.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Step 5: Export to deployment-output.env\n",
        "\n",
        "**Always run this cell** - creates a `.env` file for reuse in other notebooks."
    ]
})

# Cell 10: Export .env
cells_to_insert.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Export to .env file\n",
        "print('[*] Creating deployment-output.env...')\n",
        "\n",
        "env_content = f\"\"\"# Master Lab Deployment Outputs\n",
        "# Generated: {time.strftime(\"%Y-%m-%d %H:%M:%S\")}\n",
        "\n",
        "# APIM\n",
        "APIM_GATEWAY_URL={apim_gateway_url}\n",
        "APIM_SERVICE_ID={apim_service_id}\n",
        "APIM_API_KEY={api_key}\n",
        "\n",
        "# AI Foundry\n",
        "FOUNDRY_ENDPOINT={foundry_endpoint}\n",
        "\n",
        "# Redis\n",
        "REDIS_HOST={redis_host}\n",
        "REDIS_PORT={redis_port}\n",
        "REDIS_KEY={redis_key}\n",
        "\n",
        "# Search\n",
        "SEARCH_ENDPOINT={search_endpoint}\n",
        "SEARCH_KEY={search_key}\n",
        "\n",
        "# Cosmos DB\n",
        "COSMOS_ENDPOINT={cosmos_endpoint}\n",
        "\n",
        "# Resource Group\n",
        "RESOURCE_GROUP={resource_group_name}\n",
        "DEPLOYMENT_NAME={deployment_name}\n",
        "\"\"\"\n",
        "\n",
        "with open('deployment-output.env', 'w') as f:\n",
        "    f.write(env_content)\n",
        "\n",
        "print('[OK] Created deployment-output.env')\n",
        "print(f'[OK] File location: {os.getcwd()}/deployment-output.env')\n",
        "print('')\n",
        "print('[OK] =========================================')\n",
        "print('[OK] SETUP COMPLETE!')\n",
        "print('[OK] =========================================')\n",
        "print('')\n",
        "print('[OK] You can now:')\n",
        "print('[OK] 1. Run any lab tests below')\n",
        "print('[OK] 2. Load deployment-output.env in other notebooks:')\n",
        "print('[OK]    from dotenv import load_dotenv')\n",
        "print('[OK]    load_dotenv(\\'deployment-output.env\\')')\n",
        "print('')\n",
        "print('[OK] All 31 labs are ready to test!')\n"
    ]
})

# Insert all cells at position 13
insert_position = 13
print(f"[*] Inserting {len(cells_to_insert)} cells at position {insert_position}")
for i, cell in enumerate(cells_to_insert):
    nb['cells'].insert(insert_position + i, cell)

# Remove old markdown header (now redundant)
print("[*] Removing old deployment header at position 12")
del nb['cells'][12]

print(f"[*] Total cells after split: {len(nb['cells'])}")

# Save notebook
with open('master-ai-gateway.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("[OK] Notebook updated successfully!")
print("")
print("[OK] New cell structure:")
print("  Cell 12: Step 1 - Check deployment status")
print("  Cell 13: [Code] Check if deployment exists")
print("  Cell 14: Step 2 - Create resource group")
print("  Cell 15: [Code] Create RG (if needed)")
print("  Cell 16: Step 3 - Deploy Bicep")
print("  Cell 17: [Code] Deploy infrastructure (30-45 min)")
print("  Cell 18: Step 4 - Retrieve outputs")
print("  Cell 19: [Code] Retrieve all outputs")
print("  Cell 20: Step 5 - Export .env")
print("  Cell 21: [Code] Export to deployment-output.env")
print("")
print("[OK] Benefits:")
print("  - Each step can be run individually")
print("  - Easy to debug if something fails")
print("  - Can re-run just the failed step")
print("  - Clear progress tracking")
print("  - Still 'one-click' (just run cells 13, 15, 17, 19, 21 in sequence)")
print("")
print("[OK] First run: Cells 13 → 15 → 17 (long) → 19 → 21")
print("[OK] Subsequent runs: Cell 13 (skip to 19) → 19 → 21")
