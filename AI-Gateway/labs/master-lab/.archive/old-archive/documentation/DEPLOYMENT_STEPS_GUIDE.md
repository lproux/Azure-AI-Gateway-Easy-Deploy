# Deployment Steps Guide - Split Cells for Debugging

## Overview

The deployment has been split into **5 steps** (10 cells total) for easy debugging:

- **Step 1**: Check if deployment exists
- **Step 2**: Create resource group (if needed)
- **Step 3**: Deploy Bicep infrastructure (if needed) - **30-45 minutes**
- **Step 4**: Retrieve all outputs
- **Step 5**: Export to deployment-output.env

---

## Cell Structure

```
Cell 11: [Code] Set deployment_name, resource_group_name

Cell 12: [Markdown] Step 1 header
Cell 13: [Code] Check deployment status
         └─> Sets: deployment_exists (True/False)

Cell 14: [Markdown] Step 2 header
Cell 15: [Code] Create resource group
         └─> Only runs if: deployment_exists == False

Cell 16: [Markdown] Step 3 header
Cell 17: [Code] Deploy Bicep (30-45 min)
         └─> Only runs if: deployment_exists == False
         └─> Updates: deployment_exists = True on success

Cell 18: [Markdown] Step 4 header
Cell 19: [Code] Retrieve outputs
         └─> Defines ALL variables (apim_gateway_url, etc.)
         └─> Always runs

Cell 20: [Markdown] Step 5 header
Cell 21: [Code] Export to .env
         └─> Creates: deployment-output.env
         └─> Always runs
```

---

## Execution Workflows

### First Run (No Deployment Exists)

**Run cells in sequence**: 11 → 13 → 15 → 17 → 19 → 21

```bash
# Cell 11: Config
deployment_name = 'master-lab-deployment'
resource_group_name = 'lab-master-lab'
[OK] Config set

# Cell 13: Check status
[*] Checking if deployment exists...
[!] Deployment not found
[*] Continue to Step 2 to create it

# Cell 15: Create RG
[*] Creating resource group: lab-master-lab
[*] Location: UK South
[OK] Resource group created successfully!
[OK] Continue to Step 3

# Cell 17: Deploy Bicep (THIS TAKES 30-45 MINUTES!)
[*] Starting Bicep deployment...
[*] This will take 30-45 minutes
[*] Deploying:
    - API Management (StandardV2)
    - 3 AI Foundry hubs + projects
    - Redis Enterprise
    - Azure Cognitive Search
    - Cosmos DB
    - 7 MCP servers
    - Content Safety
[*] Monitor progress: https://portal.azure.com/...
[*] Deployment started...
... (30-45 minutes) ...
[OK] Deployment completed successfully!
[OK] Continue to Step 4

# Cell 19: Retrieve outputs
[*] Retrieving deployment outputs...
[OK] All outputs retrieved successfully!
[OK] APIM Gateway: https://...
[OK] AI Foundry: https://...
[OK] Redis: ...
[OK] Search: ...
[OK] Cosmos: ...
[OK] MCP Servers: 7 deployed
[OK] All variables are now defined!
[OK] Continue to Step 5

# Cell 21: Export .env
[*] Creating deployment-output.env...
[OK] Created deployment-output.env
[OK] =========================================
[OK] SETUP COMPLETE!
[OK] =========================================
[OK] All 31 labs are ready to test!
```

**Total time**: ~30-45 minutes

---

### Subsequent Runs (Deployment Exists)

**Run cells**: 11 → 13 → **SKIP to 19** → 21

```bash
# Cell 11: Config
[OK] Config set

# Cell 13: Check status
[*] Checking if deployment exists...
[OK] Deployment already exists!
[OK] You can skip to Step 4 (Retrieve Outputs)

# ⏭️ SKIP Cells 15 & 17 (not needed)

# Cell 19: Retrieve outputs
[*] Retrieving deployment outputs...
[OK] All outputs retrieved successfully!
[OK] All variables are now defined!

# Cell 21: Export .env
[*] Creating deployment-output.env...
[OK] SETUP COMPLETE!
```

**Total time**: ~5 seconds

---

## Debugging Scenarios

### Scenario 1: Deployment Fails at Step 3 (Cell 17)

```bash
# Cell 17 output:
[*] Deployment started...
... (waiting) ...
[!] Deployment failed!
[!] Check Azure Portal for error details:
[!] Resource Group: lab-master-lab
[!] Deployment: master-lab-deployment

Common issues:
  - Quota limits (especially for AI models)
  - Region capacity
  - Permissions (need Contributor role)

You can re-run this cell after fixing the issue.
```

**What to do:**

1. **Check Azure Portal**
   - Go to: https://portal.azure.com
   - Navigate to Resource Group: `lab-master-lab`
   - Click "Deployments" → `master-lab-deployment`
   - Check error message

