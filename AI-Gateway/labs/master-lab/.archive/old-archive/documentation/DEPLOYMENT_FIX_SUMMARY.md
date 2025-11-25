# Deployment Cell Fix Summary

## Problem
The notebook had a NameError when trying to export deployment outputs to `.env` file because:
1. The .env export cell ran BEFORE the deployment outputs were retrieved
2. There was no cell to actually RUN the Bicep deployment
3. Variables like `apim_gateway_url` were undefined when the export cell ran

## Solution
Created a comprehensive deployment cell that handles everything in the correct order:

### Cell 13: Deploy or Load Infrastructure

This single cell now:

1. **Checks if deployment exists**
   ```python
   check_output = utils.run(
       f'az deployment group show --name {deployment_name} -g {resource_group_name}'
   )
   deployment_exists = check_output.success and check_output.json_data
   ```

2. **If deployment doesn't exist, creates it:**
   - Creates resource group: `az group create --name {resource_group_name} --location uksouth`
   - Deploys Bicep template: `az deployment group create --template-file master-deployment.bicep`
   - Deployment includes:
     - API Management (StandardV2)
     - 3 AI Foundry hubs + projects (UK South, Sweden Central, West Europe)
     - 14 AI models in UK South + gpt-4o-mini in other regions
     - Redis Enterprise (semantic caching)
     - Azure Cognitive Search
     - Cosmos DB
     - 7 MCP servers in Container Apps
     - Content Safety

3. **If deployment exists, skips to retrieval:**
   ```python
   print('[OK] Deployment already exists. Loading outputs...')
   ```

4. **Retrieves ALL deployment outputs:**
   - APIM: `apim_gateway_url`, `apim_service_id`, `api_key`
   - AI Foundry: `foundry_endpoint`
   - Redis: `redis_host`, `redis_port`, `redis_key`
   - Search: `search_endpoint`, `search_key`
   - Cosmos: `cosmos_endpoint`
   - MCP Servers: `mcp_servers[]`

5. **Exports to deployment-output.env:**
   ```bash
   # Master Lab Deployment Outputs
   # Generated: 2025-10-24 HH:MM:SS

   # APIM
   APIM_GATEWAY_URL=https://...
   APIM_SERVICE_ID=/subscriptions/...
   APIM_API_KEY=...

   # AI Foundry
   FOUNDRY_ENDPOINT=https://...

   # Redis
   REDIS_HOST=...
   REDIS_PORT=6380
   REDIS_KEY=...

   # Search
   SEARCH_ENDPOINT=https://...
   SEARCH_KEY=...

   # Cosmos DB
   COSMOS_ENDPOINT=https://...

   # Resource Group
   RESOURCE_GROUP=lab-master-lab
   DEPLOYMENT_NAME=master-lab-deployment
   ```

## Changes Made

### Removed Cells:
- **Cell 10-11**: Premature .env export (markdown + code)
- **Cell 14-15**: Old deployment retrieval (markdown + code)

### Added Cells:
- **Cell 12**: Markdown header "Deploy or Load Infrastructure"
- **Cell 13**: Comprehensive deployment code (check → create → retrieve → export)

### Result:
- **Before**: 746 cells
- **After**: 744 cells (removed 4, added 2)

## Workflow

### New Cell Execution Order:

1. **Cells 0-11**: Setup
   - Install packages
   - Import libraries
   - Azure authentication
   - Master configuration (sets `deployment_name`, `resource_group_name`)

2. **Cells 12-13**: Deploy or Load (ONE-CLICK)
   - Checks if deployment exists
   - If not, runs full Bicep deployment (30-45 minutes)
   - Retrieves all outputs
   - Exports to deployment-output.env
   - **All variables are now defined and ready!**

3. **Cells 14+**: Lab Tests
   - All 31 labs can now access variables like `apim_gateway_url`, `api_key`, etc.
   - No more NameError!

## Usage

### First Time (No Deployment):
```bash
# Run cells 0-13 sequentially
# Cell 13 will:
#   - Create resource group
#   - Deploy all infrastructure (30-45 min)
#   - Export to .env
```

### Subsequent Runs (Deployment Exists):
```bash
# Run cells 0-13 sequentially
# Cell 13 will:
#   - Detect existing deployment
#   - Load outputs (5 seconds)
#   - Export to .env
```

### Using .env in Other Notebooks:
```python
from dotenv import load_dotenv
load_dotenv('deployment-output.env')

import os
apim_url = os.getenv('APIM_GATEWAY_URL')
api_key = os.getenv('APIM_API_KEY')
```

## Fixed!

✅ No more NameError
✅ One-click deployment or load
✅ Automatic .env export
✅ All variables defined before lab tests
✅ Idempotent (safe to re-run)
