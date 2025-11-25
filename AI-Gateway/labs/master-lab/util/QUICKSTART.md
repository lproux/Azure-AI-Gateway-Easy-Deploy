# Quick Start Guide

Deploy all Azure AI Gateway resources in 3 steps.

## Prerequisites

```bash
# 1. Install Azure CLI
# https://aka.ms/azure-cli

# 2. Install Bicep
az bicep install

# 3. Install Python packages
pip install azure-identity azure-mgmt-resource azure-mgmt-cognitiveservices python-dotenv

# 4. Login to Azure
az login
az account set --subscription "your-subscription-id"
```

## Deploy in 3 Steps

### Step 1: Import

```python
from util import deploy_complete_infrastructure, DeploymentConfig
```

### Step 2: Configure

```python
config = DeploymentConfig(
    subscription_id='your-subscription-id',
    resource_group='lab-master-lab'
)
```

### Step 3: Deploy

```python
outputs = deploy_complete_infrastructure(config)
outputs.to_env_file('master-lab.env')
```

**That's it!** Your infrastructure will be deployed in ~60 minutes.

## What Gets Deployed

| Resource | Purpose | Time |
|----------|---------|------|
| **APIM** | API Gateway | ~15 min |
| **AI Foundry Hubs** | 3 regions with models | ~30 min |
| **Redis Cache** | Semantic caching | ~10 min |
| **Cosmos DB** | Message storage | ~10 min |
| **AI Search** | Vector search | ~10 min |
| **MCP Servers** | 5 container apps | ~5 min |

## Example: Jupyter Notebook

```python
# Cell 1: Setup
import os
from util import deploy_complete_infrastructure, DeploymentConfig

config = DeploymentConfig(
    subscription_id=os.getenv('AZURE_SUBSCRIPTION_ID'),
    resource_group='lab-master-lab'
)

# Cell 2: Deploy with progress
def show_progress(progress):
    print(f"[{progress.status}] {progress.step}: {progress.message}")

outputs = deploy_complete_infrastructure(config, progress_callback=show_progress)

# Cell 3: Save outputs
outputs.to_env_file('master-lab.env')
print(f"✅ Deployed in {outputs.deployment_duration_seconds/60:.1f} minutes")
```

## Example: Command Line

```bash
python -m util.deploy_all \
    --subscription-id "your-subscription-id" \
    --resource-group "lab-master-lab" \
    --output "master-lab.env"
```

## Example: Custom Models

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
            'capacity': 150  # Higher capacity
        }
    ]
)

outputs = deploy_complete_infrastructure(config)
```

## Example: Skip Optional Components

```python
config = DeploymentConfig(
    subscription_id='xxx',
    resource_group='lab-master-lab',
    deploy_mcp_servers=False,      # Skip MCP servers
    deploy_content_safety=False    # Skip Content Safety
)

outputs = deploy_complete_infrastructure(config)
```

## Authentication

Three methods (auto-detected in order):

### 1. Explicit Credentials

```python
config = DeploymentConfig(
    subscription_id='xxx',
    resource_group='lab-master-lab',
    tenant_id='xxx',
    client_id='xxx',
    client_secret='xxx'
)
```

### 2. Environment File

Create `.azure-credentials.env`:

```bash
AZURE_TENANT_ID=xxx
AZURE_CLIENT_ID=xxx
AZURE_CLIENT_SECRET=xxx
AZURE_SUBSCRIPTION_ID=xxx
```

### 3. Azure CLI

```bash
az login
az account set --subscription "xxx"
```

## Output Files

- `master-lab.env` - All credentials and endpoints
- `deployment-outputs.json` - Complete outputs
- `deployment.log` - Detailed log
- `step1-outputs.json` - Core infrastructure
- `step2-outputs.json` - AI Foundry
- `step3-outputs.json` - Supporting services
- `step4-outputs.json` - MCP servers

## Resume Failed Deployments

Already-deployed resources are automatically skipped:

```python
# First attempt (fails at Step 3)
try:
    outputs = deploy_complete_infrastructure(config)
except:
    pass

# Second attempt (skips Steps 1-2, retries Step 3)
outputs = deploy_complete_infrastructure(config)
```

## Common Issues

**"Azure CLI not installed"**
```bash
# Install: https://aka.ms/azure-cli
```

**"Bicep not installed"**
```bash
az bicep install
```

**"Authentication failed"**
```bash
az login
az account set --subscription "your-id"
```

**"Quota exceeded"**
```python
# Reduce model capacity
config = DeploymentConfig(
    subscription_id='xxx',
    resource_group='lab-master-lab',
    primary_models=[
        {'name': 'gpt-4o-mini', 'format': 'OpenAI',
         'version': '2024-07-18', 'sku': 'GlobalStandard',
         'capacity': 50}  # Reduced
    ]
)
```

## Next Steps

1. Load environment: `source master-lab.env`
2. Configure APIM APIs
3. Test individual labs
4. Monitor in Azure Portal

## Clean Up

```bash
az group delete --name lab-master-lab --yes --no-wait
```

## More Examples

- `examples/basic_deployment.py` - Simple deployment
- `examples/custom_models.py` - Custom model config
- `examples/cicd_deployment.py` - CI/CD integration
- `examples/notebook_example.ipynb` - Jupyter notebook

## Documentation

See `README.md` for comprehensive documentation.
