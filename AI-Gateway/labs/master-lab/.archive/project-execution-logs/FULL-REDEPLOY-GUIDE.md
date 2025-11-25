# Full Redeploy Guide - Post Resource Group Deletion

**Date**: 2025-11-15
**Status**: Resource Group Deleted - Ready for Redeployment
**Deletion Duration**: 11 minutes

---

## Pre-Deployment Status

### Resource Group Deletion
- **Name**: lab-master-lab
- **Status**: ✅ DELETED (confirmed at 2025-11-15)
- **Deletion Method**: `az group delete --name lab-master-lab --yes --no-wait`
- **Verification**: `az group exists --name lab-master-lab` returns `false`

### Why Full Redeploy Was Needed
1. **Attempt 1 FAILED**: Container Instance restart (1/7 working)
2. **Attempt 2 FAILED**: Bicep deployment of Container Apps (6/7 failed to provision)
3. **User Decision**: "option 1" - Full redeploy from scratch

---

## Deployment Instructions

### Step 1: Open Jupyter Notebook

```bash
cd "/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab"

# Open notebook (choose your editor)
code master-ai-gateway-fix-MCP.ipynb
# OR
jupyter lab master-ai-gateway-fix-MCP.ipynb
```

### Step 2: Execute Deployment Cells (1-32)

#### Cells 1-13: Environment Setup (1-2 minutes)
**Purpose**: Configure Python environment and import packages

**Expected Output**:
```python
# Cell 1: Package installation
Successfully installed azure-cli azure-identity ...

# Cell 2-13: Variable definitions
subscription_id = "d334f2cd-3efd-494e-9fd3-2470b1a13e4c"
resource_group_name = "lab-master-lab"
location = "uksouth"
```

**Action**: Run cells 1-13 sequentially. Should complete without errors.

---

#### Cell 14-31: 4-Step Infrastructure Deployment (~40 minutes)

##### **Step 1: Core Infrastructure** (~10 min)

**What Deploys**:
- API Management (APIM) Service
- Log Analytics Workspace
- Application Insights

**Cell to Run**: Cell containing `deployment_step1 = 'master-lab-01-core'`

**Expected Output**:
```
Deployment 'master-lab-01-core' started...
[10 min wait]
✅ APIM created: apim-{uniqueId}.azure-api.net
✅ Log Analytics created: law-{uniqueId}
✅ Step 1 Complete
```

**Verification Command** (after cell completes):
```bash
az resource list -g lab-master-lab --query "[?type=='Microsoft.ApiManagement/service'].name" -o tsv
# Should show: apim-{uniqueId}
```

---

##### **Step 2: AI Foundry** (~15 min)

**What Deploys**:
- 3 AI Foundry Hubs (UK South, West Europe, East US 2)
- 14 Azure OpenAI models across hubs:
  - gpt-4o-mini (×3 regions)
  - gpt-4o (×3 regions)
  - text-embedding-ada-002 (×3 regions)
  - dall-e-3 (×3 regions - may fail due to quota)
  - whisper (×2 regions)

**Cell to Run**: Cell containing `deployment_step2 = 'master-lab-02-ai-foundry'`

**Expected Output**:
```
Deployment 'master-lab-02-ai-foundry' started...
[15 min wait - longest step]
✅ Hub 1 created: foundry1-{uniqueId} (UK South)
✅ Hub 2 created: foundry2-{uniqueId} (West Europe)
✅ Hub 3 created: foundry3-{uniqueId} (East US 2)
✅ Models deployed: 11-14/14 (dall-e-3 may fail - expected)
✅ Step 2 Complete
```

**Known Issue**: dall-e-3 deployment may fail with quota errors. This is EXPECTED and non-blocking.

**Verification Command**:
```bash
az resource list -g lab-master-lab --query "[?type=='Microsoft.MachineLearningServices/workspaces'].name" -o tsv
# Should show 3 AI Foundry hubs
```

---

##### **Step 3: Supporting Services** (~10 min)

**What Deploys**:
- Azure Redis Cache (semantic caching)
- Azure Cognitive Search (vector search)
- Azure Cosmos DB (state storage)
- Azure Content Safety

**Cell to Run**: Cell containing `deployment_step3 = 'master-lab-03-supporting'`

**Expected Output**:
```
Deployment 'master-lab-03-supporting' started...
[10 min wait]
✅ Redis created: redis-{uniqueId}.redis.azure.net
✅ Search created: search-{uniqueId}.search.windows.net
✅ Cosmos created: cosmos-{uniqueId}.documents.azure.com
✅ Content Safety created
✅ Step 3 Complete
```

**Verification Command**:
```bash
az redis show -g lab-master-lab -n redis-{uniqueId} --query "provisioningState" -o tsv
# Should show: Succeeded
```

---

##### **Step 4: MCP Servers** (~5 min) - **CRITICAL**

**What Deploys**:
- Azure Container App Environment
- 7 MCP Container Apps:
  1. mcp-weather
  2. mcp-oncall
  3. mcp-github
  4. mcp-spotify
  5. mcp-product-catalog
  6. mcp-place-order
  7. mcp-ms-learn

