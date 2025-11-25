# MCP Server Deployment Plan
**Date**: 2025-11-15
**Objective**: Deploy all working MCP servers to lab-master-lab resource group

---

## MCP Server Images Found

### Available Container Images

| MCP Server | ACR | Image | Latest Tag | Status |
|------------|-----|-------|------------|--------|
| **Excel Analytics** | acrmcpwksp321028 | excel-analytics-mcp | v4 | ✅ Found & Working |
| **Research Docs** | acrmcpwksp321028 | research-docs-mcp | v2 | ✅ Found & Working |
| **Weather** | acriauylgmgqsk3i | weather-mcp-server | v0.2 | ✅ Found |
| **GitHub** | acr3ilfnkpe2evck | github-mcp-server | v0.2 | ✅ Found |
| **OnCall** | acriauylgmgqsk3i | oncall-mcp-server | v0.2 | ✅ Found |
| **CSV Analyzer** | acrrhethhu3l5tuk | csv-analyzer-mcp-server | v0.1 | ✅ Found |

### Missing / Different Implementation

| MCP Server | Implementation | Notes |
|------------|----------------|-------|
| **Product Catalog** | APIM MCP API | Implemented in mcp-from-api lab using APIM type:'mcp' |
| **Place Order** | APIM MCP API | Implemented in mcp-from-api lab using APIM type:'mcp' |
| **MS Learn** | APIM Passthrough | Proxies to https://learn.microsoft.com/api/mcp |
| **Spotify** | ❌ Removed | No reliable image found |

---

## Deployment Strategy

### Phase 1: Deploy Container Instance MCP Servers

Deploy the following MCP servers as Azure Container Instances in `lab-master-lab`:

#### 1. Excel Analytics MCP
```bash
Container Name: excel-mcp-master
Image: acrmcpwksp321028.azurecr.io/excel-analytics-mcp:v4
Port: 8000
Endpoint: http://excel-mcp-master.eastus.azurecontainer.io:8000
```

#### 2. Research Docs MCP
```bash
Container Name: docs-mcp-master
Image: acrmcpwksp321028.azurecr.io/research-docs-mcp:v2
Port: 8000
Endpoint: http://docs-mcp-master.eastus.azurecontainer.io:8000
```

#### 3. Weather MCP
```bash
Container Name: weather-mcp-master
Image: acriauylgmgqsk3i.azurecr.io/weather-mcp-server:v0.2
Port: 8080
Endpoint: http://weather-mcp-master.eastus.azurecontainer.io:8080
```

#### 4. GitHub MCP
```bash
Container Name: github-mcp-master
Image: acr3ilfnkpe2evck.azurecr.io/github-mcp-server:v0.2
Port: 8080
Endpoint: http://github-mcp-master.eastus.azurecontainer.io:8080
```

#### 5. CSV Analyzer MCP (Optional - for Excel alternative)
```bash
Container Name: csv-mcp-master
Image: acrrhethhu3l5tuk.azurecr.io/csv-analyzer-mcp-server:v0.1
Port: 8080
Endpoint: http://csv-mcp-master.eastus.azurecontainer.io:8080
```

### Phase 2: Configure APIM MCP APIs

For product-catalog, place-order, and ms-learn, use the mcp-from-api pattern:

1. Create REST APIs in APIM (or use existing)
2. Create MCP APIs of type `'mcp'` that wrap the REST operations
3. Endpoints will be:
   - Product Catalog: `https://apim-pavavy6pu5hpa.azure-api.net/product-catalog-mcp/mcp`
   - Place Order: `https://apim-pavavy6pu5hpa.azure-api.net/place-order-mcp/mcp`
   - MS Learn: `https://apim-pavavy6pu5hpa.azure-api.net/ms-learn-mcp/mcp`

### Phase 3: Update Notebook Configuration

Update master-lab.env and .mcp-servers-config:

```env
# Container Instance MCP Servers
EXCEL_MCP_URL=http://excel-mcp-master.eastus.azurecontainer.io:8000
DOCS_MCP_URL=http://docs-mcp-master.eastus.azurecontainer.io:8000
WEATHER_MCP_URL=http://weather-mcp-master.eastus.azurecontainer.io:8080
GITHUB_MCP_URL=http://github-mcp-master.eastus.azurecontainer.io:8080
CSV_MCP_URL=http://csv-mcp-master.eastus.azurecontainer.io:8080

# APIM MCP APIs
PRODUCT_CATALOG_MCP_URL=https://apim-pavavy6pu5hpa.azure-api.net/product-catalog-mcp
PLACE_ORDER_MCP_URL=https://apim-pavavy6pu5hpa.azure-api.net/place-order-mcp
MS_LEARN_MCP_URL=https://apim-pavavy6pu5hpa.azure-api.net/ms-learn-mcp
```

