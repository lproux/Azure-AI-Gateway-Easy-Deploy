# COMPREHENSIVE ERROR ANALYSIS & RESOLUTION PLANS
## Notebook: master-ai-gateway-fix-MCP.ipynb
**Date:** 2025-11-11  
**Total Cells:** 230 (115 Markdown, 115 Code)

================================================================================
## ERROR CATEGORIZATION
================================================================================

### CATEGORY 1: DEPLOYMENT ISSUES
**Priority:** HIGH  
**Cells Affected:** 22, 30-31, 32

| Cell | Issue | Type |
|------|-------|------|
| 22 | API_ID not properly configured | Configuration |
| 30 | Missing model deployments (dall-e-3, FLUX, etc.) | Incomplete Deployment |
| 31 | Model metadata not recorded in master-lab.env | Missing Variables |
| 32 | master-lab.env missing model endpoints, keys, regions | Incomplete Configuration |

**Specific Missing Deployments:**
- dall-e-3
- FLUX.1-Kontext-pro  
- FLUX-1.1-pro
- model-router
- gpt-image-1
- gpt-image-1-mini
- gpt-4o-mini (regions 2 & 3 for load balancing)

**Missing Variables in master-lab.env:**
- Model endpoints (per region)
- Model keys (per region)
- Model names (all models)
- Model regions (deployment mapping)
- API_ID for APIM

---

### CATEGORY 2: POLICY APPLICATION ERRORS
**Priority:** HIGH  
**Cells Affected:** 38, 45, 55, 64

| Cell | Policy | Error | Error Code |
|------|--------|-------|------------|
| 38 | Token Metrics | ValidationError: Entity with specified identifier not found | Bad Request 400 |
| 45 | Load Balancing | ValidationError: Error parsing EntityName | Bad Request 400 |
| 55 | Token Rate Limiting | ValidationError: Entity not found + spacing issues | Bad Request 400 |
| 64 | Private Connectivity | ValidationError: Error parsing EntityName + spacing issues | Bad Request 400 |

**Root Causes:**
1. API_ID not properly set (from Cell 22 issue)
2. XML parsing errors in policy definitions
3. Missing or incorrect APIM API identifier
4. Code formatting issues (extra spaces)

---

### CATEGORY 3: LOAD BALANCING CONFIGURATION
**Priority:** MEDIUM  
**Cells Affected:** 47, 48

| Cell | Issue | Impact |
|------|-------|--------|
| 47 | Region unknown for load balancing | Cannot distribute across regions |
| 48 | Load balancing not configured for multi-region | Ineffective distribution |

**Requirements:**
- Load balance across 3 regions (foundry1, foundry2, foundry3)
- Use different project hubs deployed in different regions
- Track and display region distribution
- Configure backend pools with all regional endpoints

---

### CATEGORY 4: MCP SERVER CONNECTION
**Priority:** MEDIUM (Code fixed, servers down)  
**Cells Affected:** 71+

| Server | Status | Issue |
|--------|--------|-------|
| GitHub MCP | Timeout | Container App not responding |
| OnCall MCP | Timeout | Container App not responding |
| Spotify MCP | Timeout | Container App not responding |
| Weather MCP | Timeout | Container App not responding |
| Product Catalog MCP | Timeout | Container App not responding |
| Docs MCP | ✅ Working | Container Instance OK |
| Excel MCP | File Path | Container Instance OK |

**Status:** Code is 100% correct. Infrastructure issue - Container Apps need to be restarted.

---

### CATEGORY 5: CODE FORMATTING
**Priority:** LOW  
**Cells Affected:** 55, 64

**Issues:**
- Unnecessary spaces in code
- Inconsistent indentation
- Needs cleanup for readability

================================================================================
## RESOLUTION PLANS
================================================================================

## 📋 PLAN 1: DEPLOYMENT ISSUES
**Status:** PENDING  
**Priority:** HIGH  
**Estimated Time:** 30 minutes

### Problem Summary
- API_ID not configured in Cell 22
- Missing 9 model deployments in Cell 30
- master-lab.env missing critical model metadata in Cell 32

### Sub-Plans

#### PLAN 1.1: Fix API_ID Configuration (Cell 22)
**Steps:**
1. Check reference notebook for working API_ID initialization
2. Add code to Cell 22 to load API_ID from deployment outputs
3. Store API_ID as environment variable
4. Verify API_ID is available for policy cells

**Expected Output:**
```
[OK] API_ID configured: azure-openai-api
```

#### PLAN 1.2: Deploy Additional Models (Cell 30)
**Steps:**
1. Review current deployment code in Cell 30
2. Add model specifications for:
   - dall-e-3 (image generation)
   - FLUX.1-Kontext-pro, FLUX-1.1-pro (advanced image)
   - model-router (routing)
   - gpt-image-1, gpt-image-1-mini (GPT image)