**Cell to Run**: Cell containing `deployment_step4 = 'master-lab-04-mcp'`

**Expected Output**:
```
Deployment 'master-lab-04-mcp' started...
[5 min wait]
✅ Container App Environment created: cae-{uniqueId}
✅ MCP App 1/7: mcp-weather (Succeeded)
✅ MCP App 2/7: mcp-oncall (Succeeded)
✅ MCP App 3/7: mcp-github (Succeeded)
✅ MCP App 4/7: mcp-spotify (Succeeded)
✅ MCP App 5/7: mcp-product-catalog (Succeeded)
✅ MCP App 6/7: mcp-place-order (Succeeded)
✅ MCP App 7/7: mcp-ms-learn (Succeeded)
✅ Step 4 Complete - ALL APPS DEPLOYED
```

**CRITICAL**: This step must deploy ALL 7 apps successfully (not 1/7 like before).

**Verification Commands** (run IMMEDIATELY after cell completes):
```bash
# Check Container App count
az containerapp list -g lab-master-lab --query "length([])"
# MUST show: 7

# Check individual app status
az containerapp list -g lab-master-lab \
  --query "[].{Name:name, State:properties.provisioningState, Health:properties.runningStatus}" \
  -o table

# EXPECTED:
# Name                          State      Health
# ----------------------------  ---------  --------
# mcp-weather-{uniqueId}        Succeeded  Running
# mcp-oncall-{uniqueId}         Succeeded  Running
# mcp-github-{uniqueId}         Succeeded  Running
# mcp-spotify-{uniqueId}        Succeeded  Running
# mcp-product-catalog-{uniqueId} Succeeded Running
# mcp-place-order-{uniqueId}    Succeeded  Running
# mcp-ms-learn-{uniqueId}       Succeeded  Running
```

**IF ANY APPS SHOW "Failed"**: STOP and investigate logs before proceeding.

---

#### Cell 32: Generate master-lab.env (30 seconds)

**Purpose**: Create environment configuration file with deployment outputs

**Expected Output**:
```bash
# master-lab.env created with:
APIM_GATEWAY_URL=https://apim-{uniqueId}.azure-api.net
APIM_API_KEY={generated-key}

MCP_SERVER_WEATHER_URL=https://mcp-weather-{uniqueId}.{region}.azurecontainerapps.io
MCP_SERVER_ONCALL_URL=https://mcp-oncall-{uniqueId}.{region}.azurecontainerapps.io
# ... (7 MCP URLs total)

REDIS_HOST=redis-{uniqueId}.redis.azure.net
SEARCH_ENDPOINT=https://search-{uniqueId}.search.windows.net
COSMOS_ENDPOINT=https://cosmos-{uniqueId}.documents.azure.com
```

**File Location**: `master-lab/master-lab.env`

---

## Post-Deployment Verification

### Verification Script (Run After Cell 32 Completes)

```bash
cd "/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab"

# Test all 7 MCP Container Apps HTTP connectivity
python3 << 'EOF'
import httpx
import os
from dotenv import load_dotenv

load_dotenv("master-lab.env")

mcp_servers = {
    "weather": os.getenv("MCP_SERVER_WEATHER_URL"),
    "oncall": os.getenv("MCP_SERVER_ONCALL_URL"),
    "github": os.getenv("MCP_SERVER_GITHUB_URL"),
    "spotify": os.getenv("MCP_SERVER_SPOTIFY_URL"),
    "product-catalog": os.getenv("MCP_SERVER_PRODUCT_CATALOG_URL"),
    "place-order": os.getenv("MCP_SERVER_PLACE_ORDER_URL"),
    "ms-learn": os.getenv("MCP_SERVER_MS_LEARN_URL")
}

print("=== MCP Container Apps Connectivity Test ===\n")

results = {}
for name, url in mcp_servers.items():
    if not url:
        print(f"❌ {name}: URL not found in master-lab.env")
        continue

    print(f"[{name}] {url}")

    for endpoint in ["/health", "/"]:
        try:
            response = httpx.get(f"{url}{endpoint}", timeout=15.0, follow_redirects=True)
            print(f"  ✅ {endpoint}: {response.status_code}")
            results[name] = {"status": "UP", "code": response.status_code}
            break
        except httpx.TimeoutException:
            print(f"  ⏱️  {endpoint}: Timeout (30s)")
        except Exception as e:
            print(f"  ❌ {endpoint}: {str(e)[:60]}")

    if name not in results:
        results[name] = {"status": "DOWN"}
    print()

up = sum(1 for r in results.values() if r["status"] == "UP")
print(f"\n=== SUMMARY ===")
print(f"MCP Apps UP: {up}/7")
print(f"MCP Apps DOWN: {7-up}/7")

if up == 7:
    print("\n✅ SUCCESS: All 7 MCP Container Apps are responding!")
    print("✅ Ready to proceed with notebook cell updates")
elif up > 0:
    print(f"\n⚠️  PARTIAL: {up}/7 apps responding")
    print("⚠️  Investigate failed apps before proceeding")
else:
    print("\n❌ FAILURE: 0/7 apps responding")
    print("❌ Check Container App logs and redeploy if needed")
EOF
```

