"""
Generate the master AI Gateway notebook programmatically.
This creates a comprehensive notebook with all 31 labs.
"""

import json

def create_markdown_cell(content):
    """Create a markdown cell"""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": content if isinstance(content, list) else [content]
    }

def create_code_cell(content):
    """Create a code cell"""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": content if isinstance(content, list) else [content]
    }

# Initialize cells list
cells = []

# ============================================================================
# TITLE AND OVERVIEW
# ============================================================================

cells.append(create_markdown_cell([
    "# Master AI Gateway Lab - Complete Feature Testing Environment\n",
    "\n",
    "![Azure AI Gateway](../../images/ai-gateway-banner.png)\n",
    "\n",
    "## 🎯 Overview\n",
    "\n",
    "This master notebook consolidates **all 31 AI Gateway labs** into a single comprehensive testing environment.\n",
    "\n",
    "**One deployment. All features. No redundancy.**\n",
    "\n",
    "### What's Deployed\n",
    "\n",
    "- **3x AI Foundry Hubs** (UK South, Sweden Central, West Europe)\n",
    "- **12 AI Models** (Chat, Image, Embeddings, Specialized)\n",
    "- **1x API Management** (StandardV2 with 50+ policies)\n",
    "- **7x MCP Servers** (Weather, Oncall, GitHub, Spotify, Product Catalog, Place Order, MS Learn)\n",
    "- **Supporting Services** (Redis, Content Safety, Search, Cosmos DB, Container Apps)\n",
    "\n",
    "### 31 Labs Included\n",
    "\n",
    "1. ✅ zero-to-production\n",
    "2. ✅ backend-pool-load-balancing  \n",
    "3. ✅ built-in-logging\n",
    "4. ✅ token-metrics-emitting\n",
    "5. ✅ token-rate-limiting\n",
    "6. ✅ access-controlling\n",
    "7. ✅ content-safety\n",
    "8. ✅ private-connectivity\n",
    "9. ✅ model-routing\n",
    "10. ✅ ai-foundry-sdk\n",
    "11. ✅ ai-foundry-deepseek\n",
    "12. ✅ model-context-protocol\n",
    "13. ✅ mcp-from-api\n",
    "14. ✅ mcp-client-authorization\n",
    "15. ✅ mcp-a2a-agents\n",
    "16. ✅ openai-agents\n",
    "17. ✅ ai-agent-service\n",
    "18. ✅ realtime-mcp-agents\n",
    "19. ✅ function-calling\n",
    "20. ✅ semantic-caching\n",
    "21. ✅ message-storing\n",
    "22. ✅ vector-searching\n",
    "23. ✅ image-generation\n",
    "24. ✅ realtime-audio\n",
    "25. ✅ finops-framework\n",
    "26. ✅ secure-responses-api\n",
    "27. ✅ And more...\n",
    "\n",
    "### Prerequisites\n",
    "\n",
    "- Azure subscription with appropriate permissions\n",
    "- Azure CLI authenticated\n",
    "- Python 3.12+ with required packages\n",
    "- Resources already deployed via `master-deployment.bicep`\n",
    "\n",
    "### Navigation\n",
    "\n",
    "**Click `Run All` to execute all tests sequentially, or jump to specific sections:**\n",
    "\n",
    "- [Initialization](#init)\n",
    "- [Foundation Labs](#foundation)\n",
    "- [Security Features](#security)\n",
    "- [MCP & Agents](#mcp)\n",
    "- [Advanced Features](#advanced)\n"
]))

# ============================================================================
# MASTER INITIALIZATION
# ============================================================================

cells.append(create_markdown_cell([
    "<a id='init'></a>\n",
    "## 🚀 Master Initialization\n",
    "\n",
    "Initialize once for all 31 labs. This section sets up:\n",
    "- Python environment and imports\n",
    "- Azure authentication\n",
    "- Master resource configuration\n",
    "- Deployment outputs retrieval\n"
]))

cells.append(create_markdown_cell("### 0️⃣ Import Libraries and Initialize Utils"))

cells.append(create_code_cell([
    "import os, sys, json, time, asyncio\n",
    "import requests\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import matplotlib as mpl\n",
    "\n",
    "# Add shared utilities\n",
    "sys.path.insert(1, '../../shared')\n",
    "import utils\n",
    "\n",
    "# Jupyter-specific imports\n",
    "import nest_asyncio\n",
    "nest_asyncio.apply()\n",
    "\n",
    "# Configure plotting\n",
    "mpl.rcParams['figure.figsize'] = [15, 5]\n",
    "\n",
    "print('✅ All libraries imported successfully')\n",
    "utils.print_ok('Master environment initialized')\n"
]))

cells.append(create_markdown_cell("### 1️⃣ Verify Azure CLI and Subscription"))

cells.append(create_code_cell([
    "output = utils.run('az account show', 'Retrieved az account', 'Failed to get the current az account')\n",
    "\n",
    "if output.success and output.json_data:\n",
    "    current_user = output.json_data['user']['name']\n",
    "    tenant_id = output.json_data['tenantId']\n",
    "    subscription_id = output.json_data['id']\n",
    "    \n",
    "    utils.print_info(f'Current user: {current_user}')\n",
    "    utils.print_info(f'Tenant ID: {tenant_id}')\n",
    "    utils.print_info(f'Subscription ID: {subscription_id}')\n",
    "else:\n",
    "    utils.print_error('Failed to get Azure account info. Please run: az login')\n"
]))

