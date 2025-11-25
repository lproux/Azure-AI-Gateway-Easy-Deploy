# MCP Server Documentation for Master AI Gateway Lab

## Deployment Summary

**Date**: 2025-10-28  
**Status**: ✅ Successfully deployed 2 REAL MCP servers from workshop

---

## Deployed MCP Servers

### 1. Excel Analytics MCP Server
- **URL**: `http://excel-mcp-72998.eastus.azurecontainer.io:8000`
- **Status**: ✅ Healthy
- **Service**: excel-analytics-mcp v1.0.0
- **Platform**: Azure Container Instances (ACI)
- **Source**: Workshop `.archive/workshop-mcp/06-building-http-server/excel-analytics-mcp/`

**Capabilities**:
- Excel file analysis and data processing
- Sales performance analytics
- Data aggregation and grouping
- Chart generation and visualization
- Multi-sheet workbook support

**Key Tools**:
- `analyze_sales`: Analyze sales data with grouping options
- `upload_excel`: Upload and process Excel files
- `create_pivot`: Generate pivot tables from data
- `generate_chart`: Create visualizations from Excel data

---

### 2. Research Documents MCP Server
- **URL**: `http://docs-mcp-72998.eastus.azurecontainer.io:8000`
- **Status**: ✅ Healthy
- **Service**: research-docs-mcp v1.0.0
- **Platform**: Azure Container Instances (ACI)
- **Source**: Workshop `.archive/workshop-mcp/06-building-http-server/research-docs-mcp/`
- **Documents Available**: 3 research papers

**Capabilities**:
- Full-text document search across research papers
- Document retrieval and summarization
- Keyword-based search
- Document metadata extraction

**Key Tools**:
- `search_documents`: Search across all documents
- `get_document`: Retrieve specific document content
- `list_documents`: Get available documents list
- `search_by_keyword`: Find documents by keywords

---

## Docker Images

All images are stored in Azure Container Registry (ACR):
- **ACR Name**: acrmcp72998
- **ACR Server**: acrmcp72998.azurecr.io
- **Images**:
  - `excel-mcp:latest` - Excel Analytics server
  - `docs-mcp:latest` - Research Documents server

---

## Key Discovery

The master lab originally attempted to deploy 7 MCP servers (weather, oncall, github, spotify, product-catalog, place-order, ms-learn) as Azure Container Apps. However, **these were using placeholder demo images** (`mcr.microsoft.com/azuredocs/containerapps-helloworld:latest`) and **did not have real MCP server implementations**.

The workshop only ever deployed **2 real MCP servers** with actual Dockerfiles and Python/FastAPI implementations:
1. Excel Analytics MCP
2. Research Documents MCP

These 2 servers have been successfully deployed to Azure Container Instances and are working correctly.

---

## Usage in Notebook

```python
from notebook_mcp_helpers import MCPClient

# Initialize MCP client
mcp = MCPClient()

# Call Excel Analytics
result = mcp.excel.analyze_sales(
    file_path="/app/data/sales_performance.xlsx",
    group_by="Region"
)

# Call Research Documents
docs = mcp.docs.search_documents(
    query="machine learning",
    max_results=5
)
```

---

## Configuration Files

- **master-lab.env**: Contains `EXCEL_MCP_URL` and `DOCS_MCP_URL`
- **.mcp-servers-config**: MCP server configuration for notebook helpers
- **mcp-deployment-urls.txt**: Deployment reference with ACR and server URLs

---

## Health Check

Both servers expose `/health` endpoints:

```bash
curl http://excel-mcp-72998.eastus.azurecontainer.io:8000/health
# Returns: {"status":"healthy","service":"excel-analytics-mcp","version":"1.0.0","timestamp":"..."}

curl http://docs-mcp-72998.eastus.azurecontainer.io:8000/health
# Returns: {"status":"healthy","service":"research-docs-mcp","version":"1.0.0","timestamp":"...","documents_available":3}
```

---

## Architecture

```
┌─────────────────────────────────────────┐
│   Jupyter Notebook (master-ai-gateway.ipynb)   │
└──────────────┬──────────────────────────┘
               │
               │ notebook_mcp_helpers.py
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
┌───────────────┐  ┌───────────────┐
│  Excel MCP    │  │  Docs MCP     │
│  ACI          │  │  ACI          │
│  Port 8000    │  │  Port 8000    │
└───────────────┘  └───────────────┘
        │                   │
        └───────┬───────────┘
                │
        ┌───────▼────────┐
        │  ACR (acrmcp72998)  │
        │  Docker Images   │
        └─────────────────┘
```

---

## Troubleshooting

**If servers are not responding**:
1. Check server status: `az container show --name excel-mcp-72998 --resource-group lab-master-lab`
2. View logs: `az container logs --name excel-mcp-72998 --resource-group lab-master-lab`
3. Restart container: `az container restart --name excel-mcp-72998 --resource-group lab-master-lab`

**If deployment failed**:
- Verify ACR exists and has images: `az acr repository list --name acrmcp72998`
- Check resource group: `az group show --name lab-master-lab`
- Review deployment script: `./deploy_real_mcp_servers.sh`

---

## Future Enhancements

To add more MCP servers:
1. Create Dockerfile and server.py implementation (see workshop examples)
2. Add server code to `workshop/.archive/workshop-mcp/06-building-http-server/`
3. Build image: `az acr build --registry acrmcp72998 --image <server-name>:latest .`
4. Deploy to ACI: `az container create --name <server-name> --image acrmcp72998.azurecr.io/<server-name>:latest ...`
5. Update `.mcp-servers-config` and `notebook_mcp_helpers.py`

