# Azure AI Gateway Complete Deployment Guide

## Overview

This module provides a **one-command deployment** solution for all Azure AI Gateway lab resources. Instead of running multiple deployment scripts and manually managing dependencies, you can deploy everything with a single Python function call.

## Architecture

```
Azure AI Gateway Complete Infrastructure
├── Step 1: Core Infrastructure (~15 min)
│   ├── API Management (StandardV2)
│   ├── Application Insights
│   └── Log Analytics Workspace
│
├── Step 2: AI Foundry Hubs + Models (~30 min)
│   ├── Hub 1 (uksouth) - Primary
│   │   ├── gpt-4o-mini
│   │   ├── gpt-4o
│   │   ├── text-embedding-3-small
│   │   └── text-embedding-3-large
│   ├── Hub 2 (swedencentral) - Secondary
│   │   └── gpt-4o-mini
│   └── Hub 3 (westeurope) - Secondary
│       └── gpt-4o-mini
│
├── Step 3: Supporting Services (~10 min)
│   ├── Redis Enterprise (semantic caching)
│   ├── Azure Cognitive Search (vector search)
│   ├── Cosmos DB (message storage)
│   └── Content Safety (optional)
│
└── Step 4: MCP Servers (~5 min)
    ├── Container Registry
    ├── Container Apps Environment
    └── 5 MCP Server Containers
        ├── weather
        ├── github
        ├── product-catalog
        ├── place-order
        └── ms-learn
```

**Total Deployment Time**: ~60 minutes

## Key Features

### 1. Single Command Deployment
Deploy all resources with one function call - no need to manage multiple scripts or track dependencies.

### 2. Intelligent Skip Logic
Already-deployed resources are automatically detected and skipped, allowing you to:
- Resume failed deployments
- Re-run scripts without errors
- Update specific components

### 3. Resilient Model Deployment
AI model deployments include:
- Automatic retry logic
- Quota-aware error handling
- Graceful degradation (continues on failures)
- Detailed failure reporting

### 4. Progress Tracking
Real-time progress updates with:
- Step-by-step status
- Elapsed time tracking
- Error reporting
- Estimated completion time

### 5. Comprehensive Error Handling
- Try/except around each deployment step
- Detailed error logging to `deployment.log`
- Partial output preservation for resume
- Clear error messages with remediation hints

### 6. Automatic Credential Management
Three-tier credential resolution:
1. Explicit credentials in `DeploymentConfig`
2. `.azure-credentials.env` file
3. Azure CLI (fallback)

### 7. Environment Generation
Automatically generates:
- `master-lab.env` - Environment variables for labs
- `deployment-outputs.json` - Complete deployment outputs
- `step{1-4}-outputs.json` - Individual step outputs
- `deployment.log` - Detailed execution log

## Installation

### Prerequisites

```bash
# 1. Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# 2. Install Bicep
az bicep install

# 3. Install Python packages
pip install azure-identity azure-mgmt-resource azure-mgmt-cognitiveservices python-dotenv
```

### Verify Installation

```bash
# Check Azure CLI
az --version

# Check Bicep
az bicep version

# Check Python packages
python -c "from util import deploy_complete_infrastructure; print('✅ Ready')"
```

## Quick Start

### Minimal Example

```python
from util import deploy_complete_infrastructure, DeploymentConfig

config = DeploymentConfig(
    subscription_id='your-subscription-id',
    resource_group='lab-master-lab'
)

outputs = deploy_complete_infrastructure(config)
outputs.to_env_file('master-lab.env')
```

### With Progress Tracking

```python
from util import deploy_complete_infrastructure, DeploymentConfig

def show_progress(progress):
    print(f"[{progress.status}] {progress.step}: {progress.message}")

config = DeploymentConfig(
    subscription_id='your-subscription-id',
    resource_group='lab-master-lab'
)

outputs = deploy_complete_infrastructure(config, progress_callback=show_progress)
outputs.to_env_file('master-lab.env')
```

## Configuration Reference

### DeploymentConfig Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `subscription_id` | str | ✅ | - | Azure subscription ID |
| `resource_group` | str | ✅ | - | Resource group name |
| `location` | str | ❌ | 'uksouth' | Primary Azure region |
| `resource_suffix` | str | ❌ | auto | Unique resource suffix |
| `tenant_id` | str | ❌ | None | Service principal tenant |
| `client_id` | str | ❌ | None | Service principal client ID |
| `client_secret` | str | ❌ | None | Service principal secret |
| `primary_models` | list | ❌ | DEFAULT_PRIMARY_MODELS | Models for primary region |
| `secondary_models` | list | ❌ | DEFAULT_SECONDARY_MODELS | Models for secondary regions |
| `deploy_private_endpoints` | bool | ❌ | False | Deploy private endpoints |
| `deploy_content_safety` | bool | ❌ | True | Deploy Content Safety |
| `deploy_mcp_servers` | bool | ❌ | True | Deploy MCP servers |
| `apim_sku` | str | ❌ | 'Standardv2' | APIM SKU |
| `redis_sku` | str | ❌ | 'Balanced_B0' | Redis SKU |
| `search_sku` | str | ❌ | 'basic' | Search SKU |

