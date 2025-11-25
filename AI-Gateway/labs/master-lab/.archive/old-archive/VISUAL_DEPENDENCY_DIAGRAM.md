# VISUAL DEPENDENCY DIAGRAM
## Master AI Gateway Notebook - Execution Flow

---

## CURRENT STATE (BROKEN) ❌

```
┌──────────────────────────────────────────────────────────────────┐
│                    SECTION 1: DEPLOY EVERYTHING                  │
└──────────────────────────────────────────────────────────────────┘
    │
    ├─► Cell 2: az() function ✓
    │       │
    │       └─► Used by: cells 3, 11, 14, 29, etc.
    │
    ├─► Cell 3: Deployment helpers ✓
    │       │
    │       └─► Defines: compile_bicep(), deploy_template(), get_deployment_outputs()
    │
    ├─► Cell 7: Load master-lab.env ⚠️ BROKEN!
    │       │
    │       └─► 💥 ERROR: File doesn't exist yet!
    │           master-lab.env is created by Cell 24 (which runs LATER)
    │
    ├─► Cell 13: Create .env template (duplicate) ❌
    │
    ├─► Cell 14: Check Azure CLI ✓
    │
    ├─► Cell 15: Initialize MCP servers ⚠️ BROKEN!
    │       │
    │       └─► 💥 ERROR: MCP_SERVER_*_URL variables don't exist!
    │           These URLs are written by Cell 24 (which runs LATER)
    │           And loaded by Cell 7 (which failed above)
    │
    ├─► Cell 16: Create .env template (duplicate) ❌
    │
    ├─► Cell 20: Set deployment config ✓
    │       │
    │       └─► Defines: subscription_id, resource_group_name, location
    │
    ├─► Cell 21: Azure authentication ✓
    │       │
    │       └─► Creates: credential, resource_client
    │
    ├─► Cell 22: Auth + deployment (duplicate) ❌
    │
    ├─► Cell 11: MAIN DEPLOYMENT (~40 min) ✓
    │       │
    │       │   Requires:
    │       │   ├─ Cell 2: az() function
    │       │   ├─ Cell 3: deployment helpers
    │       │   ├─ Cell 20: config variables
    │       │   └─ Cell 21: credential
    │       │
    │       │   Deploys:
    │       │   ├─ Step 1: APIM, Log Analytics, App Insights
    │       │   ├─ Step 2: 3 AI Hubs, 14 Models
    │       │   ├─ Step 3: Redis, Search, Cosmos, Content Safety
    │       │   └─ Step 4: 7 MCP Servers (Container Apps)
    │       │
    │       └─► Creates:
    │           ├─ step1_outputs (APIM URLs, keys)
    │           ├─ step2_outputs (AI model endpoints)
    │           ├─ step3_outputs (Redis, Search, Cosmos, Content Safety)
    │           └─ step4_outputs (MCP server URLs)
    │
    ├─► Cell 24: Generate master-lab.env ✓
    │       │
    │       │   Reads:
    │       │   ├─ step1_outputs (from Cell 11)
    │       │   ├─ step2_outputs (from Cell 11)
    │       │   ├─ step3_outputs (from Cell 11)
    │       │   ├─ step4_outputs (from Cell 11)
    │       │   ├─ subscription_id (from Cell 20)
    │       │   ├─ resource_group_name (from Cell 20)
    │       │   └─ location (from Cell 20)
    │       │
    │       └─► Writes master-lab.env:
    │           ├─ APIM_GATEWAY_URL
    │           ├─ APIM_SUBSCRIPTION_KEY
    │           ├─ MCP_SERVER_WEATHER_URL
    │           ├─ MCP_SERVER_GITHUB_URL
    │           ├─ MCP_SERVER_ONCALL_URL
    │           ├─ MCP_SERVER_SPOTIFY_URL
    │           ├─ REDIS_HOST, REDIS_PASSWORD
    │           ├─ SEARCH_ENDPOINT, SEARCH_API_KEY
    │           └─ ~50+ more variables...
    │
    ├─► Cell 28: Normalize endpoints ⚠️ RUNS TOO EARLY
    │       │
    │       │   Should run immediately after Cell 24!
    │       │   Instead it's at position 28 (after Cell 24, but before Cell 7 loads it)
    │       │
    │       └─► Updates master-lab.env:
    │           └─ OPENAI_ENDPOINT (derived from APIM_GATEWAY_URL + INFERENCE_API_PATH)
    │
    └─► Cell 38: Master imports ✓

    ⬇️  PROBLEM: Cell 7 (load .env) ran at position 7, BEFORE Cell 24 created the file!
    ⬇️  PROBLEM: Cell 15 (init MCP) ran at position 15, BEFORE Cell 24 wrote the URLs!
    ⬇️  PROBLEM: Cell 28 (normalize) should run immediately after Cell 24, but before Cell 7!

┌──────────────────────────────────────────────────────────────────┐
│                    SECTION 2-6: LABS & TESTS                     │
└──────────────────────────────────────────────────────────────────┘
    │
    └─► Cells 40-248: All depend on successful initialization
            │
            └─► 💥 BROKEN because Cells 7 and 15 failed!
```

