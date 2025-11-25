# Modular Deployment Guide - Master AI Gateway Lab

**Status**: ✅ Complete and Ready to Use
**Date**: October 26, 2025

---

## What Changed

The master-ai-gateway.ipynb has been **completely rebuilt** with a modular, debuggable deployment approach using **Azure Python SDK** instead of the monolithic Bicep file.

### Key Improvements

✅ **Modular Bicep Files** - 4 separate deployment steps instead of 1 giant file
✅ **Azure Python SDK** - No more "content already consumed" errors
✅ **Resource Checking** - Skips deployment if resources already exist
✅ **Progress Tracking** - Shows real-time deployment progress every minute
✅ **Error Recovery** - Easy to re-run individual steps
✅ **Grouped .env** - Clean, organized environment variables
✅ **.venv Compatible** - Uses your Python virtual environment only

---

## New File Structure

### Bicep Files (4 Steps)

```
deploy-01-core.bicep              (Core: APIM, Log Analytics, App Insights)
deploy-02-ai-foundry.bicep        (AI: 3 Foundry hubs + 14 models)
deploy-03-supporting.bicep        (Supporting: Redis, Search, Cosmos, Content Safety)
deploy-04-mcp.bicep               (MCP: Container Apps + 7 MCP servers)
```

### Parameter Files

```
params-01-core.json               (APIM SKU, subscriptions)
params-03-supporting.json         (Redis SKU, Search SKU, location)
```

Note: params-02 and params-04 are built dynamically from previous step outputs

### Python Scripts

```
rebuild_deployment_cells.py       (Rebuilds notebook cells - already run)
update_env_references.py          (Updates .env loading - already run)
```

### Generated Files

```
master-lab.env                    (Generated after deployment completes)
deploy-01-core.json               (Compiled from Bicep)
deploy-02-ai-foundry.json         (Compiled from Bicep)
deploy-03-supporting.json         (Compiled from Bicep)
deploy-04-mcp.json                (Compiled from Bicep)
```

---

## Notebook Structure (New)

### Setup Cells (0-9)

```
Cell 0-6:  Standard setup (imports, libraries, path)
Cell 7:    Load Environment Variables header
Cell 8:    Load from master-lab.env (NEW)
Cell 9:    Azure Authentication
```

### Deployment Cells (10-17) - NEW!

```
Cell 10:   Configuration header
Cell 11:   Configuration code (resource group, location, deployment names)

Cell 12:   Helper Functions header
Cell 13:   Helper Functions code (Azure SDK, compile_bicep, deploy_template, etc.)

Cell 14:   Main Deployment header
Cell 15:   Main Deployment code (4 sequential steps with progress tracking)

Cell 16:   Generate .env header
Cell 17:   Generate .env code (creates master-lab.env with all outputs)
```

### Lab Test Cells (18+)

```
Cell 18+:  All 31 lab tests (unchanged, now load from master-lab.env)
```

---

## How to Use

### First Time Deployment

1. **Open Notebook**
   ```bash
   jupyter notebook master-ai-gateway.ipynb
   ```

2. **Run Setup Cells** (0-9)
   - Installs packages
   - Loads libraries
   - Authenticates to Azure

3. **Run Configuration** (Cells 10-11)
   - Sets resource group name: `lab-master-lab`
   - Sets location: `uksouth`
   - Sets deployment names

4. **Run Helper Functions** (Cells 12-13)
   - Initializes Azure SDK
   - Defines deployment functions

5. **Run Main Deployment** (Cells 14-15)
   - **This is the big one!** ~40 minutes
   - Deploys all 4 steps sequentially:
     1. Core (10 min): APIM, Log Analytics, App Insights
     2. AI Foundry (15 min): 3 hubs, 14 models
     3. Supporting (10 min): Redis, Search, Cosmos, Content Safety
     4. MCP (5 min): Container Apps, 7 MCP servers
   - **Shows progress** every minute
   - **Skips steps** that are already deployed

