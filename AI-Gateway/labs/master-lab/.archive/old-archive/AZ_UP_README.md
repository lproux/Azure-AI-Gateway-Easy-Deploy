# Master AI Gateway Lab - Automated Deployment (`az up`)

## Overview

The `az_up` deployment automation provides a one-command deployment of all Azure resources needed for the Master AI Gateway Lab. It mimics the behavior of `azd up` or `az up` by deploying infrastructure, configuring services, and generating environment files automatically.

## Features

- **One-Command Deployment**: Deploy all resources with a single command
- **Resilient**: Automatically detects and skips already-deployed resources
- **Resumable**: Can resume from failed steps
- **Progress Tracking**: Real-time progress updates with color-coded output
- **Environment Generation**: Automatically generates `.env` file with all outputs
- **Cross-Platform**: Works on Windows, macOS, Linux, and WSL
- **4-Step Process**: Deploys infrastructure in logical order
  - Step 1: Core (APIM, Log Analytics, App Insights) - ~10 min
  - Step 2: AI Foundry (3 hubs + 14 models) - ~15 min
  - Step 3: Supporting Services (Redis, Search, Cosmos) - ~10 min
  - Step 4: MCP Servers (Container Apps + 7 servers) - ~5 min

## Prerequisites

1. **Azure CLI**: Installed and authenticated
   ```bash
   az login
   ```

2. **Python 3.11+**: Required for deployment script
   ```bash
   python --version  # Should be 3.11 or higher
   ```

3. **Azure SDK for Python**: Installed automatically or manually
   ```bash
   pip install azure-identity azure-mgmt-resource
   ```

4. **Subscription Permissions**: Contributor or Owner role on target subscription

## Quick Start

### Option 1: Using Bash Script (Recommended)

```bash
# Navigate to lab directory
cd MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab

# Run deployment
./az_up.sh

# Or with custom options
./az_up.sh --location eastus --resource-group my-lab-rg
```

### Option 2: Using Python Script

```bash
# Navigate to lab directory
cd MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab

# Deploy with default settings
python az_up.py

# Deploy with custom configuration
python az_up.py --subscription-id "your-sub-id" --location "eastus"
```

### Option 3: From Notebook

```python
# Run from Jupyter notebook cell
!python az_up.py

# Or with parameters
!python az_up.py --location eastus --resource-group my-lab-rg
```

## Command-Line Options

```
usage: az_up.py [-h] [--subscription-id ID] [--location LOCATION]
                [--resource-group NAME] [--prefix PREFIX] [--no-color]

Master AI Gateway Lab - Automated Deployment

optional arguments:
  -h, --help            Show help message and exit
  --subscription-id ID, -s ID
                        Azure subscription ID (defaults to current Azure CLI)
  --location LOCATION, -l LOCATION
                        Azure region (default: uksouth)
  --resource-group NAME, -g NAME
                        Resource group name (default: lab-master-lab)
  --prefix PREFIX, -p PREFIX
                        Deployment name prefix (default: master-lab)
  --no-color            Disable color output
```

## Examples

### Deploy to Default Location (UK South)
```bash
./az_up.sh
```

### Deploy to Specific Region
```bash
python az_up.py --location eastus
```

### Deploy with Custom Resource Group
```bash
python az_up.py --resource-group prod-ai-gateway --location westus2
```

### Deploy to Specific Subscription
```bash
python az_up.py --subscription-id "12345678-1234-1234-1234-123456789abc"
```

### Deploy Without Colors (for CI/CD)
```bash
python az_up.py --no-color | tee deployment.log
```

## Deployment Process

### Step 1: Core Infrastructure (~10 minutes)

Deploys:
- API Management (APIM) instance
- Log Analytics workspace
- Application Insights

**Status Check**: Script checks if deployment already succeeded and skips if so.

### Step 2: AI Foundry (~15 minutes)

Deploys:
- 3 AI Foundry hubs (Hub A, Hub B, Hub C)
- 14 AI models across hubs
- Model deployments

**Note**: This is the longest step due to model deployments.

### Step 3: Supporting Services (~10 minutes)

Deploys:
- Azure Cache for Redis
- Azure AI Search
- Cosmos DB
- Content Safety service

### Step 4: MCP Servers (~5 minutes)

Deploys:
- Azure Container Apps environment
- 7 MCP servers:
  - Weather MCP
  - OnCall MCP
  - GitHub MCP
  - Spotify MCP
  - Excel MCP
  - SQL MCP
  - Custom MCP

## Output

### Console Output

Real-time progress with color-coded messages:
- `[*]` (Blue): Information
- `[OK]` (Green): Success
- `[WARN]` (Yellow): Warning (non-critical)
- `[ERROR]` (Red): Error (critical)

Example output:
```
================================================================================
STEP 1: CORE INFRASTRUCTURE (APIM, Log Analytics, App Insights)
================================================================================
Deployment: master-lab-01-core
Bicep Template: main-step1-core.bicep
Estimated Time: ~10 minutes

[*] Compiling Bicep template...
[*] Starting deployment...
[*] Deployment in progress... (2m 15s elapsed)
[*] Deployment in progress... (5m 30s elapsed)
[OK] Deployment succeeded in 8m 45s
```

### Environment File

After successful deployment, a `master-lab.env` file is generated with all deployment outputs:

