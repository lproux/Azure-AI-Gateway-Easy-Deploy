# Master AI Gateway Lab

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/yourusername/AI-Gateway?devcontainer_path=.devcontainer/devcontainer.json&quickstart=1)
[![Open in Dev Container](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/yourusername/AI-Gateway)

> **Comprehensive Azure AI Gateway experience consolidating 7 individual labs into one fully-documented Jupyter notebook**

## Overview

The Master AI Gateway Lab provides a complete, production-ready implementation of Azure API Management as an AI Gateway, combining seven essential labs into a single, cohesive learning experience. Deploy once, explore everything.

This lab demonstrates how to build enterprise-grade AI applications with proper access control, caching, vector search, load balancing, MCP integration, and comprehensive logging—all managed through Azure API Management.

## What's Included

This consolidated lab combines **7 individual labs** into one comprehensive environment:

| Lab | Name | Key Technologies | What You'll Learn |
|-----|------|------------------|-------------------|
| **Lab 08** | Access Control | OAuth 2.0, JWT, API Keys | Secure AI endpoints with multiple authentication methods |
| **Lab 09** | Semantic Caching | Redis, Embeddings | Accelerate responses 5-20x with semantic caching |
| **Lab 10** | Message Storing | Cosmos DB, SQL | Store and analyze AI conversations for compliance |
| **Lab 11** | Vector Search | AI Search, RAG | Implement retrieval-augmented generation patterns |
| **Lab 02** | Load Balancing | Multi-region, Failover | Distribute load across 3 Azure regions |
| **Lab 06** | MCP Integration | Model Context Protocol | Integrate 7 external data sources via MCP |
| **Lab 12** | Built-in Logging | Log Analytics, KQL | Monitor token usage and analyze AI performance |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  API Management (StandardV2)                     │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ - Access Control (OAuth 2.0, JWT, API Key)             │    │
│  │ - Semantic Caching (Redis-backed)                       │    │
│  │ - Message Storing (Cosmos DB)                           │    │
│  │ - Built-in Logging (Application Insights)              │    │
│  │ - Load Balancing (Multi-region with priority routing)  │    │
│  │ - MCP Integration (7 data sources)                      │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────┬──────────────┬──────────────┬─────────────────┘
                  │              │              │
        ┌─────────▼────────┐ ┌──▼───────────┐ ┌▼──────────────┐
        │ AI Foundry #1    │ │ AI Foundry #2│ │ AI Foundry #3 │
        │ (UK South)       │ │ (Sweden C.)  │ │ (West Europe) │
        │ Priority: 1      │ │ Priority: 2  │ │ Priority: 2   │
        │ 7 AI Models      │ │ gpt-4o-mini  │ │ gpt-4o-mini   │
        └──────────────────┘ └──────────────┘ └───────────────┘

Supporting Services:
├─ Redis Enterprise     (Semantic caching with RediSearch)
├─ Azure AI Search      (Vector search for RAG patterns)
├─ Cosmos DB           (Message storage and analytics)
├─ Content Safety      (Content moderation)
├─ Container Apps      (7 MCP servers)
├─ Log Analytics       (Centralized logging and monitoring)
└─ Application Insights (Performance and token metrics)
```

## Prerequisites

### Azure Requirements

- **Azure Subscription** with one of the following roles:
  - [Owner](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles/privileged#owner) (recommended for full access)
  - [Contributor](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles/privileged#contributor) + [RBAC Administrator](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles/privileged#role-based-access-control-administrator)

- **Azure Quota** requirements:
  - API Management StandardV2: 1 instance
  - Azure OpenAI: 7 model deployments (gpt-4o, gpt-4o-mini, gpt-4, dall-e-3, embeddings)
  - Redis Enterprise: 1 instance
  - Cognitive Search: 1 Basic tier instance
  - Cosmos DB: 1 account
  - Container Apps: 7 containers

### Development Tools

- **Python 3.11+** (Python 3.12 recommended) - [Download](https://www.python.org/)
- **Azure CLI** - [Install](https://learn.microsoft.com/cli/azure/install-azure-cli)
- **VS Code** with extensions:
  - [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)
  - [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
  - [Azure Tools](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

### Optional Tools

- **Docker Desktop** - For local MCP server development
- **Azure Developer CLI (azd)** - For infrastructure-as-code deployment
- **Git** - For version control and collaboration

## Quick Start

Choose the option that best fits your environment:

### Option 1: GitHub Codespaces (Fastest - One Click!)

Perfect for: Quick exploration, no local setup required

1. Click the "Open in GitHub Codespaces" badge at the top of this README
2. Wait 2-3 minutes for the environment to initialize
3. Open `master-ai-gateway-fix-MCP-clean-documented-final.ipynb`
4. Run cells in order starting from Section 0

**Advantages:**
- Zero local configuration
- Pre-configured development environment
- 60 hours/month free for GitHub users
- Full VS Code experience in browser

### Option 2: VS Code Dev Container (Local)

Perfect for: Consistent local development, offline work

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/AI-Gateway.git
   cd AI-Gateway/labs/master-lab
   ```

2. **Open in VS Code:**
   ```bash
   code .
   ```

3. **Reopen in Container:**
   - Press `F1` and select "Dev Containers: Reopen in Container"
   - Wait for container to build (5-10 minutes first time)

4. **Open the notebook:**
   ```bash
   # Automatically opens: master-ai-gateway-fix-MCP-clean-documented-final.ipynb
   ```

**Advantages:**
- Full isolation from your local environment
- Reproducible development environment
- Works offline after initial setup
- Faster than Codespaces after first build

### Option 3: Manual Setup (Traditional)

Perfect for: Maximum control, existing Python environment

1. **Clone and navigate:**
   ```bash
   git clone https://github.com/yourusername/AI-Gateway.git
   cd AI-Gateway/labs/master-lab
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Login to Azure:**
   ```bash
   az login
   az account set --subscription <your-subscription-id>
   ```

5. **Open the notebook in VS Code:**
   ```bash
   code master-ai-gateway-fix-MCP-clean-documented-final.ipynb
   ```

## Authentication Options

The lab supports three authentication methods. Choose based on your scenario:

### Method 1: Azure CLI (Recommended for Development)

**Best for:** Local development, interactive learning, getting started quickly

```bash
# Login interactively
az login

# Set your subscription
az account set --subscription <subscription-id>

# Verify
az account show
```

**Advantages:**
- Simplest to set up
- Uses your personal Azure credentials
- No additional configuration needed
- Great for learning and testing

**Use in notebook:**
```python
# Cells in Section 0 will automatically detect Azure CLI authentication
# No additional code needed
```

### Method 2: Service Principal (Recommended for Automation)

**Best for:** CI/CD pipelines, automation, production deployments

1. **Create service principal:**
   ```bash
   az ad sp create-for-rbac --name "master-lab-sp" \
     --role Contributor \
     --scopes /subscriptions/<subscription-id>/resourceGroups/<resource-group>
   ```

2. **Set environment variables:**
   ```bash
   export AZURE_CLIENT_ID="<appId from output>"
   export AZURE_TENANT_ID="<tenant from output>"
   export AZURE_CLIENT_SECRET="<password from output>"
   export AZURE_SUBSCRIPTION_ID="<subscription-id>"
   ```

3. **Or create `.env` file:**
   ```env
   AZURE_CLIENT_ID=<appId>
   AZURE_TENANT_ID=<tenant>
   AZURE_CLIENT_SECRET=<password>
   AZURE_SUBSCRIPTION_ID=<subscription-id>
   ```

**Advantages:**
- Non-interactive authentication
- Works in CI/CD pipelines
- Explicit permission scoping
- Credential rotation support

### Method 3: Managed Identity (Recommended for Azure-Hosted)

**Best for:** Azure VMs, Azure Container Apps, AKS

```python
from azure.identity import DefaultAzureCredential

# Automatically uses Managed Identity when running on Azure
credential = DefaultAzureCredential()
```

**Advantages:**
- No secrets to manage
- Automatic credential handling
- Highest security posture
- Best for production on Azure

**Requires:**
- Running on Azure compute (VM, Container App, AKS, etc.)
- Managed Identity enabled on the resource
- RBAC assignments to target resources

## Deployment Guide

### Step 1: Initialize Environment

Open `master-ai-gateway-fix-MCP-clean-documented-final.ipynb` and run **Section 0: Initialization & Deployment**

**Time:** 5 minutes
**Cells:** 1-27

This section will:
- Detect your OS and Python environment
- Install required packages
- Authenticate to Azure
- Set up helper functions
- Configure deployment variables

### Step 2: Deploy Core Infrastructure

Continue in Section 0, running the deployment cells.

**Time:** 15-20 minutes
**What gets deployed:**
- API Management (StandardV2)
- Log Analytics Workspace
- Application Insights

**Monitor progress:**
```bash
# In a separate terminal
az deployment group show \
  --name coreInfraDeployment \
  --resource-group <your-rg> \
  --query properties.provisioningState
```

### Step 3: Deploy AI Foundry

**Time:** 15-20 minutes
**What gets deployed:**
- 3 AI Foundry Hubs (UK South, Sweden Central, West Europe)
- 3 AI Foundry Projects
- 7 AI Models:
  - gpt-4o-mini (3 regions)
  - gpt-4o (UK South)
  - gpt-4 (UK South)
  - dall-e-3 (UK South)
  - text-embedding-3-small (UK South)
  - text-embedding-3-large (UK South)
  - text-embedding-ada-002 (UK South)

### Step 4: Deploy Supporting Services

**Time:** 5-10 minutes
**What gets deployed:**
- Redis Enterprise (for semantic caching)
- Azure AI Search (for vector search)
- Cosmos DB (for message storage)
- Content Safety (for content moderation)

### Step 5: Deploy MCP Servers (Optional)

**Time:** 5-10 minutes
**What gets deployed:**
- Container Apps Environment
- 7 MCP servers as container apps

**Total Deployment Time:** 35-40 minutes

## Lab Structure

The notebook is organized into 8 major sections with **152 cells total**:

### Section 0: Initialization & Deployment (Cells 1-27)

**Purpose:** Set up environment and deploy all Azure resources

**Key Topics:**
- Environment detection and package installation
- Azure authentication (3 methods)
- Infrastructure deployment with Bicep
- Configuration file generation
- Helper function definitions

**Documentation:** Comprehensive setup guide with authentication options, prerequisites, and troubleshooting

### Lab 08: Access Control (Cells 28-37)

**Purpose:** Secure AI endpoints with enterprise authentication

**What You'll Learn:**
- OAuth 2.0 and JWT token validation
- API key authentication
- Dual authentication (JWT + API key)
- Security best practices for AI APIs

**Tests Included:**
1. No authentication (401 expected)
2. JWT token authentication
3. JWT-only validation
4. Dual authentication
5. API key-only authentication

### Lab 09: Semantic Caching (Cells 38-44)

**Purpose:** Accelerate AI responses with intelligent caching

**What You'll Learn:**
- How semantic caching works with embeddings
- Redis integration with RediSearch
- Cache hit/miss analysis
- Performance improvements (5-20x faster)
- Cost savings from cache hits

**Includes:**
- Performance comparison charts
- Cache statistics visualization
- Redis query examples

### Lab 10: Message Storing (Cells 45-49)

**Purpose:** Store and analyze AI conversations for compliance

**What You'll Learn:**
- Cosmos DB integration with APIM
- Message schema design
- SQL queries for analytics
- Token usage tracking
- Compliance and auditing patterns

### Lab 11: Vector Search (Cells 50-62)

**Purpose:** Implement RAG (Retrieval Augmented Generation) patterns

**What You'll Learn:**
- Vector embeddings generation
- Azure AI Search indexing
- Semantic search queries
- RAG pattern implementation
- Source citation and grounding

### Lab 02: Load Balancing (Cells 63-94)

**Purpose:** Distribute AI traffic across multiple regions

**What You'll Learn:**
- Multi-region backend pools
- Priority-based routing
- Health checks and failover
- Load balancing strategies
- High availability patterns

### Lab 06: MCP Integration (Cells 95-119)

**Purpose:** Integrate external data sources via Model Context Protocol

**What You'll Learn:**
- MCP server deployment
- APIM as unified gateway
- Cross-domain data aggregation
- AI orchestration patterns
- Multi-source analysis

**7 MCP Servers Included:**
- Weather API
- GitHub API
- Time/Date service
- File system access
- Web search
- Database connector
- Custom business logic

### Lab 12: Built-in Logging (Cells 120-152)

**Purpose:** Monitor and analyze AI usage with built-in logging

**What You'll Learn:**
- Log Analytics integration
- KQL queries for AI metrics
- Token usage by model
- Cost allocation and chargeback
- Compliance considerations
- PII handling in logs

**Queries Included:**
- Token usage by model
- Token usage by subscription
- Cost analysis
- Prompt and completion viewing

## Folder Structure

```
master-lab/
├── .devcontainer/
│   ├── devcontainer.json           # VS Code Dev Container configuration
│   └── post-create.sh              # Environment setup script
│
├── .archive/                        # Historical notebooks and reports
│   └── analysis-reports/           # Detailed analysis documents
│
├── deploy/                          # Bicep deployment modules
│   ├── deploy-01-core.bicep        # APIM, Log Analytics, App Insights
│   ├── deploy-02-ai-foundry.bicep  # AI Foundry Hubs + Models
│   ├── deploy-03-supporting.bicep  # Redis, Search, Cosmos, Content Safety
│   └── deploy-04-mcp.bicep         # Container Apps + MCP servers
│
├── infra/                           # Azure Developer CLI infrastructure
│   ├── main.bicep                  # Main orchestration template
│   └── main.parameters.json        # Parameter values
│
├── images/                          # Architecture diagrams and screenshots
├── logs/                            # Execution logs
├── mcp-http-wrappers/              # MCP server implementations
├── policies/                        # APIM policy XML files
├── sample-data/                     # Test data for labs
│
├── master-ai-gateway-fix-MCP-clean-documented-final.ipynb  # Main notebook (USE THIS)
├── NOTEBOOK_DOCUMENTATION_README.md                        # Documentation guide
├── DOCUMENTATION_SUMMARY.md                                # Coverage report
├── requirements.txt                                        # Python dependencies
├── azure.yaml                                              # Azure Developer CLI config
└── README.md                                               # This file
```

## Cost Estimation

### Monthly Cost Breakdown

| Service | SKU/Tier | Estimated Monthly Cost | Notes |
|---------|----------|------------------------|-------|
| **API Management** | StandardV2 | ~$175 | Core gateway service |
| **AI Foundry (3 regions)** | Pay-per-use | ~$0 base | Model usage billed separately |
| **AI Model Usage** | Various | ~$500-800 | Varies by usage (see below) |
| **Redis Enterprise** | Balanced_B0 | ~$20 | Semantic caching |
| **Azure AI Search** | Basic | ~$75 | Vector search |
| **Cosmos DB** | Serverless | ~$25 | Message storage (low usage) |
| **Content Safety** | S0 | Pay-per-use | ~$10 for moderate usage |
| **Container Apps** | Consumption | ~$30 | 7 MCP servers |
| **Log Analytics** | Pay-per-GB | ~$50 | Depends on ingestion volume |
| **Application Insights** | Included | ~$0 | Included with Log Analytics |
| **Storage** | Standard | ~$5 | Logs and backups |
| **TOTAL** | | **~$890-1,190/month** | Varies by usage |

### AI Model Usage Cost Examples

Based on [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/):

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Typical Cost for 100 requests |
|-------|----------------------|------------------------|------------------------------|
| gpt-4o-mini | $0.15 | $0.60 | ~$0.08 |
| gpt-4o | $2.50 | $10.00 | ~$1.26 |
| gpt-4 | $30.00 | $60.00 | ~$9.00 |
| text-embedding-3-small | $0.02 | N/A | ~$0.001 |

**Cost Optimization Tips:**
1. Use semantic caching to reduce redundant calls (50-80% cache hit rate possible)
2. Start with gpt-4o-mini for development ($15-20x cheaper than gpt-4)
3. Enable load balancing to leverage reserved capacity across regions
4. Monitor usage with Lab 12 logging to identify optimization opportunities
5. Delete resources when not actively using: `az group delete --name <rg-name>`

## Troubleshooting

### Common Issues and Solutions

#### Issue: "Azure CLI not found"

**Solution:**
```bash
# Install Azure CLI
# Windows (PowerShell as Admin):
winget install Microsoft.AzureCLI

# macOS:
brew install azure-cli

# Linux:
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Verify
az --version
```

#### Issue: "Please run 'az login' to setup account"

**Solution:**
```bash
# Login interactively
az login

# Or use device code flow (for remote/container environments)
az login --use-device-code

# Verify
az account show
```

#### Issue: "Insufficient quota for AI models"

**Solution:**
1. Check current quota:
   ```bash
   az cognitiveservices usage list \
     --location uksouth \
     --query "[?name.value=='OpenAI.Standard.gpt-4o']"
   ```

2. Request quota increase in Azure Portal:
   - Navigate to **Azure OpenAI** > **Quotas**
   - Click **Request quota increase**
   - Select model and desired capacity
   - Submit request (usually approved within 1-2 business days)

3. Or modify `deploy/deploy-02-ai-foundry.bicep` to reduce model capacities

#### Issue: "Deployment timeout" or "Long-running operation failed"

**Solution:**
```bash
# Check deployment status
az deployment group show \
  --name <deployment-name> \
  --resource-group <rg-name> \
  --query properties.provisioningState

# View detailed errors
az deployment group show \
  --name <deployment-name> \
  --resource-group <rg-name> \
  --query properties.error

# Common causes:
# - API Management takes 30-45 minutes (this is normal)
# - AI model deployments queued (retry after quota increase)
# - Region capacity issues (try different region)
```

#### Issue: "ModuleNotFoundError" when running notebook

**Solution:**
```bash
# Ensure you're using the correct Python environment
# Check current Python:
which python  # Should point to .venv/bin/python

# Reinstall requirements:
pip install --upgrade -r requirements.txt

# Verify key packages:
pip list | grep -E "openai|azure|mcp|httpx"
```

#### Issue: Cells fail with authentication errors

**Solution:**
Check your authentication method:

```python
# In a notebook cell, verify credentials:
from azure.identity import DefaultAzureCredential

try:
    credential = DefaultAzureCredential()
    # This will raise an error if no valid credential is found
    token = credential.get_token("https://management.azure.com/.default")
    print("✓ Authentication successful")
except Exception as e:
    print(f"✗ Authentication failed: {e}")
```

#### Issue: MCP servers not accessible

**Solution:**
```bash
# Check Container Apps status
az containerapp list \
  --resource-group <rg-name> \
  --output table

# View logs for specific MCP server
az containerapp logs show \
  --name <mcp-server-name> \
  --resource-group <rg-name> \
  --tail 50

# Restart a specific MCP server
az containerapp revision restart \
  --name <mcp-server-name> \
  --resource-group <rg-name>
```

#### Issue: Redis cache connection failures

**Solution:**
```bash
# Get Redis connection string
az redis show \
  --name <redis-name> \
  --resource-group <rg-name> \
  --query hostName

# Test connectivity from notebook:
import redis
r = redis.Redis(
    host='<redis-hostname>',
    port=10000,
    password='<redis-key>',
    ssl=True
)
r.ping()  # Should return True
```

### Getting Help

If you encounter issues not covered here:

1. **Check the cell-specific documentation** in the notebook
2. **Review Section 0 troubleshooting** for setup issues
3. **Check Azure service health**: [Azure Status](https://status.azure.com/)
4. **Review logs**:
   ```bash
   # APIM logs
   az monitor app-insights query \
     --app <app-insights-name> \
     --analytics-query "requests | limit 50"
   ```
5. **Create an issue** in the GitHub repository with:
   - Error message (full text)
   - Cell number where error occurred
   - Steps to reproduce
   - Environment details (OS, Python version)

## Cleanup

### Delete All Resources

To remove all deployed resources and stop incurring charges:

```bash
# Delete the resource group (WARNING: This is irreversible!)
az group delete \
  --name <your-resource-group-name> \
  --yes \
  --no-wait

# Verify deletion (will show "NotFound" when complete)
az group show --name <your-resource-group-name>
```

### Selective Resource Deletion

To keep some resources:

```bash
# List all resources
az resource list \
  --resource-group <rg-name> \
  --output table

# Delete specific resource
az resource delete \
  --resource-group <rg-name> \
  --name <resource-name> \
  --resource-type <resource-type>

# Example: Delete only APIM (most expensive)
az apim delete \
  --name <apim-name> \
  --resource-group <rg-name> \
  --yes
```

### Cost-Saving Mode

To pause without deleting:

```bash
# Scale down APIM (not available for V2 SKUs - must delete)
# Scale down Container Apps
az containerapp scale \
  --name <mcp-server-name> \
  --resource-group <rg-name> \
  --min-replicas 0 \
  --max-replicas 0

# Note: Most services bill even when idle (APIM, Redis, Search)
# Recommendation: Delete resource group if not actively using
```

## Contributing

We welcome contributions to improve the Master AI Gateway Lab!

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** (code, documentation, examples)
4. **Test thoroughly**:
   - Run all notebook cells
   - Verify deployment works
   - Check documentation is accurate
5. **Commit with clear messages**:
   ```bash
   git commit -m "Add: New MCP server integration example"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request** with:
   - Description of changes
   - Testing performed
   - Screenshots (if applicable)
   - Related issue number (if any)

### Areas for Contribution

- **New MCP server implementations** (data sources, APIs)
- **Additional policy examples** (rate limiting, throttling)
- **Cost optimization guides** (reducing expenses)
- **Alternative deployment options** (Terraform, Pulumi)
- **Localization** (translate documentation)
- **Bug fixes** (errors, typos, outdated info)
- **Performance improvements** (faster deployments, better caching)

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Test your changes before submitting
- Follow existing code style and conventions
- Update documentation for any changes

## License

This project is licensed under the [MIT License](../../LICENSE.md) - see the LICENSE file for details.

## Resources

### Azure Documentation

- [Azure API Management](https://learn.microsoft.com/azure/api-management/) - Gateway service documentation
- [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/) - AI model hosting
- [Azure AI Foundry](https://learn.microsoft.com/azure/ai-studio/) - AI project management
- [Azure AI Search](https://learn.microsoft.com/azure/search/) - Vector search service
- [Azure Cache for Redis](https://learn.microsoft.com/azure/azure-cache-for-redis/) - Caching service
- [Azure Cosmos DB](https://learn.microsoft.com/azure/cosmos-db/) - NoSQL database
- [Azure Container Apps](https://learn.microsoft.com/azure/container-apps/) - Container hosting
- [Azure Monitor](https://learn.microsoft.com/azure/azure-monitor/) - Logging and analytics

### AI Gateway Concepts

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) - Data source integration
- [Retrieval Augmented Generation (RAG)](https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview) - Grounded AI responses
- [Semantic Caching](https://redis.io/blog/what-is-semantic-caching/) - Intelligent response caching
- [OAuth 2.0](https://oauth.net/2/) - Authentication framework
- [JWT Tokens](https://jwt.io/) - Secure token format

### Related Labs

- [Individual Lab Documentation](../) - Original 7 labs (if you want to deploy individually)
- [AI Gateway Workshops](../../workshop/) - Hands-on workshop materials

### Tools & Utilities

- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/) - Infrastructure deployment
- [Bicep](https://learn.microsoft.com/azure/azure-resource-manager/bicep/) - Infrastructure as Code
- [VS Code Jupyter](https://code.visualstudio.com/docs/datascience/jupyter-notebooks) - Notebook editing
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector) - MCP debugging tool

### Community

- [Azure OpenAI Community](https://techcommunity.microsoft.com/azure/cognitive-services) - Forums and discussions
- [GitHub Issues](https://github.com/yourusername/AI-Gateway/issues) - Report bugs or request features
- [GitHub Discussions](https://github.com/yourusername/AI-Gateway/discussions) - Ask questions

---

## Quick Reference Card

**Notebook:** `master-ai-gateway-fix-MCP-clean-documented-final.ipynb` (152 cells)

**Deployment Time:** 35-40 minutes
**Monthly Cost:** $890-1,190 USD (varies by usage)
**Labs Included:** 7 comprehensive labs
**Total Resources:** ~15 Azure resources

**Essential Commands:**
```bash
# Login
az login

# Deploy infrastructure
az deployment group create \
  --resource-group <rg-name> \
  --template-file infra/main.bicep \
  --parameters infra/main.parameters.json

# View resources
az resource list --resource-group <rg-name> --output table

# Cleanup
az group delete --name <rg-name> --yes --no-wait
```

**Getting Started Checklist:**
- [ ] Azure subscription with appropriate permissions
- [ ] Python 3.11+ installed
- [ ] Azure CLI installed and logged in
- [ ] VS Code with Jupyter extension
- [ ] Repository cloned
- [ ] Dependencies installed
- [ ] Notebook opened
- [ ] Section 0 cells run successfully

---

**Built with ❤️ to demonstrate enterprise-grade AI Gateway patterns on Azure**

**Last Updated:** 2025-11-24
**Version:** 1.0.0
**Status:** Production Ready