6. **Generate .env** (Cells 16-17)
   - Creates `master-lab.env`
   - Contains all deployment outputs
   - Grouped by service type

7. **Test Labs** (Cells 18+)
   - All labs now load from `master-lab.env`
   - No hardcoded values

### Subsequent Runs

If you've already deployed once:

1. **Run Setup** (Cells 0-9)
2. **Run Configuration** (Cells 10-11)
3. **Run Helper Functions** (Cells 12-13)
4. **Run Main Deployment** (Cells 14-15)
   - **Takes ~1 minute** (checks all 4 steps exist, skips deployment)
   - Just retrieves outputs
5. **Regenerate .env** (Cells 16-17)
6. **Test Labs** (Cells 18+)

---

## Deployment Steps Explained

### Step 1: Core Infrastructure (~10 minutes)

**Resources:**
- Log Analytics Workspace
- Application Insights
- API Management (StandardV2)

**Outputs:**
- `apimGatewayUrl` - APIM endpoint URL
- `apimPrincipalId` - Managed identity for Step 2
- `apimLoggerId` - Logger for Step 2
- `logAnalyticsCustomerId` - For Step 4
- `logAnalyticsPrimarySharedKey` - For Step 4

**What happens:**
1. Compiles `deploy-01-core.bicep` to JSON
2. Reads `params-01-core.json`
3. Deploys using Azure SDK
4. Polls status every 30 seconds
5. Shows progress every minute

### Step 2: AI Foundry (~15 minutes)

**Resources:**
- 3 AI Foundry Hubs (UK South, Sweden Central, West Europe)
- 3 AI Foundry Projects
- 12 AI Models in UK South:
  - gpt-4o-mini, gpt-4.1-mini, gpt-4.1, gpt-4o
  - gpt-4o-realtime-preview, dall-e-3, FLUX-1.1-pro
  - text-embedding-3-small, text-embedding-3-large, text-embedding-ada-002
  - DeepSeek-R1, Phi-4
- 1 Model in Sweden Central: gpt-4o-mini
- 1 Model in West Europe: gpt-4o-mini
- Inference API in APIM

**Parameters from Step 1:**
- `apimPrincipalId` - For role assignments
- `appInsightsId` - For monitoring
- `apimLoggerId` - For API logging

**Outputs:**
- `foundryProjectEndpoint` - Primary endpoint for AI calls
- `inferenceAPIPath` - API path in APIM

### Step 3: Supporting Services (~10 minutes)

**Resources:**
- Redis Enterprise (semantic caching with RediSearch module)
- Azure Cognitive Search (Basic tier)
- Cosmos DB (Session consistency)
- Content Safety

**Outputs:**
- `redisCacheHost`, `redisCachePort`, `redisCacheKey`
- `searchServiceEndpoint`, `searchServiceAdminKey`
- `cosmosDbEndpoint`, `cosmosDbKey`
- `contentSafetyEndpoint`, `contentSafetyKey`

### Step 4: MCP Servers (~5 minutes)

**Resources:**
- Container Registry (Basic SKU)
- Managed Identity for Container Apps
- Container Apps Environment
- 7 MCP Server Container Apps:
  - weather, oncall, github, spotify
  - product-catalog, place-order, ms-learn

**Parameters from Step 1:**
- `logAnalyticsCustomerId` - For Container Apps logging
- `logAnalyticsPrimarySharedKey` - For Container Apps logging

**Outputs:**
- `containerRegistryLoginServer`
- `mcpServerUrls` - Array of MCP server endpoints

---

## master-lab.env Structure

