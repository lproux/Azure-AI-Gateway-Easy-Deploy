# Quick Start - Modular Azure AI Gateway Labs

> **Minimal initialization, maximum learning** - Run individual labs without repeating setup code.

## Overview

This folder contains modular, standalone lab notebooks that share a common initialization module. Each lab focuses on a single feature and can be run independently after the initial setup.

### Key Features

- **Minimal Initialization**: 5-cell setup vs 27 cells in master notebook
- **Azure CLI Authentication**: Easiest method - just `az login` (no service principal needed)
- **Shared Module**: Reusable `shared_init.py` for all labs
- **Independent Labs**: Run any lab in any order
- **Same Resources**: Uses the same Azure resources from master-lab

## Prerequisites

1. **Azure Resources Deployed**: Run the main deployment notebook first:
   ```bash
   # From master-lab directory
   jupyter notebook master-ai-gateway-fix-MCP-clean-documented-final.ipynb
   # Run Section 0 to deploy all resources
   ```

2. **Azure CLI Authenticated**:
   ```bash
   az login
   az account set --subscription <your-subscription-id>
   ```

3. **Python Dependencies Installed**:
   ```bash
   cd ../  # Back to master-lab
   pip install -r requirements.txt
   ```

## Quick Start

### Option 1: One-Liner Initialization (Recommended)

In any lab notebook:

```python
# Cell 1 - Import and initialize everything
import sys
sys.path.append('..')
from quick_start.shared_init import quick_init

config = quick_init()
```

That's it! You're ready to run the lab.

### Option 2: Step-by-Step Initialization

For more control:

```python
# Cell 1 - Import module
import sys
sys.path.append('..')
from quick_start.shared_init import *

# Cell 2 - Load environment
env = load_environment()

# Cell 3 - Check authentication
account = check_azure_cli_auth()

# Cell 4 - Create clients as needed
openai_client = get_azure_openai_client()
cosmos_client = get_cosmos_client()
search_client = get_search_client()
```

## Lab Notebooks

Each lab is a standalone notebook focusing on one feature:

### 01-access-control.ipynb
**Duration:** ~10 minutes | **Cells:** ~15

Test different authentication methods:
- No authentication (expect 401)
- API Key authentication
- OAuth 2.0 / JWT token authentication
- Dual authentication (JWT + API Key)

**What You'll Learn:**
- APIM access control policies
- JWT token validation
- API key management
- OAuth 2.0 with Azure AD

### 02-semantic-caching.ipynb
**Duration:** ~10 minutes | **Cells:** ~12

Implement semantic caching with Redis:
- Configure Redis cache connection
- Test cache hits for identical queries
- Verify cache invalidation
- Measure performance improvements

**What You'll Learn:**
- APIM caching policies
- Redis integration
- Cache key strategies
- Performance optimization

### 03-message-storing.ipynb
**Duration:** ~10 minutes | **Cells:** ~10

Store conversation history in Cosmos DB:
- Connect to Cosmos DB with Azure AD
- Store messages by conversation ID
- Query conversation history
- Handle RBAC permissions

**What You'll Learn:**
- Cosmos DB integration
- NoSQL data modeling
- Azure AD authentication
- Conversation tracking

### 04-vector-search.ipynb
**Duration:** ~15 minutes | **Cells:** ~18

Implement RAG with Azure AI Search:
- Generate embeddings for documents
- Create and populate search index
- Perform vector similarity search
- Build RAG query pipeline

**What You'll Learn:**
- Text embeddings with text-embedding-3-small
- Azure AI Search vector indexing
- Semantic search
- RAG architecture patterns

### 05-load-balancing.ipynb
**Duration:** ~10 minutes | **Cells:** ~12

Test backend pool load balancing:
- Configure priority-based routing
- Test failover scenarios
- Monitor backend health
- Analyze request distribution

**What You'll Learn:**
- APIM backend pools
- Load balancing strategies
- Failover handling
- Health monitoring

### 06-mcp-integration.ipynb
**Duration:** ~20 minutes | **Cells:** ~25

Work with Model Context Protocol servers:
- List available MCP tools
- Call MCP servers through APIM
- Handle tool responses
- Build agent workflows

**What You'll Learn:**
- MCP protocol fundamentals
- Tool discovery and invocation
- APIM routing to MCP servers
- Agent orchestration patterns

### 07-logging.ipynb
**Duration:** ~10 minutes | **Cells:** ~15

Analyze built-in logging with Log Analytics:
- Query APIM request logs
- Analyze token usage metrics
- Track errors and latencies
- Build monitoring dashboards

