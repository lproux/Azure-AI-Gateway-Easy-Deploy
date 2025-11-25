# Phase 1.6 - Infrastructure Fixes Reference

**Created**: 2025-11-14T05:00:00Z
**Purpose**: Document CLI and Portal methods to resolve backend service issues

---

## Cell 154: Cosmos DB Firewall

### Issue
```
ERROR: Request originated from IP 79.97.178.198 through public internet.
This is blocked by your Cosmos DB account firewall settings.
```

### Fix Option 1: Add Client IP via Azure CLI
```bash
# Get Cosmos DB account name
COSMOS_ACCOUNT=$(az cosmosdb list --resource-group lab-master-lab --query "[0].name" -o tsv)

# Add current client IP to firewall
CLIENT_IP="79.97.178.198"  # Or use: $(curl -s ifconfig.me)

az cosmosdb update \
  --resource-group lab-master-lab \
  --name $COSMOS_ACCOUNT \
  --ip-range-filter "$CLIENT_IP"

# Verify firewall rules
az cosmosdb show \
  --resource-group lab-master-lab \
  --name $COSMOS_ACCOUNT \
  --query "{ipRules:ipRules}" -o json
```

### Fix Option 2: Enable "Allow Azure Services" via CLI
```bash
COSMOS_ACCOUNT=$(az cosmosdb list --resource-group lab-master-lab --query "[0].name" -o tsv)

# Enable Azure services access
az cosmosdb update \
  --resource-group lab-master-lab \
  --name $COSMOS_ACCOUNT \
  --enable-public-network true \
  --enable-automatic-failover false

# Note: For production, use private endpoints instead
```

### Fix Option 3: Azure Portal
1. Navigate to: **Azure Portal → Cosmos DB → [Your Account] → Networking**
2. Under **Firewall**:
   - Option A: Add your IP address (click "+ Add my current IP")
   - Option B: Select "Allow access from Azure Portal" + "Allow access from Azure datacenters"
3. Click **Save**
4. Wait 1-2 minutes for changes to propagate

### Fix Option 4: Grant Service Principal Access (For CI/CD)
```bash
# Create managed identity or service principal
SP_NAME="cosmos-access-sp"
SP_JSON=$(az ad sp create-for-rbac --name $SP_NAME --role "Cosmos DB Account Reader Role" --scopes /subscriptions/$(az account show --query id -o tsv)/resourceGroups/lab-master-lab)

# Add to Cosmos DB access policies
COSMOS_ID=$(az cosmosdb show --resource-group lab-master-lab --name $COSMOS_ACCOUNT --query id -o tsv)

az role assignment create \
  --assignee $(echo $SP_JSON | jq -r '.appId') \
  --role "DocumentDB Account Contributor" \
  --scope $COSMOS_ID
```

### Verification
```bash
# Test connectivity from command line
az cosmosdb database list \
  --resource-group lab-master-lab \
  --name $COSMOS_ACCOUNT
```

---

## Cell 156: Azure AI Search Service

### Issue
```
404 - Resource not found
```

### Investigation: Check if Search Service Exists
```bash
# List all search services in resource group
az search service list \
  --resource-group lab-master-lab \
  --query "[].{name:name, location:location, sku:sku.name, status:provisioningState}" -o table

# If no services found, need to create one
```

### Fix Option 1: Create Search Service via CLI
```bash
SEARCH_NAME="search-$(openssl rand -hex 4)"  # Generate unique name

# Create Basic tier search service (free tier limited to 1 per subscription)
az search service create \
  --resource-group lab-master-lab \
  --name $SEARCH_NAME \
  --sku Basic \
  --location uksouth \
  --partition-count 1 \
  --replica-count 1

# Get admin key
SEARCH_KEY=$(az search admin-key show \
  --resource-group lab-master-lab \
  --service-name $SEARCH_NAME \
  --query primaryKey -o tsv)

# Get endpoint
SEARCH_ENDPOINT="https://${SEARCH_NAME}.search.windows.net"

echo "SEARCH_ENDPOINT=$SEARCH_ENDPOINT"
echo "SEARCH_ADMIN_KEY=$SEARCH_KEY"
```

### Fix Option 2: Azure Portal
1. Navigate to: **Azure Portal → Create a resource → Azure AI Search**
2. Configure:
   - **Resource group**: lab-master-lab
   - **Service name**: search-[unique] (e.g., search-aigateway)
   - **Location**: UK South (same as other resources)
   - **Pricing tier**: Basic (or Free if available)