```bash
# ===========================================
# APIM (API Management)
# ===========================================
APIM_GATEWAY_URL=https://apim-xxx.azure-api.net
APIM_SERVICE_ID=/subscriptions/.../apim-xxx
APIM_SERVICE_NAME=apim-xxx
APIM_API_KEY=abc123...

# ===========================================
# AI Foundry
# ===========================================
FOUNDRY_PROJECT_ENDPOINT=https://xxx.inference.ml.azure.com
INFERENCE_API_PATH=inference

# ===========================================
# Supporting Services
# ===========================================

# Redis (Semantic Caching)
REDIS_HOST=redis-xxx.redis.cache.windows.net
REDIS_PORT=10000
REDIS_KEY=xyz789...

# Azure Cognitive Search
SEARCH_SERVICE_NAME=search-xxx
SEARCH_ENDPOINT=https://search-xxx.search.windows.net
SEARCH_ADMIN_KEY=def456...

# Cosmos DB
COSMOS_ACCOUNT_NAME=cosmos-xxx
COSMOS_ENDPOINT=https://cosmos-xxx.documents.azure.com
COSMOS_KEY=ghi012...

# Content Safety
CONTENT_SAFETY_ENDPOINT=https://contentsafety-xxx.cognitiveservices.azure.com
CONTENT_SAFETY_KEY=jkl345...

# ===========================================
# MCP Servers
# ===========================================
CONTAINER_REGISTRY=acrxxx.azurecr.io
CONTAINER_APP_ENV_ID=/subscriptions/.../cae-xxx
MCP_SERVER_WEATHER_URL=https://mcp-weather-xxx.azurecontainerapps.io
MCP_SERVER_ONCALL_URL=https://mcp-oncall-xxx.azurecontainerapps.io
...

# ===========================================
# Deployment Info
# ===========================================
RESOURCE_GROUP=lab-master-lab
LOCATION=uksouth
DEPLOYMENT_PREFIX=master-lab
```

---

## Progress Tracking Example

When you run Cell 15, you'll see:

```
======================================================================
MASTER LAB DEPLOYMENT - 4 STEPS
======================================================================

[*] Step 0: Ensuring resource group exists...
[OK] Resource group already exists

======================================================================
STEP 1: CORE INFRASTRUCTURE
======================================================================
[*] Resources: Log Analytics, App Insights, API Management
[*] Estimated time: ~10 minutes

[OK] Step 1 already deployed. Skipping...

[OK] Step 1 outputs retrieved:
  - APIM Gateway: https://apim-xxx.azure-api.net
  - Log Analytics: /subscriptions/.../law-xxx...

======================================================================
STEP 2: AI FOUNDRY
======================================================================
[*] Resources: 3 Foundry hubs, 3 projects, 14 AI models
[*] Estimated time: ~15 minutes

[*] Step 2 not found. Deploying...
[*] Compiling deploy-02-ai-foundry.bicep...
[OK] Compiled to deploy-02-ai-foundry.json
[*] Deploying master-lab-02-ai-foundry...
[*] Deployment started. Polling status...
[*] Still deploying... 1m 30s elapsed
[*] Still deploying... 2m 30s elapsed
...
[*] Still deploying... 14m 30s elapsed
[OK] Deployment succeeded in 15m 23s

[OK] Step 2 outputs retrieved:
  - Foundry Endpoint: https://xxx.inference.ml.azure.com

...
```

---

## Error Handling

### If Step 2 Fails (for example)

```
[ERROR] Deployment failed: Failed

Exception: Step 2 deployment failed
```

**What to do:**
1. Check Azure Portal for error details
2. Go to Resource Group: `lab-master-lab`
3. Click "Deployments"
4. Find `master-lab-02-ai-foundry`
5. Check error message (likely quota issue)

**Fix and Re-run:**
1. Fix the issue (request quota, change region, etc.)
2. Just re-run Cell 15 (Main Deployment)
3. Steps 1, 3, 4 will be skipped (already deployed)
4. Step 2 will retry

---

## Debugging Tips

### Check What's Deployed