---

## Deployment Commands

### Prerequisites

1. **ACR Access**: Ensure the deployment has pull access to all ACRs
2. **Resource Group**: lab-master-lab
3. **Region**: eastus (for consistency with existing deployments)

### Deploy Container Instances

```bash
# Set variables
RG="lab-master-lab"
LOCATION="eastus"

# Excel MCP
az container create \
  --resource-group $RG \
  --name excel-mcp-master \
  --image acrmcpwksp321028.azurecr.io/excel-analytics-mcp:v4 \
  --dns-name-label excel-mcp-master \
  --ports 8000 \
  --cpu 1 \
  --memory 1 \
  --registry-login-server acrmcpwksp321028.azurecr.io \
  --registry-username <ACR_USERNAME> \
  --registry-password <ACR_PASSWORD>

# Docs MCP
az container create \
  --resource-group $RG \
  --name docs-mcp-master \
  --image acrmcpwksp321028.azurecr.io/research-docs-mcp:v2 \
  --dns-name-label docs-mcp-master \
  --ports 8000 \
  --cpu 1 \
  --memory 1 \
  --registry-login-server acrmcpwksp321028.azurecr.io \
  --registry-username <ACR_USERNAME> \
  --registry-password <ACR_PASSWORD>

# Weather MCP
az container create \
  --resource-group $RG \
  --name weather-mcp-master \
  --image acriauylgmgqsk3i.azurecr.io/weather-mcp-server:v0.2 \
  --dns-name-label weather-mcp-master \
  --ports 8080 \
  --cpu 1 \
  --memory 1 \
  --registry-login-server acriauylgmgqsk3i.azurecr.io \
  --registry-username <ACR_USERNAME> \
  --registry-password <ACR_PASSWORD>

# GitHub MCP
az container create \
  --resource-group $RG \
  --name github-mcp-master \
  --image acr3ilfnkpe2evck.azurecr.io/github-mcp-server:v0.2 \
  --dns-name-label github-mcp-master \
  --ports 8080 \
  --cpu 1 \
  --memory 1 \
  --registry-login-server acr3ilfnkpe2evck.azurecr.io \
  --registry-username <ACR_USERNAME> \
  --registry-password <ACR_PASSWORD>
```

---

## Clean Up Old Resources

### Delete Container Apps (wrong architecture)

```bash
az containerapp delete --name mcp-weather-pavavy6pu5 --resource-group lab-master-lab --yes
az containerapp delete --name mcp-github-pavavy6pu5 --resource-group lab-master-lab --yes
az containerapp delete --name mcp-product-catalog-pavavy6pu5 --resource-group lab-master-lab --yes
az containerapp delete --name mcp-place-order-pavavy6pu5 --resource-group lab-master-lab --yes
az containerapp delete --name mcp-ms-learn-pavavy6pu5 --resource-group lab-master-lab --yes

# Delete Container Apps Environment if no longer needed
az containerapp env delete --name cae-pavavy6pu5hpa --resource-group lab-master-lab --yes
```

---

## Testing Plan

After deployment, test each MCP server:

### Health Checks

```bash
# Excel MCP
curl http://excel-mcp-master.eastus.azurecontainer.io:8000/health

# Docs MCP
curl http://docs-mcp-master.eastus.azurecontainer.io:8000/health

# Weather MCP
curl http://weather-mcp-master.eastus.azurecontainer.io:8080/health

# GitHub MCP
curl http://github-mcp-master.eastus.azurecontainer.io:8080/health
```

### MCP Protocol Tests

```bash
# Test MCP /mcp endpoint (should return JSON-RPC response)
curl -X POST http://excel-mcp-master.eastus.azurecontainer.io:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'
```

### Notebook Cell Tests

Run cells in order:
1. Cell 10: MCP initialization
2. Cell 84: Weather MCP test
3. Cell 85: GitHub MCP test
4. Cell 89: Product Catalog test (if APIM API deployed)

---

## Success Criteria

- ✅ All Container Instances deployed and running
- ✅ Health endpoints return 200 OK
- ✅ MCP endpoints return JSON-RPC responses (not HTML)
- ✅ Notebook cells execute without `MCPError: Server did not return Mcp-Session-Id header`
- ✅ All MCP servers return expected outputs

---

## Rollback Plan

If deployment fails:
1. Container Instances can be deleted without affecting other resources
2. Revert to using existing servers in rg-mcp-workshop-1759321028
3. Update .mcp-servers-config to point back to old URLs

---

## Next Steps

1. **Get ACR Credentials**: Extract admin credentials from each ACR
2. **Deploy Container Instances**: Execute deployment commands
3. **Update Notebook**: Modify .mcp-servers-config and test
4. **Clean Up**: Remove unused Container Apps
5. **Document**: Update final configuration
