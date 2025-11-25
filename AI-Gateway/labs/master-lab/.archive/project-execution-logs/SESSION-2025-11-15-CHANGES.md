# Session 2025-11-15 - Changes Applied

**Date**: 2025-11-15
**Status**: IN PROGRESS
**Objectives**: Fix Access Control, Update MCP images, Remove OnCall

---

## Summary of Changes

### 1. Access Control Section - FIXED ✅

**Issue**: Cell 61 was missing critical JWT authentication logic after redeploy

**Root Cause**:
- Missing `subscriptionRequired: false` logic
- Missing `<issuers>` element for v1.0/v2.0 token support
- Wrong policy type (API Key instead of JWT)

**Solution Applied**:
- Updated Cell 61 with working code from archive (`access-control-verbose.ipynb`)
- Added STEP 1: Disable subscription requirement for pure JWT auth
- Added STEP 2: Apply JWT policy with multi-issuer support (v1.0 + v2.0)
- Verified Cell 67 (Reset) already has correct subscriptionRequired re-enable logic

**Files Modified**:
- `master-ai-gateway-fix-MCP.ipynb` - Cell 61 (cell_id: cell_59_8f6ce564)

**Reference Documentation**:
- `analysis-reports/access-control-troubleshooting-complete.md`
- `analysis-reports/COMPLETION-SUMMARY.md`

---

### 2. MCP Docker Images - UPDATED ✅

**Issue**: All MCP servers using placeholder "helloworld" image

**Research Findings**:
- ✅ GitHub MCP: `ghcr.io/github/github-mcp-server:latest` (public)
- ✅ Weather MCP: `mcp/openweather:latest` (public Docker Hub)
- ✅ Spotify MCP: `richbai90/spotify-mcp:latest` (public Docker Hub)
- ❌ OnCall MCP: No public Docker image (Python package only)
- ❌ product-catalog, place-order, ms-learn: Intentional placeholders

**Solution Applied**:
- Removed 'oncall' from mcpServers array (7 → 6 servers)
- Added `mcpServerImages` variable mapping servers to Docker images
- Updated container template to use `mcpServerImages[server]`
- Compiled Bicep to JSON successfully

**Files Modified**:
- `deploy/deploy-04-mcp.bicep`
- `deploy/deploy-04-mcp.json` (auto-generated)

**New MCP Server Configuration**:
```bicep
var mcpServers = [
  'weather'      // mcp/openweather:latest
  'github'       // ghcr.io/github/github-mcp-server:latest
  'spotify'      // richbai90/spotify-mcp:latest
  'product-catalog'  // placeholder
  'place-order'      // placeholder
  'ms-learn'         // placeholder
]
```

---

### 3. OnCall MCP Server - REMOVED 🔄 IN PROGRESS

**Decision**: Remove OnCall completely (user approved)

**Rationale**:
- No public Docker image available
- Only distributed as Python package (`uvx pagerduty-mcp`)
- 3 other working MCP servers (GitHub, Weather, Spotify) sufficient for workshop

**Cells to Remove** (4 cells):
- [ ] Cell 84: OnCall MCP Server example
- [ ] Cell 88: OnCall engineers helper
- [ ] Cell 89: Lab 13 markdown header
- [ ] Cell 90: OnCall Schedule Access

**Cells to Update** (5 cells - remove oncall from lists):
- [ ] Cell 10: Unified MCP Initialization
- [ ] Cell 80: Lab 10 MCP Integration
- [ ] Cell 98: AutoGen MCP examples
- [ ] Cell 102: Semantic Kernel diagnostic
- [ ] Cell 108: Section 2 header

**Files to Modify**:
- `master-ai-gateway-fix-MCP.ipynb` - Remove 4 cells, update 5 cells
- Update any documentation/markdown referencing Lab 13

---

## Testing Plan

### Phase 1: Access Control Testing
**Cells to Test**: 60-67 (8 cells)
1. Cell 60: Baseline (No Auth) → Expected: 401
2. Cell 61: Apply JWT Policy → Expected: 200 (with subscriptionRequired disabled)
3. Cell 62: Test API Key → Expected: 200
4. Cell 63: (verify content)
5. Cell 64: Test JWT → Expected: 200
6. Cell 65: Apply Dual Auth → Expected: 200
7. Cell 66: Test Dual Auth → Expected: 200
8. Cell 67: Reset to API-KEY → Expected: 200

**Success Criteria**: All 8 cells execute without errors, status codes match expected

### Phase 2: MCP Deployment Testing
**After removing OnCall cells**:
1. Run Cell 32 (deployment) with updated Bicep
2. Verify 6 MCP container apps deploy successfully
3. Verify GitHub, Weather, Spotify use real images
4. Verify product-catalog, place-order, ms-learn use placeholder images
5. Test MCP endpoints return JSON-RPC (not HTML)

**Success Criteria**: 6/6 container apps running, 3/6 functional (real images)

### Phase 3: Full Sequential Test
1. Run all cells from 1 to end
2. Document any failures
3. Fix failures following testing protocol (A-L)
4. Repeat until 100% success

---

## Key Technical Details

### Access Control Fix - JWT Policy

**Critical Elements**:
1. **Disable subscriptionRequired**:
   ```python
   api_config['properties']['subscriptionRequired'] = False
   ```

2. **Multi-Issuer Support** (v1.0 + v2.0):
   ```xml
   <issuers>
     <issuer>https://sts.windows.net/{tenant}/</issuer>
     <issuer>https://login.microsoftonline.com/{tenant}/</issuer>
     <issuer>https://login.microsoftonline.com/{tenant}/v2.0</issuer>
   </issuers>
   ```

3. **Correct XML Element Order**:
   - `<openid-config>`
   - `<audiences>`
   - `<issuers>` (NOT before audiences!)

### MCP Images - Bicep Implementation

**Variable Declaration**:
```bicep
var mcpServerImages = {
  weather: 'mcp/openweather:latest'
  github: 'ghcr.io/github/github-mcp-server:latest'
  spotify: 'richbai90/spotify-mcp:latest'
  'product-catalog': 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
  'place-order': 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
  'ms-learn': 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
}
```

**Usage in Container Template**:
```bicep
image: mcpServerImages[server]
```

---

## Remaining Tasks

- [ ] Remove 4 OnCall-dedicated cells
- [ ] Update 5 cells that mention OnCall
- [ ] Test Access Control section (8 cells)
- [ ] Test MCP deployment with new images
- [ ] Full sequential notebook test
- [ ] Document final state
- [ ] Git commit (with user approval)

---

## Next Session Resume Point

If interrupted, resume with:
1. Read this document
2. Check TodoWrite for current task
3. Continue from "Remaining Tasks" section above

---

**Created**: 2025-11-15
**Updated**: 2025-11-15 (in progress)
**Session**: master-ai-gateway-fix-MCP.ipynb fixes
