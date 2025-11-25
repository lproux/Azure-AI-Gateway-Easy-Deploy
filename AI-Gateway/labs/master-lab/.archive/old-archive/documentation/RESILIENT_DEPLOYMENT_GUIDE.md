# Resilient AI Gateway Deployment Guide

## Overview

This guide documents the **resilient phased deployment approach** that successfully deploys the Master AI Gateway Lab infrastructure despite individual component failures.

---

## Problem Solved

**Original Issue**: Monolithic Bicep deployment failed completely if ANY resource had issues:
- Circular reference errors with duplicate model names
- Model availability errors (region-specific)
- SKU compatibility issues
- All-or-nothing deployment (one failure = total failure)

**Solution**: Phased Python deployment with per-resource error handling

---

## Deployment Architecture

### Phase 1: Core Infrastructure (Step 1) - BICEP ✅
**Status**: Completed successfully
**File**: `deploy-01-core.bicep`
**Resources**:
- ✓ Log Analytics Workspace
- ✓ Application Insights
- ✓ API Management (StandardV2)

**Time**: ~5 minutes

---

### Phase 2a: AI Foundry Hubs - PYTHON ✅
**Status**: Completed successfully
**Script**: `deploy_ai_foundry_resilient.py`
**Resources**:
- ✓ foundry1-pavavy6pu5hpa (UK South)
- ✓ foundry2-pavavy6pu5hpa (Sweden Central)
- ✓ foundry3-pavavy6pu5hpa (West Europe)

**Time**: ~3 minutes (hubs already existed)

---

### Phase 2b: AI Models - PYTHON ✅
**Status**: Completed successfully
**Script**: `deploy_ai_foundry_resilient.py` (same script, phase 2)
**Models Deployed**:

**Foundry 1 (UK South) - 4 models**:
- ✓ gpt-4o-mini
- ✓ gpt-4o
- ✓ text-embedding-3-small
- ✓ text-embedding-3-large

**Foundry 2 (Sweden Central) - 1 model**:
- ✓ gpt-4o-mini

**Foundry 3 (West Europe) - 1 model**:
- ✓ gpt-4o-mini

**Total**: 6 models across 3 regions

**Models Removed** (regional availability issues):
- ✗ gpt-4o-realtime-preview - Not available in UK South
- ✗ gpt-4.1 / gpt-4.1-mini - Not GA yet
- ✗ dall-e-3 - SKU 'Standard' not supported in UK South
- ✗ DeepSeek-R1 - Not available via Azure
- ✗ Phi-4 - Limited availability
- ✗ FLUX-1.1-pro - Not available via Bicep

**Time**: ~15 minutes (2 new models deployed, 4 skipped as already existed)

**Key Feature**: Resilient error handling - continues deploying even if individual models fail

---

### Phase 2c: APIM Inference API - BICEP 🔄
**Status**: In progress
**File**: `deploy-02c-apim-api.bicep`
**Script**: `deploy_apim_api.py`
**Resources**:
- APIM Inference API configuration
- Backend pool with 3 AI Foundry hubs
- Priority-based load balancing:
  - Priority 1: UK South (weight: 100)
  - Priority 2: Sweden Central + West Europe (weight: 50 each)

**Time**: ~5 minutes (estimated)

---

### Phase 3: Supporting Services (Step 3) - BICEP ⏳
**Status**: Pending
**File**: `deploy-03-supporting.bicep`
**Resources**:
- Redis Enterprise (semantic caching)
- Cognitive Search
- Cosmos DB
- Content Safety

**Time**: ~10 minutes (estimated)

---

### Phase 4: MCP Servers (Step 4) - BICEP ⏳
**Status**: Pending
**File**: `deploy-04-mcp.bicep`
**Resources**:
- Container Registry
- Container Apps Environment
- 7 MCP Container Apps:
  - weather, oncall, github, spotify
  - product-catalog, place-order, ms-learn

**Time**: ~5 minutes (estimated)

---

## Key Scripts

### 1. `deploy_ai_foundry_resilient.py`
**Purpose**: Deploy AI Foundry hubs and models with resilience