```env
# Master AI Gateway Lab - Environment Variables
# Generated: 2025-11-09T22:45:30

# Azure Configuration
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_RESOURCE_GROUP=lab-master-lab
AZURE_LOCATION=uksouth

# Step 1: Core Infrastructure Outputs
APIM_NAME=apim-master-lab-abc123
APIM_ENDPOINT=https://apim-master-lab-abc123.azure-api.net
LOG_ANALYTICS_WORKSPACE_ID=/subscriptions/.../workspace-id
...

# Step 2: AI Foundry Outputs
HUB_A_ENDPOINT=https://hub-a.openai.azure.com
HUB_A_KEY=...
...

# Step 3: Supporting Services Outputs
REDIS_CONNECTION_STRING=...
COSMOS_ENDPOINT=...
...

# Step 4: MCP Servers Outputs
MCP_WEATHER_ENDPOINT=https://mcp-weather.app.azure.com
...
```

## Troubleshooting

### Authentication Issues

**Problem**: `Azure authentication failed`

**Solution**:
```bash
# Re-authenticate with Azure CLI
az login

# Or use device code flow
az login --use-device-code

# Verify authentication
az account show
```

### Bicep Compilation Errors

**Problem**: `Bicep compilation failed`

**Solution**:
```bash
# Ensure Bicep is installed
az bicep install

# Update to latest version
az bicep upgrade

# Verify installation
az bicep version
```

### Deployment Timeout

**Problem**: Deployment takes longer than expected

**Solution**:
- This is normal, especially for Step 2 (AI Foundry)
- The script will continue waiting
- You can monitor in Azure Portal:
  ```bash
  # Open deployment in portal
  az deployment group show --resource-group lab-master-lab --name master-lab-01-core
  ```

### Partial Failure

**Problem**: One step failed but others succeeded

**Solution**:
- Re-run the script - it will skip successful deployments
  ```bash
  ./az_up.sh
  ```
- The script automatically checks deployment status and resumes

### Missing Bicep Templates

**Problem**: `Bicep file not found`

**Solution**:
- Ensure you're in the correct directory:
  ```bash
  cd MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab
  ```
- Verify `bicep/` directory exists with templates

### Region Capacity Issues

**Problem**: `Region does not support this resource type`

**Solution**:
- Try a different region:
  ```bash
  python az_up.py --location eastus
  # or
  python az_up.py --location westeurope
  ```

Recommended regions:
- `eastus` (US East)
- `westus2` (US West 2)
- `uksouth` (UK South) - default
- `westeurope` (West Europe)

## Resuming Failed Deployments

The script is resilient and can resume from failed steps:

1. **Identify the failed step** from console output
2. **Fix the issue** (quota, permissions, etc.)
3. **Re-run the script**:
   ```bash
   ./az_up.sh
   ```
4. The script will:
   - Check each deployment status
   - Skip successful deployments
   - Retry failed deployments

Example:
```
Step 1: [OK] Deployment already succeeded, skipping
Step 2: [OK] Deployment already succeeded, skipping
Step 3: [*] Starting deployment...  # Resumes here
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy AI Gateway Lab

on:
  workflow_dispatch:
    inputs:
      location:
        description: 'Azure region'
        required: true
        default: 'uksouth'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Install Python dependencies
        run: pip install azure-identity azure-mgmt-resource

      - name: Run deployment
        working-directory: MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab
        run: |
          python az_up.py \
            --location ${{ github.event.inputs.location }} \
            --no-color
```

### Azure DevOps Pipeline Example

```yaml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: AzureCLI@2
    displayName: 'Deploy AI Gateway Lab'
    inputs:
      azureSubscription: 'YOUR_SERVICE_CONNECTION'
      scriptType: 'bash'
      scriptLocation: 'inlineScript'
      inlineScript: |
        cd MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab
        pip install azure-identity azure-mgmt-resource
        python az_up.py --no-color
```

## Cleanup

To delete all deployed resources:

```bash
# Delete resource group (removes all resources)
az group delete --name lab-master-lab --yes --no-wait

# Or use cleanup script (if available)
python cleanup.py --resource-group lab-master-lab
```

## Next Steps

After successful deployment:

1. **Load environment variables**:
   ```bash
   source master-lab.env
   ```

2. **Open Jupyter notebook**:
   ```bash
   jupyter notebook master-ai-gateway.ipynb
   ```

3. **Run cells sequentially** following lab instructions

4. **Test deployed services**:
   - APIM endpoints
   - AI models
   - MCP servers

## Files Created

- `master-lab.env` - Environment variables with deployment outputs
- `.azure-credentials.env` - Service Principal credentials (if used)
- Deployment logs in Azure Portal

## Estimated Costs

Approximate monthly costs (varies by region and usage):

| Service | Estimated Cost |
|---------|---------------|
| API Management (Developer tier) | $50 |
| AI Foundry Hubs (3) + Models (14) | $500-$1000 |
| Redis Cache (Basic) | $15 |
| Azure AI Search (Basic) | $75 |
| Cosmos DB (Serverless) | $10-$50 |
| Container Apps (MCP servers) | $20 |
| **Total** | **$670-$1210/month** |

**Note**: Costs vary significantly based on:
- AI model usage (tokens processed)
- Container Apps scale
- Redis cache usage
- Search query volume

## Support

For issues:
1. Check `COMPREHENSIVE-TEST-REPORT.md` for notebook validation results
2. Review Azure Portal deployment logs
3. Check Azure resource health in portal
4. Review [troubleshooting section](#troubleshooting) above

## Version Information

- **Python**: 3.11+
- **Azure CLI**: Latest
- **Azure SDK**: azure-identity, azure-mgmt-resource
- **Bicep**: Latest (via Azure CLI)

Last Updated: 2025-11-09
