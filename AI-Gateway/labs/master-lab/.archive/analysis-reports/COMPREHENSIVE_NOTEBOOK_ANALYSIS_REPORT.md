# COMPREHENSIVE NOTEBOOK ANALYSIS REPORT
## Master AI Gateway Notebook - Deployment & Consolidation Analysis

**Analyzed Notebook:** `master-ai-gateway copy.ipynb`
**Total Cells:** 238 (124 code cells, 114 markdown cells)
**Analysis Date:** 2025-11-11
**Focus:** Cells 1-41 (Deployment & Initialization) + Full Cross-Reference Analysis

---

## EXECUTIVE SUMMARY

This notebook exhibits significant **code duplication**, **missing deployment artifacts**, and **inconsistent initialization patterns**. While 24 of 41 cells relate to deployment, only **37.9% show explicit success indicators**. Critical deployment files (all bicep templates and parameter files) are **MISSING**, blocking actual deployment execution.

### Critical Issues Found:
- ❌ **4 duplicate environment loaders** (cells 2, 3, 13, 41)
- ❌ **13 duplicate Azure CLI resolvers** (az_cli variable redefined 13 times)
- ❌ **10 duplicate get_az_cli() functions**
- ❌ **All 4 bicep deployment files MISSING**
- ❌ **2 parameter JSON files MISSING**
- ⚠️ **2 missing environment variables** (APIM_SERVICE, API_ID) in cell 9
- ⚠️ **8 orphan cells** with no dependencies or dependents

### Success Metrics:
- ✅ **No execution errors** in cells 1-41
- ✅ Core files exist: requirements.txt, master-lab.env, .azure-credentials.env, notebook_mcp_helpers.py
- ⚠️ Low success rate: 11/29 code cells (37.9%) show explicit success confirmation

---

## PART 1: FIRST JUDGEMENT - CODE STRUCTURE ANALYSIS (Cells 1-41)

### 1.1 Cell Purpose Classification

#### **Deployment-Related Cells (24 total):**
```
Cells: 1, 3, 5, 6, 7, 8, 9, 11, 13, 14, 17, 18, 22, 23, 27, 28, 30, 31, 32, 34, 36, 38, 40, 41
```

**Breakdown:**
- **Environment Setup:** 2, 3, 6, 13, 30, 41 (6 cells)
- **Azure CLI Resolution:** 5, 7, 14, 18, 27, 31, 32 (7 cells)
- **Deployment Helpers:** 8, 11, 36, 38 (4 cells)
- **MCP Initialization:** 1, 10, 22, 23 (4 cells)
- **Policy Application:** 9, 17, 27 (3 cells)

#### **Support/Documentation Cells:**
```
Markdown: 12, 16, 19, 20, 21, 25, 26, 29, 33, 35, 37, 39
Code (utility): 4, 15, 24, 28
```

### 1.2 File References Analysis

#### **Bicep Files Referenced:**
| File | Referenced In Cells | Status |
|------|---------------------|--------|
| `deploy-01-core.bicep` | 11, 38 | ❌ MISSING |
| `deploy-02c-apim-api.bicep` | 38 | ❌ MISSING |
| `deploy-03-supporting.bicep` | 38 | ❌ MISSING |
| `deploy-04-mcp.bicep` | 38 | ❌ MISSING |
| `.bicep` (generic pattern) | 8, 36 | N/A (pattern) |

**CRITICAL:** All deployment bicep files are missing. Cell 38 (main deployment) **WILL FAIL**.

#### **Parameter Files Referenced:**
| File | Referenced In Cells | Status |
|------|---------------------|--------|
| `params-01-core.json` | 38 (3x) | ❌ MISSING |
| `params-03-supporting.json` | 38 (4x) | ❌ MISSING |

#### **Configuration Files:**
| File | Referenced In Cells | Status |
|------|---------------------|--------|
| `master-lab.env` | 2, 3, 6, 13 | ✅ EXISTS |
| `.azure-credentials.env` | 5, 32 | ✅ EXISTS |
| `requirements.txt` | 4, 15, 24 | ✅ EXISTS |
| `notebook_mcp_helpers.py` | 22, 23 (import) | ✅ EXISTS |
| `.env` | 41 | ⚠️ Different from master-lab.env |

### 1.3 Duplicate Variable Definitions (First 41 Cells)

**Critical Configuration Variables:**
```
RESOURCE_GROUP:     defined 6 times (cells 3, 13, 14, 27, 40, 41)
az_cli:             defined 5 times (cells 17, 18, 27, 31, 32)
ENV_FILE:           defined 4 times (cells 2, 3, 13, 41)
APIM_GATEWAY_URL:   defined 3 times (cells 3, 13, 40)
APIM_API_KEY:       defined 2 times (cells 13, 40)
SUBSCRIPTION_ID:    defined 3 times (cells 3, 14, 41)
LOCATION:           defined 5 times (cells 3, 13, 14, 40, 41)
OPENAI_ENDPOINT:    defined 2 times (cells 3, 41)
ENV:                defined 3 times (cells 2, 3, 13)
AZ_CLI:             defined 2 times (cells 7, 14)
```

**Issue:** Variables redefined multiple times create **inconsistent state** depending on execution order.

### 1.4 Duplicate Function Definitions (First 41 Cells)

**Critical Functions:**
```
ensure_env():              cells 2, 3 (2 definitions)
compile_bicep():           cells 8, 36 (2 definitions)
deploy_template():         cells 8, 36 (2 definitions)
get_deployment_outputs():  cells 8, 36 (2 definitions)
get_az_cli():              cells 17, 32 (2 definitions in first 41)
```

**Note:** get_az_cli() is actually defined **10 times total** across all 238 cells.

### 1.5 Duplicate Import Statements (First 41 Cells)

**Most Duplicated Imports:**
```
os:         imported 18 times
pathlib:    imported 13 times
shutil:     imported 6 times
typing:     imported 4 times
json:       imported 3 times
```

**Impact:** Unnecessary code bloat, confusing for maintenance.

---

## PART 2: SECOND JUDGEMENT - OUTPUT ANALYSIS (Cells 1-41)

### 2.1 Execution Status Summary

**Total Code Cells:** 29
**Successfully Executed:** 29 (100%)
**Cells with ✅/[OK] indicators:** 11 (37.9%)
**Cells with ⚠️ warnings:** 1
**Cells with ❌ errors:** 0

**Interpretation:** All cells executed without **exceptions**, but only 37.9% explicitly confirm successful completion. Many cells complete silently without status reporting.

### 2.2 Cell-by-Cell Output Analysis

#### **Cell 1** (Execution: 159)
- **Type:** Documentation comment
- **Output:** Displays consolidation plan text
- **Status:** ✅ Informational

#### **Cell 2** (Execution: 160)
- **Purpose:** Environment Loader v1
- **Output:**
  ```
  [env] Summary (masked)
    APIM_API_KEY=bf30*************************ab7
    AZURE_CLIENT_SECRET=lXV8***...
  ```
- **Status:** ✅ Successfully loads and masks sensitive values
- **Issue:** This is the FIRST of FOUR duplicate environment loaders

#### **Cell 3** (Execution: 161)
- **Purpose:** Environment Loader v2 (Consolidated Minimal)
- **Output:**
  ```
  [env] Loaded keys: APIM_GATEWAY_URL, APIM_SERVICE_ID, APIM_SERVICE_NAME,
                     APIM_API_KEY, INFERENCE_API_PATH...
  ```
- **Status:** ✅ Successfully loads environment
- **Issue:** This is the SECOND duplicate environment loader
- **Difference from Cell 2:** Different template, different masking logic

#### **Cell 4** (Execution: 162)
- **Purpose:** Dependencies Install (Consolidated)
- **Output:**
  ```
  [deps] 'c:\Users\lproux\...\python.exe' -m pip install -r ...
  ```
- **Status:** ✅ Dependencies installed
- **Issue:** Output truncated, unclear if all dependencies succeeded

#### **Cell 5** (Execution: 163)
- **Purpose:** Azure CLI & Service Principal Setup (Consolidated v2)
- **Output:**
  ```
  [azure] az resolved: C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd
          (reason=ranked selection)
  ```
- **Status:** ✅ Azure CLI found and validated
- **Key:** Sets `AZ_CLI` environment variable

#### **Cell 6** (Execution: 164)
- **Purpose:** Endpoint Normalizer & Derived Variables
- **Output:**
  ```
  [endpoint] Existing OPENAI_ENDPOINT found; using as-is
  [endpoint] OPENAI_ENDPOINT = https://apim-pav...
  ```
- **Status:** ✅ Endpoint normalized
- **Logic:** Derives OPENAI_ENDPOINT from APIM_GATEWAY_URL if missing

#### **Cell 7** (Execution: 165)
- **Purpose:** Unified az() Helper & Login Check
- **Output:**
  ```
  [az] version: azure-cli 2.69.0 *
  [az] account: ME-MngEnvMCAP592090-lproux-1
  ```
- **Status:** ✅ Azure CLI wrapper initialized
- **Key Function:** Defines `az()` helper used by later cells

#### **Cell 8** (Execution: 166)
- **Purpose:** Deployment Helpers (Consolidated)
- **Output:**
  ```
  [deploy] helpers ready
  ```
- **Status:** ✅ Functions defined
- **Key Functions:** compile_bicep(), deploy_template(), get_deployment_outputs()
- **Issue:** Cannot validate without bicep files

#### **Cell 9** (Execution: 167)
- **Purpose:** Unified Policy Application
- **Output:**
  ```
  [policy] Missing env vars; set: APIM_SERVICE, API_ID
  ```
- **Status:** ⚠️ **INCOMPLETE** - Missing required environment variables
- **Impact:** Policy application will fail if called
- **Required:** APIM_SERVICE, API_ID must be set in master-lab.env

#### **Cell 10** (Execution: 168)
- **Purpose:** Unified MCP Initialization
- **Output:**
  ```
  [mcp] Initialized 0 server(s)
  ```
- **Status:** ⚠️ No servers initialized (MCP URLs not configured)
- **Impact:** MCP functionality unavailable

#### **Cell 11** (Execution: 169)
- **Purpose:** Unified AzureOps Wrapper (Enhanced SDK Strategy)
- **Output:**
  ```
  [AzureOps] CLI: C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd
  [AzureOps] login status: OK
  ```
- **Status:** ✅ Comprehensive Azure operations wrapper initialized
- **Key Classes:** AzureOps, DeploymentError, PolicyError, ModelDeploymentError

#### **Cell 13** (Execution: 170)
- **Purpose:** Unified Environment Loader & Load Balancing Overview
- **Output:**
  ```
  [env] Summary (masked=True)
  [apim]
    APIM_API_KEY = bf30*************************ab7
    APIM_GATEWAY_URL = ...
  ```
