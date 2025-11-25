# Post-Redeployment Status & Fix Strategy

**Date**: 2025-11-15
**Status**: Deployment Complete - Configuration Issues
**Strategy**: Option D - Systematic Initialization & Sequential Fixes

---

## Deployment Status Summary

### ✅ Infrastructure Deployed Successfully

| Component | Status | Details |
|-----------|--------|---------|
| **Resource Group** | ✅ EXISTS | lab-master-lab |
| **APIM** | ✅ DEPLOYED | apim-pavavy6pu5hpa.azure-api.net |
| **AI Foundry Hubs** | ✅ DEPLOYED | 3 hubs (UK South, West Europe, East US 2) |
| **AI Models** | ⚠️ PARTIAL | 11-14/14 (dall-e-3 failed - expected) |
| **Redis** | ✅ DEPLOYED | redis-pavavy6pu5hpa.redis.azure.net |
| **Cosmos DB** | ✅ DEPLOYED | cosmos-pavavy6pu5hpa.documents.azure.com |
| **Search** | ✅ DEPLOYED | search-pavavy6pu5hpa.search.windows.net |
| **MCP Container Apps** | ✅ DEPLOYED | 7/7 Running |

### ❌ Configuration Issues

| Issue | Impact | Root Cause |
|-------|--------|------------|
| **APIM_API_KEY missing** | All 401 errors | master-lab.env generation timeout |
| **Client not initialized** | Cell execution errors | Variable not set in cells |
| **MCP servers timeout** | 30+ cells fail | Ingress/URL configuration issue |
| **JWT not working** | Access control fails | Missing subscription key |
| **Load balancing not working** | Policy applied but no effect | Auth issues block testing |

---

## Critical Findings

### Issue 1: APIM Subscription Key Missing

**Cell 34 Output**:
```
[!] Could not auto-discover APIM_API_ID: Command timeout after 60 seconds
[!] Using default APIM_API_ID: inference-api
```

**Impact**: master-lab.env missing `APIM_API_KEY` variable
**Result**: All API calls return 401 "Access denied due to invalid subscription key"

**Solution Required**:
1. Get APIM subscription key via Azure Portal or REST API
2. Add to master-lab.env
3. Reload env in all cells

### Issue 2: Client Variable Not Initialized

**Cell 43 Error**:
```python
NameError: name 'client' is not defined
```

**Root Cause**: OpenAI client initialization cell not executed or variable not propagated

**Solution Required**:
1. Add client initialization in early setup cells
2. Ensure client variable is in notebook scope
3. Reference working initialization from archive/access-control-verbose.ipynb

### Issue 3: MCP Servers Deployed But Unreachable

**Cell 83-85 Errors**:
```
httpx.ReadTimeout: The read operation timed out (30s)
MCP initialization error: The read operation timed out
```

**Status**:
- Azure Status: 7/7 apps "Running"
- HTTP Test: 0/7 responding (all timeout after 30s)

**Possible Causes**:
1. Ingress not configured (external access disabled)
2. Port mismatch (container vs ingress)
3. Health probe failing (apps crash-looping)
4. Firewall/network rules

**Solution Required**:
1. Check Container App ingress configuration
2. Verify health probes
3. Check application logs
4. Test with longer timeout (60s+)

### Issue 4: Azure CLI MSAL Bug

**Cell 64 Error**:
```
ERROR: Can't get attribute 'NormalizedResponse' on <module 'msal.throttled_http_client'
```

**Known Issue**: Azure CLI version incompatibility
**Workaround**: Use direct REST API calls instead of `az` commands

---

## Reference: Working Archive

**File**: `archive/access-control-verbose.ipynb`
**Last Known Working**: 2025-11-14 (per filename)

**What to Extract**:
1. APIM subscription key retrieval method
2. Client initialization pattern
3. JWT token configuration
4. Environment variable propagation
5. MCP server connection logic

---

## Fix Strategy: Option D Implementation

### Phase 1: Variable Initialization & Propagation (PRIORITY 1)

**Goal**: Ensure all variables are properly initialized and propagated throughout notebook

**Tasks**:
1. **Extract working patterns from archive/access-control-verbose.ipynb**:
   - APIM subscription key retrieval
   - OpenAI client initialization
   - JWT token configuration
   - Environment loading pattern

