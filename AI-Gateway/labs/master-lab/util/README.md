# Azure AI Gateway Deployment Utilities

One-command deployment for all Azure AI Gateway lab resources.

## Features

- **Complete Infrastructure Deployment**: Deploy all required Azure resources in a single command
- **Resilient Model Deployment**: Automatic retry logic for AI model deployments
- **Progress Tracking**: Real-time progress updates during deployment
- **Smart Skip Logic**: Automatically skips already-deployed resources
- **Environment Generation**: Auto-generates `.env` files with all credentials
- **Error Handling**: Comprehensive error handling with detailed logging

## Resources Deployed

### Step 1: Core Infrastructure (~15 minutes)
- **API Management** (StandardV2)
- **Application Insights**
- **Log Analytics Workspace**

### Step 2: AI Foundry Hubs + Models (~30 minutes)
- **3 AI Foundry Hubs** (uksouth, swedencentral, westeurope)
- **Model Deployments**:
  - Primary region: gpt-4o-mini, gpt-4o, text-embedding-3-small, text-embedding-3-large
  - Secondary regions: gpt-4o-mini

### Step 3: Supporting Services (~10 minutes)
- **Redis Enterprise** (for semantic caching)
- **Azure Cognitive Search**
- **Cosmos DB** (for message storage)
- **Content Safety** (optional)

### Step 4: MCP Servers (~5 minutes)
- **Container Registry**
- **Container Apps Environment**
- **5 MCP Server Deployments**:
  1. weather
  2. github
  3. product-catalog
  4. place-order
  5. ms-learn

**Total Estimated Time**: ~60 minutes

## Installation

```bash
# Install required Python packages
pip install azure-identity azure-mgmt-resource azure-mgmt-cognitiveservices python-dotenv
```

## Quick Start

### Option 1: Python Script

```python
from util import deploy_complete_infrastructure, DeploymentConfig

# Configure deployment
config = DeploymentConfig(
    subscription_id='your-subscription-id',
    resource_group='lab-master-lab',
    location='uksouth'
)

# Deploy with progress tracking
def show_progress(progress):
    print(f"[{progress.status.upper()}] {progress.step}: {progress.message}")

outputs = deploy_complete_infrastructure(config, progress_callback=show_progress)

# Save environment file
outputs.to_env_file('master-lab.env')
print("✅ Deployment complete!")
```

### Option 2: Command Line

```bash
python -m util.deploy_all \
    --subscription-id "your-subscription-id" \
    --resource-group "lab-master-lab" \
    --location "uksouth" \
    --output "master-lab.env"
```

### Option 3: Jupyter Notebook

```python
# Cell 1: Import and configure
import os
from util import deploy_complete_infrastructure, DeploymentConfig

config = DeploymentConfig(
    subscription_id=os.getenv('SUBSCRIPTION_ID'),
    resource_group='lab-master-lab',
    location='uksouth'
)

# Cell 2: Deploy with progress
def show_progress(progress):
    status_icons = {
        'pending': '⏳',
        'in_progress': '🔄',
        'completed': '✅',
        'failed': '❌'
    }
    icon = status_icons.get(progress.status, '•')
    print(f"{icon} [{progress.status.upper()}] {progress.step}: {progress.message}")

outputs = deploy_complete_infrastructure(config, progress_callback=show_progress)

# Cell 3: Save and display results
outputs.to_env_file('master-lab.env')
outputs.to_json('deployment-outputs.json')

print("\n" + "="*70)
print("DEPLOYMENT COMPLETE")
print("="*70)
print(f"Duration: {outputs.deployment_duration_seconds/60:.1f} minutes")
print(f"APIM Gateway: {outputs.apim_gateway_url}")
print(f"Environment file: master-lab.env")
print("="*70)
```

## Configuration Options

### DeploymentConfig