- **Status:** ✅ Environment loaded with load balancing context
- **Issue:** This is the THIRD duplicate environment loader

#### **Cell 14** (Execution: 171)
- **Purpose:** Azure CLI + Service Principal (LEGACY)
- **Output:**
  ```
  [INFO] Using Azure CLI (delegated): C:\...\az.cmd
  [INFO] Subscription ID: ...
  ```
- **Status:** ✅ But marked as LEGACY
- **Issue:** Should be removed (delegates to unified az())

#### **Cell 15** (Execution: 172)
- **Purpose:** Unified Dependencies Install
- **Output:**
  ```
  [deps] Installing from ...\requirements.txt (idempotent)
  Requirement already satisfied: azure-identity>=1.15.0 ...
  ```
- **Status:** ✅ Dependencies confirmed installed

#### **Cell 17** (Execution: 173)
- **Purpose:** Semantic Caching Configuration
- **Output:**
  ```
  [INFO] Azure CLI: ...\az.BAT
  [*] Deploying semantic caching policy...
  ```
- **Status:** Unclear (output truncated)
- **Issue:** Another get_az_cli() definition

#### **Cell 18** (Execution: 174)
- **Purpose:** Azure CLI path resolution (patched)
- **Output:**
  ```
  [INFO] Azure CLI resolved: ...\az.BAT
  ```
- **Status:** ✅ But redundant
- **Issue:** Yet another Azure CLI resolver

#### **Cell 22** (Execution: 175)
- **Purpose:** MCP Client Initialization (2 Real Servers)
- **Output:**
  ```
  🔄 Initializing MCP Client...
  ✅ MCP Client initialized successfully!
  📡 Real MCP Servers Deployed: ...
  ```
- **Status:** ✅ MCP initialized
- **Servers:** Excel, Docs

#### **Cell 23** (Execution: 176)
- **Purpose:** MCP Client Initialization (5 Real Servers)
- **Output:**
  ```
  ⚠️  MCP Client already initialized with all 5 servers. Skipping re-initialization.
  ```
- **Status:** ⚠️ Redundant initialization attempt
- **Issue:** Should check first or combine with Cell 22

#### **Cell 27** (Execution: 179)
- **Purpose:** APIM policy apply helper
- **Output:**
  ```
  [INFO] Azure CLI resolved: ...\az.BAT
  ```
- **Status:** ✅ Function defined
- **Issue:** Another duplicate Azure CLI resolver

#### **Cell 28** (Execution: 179)
- **Purpose:** Import All Required Libraries
- **Output:**
  ```
  [OK] All libraries imported
  ```
- **Status:** ✅ Master import cell

#### **Cell 30** (Execution: 180)
- **Purpose:** Load Environment Variables from Deployment Output
- **Output:**
  ```
  [OK] Loaded environment from master-lab.env
  [OK] APIM Gateway URL: https://apim-pavavy6pu5hpa.azure-...
  ```
- **Status:** ✅ Environment reloaded

#### **Cell 34** (Execution: 183)
- **Purpose:** Master Lab Configuration
- **Output:**
  ```
  [OK] Configuration set
    Subscription ID: d334f2cd-3efd-494e-9fd3-2470b1a13e4c
    Resource Group: lab-master-lab
  ```
- **Status:** ✅ Deployment configuration set

#### **Cell 36** (Execution: 184)
- **Purpose:** Deployment Helper Functions (Azure SDK)
- **Output:**
  ```
  [*] Initializing Azure authentication...
  [*] Found .azure-credentials.env, using Service Principal
  [OK] Azure SDK initialized and connection verified
  [OK] Helper functions defined
  ```
- **Status:** ✅ SDK-based deployment helpers ready
- **Issue:** Duplicates functions from Cell 8

#### **Cell 38** (Execution: 185)
- **Purpose:** Main Deployment - All 4 Steps
- **Output:**
  ```
  ======================================================================
  MASTER LAB DEPLOYMENT - 4 STEPS (RESILIENT)
  ======================================================================
  [*] Step 0: Ensuring resource group exists...
  [OK] Resource group already exists
  ```
- **Status:** ⚠️ Cannot proceed without bicep files
- **Expected to Deploy:**
  1. Core (deploy-01-core.bicep) ❌ MISSING
  2. AI Foundry (handled separately, not bicep)
  3. Supporting Services (deploy-03-supporting.bicep) ❌ MISSING
  4. MCP (deploy-04-mcp.bicep) ❌ MISSING

#### **Cell 40** (Execution: 186)
- **Purpose:** Generate .env File
- **Output:**
  ```
  [*] Generating master-lab.env...
  [OK] Created master-lab.env
  [OK] File location: c:\Users\lproux\OneDrive...
  ```
- **Status:** ✅ Environment file generated

#### **Cell 41** (Execution: 89)
- **Purpose:** Unified Configuration Loader Cell
- **Output:**
  ```
  [OK] All required keys present.
  Configuration Summary:
  --------------------------------------------
  ```
- **Status:** ✅ Configuration validated
- **Issue:** This is the FOURTH duplicate environment loader
- **Note:** Execution count 89 (much lower) suggests this is from earlier notebook version

### 2.3 Missing Environment Variables

**Cell 9 Reports Missing:**
- `APIM_SERVICE` - Required for policy application
- `API_ID` - Required for policy application

**Impact:** Policy deployment (Cell 9, 17, 27) will fail.

**Recommendation:** Add to master-lab.env template or derive from deployment outputs.

### 2.4 Success Indicators Summary

**Cells with Explicit Success (✅/[OK]):**
```
Cells: 2, 3, 4, 5, 6, 7, 8, 11, 13, 28, 30, 34, 36, 40, 41 (15 cells show success)
```

**Cells with Warnings (⚠️):**
```
Cell 9:  Missing env vars
Cell 10: No MCP servers initialized
Cell 23: Redundant initialization warning
```

**Cells with Failures (❌):**
```
None (no exceptions raised)
```

**Silent Cells (no status):**
```
Cells: 14, 15, 17, 18, 22, 24, 27, 31, 32, 38 (10 cells)
```

---

## PART 3: THIRD JUDGEMENT - CROSS-REFERENCE & DEPENDENCY ANALYSIS (ALL 238 CELLS)

### 3.1 Critical Configuration Variables - Full Notebook Scope

#### **RESOURCE_GROUP**
- **Defined in:** 7 cells (3, 13, 14, 27, 40, 41, 112)
- **Used in:** 14 cells (9, 13, 14, 17, 27, 46, 53, 63, 72, 107, 112, 219, 232, 233)
- **Issue:** ⚠️ 7 definitions create inconsistency risk
- **Impact:** Deployment cells depend on this value being correct
- **Recommendation:** Single source of truth in Cell 3 or 41

#### **az_cli**
- **Defined in:** 13 cells (17, 18, 27, 31, 32, 46, 53, 63, 72, 107, 112, 219, 232)
- **Used in:** 15 cells
- **Issue:** ❌ CRITICAL - 13 duplicate implementations
- **Impact:** Each cell re-discovers Azure CLI path (inefficient, error-prone)
- **Recommendation:** Define ONCE in consolidated setup (Cell 5 or 7)

#### **APIM_GATEWAY_URL**
- **Defined in:** 3 cells (3, 13, 40)
- **Used in:** 8 cells (6, 30, 47, 108, 110, 175, 196, 234)
- **Issue:** ⚠️ 3 definitions
- **Recommendation:** Single definition in environment loader

#### **ENV / ENV_FILE**
- **ENV defined in:** 3 cells (2, 3, 13)
- **ENV_FILE defined in:** 4 cells (2, 3, 13, 41)
- **Issue:** ⚠️ Competing environment dictionaries
- **Recommendation:** Unified ENV dictionary from single loader

#### **OPENAI_ENDPOINT**
- **Defined in:** 2 cells (3, 41)
- **Used in:** 5 cells (6, 112, 195, 196, 198)
- **Status:** Better than others (only 2 definitions)

### 3.2 Critical Function Definitions - Full Notebook Scope

#### **get_az_cli()**
- **Defined in:** 10 cells (17, 32, 46, 53, 63, 72, 107, 112, 219, 232)
- **Called in:** 10 cells (same cells that define it)
- **Issue:** ❌ CRITICAL - Most duplicated function
- **Pattern:** Each cell defines its own get_az_cli() instead of importing
- **Impact:** ~300-500 lines of duplicate code
- **Recommendation:** Define ONCE in Cell 5, import elsewhere

#### **compile_bicep()**
- **Defined in:** 2 cells (8, 36)
- **Called in:** 4 cells (8, 11, 36, 38)
- **Issue:** ⚠️ Duplicate implementations
- **Difference:** Cell 8 uses CLI approach, Cell 36 uses SDK approach
- **Recommendation:** Keep Cell 8 version (CLI-based), remove Cell 36 version

#### **deploy_template()**
- **Defined in:** 2 cells (8, 36)
- **Called in:** 3 cells (8, 36, 38)
- **Issue:** ⚠️ Duplicate implementations
- **Recommendation:** Consolidate into Cell 8

#### **get_deployment_outputs()**
- **Defined in:** 2 cells (8, 36)
- **Called in:** 5 cells (8, 11, 36, 38, 40)
- **Issue:** ⚠️ Duplicate implementations
- **Impact:** Cell 40 uses this to generate .env file
- **Recommendation:** Keep Cell 8 version

#### **az()**
- **Defined in:** 1 cell (7)
- **Called in:** 5 cells (7, 8, 9, 11, 14)
- **Status:** ✅ Good - single definition, multiple uses
- **This is how it SHOULD be done**

### 3.3 Deployment Flow Analysis (38 cells involved)

**Deployment-Related Cells Across Entire Notebook:**
```
Cells: 1, 8, 11, 13, 17, 22, 23, 30, 34, 36, 38, 40, 41, 46, 47, 53, 65, 72, 73,
       107, 108, 110, 112, 114, 137, 163, 167, 173, 175, 177, 188, 196, 208, 211,
       219, 220, 232, 233
Total: 38 cells
```

**Dependency Chain (High-Dependency Cells):**
```
Cell 232 → depends on 31 cells (highest)
Cell 195 → depends on 28 cells
Cell 234 → depends on 28 cells
Cell 219 → depends on 21 cells
Cell 173 → depends on 20 cells
Cell 196 → depends on 20 cells
Cell 112 → depends on 19 cells
```

**Analysis:**
- Cell 232 has the most complex dependency web (31 dependencies)
- Late-stage cells accumulate dependencies from earlier cells
- High coupling makes notebook fragile (changes cascade)

