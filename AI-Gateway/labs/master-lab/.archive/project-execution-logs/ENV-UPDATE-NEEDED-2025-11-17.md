# Environment Variables Update Needed - 2025-11-17

## Current Status

**master-lab.env** exists with many variables, but missing critical ones:

### ✅ Already Present
- APIM_GATEWAY_URL
- APIM_SERVICE_NAME
- APIM_API_KEY
- RESOURCE_GROUP=lab-master-lab
- LOCATION=uksouth
- REDIS, SEARCH, COSMOS, CONTENT_SAFETY endpoints and keys
- MCP server URLs

### ❌ Missing Critical Variables

**For Authentication (Service Principal)**:
```bash
# Not in .env file:
AZURE_CLIENT_ID=<service-principal-client-id>
AZURE_CLIENT_SECRET=<service-principal-secret>
AZURE_TENANT_ID=<azure-tenant-id>
SUBSCRIPTION_ID=d334f2cd-3efd-494e-9fd3-2470b1a13e4c  # Visible in paths but not as variable
```

**For Backend Pool (Load Balancing)**:
```bash
# Not in .env file:
AZURE_OPENAI_ENDPOINT_FOUNDRY1=<uk-south-endpoint>
AZURE_OPENAI_ENDPOINT_FOUNDRY2=<east-us-endpoint>
AZURE_OPENAI_ENDPOINT_FOUNDRY3=<norway-east-endpoint>
AZURE_OPENAI_KEY_FOUNDRY1=<key1>
AZURE_OPENAI_KEY_FOUNDRY2=<key2>
AZURE_OPENAI_KEY_FOUNDRY3=<key3>
```

**For APIM Configuration**:
```bash
# May be needed:
APIM_SERVICE_ID=/subscriptions/.../Microsoft.ApiManagement/service/apim-pavavy6pu5hpa
```

---

## Recommendations

### Option 1: Extract from Azure (Automated)
Run this script to auto-populate missing values from Azure:

```python
# Add to Cell 2 or create new cell after Cell 26
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient

subscription_id = "d334f2cd-3efd-494e-9fd3-2470b1a13e4c"
resource_group = "lab-master-lab"

# Get Azure foundry endpoints
credential = DefaultAzureCredential()
client = CognitiveServicesManagementClient(credential, subscription_id)

foundries = {}
for account in client.accounts.list_by_resource_group(resource_group):
    if 'foundry' in account.name:
        endpoint = account.properties.endpoint
        keys = client.accounts.list_keys(resource_group, account.name)

        if 'foundry1' in account.name:
            foundries['FOUNDRY1'] = (endpoint, keys.key1)
        elif 'foundry2' in account.name:
            foundries['FOUNDRY2'] = (endpoint, keys.key1)
        elif 'foundry3' in account.name:
            foundries['FOUNDRY3'] = (endpoint, keys.key1)

# Append to master-lab.env
with open('master-lab.env', 'a') as f:
    f.write('\n# Azure OpenAI Foundries (Auto-added)\n')
    f.write(f'SUBSCRIPTION_ID={subscription_id}\n')
    for name, (endpoint, key) in foundries.items():
        f.write(f'AZURE_OPENAI_ENDPOINT_{name}={endpoint}\n')
        f.write(f'AZURE_OPENAI_KEY_{name}={key}\n')
```

### Option 2: Manual Update (Quick)
User manually adds these lines to master-lab.env:

```bash
# Add to master-lab.env:

# ===========================================
# Azure Authentication
# ===========================================
SUBSCRIPTION_ID=d334f2cd-3efd-494e-9fd3-2470b1a13e4c
AZURE_CLIENT_ID=<from-service-principal-setup>
AZURE_CLIENT_SECRET=<from-service-principal-setup>
AZURE_TENANT_ID=<your-tenant-id>

# ===========================================
# Azure OpenAI Foundries (for Backend Pool)
# ===========================================
AZURE_OPENAI_ENDPOINT_FOUNDRY1=https://foundry1-pavavy6pu5hpa.openai.azure.com
AZURE_OPENAI_ENDPOINT_FOUNDRY2=https://foundry2-pavavy6pu5hpa.openai.azure.com
AZURE_OPENAI_ENDPOINT_FOUNDRY3=https://foundry3-pavavy6pu5hpa.openai.azure.com
AZURE_OPENAI_KEY_FOUNDRY1=<key-from-azure-portal>
AZURE_OPENAI_KEY_FOUNDRY2=<key-from-azure-portal>
AZURE_OPENAI_KEY_FOUNDRY3=<key-from-azure-portal>
```

### Option 3: Update .env Generation Cell (Best)
Update Cell 2 or the deployment output generation to automatically include these variables.

---

## Next Steps

1. **Choose option** (recommend Option 1 - automated extraction)
2. **Run extraction** or manual update
3. **Reload environment** with `load_dotenv('master-lab.env', override=True)`
4. **Verify** all cells can access needed variables
5. **Proceed** with notebook execution

---

**Status**: Waiting for user to select approach
**Priority**: HIGH (blocks execution)
**Estimated Time**: 5-10 minutes
