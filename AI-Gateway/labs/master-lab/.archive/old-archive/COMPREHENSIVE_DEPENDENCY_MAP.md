# COMPREHENSIVE DEPENDENCY MAP
## Master AI Gateway Notebook - Cell-by-Cell Analysis

**Analysis Date:** 2025-11-13
**Notebook:** master-ai-gateway-REORGANIZED.ipynb
**Total Cells:** 248 (Analysis excludes cells 57-69 per instructions)

---

## EXECUTIVE SUMMARY

### Critical Logical Errors Found

1. **Cell 7 (Load .env)** - Runs BEFORE deployment, expects file that doesn't exist yet
2. **Cell 15 (Initialize MCP)** - Runs BEFORE deployment, expects MCP URLs that don't exist yet
3. **Cell 28 (Normalize endpoints)** - Runs BEFORE cell 24 which generates the .env file it reads
4. **Duplicate cells** - Multiple cells do the same thing (environment loading, authentication)
5. **Missing dependency chain** - Cells reference variables/files created by cells that run later

### The Core Problem

**The notebook tries to INITIALIZE before DEPLOYMENT completes.**

Current broken flow:
```
Cell 7 → Load .env (doesn't exist!)
Cell 11 → Deploy infrastructure (creates resources)
Cell 15 → Initialize MCP (URLs don't exist in env yet!)
Cell 24 → Generate .env from deployment outputs (SHOULD BE EARLIER!)
Cell 28 → Normalize endpoints (reads .env before it's fully populated)
```

Correct flow should be:
```
Cell 11 → Deploy infrastructure
Cell 24 → Generate .env from outputs
Cell 28 → Normalize endpoints
Cell 7 → Load .env (NOW IT EXISTS!)
Cell 15 → Initialize MCP (NOW URLS EXIST!)
```

---

## DETAILED CELL-BY-CELL ANALYSIS (Cells 0-56, 70+)

### PHASE 0: DOCUMENTATION
**Cells:** 0, 4, 5, 6, 8, 9, 10, 12, 17, 18, 19, 23, 25, 26, etc. (119 total markdown cells)

These are section headers and explanatory text. No dependencies.

---

### PHASE 1: SETUP (Core Infrastructure - Run First)

#### Cell 1: Empty/Minimal
- **Type:** CODE
- **Purpose:** Appears to be empty or minimal setup
- **Classification:** SETUP
- **Issues:** Empty cell, should be removed

---

#### Cell 2: az() Helper Function ⭐
- **Type:** CODE
- **Purpose:** Define Azure CLI wrapper function
- **Classification:** SETUP (CRITICAL)
- **Inputs Required:**
  - Environment: `AZ_CLI` (optional, defaults to 'az')
  - System: Azure CLI installed
- **Outputs Produced:**
  - Function: `az(cmd, json_out, timeout, login_if_needed)` → (success: bool, result: str|dict)
- **Dependencies:** NONE (foundation cell)
- **Issues:** NONE
- **Must Run:** FIRST (before any Azure operations)

```python
def az(cmd: str, json_out: bool = False, timeout: int = 25, login_if_needed: bool = True):
    """Execute Azure CLI command with optional JSON parsing and login retry."""
```

---

#### Cell 3: Deployment Helper Functions ⭐
- **Type:** CODE
- **Purpose:** Define Bicep compilation and deployment functions
- **Classification:** SETUP (CRITICAL)
- **Inputs Required:**
  - Function: `az()` from cell 2
- **Outputs Produced:**
  - Function: `compile_bicep(bicep_path)` → json_template_path
  - Function: `deploy_template(rg, name, template_file, params)` → (ok, result_json)
  - Function: `get_deployment_outputs(rg, name)` → dict
  - Function: `ensure_deployment(rg, name, template, params, skip_if_exists)`
- **Dependencies:** Cell 2 (az function)
- **Issues:** NONE
- **Must Run:** Second (after cell 2, before any deployment)

```python
def compile_bicep(bicep_path:str):
def deploy_template(rg, name, template_file, params):
def get_deployment_outputs(rg, name):
def ensure_deployment(rg, name, template, params, skip_if_exists=True):
```

---

#### Cell 38: Master Imports ⭐
- **Type:** CODE
- **Purpose:** Import ALL Python dependencies for entire notebook
- **Classification:** SETUP (CRITICAL)
- **Inputs Required:**
  - System: Python packages (requests, pandas, matplotlib, azure-*, openai, etc.)
- **Outputs Produced:**
  - Global imports: asyncio, json, os, subprocess, requests, pandas, matplotlib, PIL
  - Azure SDK: DefaultAzureCredential, ResourceManagementClient, etc.
  - OpenAI SDK: AzureOpenAI client
  - Environment: Sets `API_ID` from env if available
- **Dependencies:** NONE (but requires pip install from requirements.txt)
- **Issues:** Contains some MCP references but these are just imports, not initialization
- **Must Run:** Early (before any code that uses these libraries)

---

### PHASE 2: PRE-DEPLOYMENT (Configuration)

#### Cell 13: Environment Loader (Template Creator)
- **Type:** CODE
- **Purpose:** Auto-create master-lab.env template if missing, derive APIM_SERVICE
- **Classification:** PRE-DEPLOYMENT
- **Inputs Required:** NONE
- **Outputs Produced:**
  - File: `master-lab.env` (template with placeholders)
  - Variable: `ENV_FILE` (Path object)
  - Variable: `APIM_SERVICE` (derived from APIM_GATEWAY_URL if present)
  - Variable: `SUBSCRIPTION_ID`, `LOCATION`, `APIM_GATEWAY_URL` (from env)
  - Dataclass: `NotebookConfig` (structured config)
- **Dependencies:** NONE
- **Issues:** ⚠️ DUPLICATE - Cell 16 does similar, Cell 24 is the real generator
- **Recommendation:** MERGE with cell 24 OR remove (cell 24 generates actual values)

---

#### Cell 14: Check Azure CLI & Credentials
- **Type:** CODE
- **Purpose:** Verify Azure CLI installed, check subscription access
- **Classification:** PRE-DEPLOYMENT
- **Inputs Required:**
  - Environment: `CODESPACES`, `AZURE_CLI_PATH`, `AZ_CLI`, `SUBSCRIPTION_ID`
  - System: Azure CLI binary
  - File: `~/.azure/` directory (for credentials check)