3. Click **Review + Create** → **Create**
4. After deployment, go to **Keys** and copy **Primary admin key**
5. Note the **URL** (e.g., https://search-aigateway.search.windows.net)

### Fix Option 3: Update Notebook to Use Existing Service
```bash
# If search service exists with different name
ACTUAL_SEARCH=$(az search service list --resource-group lab-master-lab --query "[0].name" -o tsv)

# Update environment variable
export SEARCH_ENDPOINT="https://${ACTUAL_SEARCH}.search.windows.net"
export SEARCH_ADMIN_KEY=$(az search admin-key show --resource-group lab-master-lab --service-name $ACTUAL_SEARCH --query primaryKey -o tsv)
```

### Verification
```bash
# Test search service connectivity
curl -H "api-key: $SEARCH_ADMIN_KEY" \
  "$SEARCH_ENDPOINT/indexes?api-version=2021-04-30-Preview"
```

---

## Cell 162: Model Routing / Backend Pool

### Issue
```
[FALLBACK] No available model succeeded (all returned 404 or errors)
```

### Investigation: Check APIM Backend Configuration
```bash
# List all backends in APIM
az apim backend list \
  --resource-group lab-master-lab \
  --service-name apim-pavavy6pu5hpa \
  --query "[].{name:name, url:url, protocol:protocol}" -o table

# Check specific backend pool
az apim backend show \
  --resource-group lab-master-lab \
  --service-name apim-pavavy6pu5hpa \
  --backend-id inference-backend-pool
```

### Fix Option 1: Verify Foundry Endpoints
```bash
# Get all foundry endpoints
for foundry in foundry1-pavavy6pu5hpa foundry2-pavavy6pu5hpa foundry3-pavavy6pu5hpa; do
  echo "=== $foundry ==="
  ENDPOINT=$(az cognitiveservices account show \
    --resource-group lab-master-lab \
    --name $foundry \
    --query "properties.endpoint" -o tsv)

  STATE=$(az cognitiveservices account show \
    --resource-group lab-master-lab \
    --name $foundry \
    --query "properties.provisioningState" -o tsv)

  echo "Endpoint: $ENDPOINT"
  echo "State: $STATE"
  echo ""
done
```

### Fix Option 2: Test Foundry Accessibility
```bash
# Test foundry1 directly (bypass APIM)
FOUNDRY1_KEY=$(az cognitiveservices account keys list \
  --resource-group lab-master-lab \
  --name foundry1-pavavy6pu5hpa \
  --query key1 -o tsv)

FOUNDRY1_ENDPOINT=$(az cognitiveservices account show \
  --resource-group lab-master-lab \
  --name foundry1-pavavy6pu5hpa \
  --query "properties.endpoint" -o tsv)

# Test chat completion
curl -X POST "${FOUNDRY1_ENDPOINT}openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview" \
  -H "api-key: $FOUNDRY1_KEY" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello"}],"max_tokens":5}'
```

### Fix Option 3: Update APIM Backend URLs
```bash
# If backends are misconfigured, update them
# Example: Update foundry1 backend

FOUNDRY1_URL=$(az cognitiveservices account show \
  --resource-group lab-master-lab \
  --name foundry1-pavavy6pu5hpa \
  --query "properties.endpoint" -o tsv)

az apim backend update \
  --resource-group lab-master-lab \
  --service-name apim-pavavy6pu5hpa \
  --backend-id foundry1-backend \
  --url "$FOUNDRY1_URL" \
  --protocol http \
  --description "Foundry1 AI Services endpoint"
```

### Fix Option 4: Check for Rate Limiting / Throttling
```bash
# Check APIM gateway logs for throttling
az monitor activity-log list \
  --resource-group lab-master-lab \
  --max-events 50 \
  --query "[?contains(resourceId, 'apim-pavavy6pu5hpa')]" \
  -o table
```

---

## Cell 164: Log Analytics Workspace

### Issue
```
(PathNotFoundError) The requested path does not exist
```

### Investigation: Verify Workspace ID
```bash
# List all Log Analytics workspaces
az monitor log-analytics workspace list \
  --resource-group lab-master-lab \
  --query "[].{name:name, customerId:customerId, location:location}" -o table

# Get specific workspace details
WORKSPACE_NAME=$(az monitor log-analytics workspace list \
  --resource-group lab-master-lab \
  --query "[0].name" -o tsv)

WORKSPACE_ID=$(az monitor log-analytics workspace show \
  --resource-group lab-master-lab \
  --workspace-name $WORKSPACE_NAME \
  --query customerId -o tsv)

echo "WORKSPACE_ID=$WORKSPACE_ID"
```

### Fix Option 1: Verify APIM Diagnostic Settings
```bash
# Check if APIM is sending logs to workspace
az monitor diagnostic-settings list \
  --resource /subscriptions/$(az account show --query id -o tsv)/resourceGroups/lab-master-lab/providers/Microsoft.ApiManagement/service/apim-pavavy6pu5hpa \
  --query "value[].{name:name, workspaceId:workspaceId}" -o table
```

### Fix Option 2: Enable APIM Logging to Log Analytics
```bash
APIM_ID="/subscriptions/$(az account show --query id -o tsv)/resourceGroups/lab-master-lab/providers/Microsoft.ApiManagement/service/apim-pavavy6pu5hpa"

WORKSPACE_RESOURCE_ID="/subscriptions/$(az account show --query id -o tsv)/resourceGroups/lab-master-lab/providers/Microsoft.OperationalInsights/workspaces/$WORKSPACE_NAME"

# Create diagnostic setting
az monitor diagnostic-settings create \
  --resource $APIM_ID \
  --name "apim-to-log-analytics" \
  --workspace $WORKSPACE_RESOURCE_ID \
  --logs '[
    {"category": "GatewayLogs", "enabled": true},
    {"category": "WebSocketConnectionLogs", "enabled": true}
  ]' \
  --metrics '[
    {"category": "AllMetrics", "enabled": true}
  ]'
```

### Fix Option 3: Wait for Data Ingestion
```
Note: Log Analytics data ingestion has a 5-10 minute delay.
After enabling logging, wait 10 minutes before querying.
```

### Verification: Test Query
```bash
# Simple query to verify data
az monitor log-analytics query \
  --workspace $WORKSPACE_ID \
  --analytics-query "ApiManagementGatewayLogs | take 10" \
  --timespan P1D
```

---

## Cell 47: Load Balancing Region Detection

### Issue
```
All requests show "Region: Unknown"
```

### Root Cause
OpenAI Python SDK doesn't expose HTTP response headers that contain region information.

### Fix: Use Direct HTTP Requests with `requests` Library

**Current Approach** (doesn't work):
```python
response = client.chat.completions.create(...)  # SDK wraps response
region = response._headers.get('x-ms-region')   # _headers doesn't exist
```

**Fixed Approach** (see updated cell code):
```python
import requests

response = requests.post(
    url=f"{apim_gateway_url}/inference/openai/deployments/gpt-4o-mini/chat/completions",
    headers={"api-key": apim_api_key},
    json={"messages": [...], "max_tokens": 5}
)

# Now we can access headers
region = response.headers.get('x-ms-region', 'Unknown')
backend_id = response.headers.get('x-ms-backend-id', 'Unknown')
```

### APIM Policy to Add Region Headers

If region headers aren't being returned, add this to APIM policy (outbound section):

```xml
<outbound>
    <base />
    <!-- Add backend information to response headers -->
    <set-header name="x-ms-region" exists-action="override">
        <value>@(context.Deployment.Region)</value>
    </set-header>
    <set-header name="x-ms-backend-id" exists-action="override">
        <value>@(context.Request.MatchedParameters["backend-id"])</value>
    </set-header>
</outbound>
```

---

## Quick Reference: Service Principal Permissions

If using Service Principal for automation, grant these roles:

```bash
SP_ID="<your-service-principal-object-id>"
SUB_ID=$(az account show --query id -o tsv)
RG_ID="/subscriptions/$SUB_ID/resourceGroups/lab-master-lab"

# Cosmos DB access
az role assignment create \
  --assignee $SP_ID \
  --role "DocumentDB Account Contributor" \
  --scope "$RG_ID/providers/Microsoft.DocumentDB/databaseAccounts/<cosmos-name>"

# Search access
az role assignment create \
  --assignee $SP_ID \
  --role "Search Service Contributor" \
  --scope "$RG_ID/providers/Microsoft.Search/searchServices/<search-name>"

# APIM access
az role assignment create \
  --assignee $SP_ID \
  --role "API Management Service Contributor" \
  --scope "$RG_ID/providers/Microsoft.ApiManagement/service/apim-pavavy6pu5hpa"

# Log Analytics access
az role assignment create \
  --assignee $SP_ID \
  --role "Log Analytics Reader" \
  --scope "$RG_ID/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>"
```

---

## Validation Commands Summary

```bash
# Check all services status
echo "=== Cosmos DB ==="
az cosmosdb list --resource-group lab-master-lab --query "[].{name:name, state:provisioningState}" -o table

echo -e "\n=== Azure AI Search ==="
az search service list --resource-group lab-master-lab --query "[].{name:name, state:provisioningState}" -o table

echo -e "\n=== Cognitive Services (Foundries) ==="
az cognitiveservices account list --resource-group lab-master-lab --query "[].{name:name, state:provisioningState, location:location}" -o table

echo -e "\n=== APIM ==="
az apim show --resource-group lab-master-lab --name apim-pavavy6pu5hpa --query "{name:name, state:provisioningState, gateway:gatewayUrl}" -o table

echo -e "\n=== Log Analytics ==="
az monitor log-analytics workspace list --resource-group lab-master-lab --query "[].{name:name, state:provisioningState}" -o table
```

---

**Created**: 2025-11-14T05:00:00Z
**Updated**: Auto-updated with each fix implementation
**For**: Phase 1.6 - Backend Services Infrastructure Support
