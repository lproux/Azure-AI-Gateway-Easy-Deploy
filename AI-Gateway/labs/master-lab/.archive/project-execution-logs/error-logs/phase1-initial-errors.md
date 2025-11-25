# Phase 1 - Initial Error Catalog

**Generated**: 2025-11-14
**Notebook**: master-ai-gateway-fix-MCP.ipynb
**Total Cells**: 203 (102 code, 101 markdown)
**Total Errors Reported**: 30+

## Error Classification

### CRITICAL Errors (Blocking functionality)
1. Cell 41 - Client undefined for streaming
2. Cell 63 - JWT token acquisition failure
3. Cell 75 - Azure CLI MSAL error
4. Cell 81-82 - MCP server connectivity failures
5. Cell 106 - Model routing policy CLI error

### HIGH Priority (Feature not working)
1. Cell 47 - Load balancing region detection (Unknown region)
2. Cell 85 - Spotify MCP missing attribute
3. Cell 93 - GitHub MCP fallback issues
4. Cell 96 - Product catalog MCP timeout
5. Cell 99 - Workflow MCP initialization error
6. Cell 109 - Image generation 404 errors
7. Cell 130 - Image generation failures
8. Cell 140 - MCP server health check failures
9. Cell 142 - MCP server testing timeouts
10. Cell 154 - Cosmos DB firewall blocking
11. Cell 156 - Search index creation failure
12. Cell 160 - Secure policy model name issues
13. Cell 162 - Model routing fallback failures
14. Cell 171 - Image generation test failures
15. Cell 177 - MCP docs server errors

### MEDIUM Priority (Warnings/Missing features)
1. Cell 22 - API_ID not configured (autodiscovery possible)
2. Cell 23 - API_ID autodiscovery warning
3. Cell 33 - .env generation value capture unclear
4. Cell 101 - No cache indication
5. Cell 107 - Image deployment autodiscovery failing
6. Cell 111 - Missing RESOURCE_GROUP
7. Cell 164 - Log analytics path not found

### LOW Priority (Package installation/Setup)
1. Cell 180 - agentframework package not found
2. Cells 183, 186-187 - Not yet tested/executed
3. Cells 189-203 - Framework integration (to be tested)

---

## Detailed Error Breakdown

### Cell 22: API_ID Configuration Warning
**Type**: Warning
**Status**: Working but suboptimal
**Error**:
```
[policy] WARNING: API_ID not properly configured
[policy] HINT: Run cell 9 first to auto-discover API_ID, or set APIM_API_ID in environment
```
**Impact**: Medium - functionality works but relies on manual configuration
**Root Cause**: Autodiscovery not enabled in cell
**Fix Strategy**: Implement autodiscovery logic
**Dependencies**: Cell 9 (must run first for autodiscovery)

---

### Cell 23: API_ID Autodiscovery Warning
**Type**: Warning
**Status**: Working but suboptimal
**Error**: API_ID could be autodiscovered
**Impact**: Medium - manual configuration required
**Root Cause**: Similar to Cell 22
**Fix Strategy**: Enable autodiscovery
**Dependencies**: None

---

### Cell 33: .env Generation Value Capture
**Type**: Verification needed
**Status**: Unknown - needs testing
**Question**: Is every value captured in the .env generation?
**Impact**: Medium-High - could cause downstream configuration issues
**Root Cause**: Unclear .env generation logic
**Fix Strategy**: Audit .env generation, verify all required values
**Dependencies**: None
**Testing Required**: Check generated .env against requirements

---

### Cell 41: Client Not Defined (CRITICAL)
**Type**: Runtime Error
**Status**: BROKEN
**Error**:
```python
[*] Testing streaming...
[ERROR] Streaming exception: name 'client' is not defined
[HINT] If this persists, verify the APIM operation allows streaming and the backend model supports it.
```
**Impact**: CRITICAL - streaming functionality broken
**Root Cause**: Missing client initialization before streaming test
**Fix Strategy**:
1. Identify where client should be initialized
2. Add client initialization before streaming test
3. Verify APIM operation configuration
**Dependencies**: Previous cells for client setup
**Testing Protocol**: Full A-L protocol required

---

