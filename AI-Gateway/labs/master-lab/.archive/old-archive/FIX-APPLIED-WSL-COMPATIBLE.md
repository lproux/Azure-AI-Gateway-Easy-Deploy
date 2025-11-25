# Fix Applied: WSL-Compatible RBAC Configuration

**Date**: 2025-11-18
**Issue**: FileNotFoundError when running RBAC configuration cell
**Root Cause**: Azure CLI (`az` command) not available in WSL environment
**Solution**: Replaced subprocess calls with Azure Python SDKs

---

## Problem

Original error when running Cell 101:
```
❌ Error: FileNotFoundError: [WinError 2] The system cannot find the file specified
```

This occurred because the cell was trying to execute `az` CLI commands via `subprocess.run()`, but the Azure CLI was not installed or accessible in the WSL (Windows Subsystem for Linux) environment.

---

## Solution Applied

### Changed Approach

**Before**: Used `subprocess` to call `az` CLI commands
```python
cmd = ['az', 'apim', 'show', '--name', apim_service_name, ...]
result = subprocess.run(cmd, ...)
```

**After**: Use Azure Python Management SDKs directly
```python
from azure.mgmt.apimanagement import ApiManagementClient
apim_client = ApiManagementClient(credential, subscription_id)
apim_service = apim_client.api_management_service.get(...)
```

### Benefits

1. **No az CLI dependency** - Works without Azure CLI installation
2. **Cross-platform** - Works on Windows, Linux, macOS, WSL
3. **More reliable** - Direct API calls, no subprocess overhead
4. **Better error handling** - Native Python exceptions instead of parsing CLI output

---

## New Cell Structure

### Cell 101: SDK Installation (NEW)
Installs required Azure SDK packages:
- `azure-mgmt-apimanagement`
- `azure-mgmt-cognitiveservices`
- `azure-mgmt-cosmosdb`
- `azure-mgmt-loganalytics`
- `azure-mgmt-authorization`
- `azure-identity`

**Run this cell first if you encounter ImportError**

### Cell 102: RBAC Configuration (UPDATED)
Configures all RBAC permissions using Azure Python SDKs:
- Gets APIM managed identity principal ID
- Grants permissions for Semantic Caching
- Grants permissions for Cosmos DB
- Grants permissions for Log Analytics

---

## How to Use

### Step 1: Install SDKs (if needed)

```python
# Run Cell 101 if you see ImportError
# This installs all required Azure SDK packages
```

**Expected Output**:
```
Installing required Azure SDK packages...
Installing azure-mgmt-apimanagement...
  ✅ azure-mgmt-apimanagement
Installing azure-mgmt-cognitiveservices...
  ✅ azure-mgmt-cognitiveservices
...
✅ Installation complete!
```

### Step 2: Run RBAC Configuration

```python
# Run Cell 102
```

**Expected Output**:
```
================================================================================
RBAC Configuration - Setting up permissions
================================================================================

[config] Subscription: d334f2cd...
[config] Resource Group: lab-master-lab
[config] APIM Service: apim-pavavy6pu5hpa

[step 1] Getting APIM managed identity...
✅ APIM Principal ID: fe3283fb-...

[step 2] Configuring semantic caching permissions...
[ai-services] Checking 3 potential AI Services resource(s)

[ai-services] Configuring: foundry1-pavavy6pu5hpa
   [assign] Granting 'Cognitive Services OpenAI User' role...
   ✅ Role assigned successfully

[ai-services] ✅ Configured 1 AI Services resource(s)

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

[info] Waiting 60 seconds for initial RBAC propagation...
   60 seconds remaining...
   50 seconds remaining...
   ...
✅ Initial propagation wait complete

You can now proceed to test the features in subsequent cells.
```

### Step 3: Wait for Propagation

**Important**: RBAC changes take 5-10 minutes to fully propagate. The cell includes a 60-second initial wait, but you may need to wait longer before testing.

### Step 4: Test Features

| Feature | Cell | Expected Result |
|---------|------|-----------------|
| Semantic Caching | 103-104 | Cache hits: ~95% |
| Cosmos DB | 122 | ✅ Message storage enabled |
| Log Analytics | 126 | ✅ Token metrics displayed |

---

## Technical Details

### SDK Packages Used

1. **ApiManagementClient** (`azure-mgmt-apimanagement`)
   - Get APIM service details
   - Retrieve managed identity principal ID

2. **CognitiveServicesManagementClient** (`azure-mgmt-cognitiveservices`)
   - Get AI Services (foundry) account details
   - Retrieve resource IDs for RBAC assignment

3. **CosmosDBManagementClient** (`azure-mgmt-cosmosdb`)
   - Get Cosmos DB account details
   - Retrieve resource IDs for RBAC assignment

4. **LogAnalyticsManagementClient** (`azure-mgmt-loganalytics`)
   - Get Log Analytics workspace details
   - Retrieve resource IDs for RBAC assignment

5. **AuthorizationManagementClient** (`azure-mgmt-authorization`)
   - List existing role assignments
   - Create new role assignments
   - Get role definition IDs by name

6. **DefaultAzureCredential** (`azure-identity`)
   - Authenticate with Azure using default credential chain
   - Works with Azure CLI, managed identity, environment variables, etc.

### Helper Functions