2. **Fix Cell 34 (master-lab.env generation)**:
   - Add robust APIM subscription key retrieval
   - Remove timeout on REST API calls
   - Validate all required variables present
   - Add error handling for missing values

3. **Add Client Initialization Cell** (after env load):
   ```python
   from openai import AzureOpenAI
   from dotenv import load_dotenv
   import os

   load_dotenv("master-lab.env")

   client = AzureOpenAI(
       azure_endpoint=os.getenv("APIM_GATEWAY_URL"),
       api_key=os.getenv("APIM_API_KEY"),
       api_version="2024-08-01-preview"
   )
   ```

4. **Validate Variable Propagation**:
   - Add diagnostic cell showing all critical variables
   - Verify variables accessible in later cells
   - Test client object available

### Phase 2: MCP Server Connectivity (PRIORITY 2)

**Goal**: Fix MCP Container Apps HTTP connectivity

**Diagnostic Steps**:
1. **Check Container App Ingress**:
   ```bash
   az containerapp show -g lab-master-lab -n mcp-weather-pavavy6pu5 \
     --query "properties.configuration.ingress" -o json
   ```

2. **Check Application Logs**:
   ```bash
   az containerapp logs show -g lab-master-lab -n mcp-weather-pavavy6pu5 \
     --type console --tail 50
   ```

3. **Test with Direct HTTP** (bypass notebook):
   ```bash
   curl -v https://mcp-weather-pavavy6pu5.niceriver-900455a0.uksouth.azurecontainerapps.io/health
   ```

**Fix Actions**:
- If ingress disabled: Enable external ingress
- If port mismatch: Update ingress target port
- If app crashing: Fix startup command/env vars
- If timeout persists: Increase to 60s+ timeout

### Phase 3: Access Control Lab (PRIORITY 3)

**Goal**: Fix JWT authentication and API key flows

**Dependencies**: Phase 1 complete (APIM_API_KEY available)

**Tasks**:
1. Fix Cell 41: Basic chat completion (requires client + APIM_API_KEY)
2. Fix Cell 43: Streaming (requires client initialization)
3. Fix Cell 45: JWT authentication (requires JWT token generation)
4. Fix Cell 59-64: API-KEY-only and JWT-only flows

**Reference**: `archive/access-control-verbose.ipynb` cells with JWT logic

### Phase 4: Sequential Cell Fixes (PRIORITY 4)

**Goal**: Continue sequential fixes per original RUNALL-FIX-TRACKER.md plan

**Order**:
1. Load balancing (Cell 48) - after auth fixed
2. Token metrics (Cell 52) - after API calls working
3. Semantic cache (Cell 107) - after APIM policy working
4. Cosmos DB firewall (Cell 160)
5. Search index creation (Cell 162)

---

## Immediate Action Plan

### Step 1: Get APIM Subscription Key (5 min)

**Option A: Azure Portal** (Manual)
1. Navigate to Azure Portal → APIM service → Subscriptions
2. Find "master" or "all-apis" subscription
3. Copy Primary Key
4. Manually add to master-lab.env

**Option B: REST API** (Automated)
```bash
# Try different subscription names
for sub in "master" "all-apis" "unlimited" "built-in"; do
  az rest --method get \
    --url "https://management.azure.com/subscriptions/d334f2cd-3efd-494e-9fd3-2470b1a13e4c/resourceGroups/lab-master-lab/providers/Microsoft.ApiManagement/service/apim-pavavy6pu5hpa/subscriptions/$sub?api-version=2022-08-01" \
    --query "properties.primaryKey" -o tsv 2>/dev/null && break
done
```

**Option C: List All Subscriptions**
```bash
az rest --method get \
  --url "https://management.azure.com/subscriptions/d334f2cd-3efd-494e-9fd3-2470b1a13e4c/resourceGroups/lab-master-lab/providers/Microsoft.ApiManagement/service/apim-pavavy6pu5hpa/subscriptions?api-version=2022-08-01" \
  --query "value[0].properties.primaryKey" -o tsv
```

### Step 2: Update master-lab.env (2 min)

Add missing line:
```bash
APIM_API_KEY=<key-from-step-1>
```

### Step 3: Add Client Initialization Cell (3 min)