**Features**:
- Checks if hubs exist before creating
- Deploys models one-by-one
- Continues on failure (doesn't stop entire deployment)
- Detailed success/failure reporting
- Saves results to `deployment-results.json`

**Usage**:
```bash
python deploy_ai_foundry_resilient.py
```

**Output Example**:
```
======================================================================
PHASE 1: CHECK/CREATE AI FOUNDRY HUBS
======================================================================
[*] Checking: foundry1-pavavy6pu5hpa
    [OK] Already exists (State: Succeeded)

======================================================================
PHASE 2: DEPLOY MODELS (RESILIENT)
======================================================================
[*] Foundry: foundry1-pavavy6pu5hpa (4 models)
  [*] Deploying: gpt-4o-mini...
      [OK] Already deployed (skipping)
  [*] Deploying: text-embedding-3-small...
      [OK] Deployed successfully

======================================================================
DEPLOYMENT SUMMARY
======================================================================
[OK] Succeeded: 2 models
  + foundry1-pavavy6pu5hpa/text-embedding-3-small
  + foundry1-pavavy6pu5hpa/text-embedding-3-large

[*] Skipped: 4 models (already deployed)
  o foundry1-pavavy6pu5hpa/gpt-4o-mini
  o foundry1-pavavy6pu5hpa/gpt-4o
  o foundry2-pavavy6pu5hpa/gpt-4o-mini
  o foundry3-pavavy6pu5hpa/gpt-4o-mini
```

---

### 2. `deploy_apim_api.py`
**Purpose**: Configure APIM Inference API for AI Foundry backend pool

**Features**:
- Loads Step 1 outputs from `step1-outputs.json`
- Compiles Bicep to JSON
- Deploys APIM API configuration
- Configures backend pool with 3 hubs
- Saves outputs to `step2c-outputs.json`

**Usage**:
```bash
python extract_step1_outputs.py  # First time only
python deploy_apim_api.py
```

---

### 3. `extract_step1_outputs.py`
**Purpose**: Extract outputs from Step 1 deployment for use in later steps

**Outputs Extracted**:
- apimLoggerId
- appInsightsId
- appInsightsInstrumentationKey
- apimGatewayUrl
- apimPrincipalId
- etc.

---

## Benefits of Resilient Approach

### 1. **Failure Isolation**
- One model failure doesn't stop entire deployment
- Can manually fix failing resources and re-run
- Continue where you left off

### 2. **Better Debugging**
- Clear per-resource error messages
- Know exactly which resource failed and why
- Easy to identify regional availability issues

### 3. **Idempotency**
- Safe to re-run scripts multiple times
- Skips already-deployed resources
- Only deploys what's missing

### 4. **Progress Visibility**
- Real-time progress updates
- Detailed success/failure reporting
- Saved results for audit trail

### 5. **Flexibility**
- Easy to add/remove models
- Can adjust regional configuration
- Simple to customize per environment

---

## Next Steps

1. **Wait for Phase 2c** (APIM API) to complete (~5 minutes)
2. **Deploy Phase 3** (Supporting Services) via Bicep
3. **Deploy Phase 4** (MCP Servers) via Bicep
4. **Generate master-lab.env** with all deployment outputs
5. **Test all 31 labs** using the deployed infrastructure

---

## Files Created

### Python Scripts
- `deploy_ai_foundry_resilient.py` - Resilient AI Foundry deployment
- `deploy_apim_api.py` - APIM API configuration
- `extract_step1_outputs.py` - Extract deployment outputs

### Bicep Files
- `deploy-01-core.bicep` - Core infrastructure (already deployed)
- `deploy-02c-apim-api.bicep` - APIM API configuration (deploying)
- `deploy-03-supporting.bicep` - Supporting services (pending)
- `deploy-04-mcp.bicep` - MCP servers (pending)

### Configuration Files
- `step1-outputs.json` - Step 1 deployment outputs
- `deployment-results.json` - AI Foundry deployment results
- `step2c-outputs.json` - APIM API outputs (pending)

### Documentation
- `RESILIENT_DEPLOYMENT_GUIDE.md` - This guide
- `CREATIVE_SOLUTIONS.md` - Alternative approaches
- `FIX_PERMISSIONS_ERROR.md` - Service Principal permission fix
- `MODULAR_DEPLOYMENT_GUIDE.md` - Original modular approach

---

## Troubleshooting

### Model Deployment Fails
**Error**: `DeploymentModelNotSupported`
**Solution**: Remove model from configuration or try different region

### Permission Errors
**Error**: `Authorization failed for roleAssignments`
**Solution**: Grant User Access Administrator role to Service Principal
**See**: `FIX_PERMISSIONS_ERROR.md`

### Bicep Compilation Errors
**Error**: `BCP104: The referenced module has errors`
**Solution**: Check module paths and syntax in Bicep files

### Azure CLI Cache Issues
**Error**: `Can't get attribute 'NormalizedResponse'`
**Solution**: Use Service Principal authentication instead of Azure CLI
**See**: Cell 11 in `master-ai-gateway.ipynb`

---

## Summary

✅ **Core Infrastructure**: Deployed (Step 1)
✅ **AI Foundry Hubs**: Deployed (Step 2a)
✅ **AI Models**: Deployed (Step 2b) - 6 models across 3 regions
🔄 **APIM API**: Deploying (Step 2c)
⏳ **Supporting Services**: Pending (Step 3)
⏳ **MCP Servers**: Pending (Step 4)

**Total time so far**: ~20 minutes
**Estimated remaining**: ~15 minutes
**Total estimated**: ~35 minutes

This resilient approach successfully bypasses the issues that caused the original monolithic deployment to fail completely.