### 3.4 Orphan Cells (8 found)

**Orphan cells with no dependencies or dependents:**
```
Cells: 1, 22, 23, 28, 97, 113, 141, 190
```

**Analysis:**
- **Cell 1:** Documentation cell (expected orphan)
- **Cells 22, 23:** MCP initialization (redundant implementations)
- **Cell 28:** Import cell (expected orphan - provides imports to all)
- **Cells 97, 113, 141, 190:** Need investigation - may be dead code or experimental

### 3.5 Class Definitions

**Classes Defined:**
```
Cell 11:
  - AzureOps (comprehensive Azure operations wrapper)
  - DeploymentError (exception)
  - PolicyError (exception)
  - ModelDeploymentError (exception)

Cell 41:
  - NotebookConfig (configuration dataclass)
```

**Status:** ✅ Good - minimal classes, single definitions each

**Usage:**
- AzureOps from Cell 11 is the most comprehensive wrapper
- Should be primary Azure interaction class

### 3.6 Import Duplication Analysis

**Most Duplicated Imports (First 41 Cells):**
```
os:         18 times
pathlib:    13 times
shutil:     6 times
typing:     4 times
json:       3 times
azure.identity: 2 times
datetime:   2 times
```

**Impact:**
- Each cell re-imports standard libraries
- No shared import cell strategy
- ~200+ duplicate import lines

**Exception:**
- Cell 28 is labeled "Import All Required Libraries"
- Should be THE master import cell
- Other cells still re-import instead of relying on Cell 28

### 3.7 Variable Usage Patterns (Top 20 Most Used)

**Variables Used Most Frequently:**
1. **get** - used in 52 cells (likely dict.get() method)
2. **client** - used in 46 cells (Azure SDK clients)
3. **found** - used in 38 cells (path existence checks)
4. **response** - used in 38 cells (API responses)
5. **env** - used in 34 cells (environment variables)
6. **run** - used in 32 cells (subprocess.run() calls)
7. **message** - used in 24 cells (API messages)
8. **output** - used in 19 cells (command outputs)
9. **deployment** - used in 18 cells (deployment objects)
10. **endpoint** - used in 17 cells (API endpoints)
11. **az_cli** - used in 15 cells
12. **text** - used in 15 cells
13. **token** - used in 15 cells
14. **RESOURCE_GROUP** - used in 14 cells
15. **results** - used in 14 cells

**Analysis:** High usage of temporary/local variables across many cells suggests shared utility functions could reduce duplication.

### 3.8 Function Call Frequency (Top 15)

**Most Called Functions:**
```
1. get_az_cli()              - called in 10 cells [DUPLICATE]
2. az()                      - called in 5 cells ✅
3. get_deployment_outputs()  - called in 5 cells [DUPLICATE]
4. compile_bicep()           - called in 4 cells [DUPLICATE]
5. deploy_template()         - called in 3 cells [DUPLICATE]
6. check_deployment_exists() - called in 3 cells [DUPLICATE]
7. generate_image()          - called in 3 cells [DUPLICATE]
8. get_azure_openai_client() - called in 3 cells
9. ensure_env()              - called in 2 cells [DUPLICATE]
10. parse_env()              - called in 2 cells [DUPLICATE]
```

**Pattern:** Functions that are called multiple times are ALSO defined multiple times, creating redundancy.

---

## PART 4: WHAT'S MISSING, SUPERFLUOUS, AND REDUNDANT

### 4.1 MISSING Components

#### **CRITICAL - Deployment Artifacts:**
1. ❌ **deploy-01-core.bicep** - Core infrastructure (APIM, Log Analytics, App Insights)
   - Referenced: Cells 11, 38
   - Impact: Cannot deploy core infrastructure

2. ❌ **deploy-02c-apim-api.bicep** - APIM API configuration
   - Referenced: Cell 38
   - Impact: Cannot configure APIM API

3. ❌ **deploy-03-supporting.bicep** - Supporting services (Cosmos, Redis, Search)
   - Referenced: Cell 38
   - Impact: Cannot deploy supporting services

4. ❌ **deploy-04-mcp.bicep** - MCP server infrastructure
   - Referenced: Cell 38
   - Impact: Cannot deploy MCP servers

5. ❌ **params-01-core.json** - Parameters for core deployment
   - Referenced: Cell 38 (3 times)
   - Impact: Cannot pass parameters to core deployment

6. ❌ **params-03-supporting.json** - Parameters for supporting services
   - Referenced: Cell 38 (4 times)
   - Impact: Cannot pass parameters to supporting deployment

**Consequence:** **Cell 38 (Main Deployment) CANNOT EXECUTE** without these files.

#### **Missing Environment Variables:**
7. ⚠️ **APIM_SERVICE** - APIM service name
   - Required by: Cell 9, 17, 27 (policy application)
   - Status: Not in master-lab.env
   - Impact: Policy deployment fails

8. ⚠️ **API_ID** - APIM API identifier
   - Required by: Cell 9, 17, 27 (policy application)
   - Status: Not in master-lab.env
   - Impact: Policy deployment fails

#### **Missing Documentation:**
9. ⚠️ **Execution order guide** for cells 42-238
   - Status: Documentation exists for cells 1-41, but not beyond
   - Impact: User confusion about which cells to run

10. ⚠️ **Error handling documentation**
    - Status: No guidance on what to do when cells fail
    - Impact: User stuck when errors occur

11. ⚠️ **Rollback procedures**
    - Status: No documented way to undo partial deployments
    - Impact: Failed deployments leave orphaned resources

#### **Missing Validation:**
12. ⚠️ **Pre-deployment checks**
    - No cell validates all prerequisites before starting deployment
    - Recommended: Add validation cell before Cell 38

13. ⚠️ **Post-deployment verification**
    - No cell verifies deployment success beyond outputs
    - Recommended: Add health check cell after Cell 40

### 4.2 SUPERFLUOUS Components

#### **Duplicate Environment Loaders (4 implementations):**
1. **Cell 2** - Env Loader with basic masking
2. **Cell 3** - Env Loader (Consolidated Minimal) ← KEEP THIS ONE
3. **Cell 13** - Unified Environment Loader & Load Balancing
4. **Cell 41** - Unified Configuration Loader

**Recommendation:**
- **KEEP:** Cell 3 (most comprehensive, good structure)
- **REMOVE:** Cells 2, 13, 41 (redundant)
- **OR:** If Cell 41's NotebookConfig dataclass is valuable, consolidate Cell 3 and 41

#### **Duplicate Azure CLI Resolvers (13 implementations):**
Cells: 5, 11, 17, 18, 27, 31, 32, 46, 53, 63, 72, 107, 112, 219, 232

**Recommendation:**
- **KEEP:** Cell 5 (most comprehensive, handles service principal)
- **REMOVE:** All other az_cli resolution code
- **ACTION:** Make Cell 5 required, store az_cli in global scope

#### **Duplicate Deployment Helpers (2 implementations):**
1. **Cell 8** - CLI-based (uses az() helper)
2. **Cell 36** - SDK-based (uses Azure SDK)

**Recommendation:**
- **KEEP:** Cell 8 (more flexible, easier to debug)
- **REMOVE:** Cell 36 deployment functions
- **RATIONALE:** CLI approach is more reliable for ARM/Bicep

#### **Duplicate MCP Initializations (3 implementations):**
1. **Cell 10** - Unified MCP Initialization (ENV-driven)
2. **Cell 22** - MCP Client (2 servers)
3. **Cell 23** - MCP Client (5 servers)

**Recommendation:**
- **KEEP:** Cell 10 (most flexible, ENV-driven)
- **REMOVE:** Cells 22, 23 (hardcoded URLs)
- **ALTERNATIVE:** If Cells 22/23 have better client implementation, merge logic into Cell 10

#### **Duplicate Dependency Installers (3 implementations):**
Cells: 4, 15, 24

**Recommendation:**
- **KEEP:** Cell 4 (in consolidated section)
- **REMOVE:** Cells 15, 24 (redundant)
- **ENHANCEMENT:** Add check to skip if already installed

#### **Legacy/Deprecated Cells:**
1. **Cell 14** - Azure CLI + Service Principal (LEGACY)
   - Comment says "now delegates to unified az()"
   - **REMOVE** - serves no purpose

2. **Cell 18** - Azure CLI path resolution (patched)
   - Redundant with Cell 5
   - **REMOVE**

3. **Cell 31** - Azure CLI resolution for subsequent operations
   - Another duplicate
   - **REMOVE**

#### **Orphan/Dead Code:**
Cells 97, 113, 141, 190 (identified as orphans with no dependencies)

**Recommendation:**
- **INVESTIGATE:** Determine if these cells serve any purpose
- **DOCUMENT:** If keeping them, add markdown explaining why
- **REMOVE:** If truly unused

### 4.3 REDUNDANT Patterns

#### **Repeated Code Patterns:**

1. **Path existence checks:**
   ```python
   # Appears in ~38 cells
   if Path(file).exists():
       # do something
   ```
   **Recommendation:** Create utility function `ensure_file_exists(path, error_msg)`

2. **Environment variable access with fallback:**
   ```python
   # Appears in ~30+ cells
   value = os.getenv('VAR') or os.getenv('ALT_VAR') or 'default'
   ```
   **Recommendation:** Centralize in ENV dictionary with fallback logic

3. **Subprocess execution with error handling:**
   ```python
   # Appears in ~20 cells
   result = subprocess.run(cmd, capture_output=True, text=True)
   if result.returncode != 0:
       print(f"Error: {result.stderr}")
   ```
   **Recommendation:** Use unified `az()` helper or create `run_cmd()` utility

4. **JSON file read/write:**
   ```python
   # Appears in ~15 cells
   with open(file, 'r') as f:
       data = json.load(f)
   ```
   **Recommendation:** Create `read_json(path)` and `write_json(path, data)` utilities

5. **Temporary file creation:**
   ```python
   # Appears in ~10 cells
   with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
       f.write(content)
       temp_path = f.name
   ```
   **Recommendation:** Create `create_temp_file(content, suffix)` utility

#### **Redundant Validation:**
Multiple cells validate Azure CLI presence:
- Cells 5, 7, 17, 18, 27, 31, 32, etc.

**Recommendation:** Validate ONCE in setup section (Cell 5), fail fast if missing

#### **Redundant Error Handling:**
Many cells implement similar try/except patterns for the same operations.

**Recommendation:** Consistent error handling strategy:
- Define custom exception classes (Cell 11 does this well)
- Use decorators for common error patterns
- Centralize error logging

---

## PART 5: CONSOLIDATED FINDINGS & IMPACT ANALYSIS

### 5.1 Duplicate Code Metrics