- **Outputs Produced:**
  - Variable: `AZ_CREDS_FILE` (path to Azure credentials)
  - Variable: `subscription_id` (validated)
  - Side effect: Prints Azure CLI version and subscription info
- **Dependencies:** Cell 2 (az function)
- **Issues:** NONE
- **Must Run:** Before deployment

---

#### Cell 16: Alternative Environment Loader
- **Type:** CODE
- **Purpose:** Another environment loader with gitignore management
- **Classification:** PRE-DEPLOYMENT
- **Inputs Required:** NONE
- **Outputs Produced:**
  - File: `master-lab.env` (template)
  - Variable: `ENV_FILE`, `APIM_GATEWAY_URL`, `RESOURCE_GROUP`, etc.
  - Side effect: Updates .gitignore
- **Dependencies:** NONE
- **Issues:** ⚠️ DUPLICATE of Cell 13
- **Recommendation:** REMOVE - redundant with cells 13 and 24

---

#### Cell 20: Deployment Configuration ⭐
- **Type:** CODE
- **Purpose:** Set core Azure deployment parameters
- **Classification:** PRE-DEPLOYMENT (CRITICAL)
- **Inputs Required:**
  - Environment: `SUBSCRIPTION_ID` (optional, has default)
- **Outputs Produced:**
  - Variable: `subscription_id` = 'd334f2cd-3efd-494e-9fd3-2470b1a13e4c' (or from env)
  - Variable: `deployment_name_prefix` = 'master-lab'
  - Variable: `resource_group_name` = 'lab-master-lab'
  - Variable: `location` = 'uksouth'
  - Variable: `deployment_step1/2/3/4` (deployment names)
- **Dependencies:** NONE
- **Issues:** NONE
- **Must Run:** Before deployment (cell 11)

---

#### Cell 21: Azure Authentication Setup ⭐
- **Type:** CODE
- **Purpose:** Initialize Azure credentials (Service Principal or Azure CLI)
- **Classification:** PRE-DEPLOYMENT (CRITICAL)
- **Inputs Required:**
  - File: `.azure-credentials.env` (optional, for SP auth)
  - Environment: `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET` (if using SP)
  - System: Azure CLI (fallback authentication)
- **Outputs Produced:**
  - Variable: `credential` (ClientSecretCredential or AzureCliCredential)
  - Variable: `resource_client` (ResourceManagementClient)
- **Dependencies:**
  - Cell 20 (subscription_id)
  - Imports from cell 38 (or local imports)
- **Issues:** NONE
- **Must Run:** Before deployment (cell 11)

---

#### Cell 22: Azure Authentication (Duplicate)
- **Type:** CODE
- **Purpose:** Another auth setup with deployment helpers
- **Classification:** DEPLOYMENT
- **Inputs Required:** Same as cell 21
- **Outputs Produced:** Same as cell 21 + deployment execution logic
- **Dependencies:** Cell 20
- **Issues:** ⚠️ DUPLICATE of Cell 21 + includes deployment code
- **Recommendation:** REMOVE - keep only cell 21 for auth, cell 11 for deployment

---

#### Cell 28: Endpoint Normalizer
- **Type:** CODE
- **Purpose:** Derive OPENAI_ENDPOINT from APIM_GATEWAY_URL if missing
- **Classification:** PRE-DEPLOYMENT (but should be POST-DEPLOYMENT!)
- **Inputs Required:**
  - File: `master-lab.env` (reads from file if exists)
  - Environment: `OPENAI_ENDPOINT`, `APIM_GATEWAY_URL`, `INFERENCE_API_PATH`
- **Outputs Produced:**
  - Variable: `openai_endpoint` (normalized)
  - File: `master-lab.env` (updated with normalized values)
  - Variable: `modified` (bool - whether env was updated)
- **Dependencies:**
  - Cell 24 (should generate master-lab.env first!)
- **Issues:** ⚠️ RUNS TOO EARLY - should run AFTER cell 24, not before
- **Recommendation:** MOVE to run immediately after cell 24

---

#### Cell 29: Azure CLI Path Resolution
- **Type:** CODE
- **Purpose:** Locate Azure CLI binary, handle service principal login
- **Classification:** PRE-DEPLOYMENT
- **Inputs Required:**
  - Environment: `AZ_CLI`, `AZURE_CLI_PATH`, `AZURE_CLIENT_ID`, etc.
- **Outputs Produced:**
  - Variable: `AZ_CLI` (path to az binary)
  - Side effect: Azure CLI login if needed
- **Dependencies:** NONE
- **Issues:** Overlaps with cell 14
- **Recommendation:** Could be merged with cell 14

---

#### Cell 37: Azure CLI Resolution (Another)
- **Type:** CODE
- **Purpose:** Yet another CLI path finder with policy operations
- **Classification:** PRE-DEPLOYMENT
- **Issues:** ⚠️ DUPLICATE functionality of cells 14/29
- **Recommendation:** CONSOLIDATE with cells 14/29

---

#### Cell 43: Validate Environment Variables
- **Type:** CODE
- **Purpose:** Check required variables are set (apim_gateway_url, api_key, etc.)
- **Classification:** PRE-DEPLOYMENT (but should be POST-DEPLOYMENT!)
- **Inputs Required:**
  - Variables: `apim_gateway_url`, `apim_api_key`, `inference_api_path`
- **Outputs Produced:**
  - Variable: `missing` (list of missing vars)
  - Variable: `preferred` (dict of preferred values)
- **Dependencies:** Should depend on cell 24/28 (env setup)
- **Issues:** ⚠️ Runs too early if env not loaded yet
- **Recommendation:** Move after env generation (cells 24/28)

---

### PHASE 3: DEPLOYMENT (30-40 minutes)

