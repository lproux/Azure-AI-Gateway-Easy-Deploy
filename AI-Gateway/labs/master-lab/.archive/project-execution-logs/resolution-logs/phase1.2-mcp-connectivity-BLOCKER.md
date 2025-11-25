# Phase 1.2 - MCP Server Connectivity BLOCKER

**Timestamp**: 2025-11-14T02:50:00Z
**Phase**: 1.2
**Status**: BLOCKED
**Severity**: CRITICAL

## Issue Summary

All 7 MCP Container Apps are NOT DEPLOYED in the subscription. Connectivity test shows 100% failure rate (7/7 servers DOWN).

## MCP Servers Expected

| Server Name | Expected URL | Status |
|-------------|-------------|---------|
| weather | https://mcp-weather-pavavy6pu5.ambitiousfield-f6abdfb4.uksouth.azurecontainerapps.io | NOT FOUND |
| oncall | https://mcp-oncall-pavavy6pu5.ambitiousfield-f6abdfb4.uksouth.azurecontainerapps.io | NOT FOUND |
| github | https://mcp-github-pavavy6pu5.ambitiousfield-f6abdfb4.uksouth.azurecontainerapps.io | NOT FOUND |
| spotify | https://mcp-spotify-pavavy6pu5.ambitiousfield-f6abdfb4.uksouth.azurecontainerapps.io | NOT FOUND |
| product-catalog | https://mcp-product-catalog-pavavy6pu5.ambitiousfield-f6abdfb4.uksouth.azurecontainerapps.io | NOT FOUND |
| place-order | https://mcp-place-order-pavavy6pu5.ambitiousfield-f6abdfb4.uksouth.azurecontainerapps.io | NOT FOUND |
| ms-learn | https://mcp-ms-learn-pavavy6pu5.ambitiousfield-f6abdfb4.uksouth.azurecontainerapps.io | NOT FOUND |

## Investigation Results

### Connectivity Test
```
UP/WAKING: 0/7
DOWN/ERROR: 7/7
```

All servers timing out - both `/health` and root endpoints unreachable.

### Azure Resource Check
```bash
az containerapp list --resource-group lab-master-lab
# Result: []  (empty - no Container Apps in this RG)
```

## Root Cause

**MCP Container Apps are not deployed** in the Azure subscription.

## Configuration Found

The `.mcp-servers-config` file contains these URLs, suggesting they SHOULD exist:
```
WEATHER_MCP_URL=https://mcp-weather-pavavy6pu5.ambitiousfield-f6abdfb4.uksouth.azurecontainerapps.io
ONCALL_MCP_URL=https://mcp-oncall-pavavy6pu5.ambitiousfield-f6abdfb4.uksouth.azurecontainerapps.io
... (and 5 more)
```

Comment in config states: "Status: All servers deployed and accessible" - **THIS IS INCORRECT**

## Impact

### Cells Affected (15+)
- Cell 81: Weather MCP
- Cell 82: GitHub MCP
- Cell 85: Spotify MCP
- Cell 86: OnCall MCP
- Cell 89: OnCall MCP (duplicate)
- Cell 93: GitHub MCP analysis
- Cell 96: Product Catalog MCP
- Cell 99: Workflow MCP
- Cell 140: MCP health checks (all 7 servers)
- Cell 142: MCP testing (all 7 servers)
- Cell 144: MCP OAuth (all 7 servers)

**Total Impact**: ~15 cells cannot execute successfully

## Options to Resolve

### Option 1: Deploy MCP Container Apps (RECOMMENDED)
**Action**: Run deployment scripts in `/deploy` folder
- Check `deploy-04-mcp.bicep`
- Run `deploy_real_mcp_servers.sh` or `deploy_all_remaining_mcp_servers.sh`
- Verify deployment with `az containerapp list`

**Pros**: Enables all MCP functionality
**Cons**: Requires deployment time and Azure resources
**Estimated Time**: 30-60 minutes

### Option 2: Use Mock MCP Servers
**Action**: Create mock implementations for testing
**Pros**: Fast, no Azure resources needed
**Cons**: Violates "no mock testing" requirement - NOT ALLOWED per project requirements

### Option 3: Skip MCP Sections
**Action**: Document MCP cells as "requires deployment" and skip in testing
**Pros**: Allows progress on other cells
**Cons**: Leaves 15+ cells unfixed

### Option 4: Use Alternative MCP Servers
**Action**: Check if Container Instances are available instead
- Excel MCP: `http://excel-mcp-72998.eastus.azurecontainer.io:8000`
- Docs MCP: `http://docs-mcp-72998.eastus.azurecontainer.io:8000`

**Pros**: May have some working servers
**Cons**: Only 2 servers vs 7 needed

## Recommended Path Forward

**BLOCKED - USER DECISION REQUIRED**

**Question for User**:
Should I:
1. **Deploy the MCP Container Apps** using the deployment scripts?
2. **Investigate alternative MCP server locations** (different resource group/subscription)?
3. **Skip MCP sections** and continue with other Phase 1 fixes?
4. **Document as known limitation** and mark MCP cells as "deployment required"?

## Next Steps (Pending Decision)

- If Option 1: Execute deployment scripts, wait for deployment, retest
- If Option 2: NOT ALLOWED per requirements
- If Option 3: Move to Phase 1.3 (JWT auth) and document MCP as incomplete
- If Option 4: Test Container Instances, check for other deployed servers

## Files to Check

Deployment scripts:
- `/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab/deploy/deploy-04-mcp.bicep`
- `/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab/deploy/deploy_real_mcp_servers.sh`
- `/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab/deploy/deploy_all_remaining_mcp_servers.sh`

## Status Log

```
[2025-11-14T02:35:30Z] Phase 1.2 START - MCP Server Connectivity
[2025-11-14T02:45:00Z] Connectivity test complete - 7/7 DOWN
[2025-11-14T02:48:00Z] Azure resource check - NO CONTAINER APPS FOUND
[2025-11-14T02:50:00Z] BLOCKED - Awaiting user decision on deployment
```

---

**AWAITING USER INPUT TO PROCEED**