### Cell 47: Load Balancing Region Unknown (HIGH)
**Type**: Logic Error
**Status**: Running but not working correctly
**Error**:
```
Testing load balancing across 3 regions...
Request 1-20: Region: Unknown (100% of requests)
Average response time: 0.38s
Region Distribution: Unknown: 20 requests (100.0%)
```
**Impact**: HIGH - load balancing verification not working
**Root Cause**: Region information not being extracted from responses
**Possible Causes**:
1. Missing header extraction logic
2. Backend not sending region information
3. APIM policy not propagating region headers
**Fix Strategy**:
1. Check APIM backend configuration for region tagging
2. Verify response headers contain region info
3. Update extraction logic to find region data
**Dependencies**: APIM backend configuration, deployment verification
**Testing Protocol**: Full A-L protocol required
**Additional Verification**: Confirm 3 regions are actually deployed

---

### Cell 63: JWT Token Acquisition (CRITICAL)
**Type**: Authentication Error
**Status**: BROKEN
**Error**:
```
ERROR: Cannot get JWT token. Please run: az login
```
**Impact**: CRITICAL - JWT authentication broken
**Root Cause**: Token acquisition logic failing
**Known Good Version**: Working version exists in archive
- File: `C:\Users\lproux\OneDrive - Microsoft\bkp\Documents\GitHub\MCP-servers-internalMSFT-and-external\AI-Gateway\labs\master-lab\archive\master-ai-gateway-fix-MCP copy22.ipynb`
**Fix Strategy**:
1. Compare current cell with working archive version
2. Identify differences in token acquisition logic
3. Port working code to current notebook
4. Test JWT token flow end-to-end
**Dependencies**: az login, Azure authentication
**Testing Protocol**: Full A-L protocol required
**Priority**: HIGHEST - blocking other authentication tests

---

### Cell 75: Azure CLI MSAL Error (CRITICAL)
**Type**: Azure CLI Error
**Status**: BROKEN
**Error**:
```
[FAIL] az helper error: ERROR: The command failed with an unexpected error. Here is the traceback:
ERROR: Can't get attribute 'NormalizedResponse' on <module 'msal.throttled_http_client' from 'C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\Lib\\site-packages\\msal\\throttled_http_client.pyc'>
```
**Impact**: CRITICAL - private connectivity policy cannot be applied
**Root Cause**: Azure CLI / MSAL version compatibility issue
**Possible Solutions**:
1. Update Azure CLI
2. Downgrade MSAL
3. Use alternative authentication method
4. Use Azure SDK instead of CLI
**Fix Strategy**:
1. Check Azure CLI version
2. Check MSAL version
3. Test if issue is environment-specific
4. Implement workaround using Azure SDK
**Dependencies**: Azure CLI installation
**Testing Protocol**: Full A-L protocol required

---

### Cell 81: MCP Weather Server Timeout (HIGH)
**Type**: Network/Connectivity Error
**Status**: BROKEN
**Error**:
```python
httpx.ConnectTimeout: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time
```
**Impact**: HIGH - MCP weather functionality unavailable
**Server URL**: `https://mcp-weather-pavavy6pu5.ambitiousfield-f6abdfb4.uksouth.azurecontainerapps.io`
**Root Cause**: MCP server not responding or not accessible
**Possible Causes**:
1. Server not deployed
2. Server scaled to zero
3. Network connectivity issue
4. Firewall blocking access
**Fix Strategy**:
1. Verify server deployment status in Azure
2. Check container app logs
3. Test server endpoint directly
4. Verify network/firewall rules
5. Check server health endpoint
**Dependencies**: Azure Container Apps deployment
**Testing Protocol**: Full A-L protocol required

---

### Cell 82: MCP GitHub Server Timeout (HIGH)
**Type**: Network/Connectivity Error
**Status**: BROKEN
**Error**: Same timeout as Cell 81
**Server URL**: `https://mcp-github-pavavy6pu5.ambitiousfield-f6abdfb4.uksouth.azurecontainerapps.io`
**Impact**: HIGH - GitHub MCP functionality unavailable
**Root Cause**: Same as Cell 81 - server connectivity
**Fix Strategy**: Same as Cell 81
**Dependencies**: Azure Container Apps deployment
**Testing Protocol**: Full A-L protocol required

---