3. Deploy gpt-4o-mini to foundry2 and foundry3 (load balancing)
4. Capture deployment outputs (endpoints, keys, regions)
5. Store in variables for Cell 32

**Expected Output:**
```
[*] Phase 2b: AI Models (Resilient)
  [*] foundry1-pavavy6pu5hpa: 10 models
    [OK] gpt-4o-mini already deployed
    [OK] gpt-4o already deployed
    [OK] text-embedding-3-small already deployed
    [OK] text-embedding-3-large already deployed
    [NEW] dall-e-3 deployed
    [NEW] FLUX.1-Kontext-pro deployed
    [NEW] FLUX-1.1-pro deployed
    [NEW] model-router deployed
    [NEW] gpt-image-1 deployed
    [NEW] gpt-image-1-mini deployed
  [*] foundry2-pavavy6pu5hpa: 1 models
    [OK] gpt-4o-mini already deployed
  [*] foundry3-pavavy6pu5hpa: 1 models
    [OK] gpt-4o-mini already deployed

[OK] Models: 6 deployed, 6 skipped, 0 failed
```

#### PLAN 1.3: Update master-lab.env Generation (Cell 32)
**Steps:**
1. Add model endpoint variables for each deployment
2. Add model key variables for each region
3. Add model name mappings
4. Add region mappings for load balancing
5. Add API_ID variable

**Expected Variables Added:**
```bash
# API Management
APIM_API_ID=azure-openai-api

# Model Deployments - Region 1 (uksouth)
MODEL_GPT4O_ENDPOINT_R1=https://foundry1-pavavy6pu5hpa-aiservices.openai.azure.com
MODEL_GPT4O_KEY_R1=<key>
MODEL_GPT4O_MINI_ENDPOINT_R1=https://foundry1-pavavy6pu5hpa-aiservices.openai.azure.com
MODEL_GPT4O_MINI_KEY_R1=<key>
MODEL_DALLE3_ENDPOINT_R1=https://foundry1-pavavy6pu5hpa-aiservices.openai.azure.com
MODEL_DALLE3_KEY_R1=<key>
# ... (all models)

# Model Deployments - Region 2 (eastus)
MODEL_GPT4O_MINI_ENDPOINT_R2=https://foundry2-pavavy6pu5hpa-aiservices.openai.azure.com
MODEL_GPT4O_MINI_KEY_R2=<key>

# Model Deployments - Region 3 (westus)
MODEL_GPT4O_MINI_ENDPOINT_R3=https://foundry3-pavavy6pu5hpa-aiservices.openai.azure.com
MODEL_GPT4O_MINI_KEY_R3=<key>

# Load Balancing Configuration
LB_REGIONS=uksouth,eastus,westus
LB_GPT4O_MINI_ENDPOINTS=<r1>,<r2>,<r3>
```

**Acceptance Criteria:**
- ✅ All 9 models deployed across regions
- ✅ master-lab.env contains all model metadata
- ✅ API_ID properly configured
- ✅ No deployment errors

---

## 📋 PLAN 2: POLICY APPLICATION ERRORS
**Status:** PENDING (Blocked by PLAN 1)  
**Priority:** HIGH  
**Estimated Time:** 20 minutes

### Problem Summary
All 4 policy cells failing with ValidationError due to:
1. API_ID not found
2. XML parsing errors
3. Code formatting issues

### Dependencies
- ✅ PLAN 1 must be completed first (provides API_ID)

### Sub-Plans

#### PLAN 2.1: Fix Token Metrics Policy (Cell 38)
**Steps:**
1. Verify API_ID is loaded from environment
2. Check XML policy format against working reference
3. Fix any XML syntax errors
4. Test policy application

**Expected Output:**
```
[*] Applying token metrics policy to APIM...
[policy] Subscription ID: d334f2cd-3efd-494e-9fd3-2470b1a13e4c
[policy] Using API ID: azure-openai-api
[policy] Applying token-metrics via REST API...
[OK] token-metrics applied successfully
```

#### PLAN 2.2: Fix Load Balancing Policy (Cell 45)
**Steps:**
1. Fix XML parsing error at Line 8, position 151
2. Verify backend pool configuration
3. Update with regional endpoints from PLAN 1
4. Test policy application

#### PLAN 2.3: Fix Token Rate Limiting Policy (Cell 55)
**Steps:**
1. Remove extra spaces in code
2. Fix API_ID reference
3. Verify XML policy format
4. Test policy application

#### PLAN 2.4: Fix Private Connectivity Policy (Cell 64)
**Steps:**
1. Remove extra spaces in code
2. Fix XML parsing error at Line 23, position 151
3. Verify API_ID reference
4. Test policy application

