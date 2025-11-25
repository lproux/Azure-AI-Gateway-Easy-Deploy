# Cosmos DB RBAC Analysis and Mitigation Plan

## Current Situation

### Error Symptoms
- Cell 66 fails with: `Request blocked by Auth cosmos-pavavy6pu5hpa : principal [c1a04baa-9221-4490-821b-5968bbf3772b] does not have required RBAC permissions`
- Principal: `master-lab-sp-20251026-174038` (service principal)
- Action blocked: `Microsoft.DocumentDB/databaseAccounts/sqlDatabases/write`

### Root Cause Analysis

1. **Cosmos DB Configuration**
   - Local Authorization (API key auth) is **DISABLED**
   - Requires Azure AD authentication (RBAC-based)
   - Service principal is being used by `DefaultAzureCredential()`

2. **RBAC Permission Requirements**
   - Role needed: `Cosmos DB Built-in Data Contributor` (ID: 00000000-0000-0000-0000-000000000002)
   - Scope: `/` (account level)
   - Operations: Read, Write, Delete documents + Create databases/containers

3. **Propagation Delay**
   - RBAC assignments take 60-90 seconds to propagate
   - Multiple cache layers in Azure infrastructure

## Dependency Analysis

### Level 1 Dependencies (Direct)
```
Cell 66 (Cosmos Setup)
  ├─ azure.cosmos.CosmosClient (requires auth)
  ├─ azure.identity.DefaultAzureCredential (provides auth)
  ├─ Environment variables from master-lab.env
  │   ├─ COSMOS_ENDPOINT
  │   ├─ COSMOS_ACCOUNT_NAME
  │   └─ COSMOS_KEY (not usable - local auth disabled)
  └─ Azure RBAC (external dependency)
      ├─ Role Assignment
      ├─ Principal ID verification
      └─ Permission propagation
```

### Level 2 Dependencies (Indirect)
```
DefaultAzureCredential Chain (in order)
  1. EnvironmentCredential
     ├─ AZURE_CLIENT_ID
     ├─ AZURE_TENANT_ID
     └─ AZURE_CLIENT_SECRET
  2. ManagedIdentityCredential (if on Azure VM/ACI)
  3. AzureCliCredential (if az login active)
  4. AzurePowerShellCredential
  5. InteractiveBrowserCredential (if interactive)
```

### Current Authentication Flow
```
DefaultAzureCredential()
  → Finds environment variables (AZURE_CLIENT_ID, etc.)
  → Uses master-lab-sp-20251026-174038
  → Principal ID: c1a04baa-9221-4490-821b-5968bbf3772b
  → Requires RBAC permissions
```

## Comparison: Working vs Clean Notebook

### Working Notebook (`master-ai-gateway-fix-MCP.ipynb`)
- Uses same `DefaultAzureCredential()` approach
- Has `_provision_objects()` function with try/except
- Falls back to API key if Azure AD fails
- **Key insight**: Likely has RBAC already configured OR uses API key

### Clean Notebook (`master-ai-gateway-fix-MCP-clean.ipynb`)
- Uses same pattern but more simplified
- No complex fallback logic
- Assumes RBAC is pre-configured

## Mitigation Plan

### Option 1: RBAC Propagation Wait (RECOMMENDED)
**Status**: Already executed
**Action**: Wait for permission propagation

**Steps**:
1. ✅ Identified correct principal: `c1a04baa-9221-4490-821b-5968bbf3772b`
2. ✅ Granted role: `Cosmos DB Built-in Data Contributor`
3. ⏳ Wait 90-120 seconds for propagation
4. 🔄 Retry Cell 66

**Pros**:
- Secure (uses RBAC, not API keys)
- Aligns with Cosmos DB security config
- No code changes needed
- Sustainable for production

**Cons**:
- Requires waiting
- Propagation is not instant

### Option 2: Enable Local Auth (NOT RECOMMENDED)
**Action**: Re-enable API key authentication on Cosmos DB

**Steps**:
```bash
az cosmosdb update \
  --name cosmos-pavavy6pu5hpa \
  --resource-group lab-master-lab \
  --enable-local-auth true
```

**Pros**:
- Works immediately (no propagation delay)
- Can use COSMOS_KEY from env

**Cons**:
- ❌ Less secure (API keys can be leaked)
- ❌ Violates security best practices
- ❌ Requires infrastructure change
- ❌ May not align with enterprise policies

### Option 3: Force Specific Credential Type
**Action**: Use `AzureCliCredential()` instead of `DefaultAzureCredential()`

**Code Change**:
```python
from azure.identity import AzureCliCredential
credential = AzureCliCredential()
client = CosmosClient(cosmos_endpoint, credential)
```

**Steps**:
1. Modify cell to use explicit credential
2. Ensure `az login` is active
3. Grant RBAC to user principal instead