---

## CORRECTED STATE (WORKING) ✅

```
┌──────────────────────────────────────────────────────────────────┐
│                     PHASE 1: SETUP (Foundation)                  │
└──────────────────────────────────────────────────────────────────┘
    │
    ├─► Cell 2: az() function ⭐
    │       │
    │       │   def az(cmd, json_out=False, timeout=25, login_if_needed=True):
    │       │       """Execute Azure CLI commands with JSON parsing"""
    │       │
    │       └─► Used by: ALL Azure operations
    │
    ├─► Cell 3: Deployment helpers ⭐
    │       │
    │       │   def compile_bicep(bicep_path) -> json_template_path
    │       │   def deploy_template(rg, name, template, params) -> (ok, result)
    │       │   def get_deployment_outputs(rg, name) -> dict
    │       │   def ensure_deployment(rg, name, template, params, skip_if_exists)
    │       │
    │       └─► Used by: Cell 11 (deployment)
    │
    ├─► Cell 27: pip install requirements
    │       │
    │       └─► Installs: azure-*, openai, requests, pandas, etc.
    │
    └─► Cell 38: Master imports ⭐
            │
            └─► Imports: All Python dependencies for notebook

        ⬇️  Foundation ready! Now we can configure Azure...

┌──────────────────────────────────────────────────────────────────┐
│              PHASE 2: PRE-DEPLOYMENT (Configuration)             │
└──────────────────────────────────────────────────────────────────┘
    │
    ├─► Cell 14: Check Azure CLI ✓
    │       │
    │       └─► Validates: az --version, subscription access
    │
    ├─► Cell 20: Set deployment config ⭐
    │       │
    │       │   subscription_id = 'd334f2cd-...' or os.getenv('SUBSCRIPTION_ID')
    │       │   resource_group_name = 'lab-master-lab'
    │       │   location = 'uksouth'
    │       │   deployment_step1 = 'master-lab-step1-core'
    │       │   deployment_step2 = 'master-lab-step2-foundry'
    │       │   deployment_step3 = 'master-lab-step3-supporting'
    │       │   deployment_step4 = 'master-lab-step4-mcp'
    │       │
    │       └─► Provides: Core config for deployment
    │
    └─► Cell 21: Azure authentication ⭐
            │
            │   Option 1: Service Principal (from .azure-credentials.env)
            │       AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET
            │       → ClientSecretCredential
            │
            │   Option 2: Azure CLI (fallback)
            │       → AzureCliCredential
            │
            └─► Creates:
                ├─ credential (for Azure SDK)
                └─ resource_client (ResourceManagementClient)

        ⬇️  Azure configured! Now we can deploy...

┌──────────────────────────────────────────────────────────────────┐
│                 PHASE 3: DEPLOYMENT (~40 minutes)                │
└──────────────────────────────────────────────────────────────────┘
    │
    └─► Cell 11: MAIN DEPLOYMENT ⭐⭐⭐
            │
            │   Input Dependencies:
            │   ├─ Cell 2: az() function
            │   ├─ Cell 3: compile_bicep(), deploy_template(), get_deployment_outputs()
            │   ├─ Cell 20: subscription_id, resource_group_name, location
            │   ├─ Cell 21: credential, resource_client
            │   └─ Files: deploy-01-core.bicep, deploy-02-foundry.bicep, etc.
            │
            │   STEP 0: Ensure Resource Group
            │   ├─ Check if 'lab-master-lab' exists
            │   └─ Create if missing
            │
            │   STEP 1: Core Infrastructure (~10 min) ☕
            │   ├─ Compile: deploy-01-core.bicep → deploy-01-core.json
            │   ├─ Deploy:
            │   │   ├─ API Management (lab-master-lab-apim)
            │   │   ├─ Log Analytics Workspace
            │   │   └─ Application Insights
            │   └─ Output: step1_outputs = {
            │         apimGatewayUrl: "https://lab-master-lab-apim.azure-api.net"
            │         apimServiceId: "/subscriptions/.../microsoft.apimanagement/..."
            │         apimSubscriptionKey: "***"
            │         apiId: "openai-api"
            │       }
            │
            │   STEP 2: AI Foundry (~15 min) ☕☕☕
            │   ├─ Compile: deploy-02-foundry.bicep → deploy-02-foundry.json
            │   ├─ Deploy:
            │   │   ├─ AI Hub (East US) + Models (GPT-4, GPT-4o, embeddings)
            │   │   ├─ AI Hub (UK South) + Models (GPT-4, GPT-4o, embeddings, DALL-E)
            │   │   └─ AI Hub (North Central US) + Models (GPT-4, GPT-4o, embeddings)
            │   └─ Output: step2_outputs = {
            │         eastusEndpoint: "https://hub-eastus.openai.azure.com"
            │         uksouthEndpoint: "https://hub-uksouth.openai.azure.com"
            │         northcentralusEndpoint: "https://hub-northcentralus.openai.azure.com"
            │         modelDeployments: [...]
            │       }
            │
            │   STEP 3: Supporting Services (~10 min) ☕☕
            │   ├─ Compile: deploy-03-supporting.bicep → deploy-03-supporting.json
            │   ├─ Deploy:
            │   │   ├─ Redis Cache (Premium, 6GB)
            │   │   ├─ Azure AI Search (Standard)
            │   │   ├─ Cosmos DB (NoSQL)
            │   │   └─ Content Safety (Cognitive Service)
            │   └─ Output: step3_outputs = {
            │         redisHost: "lab-master-lab-redis.redis.cache.windows.net"
            │         redisPort: "6380"
            │         redisPassword: "***"
            │         searchEndpoint: "https://lab-master-lab-search.search.windows.net"
            │         searchApiKey: "***"
            │         cosmosdbEndpoint: "https://lab-master-lab-cosmos.documents.azure.com"
            │         cosmosdbKey: "***"
            │         contentSafetyEndpoint: "https://...cognitiveservices.azure.com"
            │         contentSafetyKey: "***"
            │       }
            │
            │   STEP 4: MCP Servers (~5 min) ☕
            │   ├─ Compile: deploy-04-mcp.bicep → deploy-04-mcp.json
            │   ├─ Deploy:
            │   │   ├─ Container Apps Environment
            │   │   ├─ MCP Weather Server (Container App)
            │   │   ├─ MCP GitHub Server (Container App)
            │   │   ├─ MCP OnCall Server (Container App)
            │   │   ├─ MCP Spotify Server (Container App)
            │   │   ├─ MCP Excel Server (Container App)
            │   │   ├─ MCP Docs Server (Container App)
            │   │   └─ MCP Product Catalog Server (Container App)
            │   └─ Output: step4_outputs = {
            │         mcpWeatherUrl: "https://mcp-weather.app.uksouth.azurecontainerapps.io"
            │         mcpGithubUrl: "https://mcp-github.app.uksouth.azurecontainerapps.io"
            │         mcpOncallUrl: "https://mcp-oncall.app.uksouth.azurecontainerapps.io"
            │         mcpSpotifyUrl: "https://mcp-spotify.app.uksouth.azurecontainerapps.io"
            │         mcpExcelUrl: "https://mcp-excel.app.uksouth.azurecontainerapps.io"
            │         mcpDocsUrl: "https://mcp-docs.app.uksouth.azurecontainerapps.io"
            │         mcpProductCatalogUrl: "https://mcp-product-catalog.app..."
            │       }
            │
            └─► DEPLOYMENT COMPLETE! (~40 min elapsed)
                │
                │   Created Resources:
                │   ├─ 1 Resource Group
                │   ├─ 1 API Management
                │   ├─ 1 Log Analytics + 1 App Insights
                │   ├─ 3 AI Hubs
                │   ├─ 14 AI Model Deployments
                │   ├─ 1 Redis Cache
                │   ├─ 1 Azure AI Search
                │   ├─ 1 Cosmos DB
                │   ├─ 1 Content Safety
                │   ├─ 1 Container Apps Environment
                │   └─ 7 MCP Container Apps
                │
                │   Total: ~32 Azure resources
                │
                │   Output Variables Available:
                │   ├─ step1_outputs (dict)
                │   ├─ step2_outputs (dict)
                │   ├─ step3_outputs (dict)
                │   └─ step4_outputs (dict)

        ⬇️  Deployment complete! Now generate configuration file...

┌──────────────────────────────────────────────────────────────────┐
│           PHASE 4: POST-DEPLOYMENT (Config Generation)           │
└──────────────────────────────────────────────────────────────────┘
    │
    ├─► Cell 24: Generate master-lab.env ⭐⭐⭐
    │       │
    │       │   Input Dependencies:
    │       │   ├─ step1_outputs (from Cell 11)
    │       │   ├─ step2_outputs (from Cell 11)
    │       │   ├─ step3_outputs (from Cell 11)
    │       │   ├─ step4_outputs (from Cell 11)
    │       │   ├─ subscription_id (from Cell 20)
    │       │   ├─ resource_group_name (from Cell 20)
    │       │   └─ location (from Cell 20)
    │       │
    │       │   Process:
    │       │   1. Extract values from deployment outputs
    │       │   2. Get APIM subscription key from APIM API
    │       │   3. Build env_content string with all variables
    │       │   4. Write to master-lab.env file
    │       │
    │       └─► Creates master-lab.env with ~50+ variables:
    │           │
    │           │   # Core Azure
    │           │   SUBSCRIPTION_ID=d334f2cd-3efd-494e-9fd3-2470b1a13e4c
    │           │   RESOURCE_GROUP=lab-master-lab
    │           │   LOCATION=uksouth
    │           │
    │           │   # APIM
    │           │   APIM_GATEWAY_URL=https://lab-master-lab-apim.azure-api.net
    │           │   APIM_SERVICE_ID=/subscriptions/.../microsoft.apimanagement/...
    │           │   APIM_SUBSCRIPTION_KEY=***
    │           │   APIM_API_ID=openai-api
    │           │   INFERENCE_API_PATH=/inference
    │           │
    │           │   # AI Model Endpoints
    │           │   EASTUS_ENDPOINT=https://hub-eastus.openai.azure.com
    │           │   UKSOUTH_ENDPOINT=https://hub-uksouth.openai.azure.com
    │           │   NORTHCENTRALUS_ENDPOINT=https://hub-northcentralus.openai.azure.com
    │           │
    │           │   # MCP Servers (7 servers)
    │           │   MCP_SERVER_WEATHER_URL=https://mcp-weather.app.uksouth...
    │           │   MCP_SERVER_GITHUB_URL=https://mcp-github.app.uksouth...
    │           │   MCP_SERVER_ONCALL_URL=https://mcp-oncall.app.uksouth...
    │           │   MCP_SERVER_SPOTIFY_URL=https://mcp-spotify.app.uksouth...
    │           │   MCP_SERVER_EXCEL_URL=https://mcp-excel.app.uksouth...
    │           │   MCP_SERVER_DOCS_URL=https://mcp-docs.app.uksouth...
    │           │   MCP_SERVER_PRODUCT_CATALOG_URL=https://mcp-product-catalog...
    │           │
    │           │   # Redis
    │           │   REDIS_HOST=lab-master-lab-redis.redis.cache.windows.net
    │           │   REDIS_PORT=6380
    │           │   REDIS_PASSWORD=***
    │           │
    │           │   # Azure AI Search
    │           │   SEARCH_ENDPOINT=https://lab-master-lab-search.search.windows.net
    │           │   SEARCH_API_KEY=***
    │           │
    │           │   # Cosmos DB
    │           │   COSMOSDB_ENDPOINT=https://lab-master-lab-cosmos.documents.azure.com
    │           │   COSMOSDB_KEY=***
    │           │
    │           │   # Content Safety
    │           │   CONTENT_SAFETY_ENDPOINT=https://...cognitiveservices.azure.com
    │           │   CONTENT_SAFETY_KEY=***
    │           │
    │           │   # ... and more
    │           │
    │           └─► File: master-lab.env (ready to load!)
    │
    └─► Cell 28: Normalize endpoints ⭐
            │
            │   Input Dependencies:
            │   └─ master-lab.env (from Cell 24)
            │
            │   Process:
            │   1. Read master-lab.env
            │   2. Check if OPENAI_ENDPOINT is set
            │   3. If not, derive from APIM_GATEWAY_URL + INFERENCE_API_PATH
            │   4. Update master-lab.env with normalized value
            │
            └─► Updates master-lab.env:
                │
                │   OPENAI_ENDPOINT=https://lab-master-lab-apim.azure-api.net/inference
                │   # (derived from APIM_GATEWAY_URL + INFERENCE_API_PATH)
                │
                └─► master-lab.env is now COMPLETE and NORMALIZED!

        ⬇️  Configuration file ready! Now load it into environment...

┌──────────────────────────────────────────────────────────────────┐
│              PHASE 5: INITIALIZATION (Load & Connect)            │
└──────────────────────────────────────────────────────────────────┘
    │
    ├─► Cell 7: Load master-lab.env ⭐ [MOVED FROM POSITION 7]
    │       │
    │       │   from dotenv import load_dotenv
    │       │
    │       │   env_file = 'master-lab.env'
    │       │   if os.path.exists(env_file):  # ✅ FILE EXISTS NOW!
    │       │       load_dotenv(env_file)
    │       │       print(f'[OK] Loaded environment from {env_file}')
    │       │       apim_url = os.getenv('APIM_GATEWAY_URL')
    │       │       print(f'[OK] APIM Gateway URL: {apim_url}')
    │       │
    │       └─► Result:
    │           │
    │           │   All ~50+ variables now in os.environ!
    │           │   ✅ APIM_GATEWAY_URL available
    │           │   ✅ MCP_SERVER_*_URL available
    │           │   ✅ REDIS_HOST available
    │           │   ✅ All credentials available
    │           │
    │           └─► Python code can now use os.getenv('APIM_GATEWAY_URL'), etc.
    │
    └─► Cell 15: Initialize MCP servers ⭐ [MOVED FROM POSITION 15]
            │
            │   from notebook_mcp_helpers import MCPClient
            │
            │   Input Dependencies:
            │   ├─ Cell 7: os.environ now has MCP_SERVER_*_URL variables ✅
            │   ├─ Cell 11: MCP Container Apps deployed and running ✅
            │   └─ File: .mcp-servers-config
            │
            │   Process:
            │   1. Read .mcp-servers-config
            │   2. For each server, get URL from os.environ
            │   3. Create MCPClient instance for each server
            │   4. Test connection to each server
            │   5. Build mcp object with server attributes
            │
            └─► Creates global 'mcp' object:
                │
                │   mcp.weather → WeatherMCPClient(url=MCP_SERVER_WEATHER_URL)
                │   mcp.github → GitHubMCPClient(url=MCP_SERVER_GITHUB_URL)
                │   mcp.oncall → OnCallMCPClient(url=MCP_SERVER_ONCALL_URL)
                │   mcp.spotify → SpotifyMCPClient(url=MCP_SERVER_SPOTIFY_URL)
                │   mcp.excel → ExcelMCPClient(url=MCP_SERVER_EXCEL_URL)
                │   mcp.docs → DocsMCPClient(url=MCP_SERVER_DOCS_URL)
                │   mcp.product_catalog → ProductCatalogMCPClient(url=...)
                │   mcp.place_order → PlaceOrderMCPClient(url=...)
                │
                └─► ✅ All MCP servers initialized and ready to use!

        ⬇️  Everything initialized! Now we can run tests and labs...

┌──────────────────────────────────────────────────────────────────┐
│              PHASE 6: VERIFICATION & LABS (Use It!)              │
└──────────────────────────────────────────────────────────────────┘
    │
    ├─► Cell 30: APIM Policy Validation
    │       └─► Verify load balancing policies are configured
    │
    ├─► Cell 34: Backend Health Check
    │       └─► Test APIM backends are responding
    │
    ├─► Cells 42-56: Various Tests
    │       ├─ Basic chat completion
    │       ├─ Streaming responses
    │       ├─ Multiple requests
    │       ├─ Load distribution
    │       └─ Response time visualization
    │
    └─► Cells 70-248: 25 Lab Exercises
            ├─ Lab 01: Basic APIM usage
            ├─ Lab 02: Backend pool load balancing
            ├─ Lab 04: Circuit breaker
            ├─ Lab 05: Rate limiting
            ├─ Lab 07: Custom headers
            ├─ Lab 08: Model routing
            ├─ Lab 09: AI Foundry SDK
            ├─ Lab 10: DeepSeek integration
            ├─ Lab 11-16: MCP server integrations
            │   ├─ Weather data
            │   ├─ GitHub repositories
            │   ├─ OnCall schedules
            │   ├─ Spotify music
            │   ├─ Excel documents
            │   └─ Product catalog
            ├─ Lab 17-20: Azure AI services
            ├─ Lab 21-23: Multi-server orchestration
            └─ Lab 24-25: Advanced agent frameworks

            ✅ All labs work because:
               ├─ Infrastructure is deployed (Cell 11) ✅
               ├─ Configuration is generated (Cell 24, 28) ✅
               ├─ Environment is loaded (Cell 7) ✅
               └─ MCP servers are initialized (Cell 15) ✅
```