```python
@dataclass
class DeploymentConfig:
    # Required
    subscription_id: str
    resource_group: str

    # Optional - Basic
    location: str = 'uksouth'
    resource_suffix: Optional[str] = None  # Auto-generated if None

    # Optional - Credentials (auto-detected if not provided)
    tenant_id: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None

    # Optional - Model Configuration
    primary_models: List[dict] = None  # Defaults to DEFAULT_PRIMARY_MODELS
    secondary_models: List[dict] = None  # Defaults to DEFAULT_SECONDARY_MODELS

    # Optional - Feature Flags
    deploy_private_endpoints: bool = False
    deploy_content_safety: bool = True
    deploy_mcp_servers: bool = True

    # Optional - SKU Configuration
    apim_sku: str = 'Standardv2'
    redis_sku: str = 'Balanced_B0'
    search_sku: str = 'basic'
```

### Custom Model Configuration

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
            'capacity': 100
        },
        {
            'name': 'gpt-4o',
            'format': 'OpenAI',
            'version': '2024-08-06',
            'sku': 'GlobalStandard',
            'capacity': 100
        }
    ],
    secondary_models=[
        {
            'name': 'gpt-4o-mini',
            'format': 'OpenAI',
            'version': '2024-07-18',
            'sku': 'GlobalStandard',
            'capacity': 100
        }
    ]
)
```

### Skip Optional Components

```python
config = DeploymentConfig(
    subscription_id='xxx',
    resource_group='lab-master-lab',
    deploy_mcp_servers=False,  # Skip MCP server deployment
    deploy_content_safety=False  # Skip Content Safety
)
```

## Authentication

The module supports three authentication methods (in priority order):

### 1. Explicit Credentials (Highest Priority)

```python
config = DeploymentConfig(
    subscription_id='xxx',
    resource_group='lab-master-lab',
    tenant_id='your-tenant-id',
    client_id='your-client-id',
    client_secret='your-client-secret'
)
```

### 2. Environment File (.azure-credentials.env)

Create a file named `.azure-credentials.env`:

```bash
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_SUBSCRIPTION_ID=your-subscription-id
```

### 3. Azure CLI (Fallback)

```bash
az login
az account set --subscription "your-subscription-id"
```

## Output Files

The deployment generates several output files:

- **`master-lab.env`**: Environment file with all credentials and endpoints
- **`deployment-outputs.json`**: Complete deployment outputs in JSON format
- **`step1-outputs.json`**: Core infrastructure outputs
- **`step2-outputs.json`**: AI Foundry outputs
- **`step3-outputs.json`**: Supporting services outputs
- **`step4-outputs.json`**: MCP server outputs
- **`deployment.log`**: Detailed deployment log

## ResourceOutputs

The `deploy_complete_infrastructure()` function returns a `ResourceOutputs` object:

```python
@dataclass
class ResourceOutputs:
    # Core
    apim_gateway_url: str
    apim_subscription_key: str
    apim_service_name: str

    # AI Foundry
    foundry1_endpoint: str
    foundry1_key: str
    foundry2_endpoint: str
    foundry2_key: str
    foundry3_endpoint: str
    foundry3_key: str

    # Supporting Services
    redis_host: str
    redis_key: str
    cosmos_endpoint: str
    cosmos_account_name: str
    cosmos_key: str
    search_endpoint: str
    search_service_name: str
    search_api_key: str

    # Infrastructure
    log_analytics_workspace_id: str
    app_insights_connection_string: str

    # Container Registry
    container_registry_name: str
    container_registry_login_server: str

    # MCP Servers
    mcp_server_urls: Dict[str, str]

    # Metadata
    deployment_timestamp: str
    deployment_duration_seconds: float
```

### Methods

```python
# Save to environment file
outputs.to_env_file('master-lab.env')

# Save to JSON
outputs.to_json('deployment-outputs.json')
```

## Progress Tracking

The `progress_callback` parameter allows you to track deployment progress:

```python
def show_progress(progress: DeploymentProgress):
    print(f"{progress.step}: {progress.message}")
    if progress.error:
        print(f"  Error: {progress.error}")

