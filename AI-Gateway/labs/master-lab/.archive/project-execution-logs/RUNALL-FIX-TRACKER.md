# Run All Fix Tracker - Sequential Cell Repairs

**Goal**: Execute entire notebook with "Run All" command successfully
**Strategy**: Fix cells sequentially, skip working cells, test incrementally
**Status**: IN PROGRESS

---

## MCP Server Status (Current)

| Server | Status | URL |
|--------|--------|-----|
| docs | ✅ UP | http://docs-mcp-72998.eastus.azurecontainer.io:8000 |
| weather | ❌ DOWN | Container Instance timeout |
| oncall | ❌ DOWN | Container Instance timeout |
| github | ❌ DOWN | Container Instance timeout |
| spotify | ❌ DOWN | Container Instance timeout |
| product-catalog | ❌ DOWN | Container Instance timeout |
| place-order | ❌ DOWN | Container Instance timeout |

**Action Required**: Restart/redeploy 6 MCP Container Instances

---

## Cell-by-Cell Fix Status

### ✅ WORKING CELLS (Skip - Don't Touch)

| Cell | Status | Description |
|------|--------|-------------|
| 1-13 | ✅ WORKING | Environment setup, variables |
| 14-31 | ✅ WORKING | Deployment steps (already complete) |
| 33-46 | ✅ WORKING | Lab 01-02 (basic APIM tests) |
| 47 | ✅ WORKING | Lab 02 Test 1 (works, but all UK South) |
| 49 | ✅ WORKING | Lab 02 Test 2 (visualization) |

### ❌ BROKEN CELLS (Need Fixes)

#### **PRIORITY 1: Infrastructure Blocking Issues**

| Cell | Issue | Root Cause | Fix Required |
|------|-------|------------|--------------|
| 48 | Load balancing shows 100% UK South | Missing/incorrect APIM policy | Add backend pool routing policy |
| 52 | Token metrics - unclear if logging works | No verification | Add Log Analytics query verification |
| 76 | NormalizedResponse error | Azure CLI msal bug | Workaround or update Azure CLI |
| 82-94 | All MCP timeout errors | MCP servers scaled to zero | Restart Container Instances |
| 96 | Product catalog timeout | MCP server down | Fix after MCP restart |
| 98 | AutoGen 404 on `/weather/sse` | APIM missing SSE endpoints | Add SSE endpoints to APIM OR change to HTTP |
| 100 | Semantic Kernel API error | SK API changed in v1.37 | Update `invoke_prompt()` calls |
| 102 | SK diagnostic errors | Same SK API issue | Update `invoke_prompt()` calls |
| 107 | Semantic cache not working | Cache not enabled/configured | Enable semantic cache in APIM |
| 112 | Model routing policy error | Azure CLI msal bug | Same as cell 76 |
| 160 | Cosmos DB firewall block | Public IP not allowed | Add firewall rule for client IP |
| 162 | Search index 404 | Index not created | Create search index |

#### **PRIORITY 2: Code/Config Issues**

| Cell | Issue | Fix Required |
|------|-------|--------------|
| 32 | dall-e-3 deployment failed | Document limitation (quota issue) |
| 85 | Spotify missing `search_tracks` | Fix helper method or document |
| 86 | Can be removed | Remove if redundant |
| 105 | Workflow failed (MCP timeout) | Fix after MCP restart |
| 113 | No image deployment found | Document as expected (not deployed) |
| 115 | Image gen 401 errors | Missing subscription key or wrong endpoint |
| 117 | Deployment endpoint format wrong | Fix endpoint URL construction |
| 122 | Expected 404 (DeploymentNotFound) | Already documented as expected |
| 136 | Image generation 404s | Same as 113/115 |
| 146-150 | MCP authorization tests fail | Fix after MCP restart |
| 166 | Model routing 404s | Backend pool misconfigured |
| 168 | Vector search disabled | Document as optional |
| 170 | Log Analytics query error | Query syntax or no data yet |
| 177-178 | Image generation failures | Same as 113/115/136 |
| 183-184 | Docs MCP KeyError | MCP client code issue |
| 186 | Agent framework not found | Remove cell or fix package reference |
| 189 | Semantic Kernel timeout | User interrupted (expected behavior) |
| 195+ | Duplicate content issues | Consolidate/reorganize |

