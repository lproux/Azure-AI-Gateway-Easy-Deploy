# Azure AI Gateway - Easy Deploy Notebook

## Overview

The `master-ai-gateway-easy-deploy.ipynb` notebook is a **streamlined version** of the comprehensive `master-ai-gateway-deploy-from-notebook.ipynb` that leverages modular utilities for maximum efficiency.

## Key Improvements

### Dramatic Size Reduction

| Metric | Original Notebook | Easy Deploy Notebook | Improvement |
|--------|-------------------|----------------------|-------------|
| **Total Cells** | 152 cells | 34 cells | **78% reduction** |
| **Code Cells** | ~110 cells | 15 cells | **86% reduction** |
| **File Size** | 791 KB | 33 KB | **96% reduction** |
| **Lines of Code** | ~3,500+ lines | ~400 lines | **89% reduction** |

### What Makes It Different

1. **Modular Deployment**
   - Uses `util.deploy_all.py` for one-command deployment
   - No repeated ARM template code
   - Automatic credential handling

2. **Shared Initialization**
   - Uses `quick_start.shared_init.py` for setup
   - One-line client creation
   - Automatic environment loading

3. **Focused Labs**
   - Each lab is 1-2 cells (vs 5-10 cells in original)
   - Minimal boilerplate code
   - Clear, concise examples

4. **Azure CLI Authentication**
   - Simplest authentication method
   - No manual credential management
   - Works out of the box with `az login`

## Notebook Structure

### Section 0: One-Command Deployment (6 cells)
- Install dependencies
- Configure deployment
- Deploy complete infrastructure
- Save configuration

**Time**: ~60 minutes (automated)

### Section 1: Core AI Gateway Labs (8 cells)
1. **Lab 1.1: Access Control** - OAuth 2.0 and API key testing
2. **Lab 1.2: Load Balancing** - Multi-region distribution
3. **Lab 1.3: Token Metrics** - Usage monitoring
4. **Lab 1.4: Content Safety** - Content moderation

**Time**: ~10 minutes

### Section 2: Advanced Features (8 cells)
1. **Lab 2.1: Semantic Caching** - Redis-based response caching
2. **Lab 2.2: Message Storing** - Cosmos DB conversation history
3. **Lab 2.3: Vector Search (RAG)** - Azure AI Search integration
4. **Lab 2.4: Built-in Logging** - Comprehensive monitoring

**Time**: ~15 minutes

### Section 3: MCP Integration (6 cells)
1. **Lab 3.1: MCP Tool Calling** - Single tool usage
2. **Lab 3.2: Multi-Tool Orchestration** - Multiple tools in one call
3. **Lab 3.3: MCP Server Status** - Health checking

**Time**: ~10 minutes

## Quick Start

### Prerequisites

1. **Azure CLI** - Install and authenticate
   ```bash
   az login
   az account set --subscription <your-subscription-id>
   ```

2. **Python 3.11+** with required packages
   ```bash
   pip install -r requirements.txt
   ```

3. **Azure Subscription** with Contributor role

### Running the Notebook

1. Open `master-ai-gateway-easy-deploy.ipynb` in Jupyter or VS Code
2. Run Cell 1-2: Install dependencies
3. Run Cell 3-4: Deploy infrastructure (enter subscription ID when prompted)
4. Run Cell 5: Save configuration
5. Run remaining cells: Execute labs in any order

## What Gets Deployed

### Core Infrastructure
- **API Management**: Standardv2 tier with OAuth 2.0
- **Application Insights**: Request telemetry and monitoring
- **Log Analytics**: Comprehensive logging workspace

### AI Services
- **AI Foundry Hub 1** (UK South): gpt-4o-mini, gpt-4o, text-embedding-3-small, text-embedding-3-large
- **AI Foundry Hub 2** (Sweden Central): gpt-4o-mini
- **AI Foundry Hub 3** (West Europe): gpt-4o-mini

### Supporting Services
- **Redis Cache**: Semantic caching (Balanced_B0)
- **Cosmos DB**: Message storage
- **Azure AI Search**: Vector search (Basic tier)
- **Content Safety**: Content moderation

### MCP Servers (Container Apps)
- Weather MCP server
- GitHub MCP server
- Product catalog MCP server
- Place order MCP server
- MS Learn MCP server

## Comparison: Original vs Easy Deploy

### Original Notebook (`master-ai-gateway-deploy-from-notebook.ipynb`)

**Pros:**
- Comprehensive step-by-step explanations
- Full ARM template visibility
- Detailed error handling in each cell
- Educational for learning deployment details