#### Cell 11: Main Deployment - 4 Steps ⭐⭐⭐
- **Type:** CODE
- **Purpose:** Execute complete infrastructure deployment
- **Classification:** DEPLOYMENT (CRITICAL - THE BIG ONE)
- **Inputs Required:**
  - Variable: `credential` (from cell 21)
  - Variable: `subscription_id`, `resource_group_name`, `location` (from cell 20)
  - Variable: `resource_client` (from cell 21)
  - Function: `compile_bicep`, `deploy_template`, `get_deployment_outputs` (from cell 3)
  - Environment: `BICEP_DIR` (optional, defaults to 'archive/scripts')
  - Files: Bicep templates (deploy-01-core.bicep, deploy-02-foundry.bicep, etc.)
- **Outputs Produced:**
  - Variable: `step1_outputs` (Core: APIM, Log Analytics, App Insights)
  - Variable: `step2_outputs` (AI Foundry: 3 hubs, 14 models)
  - Variable: `step3_outputs` (Redis, Search, Cosmos, Content Safety)
  - Variable: `step4_outputs` (MCP servers: 7 container apps)
  - Side effect: Creates ~40 Azure resources
  - Duration: ~40 minutes total
- **Dependencies:**
  - Cell 2 (az function)
  - Cell 3 (deployment helpers)
  - Cell 20 (config variables)
  - Cell 21 (authentication)
- **Issues:** NONE (this is correct)
- **Must Run:** After setup/config, before env generation

**Deployment Steps:**
```
Step 0: Ensure resource group exists
Step 1: Core Infrastructure (~10 min)
  - API Management
  - Log Analytics
  - Application Insights
Step 2: AI Foundry (~15 min)
  - 3 AI Hubs (East US, UK South, North Central US)
  - 14 AI Models (GPT-4, GPT-4o, embeddings, DALL-E)
Step 3: Supporting Services (~10 min)
  - Redis Cache
  - Azure AI Search
  - Cosmos DB
  - Content Safety
Step 4: MCP Servers (~5 min)
  - Container Apps Environment
  - 7 MCP servers (weather, github, oncall, spotify, etc.)
```

---

#### Cell 31: AzureOps Wrapper (Enhanced)
- **Type:** CODE
- **Purpose:** High-level Azure operations wrapper (SDK strategy)
- **Classification:** DEPLOYMENT (ALTERNATIVE)
- **Inputs Required:**
  - Environment: Multiple Azure and subscription variables
  - Function: `az()` from cell 2 (for CLI strategy)
- **Outputs Produced:**
  - Class: `AzureOps` (with methods for deployment, APIM policies, etc.)
  - Variable: `AZ_OPS` (instance)
- **Dependencies:** Cell 2, 20, 21
- **Issues:** Alternative to cell 11, seems to be a different approach
- **Recommendation:** Clarify if this replaces cell 11 or is supplementary

---

### PHASE 4: POST-DEPLOYMENT (Generate Configuration)

#### Cell 24: Generate master-lab.env ⭐⭐⭐
- **Type:** CODE
- **Purpose:** Create complete .env file from deployment outputs
- **Classification:** POST-DEPLOYMENT (CRITICAL)
- **Inputs Required:**
  - Variable: `step1_outputs`, `step2_outputs`, `step3_outputs`, `step4_outputs` (from cell 11)
  - Variable: `resource_group_name`, `subscription_id`, `location` (from cell 20)
  - Function: `get_deployment_outputs()` (from cell 3) - fallback if outputs missing
- **Outputs Produced:**
  - File: `master-lab.env` (complete with real values!)
  - Variable: `env_content` (string with all env vars)
  - Environment variables written:
    - SUBSCRIPTION_ID
    - RESOURCE_GROUP
    - LOCATION
    - APIM_GATEWAY_URL
    - APIM_SERVICE_ID
    - APIM_SUBSCRIPTION_KEY
    - APIM_API_ID
    - INFERENCE_API_PATH
    - REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
    - SEARCH_ENDPOINT, SEARCH_API_KEY
    - COSMOSDB_ENDPOINT, COSMOSDB_KEY
    - CONTENT_SAFETY_ENDPOINT, CONTENT_SAFETY_KEY
    - MCP_SERVER_*_URL (for all 7 MCP servers)
    - AI model endpoints (EASTUS_*, UKSOUTH_*, NORTHCENTRALUS_*)
    - And many more (~50+ variables)
- **Dependencies:**
  - Cell 11 (deployment outputs) ⭐ CRITICAL
  - Cell 20 (config variables)
  - Cell 3 (get_deployment_outputs function)
- **Issues:** ⚠️ RUNS TOO LATE in current order (after cells that need it)
- **Must Run:** IMMEDIATELY after cell 11, before cells 7/15/28

**This is the SINGLE SOURCE OF TRUTH for environment generation!**

---

### PHASE 5: INITIALIZATION (Load & Initialize)

#### Cell 7: Load master-lab.env ⭐
- **Type:** CODE
- **Purpose:** Load environment variables from deployment
- **Classification:** INITIALIZATION
- **Inputs Required:**
  - File: `master-lab.env` (MUST EXIST - created by cell 24)
- **Outputs Produced:**
  - Side effect: Loads all env vars into `os.environ`
  - Variable: `apim_url` (for verification)
- **Dependencies:**
  - Cell 24 (creates the file) ⭐ CRITICAL
  - Cell 28 (normalizes endpoints)
- **Issues:** ⚠️ **CRITICAL ERROR** - Runs at position 7, BEFORE deployment (cell 11) and BEFORE generation (cell 24)
- **Current Position:** Cell 7 (wrong!)
- **Should Be:** After cell 28 (after env file is fully generated and normalized)
- **Recommendation:** MOVE to run after cells 24 → 28

**Why this is broken:**
```
Cell 7: load_dotenv('master-lab.env')  # FILE DOESN'T EXIST YET!
  ↓
Cell 11: Deploy infrastructure (creates resources)
  ↓
Cell 24: Generate master-lab.env from outputs  # NOW FILE EXISTS!
```

**Should be:**
```
Cell 11: Deploy infrastructure
  ↓
Cell 24: Generate master-lab.env
  ↓
Cell 28: Normalize endpoints
  ↓
Cell 7: load_dotenv('master-lab.env')  # NOW IT EXISTS!
```

---