---

## DEPENDENCY MATRIX (Detailed)

```
┌──────┬─────────────┬───────────────────────────────────┬─────────────────────────────┐
│ Cell │ Type        │ Depends On                        │ Provides                    │
├──────┼─────────────┼───────────────────────────────────┼─────────────────────────────┤
│  2   │ SETUP       │ None                              │ az() function               │
│  3   │ SETUP       │ Cell 2                            │ deployment helpers          │
│ 27   │ SETUP       │ None                              │ pip packages installed      │
│ 38   │ SETUP       │ Cell 27                           │ Python imports              │
├──────┼─────────────┼───────────────────────────────────┼─────────────────────────────┤
│ 14   │ PRE-DEPLOY  │ Cell 2                            │ Azure CLI validation        │
│ 20   │ PRE-DEPLOY  │ None                              │ subscription_id, rg, loc    │
│ 21   │ PRE-DEPLOY  │ Cell 20                           │ credential, resource_client │
├──────┼─────────────┼───────────────────────────────────┼─────────────────────────────┤
│ 11   │ DEPLOYMENT  │ Cells 2,3,20,21 + Bicep files    │ step1-4_outputs             │
├──────┼─────────────┼───────────────────────────────────┼─────────────────────────────┤
│ 24   │ POST-DEPLOY │ Cells 11,20                       │ master-lab.env file         │
│ 28   │ POST-DEPLOY │ Cell 24                           │ normalized endpoints        │
├──────┼─────────────┼───────────────────────────────────┼─────────────────────────────┤
│  7   │ INIT        │ Cells 24,28                       │ os.environ loaded           │
│ 15   │ INIT        │ Cells 7,11,24                     │ mcp object (8 servers)      │
├──────┼─────────────┼───────────────────────────────────┼─────────────────────────────┤
│ 30+  │ LAB/TEST    │ Cells 7,15                        │ Test results                │
│ 70+  │ LAB         │ Cells 7,15                        │ Lab exercises               │
└──────┴─────────────┴───────────────────────────────────┴─────────────────────────────┘

CELLS TO REMOVE (Duplicates):
┌──────┬─────────────┬────────────────────────────────────────────────────────┐
│ Cell │ Reason      │ Replacement                                            │
├──────┼─────────────┼────────────────────────────────────────────────────────┤
│  1   │ Empty       │ None (just delete)                                     │
│ 13   │ Dup env     │ Cell 24 (real generator, not template)                 │
│ 16   │ Dup env     │ Cell 24 (real generator, not template)                 │
│ 22   │ Dup auth    │ Cell 21 (clean auth) + Cell 11 (clean deployment)     │
│ 32   │ Dup pip     │ Cell 27 (first pip install)                            │
└──────┴─────────────┴────────────────────────────────────────────────────────┘
```

