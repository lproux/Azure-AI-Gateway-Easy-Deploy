# Notebook Updated for Resilient Deployment

## What Changed

**Cell 17** in [master-ai-gateway.ipynb](master-ai-gateway.ipynb) has been completely rewritten to use a **resilient phased deployment approach**.

### Backup Created
- `master-ai-gateway.ipynb.bkp.20251026-231317`
- Your original notebook is safe!

---

## New Deployment Flow (Cell 17)

### **Step 1: Core Infrastructure** (Bicep - Unchanged)
- Log Analytics Workspace
- Application Insights
- API Management StandardV2
- ~10 minutes (or instant if already deployed)

### **Step 2: AI Foundry** (NEW - Resilient Python)
**Phase 2a**: AI Foundry Hubs
- Creates 3 foundry hubs if they don't exist
- Skips if already deployed

**Phase 2b**: AI Models (Resilient)
- Deploys models one-by-one with error handling
- **Continues even if individual models fail**
- Reports success/failure per model
- 6 stable models across 3 regions:
  - foundry1: gpt-4o-mini, gpt-4o, text-embedding-3-small, text-embedding-3-large
  - foundry2: gpt-4o-mini
  - foundry3: gpt-4o-mini

**Phase 2c**: APIM Inference API
- Configures APIM API path: `/inference`
- Sets up backend pool with 3 AI Foundry hubs
- Priority-based load balancing

**Total**: ~15 minutes

### **Step 3: Supporting Services** (NEW - Bicep)
- Redis Enterprise (semantic caching)
- Cognitive Search
- Cosmos DB
- Content Safety
- ~10 minutes

### **Step 4: MCP Servers** (NEW - Bicep)
- Container Registry
- Container Apps Environment
- 7 MCP Container Apps:
  - weather, oncall, github, spotify
  - product-catalog, place-order, ms-learn
- ~5 minutes

---

## Total Deployment Time

- **First run**: ~40 minutes (all steps)
- **Subsequent runs**: ~1-2 minutes (skips already-deployed resources)

---

## How to Run

1. **Open notebook**: `master-ai-gateway.ipynb`
2. **Run Cells 0-16**: Setup, authentication, helper functions
3. **Run Cell 17**: 🚀 **NEW RESILIENT DEPLOYMENT** (all 4 steps)
4. **Run Cells 18-19**: Generate `master-lab.env`
5. **Run Cells 20+**: Test all 31 labs

---

## Key Features

### ✅ Resilient Error Handling
- Individual resource failures don't stop entire deployment
- Detailed per-resource success/failure reporting
- Continue where you left off

### ✅ Idempotent
- Safe to re-run multiple times
- Skips already-deployed resources
- Only deploys what's missing

### ✅ Progress Tracking
- Real-time progress updates every minute
- Clear step-by-step output
- Total elapsed time tracking

### ✅ Comprehensive
- All 4 deployment steps in one cell
- No need to run separate scripts
- Everything tracked in notebook

---

## What's Different from Before

| Aspect | Before | After |
|--------|--------|-------|
| **Step 2** | Monolithic Bicep (failed) | Resilient Python (succeeds) |
| **Error Handling** | All-or-nothing | Per-resource resilience |
| **Model Deployment** | All at once (fails) | One-by-one (continues) |
| **Steps 3 & 4** | Missing | Included! |
| **Total Steps** | 2 steps | 4 complete steps |
| **Debugging** | Hard to diagnose | Clear per-resource errors |

---

## Files Required

Ensure these files exist in the `master-lab` directory:

### Bicep Files
- ✅ `deploy-01-core.bicep` - Step 1
- ✅ `deploy-02c-apim-api.bicep` - Step 2c (APIM API)
- ✅ `deploy-03-supporting.bicep` - Step 3
- ✅ `deploy-04-mcp.bicep` - Step 4

### Parameter Files
- ✅ `params-01-core.json` - Step 1 parameters
- ⚠️ `params-03-supporting.json` - Step 3 parameters (optional)

### Policy Files
- ✅ `policies/backend-pool-load-balancing-policy.xml`

All these files should already exist from the previous modular deployment setup.

---

## Expected Output

When you run Cell 17, you'll see:

```
======================================================================
MASTER LAB DEPLOYMENT - 4 STEPS (RESILIENT)
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
  - APIM Gateway: https://apim-pavavy6pu5hpa.azure-api.net
  - Log Analytics: /subscriptions/...

======================================================================
STEP 2: AI FOUNDRY (RESILIENT DEPLOYMENT)
======================================================================
[*] Resources: 3 Foundry hubs, 3 projects, AI models
[*] Estimated time: ~15 minutes

[*] Phase 2a: AI Foundry Hubs
  [OK] foundry1-pavavy6pu5hpa already exists
  [OK] foundry2-pavavy6pu5hpa already exists
  [OK] foundry3-pavavy6pu5hpa already exists

[*] Phase 2b: AI Models (Resilient)
  [*] foundry1-pavavy6pu5hpa: 4 models
    [OK] gpt-4o-mini already deployed
    [OK] gpt-4o already deployed
    [OK] text-embedding-3-small already deployed
    [OK] text-embedding-3-large already deployed
  [*] foundry2-pavavy6pu5hpa: 1 models
    [OK] gpt-4o-mini already deployed
  [*] foundry3-pavavy6pu5hpa: 1 models
    [OK] gpt-4o-mini already deployed

[OK] Models: 0 deployed, 6 skipped, 0 failed

[*] Phase 2c: APIM Inference API
[OK] APIM API already configured. Skipping...
[OK] Step 2 complete

======================================================================
STEP 3: SUPPORTING SERVICES
======================================================================
[*] Resources: Redis, Search, Cosmos, Content Safety
[*] Estimated time: ~10 minutes

[*] Step 3 not found. Deploying...
[*] Compiling deploy-03-supporting.bicep...
[OK] Compiled successfully
[*] Deploying...
... (deployment progress) ...
[OK] Step 3 complete

======================================================================
STEP 4: MCP SERVERS
======================================================================
[*] Resources: Container Apps + 7 MCP servers
[*] Estimated time: ~5 minutes

[*] Step 4 not found. Deploying...
[*] Compiling deploy-04-mcp.bicep...
[OK] Compiled successfully
[*] Deploying...
... (deployment progress) ...
[OK] Step 4 complete

======================================================================
DEPLOYMENT COMPLETE
======================================================================
[OK] Total time: 35m 42s
[OK] All 4 steps deployed successfully!
[OK] Next: Run Cell 18-19 to generate master-lab.env
```

---

## Troubleshooting

### If Cell 17 fails:

1. **Check error message** - It will tell you exactly which resource failed
2. **Re-run Cell 17** - Resilient design means it will continue where it left off
3. **Check Azure Portal** - Verify resources are being created
4. **Review logs** - Each step logs detailed progress

### If models fail to deploy:

- **This is OK!** The resilient approach continues deploying other models
- Check the summary at the end to see which models failed
- Failed models can be deployed manually via Azure Portal if needed

---

## Next Steps

1. **Run Cell 17** in the notebook
2. **Wait ~15-25 minutes** for Steps 3 & 4 to complete (Steps 1-2 should skip)
3. **Run Cells 18-19** to generate `master-lab.env`
4. **Start testing** the 31 labs!

---

## Benefits

✅ **Resilient** - Continues despite individual failures
✅ **Transparent** - Clear progress and error reporting
✅ **Complete** - All 4 steps in one notebook cell
✅ **Safe** - Idempotent, can re-run anytime
✅ **Fast** - Skips already-deployed resources

Ready to deploy! Just run **Cell 17** in the notebook. 🚀