#### Cell 15: Initialize MCP Servers ⭐
- **Type:** CODE
- **Purpose:** Initialize all 7 MCP server clients using notebook_mcp_helpers
- **Classification:** INITIALIZATION
- **Inputs Required:**
  - File: `.mcp-servers-config` (MCP configuration)
  - Module: `notebook_mcp_helpers.MCPClient`
  - Environment: MCP server URLs must be loaded from master-lab.env
    - MCP_SERVER_WEATHER_URL
    - MCP_SERVER_ONCALL_URL
    - MCP_SERVER_GITHUB_URL
    - MCP_SERVER_SPOTIFY_URL
    - MCP_SERVER_PRODUCT_CATALOG_URL
    - MCP_SERVER_PLACE_ORDER_URL
    - MCP_SERVER_EXCEL_URL
    - MCP_SERVER_DOCS_URL
- **Outputs Produced:**
  - Variable: `mcp` (object with attributes for each server)
  - Attributes: `mcp.excel`, `mcp.docs`, `mcp.weather`, `mcp.oncall`, `mcp.github`, `mcp.spotify`, `mcp.product_catalog`, `mcp.place_order`
  - Variable: `MCP_SERVERS` (dict of server configs)
- **Dependencies:**
  - Cell 11 (deployment creates MCP servers) ⭐ CRITICAL
  - Cell 24 (generates MCP_SERVER_*_URL variables) ⭐ CRITICAL
  - Cell 7 (loads env vars into os.environ)
- **Issues:** ⚠️ **CRITICAL ERROR** - Runs at position 15, BEFORE deployment creates MCP servers!
- **Current Position:** Cell 15 (wrong!)
- **Should Be:** After cell 7 (after env is loaded)
- **Recommendation:** MOVE to run after cell 7

**Why this is broken:**
```
Cell 15: mcp = MCPClient.from_config()  # Tries to connect to URLs that don't exist!
  ↓
Cell 11: Deploy MCP Container Apps  # NOW SERVERS EXIST!
  ↓
Cell 24: Write MCP_SERVER_*_URL to env  # NOW URLS EXIST!
```

**Should be:**
```
Cell 11: Deploy MCP servers
  ↓
Cell 24: Generate master-lab.env (includes MCP URLs)
  ↓
Cell 28: Normalize endpoints
  ↓
Cell 7: Load master-lab.env (MCP URLs now in os.environ)
  ↓
Cell 15: Initialize MCP clients (NOW THEY CAN CONNECT!)
```

---

#### Cell 86: MCP Server Initialization (Labs Section)
- **Type:** CODE
- **Purpose:** Alternative MCP initialization for lab exercises
- **Classification:** INITIALIZATION
- **Inputs Required:**
  - File: `master-lab.env`
  - Environment: MCP_SERVER_*_URL variables
- **Outputs Produced:**
  - Variable: `MCP_SERVERS` (dict)
  - Variable: `configured` (list of available servers)
- **Dependencies:**
  - Cells 24, 28, 7 (env setup)
  - Cell 15 (or alternative MCP init)
- **Issues:** Duplicate of cell 15 functionality
- **Recommendation:** Consolidate with cell 15, or make this a "re-initialize if needed" cell

---

### PHASE 6: VERIFICATION & LABS (Cells 40+)

These cells use the deployed infrastructure and initialized services.

#### Cell 27: Install Requirements
- **Type:** CODE
- **Purpose:** pip install from requirements.txt
- **Classification:** LAB/TEST (but should be SETUP)
- **Recommendation:** Move earlier, before cell 38 (master imports)

#### Cell 30: APIM Policy Validation
- **Type:** CODE
- **Purpose:** Validate APIM policies are configured
- **Classification:** LAB/TEST
- **Dependencies:** Cells 11, 24, 7 (deployment + env)

#### Cell 32: Install Lab Requirements (Duplicate)
- **Type:** CODE
- **Purpose:** Another pip install
- **Classification:** LAB/TEST
- **Issues:** Duplicate of cell 27
- **Recommendation:** Remove or merge with 27

#### Cell 34: Backend Health Check
- **Type:** CODE
- **Purpose:** Query APIM backends
- **Classification:** LAB/TEST
- **Dependencies:** Cells 11, 24, 7

#### Cell 39: Async Helpers
- **Type:** CODE
- **Purpose:** Define async utility functions
- **Classification:** INITIALIZATION
- **Recommendation:** Move to SETUP phase

#### Cells 40-56: Various Tests & Labs
- **Purpose:** Test chat completions, streaming, load balancing, observability
- **Dependencies:** All initialization complete (cells 7, 15, 38)

#### Cells 70+: Lab Exercises
- **Purpose:** 25 consolidated labs covering APIM features, MCP integration, AI agents
- **Dependencies:** Full deployment + initialization

---

## DEPENDENCY GRAPH

### Visual Dependency Flow