```python
# In a new cell
exists1, _ = check_deployment_exists(resource_group_name, deployment_step1)
exists2, _ = check_deployment_exists(resource_group_name, deployment_step2)
exists3, _ = check_deployment_exists(resource_group_name, deployment_step3)
exists4, _ = check_deployment_exists(resource_group_name, deployment_step4)

print(f'Step 1 (Core): {"✅" if exists1 else "❌"}')
print(f'Step 2 (AI Foundry): {"✅" if exists2 else "❌"}')
print(f'Step 3 (Supporting): {"✅" if exists3 else "❌"}')
print(f'Step 4 (MCP): {"✅" if exists4 else "❌"}')
```

### Manual Compilation Check

```python
# Check Bicep compilation
compile_bicep('deploy-01-core.bicep')
compile_bicep('deploy-02-ai-foundry.bicep')
compile_bicep('deploy-03-supporting.bicep')
compile_bicep('deploy-04-mcp.bicep')
```

### Get Outputs Manually

```python
# Get outputs from a specific step
outputs = get_deployment_outputs(resource_group_name, deployment_step1)
print(json.dumps(outputs, indent=2))
```

---

## Cost Estimates

**Total Monthly Cost (24/7)**: ~$650-750

Breakdown:
- **APIM StandardV2**: ~$300/month
- **Redis Enterprise**: ~$150/month
- **Cognitive Search (Basic)**: ~$75/month
- **AI Foundry (3 hubs)**: $0 (pay-per-use)
- **Cosmos DB**: ~$25/month
- **Container Apps**: ~$50/month
- **Other**: ~$50/month

**Optimization**:
- Stop APIM when not in use: Save ~$300/month
- Use Free tier Cosmos DB: Save ~$25/month
- Scale Container Apps to 0: Save ~$50/month
- **Optimized cost**: ~$200-300/month

---

## Cleanup

To remove all resources:

1. **Via Portal**:
   - Go to Resource Group: `lab-master-lab`
   - Click "Delete resource group"
   - Type name to confirm
   - Delete

2. **Via CLI**:
   ```bash
   az group delete --name lab-master-lab --yes --no-wait
   ```

3. **Via Python**:
   ```python
   resource_client.resource_groups.begin_delete(resource_group_name)
   ```

---

## Troubleshooting

### Issue: "azure.mgmt.resource not found"

**Solution**: Install packages from requirements.txt
```bash
pip install -r requirements.txt
```

### Issue: "AzureCliCredential failed to get token"

**Solution**: Re-authenticate
```bash
az login
az account set --subscription <your-subscription-id>
```

### Issue: Deployment takes too long (>60 minutes)

**Solution**: This is normal for first deployment
- APIM alone takes 15-20 minutes
- AI Foundry with 14 models takes 15-20 minutes
- Total can be 40-50 minutes
- Monitor in Azure Portal

### Issue: Quota exceeded for AI models

**Solution**: Request quota increase
1. Azure Portal → Quotas
2. Search for "Azure OpenAI"
3. Request increase for your region
4. Or reduce models in `deploy-02-ai-foundry.bicep`

---

## Backup Files Created

- `master-ai-gateway.ipynb.bkp-20251026-155639` - Before rebuild
- `master-ai-gateway.ipynb.bkp-20251026-102408` - Earlier backup

To restore:
```bash
cp master-ai-gateway.ipynb.bkp-20251026-155639 master-ai-gateway.ipynb
```

---

## Summary

✅ **Modular Architecture** - 4 separate deployment steps
✅ **Azure Python SDK** - No CLI consumption errors
✅ **Resource Checking** - Skips if already deployed
✅ **Progress Tracking** - Real-time updates
✅ **Error Recovery** - Re-run individual steps
✅ **Clean .env** - Grouped by service
✅ **WSL Compatible** - Uses .venv Python only
✅ **Debuggable** - Easy to see where failures occur

**Total Deployment Time**: ~40 minutes (first time), ~1 minute (subsequent)
**Total Resources**: ~35 Azure resources
**Ready to Use**: Yes! Open notebook and run cells 0-17

🚀 **Happy deploying!**
