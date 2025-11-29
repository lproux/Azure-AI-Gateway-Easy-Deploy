# Master AI Gateway Lab

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/lproux/Azure-AI-Gateway-Easy-Deploy?quickstart=1)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)

> **Deploy once, explore 7 comprehensive AI Gateway labs in a single Jupyter notebook**

## Quick Start

### Option 1: GitHub Codespaces (Recommended)

1. Click the **Open in Codespaces** badge above
2. Wait 3-5 minutes for environment setup
3. Run: `az login --use-device-code`
4. Open `master-ai-gateway-deploy-from-notebook.ipynb`
5. Run cells in Section 0 to deploy infrastructure

### Option 2: Local Setup

```bash
# Clone and setup
git clone https://github.com/lproux/Azure-AI-Gateway-Easy-Deploy.git
cd Azure-AI-Gateway-Easy-Deploy/AI-Gateway/labs/master-lab

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Login to Azure
az login
az account set --subscription <your-subscription-id>

# Open notebook
code master-ai-gateway-deploy-from-notebook.ipynb
```

## Prerequisites

### Azure Requirements
- **Azure Subscription** with Contributor + RBAC Administrator (or Owner) role
- **Azure OpenAI** access ([Request here](https://aka.ms/oai/access))

### Tools
- Python 3.11+
- Azure CLI 2.50+
- VS Code with Jupyter extension

## What Gets Deployed

| Service | Purpose | Cost/Month |
|---------|---------|------------|
| API Management (StandardV2) | Central gateway | ~$175 |
| AI Foundry (3 regions) | AI models | Usage-based |
| Redis Enterprise | Semantic caching | ~$20 |
| Azure AI Search | Vector search/RAG | ~$75 |
| Cosmos DB | Message storage | ~$25 |
| Container Apps | 7 MCP servers | ~$30 |
| Log Analytics | Monitoring | ~$50 |
| **Total** | | **~$890-1,190** |

**Deployment Time:** 35-40 minutes

## Notebook Structure

The notebook contains **57 TOC links** organized into 4 sections:

### Section 0: Initialize and Deploy
Setup and deploy all Azure infrastructure (Cells 1-44)
- Environment detection, dependencies, Azure auth
- Deploy APIM, AI Foundry, supporting services
- Configure MCP servers

### Section 1: Core AI Gateway Features
9 labs with 17 subsections covering:
- **1.1** Advanced Caching & Storage (semantic caching with Redis)
- **1.2** Message Storing with Cosmos DB
- **1.3** Vector Searching with RAG
- **1.4** Zero to Production
- **1.5** Backend Pool Load Balancing
- **1.6** Token Metrics Emitting
- **1.7** Content Safety
- **1.8** Model Routing
- **1.9** AI Foundry SDK

### Section 2: MCP Fundamentals
7 labs covering Model Context Protocol:
- **2.1-2.3** Excel/Azure cost analysis via MCP
- **2.4** Function calling with MCP tools
- **2.5-2.6** GitHub integration
- **2.7** Multi-MCP AI aggregation

### Section 3: Semantic Kernel & AutoGen
6 labs covering advanced orchestration:
- **3.1-3.2** SK plugins and streaming
- **3.3** AutoGen multi-agent
- **3.4** SK with custom clients
- **3.5** Built-in LLM logging
- **3.6** Hybrid SK + AutoGen

## Authentication Methods

### Azure CLI (Recommended for Development)
```bash
az login
az account set --subscription <subscription-id>
```

### Service Principal (For Automation)
```bash
export AZURE_CLIENT_ID="<appId>"
export AZURE_TENANT_ID="<tenant>"
export AZURE_CLIENT_SECRET="<password>"
export AZURE_SUBSCRIPTION_ID="<subscription-id>"
```

### Managed Identity (For Azure-Hosted)
Automatically used when running on Azure compute.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `az login` required | Run `az login --use-device-code` (Codespaces) |
| Quota exceeded | Request increase in Azure Portal > Quotas |
| Deployment timeout | APIM takes 30-45 min (normal) |
| Module not found | `pip install -r requirements.txt` then restart kernel |
| Cosmos DB Forbidden | Add your IP to Cosmos DB firewall |

### Check Deployment Status
```bash
az deployment group show \
  --name <deployment-name> \
  --resource-group <rg-name> \
  --query properties.provisioningState
```

### View Container App Logs
```bash
az containerapp logs show \
  --name <app-name> \
  --resource-group <rg-name> \
  --tail 50
```

## Key Files

```
master-lab/
├── master-ai-gateway-deploy-from-notebook.ipynb  # Main notebook
├── master-ai-gateway-easy-deploy.ipynb           # Streamlined version
├── master-lab.env                                 # Generated config
├── requirements.txt                               # Python dependencies
├── .mcp-servers-config                           # MCP server URLs
├── notebook_mcp_helpers.py                       # Helper functions
├── deploy/                                        # Bicep templates
│   ├── deploy-01-core.bicep
│   ├── deploy-02-ai-foundry.bicep
│   ├── deploy-03-supporting.bicep
│   └── deploy-04-mcp.bicep
└── util/                                         # Deployment utilities
    └── deploy_all.py
```

## Cleanup

```bash
# Delete all resources (WARNING: Irreversible!)
az group delete --name <your-rg-name> --yes --no-wait

# Verify deletion
az group show --name <your-rg-name>
```

## Cost Optimization

1. **Use semantic caching** - Reduces API calls by 50-80%
2. **Start with gpt-4o-mini** - 15-20x cheaper than gpt-4
3. **Delete when not using** - Most services bill when idle
4. **Monitor with Lab 3.5** - Track token usage

## Resources

- [Azure API Management](https://learn.microsoft.com/azure/api-management/)
- [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Main Repository README](../../../README.md)

---

**Last Updated:** 2025-11-29 | **Version:** 2.0.0
