# RBAC Configuration Fixes for Master Lab

**Created**: 2025-11-18
**Purpose**: Resolve permissions issues for Semantic Caching, Cosmos DB, and Log Analytics

## Summary of Issues

### 1. Semantic Caching (Cells 102-103)
**Problem**: No cache hits detected - all requests return "Cache: UNKNOWN"
**Root Cause**: APIM's system-assigned managed identity lacks permission to access AI Services (foundry1) for embeddings

### 2. Cosmos DB (Cell 121)
**Problem**: 403 Forbidden error when accessing Cosmos DB
**Root Cause**: APIM's managed identity lacks read/write permissions on Cosmos DB account

### 3. Log Analytics (Cell 125)
**Problem**: PathNotFoundError when querying Log Analytics workspace
**Root Cause**: Either workspace doesn't exist OR managed identity lacks Log Analytics Reader role

**Note**: Your Standard subscription is NOT the issue - Log Analytics works with all subscription types.

## Solution Implemented

### New Cell 101: RBAC Configuration

I've added a comprehensive RBAC configuration cell that automatically grants all necessary permissions:

**Cell Position**: Inserted after cell 100 (markdown header), before original cell 101
**Total Cells**: Now 141 (was 140)

### What the Cell Does

The new cell configures three sets of permissions:

#### 1. Semantic Caching Permissions
- **Role**: Cognitive Services OpenAI User
- **Assigned To**: APIM system-assigned managed identity
- **Scope**: All AI Services (foundry) resources in the resource group
- **Purpose**: Allows APIM to call embeddings API for semantic cache lookups

#### 2. Cosmos DB Permissions
- **Roles**:
  - DocumentDB Account Contributor (management plane)
  - Cosmos DB Account Reader Role (read operations)
- **Assigned To**: APIM system-assigned managed identity
- **Scope**: Cosmos DB account
- **Purpose**: Allows APIM to read/write conversation messages

#### 3. Log Analytics Permissions
- **Role**: Log Analytics Reader
- **Assigned To**: APIM system-assigned managed identity
- **Scope**: Log Analytics workspace
- **Purpose**: Allows querying token metrics and usage analytics

## How to Use

### Step 1: Run the New RBAC Cell

1. Open the notebook: `master-ai-gateway-fix-MCP.ipynb`
2. Navigate to **Cell 101** (new RBAC configuration cell)
3. Run the cell
4. Wait for completion (may take 1-2 minutes)

**Expected Output**:
```
================================================================================
RBAC Configuration - Setting up permissions
================================================================================

[config] Subscription: d334f2cd...
[config] Resource Group: lab-master-lab
[config] APIM Service: apim-pavavy6pu5hpa

[step 1] Getting APIM managed identity...
✅ APIM Principal ID: fe3283fb...

[step 2] Configuring semantic caching permissions...
[ai-services] Found 1 AI Services resource(s)

[ai-services] Configuring: foundry1-pavavy6pu5hpa
   [assign] Granting 'Cognitive Services OpenAI User' role...
   ✅ Role assigned successfully

[step 3] Configuring Cosmos DB permissions...
[cosmos] Account: cosmos-pavavy6pu5hpa
   [assign] Granting 'DocumentDB Account Contributor' role...
   ✅ Role assigned successfully
   [assign] Granting 'Cosmos DB Account Reader Role' role...
   ✅ Role assigned successfully

[step 4] Configuring Log Analytics permissions...
[log-analytics] Workspace: workspace-pavavy6pu5hpa
   [assign] Granting 'Log Analytics Reader' role...
   ✅ Role assigned successfully

================================================================================
✅ RBAC Configuration Complete
================================================================================

⏱️  Note: RBAC changes may take 5-10 minutes to propagate
```

### Step 2: Wait for RBAC Propagation

**Important**: Azure RBAC changes typically take **5-10 minutes** to fully propagate across all services.

Recommended approach:
1. Run Cell 101 (RBAC configuration)
2. Wait 5-10 minutes
3. Proceed with testing cells

### Step 3: Test Each Feature

#### Test Semantic Caching (Cells 102-103)

**Now Cell 102 and 103** (shifted by 1 due to new cell insertion)