### Model Configuration

Each model in `primary_models` and `secondary_models` must have:

```python
{
    'name': str,           # Model name (e.g., 'gpt-4o-mini')
    'format': str,         # Format (usually 'OpenAI')
    'version': str,        # Version (e.g., '2024-07-18')
    'sku': str,           # SKU (e.g., 'GlobalStandard')
    'capacity': int       # Capacity (e.g., 100)
}
```

**Default Primary Models**:
```python
DEFAULT_PRIMARY_MODELS = [
    {'name': 'gpt-4o-mini', 'format': 'OpenAI', 'version': '2024-07-18', 'sku': 'GlobalStandard', 'capacity': 100},
    {'name': 'gpt-4o', 'format': 'OpenAI', 'version': '2024-08-06', 'sku': 'GlobalStandard', 'capacity': 100},
    {'name': 'text-embedding-3-small', 'format': 'OpenAI', 'version': '1', 'sku': 'GlobalStandard', 'capacity': 20},
    {'name': 'text-embedding-3-large', 'format': 'OpenAI', 'version': '1', 'sku': 'GlobalStandard', 'capacity': 20},
]
```

**Default Secondary Models**:
```python
DEFAULT_SECONDARY_MODELS = [
    {'name': 'gpt-4o-mini', 'format': 'OpenAI', 'version': '2024-07-18', 'sku': 'GlobalStandard', 'capacity': 100},
]
```

## Advanced Usage

### Custom Model Configuration

Deploy with custom models and capacities:

```python
config = DeploymentConfig(
    subscription_id='xxx',
    resource_group='lab-master-lab',
    primary_models=[
        {
            'name': 'gpt-4o-mini',
            'format': 'OpenAI',
            'version': '2024-07-18',
            'sku': 'GlobalStandard',
            'capacity': 200  # Higher capacity
        },
        {
            'name': 'gpt-4o',
            'format': 'OpenAI',
            'version': '2024-08-06',
            'sku': 'GlobalStandard',
            'capacity': 150
        }
    ],
    secondary_models=[
        {
            'name': 'gpt-4o-mini',
            'format': 'OpenAI',
            'version': '2024-07-18',
            'sku': 'GlobalStandard',
            'capacity': 50  # Lower capacity for failover
        }
    ]
)
```

### Skip Optional Components

Save costs by skipping optional components:

```python
config = DeploymentConfig(
    subscription_id='xxx',
    resource_group='lab-master-lab',
    deploy_content_safety=False,  # Skip Content Safety
    deploy_mcp_servers=False      # Skip MCP servers
)
```

### Custom Resource Suffix

Use a specific resource suffix (e.g., for testing):

```python
config = DeploymentConfig(
    subscription_id='xxx',
    resource_group='lab-master-lab',
    resource_suffix='test123abc456'  # Custom suffix
)
```

### Service Principal Authentication

Use explicit service principal credentials:

```python
config = DeploymentConfig(
    subscription_id='xxx',
    resource_group='lab-master-lab',
    tenant_id='your-tenant-id',
    client_id='your-client-id',
    client_secret='your-client-secret'
)
```

### Advanced Progress Tracking

Create a custom progress tracker:

```python
import time
from util import deploy_complete_infrastructure, DeploymentConfig

class DeploymentMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.steps = []

    def on_progress(self, progress):
        self.steps.append(progress)
        elapsed = time.time() - self.start_time

        print(f"[{elapsed:.1f}s] {progress.step}")
        print(f"  Status: {progress.status}")
        print(f"  Message: {progress.message}")

        if progress.status == 'completed':
            print(f"  ✅ Completed in {progress.elapsed_seconds:.1f}s")
        elif progress.status == 'failed':
            print(f"  ❌ Failed: {progress.error}")

monitor = DeploymentMonitor()
config = DeploymentConfig(subscription_id='xxx', resource_group='lab-master-lab')
outputs = deploy_complete_infrastructure(config, progress_callback=monitor.on_progress)

print(f"\nTotal steps: {len(monitor.steps)}")
print(f"Total time: {(time.time() - monitor.start_time)/60:.1f} minutes")
```

## Output Files