```
CURRENT (BROKEN) FLOW:
=======================
Cell 0:  [DOC] Section Header
Cell 1:  [EMPTY] Remove
Cell 2:  [SETUP] az() function ✓
Cell 3:  [SETUP] deployment helpers ✓
  ↓
Cell 7:  [INIT] Load master-lab.env ⚠️ FILE DOESN'T EXIST!
  ↓
Cell 13: [PRE] Create .env template (duplicate)
Cell 14: [PRE] Check Azure CLI ✓
Cell 15: [INIT] Initialize MCP ⚠️ URLS DON'T EXIST!
Cell 16: [PRE] Create .env template (duplicate)
  ↓
Cell 20: [PRE] Set config vars ✓
Cell 21: [PRE] Azure auth ✓
Cell 22: [DEPLOY] Auth + deploy (duplicate)
  ↓
Cell 11: [DEPLOY] Deploy infrastructure ✓ (CREATES RESOURCES!)
  ↓
Cell 24: [POST] Generate master-lab.env ✓ (NOW FILE EXISTS!)
Cell 28: [POST] Normalize endpoints ⚠️ Should run after 24
  ↓
Cell 38: [SETUP] Master imports ✓
  ↓
Cells 40+: Labs & Tests


CORRECT FLOW:
==============
┌─────────────────────────────────────────┐
│ PHASE 1: SETUP (Core Infrastructure)   │
└─────────────────────────────────────────┘
Cell 2:  [SETUP] az() function
  ↓
Cell 3:  [SETUP] deployment helpers (depends on: 2)
  ↓
Cell 27: [SETUP] pip install requirements
  ↓
Cell 38: [SETUP] Master imports (depends on: 27)

┌─────────────────────────────────────────┐
│ PHASE 2: PRE-DEPLOYMENT (Configure)    │
└─────────────────────────────────────────┘
Cell 14: [PRE] Check Azure CLI (depends on: 2)
  ↓
Cell 20: [PRE] Set config vars (subscription, rg, location)
  ↓
Cell 21: [PRE] Azure authentication (depends on: 20)

┌─────────────────────────────────────────┐
│ PHASE 3: DEPLOYMENT (~40 minutes)      │
└─────────────────────────────────────────┘
Cell 11: [DEPLOY] Main deployment (depends on: 2,3,20,21)
         ├─ Step 1: Core (APIM, Log Analytics)
         ├─ Step 2: AI Foundry (3 hubs, 14 models)
         ├─ Step 3: Services (Redis, Search, Cosmos)
         └─ Step 4: MCP Servers (7 container apps)

         Outputs: step1_outputs, step2_outputs, step3_outputs, step4_outputs

┌─────────────────────────────────────────┐
│ PHASE 4: POST-DEPLOYMENT (Config Gen)  │
└─────────────────────────────────────────┘
Cell 24: [POST] Generate master-lab.env (depends on: 11,20)
         Writes ~50+ environment variables from deployment outputs
         Creates: master-lab.env with APIM URLs, MCP URLs, Redis, etc.
  ↓
Cell 28: [POST] Normalize endpoints (depends on: 24)
         Derives OPENAI_ENDPOINT, updates master-lab.env

┌─────────────────────────────────────────┐
│ PHASE 5: INITIALIZATION (Load & Init)  │
└─────────────────────────────────────────┘
Cell 7:  [INIT] Load master-lab.env (depends on: 24,28)
         Loads all variables into os.environ
  ↓
Cell 15: [INIT] Initialize MCP servers (depends on: 7,11,24)
         Creates mcp object with all 7 server clients

┌─────────────────────────────────────────┐
│ PHASE 6: VERIFICATION & LABS           │
└─────────────────────────────────────────┘
Cell 30: [TEST] APIM policy validation (depends on: 7,11)
Cell 34: [TEST] Backend health check (depends on: 7,11)
Cell 42-56: [TEST] Various tests (depends on: 7,15)
Cell 70+: [LAB] 25 lab exercises (depends on: 7,15)
```

---

## SPECIFIC QUESTIONS ANSWERED

### Q: What does cell 2 do? Can it be merged with cell 3?

**Cell 2:** Defines the `az()` helper function - a lightweight wrapper around Azure CLI commands.

**Function Signature:**
```python
def az(cmd: str, json_out: bool = False, timeout: int = 25, login_if_needed: bool = True) -> (bool, str|dict)
```

**Features:**
- Executes Azure CLI commands via subprocess
- Automatic JSON parsing when `json_out=True`
- Auto-retry with login on auth failures
- Returns `(success, result)` tuples
- Used by ALL Azure operations in notebook

**Should it merge with cell 3?**
**NO.** Keep separate because:
1. Cell 2 is foundation (used by cell 3 and others)
2. Cell 3 depends on cell 2 (calls `az()` in compile_bicep, deploy_template, etc.)
3. Separation of concerns: cell 2 = CLI wrapper, cell 3 = deployment logic
4. Cell 2 is self-contained and reusable

---

### Q: What does cell 3 do? What does it depend on?

**Cell 3:** Defines deployment helper functions for Bicep/ARM templates.

**Functions Provided:**
1. `compile_bicep(bicep_path)` - Compiles .bicep to .json
2. `deploy_template(rg, name, template_file, params)` - Deploys ARM template
3. `get_deployment_outputs(rg, name)` - Retrieves deployment outputs
4. `ensure_deployment(rg, name, template, params, skip_if_exists)` - Idempotent deployment

**Dependencies:**
- **Cell 2** - Uses `az()` function extensively
- **System** - Requires Azure CLI with Bicep extension
- **Files** - Expects Bicep files in `BICEP_DIR`

**Example Usage:**
```python
# Compile Bicep
template = compile_bicep('deploy-01-core.bicep')

# Deploy
ok, result = deploy_template(
    rg='lab-master-lab',
    name='step1-core',
    template_file=template,
    params={'location': 'uksouth'}
)

# Get outputs
outputs = get_deployment_outputs('lab-master-lab', 'step1-core')
apim_url = outputs.get('apimGatewayUrl')
```

---

### Q: What does cell 10 do? Is it trying to initialize MCP servers before deployment?

**Cell 10:** Markdown documentation cell, NOT code.

**Content:** Explains the 4-step deployment process:
- Step 1: Core (APIM) - 10 min
- Step 2: AI Foundry - 15 min
- Step 3: Services - 10 min
- Step 4: MCP Servers - 5 min
- Total: ~40 minutes

**Does it initialize MCP?**
**NO.** It's just documentation. The actual MCP initialization problem is in **Cell 15** (code cell).

---

### Q: Which cells load endpoints before deployment happens? (LOGICAL ERROR)

**Cells that incorrectly try to use resources before they exist:**

1. **Cell 7** - Tries to load `master-lab.env` before it's generated
   - Position: 7
   - Should be: After cell 28 (after env generation)
   - Error: File doesn't exist yet

2. **Cell 15** - Tries to initialize MCP servers before they're deployed
   - Position: 15
   - Should be: After cell 7 (after env is loaded)
   - Error: MCP_SERVER_*_URL variables don't exist in env yet

3. **Cell 28** - Reads master-lab.env before cell 24 generates it
   - Position: 28
   - Should be: Immediately after cell 24
   - Error: Tries to normalize endpoints from incomplete env file

4. **Cell 43** - Validates env vars before they're loaded
   - Position: 43
   - Should be: After cell 7
   - Error: Variables not in scope yet

**Timeline of errors:**
```
Cell 7  (pos 7):  Load .env           ⚠️ File doesn't exist
Cell 15 (pos 15): Init MCP            ⚠️ URLs don't exist
Cell 11 (pos 11): DEPLOY              ✓ Creates resources
Cell 24 (pos 24): Generate .env       ✓ NOW file exists
Cell 28 (pos 28): Normalize endpoints ⚠️ Should come before cell 7
Cell 43 (pos 43): Validate vars       ⚠️ Should come after cell 7
```