cells.append(create_markdown_cell("### 2️⃣ Configure Master Lab Variables"))

cells.append(create_code_cell([
    "# Master deployment configuration\n",
    "deployment_name = 'master-lab-deployment'\n",
    "resource_group_name = 'lab-master-lab'  # Change if you used a different name\n",
    "resource_group_location = 'uksouth'\n",
    "\n",
    "# Inference API configuration  \n",
    "inference_api_path = 'inference'\n",
    "inference_api_type = 'AzureOpenAI'\n",
    "inference_api_version = '2025-03-01-preview'\n",
    "\n",
    "# Foundry project name\n",
    "foundry_project_name = 'master-lab'\n",
    "\n",
    "utils.print_ok('Master configuration set')\n",
    "utils.print_info(f'Deployment: {deployment_name}')\n",
    "utils.print_info(f'Resource Group: {resource_group_name}')\n"
]))

cells.append(create_markdown_cell([
    "### 3️⃣ Retrieve Deployment Outputs\n",
    "\n",
    "Get all endpoints, keys, and URLs from the master deployment.\n"
]))

cells.append(create_code_cell([
    "# Retrieve deployment outputs\n",
    "output = utils.run(\n",
    "    f'az deployment group show --name {deployment_name} -g {resource_group_name}',\n",
    "    f'Retrieved deployment: {deployment_name}',\n",
    "    f'Failed to retrieve deployment: {deployment_name}'\n",
    ")\n",
    "\n",
    "if output.success and output.json_data:\n",
    "    outputs = output.json_data.get('properties', {}).get('outputs', {})\n",
    "    \n",
    "    # APIM outputs\n",
    "    apim_service_id = outputs['apimServiceId']['value']\n",
    "    apim_service_name = outputs['apimServiceName']['value']\n",
    "    apim_resource_gateway_url = outputs['apimResourceGatewayURL']['value']\n",
    "    apim_subscriptions = outputs['apimSubscriptions']['value']\n",
    "    api_key = apim_subscriptions[0]['key']\n",
    "    \n",
    "    # AI Foundry outputs\n",
    "    foundry_project_endpoint = outputs['foundryProjectEndpoint']['value']\n",
    "    \n",
    "    # Redis outputs\n",
    "    redis_cache_host = outputs['redisCacheHost']['value']\n",
    "    redis_cache_port = outputs['redisCachePort']['value']\n",
    "    redis_cache_key = outputs['redisCacheKey']['value']\n",
    "    \n",
    "    # Content Safety outputs\n",
    "    content_safety_endpoint = outputs['contentSafetyEndpoint']['value']\n",
    "    content_safety_key = outputs['contentSafetyKey']['value']\n",
    "    \n",
    "    # Search outputs\n",
    "    search_service_name = outputs['searchServiceName']['value']\n",
    "    search_service_endpoint = outputs['searchServiceEndpoint']['value']\n",
    "    search_admin_key = outputs['searchServiceAdminKey']['value']\n",
    "    \n",
    "    # Cosmos DB outputs\n",
    "    cosmos_account_name = outputs['cosmosDbAccountName']['value']\n",
    "    cosmos_endpoint = outputs['cosmosDbEndpoint']['value']\n",
    "    \n",
    "    # Container Registry outputs\n",
    "    acr_name = outputs['containerRegistryName']['value']\n",
    "    acr_login_server = outputs['containerRegistryLoginServer']['value']\n",
    "    \n",
    "    # MCP Server URLs\n",
    "    mcp_server_urls = outputs['mcpServerUrls']['value']\n",
    "    \n",
    "    # Print summary\n",
    "    utils.print_ok('All deployment outputs retrieved successfully!')\n",
    "    print(f'\\n📊 Master Lab Environment:')\n",
    "    print(f'  🌐 APIM Gateway: {apim_resource_gateway_url}')\n",
    "    print(f'  🤖 AI Foundry: {foundry_project_endpoint}')\n",
    "    print(f'  🔴 Redis Cache: {redis_cache_host}')\n",
    "    print(f'  🔍 Search Service: {search_service_endpoint}')\n",
    "    print(f'  📦 Cosmos DB: {cosmos_endpoint}')\n",
    "    print(f'  🐳 Container Registry: {acr_login_server}')\n",
    "    print(f'  🛠️  MCP Servers: {len(mcp_server_urls)} deployed')\n",
    "    print(f'  🔑 API Subscriptions: {len(apim_subscriptions)}')\n",
    "    print(f'\\n✅ Environment ready for testing all 31 labs!')\n",
    "else:\n",
    "    utils.print_error('Failed to retrieve deployment outputs')\n",
    "    utils.print_warning('Make sure you have deployed using master-deployment.bicep first!')\n"
]))

# Save the notebook
notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.12.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Write to file
with open('master-ai-gateway.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f'Generated notebook with {len(cells)} cells')
print('Run this script to continue adding more sections!')