### master-lab.env

Environment file with all credentials and endpoints:

```bash
# Azure AI Gateway Lab Environment
SUBSCRIPTION_ID=xxx
RESOURCE_GROUP=lab-master-lab
LOCATION=uksouth

# API Management
APIM_SERVICE_NAME=apim-xxx
APIM_GATEWAY_URL=https://apim-xxx.azure-api.net
APIM_SUBSCRIPTION_KEY=xxx

# AI Foundry Hubs
FOUNDRY1_ENDPOINT=https://foundry1-xxx.openai.azure.com
FOUNDRY1_KEY=xxx
FOUNDRY2_ENDPOINT=https://foundry2-xxx.openai.azure.com
FOUNDRY2_KEY=xxx
FOUNDRY3_ENDPOINT=https://foundry3-xxx.openai.azure.com
FOUNDRY3_KEY=xxx

# Redis Cache
REDIS_HOST=redis-xxx.redis.cache.windows.net
REDIS_KEY=xxx
REDIS_PORT=10000

# Cosmos DB
COSMOS_ENDPOINT=https://cosmos-xxx.documents.azure.com
COSMOS_ACCOUNT_NAME=cosmos-xxx
COSMOS_KEY=xxx

# Azure AI Search
SEARCH_ENDPOINT=https://search-xxx.search.windows.net
SEARCH_SERVICE_NAME=search-xxx
SEARCH_API_KEY=xxx

# Content Safety
CONTENT_SAFETY_ENDPOINT=https://contentsafety-xxx.cognitiveservices.azure.com
CONTENT_SAFETY_KEY=xxx

# Monitoring
LOG_ANALYTICS_WORKSPACE_ID=/subscriptions/xxx/...
LOG_ANALYTICS_CUSTOMER_ID=xxx
APP_INSIGHTS_INSTRUMENTATION_KEY=xxx

# Container Registry
CONTAINER_REGISTRY_NAME=acrxxx
CONTAINER_REGISTRY_LOGIN_SERVER=acrxxx.azurecr.io

# MCP Server URLs
MCP_WEATHER_URL=https://mcp-weather-xxx.region.azurecontainerapps.io
MCP_GITHUB_URL=https://mcp-github-xxx.region.azurecontainerapps.io
MCP_PRODUCT_CATALOG_URL=https://mcp-product-catalog-xxx.region.azurecontainerapps.io
MCP_PLACE_ORDER_URL=https://mcp-place-order-xxx.region.azurecontainerapps.io
MCP_MS_LEARN_URL=https://mcp-ms-learn-xxx.region.azurecontainerapps.io
```

### deployment-outputs.json

Complete deployment outputs in JSON format:

```json
{
  "apim_gateway_url": "https://apim-xxx.azure-api.net",
  "apim_subscription_key": "xxx",
  "foundry1_endpoint": "https://foundry1-xxx.openai.azure.com",
  "deployment_timestamp": "2025-01-24T10:30:00",
  "deployment_duration_seconds": 3600.5,
  "resource_suffix": "xxx",
  ...
}
```

### deployment.log

Detailed execution log with timestamps:

```
2025-01-24 10:30:00 - INFO - Starting deployment...
2025-01-24 10:30:05 - INFO - Verifying prerequisites...
2025-01-24 10:30:10 - INFO - Azure CLI installed
2025-01-24 10:30:15 - INFO - Deploying Step 1: Core Infrastructure...
...
```

## Error Handling & Troubleshooting

### Resume Failed Deployments

The module automatically skips already-deployed resources:

```python
# First attempt - fails at Step 3
try:
    outputs = deploy_complete_infrastructure(config)
except RuntimeError as e:
    print(f"Deployment failed: {e}")
    # Check deployment.log for details

# Second attempt - skips Steps 1-2, retries Step 3
outputs = deploy_complete_infrastructure(config)
```

### Common Errors

#### 1. "Azure CLI not installed"

**Solution**:
```bash
# Linux/WSL
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# macOS
brew install azure-cli

# Windows
https://aka.ms/installazurecliwindows
```

#### 2. "Bicep not installed"

**Solution**:
```bash
az bicep install
```

#### 3. "Authentication failed"

**Solution**:
```bash
az login
az account set --subscription "your-subscription-id"
```

#### 4. "Resource group not found"

The module will auto-create the resource group, but you can create it manually:

```bash
az group create --name lab-master-lab --location uksouth
```

#### 5. "Quota exceeded for model deployment"

**Solutions**:

