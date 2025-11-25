# Phase 1: MCP Container Investigation Results

**Date**: 2025-11-15
**Phase**: Infrastructure Troubleshooting
**Status**: MCP containers diagnosed - restart did NOT fix the issue

---

## Executive Summary

All 6 MCP Container Instances were restarted, but only 1/7 remains functional. The containers are running at the OS level, but the MCP server applications inside are not responding on port 8000.

**Root Cause**: MCP server application deployment/configuration issue (not a simple restart problem)

---

## Container Instance Status

| Server | Azure Status | HTTP Status | Root Cause |
|--------|--------------|-------------|------------|
| docs-mcp-72998 | ✅ Running | ✅ 200 OK | Working correctly |
| weather-mcp-72998 | ✅ Running | ❌ Timeout | MCP app not listening on 8000 |
| oncall-mcp-72998 | ✅ Running | ❌ Timeout | MCP app not listening on 8000 |
| github-mcp-72998 | ✅ Running | ❌ Timeout | MCP app not listening on 8000 |
| spotify-mcp-72998 | ✅ Running | ❌ Timeout | MCP app not listening on 8000 |
| product-catalog-mcp-72998 | ✅ Running | ❌ Timeout | MCP app not listening on 8000 |
| place-order-mcp-72998 | ✅ Running | ❌ Timeout | MCP app not listening on 8000 |

---

## Diagnostic Results

### Container Logs Analysis

**Weather-mcp logs**:
- Server process running
- Uvicorn web server active
- **Problem**: All `/mcp` requests return 404 Not Found
- Receiving traffic but MCP endpoint not configured

**Oncall-mcp logs**:
- Same pattern as weather-mcp
- 404 errors on `/mcp` endpoint
- Application misconfiguration

**Docs-mcp logs (WORKING)**:
- `/health` endpoint: ✅ 200 OK
- `/mcp` endpoint: ✅ 307 Temporary Redirect (correct SSE pattern)
- This is the correct configuration

---

## Impact on Master Notebook

### Cells Blocked by MCP Failures (30+ cells)

**Directly Broken**:
- Cell 82-94: Lab 10 MCP examples (13 cells)
- Cell 96: Product catalog MCP
- Cell 98: AutoGen with MCP (SSE 404 errors)
- Cell 105: Workflow with MCP timeout
- Cell 146-150: MCP authorization tests (5 cells)

**Total Impact**: ~20-30 cells will fail due to MCP unavailability

---

## Actions Taken

1. ✅ Listed all MCP Container Instances - found 8 total
2. ✅ Checked Container Instance status - all 8 running
3. ✅ Tested HTTP connectivity - 1/7 responding
4. ✅ Reviewed container logs - found 404 errors on `/mcp`
5. ✅ Restarted 6 failing containers
6. ✅ Re-tested connectivity - still 1/7 (no improvement)
7. ✅ Analyzed docs-mcp (working) vs others (failing)

---

## Root Cause Analysis

### Why Restart Failed

The containers are running but the MCP server applications are not configured correctly:

1. **Container process**: ✅ Running
2. **Uvicorn web server**: ✅ Active
3. **MCP endpoint `/mcp`**: ❌ 404 Not Found
4. **Health endpoint `/health`**: ❌ Timeout/Not Found

### Comparison: Docs-MCP (Working) vs Others (Failing)

| Feature | docs-mcp | weather/oncall/etc |
|---------|----------|-------------------|
| Container running | ✅ Yes | ✅ Yes |
| Web server active | ✅ Yes | ✅ Yes |
| `/health` endpoint | ✅ 200 | ❌ Timeout |
| `/mcp` endpoint | ✅ 307 | ❌ 404 |
| SSE protocol | ✅ Working | ❌ Not configured |

---

## Next Steps

### SHORT-TERM: Workaround Solutions

1. **Change notebook to use HTTP instead of SSE**
   - User feedback: "by experience HTTP for MCP works better than SSE"
   - Update cell 98 (AutoGen) to use HTTP `/mcp` instead of SSE
   - Use docs-mcp-72998 (only working server) for all examples

2. **Skip MCP-dependent tests**
   - Document that 20-30 cells will be skipped
   - Add clear warnings in affected cells
   - Focus on non-MCP features for "Run All" success

### LONG-TERM: Proper Fix

**Requires User Action** (beyond notebook fixes):

1. Check Container Instance environment variables
2. Review MCP server deployment configuration
3. Compare docs-mcp deployment vs failing containers
4. Redeploy failing containers with correct configuration
5. Or provide working MCP server URLs/endpoints

---

## Recommendation

**DO NOT** spend more time troubleshooting MCP containers in this session.

**INSTEAD**:
1. ✅ Move to next priority: Fix Semantic Kernel API (cells 99, 101)
2. ✅ Fix AutoGen to use HTTP (cell 98)
3. ✅ Fix Cosmos DB firewall (cell 160)
4. ✅ Document MCP issues clearly in notebook
5. ✅ Focus on getting non-MCP cells working for "Run All"

**Rationale**:
- 6/7 MCP containers require redeployment (infrastructure work)
- User can fix MCP deployment separately
- Many cells (150+) don't depend on MCP
- Better to fix what we CAN fix now

---

## Summary

**What Worked**:
- ✅ Identified exact failure pattern (404 on `/mcp` endpoint)
- ✅ Found working example (docs-mcp)
- ✅ Ruled out simple restart as solution
- ✅ Documented impact on notebook cells

**What Didn't Work**:
- ❌ Container restart (problem is deployment/config, not runtime)
- ❌ Waiting for servers to "wake up" (not a scale-to-zero issue)

**Decision**:
- Move to next priority fixes
- Document MCP issues for user to resolve separately
- Focus on maximizing "Run All" success rate with available resources

---

**Created**: 2025-11-15
**Phase**: 1.1 - MCP Container Investigation
**Outcome**: Issue diagnosed but requires infrastructure fixes beyond notebook scope