### Cell 85: Spotify MCP Missing Method (HIGH)
**Type**: Runtime Error - Missing Attribute
**Status**: BROKEN
**Error**:
```python
AttributeError: 'SpotifyMCP' object has no attribute 'search_tracks'
```
**Impact**: HIGH - Spotify integration broken
**Root Cause**: Helper class missing method or method name mismatch
**Fix Strategy**:
1. Check `notebook_mcp_helpers.py` for SpotifyMCP class
2. Identify correct method name
3. Either fix helper class or update cell to use correct method
4. Verify Spotify MCP server API
**Dependencies**: notebook_mcp_helpers.py
**Testing Protocol**: Full A-L protocol required
**Files to Check**: `notebook_mcp_helpers.py:SpotifyMCP`

---

### Cell 86: MCP OnCall Server Timeout (HIGH)
**Type**: Network/Connectivity Error
**Status**: BROKEN
**Error**: Same httpx.ConnectTimeout as previous MCP cells
**Server URL**: `https://mcp-oncall-pavavy6pu5.ambitiousfield-f6abdfb4.uksouth.azurecontainerapps.io`
**Impact**: HIGH - OnCall MCP functionality unavailable
**Root Cause**: Server connectivity issue
**Fix Strategy**: Same as Cells 81-82
**Dependencies**: Azure Container Apps deployment
**Testing Protocol**: Full A-L protocol required

---

### Cell 89: MCP OnCall Server Timeout (Duplicate)
**Type**: Network/Connectivity Error
**Status**: BROKEN
**Error**: Same as Cell 86
**Impact**: HIGH - Duplicate test of OnCall MCP
**Root Cause**: Same as previous MCP connectivity issues
**Fix Strategy**: Fix once for all MCP servers
**Dependencies**: Azure Container Apps deployment
**Testing Protocol**: Full A-L protocol required

---

### Cell 93: GitHub MCP Analysis Fallback (MEDIUM)
**Type**: Warning/Fallback Behavior
**Status**: Working with fallback
**Error**:
```
[mcp][error] MCP initialization or call failed: 'dict' object has no attribute 'github'
[mcp][info] Falling back to direct GitHub REST API.
```
**Impact**: MEDIUM - functionality works but uses fallback
**Root Cause**: MCP server unreachable, falling back to REST API
**Fix Strategy**:
1. Fix underlying MCP connectivity (relates to Cells 81-82)
2. Verify MCP GitHub server API contract
3. Ensure helper code matches server interface
**Dependencies**: MCP GitHub server connectivity
**Testing Protocol**: Verify after MCP connectivity fixed

---

### Cell 96: Product Catalog MCP Timeout (HIGH)
**Type**: Network/Connectivity Error
**Status**: BROKEN
**Error**: httpx.ConnectTimeout (same pattern)
**Server URL**: `https://mcp-product-catalog-pavavy6pu5.ambitiousfield-f6abdfb4.uksouth.azurecontainerapps.io`
**Impact**: HIGH - Product catalog unavailable
**Root Cause**: MCP server connectivity
**Fix Strategy**: Same as other MCP servers
**Dependencies**: Azure Container Apps deployment
**Testing Protocol**: Full A-L protocol required

---

### Cell 99: Workflow MCP Timeout (HIGH)
**Type**: Network/Connectivity Error
**Status**: BROKEN
**Error**: httpx.ConnectTimeout
**Impact**: HIGH - Workflow functionality unavailable
**Root Cause**: MCP server connectivity
**Fix Strategy**: Same as other MCP servers
**Dependencies**: Azure Container Apps deployment
**Testing Protocol**: Full A-L protocol required

---

### Cell 101: No Cache Indication (MEDIUM)
**Type**: Missing Feature/Indicator
**Status**: Working but no cache feedback
**Error**:
```
Request 1-20: cached: False (all requests)
```
**Impact**: MEDIUM - caching not working or not indicated
**Root Cause**: Cache not configured OR cache status not being reported
**Fix Strategy**:
1. Verify semantic caching policy is applied
2. Check APIM policy for cache headers
3. Test with identical requests to trigger cache
4. Verify cache headers in response
**Dependencies**: Semantic caching policy
**Testing Protocol**: Full A-L protocol required

---

### Cell 106: Model Routing Policy Error (CRITICAL)
**Type**: Azure CLI MSAL Error
**Status**: BROKEN
**Error**: Same MSAL error as Cell 75
**Impact**: CRITICAL - model routing policy cannot be applied
**Root Cause**: Azure CLI/MSAL compatibility issue
**Fix Strategy**: Same as Cell 75
**Dependencies**: Azure CLI
**Testing Protocol**: Full A-L protocol required