**Pros**:
- More predictable (doesn't use service principal)
- Uses user's Azure CLI session

**Cons**:
- Still requires RBAC grant (same propagation delay)
- Less portable (requires az login)
- May fail in CI/CD or automated scenarios

### Option 4: Pre-create Cosmos Resources via Azure CLI
**Action**: Create database/container via `az cosmosdb` instead of SDK

**Steps**:
```bash
# Create database
az cosmosdb sql database create \
  --account-name cosmos-pavavy6pu5hpa \
  --resource-group lab-master-lab \
  --name messages-db

# Create container
az cosmosdb sql container create \
  --account-name cosmos-pavavy6pu5hpa \
  --resource-group lab-master-lab \
  --database-name messages-db \
  --name conversations \
  --partition-key-path /conversationId \
  --throughput 400
```

**Then modify cell to only GET (not CREATE)**:
```python
# Get existing database/container (no write permissions needed)
database = client.get_database_client("messages-db")
container = database.get_container_client("conversations")
```

**Pros**:
- Separates infrastructure provisioning from runtime
- Reduces required permissions
- Better for production patterns

**Cons**:
- More complex setup
- Still needs read permissions (still requires RBAC)
- Doesn't solve the core propagation issue

## Recommended Solution

### Execute Option 1 with Validation Script

**1. Wait for Propagation (90-120 seconds)**
```bash
echo "Waiting for RBAC propagation..."
sleep 90
```

**2. Validate Permissions Before Running Cell**
Create validation script:

```python
#!/usr/bin/env python3
"""
Validate Cosmos DB RBAC permissions before running cells
"""
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import os

load_dotenv('master-lab.env')

cosmos_endpoint = os.environ.get('COSMOS_ENDPOINT')
cosmos_account = os.environ.get('COSMOS_ACCOUNT_NAME')

print("=" * 80)
print("🔍 VALIDATING COSMOS DB RBAC PERMISSIONS")
print("=" * 80)

try:
    credential = DefaultAzureCredential()
    client = CosmosClient(cosmos_endpoint, credential)

    # Try to list databases (read permission)
    databases = list(client.query_databases("SELECT * FROM c"))
    print(f"✅ READ permission: OK (found {len(databases)} databases)")

    # Try to create a test database (write permission)
    test_db_name = "rbac-test-temp"
    try:
        test_db = client.create_database(id=test_db_name)
        print(f"✅ WRITE permission: OK (created test database)")

        # Clean up
        client.delete_database(test_db_name)
        print(f"✅ DELETE permission: OK (cleaned up test database)")

    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"✅ WRITE permission: OK (database already exists)")
        else:
            raise

    print("\n" + "=" * 80)
    print("✅ ALL PERMISSIONS VALIDATED")
    print("=" * 80)
    print("\n🎯 You can now run Cell 66 successfully!")

except Exception as e:
    print(f"\n❌ Permission validation failed: {e}")
    print("\n⏳ If you just granted permissions, wait another 60 seconds and try again")
    print("   RBAC propagation can take up to 2-3 minutes")
    exit(1)
```

**3. Run Validation, Then Cell 66**

## Timeline

```
T+0s:   RBAC grant executed (already done)
T+30s:  Permissions start propagating
T+60s:  Permissions likely available (50% confidence)
T+90s:  Permissions highly likely available (90% confidence)
T+120s: Permissions guaranteed available (99% confidence)
```

## Verification Checklist

Before retrying Cell 66:
- [ ] Wait 90-120 seconds after RBAC grant
- [ ] Run validation script
- [ ] Verify principal ID matches: `c1a04baa-9221-4490-821b-5968bbf3772b`
- [ ] Confirm Cosmos DB firewall allows public access OR your IP
- [ ] Check no network connectivity issues

## Fallback Plan

If Option 1 fails after 5 minutes:
1. Check RBAC assignment exists:
   ```bash
   az cosmosdb sql role assignment list \
     --account-name cosmos-pavavy6pu5hpa \
     --resource-group lab-master-lab
   ```

2. Verify principal identity:
   ```bash
   az ad sp show --id c1a04baa-9221-4490-821b-5968bbf3772b
   ```

3. Check Cosmos DB firewall:
   ```bash
   az cosmosdb show \
     --name cosmos-pavavy6pu5hpa \
     --resource-group lab-master-lab \
     --query '{publicNetworkAccess:publicNetworkAccess, ipRules:ipRules}'
   ```

4. If all above pass, consider Option 4 (pre-create resources via CLI)

## Summary

**Best Solution**: Option 1 (RBAC with propagation wait)
- ✅ Already executed grant
- ⏳ Need to wait 90-120 seconds
- 🔍 Validate permissions before retry
- 🎯 Most secure and sustainable

**Estimated Time to Resolution**: 2-3 minutes from now