Run Cell 102 to apply the semantic caching policy, then Cell 103 to test.

**Expected Result After Fix**:
```
✓ Req  1 [IDENTICAL]: 2.214s (slow - cache MISS) | Cache: MISS
✓ Req  2 [IDENTICAL]: 0.089s (fast - cache HIT!) | Cache: HIT
✓ Req  3 [IDENTICAL]: 0.092s (fast - cache HIT!) | Cache: HIT
...

Cache Hits: 19/20 (95.0%)
Cache Misses: 1/20 (5.0%)
```

#### Test Cosmos DB (Cell 121)

**Now Cell 122** (shifted by 1)

**Expected Result After Fix**:
```
================================================================================
Cosmos DB Message Storage Configuration
================================================================================
[config] Endpoint: https://cosmos-pavavy6pu5hpa.documents.azure.com:443/...
✅ Cosmos DB connected successfully
✅ Database 'ConversationDB' ready
✅ Container 'Messages' ready
[OK] Message storage enabled
```

#### Test Log Analytics (Cell 125)

**Now Cell 126** (shifted by 1)

**Expected Result After Fix**:
```
================================================================================
Log Analytics Token Metrics
================================================================================
[*] Querying Log Analytics workspace: /subscriptions/...
[*] Using Azure Monitor Query SDK
✅ Query successful

📊 Token Usage by Subscription:
   Subscription ID          Deployment       Total Tokens
   ------------------------ --------------- -------------
   abc123...                gpt-4o-mini          125,430
   def456...                gpt-4o-mini           89,220
```

## Understanding Your Backend Policy

Your current semantic caching policy is correct:

```xml
<policies>
    <inbound>
        <base />
        <check-header name="api-key" failed-check-httpcode="401"
                      failed-check-error-message="Missing or invalid API key" />
        <azure-openai-semantic-cache-lookup
            score-threshold="0.8"
            embeddings-backend-id="foundry1"
            embeddings-backend-auth="system-assigned" />
        <set-backend-service backend-id="inference-backend-pool" />
    </inbound>
    <backend>
        <base />
    </backend>
    <outbound>
        <azure-openai-semantic-cache-store duration="120" />
        <base />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>
```

### Key Elements:

1. **`embeddings-backend-auth="system-assigned"`**: Uses APIM's system-assigned managed identity
2. **`embeddings-backend-id="foundry1"`**: References the foundry1 backend for embeddings
3. **`score-threshold="0.8"`**: 80% similarity required for cache hit (adjustable)
4. **`duration="120"`**: Cache entries expire after 120 seconds

The policy is configured correctly - the issue was purely permissions.

## Troubleshooting

### If Semantic Caching Still Doesn't Work

1. **Verify backend exists**:
   ```bash
   az apim backend show \
     --service-name apim-pavavy6pu5hpa \
     --resource-group lab-master-lab \
     --backend-id foundry1
   ```

2. **Verify embeddings model is deployed**:
   - Azure Portal → AI Services (foundry1) → Model deployments
   - Look for: `text-embedding-3-small` or `text-embedding-ada-002`

3. **Check RBAC assignment**:
   ```bash
   az role assignment list \
     --assignee <apim-principal-id> \
     --scope /subscriptions/<subscription-id>/resourceGroups/lab-master-lab/providers/Microsoft.CognitiveServices/accounts/foundry1-pavavy6pu5hpa
   ```

4. **Lower similarity threshold**: Try `score-threshold="0.5"` for testing

### If Cosmos DB Still Fails

1. **Check firewall rules**: Your IP might have changed
   - Azure Portal → Cosmos DB → Networking
   - Add your current IP: `79.97.178.198` (or current IP)

2. **Verify RBAC roles**:
   ```bash
   az role assignment list \
     --assignee <apim-principal-id> \
     --scope /subscriptions/<subscription-id>/resourceGroups/lab-master-lab/providers/Microsoft.DocumentDB/databaseAccounts/cosmos-pavavy6pu5hpa
   ```

### If Log Analytics Still Fails

1. **Verify workspace exists**:
   ```bash
   az monitor log-analytics workspace show \
     --workspace-name workspace-pavavy6pu5hpa \
     --resource-group lab-master-lab
   ```

