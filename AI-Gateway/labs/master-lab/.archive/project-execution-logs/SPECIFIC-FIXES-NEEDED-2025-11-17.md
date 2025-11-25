# Specific Cell Fixes Needed - 2025-11-17

## Status Summary

**Notebook**: 158 cells (was 171 in baseline scan)
**Already Fixed**: 3 issues
**Remaining**: ~25 issues to review

---

## ✅ ALREADY FIXED

### 1. Excel Files (Cells 79, 82) - COMPLETE
- **Issue**: BadZipFile error (CDFV2 encrypted files)
- **Fix**: CSV conversion
- **Status**: ✅ DONE

### 2. Load Balancing Backend Pool (Cell 43) - COMPLETE
- **Issue**: Backend pool never created
- **Fix**: Inserted Cell 43 to create pool
- **Status**: ✅ DONE

### 3. Environment Variables - COMPLETE
- **Issue**: Missing SUBSCRIPTION_ID, foundry endpoints
- **Fix**: Auto-extracted from Azure
- **Status**: ✅ DONE

---

## 🔧 FIXES NEEDED (From BASELINE-SCAN)

**Note**: Cell numbers from baseline (171 cells) may have shifted

### CRITICAL Priority

#### 1. Cell 41: Client Undefined for Streaming
**Reported Issue**: Client variable not defined when streaming
**Current Status**: Need to verify if issue persists
**Fix Options**:
- A) Add client initialization before streaming block
- B) Check if earlier cell failed to create client
- C) Add error handling for undefined client

**Action**: Analyze Cell 41 and provide fix

#### 2. Cell 63: JWT Token Acquisition Failure
**Reported Issue**: JWT token acquisition fails
**Note**: "HAS WORKING VERSION IN ARCHIVE"
**Fix Options**:
- A) Restore working version from archive
- B) Update JWT configuration
- C) Fix token endpoint/scope

**Action**: Find archive version and restore

#### 3. Cell 75: Azure CLI MSAL Error
**Reported Issue**: Version compatibility issues
**Fix Options**:
- A) Update Azure CLI version
- B) Clear MSAL cache
- C) Use service principal instead of CLI

**Action**: Implement service principal fallback

#### 4. Cells 81-82: MCP Server Connectivity
**Reported Issue**: MCP servers not responding
**Current Status**: Some servers crash-looping
**Fix Options**:
- A) Verify MCP server URLs in .env
- B) Check server health endpoints
- C) Add retry logic with exponential backoff

**Action**: Test MCP connectivity and add error handling

#### 5. Cell 106: Model Routing Policy CLI Error
**Reported Issue**: CLI command failure
**Fix Options**:
- A) Update CLI command syntax
- B) Use REST API instead of CLI
- C) Check RBAC permissions

**Action**: Verify and fix CLI command

---

### HIGH Priority

#### 6. Cell 47: Load Balancing Region Detection
**Status**: ⚠️ May be resolved by Cell 43 backend pool fix
**Action**: Retest after Cell 43 executes

#### 7. Cell 85: Spotify MCP Missing Attribute
**Status**: ✅ Should be resolved (Spotify removed Nov 15)
**Action**: Verify Cell 85 no longer references Spotify

#### 8. Cell 93: GitHub MCP Fallback Issues
**Reported Issue**: Fallback logic fails
**Fix Options**:
- A) Add proper try-catch blocks
- B) Implement graceful degradation
- C) Add default values for missing data

**Action**: Review and add error handling

#### 9. Cells 96, 99: Product Catalog/Workflow MCP Timeouts
**Reported Issue**: MCP servers timeout
**Fix Options**:
- A) Increase timeout values
- B) Check if servers are running
- C) Add async handling

**Action**: Test server connectivity

#### 10-12. Cells 109, 130, 171: Image Generation 404 Errors
**Note**: Notebook now has 158 cells (not 171)
**Action**: Find equivalent cells and verify image endpoint URLs

#### 13-14. Cells 140, 142: MCP Server Health Check Failures
**Reported Issue**: Health checks fail
**Action**: Verify health endpoint URLs and add error handling