---

## TIME-BASED FLOW (Before vs After)

### BEFORE (Broken) ⏱️

```
Time →  0      5      10     15     20     24     28     30
        │      │      │      │      │      │      │      │
Cell:   2,3    7❌    15❌           11✓    24✓    28✓
        │      │      │             │      │      │
        Setup  Load   Init          Deploy Gen    Norm
               .env   MCP                  .env   .env
               ❌FAIL ❌FAIL
               (no    (no URLs)
               file)

Result: Labs can't run because initialization failed
```

### AFTER (Fixed) ⏱️

```
Time →  0      5      10     40     45     46     47     50
        │      │      │      │      │      │      │      │
Cell:   2,3    14,    11✓    24✓    28✓    7✓     15✓    Labs
        │      20,21  │      │      │      │      │      │
        Setup  Config Deploy Gen    Norm   Load   Init   Test
                      (~40m) .env   .env   .env   MCP
                             ✓      ✓      ✓      ✓      ✓

Result: Everything works! 🎉
```

---

## CRITICAL PATH SUMMARY

**The notebook has ONE critical path that must be followed:**

```
1. Define infrastructure (Cells 2, 3)
   ↓
2. Configure Azure (Cells 14, 20, 21)
   ↓
3. Deploy Azure resources (Cell 11)
   ↓
4. Generate config file from outputs (Cell 24)
   ↓
5. Normalize endpoints (Cell 28)
   ↓
6. Load config into environment (Cell 7)
   ↓
7. Initialize MCP servers (Cell 15)
   ↓
8. Run labs and tests (Cells 30+, 70+)
```