**Acceptance Criteria:**
- ✅ All 4 policies apply without errors
- ✅ No ValidationError messages
- ✅ Code properly formatted
- ✅ Policies visible in Azure Portal

---

## 📋 PLAN 3: LOAD BALANCING CONFIGURATION
**Status:** PENDING (Blocked by PLAN 1 & 2)  
**Priority:** MEDIUM  
**Estimated Time:** 15 minutes

### Problem Summary
Load balancing not configured with multi-region endpoints

### Dependencies
- ✅ PLAN 1 completed (provides regional endpoints)
- ✅ PLAN 2 completed (fixes policy application)

### Sub-Plans

#### PLAN 3.1: Configure Regional Backend Pool (Cell 45)
**Steps:**
1. Add all 3 regional endpoints to backend pool
2. Configure retry logic across regions
3. Set up round-robin distribution

#### PLAN 3.2: Update Load Balancing Test (Cell 47)
**Steps:**
1. Update test to use all 3 regions
2. Track which region responds to each request
3. Display region distribution

#### PLAN 3.3: Visualize Multi-Region Distribution (Cell 48)
**Steps:**
1. Update visualization to show 3 regions
2. Add region labels to response time chart
3. Show percentage distribution across regions

**Expected Output:**
```
Load Balancing Test Results:
  Region 1 (uksouth): 34 requests (34%)
  Region 2 (eastus): 33 requests (33%)
  Region 3 (westus): 33 requests (33%)
  
  Total Requests: 100
  Average Response Time: 0.45s
```

**Acceptance Criteria:**
- ✅ All 3 regions receive requests
- ✅ Distribution is roughly equal
- ✅ Region tracking works correctly
- ✅ Visualization shows all regions

---

## 📋 PLAN 4: MCP SERVER CONNECTIONS
**Status:** PENDING (Infrastructure, not code)  
**Priority:** LOW  
**Estimated Time:** 5 minutes (just verify)

### Problem Summary
Container Apps MCP servers not responding (code is correct)

### Action Required
**USER ACTION:** Restart Container Apps in Azure Portal

### Verification Steps
1. Confirm Container Apps are running
2. Re-test Cell 71+ MCP cells
3. Verify successful connections

**Acceptance Criteria:**
- ✅ All MCP servers respond
- ✅ No timeout errors
- ✅ Successful API calls to GitHub, OnCall, Spotify, Weather, Product Catalog

---

## 📋 PLAN 5: CODE FORMATTING & CLEANUP
**Status:** PENDING  
**Priority:** LOW  
**Estimated Time:** 10 minutes

### Problem Summary
Extra spaces and formatting issues in cells 55, 64

### Steps
1. Remove unnecessary spaces
2. Fix indentation
3. Ensure consistent formatting

**Acceptance Criteria:**
- ✅ Clean, readable code
- ✅ No extra spaces
- ✅ Consistent indentation

---

## 📋 PLAN 6: CELL RENUMBERING & REORDERING
**Status:** PENDING (Final step)  
**Priority:** LOW  
**Estimated Time:** 15 minutes

### Problem Summary
Cells not in logical order (deploy → env → initialize → labs)

### Proposed Structure
1. **Section 0: Setup & Imports** (Cells 1-22)
2. **Section 1: Deployment** (Cells 23-30)
3. **Section 2: Environment Generation** (Cells 31-32)
4. **Section 3: Environment Loading & Initialization** (Cell 33+)
5. **Section 4: Labs** (Remaining cells)

### Steps
1. Analyze current cell order
2. Create reordering map
3. Preserve all markdown cells
4. Apply reordering
5. Update cell references in markdown

**Acceptance Criteria:**
- ✅ Logical flow: deploy → configure → initialize → labs
- ✅ All markdown cells preserved
- ✅ No broken references
- ✅ Clear section organization

================================================================================
## EXECUTION STRATEGY
================================================================================

### Phase 1: Analysis & Planning ✅ COMPLETE
- Error categorization ✅
- Plan creation ✅
- Reference notebook review (pending)

### Phase 2: Sequential Plan Execution (PENDING)
**Order of Execution:**
1. PLAN 1: Deployment (blocks PLAN 2, 3)
2. PLAN 2: Policies (blocks PLAN 3)
3. PLAN 3: Load Balancing
4. PLAN 4: MCP Verification (user action)
5. PLAN 5: Code Formatting
6. PLAN 6: Cell Reordering

### Phase 3: Validation (PENDING)
- Run full notebook
- Compare outputs to expected
- Document any remaining issues

================================================================================
## CURRENT STATUS
================================================================================

**Active Plan:** PLAN 1 (Deployment Issues)  
**Status:** Ready to begin  
**Next Action:** Present PLAN 1 details for user approval

================================================================================