---

## Sequential Fix Plan

### **Phase 1: Critical Infrastructure (Blocks Everything)**

**Duration**: 2-3 hours
**Outcome**: MCP servers running, APIM configured

#### 1.1 Restart MCP Container Instances (30 min)
```bash
# Restart all 6 down MCP servers
az container restart -g lab-master-lab -n weather-mcp-72998
az container restart -g lab-master-lab -n oncall-mcp-72998
az container restart -g lab-master-lab -n mcp-github-72998
az container restart -g lab-master-lab -n spotify-mcp-72998
az container restart -g lab-master-lab -n mcp-product-catalog-72998
az container restart -g lab-master-lab -n mcp-place-order-72998
```

**Cells Fixed**: 82-94, 96, 105, 146-150

#### 1.2 Add APIM SSE/HTTP Endpoints (30 min)
Options:
- **A**: Add `/weather/sse`, `/oncall/sse` endpoints to APIM
- **B**: Change AutoGen/SK code to use HTTP `/weather/mcp` instead

**Recommendation**: Option B (change code to use working HTTP endpoints)

**Cells Fixed**: 98 (AutoGen)

#### 1.3 Fix Load Balancing Policy (30 min)
Add backend pool routing policy to APIM inference API

**Cells Fixed**: 48

#### 1.4 Enable Semantic Cache (20 min)
Configure APIM caching policy

**Cells Fixed**: 107

#### 1.5 Update Cosmos DB Firewall (10 min)
```bash
az cosmosdb update \
  --name cosmos-pavavy6pu5hpa \
  --resource-group lab-master-lab \
  --ip-range-filter "109.255.46.142"
```

**Cells Fixed**: 160

---

### **Phase 2: Code Compatibility Fixes**

**Duration**: 1-2 hours
**Outcome**: SK/AutoGen working, code errors fixed

#### 2.1 Fix Semantic Kernel API (30 min)

**Cells to Fix**: 100, 102, 189

**Current (BROKEN)**:
```python
result = await kernel.invoke_prompt(
    prompt_template="Say hello",
    settings={"service_id": service_id}
)
```

**Fixed (SK 1.37.0)**:
```python
from semantic_kernel.functions import KernelArguments

result = await kernel.invoke_prompt(
    function_name="my_prompt",
    prompt="Say hello",  # Changed from prompt_template
    arguments=KernelArguments(settings={"service_id": service_id})
)
```

OR use new chat completion API:
```python
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

chat_service = kernel.get_service(service_id)
result = await chat_service.get_chat_message_content(
    chat_history=[{"role": "user", "content": "Say hello"}]
)
```

#### 2.2 Fix AutoGen to use HTTP (20 min)

**Cell 98**: Change from SSE to HTTP

```python
# CURRENT (SSE - doesn't work)
mcp_server_url=f"{apim_resource_gateway_url}/weather/sse"

# FIXED (HTTP - works)
mcp_server_url=f"{apim_resource_gateway_url}/weather/mcp"
# OR use Container Instance directly
mcp_server_url="http://weather-mcp-72998.eastus.azurecontainer.io:8000/mcp"
```

#### 2.3 Fix Docs MCP KeyError (30 min)

**Cell 183-184**: Debug and fix MCP client KeyError

#### 2.4 Remove Agent Framework Cell (5 min)