#### 15. Cell 154: Cosmos DB Firewall Blocking
**Reported Issue**: Firewall blocking access
**Fix Options**:
- A) Add IP to Cosmos DB firewall allow list
- B) Use private endpoint
- C) Enable "Allow Azure services" option

**Action**: Configure Cosmos DB firewall

#### 16. Cell 156: Search Index Creation Failure
**Reported Issue**: Index creation fails
**Fix Options**:
- A) Check search service permissions
- B) Verify index schema
- C) Check if index already exists

**Action**: Debug index creation

#### 17-18. Cells 160, 162: Model Routing Issues
**Reported Issue**: Routing configuration problems
**Action**: Review and fix routing policies

#### 19. Cell 177: MCP Docs Server Errors
**Note**: May not exist (notebook has 158 cells)
**Action**: Skip or find equivalent cell

---

### MEDIUM Priority

#### 20-21. Cells 22, 23: API_ID Configuration Warnings
**Reported Issue**: Configuration warnings
**Action**: Review and update configuration

#### 22. Cell 33: .env Generation Verification Needed
**Status**: ✅ Likely resolved (we verified .env)
**Action**: Double-check

#### 23. Cell 101: No Cache Indication
**Reported Issue**: Cache not showing status
**Action**: Add cache hit/miss logging

#### 24. Cell 107: Image Deployment Autodiscovery Failure
**Action**: Fix autodiscovery logic or use explicit URLs

#### 25. Cell 111: Missing RESOURCE_GROUP
**Status**: ✅ Should be resolved (RESOURCE_GROUP in .env)
**Action**: Verify

#### 26. Cell 164: Log Analytics Path Not Found
**Action**: Check log analytics configuration

---

## 📋 SYSTEMATIC FIX APPROACH

### Phase 1: Verify Current State (15 min)
For each CRITICAL issue:
1. Read the current cell code
2. Check if error still exists (cell numbers may have shifted)
3. Identify root cause

### Phase 2: Apply Fixes (45 min)
Priority order:
1. Cell 63: Restore JWT from archive (CRITICAL)
2. Cell 41: Fix client initialization (CRITICAL)
3. Cells 81-82: Fix MCP connectivity (CRITICAL)
4. Cell 75: Implement SP fallback (CRITICAL)
5. Cell 106: Fix CLI command (CRITICAL)

### Phase 3: Test Fixes (30 min)
- Run each fixed cell individually
- Verify error resolved
- Document any new issues

### Phase 4: HIGH Priority Fixes (60 min)
- Address remaining HIGH priority items
- Focus on cells with actual errors (not shifted numbering)

---

## 🎯 IMMEDIATE NEXT STEPS

1. **Map old cell numbers to new** (158 cells vs 171)
2. **Read Cell 41** and diagnose streaming issue
3. **Find JWT archive version** for Cell 63
4. **Test MCP servers** for Cells 81-82
5. **Create fix PRs** for each issue

---

## 📊 FIX TRACKING

| Cell | Issue | Priority | Status | Estimated Time |
|------|-------|----------|--------|----------------|
| 41 | Streaming client | CRITICAL | Pending | 15 min |
| 63 | JWT acquisition | CRITICAL | Pending | 10 min (restore) |
| 75 | Azure CLI MSAL | CRITICAL | Pending | 20 min |
| 81-82 | MCP connectivity | CRITICAL | Pending | 30 min |
| 106 | Model routing CLI | CRITICAL | Pending | 20 min |
| 47 | Load balancing | HIGH | Maybe fixed | 5 min (test) |
| 93 | GitHub MCP | HIGH | Pending | 15 min |
| 154 | Cosmos firewall | HIGH | Pending | 10 min |
| 156 | Search index | HIGH | Pending | 15 min |

**Total Estimated**: ~2-3 hours

---

**Status**: Ready to begin systematic fixes
**Next**: Analyze each CRITICAL cell and create specific fix code
**Updated**: 2025-11-17 02:30 UTC