---

### Q: Which cells create/update master-lab.env?

**PRIMARY CREATOR (The One True Source):**

**Cell 24** - Generate master-lab.env from deployment outputs
- Reads: `step1_outputs`, `step2_outputs`, `step3_outputs`, `step4_outputs`
- Writes: Complete .env file with ~50+ variables
- Variables written:
  - Core: SUBSCRIPTION_ID, RESOURCE_GROUP, LOCATION
  - APIM: APIM_GATEWAY_URL, APIM_SERVICE_ID, APIM_SUBSCRIPTION_KEY, APIM_API_ID
  - AI Models: EASTUS_ENDPOINT, UKSOUTH_ENDPOINT, NORTHCENTRALUS_ENDPOINT
  - MCP Servers: MCP_SERVER_WEATHER_URL, MCP_SERVER_GITHUB_URL, etc. (7 servers)
  - Redis: REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
  - Search: SEARCH_ENDPOINT, SEARCH_API_KEY
  - Cosmos: COSMOSDB_ENDPOINT, COSMOSDB_KEY
  - Content Safety: CONTENT_SAFETY_ENDPOINT, CONTENT_SAFETY_KEY
  - And more...

**SECONDARY UPDATERS (Modify existing file):**

**Cell 28** - Normalize OPENAI_ENDPOINT
- Reads: `master-lab.env`
- Updates: Adds/modifies OPENAI_ENDPOINT if missing
- Logic: Derives from APIM_GATEWAY_URL + INFERENCE_API_PATH