**Cell 186**: Remove or comment out (package doesn't exist)

---

### **Phase 3: Configuration & Documentation**

**Duration**: 1 hour
**Outcome**: Known limitations documented, optional features disabled gracefully

#### 3.1 Document Model Deployment Limitations

**Cells**: 32, 113, 115, 136, 177-178

Add clear documentation:
```markdown
**Note**: dall-e-3 and image generation models not available due to SKU/quota limits.
This is expected and does not affect core AI Gateway functionality.
```

#### 3.2 Fix Spotify Helper (20 min)

**Cell 85**: Add `search_tracks` method or document limitation

#### 3.3 Fix Azure CLI msal Errors (20 min)

**Cells 76, 112**:
- Update Azure CLI: `az upgrade`
- OR add workaround with direct REST API calls

#### 3.4 Create Search Index (20 min)

**Cell 162**: Create AI Search index if needed or document as optional

---

### **Phase 4: Testing & Validation**

**Duration**: 2 hours
**Outcome**: Run All succeeds, all cells tested

#### 4.1 Incremental Testing
- Test cells 1-50 (basic features)
- Test cells 51-100 (MCP integration)
- Test cells 101-150 (advanced features)
- Test cells 151-210 (end-to-end)

#### 4.2 Create Test Report
Document:
- What works ✅
- What's documented as limitation 📝
- What still needs fixing ❌

---

## Fix Priority Order

### **IMMEDIATE (Blocks Everything)**
1. ✅ Restart 6 MCP Container Instances → Fixes 10+ cells
2. ✅ Fix Semantic Kernel API → Fixes cells 100, 102, 189
3. ✅ Fix AutoGen SSE→HTTP → Fixes cell 98
4. ✅ Fix Cosmos firewall → Fixes cell 160

### **HIGH (Major Features)**
5. Add load balancing policy → Fixes cell 48
6. Enable semantic cache → Fixes cell 107
7. Fix Docs MCP KeyError → Fixes cells 183-184
8. Fix Spotify helper → Fixes cell 85

### **MEDIUM (Nice to Have)**
9. Fix Azure CLI msal errors → Fixes cells 76, 112
10. Create search index → Fixes cell 162
11. Document image gen limitations → Fixes cells 32, 113, 115, 136, 177-178

### **LOW (Cleanup)**
12. Remove agent framework cell → Fixes cell 186
13. Remove duplicate cell 86
14. Consolidate cells 195+

---

## Success Criteria

### ✅ Run All Complete When:
- [ ] All MCP servers accessible (7/7 up)
- [ ] No blocking errors (red traceback stops execution)
- [ ] All critical cells execute (may show warnings/skips)
- [ ] Known limitations clearly documented in output
- [ ] User can run notebook start-to-finish without manual intervention

### 📊 Metrics
- **Cells Total**: 210
- **Cells Working**: ~50 (24%)
- **Cells Broken**: ~40 (19%)
- **Cells Blocked by MCP**: ~30 (14%)
- **Cells Optional/Doc**: ~30 (14%)
- **Cells Unknown**: ~60 (29%)

### 🎯 Target After Fixes
- **Cells Working**: 150+ (71%)
- **Cells Documented Skips**: 40 (19%)
- **Cells Still Broken**: <20 (10%)

---

## Next Steps

**IMMEDIATE ACTION**:
Start with Phase 1.1 - Restart MCP Container Instances

**Command**:
```bash
# Execute this to start fixing
cd /mnt/c/Users/lproux/OneDrive\ -\ Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab

# Test current MCP status first
python3 << 'EOF'
import httpx
servers = ["weather-mcp-72998", "oncall-mcp-72998"]
for s in servers:
    try:
        r = httpx.get(f"http://{s}.eastus.azurecontainer.io:8000/health", timeout=5)
        print(f"✅ {s}: {r.status_code}")
    except Exception as e:
        print(f"❌ {s}: {str(e)[:50]}")
EOF
```

**Then proceed to fixes in priority order.**

---

**Created**: 2025-11-15
**Last Updated**: 2025-11-15
**Status**: Ready to execute Phase 1.1