outputs = deploy_complete_infrastructure(config, progress_callback=show_progress)
```

### DeploymentProgress

```python
@dataclass
class DeploymentProgress:
    step: str  # e.g., "Core Infrastructure"
    status: str  # 'pending', 'in_progress', 'completed', 'failed'
    message: str  # Status message
    elapsed_seconds: float  # Time elapsed
    error: Optional[str]  # Error message if failed
```

## Error Handling

The module includes comprehensive error handling:

```python
try:
    outputs = deploy_complete_infrastructure(config)
except RuntimeError as e:
    print(f"Deployment failed: {e}")
    # Check deployment.log for details
```

All errors are logged to `deployment.log` with timestamps and stack traces.

## Resume Failed Deployments

The module automatically skips already-deployed resources, allowing you to resume failed deployments:

```python
# First attempt (fails at Step 3)
try:
    outputs = deploy_complete_infrastructure(config)
except RuntimeError:
    pass

# Second attempt (skips Steps 1-2, retries Step 3)
outputs = deploy_complete_infrastructure(config)
```

## Advanced Usage

### Custom Progress Display

```python
import time
from util import deploy_complete_infrastructure, DeploymentConfig

class DeploymentTracker:
    def __init__(self):
        self.start_time = time.time()
        self.steps = []

    def track(self, progress):
        elapsed = time.time() - self.start_time
        self.steps.append(progress)

        print(f"[{elapsed:.1f}s] {progress.step}: {progress.message}")

        if progress.status == 'completed':
            print(f"  ✅ Completed in {progress.elapsed_seconds:.1f}s")
        elif progress.status == 'failed':
            print(f"  ❌ Failed: {progress.error}")

tracker = DeploymentTracker()
outputs = deploy_complete_infrastructure(config, progress_callback=tracker.track)

print(f"\nTotal steps: {len(tracker.steps)}")
```

### Deployment in CI/CD Pipeline

```python
import os
import sys
from util import deploy_complete_infrastructure, DeploymentConfig

def deploy_for_cicd():
    config = DeploymentConfig(
        subscription_id=os.environ['AZURE_SUBSCRIPTION_ID'],
        resource_group=os.environ['RESOURCE_GROUP'],
        tenant_id=os.environ['AZURE_TENANT_ID'],
        client_id=os.environ['AZURE_CLIENT_ID'],
        client_secret=os.environ['AZURE_CLIENT_SECRET']
    )

    try:
        outputs = deploy_complete_infrastructure(config)
        outputs.to_env_file('.env')
        outputs.to_json('outputs.json')
        return 0
    except Exception as e:
        print(f"Deployment failed: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(deploy_for_cicd())
```

## Troubleshooting

### Common Issues

**Issue**: `Azure CLI not installed`
```bash
# Solution: Install Azure CLI
# https://aka.ms/azure-cli
```

**Issue**: `Bicep not installed`
```bash
# Solution: Install Bicep
az bicep install
```

**Issue**: `Authentication failed`
```bash
# Solution: Login to Azure CLI
az login
az account set --subscription "your-subscription-id"
```

**Issue**: `Resource group not found`
```python
# Solution: The module will auto-create the resource group
# Or create manually:
az group create --name lab-master-lab --location uksouth
```

**Issue**: `Quota exceeded for model deployment`
```python
# Solution: Reduce model capacity or request quota increase
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

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from util import deploy_complete_infrastructure, DeploymentConfig
# ... rest of code
```

## Examples

See the `examples/` directory for complete examples:

- `basic_deployment.py`: Simple deployment
- `custom_models.py`: Custom model configuration
- `cicd_deployment.py`: CI/CD pipeline integration
- `notebook_example.ipynb`: Jupyter notebook example

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Check `deployment.log` for detailed error messages
- Review the Bicep templates in `deploy/` directory
- Consult Azure documentation for quota and regional availability

## Version History

**1.0.0** (2025-01-24)
- Initial release
- Support for complete infrastructure deployment
- Resilient model deployment with automatic retry
- Progress tracking and error handling
- Environment file generation