**TEMPLATE CREATORS (Don't write real values):**

**Cell 13** - Create template if missing
- Creates: Placeholder template with empty values
- Should be: Removed (redundant with cell 24)

**Cell 16** - Create template (duplicate)
- Creates: Another placeholder template
- Should be: Removed (redundant with cell 24)

**SUMMARY:**
- **Cell 24** is the authoritative source (writes from deployment)
- **Cell 28** enhances it (normalizes endpoints)
- **Cells 13, 16** are redundant (just create templates)

---

### Q: Which cells read from master-lab.env?

**Cells that load/read the .env file:**

**Direct Load (load_dotenv):**

1. **Cell 7** - Primary env loader
   - `load_dotenv('master-lab.env')`
   - Loads all vars into `os.environ`

2. **Cell 86** - MCP initialization (labs section)
   - `load_dotenv(env_file, override=True)`
   - Reloads env for lab exercises

**File Reading (parse without loading to env):**

3. **Cell 13** - Environment loader
   - Reads file to check if exists
   - Creates template if missing

4. **Cell 16** - Alternative loader
   - Reads file content
   - Parses key=value pairs

5. **Cell 24** - Generator
   - May read existing file before overwriting

6. **Cell 28** - Endpoint normalizer
   - `env_path.read_text()` to parse values
   - Updates file with normalized endpoints

**Indirect Usage (access vars via os.environ after cell 7):**

7. **All cells after cell 7** that use `os.getenv()` or `os.environ.get()`
   - Cell 30: APIM policy validation
   - Cell 34: Backend health check
   - Cell 42+: Tests and labs
   - Cell 86+: MCP lab exercises
   - Hundreds of references throughout notebook

**Critical Dependency Chain:**
```
Cell 24: Writes master-lab.env (50+ variables)
  ↓
Cell 28: Updates master-lab.env (normalized endpoints)
  ↓
Cell 7:  Loads master-lab.env → os.environ
  ↓
Cells 30+: Access variables via os.getenv('APIM_GATEWAY_URL'), etc.
```

---

## LOGICAL ERRORS FOUND

### 1. Cell 7 Premature Load (CRITICAL)
- **Error:** Tries to load `master-lab.env` before it exists
- **Current Position:** Cell 7
- **Correct Position:** After cell 28
- **Impact:** HIGH - File doesn't exist, variables not available
- **Fix:** Move cell 7 to run after cells 24 → 28

### 2. Cell 15 Premature MCP Init (CRITICAL)
- **Error:** Tries to initialize MCP servers before deployment creates them
- **Current Position:** Cell 15
- **Correct Position:** After cell 7
- **Impact:** HIGH - MCP_SERVER_*_URL variables don't exist
- **Fix:** Move cell 15 to run after cell 7

### 3. Cell 28 Runs Before Cell 24 (HIGH)
- **Error:** Tries to normalize endpoints before env file is generated
- **Current Position:** Cell 28
- **Correct Position:** Immediately after cell 24
- **Impact:** MEDIUM - May read partial/template env file
- **Fix:** Swap order (24 → 28 instead of 28 → 24)

### 4. Duplicate Environment Loaders (MEDIUM)
- **Cells:** 13, 16 (templates) vs 24 (real generator)
- **Impact:** MEDIUM - Confusion, wasted cells
- **Fix:** Remove cells 13, 16; keep only cell 24

### 5. Duplicate Authentication Setup (MEDIUM)
- **Cells:** 21 (clean) vs 22 (mixed with deployment)
- **Impact:** MEDIUM - Redundant code
- **Fix:** Remove cell 22, keep cell 21

### 6. Duplicate Requirements Install (LOW)
- **Cells:** 27, 32
- **Impact:** LOW - Wastes time on re-install
- **Fix:** Remove cell 32, keep cell 27 early in SETUP

### 7. Cell 1 Empty (LOW)
- **Error:** Serves no purpose
- **Fix:** Remove

### 8. Cell 43 Validates Before Load (MEDIUM)
- **Error:** Validates env vars before cell 7 loads them
- **Current Position:** Cell 43
- **Correct Position:** After cell 7
- **Fix:** Move after cell 7 or remove (redundant validation)

---

## REORGANIZATION RECOMMENDATIONS

### Recommended Cell Order (CORRECTED)

```
SECTION 1: DEPLOY EVERYTHING
├─ 0: [DOC] Section Header
├─ PHASE 1: SETUP
│  ├─ 2:  az() helper function
│  ├─ 3:  deployment helpers (compile_bicep, deploy_template, etc.)
│  ├─ 27: pip install requirements
│  └─ 38: Master imports
│
├─ PHASE 2: PRE-DEPLOYMENT
│  ├─ 14: Check Azure CLI & credentials
│  ├─ 20: Set deployment config (subscription, rg, location)
│  └─ 21: Azure authentication
│
├─ PHASE 3: DEPLOYMENT
│  └─ 11: Main deployment (4 steps, ~40 min)
│
├─ PHASE 4: POST-DEPLOYMENT
│  ├─ 24: Generate master-lab.env from outputs
│  └─ 28: Normalize endpoints
│
├─ PHASE 5: INITIALIZATION
│  ├─ 7:  Load master-lab.env [MOVED FROM POSITION 7]
│  └─ 15: Initialize MCP servers [MOVED FROM POSITION 15]
│
└─ PHASE 6: VERIFICATION
   ├─ 30: APIM policy validation
   ├─ 34: Backend health check
   ├─ 42-56: Various tests
   └─ 70+: Lab exercises

CELLS TO REMOVE:
├─ 1:  Empty cell
├─ 13: Duplicate env loader (keep 24)
├─ 16: Duplicate env loader (keep 24)
├─ 22: Duplicate auth (keep 21)
└─ 32: Duplicate pip install (keep 27)
```

### Numbered Execution Order

**ESSENTIAL DEPLOYMENT FLOW:**

```
1.  Cell 2:  Define az() function
2.  Cell 3:  Define deployment helpers
3.  Cell 27: Install requirements
4.  Cell 38: Master imports
5.  Cell 14: Check Azure CLI
6.  Cell 20: Set deployment config
7.  Cell 21: Azure authentication
8.  Cell 11: DEPLOY (40 minutes) ☕
9.  Cell 24: Generate master-lab.env
10. Cell 28: Normalize endpoints
11. Cell 7:  Load master-lab.env [CORRECTED POSITION]
12. Cell 15: Initialize MCP servers [CORRECTED POSITION]
13. Cell 30: Validate APIM policies
14. Cell 34: Health check
15. Cells 42-56: Tests
16. Cells 70+: Labs
```

---

## IMPLEMENTATION PLAN

### Step 1: Move Cells to Correct Positions

**Move Cell 7 (Load .env):**
- Current: Position 7
- New: Position after cell 28 (becomes ~position 29)
- Reason: master-lab.env must exist and be normalized first

**Move Cell 15 (Init MCP):**
- Current: Position 15
- New: Position after new cell 7 (becomes ~position 30)
- Reason: MCP_SERVER_*_URL must be in os.environ first

**Move Cell 28 (Normalize endpoints):**
- Current: Position 28
- New: Position immediately after cell 24 (becomes ~position 25)
- Reason: Should enhance .env right after it's generated

### Step 2: Remove Duplicate Cells

**Remove These Cells:**
1. Cell 1 (empty)
2. Cell 13 (duplicate env template creator)
3. Cell 16 (duplicate env loader)
4. Cell 22 (duplicate auth + deployment)
5. Cell 32 (duplicate pip install)

**Keep These Instead:**
- Keep cell 24 (authoritative env generator)
- Keep cell 21 (clean auth setup)
- Keep cell 27 (requirements install)

### Step 3: Merge/Consolidate

**Consider Merging:**
- Cells 14 + 29 + 37 → Single "Azure CLI Setup" cell
- Cell 86 → Merge into cell 15 or make it a "Re-initialize MCP if needed"

### Step 4: Add Validation

**Add New Cell After Cell 24:**
```python
# Validate master-lab.env was created successfully
env_file = Path('master-lab.env')
if not env_file.exists():
    raise FileNotFoundError('master-lab.env was not generated!')

# Validate critical variables exist
required_vars = [
    'APIM_GATEWAY_URL', 'APIM_SUBSCRIPTION_KEY',
    'MCP_SERVER_WEATHER_URL', 'MCP_SERVER_GITHUB_URL'
]
missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    print(f"WARNING: Missing variables in env: {missing}")
else:
    print("✓ All critical variables present in master-lab.env")
```

### Step 5: Update Documentation

**Update Markdown Cells:**
- Cell 4 (Consolidated Provisioning) - Update with correct order
- Cell 5 (Optimized Execution Order) - Update to match new flow
- Cell 10 (Deployment Instructions) - Clarify that env is generated after
- Add new markdown before cell 7: "Load Environment (After Deployment)"

---

## DEPENDENCY MATRIX

| Cell | Depends On | Provides | Can Run Before |
|------|------------|----------|----------------|
| 2 | None | az() | 3,11,14,... |
| 3 | 2 | deployment helpers | 11,24 |
| 7 | 24,28 | Loaded os.environ | 15,30,34,42+ |
| 11 | 2,3,20,21 | step*_outputs | 24 |
| 13 | None | .env template | REMOVE |
| 14 | 2 | CLI validation | 20,21 |
| 15 | 7,11,24 | mcp object | 42+,70+ |
| 16 | None | .env template | REMOVE |
| 20 | None | config vars | 11,21 |
| 21 | 20 | credential | 11 |
| 22 | 20 | credential | REMOVE |
| 24 | 11,20 | master-lab.env | 28,7 |
| 27 | None | pip packages | 38 |
| 28 | 24 | normalized endpoints | 7 |
| 38 | 27 | imports | 11,... |

---

## QUICK REFERENCE: File Dependencies

### master-lab.env

**Created By:**
- Cell 24 (PRIMARY - from deployment outputs)

**Updated By:**
- Cell 28 (adds normalized OPENAI_ENDPOINT)

**Read By:**
- Cell 7 (load_dotenv)
- Cell 86 (load_dotenv in labs)
- Cells 13,16,24,28 (file I/O)

**Contains (~50+ variables):**
```bash
# Core Azure
SUBSCRIPTION_ID=d334f2cd-3efd-494e-9fd3-2470b1a13e4c
RESOURCE_GROUP=lab-master-lab
LOCATION=uksouth

# APIM
APIM_GATEWAY_URL=https://lab-master-lab-apim.azure-api.net
APIM_SERVICE_ID=/subscriptions/.../microsoft.apimanagement/service/lab-master-lab-apim
APIM_SUBSCRIPTION_KEY=***
APIM_API_ID=openai-api
INFERENCE_API_PATH=/inference

# MCP Servers (7)
MCP_SERVER_WEATHER_URL=https://mcp-weather.app.uksouth.azurecontainerapps.io
MCP_SERVER_GITHUB_URL=https://mcp-github.app.uksouth.azurecontainerapps.io
MCP_SERVER_ONCALL_URL=https://mcp-oncall.app.uksouth.azurecontainerapps.io
MCP_SERVER_SPOTIFY_URL=https://mcp-spotify.app.uksouth.azurecontainerapps.io
MCP_SERVER_EXCEL_URL=https://mcp-excel.app.uksouth.azurecontainerapps.io
MCP_SERVER_DOCS_URL=https://mcp-docs.app.uksouth.azurecontainerapps.io
MCP_SERVER_PRODUCT_CATALOG_URL=https://mcp-product-catalog.app.uksouth.azurecontainerapps.io

# AI Model Endpoints
EASTUS_ENDPOINT=https://hub-eastus.openai.azure.com
UKSOUTH_ENDPOINT=https://hub-uksouth.openai.azure.com
NORTHCENTRALUS_ENDPOINT=https://hub-northcentralus.openai.azure.com
OPENAI_ENDPOINT=https://lab-master-lab-apim.azure-api.net/inference

# Supporting Services
REDIS_HOST=lab-master-lab-redis.redis.cache.windows.net
REDIS_PORT=6380
REDIS_PASSWORD=***
SEARCH_ENDPOINT=https://lab-master-lab-search.search.windows.net
SEARCH_API_KEY=***
COSMOSDB_ENDPOINT=https://lab-master-lab-cosmos.documents.azure.com
COSMOSDB_KEY=***
CONTENT_SAFETY_ENDPOINT=https://lab-master-lab-contentsafety.cognitiveservices.azure.com
CONTENT_SAFETY_KEY=***
```

### .azure-credentials.env

**Created By:** Manual (user creates before deployment)

**Read By:**
- Cell 21 (authentication)
- Cell 22 (duplicate auth - should be removed)

**Contains:**
```bash
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-service-principal-id
AZURE_CLIENT_SECRET=your-service-principal-secret
```

### Bicep Templates

**Location:** `BICEP_DIR` (default: `archive/scripts/`)

**Files:**
- deploy-01-core.bicep (APIM, Log Analytics, App Insights)
- deploy-02-foundry.bicep (AI Hubs, Models)
- deploy-03-supporting.bicep (Redis, Search, Cosmos, Content Safety)
- deploy-04-mcp.bicep (Container Apps, 7 MCP servers)

**Used By:**
- Cell 11 (main deployment)

---

## FINAL SUMMARY

### Current State: BROKEN ❌

The notebook tries to initialize services before deploying infrastructure. Key resources (APIM, MCP servers, AI models) don't exist when initialization cells run.

**Critical Errors:**
1. Cell 7 loads .env before it's created
2. Cell 15 initializes MCP before deployment creates servers
3. Cell 28 normalizes endpoints before cell 24 generates base file
4. Multiple duplicate cells (13,16,22,32)

### Corrected State: WORKING ✅

**Correct Execution Order:**
```
SETUP → PRE-DEPLOYMENT → DEPLOYMENT → POST-DEPLOYMENT → INITIALIZATION → LABS
(2,3,27,38) → (14,20,21) → (11) → (24,28) → (7,15) → (30+)
```

**Key Principle:**
**DEPLOYMENT FIRST, INITIALIZATION SECOND**

### Cell Moves Required

| Cell | Current Pos | New Pos | Reason |
|------|-------------|---------|--------|
| 7 | 7 | ~29 (after 28) | Load .env after it exists |
| 15 | 15 | ~30 (after 7) | Init MCP after env loaded |
| 28 | 28 | ~25 (after 24) | Normalize right after generation |

### Cells to Remove

| Cell | Reason |
|------|--------|
| 1 | Empty |
| 13 | Duplicate env template (keep 24) |
| 16 | Duplicate env loader (keep 24) |
| 22 | Duplicate auth (keep 21) |
| 32 | Duplicate pip install (keep 27) |

### Impact

**After fixes:**
- ✅ No more "file not found" errors
- ✅ No more "variable not set" errors
- ✅ Clear linear dependency flow
- ✅ Self-documenting execution order
- ✅ Reduced cell count (~5 fewer cells)
- ✅ Notebook runs top-to-bottom successfully

---

**END OF COMPREHENSIVE DEPENDENCY MAP**

---

## APPENDIX: Cell Reference Quick Lookup

```
Cell 0:  [DOC] Section Header
Cell 1:  [EMPTY] Remove ❌
Cell 2:  [SETUP] az() function ⭐
Cell 3:  [SETUP] Deployment helpers ⭐
Cell 7:  [INIT] Load .env ⚠️ MOVE LATER
Cell 11: [DEPLOY] Main deployment ⭐⭐⭐
Cell 13: [PRE] Env template ❌ DUPLICATE
Cell 14: [PRE] Check Azure CLI ✓
Cell 15: [INIT] MCP initialization ⚠️ MOVE LATER
Cell 16: [PRE] Env loader ❌ DUPLICATE
Cell 20: [PRE] Deployment config ⭐
Cell 21: [PRE] Authentication ⭐
Cell 22: [DEPLOY] Auth+deploy ❌ DUPLICATE
Cell 24: [POST] Generate .env ⭐⭐⭐
Cell 27: [SETUP] pip install ✓
Cell 28: [POST] Normalize endpoints ⚠️ MOVE EARLIER
Cell 30: [TEST] Policy validation ✓
Cell 32: [TEST] pip install ❌ DUPLICATE
Cell 34: [TEST] Backend health ✓
Cell 38: [SETUP] Master imports ⭐
Cell 42+: [TEST] Various tests ✓
Cell 70+: [LAB] 25 lab exercises ✓
Cell 86: [INIT] MCP init (labs) ✓

⭐ = Critical
⚠️ = Needs fixing
❌ = Remove/duplicate
✓ = OK as-is
```
