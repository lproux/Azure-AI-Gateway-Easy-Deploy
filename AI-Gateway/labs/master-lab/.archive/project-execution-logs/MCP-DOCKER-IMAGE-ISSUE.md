# MCP Container Apps - Docker Image Issue

**Date**: 2025-11-15
**Status**: 🚨 CRITICAL INFRASTRUCTURE ISSUE DISCOVERED
**Issue**: MCP servers never deployed - Container Apps using demo "helloworld" image

---

## Executive Summary

The MCP Container Apps were deployed with the **WRONG Docker images**. The Bicep deployment template has a hardcoded placeholder image (`mcr.microsoft.com/azuredocs/containerapps-helloworld:latest`) instead of actual MCP server images.

**Impact**: Cell 83 and ~30 other MCP-dependent cells fail with initialization timeouts because the MCP server applications are not running.

---

## Root Cause Analysis

### Issue #1: Bicep Template Has Wrong Image

**File**: `archive/scripts/deploy-04-mcp.json`
**Line 128**:
```json
{
  "name": "[variables('mcpServers')[copyIndex()]]",
  "image": "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest",  // ← WRONG!
  "resources": {
    "cpu": "[json('0.25')]",
    "memory": "0.5Gi"
  }
}
```

**What This Means**:
- The Bicep template deploys a demo "Hello World" web app
- No actual MCP server code is deployed
- Container Apps show "Running" but serve HTML welcome pages, not MCP JSON-RPC

---

### Issue #2: Azure Container Registry is Empty

**Command**: `az acr repository list --name acrpavavy6pu5hpa`
**Result**: (empty list)

**What This Means**:
- No MCP server Docker images were ever built
- No images were pushed to the ACR
- The infrastructure deployment is incomplete

---

### Issue #3: No MCP Server Source Code Found

**Searched for**:
- `**/mcp-*/**/*.py` - No results
- `**/mcp*/Dockerfile` - No results

**What This Means**:
- MCP server source code is NOT in this repository
- Either:
  - MCP servers are in a different repository
  - MCP servers are pre-built public Docker images
  - MCP servers were meant to be deployed separately

---

## Evidence

### Container Configuration
```bash
az containerapp show -g lab-master-lab -n mcp-weather-pavavy6pu5 \
  --query "properties.template.containers[0]"
```

**Result**:
```json
{
  "args": null,
  "command": null,
  "env": null,
  "image": "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest"
}
```

---

### MCP Endpoint Test

**Request**:
```bash
curl https://mcp-weather-pavavy6pu5.niceriver-900455a0.uksouth.azurecontainerapps.io/mcp
```

**Response**:
```html
<!DOCTYPE html>
<html lang=en>
<head>
    <title>Azure Container Apps - Welcome</title>
```

**Expected** (if MCP server was running):
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32700,
    "message": "Parse error: Invalid JSON"
  }
}
```

---

### Container Logs

**Command**:
```bash
az containerapp logs show -g lab-master-lab -n mcp-weather-pavavy6pu5 \
  --type console --tail 50