---

### Cell 107: Image Deployment Autodiscovery Failure (MEDIUM)
**Type**: Resource Discovery Error
**Status**: Working with empty result
**Error**:
```
[discovery] Failed to list deployments: 404 { "statusCode": 404, "message": "Resource not found" }
[discovery] No image deployment found; returning empty.
[discovery] AUTO_IMAGE_DEPLOYMENT=
```
**Impact**: MEDIUM - image generation unavailable
**Root Cause**: Image deployment not found OR discovery logic incorrect
**Fix Strategy**:
1. Verify image generation deployment exists
2. Check deployment resource path
3. Update discovery logic if needed
**Dependencies**: Image generation deployment
**Testing Protocol**: Full A-L protocol required

---

### Cell 109: Image Generation 404 (HIGH)
**Type**: Resource Not Found
**Status**: BROKEN
**Error**:
```
[image] gpt-image-1 failed: 404 { "statusCode": 404, "message": "Resource not found" }
```
**Impact**: HIGH - image generation broken
**Root Cause**: Image model not deployed OR incorrect endpoint
**Fix Strategy**:
1. Verify DALL-E deployment
2. Check model name configuration
3. Verify APIM routing for image generation
**Dependencies**: Image generation deployment
**Testing Protocol**: Full A-L protocol required

---

### Cell 111: Missing RESOURCE_GROUP (MEDIUM)
**Type**: Configuration Error
**Status**: BROKEN
**Error**:
```
[deploy] Endpoint format unexpected: https://apim-pavavy6pu5hpa.azure-api.netinference
[deploy] Missing resource_name or RESOURCE_GROUP; cannot deploy.
```
**Impact**: MEDIUM - deployment functionality broken
**Root Cause**: RESOURCE_GROUP environment variable not set
**Fix Strategy**:
1. Set RESOURCE_GROUP in .env
2. Update autodiscovery logic
3. Add validation earlier in notebook
**Dependencies**: .env configuration
**Testing Protocol**: Verify after .env fixes

---

### Cell 130: Image Generation 404 (Multiple)
**Type**: Resource Not Found
**Status**: BROKEN
**Error**:
```
Generating image 1-3: Error: {"error":{"code":"404","message": "Resource not found"}}
```
**Impact**: HIGH - all image generation failing
**Root Cause**: Same as Cell 109
**Fix Strategy**: Fix once with Cell 109
**Dependencies**: Image generation deployment
**Testing Protocol**: Full A-L protocol required

---

### Cell 140: MCP Server Health Check Failures (HIGH)
**Type**: Network/Connectivity Timeout
**Status**: BROKEN
**Error**: HTTPSConnectionPool timeouts for all 7 MCP servers
**Affected Servers**:
- weather
- oncall
- github
- spotify
- product-catalog
- place-order
- ms-learn
**Impact**: HIGH - all MCP servers unreachable
**Root Cause**: Systematic MCP connectivity issue
**Fix Strategy**: Fix MCP connectivity once for all servers
**Dependencies**: Azure Container Apps, network configuration
**Testing Protocol**: Full A-L protocol required

---

### Cell 142: MCP Server Testing Timeouts (HIGH)
**Type**: Network/Connectivity Error
**Status**: BROKEN
**Error**: Same timeout errors as Cell 140
**Impact**: HIGH - MCP testing unavailable
**Root Cause**: Same MCP connectivity issue
**Fix Strategy**: Fix with Cell 140
**Dependencies**: Azure Container Apps
**Testing Protocol**: Full A-L protocol required

---

### Cell 144: MCP OAuth Authorization Warning (MEDIUM)
**Type**: Authentication Warning
**Status**: Working with warning
**Error**:
```
[WARN] Failed audience api://4a5d0f1a-578e-479a-8ba9-05770ae9ce6b/.default
AADSTS500011: The resource principal was not found in the tenant
```
**Impact**: MEDIUM - OAuth not fully configured
**Root Cause**: Service principal/audience not registered
**Fix Strategy**:
1. Verify service principal exists
2. Check audience configuration
3. Update to correct audience
**Dependencies**: Azure AD configuration
**Testing Protocol**: Full A-L protocol required

---