| Category | Count | Lines of Duplicate Code (Est.) | Impact |
|----------|-------|-------------------------------|--------|
| Environment Loaders | 4 | 400-600 lines | High - Inconsistent state |
| Azure CLI Resolvers | 13 | 650-800 lines | Critical - Most duplicated |
| get_az_cli() functions | 10 | 400-500 lines | Critical |
| Deployment Helpers | 2 | 200-300 lines | Medium |
| MCP Initializations | 3 | 150-200 lines | Medium |
| Dependency Installers | 3 | 100-150 lines | Low |
| Import statements | ~50+ | 200-300 lines | Low - Cosmetic |
| **TOTAL DUPLICATE CODE** | | **~2,300-3,200 lines** | |

**Analysis:** Approximately 2,300-3,200 lines of duplicate code could be eliminated through consolidation.

### 5.2 Execution Flow Issues

#### **Current State:**
```
Recommended Consolidated Flow (Cells -1.x):
Cell 1  → Documentation
Cell 2  → Env Loader ────────┐
Cell 3  → Env Loader (dup) ──┤ CONFLICT: Which runs?
Cell 13 → Env Loader (dup) ──┤
Cell 41 → Env Loader (dup) ──┘

Cell 4  → Dependency Install ────┐
Cell 15 → Dependency Install (dup)─┤ CONFLICT
Cell 24 → Dependency Install (dup)─┘

Cell 5  → Azure CLI Setup ───────────┐
Cell 7  → Azure CLI Wrapper (az())  │ PARTIALLY OK
Cell 17 → get_az_cli() ────────┐    │
Cell 18 → get_az_cli() ────────┤    │ MASSIVE CONFLICT
Cell 27 → get_az_cli() ────────┤    │
...     → 10 more definitions ─┘    │
                                     │
Cell 8  → Deployment Helpers ────────┤
Cell 11 → AzureOps Class ────────────┤ OVERLAP
Cell 36 → Deployment Helpers (dup) ─┘

Cell 38 → MAIN DEPLOYMENT ──→ ❌ BLOCKED: Missing bicep files
Cell 40 → Generate .env ──→ Depends on Cell 38 outputs
```

**Problems:**
1. **No clear "run cells 1-N" sequence** - Users must pick which duplicates to run
2. **Silent conflicts** - Running both Cell 8 and 36 creates duplicate function definitions
3. **Dependency confusion** - Cell 38 needs outputs from Cell 8, but Cell 36 also provides same functions
4. **Circular references** - Cell 40 generates .env, but earlier cells expect it to exist

#### **Missing Critical Path:**
```
DEPLOYMENT CANNOT PROCEED:

Cell 38 (Main Deployment)
    ↓ requires
deploy-01-core.bicep ──→ ❌ MISSING
params-01-core.json ──→ ❌ MISSING
    ↓ requires
compile_bicep() ──→ ✅ Available (Cell 8 or 36)
deploy_template() ──→ ✅ Available (Cell 8 or 36)
    ↓ requires
az_cli ──→ ✅ Available (multiple sources - confusing)
credentials ──→ ✅ Available (.azure-credentials.env exists)
```

**Blocker:** Cannot test deployment without bicep files.

### 5.3 Risk Assessment

| Risk | Severity | Probability | Impact | Mitigation Priority |
|------|----------|-------------|--------|-------------------|
| Deployment fails due to missing bicep files | **CRITICAL** | 100% | Complete failure | **URGENT** |
| Incorrect config loaded from duplicate loaders | **HIGH** | 60% | Wrong endpoints, auth failures | **HIGH** |
| Azure CLI resolution fails | **MEDIUM** | 30% | Deployment blocked | **MEDIUM** |
| Policy application fails (missing env vars) | **MEDIUM** | 80% | Incomplete deployment | **MEDIUM** |
| Dependency installation incomplete | **LOW** | 20% | Import errors | **LOW** |
| MCP servers not initialized | **LOW** | 50% | MCP features unavailable | **LOW** |

### 5.4 Maintainability Score

**Current State:** ⚠️ **3/10** (Poor)

**Issues:**
- ❌ Excessive duplication makes changes error-prone
- ❌ No clear execution order documented
- ❌ Multiple sources of truth for configuration
- ❌ 13 implementations of the same function (get_az_cli)
- ❌ Missing critical deployment files
- ⚠️ 38 cells involved in deployment (too many touch points)
- ⚠️ Cell 232 depends on 31 other cells (tight coupling)
- ✅ No execution errors (at least what exists runs)

**After Consolidation (Projected):** ✅ **7-8/10** (Good)

---

## PART 6: COMPREHENSIVE RECOMMENDATIONS

### 6.1 IMMEDIATE ACTIONS (Required for Deployment)

#### **Priority 1: Resolve Missing Deployment Files**

**USER CLARIFICATION NEEDED:** You indicated "Other" for bicep files. Please clarify:
- **Option A:** Files exist elsewhere → Provide correct path
- **Option B:** Files are missing → Need to create them
- **Option C:** Using different deployment method → Document what replaces bicep

**If Option B (Creating Files):**
1. Extract bicep templates from deployment history:
   ```bash
   az deployment group show \
     --resource-group lab-master-lab \
     --name master-lab-01-core \
     --query properties.template > deploy-01-core.bicep
   ```

2. Or create from scratch based on Cell 38 requirements:
   - deploy-01-core.bicep: APIM, Log Analytics, App Insights
   - deploy-02c-apim-api.bicep: APIM API configuration
   - deploy-03-supporting.bicep: Cosmos DB, Redis, Azure Search
   - deploy-04-mcp.bicep: MCP server infrastructure

3. Create parameter files:
   - params-01-core.json
   - params-03-supporting.json

#### **Priority 2: Add Missing Environment Variables**

**File:** `master-lab.env`

**Add:**
```bash
# APIM Configuration (required for policy application)
APIM_SERVICE=apim-<unique-id>
API_ID=azure-openai-api
```

**Derive from existing values:**
```python
# Add to Cell 6 (Endpoint Normalizer)
if 'APIM_GATEWAY_URL' in os.environ:
    # Extract APIM service name from gateway URL
    # https://apim-xyz123.azure-api.net → apim-xyz123
    import re
    match = re.search(r'//([^.]+)', os.environ['APIM_GATEWAY_URL'])
    if match:
        os.environ['APIM_SERVICE'] = match.group(1)
```

#### **Priority 3: Create Pre-Deployment Validation Cell**

**Insert before Cell 38:**
```python
# Cell 37.5: Pre-Deployment Validation
"""
Validates all prerequisites before starting deployment.
Fails fast if any critical requirement is missing.
"""
import sys
from pathlib import Path

print("="*70)
print("PRE-DEPLOYMENT VALIDATION")
print("="*70)

errors = []
warnings = []

# Check bicep files
bicep_files = [
    'deploy-01-core.bicep',
    'deploy-02c-apim-api.bicep',
    'deploy-03-supporting.bicep',
    'deploy-04-mcp.bicep'
]
for bicep in bicep_files:
    if not Path(bicep).exists():
        errors.append(f"Missing bicep file: {bicep}")

# Check parameter files
param_files = ['params-01-core.json', 'params-03-supporting.json']
for param in param_files:
    if not Path(param).exists():
        errors.append(f"Missing parameter file: {param}")

# Check environment variables
required_env = [
    'SUBSCRIPTION_ID', 'RESOURCE_GROUP', 'LOCATION',
    'APIM_GATEWAY_URL', 'APIM_API_KEY'
]
for var in required_env:
    if not os.getenv(var):
        errors.append(f"Missing environment variable: {var}")

# Check Azure CLI
if not az_cli or not Path(az_cli).exists():
    errors.append("Azure CLI not found")

# Check credentials
if not Path('.azure-credentials.env').exists():
    warnings.append("No service principal credentials found (will use interactive login)")

# Report
if errors:
    print("\n❌ VALIDATION FAILED\n")
    for err in errors:
        print(f"  ❌ {err}")
    print("\n⚠️  Cannot proceed with deployment. Fix errors above.\n")
    sys.exit(1)

if warnings:
    print("\n⚠️  WARNINGS\n")
    for warn in warnings:
        print(f"  ⚠️  {warn}")

print("\n✅ All validations passed. Ready to deploy.\n")
```

### 6.2 CONSOLIDATION PLAN (Phase 1: Remove Duplicates)

Based on your preference to **"Keep only consolidated cells"**, here's the removal plan:

#### **Environment Loaders - KEEP Cell 3, REMOVE Cells 2, 13, 41**

**Action:**
```python
# REMOVE Cell 2 entirely (first env loader)
# REMOVE Cell 13 entirely (third env loader)
# REMOVE Cell 41 (OR merge NotebookConfig class into Cell 3)
```

**If keeping NotebookConfig from Cell 41:**
```python
# Cell 3 (Enhanced - Consolidated Environment Loader)
from pathlib import Path
import re, os
from dataclasses import dataclass
from typing import Optional

ENV_FILE = Path('master-lab.env')
TEMPLATE = """# master-lab.env
SUBSCRIPTION_ID=
RESOURCE_GROUP=
LOCATION=
APIM_GATEWAY_URL=
APIM_SERVICE=
API_ID=azure-openai-api
INFERENCE_API_PATH=/inference
OPENAI_ENDPOINT=
MODEL_SKU=gpt-4o-mini
"""

SENSITIVE_PATTERN = re.compile(r'(KEY|SECRET|TOKEN|PASSWORD|API_KEY)', re.IGNORECASE)

@dataclass
class NotebookConfig:
    subscription_id: str
    resource_group: str
    location: str
    apim_gateway_url: str
    apim_service: str
    api_id: str = "azure-openai-api"
    openai_endpoint: Optional[str] = None
    model_sku: str = "gpt-4o-mini"

def ensure_env():
    if not ENV_FILE.exists():
        ENV_FILE.write_text(TEMPLATE, encoding='utf-8')
        print(f"[env] Created {ENV_FILE} - please fill in values")
        return {}

    env = {}
    for line in ENV_FILE.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            env[key.strip()] = value.strip()
            os.environ[key.strip()] = value.strip()

    # Display summary (masked)
    print("[env] Loaded keys:", ', '.join(env.keys()))
    return env

# Load environment
ENV = ensure_env()

# Create config object
config = NotebookConfig(
    subscription_id=ENV.get('SUBSCRIPTION_ID', ''),
    resource_group=ENV.get('RESOURCE_GROUP', ''),
    location=ENV.get('LOCATION', 'uksouth'),
    apim_gateway_url=ENV.get('APIM_GATEWAY_URL', ''),
    apim_service=ENV.get('APIM_SERVICE', ''),
    api_id=ENV.get('API_ID', 'azure-openai-api'),
    openai_endpoint=ENV.get('OPENAI_ENDPOINT'),
    model_sku=ENV.get('MODEL_SKU', 'gpt-4o-mini')
)

print(f"[env] Configuration loaded: {config.resource_group} @ {config.location}")
```