**What You'll Learn:**
- APIM built-in logging
- KQL query language
- Token usage tracking
- Performance monitoring

## Authentication: Why Azure CLI?

This quick-start uses **Azure CLI authentication** because it's:

1. **Easiest**: Just `az login` - no secrets to manage
2. **Secure**: Tokens are managed by Azure CLI
3. **Local-first**: Perfect for development and learning
4. **No Configuration**: Works immediately after `az login`

**Comparison with other methods:**

| Method | Setup Time | Best For | Secrets Management |
|--------|-----------|----------|-------------------|
| **Azure CLI** | 30 seconds | Development, Learning | Automatic |
| Service Principal | 5 minutes | CI/CD, Production | Manual (.env files) |
| Managed Identity | N/A | Azure VMs, AKS, Functions | Automatic |

## Folder Structure

```
quick-start/
├── README.md                    # This file
├── shared_init.py               # Shared initialization module
├── 01-access-control.ipynb      # Lab 1: Access Control
├── 02-semantic-caching.ipynb    # Lab 2: Semantic Caching
├── 03-message-storing.ipynb     # Lab 3: Message Storing
├── 04-vector-search.ipynb       # Lab 4: Vector Search
├── 05-load-balancing.ipynb      # Lab 5: Load Balancing
├── 06-mcp-integration.ipynb     # Lab 6: MCP Integration
└── 07-logging.ipynb             # Lab 7: Built-in Logging
```

## Shared Initialization Module

The `shared_init.py` module provides:

### Functions

- `quick_init()` - One-line initialization for all labs
- `load_environment()` - Load master-lab.env variables
- `check_azure_cli_auth()` - Verify Azure CLI authentication
- `get_azure_openai_client()` - Create OpenAI client with Azure CLI auth
- `get_cosmos_client()` - Create Cosmos DB client with Azure CLI auth
- `get_search_client()` - Create Search client with Azure CLI auth
- `verify_resources()` - Check deployed Azure resources

### Pre-imported Modules

The module automatically imports commonly used packages:

```python
import json, time, os, sys
from datetime import datetime
from azure.identity import AzureCliCredential
from openai import AzureOpenAI
from azure.cosmos import CosmosClient
from azure.search.documents import SearchClient
import requests
```

## Troubleshooting

### "Azure CLI authentication required"

**Solution:**
```bash
az login
az account show  # Verify you're logged in
```

### "master-lab.env not found"

**Solution:**
```bash
cd ..  # Go back to master-lab directory
# Run the main deployment notebook Section 0 first
```

### "Resource group not found"

**Solution:**
You need to deploy the Azure resources first using the main notebook.

### Import errors

**Solution:**
```bash
cd ..  # Back to master-lab
pip install -r requirements.txt
```

## Comparison: Quick Start vs Master Notebook

| Feature | Quick Start | Master Notebook |
|---------|-------------|-----------------|
| **Initialization Cells** | 1-5 cells | 27 cells |
| **Authentication** | Azure CLI only | 3 methods (CLI, Service Principal, Managed Identity) |
| **Target Audience** | Learners, developers | Production, workshops |
| **Lab Structure** | Separate notebooks | Single comprehensive notebook |
| **Deployment** | Requires master deployment first | Includes full deployment |
| **Modularity** | High (run any lab independently) | Low (sequential execution) |
| **Documentation** | Focused on doing | Comprehensive explanations |

## When to Use What

### Use Quick Start When:
- Learning individual features
- Quick experimentation
- Building proof-of-concepts
- Testing specific scenarios
- You already deployed resources

### Use Master Notebook When:
- First-time deployment
- Comprehensive walkthroughs
- Production setup with service principals
- Workshop or training sessions
- Need detailed explanations

## Contributing

Found an issue or want to improve a lab? Contributions welcome!

1. Test your changes with `az login` authentication
2. Keep initialization minimal (use shared_init.py)
3. Focus on the lab's core learning objective
4. Add clear comments and markdown explanations

## Resources

- **Main Deployment Notebook**: `../master-ai-gateway-fix-MCP-clean-documented-final.ipynb`
- **Documentation**: `../NOTEBOOK_DOCUMENTATION_README.md`
- **Master Lab README**: `../README.md`
- **Azure CLI Docs**: https://learn.microsoft.com/cli/azure/
- **Azure OpenAI Docs**: https://learn.microsoft.com/azure/ai-services/openai/

---

**Ready to start?** Pick a lab and run it! 🚀