**Cons:**
- 152 cells with significant code duplication
- Manual credential management
- Repeated initialization code
- Longer to execute and maintain

### Easy Deploy Notebook (`master-ai-gateway-easy-deploy.ipynb`)

**Pros:**
- 78% fewer cells (34 vs 152)
- One-command deployment
- Modular, reusable code
- Automatic credential handling
- Production-ready patterns
- Easy to customize

**Cons:**
- Less visibility into deployment internals
- Requires understanding of utility modules
- May hide complexity for newcomers

## Best Practices

1. **First Time Users**: Review the original notebook to understand deployment details
2. **Regular Use**: Use Easy Deploy for quick deployments and lab exercises
3. **Production**: Adapt the modular utilities for CI/CD pipelines
4. **Development**: Use Azure CLI authentication for simplicity

## Modular Utilities

### `util.deploy_all.py`

Complete deployment in one function call:

```python
from util.deploy_all import deploy_complete_infrastructure, DeploymentConfig

config = DeploymentConfig(
    subscription_id='xxx',
    resource_group='lab-master-lab',
    location='uksouth'
)

outputs = deploy_complete_infrastructure(config)
outputs.to_env_file('master-lab.env')
```

**Features:**
- Automatic credential detection (Azure CLI, Service Principal, or Default)
- Idempotent deployments (skips completed steps)
- Progress tracking with callbacks
- Comprehensive error handling
- JSON and ENV file outputs

### `quick_start.shared_init.py`

One-line initialization for labs:

```python
from quick_start.shared_init import quick_init, get_azure_openai_client

# Initialize everything
config = quick_init()

# Get clients
openai_client = get_azure_openai_client()
cosmos_client = get_cosmos_client()
search_client = get_search_client()
```

**Features:**
- Automatic environment loading
- Azure CLI authentication
- Pre-configured clients
- Resource verification
- Helpful error messages

## Customization

### Custom Model Deployments

```python
config = DeploymentConfig(
    subscription_id='xxx',
    resource_group='lab-master-lab',
    primary_models=[
        {'name': 'gpt-4o', 'format': 'OpenAI', 'version': '2024-08-06', 'sku': 'GlobalStandard', 'capacity': 200},
        {'name': 'gpt-4o-mini', 'format': 'OpenAI', 'version': '2024-07-18', 'sku': 'GlobalStandard', 'capacity': 100},
    ]
)
```

### Skip Optional Features

```python
config = DeploymentConfig(
    subscription_id='xxx',
    resource_group='lab-master-lab',
    deploy_mcp_servers=False,  # Skip MCP deployment
    deploy_content_safety=False  # Skip Content Safety
)
```

### Custom SKUs

```python
config = DeploymentConfig(
    subscription_id='xxx',
    resource_group='lab-master-lab',
    apim_sku='Premium',  # Use Premium tier
    redis_sku='Balanced_B1',  # Larger Redis
    search_sku='standard'  # Standard Search
)
```

## Troubleshooting

### "Prerequisites verification failed"
- Ensure Azure CLI is installed: `az --version`
- Ensure Bicep is installed: `az bicep version`
- Authenticate: `az login`

### "Deployment failed at Step X"
- Check Azure Portal for detailed error messages
- Review `deployment.log` file
- Re-run deployment (it will skip completed steps)

### "Environment file not found"
- Ensure you ran the deployment cell successfully
- Check for `master-lab.env` in the notebook directory
- Verify deployment completed without errors

### "Authentication failed"
- Run `az login` to refresh credentials
- Verify subscription access: `az account show`
- Check Azure CLI token hasn't expired

## Next Steps

1. **Complete the Notebook**: Run all labs to understand capabilities
2. **Explore Utilities**: Review `util/deploy_all.py` and `quick_start/shared_init.py`
3. **Customize Deployment**: Modify `DeploymentConfig` for your needs
4. **Build Your Own**: Use modular utilities in custom notebooks
5. **Deploy to Production**: Adapt utilities for CI/CD pipelines

## Resources

- **Original Notebook**: `master-ai-gateway-deploy-from-notebook.ipynb`
- **Deployment Utility**: `util/deploy_all.py`
- **Shared Initialization**: `quick_start/shared_init.py`
- **Bicep Templates**: `deploy/*.bicep`
- **Requirements**: `requirements.txt`

## Support

For issues or questions:
1. Check the original comprehensive notebook for detailed explanations
2. Review Azure Portal deployment logs
3. Check `deployment.log` for detailed error messages
4. Verify all prerequisites are met

---

**Created**: November 2024
**Version**: 1.0
**Compatible with**: Azure AI Gateway Master Lab
