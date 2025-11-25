# Quick Start: RBAC Configuration

## Problem Summary

- **Semantic Caching**: No cache hits (all requests show "Cache: UNKNOWN")
- **Cosmos DB**: 403 Forbidden error
- **Log Analytics**: PathNotFoundError

## Root Cause

APIM's system-assigned managed identity lacks permissions to access:
1. AI Services (for embeddings)
2. Cosmos DB (for message storage)
3. Log Analytics (for metrics)

## Solution: 3 Steps

### Step 1: Run RBAC Configuration Cell

```
Navigate to Cell 101 → Run Cell
```

This automatically grants all required permissions.

### Step 2: Wait 5-10 Minutes

RBAC changes take time to propagate across Azure.

```bash
# Optional: Verify role assignments
az role assignment list --assignee <apim-principal-id>
```

### Step 3: Test

| Feature | Cell | Expected Result |
|---------|------|-----------------|
| Semantic Caching | 102-103 | Cache hits: 19/20 (95%) |
| Cosmos DB | 121 | ✅ Message storage enabled |
| Log Analytics | 125 | ✅ Token metrics displayed |

## Permissions Granted

```
APIM Managed Identity
├── AI Services (foundry1)
│   └── Cognitive Services OpenAI User
├── Cosmos DB
│   ├── DocumentDB Account Contributor
│   └── Cosmos DB Account Reader Role
└── Log Analytics
    └── Log Analytics Reader
```

## Verification Commands

### Check APIM Principal ID
```bash
az apim show \
  --name apim-pavavy6pu5hpa \
  --resource-group lab-master-lab \
  --query identity.principalId \
  -o tsv
```

### Check All Role Assignments
```bash
# Replace <principal-id> with output from above
az role assignment list \
  --assignee <principal-id> \
  --all \
  -o table
```

### Check Specific Resources

#### AI Services
```bash
az cognitiveservices account show \
  --name foundry1-pavavy6pu5hpa \
  --resource-group lab-master-lab \
  --query name
```

#### Cosmos DB
```bash
az cosmosdb show \
  --name cosmos-pavavy6pu5hpa \
  --resource-group lab-master-lab \
  --query name
```

#### Log Analytics
```bash
az monitor log-analytics workspace show \
  --workspace-name workspace-pavavy6pu5hpa \
  --resource-group lab-master-lab \
  --query name
```

## Troubleshooting

### Semantic Caching Still Not Working?

1. **Lower threshold**: Change `score-threshold="0.8"` to `0.5` in Cell 102
2. **Check backend**: Verify `foundry1` backend exists in APIM
3. **Check model**: Verify `text-embedding-3-small` is deployed

### Cosmos DB Still Forbidden?

1. **Check IP**: Add current IP to Cosmos DB firewall
2. **Wait longer**: RBAC can take up to 15 minutes
3. **Check network**: Ensure firewall allows Azure services

### Log Analytics Still Not Found?

1. **Check deployment**: Verify workspace was created in deployment
2. **Check workspace ID**: Ensure correct workspace name
3. **Check subscription**: Ensure workspace is in same subscription

## Standard Subscription Note

Your **Standard subscription is NOT the issue**. Log Analytics, Cosmos DB, and Semantic Caching all work with Standard subscriptions. The issue was purely RBAC permissions.

## Manual PowerShell Alternative

If you prefer PowerShell over the automated cell:

```powershell
# Get APIM Principal ID
$apim = Get-AzApiManagement -ResourceGroupName "lab-master-lab" -Name "apim-pavavy6pu5hpa"
$principalId = $apim.Identity.PrincipalId

# Grant AI Services permission
New-AzRoleAssignment `
  -ObjectId $principalId `
  -RoleDefinitionName "Cognitive Services OpenAI User" `
  -Scope "/subscriptions/d334f2cd-3efd-494e-9fd3-2470b1a13e4c/resourceGroups/lab-master-lab/providers/Microsoft.CognitiveServices/accounts/foundry1-pavavy6pu5hpa"

# Grant Cosmos DB permissions
New-AzRoleAssignment `
  -ObjectId $principalId `
  -RoleDefinitionName "DocumentDB Account Contributor" `
  -Scope "/subscriptions/d334f2cd-3efd-494e-9fd3-2470b1a13e4c/resourceGroups/lab-master-lab/providers/Microsoft.DocumentDB/databaseAccounts/cosmos-pavavy6pu5hpa"

# Grant Log Analytics permission
New-AzRoleAssignment `
  -ObjectId $principalId `
  -RoleDefinitionName "Log Analytics Reader" `
  -Scope "/subscriptions/d334f2cd-3efd-494e-9fd3-2470b1a13e4c/resourceGroups/lab-master-lab/providers/Microsoft.OperationalInsights/workspaces/workspace-pavavy6pu5hpa"
```

## Timeline

- **RBAC Cell Execution**: 1-2 minutes
- **RBAC Propagation**: 5-10 minutes
- **Testing**: 5 minutes
- **Total**: ~15-20 minutes

## Success Indicators

### Semantic Caching Working
```
✓ Req  2 [IDENTICAL]: 0.089s (fast - cache HIT!) | Cache: HIT
Cache Hits: 19/20 (95.0%)
```

### Cosmos DB Working
```
✅ Cosmos DB connected successfully
✅ Database 'ConversationDB' ready
[OK] Message storage enabled
```

### Log Analytics Working
```
✅ Query successful
📊 Token Usage by Subscription: [table with data]
```

## Need Help?

See detailed troubleshooting in `RBAC-FIXES-README.md`