### Cell 154: Cosmos DB Firewall Blocking (HIGH)
**Type**: Network/Firewall Error
**Status**: BROKEN
**Error**:
```
ERROR: Request originated from IP 79.97.178.198 through public internet. This is blocked by your Cosmos DB account firewall settings.
```
**Impact**: HIGH - message storage unavailable
**Root Cause**: Cosmos DB firewall not allowing client IP
**Fix Strategy**:
1. Add client IP to Cosmos DB firewall
2. Enable public access (if appropriate)
3. Configure service endpoint/private endpoint
4. Document IP whitelist requirement
**Dependencies**: Cosmos DB configuration
**Testing Protocol**: Full A-L protocol required
**Security Note**: Document firewall configuration in workshop

---

### Cell 156: Search Index Creation Failure (HIGH)
**Type**: Resource Not Found
**Status**: BROKEN
**Error**:
```
[WARN] Index create failed: 404 - { "statusCode": 404, "message": "Resource not found" }
```
**Impact**: HIGH - vector search unavailable
**Root Cause**: Search service not configured OR incorrect endpoint
**Fix Strategy**:
1. Verify Azure AI Search deployment
2. Check search service endpoint
3. Verify API key configuration
4. Test search service connectivity
**Dependencies**: Azure AI Search deployment
**Testing Protocol**: Full A-L protocol required

---

### Cell 160: Secure Policy Model Name Issues (MEDIUM)
**Type**: Configuration/Logic Error
**Status**: BROKEN
**Error**:
```
[WARN] Could not derive model name from models_config: 'inference-backend-pool'
Response status: 404 - Resource Not Found
```
**Impact**: MEDIUM - secure retrieval testing broken
**Root Cause**: Model name derivation logic incorrect
**Fix Strategy**:
1. Update model name extraction logic
2. Verify models_config structure
3. Add explicit model name configuration
**Dependencies**: Configuration
**Testing Protocol**: Full A-L protocol required

---

### Cell 162: Model Routing Fallback Failure (HIGH)
**Type**: Backend Error
**Status**: BROKEN
**Error**:
```
[FALLBACK] No available model succeeded (all returned 404 or errors).
ERROR: Unexpected retrieval error: 'NoneType' object has no attribute 'id'
```
**Impact**: HIGH - model routing and retrieval broken
**Root Cause**: All backend models unavailable OR routing configuration incorrect
**Fix Strategy**:
1. Verify backend deployments (foundry1/2/3)
2. Check APIM backend pool configuration
3. Verify API keys
4. Test each backend individually
**Dependencies**: Azure AI Foundry deployments
**Testing Protocol**: Full A-L protocol required

---

### Cell 164: Log Analytics Query Path Error (MEDIUM)
**Type**: Resource Path Error
**Status**: BROKEN
**Error**:
```
ERROR: (PathNotFoundError) The requested path does not exist
```
**Impact**: MEDIUM - token usage analytics unavailable
**Root Cause**: Incorrect workspace path OR query syntax
**Fix Strategy**:
1. Verify Log Analytics workspace ID
2. Check query syntax
3. Verify data ingestion is working
4. Test workspace connectivity
**Dependencies**: Log Analytics workspace
**Testing Protocol**: Full A-L protocol required

---

### Cell 171: Image Generation Test Failure (HIGH)
**Type**: Resource Not Found
**Status**: BROKEN
**Error**:
```
[test] Failure: HTTP 404 - Resource not found
```
**Impact**: HIGH - image generation testing broken
**Root Cause**: Same as Cells 109, 130
**Fix Strategy**: Fix once with other image generation issues
**Dependencies**: Image generation deployment
**Testing Protocol**: Full A-L protocol required

---

### Cell 177: MCP Docs Server KeyError (MEDIUM)
**Type**: Runtime Error
**Status**: BROKEN
**Error**:
```
ExceptionGroup: KeyError: 0
```
**Impact**: MEDIUM - MCP documentation server integration broken
**Server URL**: `http://docs-mcp-24774.eastus.azurecontainer.io:8000/mcp`
**Root Cause**: API response structure mismatch
**Fix Strategy**:
1. Check MCP docs server API response format
2. Update helper code to match API
3. Add error handling for missing fields
**Dependencies**: MCP docs server
**Testing Protocol**: Full A-L protocol required

---

### Cell 178: MCP Endpoint Discovery Success (INFO)
**Type**: Informational
**Status**: WORKING
**Note**: This cell successfully finds working endpoint `/mcp`
**No fix needed** - provides diagnostic information