a) Reduce model capacity:
```python
config = DeploymentConfig(
    subscription_id='xxx',
    resource_group='lab-master-lab',
    primary_models=[
        {
            'name': 'gpt-4o-mini',
            'format': 'OpenAI',
            'version': '2024-07-18',
            'sku': 'GlobalStandard',
            'capacity': 50  # Reduced from 100
        }
    ]
)
```

b) Request quota increase:
```bash
# Go to Azure Portal → Quotas → Request increase
```

#### 6. "Deployment timeout"

Some deployments (especially AI Foundry) can take longer. The module has built-in timeouts (10 minutes per model). If you see timeouts:

1. Check Azure Portal for deployment status
2. Re-run the script (will skip completed resources)
3. Check `deployment.log` for details

### Debug Mode

Enable detailed logging:

```python
import logging

# Set debug level
logging.basicConfig(level=logging.DEBUG)

from util import deploy_complete_infrastructure, DeploymentConfig

config = DeploymentConfig(...)
outputs = deploy_complete_infrastructure(config)
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Deploy AI Gateway

on:
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install azure-identity azure-mgmt-resource azure-mgmt-cognitiveservices python-dotenv

      - name: Install Azure CLI
        run: |
          curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
          az bicep install

      - name: Deploy infrastructure
        env:
          AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
          AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
          AZURE_CLIENT_SECRET: ${{ secrets.AZURE_CLIENT_SECRET }}
          RESOURCE_GROUP: lab-master-lab
          LOCATION: uksouth
        run: |
          python util/examples/cicd_deployment.py

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: deployment-outputs
          path: artifacts/
```

### Azure DevOps

```yaml
trigger: none

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.10'

  - script: |
      pip install azure-identity azure-mgmt-resource azure-mgmt-cognitiveservices python-dotenv
      az bicep install
    displayName: 'Install dependencies'

  - script: |
      python util/examples/cicd_deployment.py
    displayName: 'Deploy infrastructure'
    env:
      AZURE_SUBSCRIPTION_ID: $(AzureSubscriptionId)
      AZURE_TENANT_ID: $(AzureTenantId)
      AZURE_CLIENT_ID: $(AzureClientId)
      AZURE_CLIENT_SECRET: $(AzureClientSecret)
      RESOURCE_GROUP: lab-master-lab
      LOCATION: uksouth

  - task: PublishBuildArtifacts@1
    inputs:
      pathToPublish: 'artifacts'
      artifactName: 'deployment-outputs'
```

## Performance & Costs

### Deployment Time

| Step | Resources | Time | Can Skip? |
|------|-----------|------|-----------|
| 1. Core | APIM, Monitoring | ~15 min | ❌ Required |
| 2. AI Foundry | 3 hubs + models | ~30 min | ❌ Required |
| 3. Supporting | Redis, Cosmos, Search | ~10 min | ✅ Partial |
| 4. MCP Servers | Container Apps | ~5 min | ✅ Yes |

**Total**: ~60 minutes

### Estimated Monthly Costs (UK South)

| Service | SKU | Est. Cost/Month |
|---------|-----|-----------------|
| API Management | StandardV2 | $600 |
| AI Foundry (x3) | S0 | $300 |
| Redis Enterprise | Balanced_B0 | $50 |
| Cosmos DB | Standard | $25 |
| Azure Search | Basic | $75 |
| Container Apps | Consumption | $20 |
| App Insights | Standard | $10 |
| **Total** | | **~$1,080/month** |

**Cost Optimization Tips**:
- Use Developer tier APIM for non-production: Saves ~$550/month
- Reduce model capacities: Each TPM reduction saves costs
- Skip Content Safety if not needed: Saves ~$25/month
- Skip MCP servers for simple testing: Saves ~$20/month

## Clean Up

### Delete All Resources

```bash
az group delete --name lab-master-lab --yes --no-wait
```

### Delete Specific Resources

```bash
# Delete only MCP servers
az containerapp delete --name mcp-weather-xxx --resource-group lab-master-lab
az containerapp delete --name mcp-github-xxx --resource-group lab-master-lab
# ... etc

# Delete only AI Foundry hubs
az cognitiveservices account delete --name foundry1-xxx --resource-group lab-master-lab
# ... etc
```

## Support & Contributing

### Getting Help

1. Check `deployment.log` for detailed error messages
2. Review this guide and README.md
3. Consult Azure documentation for service-specific issues

### Filing Issues

When reporting issues, include:
- Contents of `deployment.log`
- Your `DeploymentConfig` (without secrets!)
- Output of `az --version` and `python --version`
- Error message and stack trace

## License

MIT License - see LICENSE file for details.

## Version History

**1.0.0** (2025-01-24)
- Initial release
- Complete infrastructure deployment
- Resilient model deployment
- Progress tracking
- Environment file generation
- CI/CD examples
