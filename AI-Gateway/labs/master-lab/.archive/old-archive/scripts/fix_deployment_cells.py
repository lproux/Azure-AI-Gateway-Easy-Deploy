#!/usr/bin/env python3
"""Fix the deployment cells in master-ai-gateway.ipynb"""

import json
import sys

# Read notebook
with open('master-ai-gateway.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"[*] Total cells before: {len(nb['cells'])}")

# Remove cells 10-11 (premature .env export)
print("[*] Removing cells 10-11 (premature .env export)")
del nb['cells'][10:12]  # Remove cells 10 and 11

print(f"[*] Total cells after removal: {len(nb['cells'])}")

# Now cell 12 is the "Retrieve All Deployment Outputs" markdown
# Insert comprehensive deployment cell BEFORE it

comprehensive_cell_markdown = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Deploy or Load Infrastructure\n",
        "\n",
        "This cell checks if the deployment exists. If not, it creates the resource group and deploys all infrastructure using Bicep."
    ]
}

comprehensive_cell_code = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Check if deployment exists, if not create it\n",
        "print('[*] Checking if deployment exists...')\n",
        "\n",
        "# Check deployment\n",
        "check_output = utils.run(\n",
        "    f'az deployment group show --name {deployment_name} -g {resource_group_name}',\n",
        "    '', ''\n",
        ")\n",
        "\n",
        "deployment_exists = check_output.success and check_output.json_data\n",
        "\n",
        "if not deployment_exists:\n",
        "    print('[!] Deployment not found. Creating new deployment...')\n",
        "    \n",
        "    # Create resource group\n",
        "    print(f'[*] Creating resource group: {resource_group_name}')\n",
        "    rg_output = utils.run(\n",
        "        f'az group create --name {resource_group_name} --location uksouth',\n",
        "        'Resource group created',\n",
        "        'Failed to create resource group'\n",
        "    )\n",
        "    \n",
        "    if not rg_output.success:\n",
        "        raise Exception('Failed to create resource group')\n",
        "    \n",
        "    # Deploy Bicep\n",
        "    print('[*] Starting Bicep deployment (this may take 30-45 minutes)...')\n",
        "    print('[*] Deploying:')\n",
        "    print('    - API Management (StandardV2)')\n",
        "    print('    - 3 AI Foundry hubs + projects (UK South, Sweden Central, West Europe)')\n",
        "    print('    - 14 AI models in UK South + gpt-4o-mini in other regions')\n",
        "    print('    - Redis Enterprise (semantic caching)')\n",
        "    print('    - Azure Cognitive Search')\n",
        "    print('    - Cosmos DB')\n",
        "    print('    - 7 MCP servers in Container Apps')\n",
        "    print('    - Content Safety')\n",
        "    print('')\n",
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
        "        raise Exception('Deployment failed. Check Azure Portal for details.')\n",
        "    \n",
        "    print('[OK] Deployment completed successfully!')\n",
        "else:\n",
        "    print('[OK] Deployment already exists. Loading outputs...')\n",
        "\n",
        "# Retrieve deployment outputs\n",
        "print('[*] Retrieving deployment outputs...')\n",
        "output = utils.run(\n",
        "    f'az deployment group show --name {deployment_name} -g {resource_group_name}',\n",
        "    '',\n",
        "    ''\n",
        ")\n",
        "\n",
        "if not output.success or not output.json_data:\n",
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
        "print(f'[OK] APIM Gateway: {apim_gateway_url}')\n",
        "print(f'[OK] AI Foundry: {foundry_endpoint}')\n",
        "print(f'[OK] Redis: {redis_host}:{redis_port}')\n",
        "print(f'[OK] Search: {search_endpoint}')\n",
        "print(f'[OK] Cosmos: {cosmos_endpoint}')\n",
        "print(f'[OK] MCP Servers: {len(mcp_servers)} deployed')\n",
        "\n",
        "# Export to .env file\n",
        "print('[*] Creating deployment-output.env...')\n",
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
        "print('[OK] Environment ready!')\n",
        "print('[OK] You can now run all lab tests below.')\n",
        "print('')\n",
        "print('To load these variables in other notebooks:')\n",
        "print('  from dotenv import load_dotenv')\n",
        "print('  load_dotenv(\\'deployment-output.env\\')')\n"
    ]
}

# Insert at position 12 (after removing 10-11, this is where "Retrieve All Deployment Outputs" was)
insert_position = 12
print(f"[*] Inserting comprehensive deployment cells at position {insert_position}")
nb['cells'].insert(insert_position, comprehensive_cell_markdown)
nb['cells'].insert(insert_position + 1, comprehensive_cell_code)

# Remove the old "Retrieve All Deployment Outputs" cells (now at position 14-15 after insertion)
print("[*] Removing old deployment retrieval cells")
del nb['cells'][14:16]  # Remove markdown + code for old retrieval

print(f"[*] Total cells after fix: {len(nb['cells'])}")

# Save notebook
with open('master-ai-gateway.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("[OK] Notebook updated successfully!")
print("[OK] Cell structure:")
print("  - Cells 0-11: Setup and imports")
print("  - Cell 12-13: Deploy or Load Infrastructure (NEW!)")
print("  - Cell 14+: Lab tests")
print("")
print("The new cell at position 13:")
print("  1. Checks if deployment exists")
print("  2. If not, creates resource group and runs Bicep deployment")
print("  3. Retrieves all outputs")
print("  4. Exports to deployment-output.env")
print("  5. All variables are now ready for lab tests!")