---

### Cell 180: agentframework Package Not Found (LOW)
**Type**: Package Installation Error
**Status**: BROKEN
**Error**:
```
ERROR: Could not find a version that satisfies the requirement agentframework
ERROR: No matching distribution found for agentframework
```
**Impact**: LOW - framework examples unavailable
**Root Cause**: Package name incorrect OR not published
**Fix Strategy**:
1. Identify correct package name
2. Check if package exists in PyPI
3. Install correct package OR implement framework example differently
4. This may be addressed in Phase 3 (framework examples)
**Dependencies**: PyPI package availability
**Testing Protocol**: Research correct package, then full A-L protocol

---

### Cells 183, 186-187: Not Yet Tested
**Type**: Unknown
**Status**: NOT TESTED
**Impact**: Unknown
**Fix Strategy**: Test and document in Phase 1 execution

---

### Cells 189-203: Framework Integration Tests
**Type**: Unknown - To Be Tested
**Status**: NOT TESTED
**Impact**: Unknown
**Fix Strategy**: Test systematically in Phase 1 execution

---

## Error Summary Statistics

| Category | Count |
|----------|-------|
| CRITICAL | 5 |
| HIGH | 15 |
| MEDIUM | 8 |
| LOW | 1 |
| NOT TESTED | 16+ |
| **TOTAL** | **45+** |

## Root Cause Analysis

### Primary Issues
1. **MCP Server Connectivity** (15+ cells affected)
   - All MCP servers timing out
   - Root cause: Deployment/network/scaling issue
   - Single fix will resolve multiple cells

2. **Azure CLI MSAL Error** (2 cells affected)
   - Version compatibility issue
   - Affects policy deployment
   - Needs environment fix or workaround

3. **Image Generation** (4 cells affected)
   - DALL-E deployment missing or misconfigured
   - Single fix will resolve multiple cells

4. **Authentication** (2 cells affected)
   - JWT token acquisition
   - OAuth configuration
   - Needs working examples from archive

5. **Resource Configuration** (5+ cells affected)
   - Missing environment variables
   - Autodiscovery not enabled
   - .env generation incomplete

## Fix Priority Order

### Phase 1.1: Environment & Configuration (Cells 22, 23, 33)
- Low-hanging fruit
- Enables other fixes
- No dependencies

### Phase 1.2: MCP Server Connectivity (Cells 81-82, 85-86, 89, 93, 96, 99, 140, 142)
- HIGH impact
- Single root cause
- Fixes 15+ cells at once

### Phase 1.3: Authentication (Cells 63, 144)
- CRITICAL
- Has working version in archive
- Blocks other tests

### Phase 1.4: Azure CLI/Policy (Cells 75, 106)
- CRITICAL
- May need environment change
- Could be skipped if not deployable in current environment

### Phase 1.5: Image Generation (Cells 107, 109, 130, 171)
- HIGH impact
- Single deployment issue
- Fixes 4+ cells

### Phase 1.6: Backend Services (Cells 47, 154, 156, 162, 164)
- HIGH impact
- Each needs individual fix
- Some may need Azure resource configuration

### Phase 1.7: Advanced Features (Cells 41, 101, 111, 160)
- MEDIUM-HIGH impact
- Requires code fixes
- Individual attention needed

### Phase 1.8: Framework Integration (Cells 177, 180, 183-203)
- LOW-MEDIUM impact
- Some deferred to Phase 3
- Test and document

---

## Testing Status Tracking

| Cell | Error Type | Status | Tested | Fixed | Verified |
|------|-----------|--------|--------|-------|----------|
| 22 | Warning | Working | ❌ | ❌ | ❌ |
| 23 | Warning | Working | ❌ | ❌ | ❌ |
| 33 | Unknown | Unknown | ❌ | ❌ | ❌ |
| 41 | Error | Broken | ❌ | ❌ | ❌ |
| 47 | Logic | Broken | ❌ | ❌ | ❌ |
| 63 | Error | Broken | ❌ | ❌ | ❌ |
| 75 | Error | Broken | ❌ | ❌ | ❌ |
| 81 | Error | Broken | ❌ | ❌ | ❌ |
| ... | ... | ... | ... | ... | ... |

*Full tracking table will be maintained in separate tracking file*

---

**Next Steps**: Begin Phase 1.1 execution with Environment & Configuration fixes