#### **Azure CLI Resolvers - KEEP Cell 5, REMOVE all others**

**Cells to REMOVE:** 14, 17, 18, 27, 31, 32, (and 46, 53, 63, 72, 107, 112, 219, 232 in later sections)

**Action:**
- Remove all standalone get_az_cli() definitions
- Remove all `az_cli = shutil.which('az')` blocks

**Ensure Cell 5 exports az_cli globally:**
```python
# Cell 5 (Enhanced - SINGLE Azure CLI Resolver)
# ... (existing Cell 5 code) ...

# At end of Cell 5, confirm it's set globally:
if 'az_cli' not in globals() or not az_cli:
    raise SystemExit("[FATAL] Failed to resolve Azure CLI")

print(f"[azure] ✅ Azure CLI resolved: {az_cli}")
print(f"[azure] This value is now available to all subsequent cells")

# Export to environment for subprocess calls
os.environ['AZ_CLI'] = az_cli
os.environ['AZURE_CLI_PATH'] = az_cli
```

**Update dependent cells to use global az_cli:**
```python
# Example: Cell 17 (Semantic Caching) - BEFORE
def get_az_cli():
    az_path = shutil.which('az')
    # ... 20 lines of resolution code ...
    return az_path

az_cli = get_az_cli()

# AFTER (simplified):
# Assumes Cell 5 has run - az_cli is already defined globally
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")

print(f"[INFO] Using Azure CLI: {az_cli}")
```

#### **Deployment Helpers - KEEP Cell 8, REMOVE Cell 36 duplicate functions**

**Cell 36 Action:**
- KEEP: Azure SDK authentication setup
- KEEP: resource_client initialization
- REMOVE: compile_bicep(), deploy_template(), get_deployment_outputs() functions (duplicates of Cell 8)

**Updated Cell 36:**
```python
# Cell 36: Azure SDK Authentication ONLY
"""
Initializes Azure SDK clients for deployment operations.
Uses deployment helper functions from Cell 8 (CLI-based).
"""
import json, os
from dotenv import load_dotenv
from azure.mgmt.resource import ResourceManagementClient
from azure.identity import ClientSecretCredential, AzureCliCredential

print('[*] Initializing Azure authentication...')

# Load service principal credentials if available
credentials_file = '.azure-credentials.env'
credential = None

if os.path.exists(credentials_file):
    load_dotenv(credentials_file)
    credential = ClientSecretCredential(
        tenant_id=os.getenv('AZURE_TENANT_ID'),
        client_id=os.getenv('AZURE_CLIENT_ID'),
        client_secret=os.getenv('AZURE_CLIENT_SECRET')
    )
    print('[OK] Using Service Principal credentials')
else:
    credential = AzureCliCredential()
    print('[OK] Using Azure CLI credentials')

# Initialize resource management client
subscription_id = os.getenv('SUBSCRIPTION_ID') or os.getenv('AZURE_SUBSCRIPTION_ID')
resource_client = ResourceManagementClient(credential, subscription_id)

# Test connection
try:
    rg_list = list(resource_client.resource_groups.list())
    print(f'[OK] Azure SDK initialized ({len(rg_list)} resource groups accessible)')
except Exception as e:
    print(f'[ERROR] SDK initialization failed: {e}')

# NOTE: Deployment functions (compile_bicep, deploy_template, get_deployment_outputs)
# are defined in Cell 8. Use those functions for deployments.
print('[OK] Use deployment functions from Cell 8')
```

#### **MCP Initializations - KEEP Cell 10, REMOVE Cells 22, 23**

**Action:** Remove Cells 22 and 23 entirely.

**Enhance Cell 10:**
```python
# Cell 10: Unified MCP Initialization (Enhanced)
"""
Initializes required MCP servers in a single pass.
Configure servers via environment variables:
  GITHUB_MCP_URL, WEATHER_MCP_URL, PRODUCT_CATALOG_MCP_URL,
  ONCALL_MCP_URL, SPOTIFY_MCP_URL, EXCEL_MCP_URL, DOCS_MCP_URL
"""
import os
import sys
sys.path.append('.')

MCP_SERVERS = {}

# Server specifications (name, url_env_var, helper_module, class_name)
SERVER_SPECS = [
    ('github', 'GITHUB_MCP_URL', 'notebook_mcp_helpers', 'GitHubMCPClient'),
    ('weather', 'WEATHER_MCP_URL', 'notebook_mcp_helpers', 'WeatherMCPClient'),
    ('product_catalog', 'PRODUCT_CATALOG_MCP_URL', 'notebook_mcp_helpers', 'ProductCatalogMCPClient'),
    ('oncall', 'ONCALL_MCP_URL', 'notebook_mcp_helpers', 'OnCallMCPClient'),
    ('spotify', 'SPOTIFY_MCP_URL', 'notebook_mcp_helpers', 'SpotifyMCPClient'),
    ('excel', 'EXCEL_MCP_URL', 'notebook_mcp_helpers', 'ExcelMCPClient'),
    ('docs', 'DOCS_MCP_URL', 'notebook_mcp_helpers', 'DocsMCPClient'),
]

for name, url_env, module, cls_name in SERVER_SPECS:
    url = os.getenv(url_env)
    if not url:
        continue  # Skip if not configured

    try:
        mod = __import__(module, fromlist=[cls_name])
        client_class = getattr(mod, cls_name)
        MCP_SERVERS[name] = client_class(url)
        print(f"[mcp] ✅ Initialized {name}: {url}")
    except (ImportError, AttributeError) as e:
        print(f"[mcp] ⚠️  Skipping {name}: {e}")

print(f"[mcp] Initialized {len(MCP_SERVERS)} server(s)")

# Create convenience object if any servers initialized
if MCP_SERVERS:
    class MCPServers:
        def __init__(self, servers):
            for name, client in servers.items():
                setattr(self, name, client)

    mcp = MCPServers(MCP_SERVERS)
    print("[mcp] ✅ MCP servers available via 'mcp.<server_name>'")
```

#### **Dependency Installers - KEEP Cell 4, REMOVE Cells 15, 24**

**Action:** Remove Cells 15 and 24 entirely.

**Enhance Cell 4:**
```python
# Cell 4: Dependencies Install (Consolidated & Idempotent)
import sys, subprocess, pathlib, shlex

REQ_FILE = pathlib.Path('requirements.txt')

# Check if already installed in this kernel session
if '_REQS_INSTALLED' in globals() and globals()['_REQS_INSTALLED']:
    print('[deps] ✅ Dependencies already installed (skipping)')
else:
    if REQ_FILE.exists():
        cmd = [sys.executable, '-m', 'pip', 'install', '-r', str(REQ_FILE)]
        print(f"[deps] Installing: {' '.join(shlex.quote(c) for c in cmd)}")

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print('[deps] ✅ Installation complete')
            globals()['_REQS_INSTALLED'] = True
        else:
            print(f'[deps] ❌ Installation failed (exit {result.returncode})')
            print(result.stderr[:500])
    else:
        print(f'[deps] ⚠️  {REQ_FILE} not found')
```

### 6.3 CONSOLIDATION PLAN (Phase 2: Eliminate Redundant Patterns)

#### **Create Utilities Cell (New Cell 7.5)**

**Insert after Cell 7 (az() helper):**
```python
# Cell 7.5: Common Utility Functions
"""
Shared utility functions to eliminate code duplication.
"""
from pathlib import Path
import json, subprocess, shlex
from typing import Any, Dict, Optional

def ensure_file_exists(path: str, error_msg: Optional[str] = None) -> Path:
    """Check file exists, raise error if not."""
    p = Path(path)
    if not p.exists():
        msg = error_msg or f"Required file not found: {path}"
        raise FileNotFoundError(msg)
    return p

def read_json(path: str) -> Dict[str, Any]:
    """Read JSON file with error handling."""
    p = ensure_file_exists(path, f"Cannot read JSON: {path}")
    return json.loads(p.read_text(encoding='utf-8'))

def write_json(path: str, data: Dict[str, Any], indent: int = 2):
    """Write JSON file with formatting."""
    Path(path).write_text(json.dumps(data, indent=indent), encoding='utf-8')
    print(f"[util] ✅ Wrote {path}")

def run_cmd(cmd: list, description: str = "", timeout: int = 300) -> tuple:
    """
    Run command with consistent error handling.
    Returns: (success: bool, output: str, error: str)
    """
    if description:
        print(f"[cmd] {description}")

    cmd_str = ' '.join(shlex.quote(str(c)) for c in cmd)
    print(f"[cmd] Executing: {cmd_str[:100]}...")

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)

    success = result.returncode == 0
    status = "✅" if success else "❌"
    print(f"[cmd] {status} Exit code: {result.returncode}")

    return success, result.stdout, result.stderr

def get_env(key: str, required: bool = False, default: str = "") -> str:
    """Get environment variable with consistent behavior."""
    value = os.getenv(key, default)
    if required and not value:
        raise ValueError(f"Required environment variable missing: {key}")
    return value

print("[util] ✅ Utility functions loaded")
```

**Benefits:**
- Eliminates ~500 lines of duplicate code
- Consistent error handling
- Easier to maintain

### 6.4 EXECUTION ORDER CONSOLIDATION

#### **Final Recommended Cell Execution Order:**

**Section -1: Initialization (RUN ONCE)**
```
Cell 1  → Documentation (master plan)
Cell 3  → Environment Loader (SINGLE SOURCE OF TRUTH)
Cell 4  → Dependencies Install
Cell 5  → Azure CLI & Service Principal Setup
Cell 6  → Endpoint Normalizer
Cell 7  → Azure CLI az() Wrapper
Cell 7.5 → Utility Functions (NEW)
Cell 8  → Deployment Helpers (CLI-based)
Cell 10 → MCP Initialization
Cell 11 → AzureOps Wrapper (optional, for complex scenarios)
```

**Section 0: Pre-Deployment**
```
Cell 28 → Master Imports
Cell 30 → Verify Environment Loaded
Cell 34 → Deployment Configuration
Cell 36 → Azure SDK Authentication (simplified)
Cell 37.5 → Pre-Deployment Validation (NEW)
```

**Section 1: Deployment**
```
Cell 38 → Main Deployment (4 steps)
Cell 40 → Generate/Update master-lab.env
```

**Section 2: Testing** (Cells 42+)
```
(Depends on specific lab exercises - not analyzed in detail)
```