#### `get_role_definition_id(role_name, scope)`
Gets the Azure role definition ID by role name (e.g., "Cognitive Services OpenAI User").

#### `create_role_assignment(principal_id, role_name, scope, resource_name)`
Creates a role assignment if it doesn't already exist:
1. Checks if role is already assigned
2. Gets role definition ID
3. Creates role assignment with unique GUID
4. Handles conflicts gracefully

---

## Troubleshooting

### ImportError: No module named 'azure.mgmt.XXX'

**Solution**: Run Cell 101 (SDK Installation)

```python
# Cell 101 will install all required packages
```

### Authentication Error

**Solution**: Ensure you're authenticated with Azure

```bash
# In WSL terminal
az login

# Or set environment variables
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export AZURE_TENANT_ID="your-tenant-id"
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"
```

### Role Assignment Already Exists

This is **not an error** - the cell will detect existing role assignments and skip them:

```
✅ Role already assigned: Cognitive Services OpenAI User
```

### Resource Not Found

If a resource (foundry, Cosmos DB, Log Analytics) is not found, the cell will skip it and continue:

```
⚠️  Resource not found: foundry1-pavavy6pu5hpa
```

**Solution**: Verify the resource exists in Azure Portal and the name is correct.

---

## Verification

### Check RBAC Assignments via Azure Portal

1. Navigate to the resource (AI Services, Cosmos DB, or Log Analytics)
2. Go to **Access control (IAM)**
3. Click **Role assignments**
4. Look for assignments where the **Assignee** is your APIM service name
5. Verify the roles are assigned:
   - AI Services: "Cognitive Services OpenAI User"
   - Cosmos DB: "DocumentDB Account Contributor" + "Cosmos DB Account Reader Role"
   - Log Analytics: "Log Analytics Reader"

### Check via Azure CLI (if available)

```bash
# Get APIM principal ID
PRINCIPAL_ID=$(az apim show \
  --name apim-pavavy6pu5hpa \
  --resource-group lab-master-lab \
  --query identity.principalId \
  -o tsv)

# List all role assignments for APIM
az role assignment list \
  --assignee $PRINCIPAL_ID \
  --all \
  -o table
```

### Check via Python SDK

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient

credential = DefaultAzureCredential()
auth_client = AuthorizationManagementClient(credential, subscription_id)

# List all role assignments for APIM principal
assignments = list(auth_client.role_assignments.list_for_scope(
    scope=f"/subscriptions/{subscription_id}",
    filter=f"principalId eq '{apim_principal_id}'"
))

for assignment in assignments:
    print(f"Role: {assignment.role_definition_id.split('/')[-1]}")
    print(f"Scope: {assignment.scope}")
```

---

## Cell Numbering Reference

| Cell | Description | Status |
|------|-------------|--------|
| 100 | Markdown: Semantic Cache Performance | Unchanged |
| **101** | **SDK Installation** | **NEW** |
| **102** | **RBAC Configuration** | **UPDATED (SDK version)** |
| 103 | Semantic Caching Configuration | Shifted +2 |
| 104 | Semantic Caching Test | Shifted +2 |
| 122 | Cosmos DB Configuration | Shifted +2 |
| 126 | Log Analytics Metrics | Shifted +2 |

**Note**: All cells after 100 have been shifted by +2 positions.

---

## What Changed

### Files Modified

1. **master-ai-gateway-fix-MCP.ipynb**
   - Added Cell 101: SDK Installation
   - Updated Cell 102: RBAC Configuration (SDK version)
   - All subsequent cells shifted by +2

2. **FIX-APPLIED-WSL-COMPATIBLE.md** (this file)
   - Documentation of the fix

### Code Changes

**Removed**:
```python
import subprocess
cmd = ['az', 'apim', 'show', ...]
result = subprocess.run(cmd, ...)
```

**Added**:
```python
from azure.mgmt.apimanagement import ApiManagementClient
apim_client = ApiManagementClient(credential, subscription_id)
apim_service = apim_client.api_management_service.get(...)
```

---

## Next Steps

1. ✅ **Run Cell 101** (SDK Installation) - if you see ImportError
2. ✅ **Run Cell 102** (RBAC Configuration)
3. ⏱️ **Wait 5-10 minutes** for RBAC propagation
4. ✅ **Test Semantic Caching** (Cells 103-104)
5. ✅ **Test Cosmos DB** (Cell 122)
6. ✅ **Test Log Analytics** (Cell 126)

---

## Support

If you continue to encounter issues:

1. **Check Azure credentials**: Run `az account show` in WSL terminal
2. **Check subscription access**: Verify you have Contributor/Owner role on subscription
3. **Check resource existence**: Verify all resources exist in Azure Portal
4. **Check firewall rules**: Ensure your IP is allowed on Cosmos DB/other resources
5. **Check APIM identity**: Verify system-assigned identity is enabled on APIM

For detailed troubleshooting, see `RBAC-FIXES-README.md`.

---

## Summary

✅ Fixed FileNotFoundError by replacing az CLI calls with Azure Python SDKs
✅ Added SDK installation cell (Cell 101)
✅ Updated RBAC configuration cell (Cell 102)
✅ Cross-platform compatible (Windows/Linux/macOS/WSL)
✅ No external dependencies on az CLI

**Status**: Ready to run. Execute Cell 101 (if needed), then Cell 102, wait for propagation, and test!