Insert after Cell 34 (env generation):
```python
# Cell 35: Initialize OpenAI Client
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv("master-lab.env")

# Verify critical variables loaded
required_vars = ["APIM_GATEWAY_URL", "APIM_API_KEY", "APIM_API_ID"]
missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    print(f"❌ Missing environment variables: {missing}")
    print("❌ Run Cell 34 to generate master-lab.env first")
else:
    # Initialize OpenAI client
    client = AzureOpenAI(
        azure_endpoint=os.getenv("APIM_GATEWAY_URL"),
        api_key=os.getenv("APIM_API_KEY"),
        api_version="2024-08-01-preview"
    )
    print(f"✅ OpenAI client initialized")
    print(f"✅ Endpoint: {os.getenv('APIM_GATEWAY_URL')}")
    print(f"✅ API Key: {os.getenv('APIM_API_KEY')[:8]}...")
```

### Step 4: Investigate MCP Connectivity (10 min)

```bash
# Check one MCP app in detail
APP_NAME="mcp-weather-pavavy6pu5"

# 1. Check ingress configuration
az containerapp show -g lab-master-lab -n $APP_NAME \
  --query "{ingress: properties.configuration.ingress, health: properties.runningStatus}" \
  -o json

# 2. Check application logs
az containerapp logs show -g lab-master-lab -n $APP_NAME \
  --type console --tail 100

# 3. Test HTTP connectivity directly
curl -v --max-time 60 \
  https://$APP_NAME.niceriver-900455a0.uksouth.azurecontainerapps.io/health
```

### Step 5: Extract Working Patterns from Archive (10 min)

Read specific cells from `archive/access-control-verbose.ipynb`:
- Cell with APIM key retrieval
- Cell with client initialization
- Cell with JWT token generation
- Cells with working MCP connections

---

## Success Criteria

### Phase 1 Complete When:
- [ ] APIM_API_KEY exists in master-lab.env
- [ ] `client` variable initialized and accessible
- [ ] Cell 41 returns 200 (not 401)
- [ ] Cell 43 streaming works
- [ ] Diagnostic cell shows all vars loaded

### Phase 2 Complete When:
- [ ] At least 1 MCP server responds within 30s
- [ ] Understand root cause of timeouts
- [ ] Have fix strategy for all 7 servers

### Phase 3 Complete When:
- [ ] Cell 59-60: API-KEY-only flow works
- [ ] Cell 61-62: JWT-only flow works
- [ ] Cell 63-64: Dual auth works
- [ ] All access control cells execute without errors

### Phase 4 Complete When:
- [ ] Load balancing shows distribution across regions
- [ ] Token metrics logging verified
- [ ] Sequential fixes per original plan proceeding

---

## Time Estimates

| Phase | Task | Est. Time |
|-------|------|-----------|
| **Phase 1** | Get APIM key + update env | 5 min |
| | Add client init cell | 3 min |
| | Extract archive patterns | 10 min |
| | Test & validate | 5 min |
| | **Phase 1 Total** | **23 min** |
| **Phase 2** | Diagnose MCP connectivity | 10 min |
| | Fix ingress/config | 10 min |
| | Test all 7 servers | 5 min |
| | **Phase 2 Total** | **25 min** |
| **Phase 3** | Fix access control cells | 15 min |
| | Test JWT flows | 10 min |
| | **Phase 3 Total** | **25 min** |
| **Phase 4** | Sequential fixes | 60+ min |
| | | |
| **TOTAL** | | **133 min (~2.5 hrs)** |

---

## Risks & Mitigations

### Risk 1: APIM Subscription Doesn't Exist
**Mitigation**: Create new subscription via REST API if needed

### Risk 2: MCP Apps Fundamentally Broken
**Mitigation**: Redeploy single app as test, fix config, then apply to all

### Risk 3: Archive Patterns Incompatible
**Mitigation**: Use archive as reference only, adapt to current structure

### Risk 4: Token Limit Reached
**Current**: 114k/200k used (86k remaining)
**Mitigation**: Complete Phase 1-2 in this session, continue Phase 3-4 in new session if needed

---

## Next Immediate Steps

**RIGHT NOW**:
1. Get APIM subscription key (Option B or C above)
2. Update master-lab.env
3. Add client initialization cell
4. Test Cell 41 for 200 response

**THEN**:
5. Diagnose MCP connectivity
6. Extract patterns from archive
7. Continue sequential fixes

---

**Created**: 2025-11-15
**Strategy**: Option D - Systematic Init + Sequential Fixes
**Status**: Ready to Execute Phase 1
**Next**: Get APIM subscription key