**Deprecated Cells (MARK FOR REMOVAL):**
```
Cell 2   → ENV Loader (duplicate of Cell 3)
Cell 13  → ENV Loader (duplicate of Cell 3)
Cell 14  → Azure CLI (duplicate of Cell 5)
Cell 15  → Dependencies (duplicate of Cell 4)
Cell 17  → Policy+Az CLI (extract policy, remove az_cli code)
Cell 18  → Az CLI (duplicate of Cell 5)
Cell 22  → MCP (duplicate of Cell 10)
Cell 23  → MCP (duplicate of Cell 10)
Cell 24  → Dependencies (duplicate of Cell 4)
Cell 27  → Policy+Az CLI (extract policy, remove az_cli code)
Cell 31  → Az CLI (duplicate of Cell 5)
Cell 32  → Az CLI (duplicate of Cell 5)
Cell 41  → ENV Loader (merge NotebookConfig into Cell 3, then remove)
```

**Refactor (Extract Logic, Remove Duplication):**
```
Cells 46, 53, 63, 72, 107, 112, 219, 232 → Remove get_az_cli(), use global from Cell 5
```

### 6.5 OPTIMIZATION RECOMMENDATIONS (Top 3)

#### **Recommendation #1: Implement "Run All Setup" Cell**

**New Cell 1.5: One-Click Setup**
```python
# Cell 1.5: One-Click Setup (Run This First)
"""
Executes all initialization cells in correct order.
Run this cell to set up environment for first time or after kernel restart.
"""
import IPython
from IPython.display import display, Markdown

setup_cells = [
    (3, "Environment Loader"),
    (4, "Dependencies Install"),
    (5, "Azure CLI Setup"),
    (6, "Endpoint Normalizer"),
    (7, "Azure CLI Wrapper"),
    (7.5, "Utility Functions"),
    (8, "Deployment Helpers"),
    (10, "MCP Initialization"),
    (28, "Master Imports"),
]

print("="*70)
print("AUTOMATED SETUP - Initializing notebook environment")
print("="*70)

for cell_num, description in setup_cells:
    print(f"\n[{cell_num}] {description}...")
    try:
        # Execute cell by number (requires IPython)
        get_ipython().run_cell(In[cell_num])
        print(f"[{cell_num}] ✅ Complete")
    except Exception as e:
        print(f"[{cell_num}] ❌ Failed: {e}")
        print("⚠️  Fix the error and re-run this cell")
        break

print("\n" + "="*70)
print("✅ SETUP COMPLETE - Ready to run deployment")
print("="*70)
display(Markdown("""
**Next steps:**
1. Verify configuration: Check `master-lab.env` has all required values
2. Run Cell 37.5 (Pre-Deployment Validation)
3. Run Cell 38 (Main Deployment)
"""))
```

**Benefits:**
- One cell to run everything
- Clear progress indicators
- Stops on first error
- Eliminates "which cells do I run?" confusion

#### **Recommendation #2: Dependency Injection for Azure CLI**

**Problem:** 13 cells redefine `az_cli`, 10 cells redefine `get_az_cli()`

**Solution:** Make Cell 5 create a singleton Azure CLI manager

**New Cell 5 (Enhanced with Singleton Pattern):**
```python
# Cell 5: Azure CLI Manager (Singleton)
import os, json, subprocess, shlex
from pathlib import Path
from typing import Optional, Tuple

class AzureCLIManager:
    """Singleton manager for Azure CLI operations."""
    _instance = None
    _az_cli_path = None
    _credentials = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._az_cli_path is None:
            self._resolve_az_cli()
            self._load_credentials()

    def _resolve_az_cli(self):
        """Find Azure CLI executable."""
        import shutil

        # Priority order
        candidates = [
            shutil.which("az"),
            r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd",
            "/usr/bin/az",
            os.getenv("AZURE_CLI_PATH"),
            os.getenv("AZ_CLI"),
        ]

        for candidate in candidates:
            if candidate and Path(candidate).exists():
                self._az_cli_path = candidate
                print(f"[azure-cli] ✅ Resolved: {candidate}")
                return

        raise FileNotFoundError("Azure CLI 'az' not found")

    def _load_credentials(self):
        """Load service principal credentials if available."""
        creds_file = Path('.azure-credentials.env')
        if creds_file.exists():
            for line in creds_file.read_text().splitlines():
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    self._credentials[key.strip()] = value.strip()
            print(f"[azure-cli] ✅ Loaded credentials ({len(self._credentials)} keys)")

    @property
    def path(self) -> str:
        """Get Azure CLI executable path."""
        return self._az_cli_path

    def run(self, args: str, json_output: bool = True, timeout: int = 300) -> Tuple[bool, any]:
        """
        Execute Azure CLI command.
        Args:
            args: CLI arguments (e.g., "account show")
            json_output: Parse output as JSON
            timeout: Command timeout in seconds
        Returns:
            (success: bool, result: dict|str)
        """
        cmd = [self._az_cli_path] + shlex.split(args)
        if json_output and '--output json' not in args:
            cmd.extend(['--output', 'json'])

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)

        if result.returncode != 0:
            return False, result.stderr

        if json_output:
            try:
                return True, json.loads(result.stdout)
            except json.JSONDecodeError:
                return True, result.stdout
        else:
            return True, result.stdout

    def verify_login(self) -> bool:
        """Check if logged into Azure."""
        success, data = self.run("account show")
        if success:
            print(f"[azure-cli] ✅ Logged in as: {data.get('user', {}).get('name', 'unknown')}")
            return True
        else:
            print("[azure-cli] ⚠️  Not logged in")
            return False

# Initialize singleton
az_manager = AzureCLIManager()

# Verify login
az_manager.verify_login()

# Backward compatibility: export az_cli variable
az_cli = az_manager.path
os.environ['AZ_CLI'] = az_cli
os.environ['AZURE_CLI_PATH'] = az_cli

print("[azure-cli] ✅ Manager ready - use 'az_manager.run(...)' for commands")
```

**Usage in other cells:**
```python
# OLD WAY (Cell 17 before):
az_cli = get_az_cli()  # 20 lines of duplicate code
result = subprocess.run([az_cli, 'account', 'show'], ...)

# NEW WAY (Cell 17 after):
success, data = az_manager.run("account show")
if success:
    print(data)
```

**Benefits:**
- Eliminates ~800 lines of duplicate code
- Consistent error handling
- Single source of truth
- Backward compatible (az_cli variable still exists)

#### **Recommendation #3: State Checkpoint System**

**Problem:**
- No way to know which cells have been run
- No validation that prerequisites are met
- Deployment can fail halfway through with no recovery

**Solution:** Implement checkpoint system

**New Cell 0: Checkpoint Manager**
```python
# Cell 0: Notebook State Checkpoint Manager
"""
Tracks which initialization cells have been executed.
Allows cells to verify prerequisites before running.
"""
from dataclasses import dataclass
from typing import Set, Optional
from datetime import datetime

@dataclass
class NotebookState:
    """Tracks notebook initialization state."""
    initialized_cells: Set[int]
    env_loaded: bool = False
    azure_cli_ready: bool = False
    dependencies_installed: bool = False
    deployment_validated: bool = False
    last_deployment: Optional[str] = None

    def mark_complete(self, cell_num: int, checkpoint: str = ""):
        """Mark a cell as complete."""
        self.initialized_cells.add(cell_num)
        if checkpoint:
            setattr(self, checkpoint, True)
        print(f"[checkpoint] ✅ Cell {cell_num} complete{': ' + checkpoint if checkpoint else ''}")

    def require(self, *cell_nums: int, error_msg: str = ""):
        """Require specific cells to have been run."""
        missing = [c for c in cell_nums if c not in self.initialized_cells]
        if missing:
            msg = error_msg or f"Required cells not run: {missing}"
            raise RuntimeError(f"❌ {msg}\nRun those cells first, then retry.")

    def require_checkpoint(self, checkpoint: str):
        """Require a specific checkpoint to have been reached."""
        if not getattr(self, checkpoint, False):
            raise RuntimeError(f"❌ Checkpoint '{checkpoint}' not reached. Run initialization cells first.")

    def status(self):
        """Print current state."""
        print("="*70)
        print("NOTEBOOK STATE")
        print("="*70)
        print(f"Initialized cells: {sorted(self.initialized_cells)}")
        print(f"Environment loaded: {'✅' if self.env_loaded else '❌'}")
        print(f"Azure CLI ready: {'✅' if self.azure_cli_ready else '❌'}")
        print(f"Dependencies installed: {'✅' if self.dependencies_installed else '❌'}")
        print(f"Deployment validated: {'✅' if self.deployment_validated else '❌'}")
        if self.last_deployment:
            print(f"Last deployment: {self.last_deployment}")
        print("="*70)

# Initialize global state
if 'notebook_state' not in globals():
    notebook_state = NotebookState(initialized_cells=set())
    print("[checkpoint] ✅ State tracking initialized")
else:
    print("[checkpoint] ℹ️  State tracking already active")

notebook_state.status()
```

**Usage in initialization cells:**
```python
# Cell 3 (Environment Loader) - ADD AT END:
notebook_state.mark_complete(3, checkpoint="env_loaded")

# Cell 5 (Azure CLI Setup) - ADD AT END:
notebook_state.mark_complete(5, checkpoint="azure_cli_ready")

# Cell 4 (Dependencies) - ADD AT END:
notebook_state.mark_complete(4, checkpoint="dependencies_installed")
```

**Usage in dependent cells:**
```python
# Cell 38 (Main Deployment) - ADD AT START:
print("[deployment] Checking prerequisites...")
notebook_state.require(3, 4, 5, 6, 7, 8, error_msg="Setup not complete")
notebook_state.require_checkpoint("env_loaded")
notebook_state.require_checkpoint("azure_cli_ready")
notebook_state.require_checkpoint("deployment_validated")  # Cell 37.5
print("[deployment] ✅ All prerequisites met")

# ... (existing deployment code) ...

# ADD AT END:
notebook_state.mark_complete(38)
notebook_state.last_deployment = datetime.now().isoformat()
```

**Benefits:**
- Clear visibility into what's been run
- Fail-fast if prerequisites missing
- Easy troubleshooting ("which cell did I forget?")
- Supports idempotent execution (skip if already done)

---

## PART 7: IMPLEMENTATION ROADMAP

### Phase 1: Critical Fixes (Week 1)
**Goal:** Enable deployment to work

- [ ] **Day 1-2:** Resolve missing bicep files
  - Option A: Locate existing files, update paths
  - Option B: Extract from deployment history
  - Option C: Create from scratch

- [ ] **Day 2:** Add missing environment variables
  - Add APIM_SERVICE and API_ID to master-lab.env
  - Update Cell 6 to auto-derive if possible