2. **Common Issues:**

   **Quota Limit Error:**
   ```bash
   # Request quota increase in Azure Portal
   # Or reduce model deployments in master-deployment.bicep
   ```

   **Region Capacity Error:**
   ```bash
   # Edit master-deployment.bicep
   # Change region from uksouth to swedencentral
   ```

   **Permission Error:**
   ```bash
   # Get Contributor role on subscription
   az role assignment create --assignee <your-email> \
     --role Contributor \
     --scope /subscriptions/<subscription-id>
   ```

3. **Fix and Re-run**
   - After fixing the issue, just re-run Cell 17
   - It will attempt deployment again
   - No need to delete resource group (unless you want clean start)

---

### Scenario 2: Retrieve Outputs Fails (Cell 19)

```bash
# Cell 19 output:
[!] Failed to retrieve deployment outputs
[!] Make sure deployment completed successfully (Step 3)
```

**What to do:**

1. **Check deployment status:**
   ```bash
   az deployment group show --name master-lab-deployment -g lab-master-lab
   ```

2. **Check if deployment completed:**
   ```bash
   az deployment group show --name master-lab-deployment -g lab-master-lab \
     --query "properties.provisioningState"
   ```

   Should return: `"Succeeded"`

3. **If deployment is still running:**
   - Wait for Cell 17 to complete
   - Don't run Cell 19 until Cell 17 succeeds

4. **If deployment failed:**
   - Go back to Cell 17
   - Check error in Azure Portal
   - Fix and re-run Cell 17

---

### Scenario 3: Want to Redeploy from Scratch

```bash
# Option 1: Delete resource group
az group delete --name lab-master-lab --yes

# Option 2: Delete deployment only
az deployment group delete --name master-lab-deployment -g lab-master-lab

# Then re-run cells 13 → 15 → 17 → 19 → 21
```

---

## Benefits of Split Cells

### ✅ Debugging
- See exactly which step failed
- Don't have to re-run everything
- Can inspect Azure Portal between steps

### ✅ Flexibility
- Can skip steps if deployment exists
- Can re-run individual steps
- Can modify deployment and re-run just Step 3

### ✅ Progress Tracking
- Clear visual progress through 5 steps
- Know exactly where you are in the process
- Helpful messages guide you to next step

### ✅ Still "One-Click"
- Just run cells sequentially
- Smart logic skips unnecessary steps
- First run: 13 → 15 → 17 → 19 → 21
- Subsequent runs: 13 → 19 → 21

---

## File Created

After running all steps, you'll have:

**deployment-output.env**
```bash
# Master Lab Deployment Outputs
# Generated: 2025-10-24 HH:MM:SS

APIM_GATEWAY_URL=https://apim-master-lab.azure-api.net
APIM_SERVICE_ID=/subscriptions/.../...
APIM_API_KEY=abc123...

FOUNDRY_ENDPOINT=https://....inference.ml.azure.com

REDIS_HOST=redis-master-lab.redis.cache.windows.net
REDIS_PORT=6380
REDIS_KEY=xyz789...

SEARCH_ENDPOINT=https://search-master-lab.search.windows.net
SEARCH_KEY=def456...

COSMOS_ENDPOINT=https://cosmos-master-lab.documents.azure.com

RESOURCE_GROUP=lab-master-lab
DEPLOYMENT_NAME=master-lab-deployment
```

---

## Backup

A backup was created before splitting:

**master-ai-gateway.ipynb.bkp-20251025-102408**

To restore backup:
```bash
cd "C:\Users\lproux\OneDrive - Microsoft\bkp\Documents\GitHub\MCP-servers-internalMSFT-and-external\AI-Gateway\labs\master-lab"
cp master-ai-gateway.ipynb.bkp-20251025-102408 master-ai-gateway.ipynb
```

---

## Quick Reference

### First Run
```
11 (Config) → 13 (Check) → 15 (Create RG) → 17 (Deploy 30-45 min) → 19 (Retrieve) → 21 (Export)
```

### Subsequent Runs
```
11 (Config) → 13 (Check) → ⏭️ SKIP → ⏭️ SKIP → 19 (Retrieve) → 21 (Export)
```

### Redeploy
```bash
az group delete --name lab-master-lab --yes
# Then: 11 → 13 → 15 → 17 → 19 → 21
```

### Debug Deployment Failure
```
1. Check Azure Portal for error
2. Fix issue (quota, permissions, region, etc.)
3. Re-run Cell 17 only
4. Continue to Cell 19 → 21
```

---

## Summary

**Before Split**: 1 giant cell (hard to debug)
**After Split**: 5 steps with 10 cells (easy to debug)

**Still one-click**: Just run cells sequentially
**Debuggable**: Can see exactly where failures occur
**Flexible**: Can skip, re-run, or modify individual steps

🎯 **Best of both worlds!**