```

**Result**:
```
{"Log": "12:35:11 Listening on :80..."}
```

**What's Missing**:
- No MCP server startup logs
- No "Initialized MCP server with tools: [...]"
- No "Loaded endpoints: weather, forecast, cities"

---

## Impact Assessment

### Cells Affected

| Cell Range | Description | Impact |
|------------|-------------|--------|
| **Cell 83** | `weather.get_cities("usa")` | ❌ MCP initialization timeout |
| **Cells 82-94** | Lab 10 MCP examples (13 cells) | ❌ All failing |
| **Cell 96** | Product catalog MCP | ❌ Failing |
| **Cell 98** | AutoGen with MCP | ❌ Failing |
| **Cell 105** | Workflow with MCP | ❌ Failing |
| **Cells 146-150** | MCP authorization tests (5 cells) | ❌ All failing |

**Total**: ~30 cells blocked by missing MCP servers

---

### What's Working vs. Not Working

| Component | Status | Reason |
|-----------|--------|--------|
| **Container Apps Deployed** | ✅ | Infrastructure provisioned |
| **Apps Show "Running"** | ✅ | Demo app starts successfully |
| **Health Checks Pass** | ✅ | Demo app responds on port 80 |
| **HTTP Responses** | ✅ | Demo app returns HTML |
| **MCP Protocol** | ❌ | MCP servers not deployed |
| **`/mcp` Endpoint** | ❌ | Returns HTML, not JSON-RPC |
| **Cell 83 Initialization** | ❌ | Timeout waiting for MCP |

---

## Failed Remediation Attempts

### Attempt #1: Port Fix (8080 → 80)
**What I Did**: Updated ingress targetPort from 8080 to 80
**Result**: ✅ Health checks now pass
**Impact**: Did NOT fix MCP issue (wrong app running)

### Attempt #2: Bicep Redeployment
**What I Did**: Re-ran `az deployment group create` with same template
**Result**: ❌ Failed - 6/7 apps failed to provision
**Reason**: Template still has wrong image, can't create new revision

---

## Options to Fix

### Option A: Find and Deploy Correct MCP Docker Images

**Requirements**:
1. Locate MCP server source code or pre-built images
2. Build Docker images for 7 MCP servers:
   - weather
   - oncall
   - github
   - spotify
   - product-catalog
   - place-order
   - ms-learn
3. Push images to ACR: `acrpavavy6pu5hpa.azurecr.io`
4. Update Container Apps to use new images

**Effort**: 2-4 hours (if source code available)

---

### Option B: Use Publicly Available MCP Servers

**Requirements**:
1. Find public Docker images for MCP servers
2. Update Bicep template with correct image references
3. Redeploy

**Effort**: 30 minutes - 2 hours (if public images exist)

---

### Option C: Disable MCP-Dependent Cells

**Requirements**:
1. Skip cells 82-94, 96, 98, 105, 146-150
2. Document as "known limitation"
3. Continue with remaining notebook fixes

**Effort**: 10 minutes
**Impact**: Lose ~30 cells of functionality

---

### Option D: Investigate Original Deployment Intent

**Requirements**:
1. Check if MCP servers exist elsewhere (different Azure subscription, Container Instances, etc.)
2. Review notebook history for MCP server URLs
3. Determine if MCP servers were external dependencies

**Effort**: 30 minutes - 1 hour

---

## Investigation Questions

### Where Are the MCP Servers?

**Checked**:
- ❌ Not in this repository
- ❌ Not in ACR (`acrpavavy6pu5hpa`)
- ❌ Not deployed to Container Apps (wrong image)

**Not Checked**:
- ❓ Different Azure subscription?
- ❓ Separate GitHub repository?
- ❓ Pre-built images in a public registry?
- ❓ Old Container Instances (deleted during resource group cleanup)?

---

### User Error Logs Show Old URLs

**From previous sessions**:
```
https://mcp-weather-pavavy6pu5.ambitiousfield-f6abdfb4.uksouth.azurecontainerapps.io
```

**Current deployment**:
```
https://mcp-weather-pavavy6pu5.niceriver-900455a0.uksouth.azurecontainerapps.io
```

**Different domains** = Different Container App Environments

**Question**: Were MCP servers working in the old deployment (`ambitiousfield`) before resource group deletion?

---

## Recommended Next Steps

### Immediate (5 minutes)

1. **Check if old MCP URLs still work**:
   ```bash
   curl https://mcp-weather-pavavy6pu5.ambitiousfield-f6abdfb4.uksouth.azurecontainerapps.io/mcp
   ```

2. **Search for MCP server images** in public registries:
   ```bash
   # Check Docker Hub
   docker search mcp-weather
   docker search azure-mcp
   ```

---

### Short-term (30 minutes)

3. **Review notebook archive** for clues:
   - Check `archive/` for old notebook versions
   - Look for comments about MCP server deployment
   - Search for Docker image references

4. **Check Azure for old Container Instances**:
   ```bash
   az container list --subscription d334f2cd-3efd-494e-9fd3-2470b1a13e4c \
     --query "[?contains(name, 'mcp')].{name:name, state:properties.instanceView.state}" \
     -o table
   ```

---

### Long-term (2-4 hours)

5. **If source code found**: Build and deploy correct images
6. **If no source code**: Implement minimal MCP servers for demo purposes
7. **If neither**: Disable MCP cells and document limitation

---

## What I've Done So Far

1. ✅ Identified wrong Docker image in Bicep template
2. ✅ Confirmed ACR is empty (no images built)
3. ✅ Verified Container Apps are running demo app, not MCP servers
4. ✅ Tested `/mcp` endpoint - returns HTML instead of JSON-RPC
5. ✅ Fixed port mismatch (8080 → 80) for health checks
6. ✅ Updated PHASE1 status documents
7. ✅ Created this comprehensive analysis

---

## What I Need from User

**Option Selection**: Which option should I pursue?
- **Option A**: Find and deploy correct MCP images (requires source code location)
- **Option B**: Find public MCP images (requires URL/registry info)
- **Option C**: Skip MCP cells and continue with remaining fixes
- **Option D**: Investigate old deployment (may reveal where MCP servers came from)

**Additional Information Needed**:
- Were MCP servers working before the resource group deletion?
- Is there a separate repository for MCP server code?
- Are MCP servers external dependencies (managed by someone else)?
- Should I check a different Azure subscription for existing MCP deployments?

---

## Current Status

### Phase 1: MCP Infrastructure
- [x] Resource group deployed
- [x] Container Apps created (7/7)
- [x] Health checks passing (7/7)
- [ ] **MCP servers deployed (0/7)** ← BLOCKED
- [ ] MCP protocol working (0/7) ← BLOCKED

### Overall Progress
**Before**: Thought Phase 1 was complete (7/7 apps HTTP 200)
**After Investigation**: Phase 1 is INCOMPLETE (wrong apps deployed)

**Cells Working**: 0/~30 MCP-dependent cells
**Blocking Issue**: No actual MCP server applications deployed

---

**Created**: 2025-11-15
**Priority**: 🔴 CRITICAL
**Next**: Await user guidance on which option to pursue