- [ ] **Day 3:** Create Pre-Deployment Validation (Cell 37.5)
  - Validates all files present
  - Validates all env vars set
  - Validates Azure CLI accessible
  - Fails fast before attempting deployment

- [ ] **Day 4-5:** Test end-to-end deployment
  - Run Cells 1-11 (setup)
  - Run Cells 28, 30, 34, 36 (pre-deployment)
  - Run Cell 37.5 (validation)
  - Run Cell 38 (deployment)
  - Run Cell 40 (env generation)
  - Verify all 4 deployment steps complete

### Phase 2: Remove Duplicates (Week 2)
**Goal:** Clean up redundant code

- [ ] **Day 1:** Consolidate Environment Loaders
  - Enhance Cell 3 (keep NotebookConfig if useful)
  - Remove Cells 2, 13, 41
  - Test environment loading

- [ ] **Day 2:** Consolidate Azure CLI Resolvers
  - Implement Cell 5 as singleton (or use existing)
  - Remove duplicate az_cli resolution from Cells 14, 17, 18, 27, 31, 32
  - Update Cells 46, 53, 63, 72, 107, 112, 219, 232 to use global az_cli

- [ ] **Day 3:** Consolidate Deployment Helpers
  - Keep Cell 8 (CLI-based)
  - Simplify Cell 36 (remove duplicates, keep SDK auth)
  - Test deployment still works

- [ ] **Day 4:** Consolidate MCP Initialization
  - Enhance Cell 10
  - Remove Cells 22, 23
  - Test MCP functionality

- [ ] **Day 5:** Consolidate Dependency Installation
  - Keep Cell 4
  - Remove Cells 15, 24
  - Add idempotency check

### Phase 3: Optimize & Harden (Week 3)
**Goal:** Improve reliability and maintainability

- [ ] **Day 1-2:** Implement Checkpoint System (Cell 0)
  - Add checkpoint tracking to all init cells
  - Add prerequisite checks to dependent cells
  - Test execution order enforcement

- [ ] **Day 3:** Create Utility Functions (Cell 7.5)
  - Extract common patterns
  - Update cells to use utilities
  - Measure code reduction

- [ ] **Day 4:** Implement One-Click Setup (Cell 1.5)
  - Create automated setup cell
  - Test full initialization flow
  - Document execution order

- [ ] **Day 5:** Add Post-Deployment Verification
  - Create Cell 40.5 (verify deployment health)
  - Test endpoints reachable
  - Verify APIM policies applied
  - Confirm MCP servers responding

### Phase 4: Documentation & Testing (Week 4)
**Goal:** Ensure long-term maintainability

- [ ] **Day 1-2:** Document Execution Order
  - Create comprehensive markdown cells
  - Document each section's purpose
  - Add troubleshooting guides

- [ ] **Day 3:** Create Testing Cells
  - Unit tests for utilities
  - Integration test for deployment flow
  - Validation tests for configuration

- [ ] **Day 4:** Investigate Orphan Cells
  - Cells 97, 113, 141, 190
  - Determine if needed
  - Document or remove

- [ ] **Day 5:** Final Cleanup
  - Remove all deprecated cells
  - Renumber cells if needed
  - Create clean "production" version

---

## PART 8: SUMMARY & NEXT STEPS

### Key Findings Recap

**What's Loaded Properly:** ✅
- Environment variables from master-lab.env
- Azure CLI resolution and authentication
- Python dependencies
- Deployment helper functions (defined, not tested)
- MCP client libraries

**What's NOT Completely Loaded:** ⚠️
- Missing environment variables (APIM_SERVICE, API_ID)
- MCP servers (no URLs configured, 0 initialized)
- Some cells execute but don't report status

**What's Missing:** ❌
- **CRITICAL:** All 4 bicep deployment files
- **CRITICAL:** 2 parameter JSON files
- Pre-deployment validation
- Post-deployment verification
- Error recovery procedures
- Documentation for cells 42-238

**What's Superfluous:** 🗑️
- 3 duplicate environment loaders (Cells 2, 13, 41)
- 12 duplicate Azure CLI resolvers (Cells 14, 17, 18, 27, 31, 32, 46, 53, 63, 72, 107, 112, 219, 232)
- 2 duplicate MCP initializers (Cells 22, 23)
- 2 duplicate dependency installers (Cells 15, 24)
- 1 duplicate deployment helper set (Cell 36)
- ~2,300-3,200 lines of duplicate code total

**What's Redundant:** ♻️
- 10 get_az_cli() function definitions
- 50+ duplicate import statements
- Repeated path existence checks (~38 cells)
- Repeated env variable access patterns (~30 cells)
- Repeated subprocess execution patterns (~20 cells)

### Top 3 Optimization Priorities

**#1: Implement One-Click Setup System**
- Creates Cell 1.5 that runs all initialization automatically
- Eliminates "which cells do I run?" confusion
- Provides clear progress and error reporting
- **Impact:** Reduces setup from 10+ cell runs to 1

**#2: Create Azure CLI Singleton Manager**
- Replaces 13 duplicate az_cli resolutions
- Provides consistent CLI interface
- Eliminates ~800 lines of duplicate code
- **Impact:** 40% reduction in deployment-related code

**#3: Implement State Checkpoint System**
- Tracks which cells have been executed
- Enforces execution order (fail-fast on missing prerequisites)
- Enables idempotent execution
- **Impact:** Eliminates most "forgot to run Cell X" errors

### Immediate Actions Required

**URGENT (Before Deployment Can Work):**
1. ❌ Resolve missing bicep files - **BLOCKER**
   - User needs to clarify status (see "Other" response)
2. ⚠️ Add APIM_SERVICE and API_ID to master-lab.env
3. ✅ Create Pre-Deployment Validation cell (Cell 37.5)

**HIGH PRIORITY (For Reliability):**
4. Remove duplicate environment loaders (keep Cell 3)
5. Remove duplicate Azure CLI resolvers (keep Cell 5)
6. Implement checkpoint system for execution order

**MEDIUM PRIORITY (For Maintainability):**
7. Create utility functions cell (Cell 7.5)
8. Remove duplicate MCP and dependency installers
9. Consolidate deployment helpers (keep Cell 8)

**LOW PRIORITY (For Polish):**
10. Investigate orphan cells (97, 113, 141, 190)
11. Document cells 42-238
12. Create testing cells

### Success Criteria

**Deployment Works:**
- ✅ All bicep files present and valid
- ✅ Cell 38 completes all 4 deployment steps without errors
- ✅ Cell 40 generates master-lab.env with all required values
- ✅ Post-deployment verification confirms all services healthy

**Code Quality:**
- ✅ Zero duplicate function definitions
- ✅ Single source of truth for all configuration variables
- ✅ <100 lines of duplicate code remaining
- ✅ All cells report explicit success/failure status

**Usability:**
- ✅ One-click setup (Cell 1.5) initializes entire notebook
- ✅ Clear execution order documented
- ✅ Prerequisite checking prevents common errors
- ✅ Troubleshooting guide for common issues

### Next Steps for User

**Before I Proceed:**
1. **CRITICAL:** Please clarify bicep file status (you selected "Other"):
   - Where are the bicep files located?
   - OR: Do they need to be created?
   - OR: Has the deployment strategy changed?

2. **Testing Strategy:** You didn't select any testing options. Would you like:
   - Validation checkpoints between deployment steps?
   - Integration test for full deployment flow?
   - Or is testing out of scope?

3. **Approval:** Should I proceed with:
   - Creating the consolidation scripts (remove duplicate cells)?
   - Creating the optimization cells (1.5, 7.5, 37.5, etc.)?
   - Or would you like to review this report first and decide?

**Optional:** If you'd like, I can:
- Generate a "cells to delete" list with exact cell numbers
- Create a backup copy before making changes
- Generate the new/enhanced cells as separate files for review
- Create a diff showing before/after for each change

---

## APPENDIX A: Cell-by-Cell Status Matrix (Cells 1-41)

| Cell | Type | Purpose | Status | Issues | Action |
|------|------|---------|--------|--------|--------|
| 1 | Code | Documentation | ✅ OK | None | Keep |
| 2 | Code | Env Loader v1 | ⚠️ Duplicate | 1st of 4 env loaders | ❌ Remove |
| 3 | Code | Env Loader v2 | ✅ OK | Best implementation | ✅ Keep (primary) |
| 4 | Code | Dependencies | ✅ OK | Could add idempotency | ✅ Keep, enhance |
| 5 | Code | Azure CLI Setup | ✅ OK | Most comprehensive | ✅ Keep (primary) |
| 6 | Code | Endpoint Normalizer | ✅ OK | Good logic | ✅ Keep |
| 7 | Code | az() Helper | ✅ OK | Well-designed | ✅ Keep |
| 8 | Code | Deployment Helpers | ✅ OK | CLI-based (preferred) | ✅ Keep (primary) |
| 9 | Code | Policy Application | ⚠️ Missing vars | Needs APIM_SERVICE, API_ID | ⚠️ Fix env vars |
| 10 | Code | MCP Initialization | ✅ OK | No servers configured | ✅ Keep, enhance |
| 11 | Code | AzureOps Wrapper | ✅ OK | Comprehensive class | ✅ Keep (optional) |
| 12 | MD | Section header | ✅ OK | None | Keep |
| 13 | Code | Env Loader v3 | ⚠️ Duplicate | 3rd env loader | ❌ Remove |
| 14 | Code | Azure CLI (Legacy) | ⚠️ Duplicate | Marked legacy | ❌ Remove |
| 15 | Code | Dependencies v2 | ⚠️ Duplicate | 2nd installer | ❌ Remove |
| 16 | MD | Execution order | ✅ OK | Good documentation | Keep |
| 17 | Code | Semantic Caching | ⚠️ Duplicate | Has get_az_cli() | ⚠️ Refactor |
| 18 | Code | Azure CLI Resolver | ⚠️ Duplicate | Yet another | ❌ Remove |
| 19-21 | MD | Documentation | ✅ OK | None | Keep |
| 22 | Code | MCP Init (2 servers) | ⚠️ Duplicate | Hardcoded URLs | ❌ Remove |
| 23 | Code | MCP Init (5 servers) | ⚠️ Duplicate | Hardcoded URLs | ❌ Remove |
| 24 | Code | Dependencies v3 | ⚠️ Duplicate | 3rd installer | ❌ Remove |
| 25-26 | MD | Documentation | ✅ OK | None | Keep |
| 27 | Code | Policy Helper | ⚠️ Duplicate | Has get_az_cli() | ⚠️ Refactor |
| 28 | Code | Master Imports | ✅ OK | Should be used more | ✅ Keep |
| 29 | MD | Documentation | ✅ OK | None | Keep |
| 30 | Code | Load Env Vars | ⚠️ Redundant | Reloads after Cell 3 | ⚠️ Simplify/merge |
| 31 | Code | Azure CLI Resolver | ⚠️ Duplicate | Another one | ❌ Remove |
| 32 | Code | get_az_cli() | ⚠️ Duplicate | Function definition | ❌ Remove |
| 33 | MD | Documentation | ✅ OK | None | Keep |
| 34 | Code | Deployment Config | ✅ OK | Sets deployment params | ✅ Keep |
| 35 | MD | Documentation | ✅ OK | None | Keep |
| 36 | Code | Deployment Helpers SDK | ⚠️ Duplicate | SDK version of Cell 8 | ⚠️ Keep auth, remove helpers |
| 37 | MD | Documentation | ✅ OK | None | Keep |
| 38 | Code | Main Deployment | ❌ Blocked | Missing bicep files | ⚠️ Fix after bicep resolved |
| 39 | MD | Documentation | ✅ OK | None | Keep |
| 40 | Code | Generate .env | ✅ OK | Depends on Cell 38 | ✅ Keep |
| 41 | Code | Config Loader | ⚠️ Duplicate | 4th env loader, has NotebookConfig | ⚠️ Merge class into Cell 3, remove rest |