**Any deviation from this order = BROKEN NOTEBOOK**

**Current deviation:** Steps 6-7 run before steps 4-5 → BROKEN

**Fix:** Move steps 6-7 to run after steps 4-5 → WORKING

---

## FILE LIFECYCLE

### master-lab.env

```
Time     Cell   Action             State
──────────────────────────────────────────────────────────────
0:00     -      (not exists)       ∅
0:05     13❌   Create template    SUBSCRIPTION_ID=
                                   RESOURCE_GROUP=
                                   (placeholders only)
0:10     11     (deployment)       (no change)
0:50     24✓    Generate from      SUBSCRIPTION_ID=d334f2cd...
                outputs            APIM_GATEWAY_URL=https://...
                                   MCP_SERVER_WEATHER_URL=...
                                   (50+ real values!)
0:51     28✓    Add normalized     + OPENAI_ENDPOINT=https://...
                endpoint           (derived value added)
0:52     7✓     Load into          (os.environ now has all vars)
                os.environ
──────────────────────────────────────────────────────────────

✅ CORRECT: Cell 7 loads file AFTER it's fully populated (Cell 24 → 28)
❌ BROKEN: Cell 7 tries to load at 0:05, file doesn't exist or has placeholders
```

---

## ANALOGY: Building a House

**Current Notebook (Broken):**
```
1. Try to turn on the lights ❌ (no electricity yet)
2. Try to use the plumbing ❌ (no water yet)
3. Pour foundation ✓
4. Build walls ✓
5. Install electrical wiring ✓
6. Install plumbing ✓
7. Connect utilities ✓

Result: Steps 1-2 failed because utilities weren't installed yet!
```

**Fixed Notebook (Working):**
```
1. Pour foundation ✓
2. Build walls ✓
3. Install electrical wiring ✓
4. Install plumbing ✓
5. Connect utilities ✓
6. Turn on the lights ✓ (works now!)
7. Use the plumbing ✓ (works now!)

Result: Everything works in the right order!
```

**The notebook is trying to use resources before they're created.**

**Fix: CREATE → CONFIGURE → USE (not USE → CREATE → CONFIGURE)**

---

## NEXT STEPS

1. **Move Cell 7** from position 7 → after Cell 28
2. **Move Cell 15** from position 15 → after new Cell 7 position
3. **Delete Cells** 1, 13, 16, 22, 32
4. **Test** entire notebook top-to-bottom
5. **Update documentation** (Cells 4, 5) to reflect new order
6. **Add validation** after Cell 24 to verify env file was created

**Estimated fix time:** 30 minutes
**Estimated test time:** 45 minutes (full deployment + labs)
**Total:** ~75 minutes to have a working notebook

---

**END OF VISUAL DEPENDENCY DIAGRAM**