**Expected Result**: `MCP Apps UP: 7/7`

---

## Success Criteria

### ✅ Deployment Successful When:

1. **Resource Group Created**:
   ```bash
   az group show --name lab-master-lab --query "properties.provisioningState" -o tsv
   # Output: Succeeded
   ```

2. **All 4 Deployment Steps Completed**:
   - Step 1: Core Infrastructure (APIM, Log Analytics)
   - Step 2: AI Foundry (3 hubs, 11-14 models)
   - Step 3: Supporting Services (Redis, Search, Cosmos)
   - Step 4: MCP Servers (7 Container Apps)

3. **7/7 MCP Container Apps Deployed**:
   ```bash
   az containerapp list -g lab-master-lab --query "length([])"
   # Output: 7
   ```

4. **7/7 MCP Apps Responding to HTTP**:
   - Run verification script above
   - All apps return 200 or 307 status codes

5. **master-lab.env File Generated**:
   - Contains 7 MCP URLs
   - Contains APIM gateway URL and key
   - Contains Redis, Search, Cosmos endpoints

---

## Next Steps After Successful Deployment

### 1. Update MCP-Dependent Notebook Cells

**Cells to Update** (30+ cells):
- Cell 82-94: Lab 10 MCP examples (13 cells)
- Cell 96: Product catalog MCP
- Cell 98: AutoGen + MCP
- Cell 105: Workflow with MCP
- Cell 146-150: MCP authorization tests (5 cells)

**Changes Needed**:
- Replace old Container Instance URLs with new Container App URLs from master-lab.env
- Update endpoint paths if needed (HTTP `/mcp` vs SSE `/sse`)

### 2. Continue Sequential Cell Fixes

**Cells 50+**: Fix remaining issues per RUNALL-FIX-TRACKER.md
- Load balancing policy (cell 48)
- Semantic cache (cell 107)
- Cosmos firewall (cell 160)
- Image generation limitations (cells 113, 115, 136, 177-178)

### 3. Test "Run All" Execution

**Goal**: Execute entire notebook (210 cells) without blocking errors

---

## Troubleshooting

### Issue: Step 4 (MCP) Deployment Fails Again

**Symptoms**:
- Container Apps created but show "Failed" state
- HTTP connectivity test shows 0/7 or 1/7 responding

**Solutions**:
1. **Check Container App Logs**:
   ```bash
   az containerapp logs show \
     --name mcp-weather-{uniqueId} \
     --resource-group lab-master-lab \
     --type console
   ```

2. **Check Container App Environment**:
   ```bash
   az containerapp env show \
     --name cae-{uniqueId} \
     --resource-group lab-master-lab
   ```

3. **Manual Redeploy of Failed App**:
   ```bash
   # Get failed app details
   az containerapp show \
     --name mcp-weather-{uniqueId} \
     --resource-group lab-master-lab

   # Delete and recreate if needed
   az containerapp delete \
     --name mcp-weather-{uniqueId} \
     --resource-group lab-master-lab \
     --yes

   # Re-run cell 32 Step 4
   ```

4. **If multiple apps fail**: Delete entire resource group again and investigate Bicep template issues

---

### Issue: dall-e-3 Model Deployment Fails

**This is EXPECTED** - dall-e-3 requires specific SKU/quota that may not be available.

**Impact**: Low - only affects image generation cells (113, 115, 136, 177-178)

**Solution**: Document as known limitation, skip affected cells

---

### Issue: Deployment Takes Longer Than 40 Minutes

**Typical Duration by Step**:
- Step 1: 8-12 minutes
- Step 2: 12-20 minutes (longest)
- Step 3: 8-12 minutes
- Step 4: 3-7 minutes

**Total Expected**: 31-51 minutes

**If exceeds 60 minutes**: Check Azure portal for stuck deployments, cancel and retry

---

## Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Resource Group Deletion | 11 min | ✅ COMPLETE |
| **Deployment (cells 1-32)** | **40 min** | **⏳ PENDING** |
| Verification | 5 min | ⏳ PENDING |
| Cell Updates | 20 min | ⏳ PENDING |
| Sequential Fixes | 60+ min | ⏳ PENDING |

---

## Summary

**Current Status**: Resource group deleted, ready for fresh deployment

**Action Required**: Run notebook cells 1-32 to deploy all infrastructure

**Critical Success Factor**: Step 4 (MCP) must deploy ALL 7 Container Apps successfully (7/7, not 1/7)

**Estimated Time**: 40 minutes for deployment + 5 minutes for verification

**Next Steps**: After successful deployment, update 30+ MCP-dependent cells and continue sequential fixes

---

**Created**: 2025-11-15
**For**: Full Redeploy After Resource Group Deletion
**Status**: ✅ Deletion Complete - Ready for Deployment