2. **Check deployment outputs**:
   - Cell output from `step1_outputs` should contain workspace ID
   - If missing, workspace might not have been created during deployment

3. **Verify RBAC**:
   ```bash
   az role assignment list \
     --assignee <apim-principal-id> \
     --scope /subscriptions/<subscription-id>/resourceGroups/lab-master-lab/providers/Microsoft.OperationalInsights/workspaces/workspace-pavavy6pu5hpa
   ```

## Alternative: Using Service Principal Instead of Managed Identity

If you prefer using a service principal instead of system-assigned managed identity:

### Create Service Principal

```bash
# Create service principal
az ad sp create-for-rbac --name "apim-lab-sp" --role Contributor \
  --scopes /subscriptions/<subscription-id>/resourceGroups/lab-master-lab

# Output will include:
# - appId (client ID)
# - password (client secret)
# - tenant
```

### Update Policy to Use Service Principal

```xml
<azure-openai-semantic-cache-lookup
    score-threshold="0.8"
    embeddings-backend-id="foundry1"
    embeddings-backend-auth="service-principal">
    <authentication-service-principal
        client-id="<app-id>"
        client-secret="<client-secret>"
        tenant-id="<tenant-id>" />
</azure-openai-semantic-cache-lookup>
```

### Grant Service Principal Permissions

```powershell
# PowerShell commands (as you mentioned preferring PowerShell)

# For AI Services (Semantic Caching)
New-AzRoleAssignment `
  -ObjectId <service-principal-object-id> `
  -RoleDefinitionName "Cognitive Services OpenAI User" `
  -Scope "/subscriptions/<subscription-id>/resourceGroups/lab-master-lab/providers/Microsoft.CognitiveServices/accounts/foundry1-pavavy6pu5hpa"

# For Cosmos DB
New-AzRoleAssignment `
  -ObjectId <service-principal-object-id> `
  -RoleDefinitionName "DocumentDB Account Contributor" `
  -Scope "/subscriptions/<subscription-id>/resourceGroups/lab-master-lab/providers/Microsoft.DocumentDB/databaseAccounts/cosmos-pavavy6pu5hpa"

# For Log Analytics
New-AzRoleAssignment `
  -ObjectId <service-principal-object-id> `
  -RoleDefinitionName "Log Analytics Reader" `
  -Scope "/subscriptions/<subscription-id>/resourceGroups/lab-master-lab/providers/Microsoft.OperationalInsights/workspaces/workspace-pavavy6pu5hpa"
```

**Note**: The current implementation uses managed identity (simpler, more secure, no credentials to manage).

## Cell Numbering Changes

After inserting the new RBAC cell, all subsequent cell numbers shifted by +1:

| Original | New | Description |
|----------|-----|-------------|
| Cell 101 | **Cell 101** | **NEW: RBAC Configuration** |
| Cell 101 | Cell 102 | Semantic Caching Configuration |
| Cell 102 | Cell 103 | Semantic Caching Test |
| Cell 120 | Cell 121 | Cosmos DB Configuration |
| Cell 124 | Cell 125 | Log Analytics Metrics |

## Expected Timeline

1. **Run Cell 101**: 1-2 minutes
2. **Wait for RBAC propagation**: 5-10 minutes
3. **Test Semantic Caching (Cells 102-103)**: 2-3 minutes
4. **Test Cosmos DB (Cell 121)**: < 1 minute
5. **Test Log Analytics (Cell 125)**: < 1 minute

**Total**: Approximately 15-20 minutes from start to finish

## Support

If issues persist after following this guide:

1. Check Azure Portal for role assignments:
   - API Management → Managed identities → System assigned → Azure role assignments

2. Review APIM diagnostic logs:
   - API Management → Diagnostics settings → Check for authentication errors

3. Verify all resources are in the same subscription and region

## References

- [Azure APIM Semantic Caching](https://learn.microsoft.com/en-us/azure/api-management/azure-openai-semantic-cache-lookup-policy)
- [Azure Managed Identities](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview)
- [Cosmos DB RBAC](https://learn.microsoft.com/en-us/azure/cosmos-db/role-based-access-control)
- [Log Analytics RBAC](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/manage-access)