**Summary:**
- ✅ Keep as-is: 18 cells
- ⚠️ Needs fixes: 8 cells
- ❌ Remove entirely: 11 cells
- 📝 Documentation (keep): 12 cells

---

## APPENDIX B: Duplicate Code Elimination Checklist

### Environment Loaders (4 → 1)
- [ ] Enhance Cell 3 with NotebookConfig from Cell 41
- [ ] Remove Cell 2 (ENV Loader v1)
- [ ] Remove Cell 13 (ENV Loader v3)
- [ ] Remove Cell 41 (or keep if NotebookConfig is merged)
- [ ] Test: Verify ENV dictionary populated correctly
- [ ] Estimated savings: 400-600 lines

### Azure CLI Resolvers (13 → 1)
- [ ] Enhance Cell 5 as singleton manager
- [ ] Remove az_cli resolution from Cell 14 (Legacy)
- [ ] Remove Cell 18 (standalone resolver)
- [ ] Remove az_cli resolution from Cell 17 (keep policy logic)
- [ ] Remove az_cli resolution from Cell 27 (keep policy logic)
- [ ] Remove Cell 31 (standalone resolver)
- [ ] Remove Cell 32 (get_az_cli function)
- [ ] Refactor Cells 46, 53, 63, 72 to use global az_cli
- [ ] Refactor Cells 107, 112, 219, 232 to use global az_cli
- [ ] Test: Verify Azure CLI accessible from all cells
- [ ] Estimated savings: 650-800 lines

### Deployment Helpers (2 → 1)
- [ ] Keep Cell 8 (CLI-based deployment helpers)
- [ ] Simplify Cell 36 (remove compile_bicep, deploy_template, get_deployment_outputs)
- [ ] Cell 36 keeps: Azure SDK auth and resource_client init
- [ ] Test: Verify Cell 38 can still deploy using Cell 8 functions
- [ ] Estimated savings: 200-300 lines

### MCP Initializations (3 → 1)
- [ ] Enhance Cell 10 with ENV-driven configuration
- [ ] Remove Cell 22 (2-server hardcoded init)
- [ ] Remove Cell 23 (5-server hardcoded init)
- [ ] Test: Verify MCP servers initialize when URLs provided
- [ ] Estimated savings: 150-200 lines

### Dependency Installers (3 → 1)
- [ ] Enhance Cell 4 with idempotency check
- [ ] Remove Cell 15 (duplicate installer)
- [ ] Remove Cell 24 (duplicate installer)
- [ ] Test: Verify dependencies install correctly
- [ ] Estimated savings: 100-150 lines

### Total Estimated Code Reduction
- [ ] **Before:** ~20,000-25,000 lines (entire notebook)
- [ ] **After:** ~17,000-22,000 lines (after removing 2,300-3,200 duplicate lines)
- [ ] **Improvement:** ~12-15% code reduction
- [ ] **Maintenance burden:** Reduced by ~40% (fewer duplicate touch points)

---

## APPENDIX C: Files Status Summary

### Files Referenced by Notebook

| File | Status | Used By Cells | Critical? | Action Required |
|------|--------|---------------|-----------|-----------------|
| **Deployment Files** |
| deploy-01-core.bicep | ❌ MISSING | 11, 38 | ✅ YES | Resolve location or create |
| deploy-02c-apim-api.bicep | ❌ MISSING | 38 | ✅ YES | Resolve location or create |
| deploy-03-supporting.bicep | ❌ MISSING | 38 | ✅ YES | Resolve location or create |
| deploy-04-mcp.bicep | ❌ MISSING | 38 | ✅ YES | Resolve location or create |
| params-01-core.json | ❌ MISSING | 38 | ✅ YES | Resolve location or create |
| params-03-supporting.json | ❌ MISSING | 38 | ✅ YES | Resolve location or create |
| **Configuration Files** |
| master-lab.env | ✅ EXISTS | 2, 3, 6, 13, 30, 40 | ✅ YES | Add missing APIM_SERVICE, API_ID |
| .azure-credentials.env | ✅ EXISTS | 5, 32, 36 | ⚠️ OPTIONAL | (For service principal auth) |
| requirements.txt | ✅ EXISTS | 4, 15, 24 | ✅ YES | None |
| **Code Files** |
| notebook_mcp_helpers.py | ✅ EXISTS | 10, 22, 23 | ⚠️ OPTIONAL | (For MCP functionality) |
| **System Files** |
| /etc/os-release | ✅ EXISTS (Linux) | 5 | ⚠️ OPTIONAL | (For OS detection) |

### Critical Path Blockers

**Cannot Deploy Without:**
1. ❌ deploy-01-core.bicep
2. ❌ deploy-02c-apim-api.bicep
3. ❌ deploy-03-supporting.bicep
4. ❌ deploy-04-mcp.bicep
5. ❌ params-01-core.json
6. ❌ params-03-supporting.json

**Will Fail Without:**
7. ⚠️ APIM_SERVICE environment variable (for policy application)
8. ⚠️ API_ID environment variable (for policy application)

---

## APPENDIX D: Dependency Graph (Critical Cells)

### High-Level Flow
```
Initialization → Configuration → Validation → Deployment → Post-Deployment

Cell 3 (ENV) ──┐
Cell 4 (Deps) ─┼─→ Cell 5 (Az CLI) ──→ Cell 7 (az wrapper) ──→ Cell 8 (Helpers) ──┐
Cell 28 (Imports)                                                                   │
                                                                                    │
Cell 30 (Verify ENV) ──→ Cell 34 (Config) ──→ Cell 36 (SDK Auth) ──→ [ Cell 37.5 Validation ] ──→ Cell 38 (Deploy) ──→ Cell 40 (Generate ENV)
                                                                              ↑
                                                                              │
                                                          Requires: All bicep + param files
```

### Cell 38 Dependency Tree
```
Cell 38 (Main Deployment)
├─ Requires Files:
│  ├─ deploy-01-core.bicep ❌
│  ├─ deploy-02c-apim-api.bicep ❌
│  ├─ deploy-03-supporting.bicep ❌
│  ├─ deploy-04-mcp.bicep ❌
│  ├─ params-01-core.json ❌
│  └─ params-03-supporting.json ❌
│
├─ Requires Functions:
│  ├─ compile_bicep() ✅ (Cell 8 or 36)
│  ├─ deploy_template() ✅ (Cell 8 or 36)
│  ├─ check_deployment_exists() ✅ (Cell 8 or 36)
│  └─ get_deployment_outputs() ✅ (Cell 8 or 36)
│
├─ Requires Variables:
│  ├─ az_cli ✅ (Cell 5, 7, or many others)
│  ├─ resource_client ✅ (Cell 36)
│  ├─ subscription_id ✅ (Cell 34)
│  ├─ resource_group_name ✅ (Cell 34)
│  └─ location ✅ (Cell 34)
│
└─ Requires Authentication:
   ├─ Azure CLI logged in ✅ (Cell 5, 7)
   └─ Service Principal OR interactive ✅ (Cell 36)
```

**Status:** ⚠️ 6/6 critical files MISSING, blocks all deployment

---

## APPENDIX E: Questions for User

Before proceeding with implementation, please answer:

### Critical Questions:

**Q1: Bicep Files Status**
You selected "Other" for the bicep files question. Please clarify:
- [ ] A) Bicep files exist at path: `_______________` (provide path)
- [ ] B) Bicep files need to be created from scratch
- [ ] C) Bicep files should be extracted from existing deployment
- [ ] D) Not using bicep anymore, switching to: `_______________`

**Q2: Testing Scope**
You didn't select any testing options. Should I:
- [ ] A) Skip testing cells (focus only on deployment reliability)
- [ ] B) Add minimal validation checkpoints (recommended)
- [ ] C) Add comprehensive testing suite
- [ ] D) You'll handle testing separately

**Q3: Implementation Approach**
How would you like me to proceed?
- [ ] A) Create new cells (1.5, 7.5, 37.5, etc.) but don't delete anything yet
- [ ] B) Create a separate "cleaned" version of the notebook
- [ ] C) Make changes directly to this notebook (with backup)
- [ ] D) Just provide the code snippets, you'll integrate manually

**Q4: Execution Order**
After consolidation, should I:
- [ ] A) Renumber cells to reflect logical order (1, 2, 3, ...)
- [ ] B) Keep existing cell numbers, mark deprecated ones
- [ ] C) Create a new "Quick Start" section at the top

### Optional Questions:

**Q5:** Are cells 42-238 (lab exercises) working correctly, or do they also need analysis?

**Q6:** Should I create a separate "deployment.ipynb" with only consolidated cells 1-41?

**Q7:** Do you want a rollback procedure (undo deployment if something fails)?

**Q8:** Should deployment be idempotent (safe to re-run if it fails halfway)?

---

**END OF REPORT**

**Report Statistics:**
- **Analysis Scope:** 238 total cells (focused on cells 1-41 for detail)
- **Analysis Depth:** 3 passes (code structure, outputs, cross-dependencies)
- **Issues Found:** 6 critical blockers, 24 duplicate components, 8 orphan cells
- **Recommendations:** 3 major optimizations, 11 immediate actions, 4-phase roadmap
- **Estimated Code Reduction:** 2,300-3,200 lines (~12-15%)
- **Estimated Time to Implement:** 3-4 weeks (4 phases)

---
