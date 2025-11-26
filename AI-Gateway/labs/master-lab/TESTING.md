# Testing Guide - Azure AI Gateway Easy Deploy

This guide provides comprehensive testing instructions for running the `master-ai-gateway-easy-deploy.ipynb` notebook in both GitHub Codespaces and VS Code Dev Containers.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start (GitHub Codespaces)](#quick-start-github-codespaces)
- [Local Setup (VS Code Dev Container)](#local-setup-vs-code-dev-container)
- [Running the Notebook](#running-the-notebook)
- [Verification Steps](#verification-steps)
- [Troubleshooting](#troubleshooting)
- [Common Issues](#common-issues)

---

## Prerequisites

### Azure Requirements

Before you start, ensure you have:

1. **Azure Subscription** with appropriate permissions:
   - **Required Role**: [Contributor](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles/privileged#contributor) + [RBAC Administrator](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles/privileged#role-based-access-control-administrator)
   - **OR**: [Owner](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles/privileged#owner) role
   - Note your subscription ID (you'll need it during deployment)

2. **Azure OpenAI Access**:
   - Azure OpenAI Service must be enabled for your subscription
   - If not already enabled, [request access](https://aka.ms/oai/access)
   - Approval typically takes 1-2 business days

3. **Sufficient Quotas**:
   - API Management: StandardV2 tier (1 instance minimum)
   - Azure OpenAI: PTU or pay-as-you-go quota in desired regions
   - Azure Cache for Redis: Enterprise tier
   - Container Apps: Sufficient core quota

### GitHub Requirements

- GitHub account (free tier is sufficient)
- For Codespaces:
  - Free tier includes 60 hours/month (4-core machine)
  - Premium tier includes 180 hours/month
  - [Check your quota](https://github.com/settings/billing)

### Local Development Requirements (Dev Container Only)

If testing locally with Dev Containers:

- **Docker Desktop** (latest version)
  - [Windows](https://docs.docker.com/desktop/install/windows-install/)
  - [Mac](https://docs.docker.com/desktop/install/mac-install/)
  - [Linux](https://docs.docker.com/desktop/install/linux-install/)
  - Minimum: 8GB RAM allocated to Docker
  - Recommended: 16GB RAM allocated

- **VS Code** with extensions:
  - [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) (ms-vscode-remote.remote-containers)
  - [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) (optional, installed in container)
  - [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) (optional, installed in container)

---

## Quick Start (GitHub Codespaces)

GitHub Codespaces provides a complete, cloud-based development environment with all dependencies pre-installed.

### Step 1: Launch Codespace

**Option A: Using the Badge (Recommended)**

Click the badge in the repository README:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/lproux/Azure-AI-Gateway-Easy-Deploy?quickstart=1)

**Option B: From GitHub UI**

1. Navigate to https://github.com/lproux/Azure-AI-Gateway-Easy-Deploy
2. Click the green **Code** button
3. Select the **Codespaces** tab
4. Click **Create codespace on main**

**Option C: From Codespaces Dashboard**

1. Go to https://github.com/codespaces
2. Click **New codespace**
3. Select repository: `lproux/Azure-AI-Gateway-Easy-Deploy`
4. Select branch: `main`
5. Click **Create codespace**

### Step 2: Wait for Environment Setup

The Codespace will automatically:
- Build the container (first time: ~3-5 minutes)
- Install Python dependencies
- Configure Azure CLI and Bicep
- Set up Jupyter kernel
- Install VS Code extensions

**You'll see:**
```
Starting Dev Container (show log)
Building: 1/10
Building: 2/10 (Installing Python packages...)
...
Dev container is running
```

### Step 3: Authenticate to Azure

Once the Codespace is ready:

1. Open a new terminal: `Terminal` → `New Terminal`
2. Login to Azure:
   ```bash
   az login --use-device-code
   ```
3. Follow the prompts:
   - Click the link shown (https://microsoft.com/devicelogin)
   - Enter the device code
   - Sign in with your Azure credentials
4. Set your subscription:
   ```bash
   az account set --subscription <your-subscription-id>
   ```
5. Verify authentication:
   ```bash
   az account show
   ```

### Step 4: Open the Notebook

The notebook should open automatically. If not:

1. Navigate to: `AI-Gateway/labs/master-lab/`
2. Open: `master-ai-gateway-easy-deploy.ipynb`
3. Select kernel: **Python 3.11.x** (should be auto-selected)

### Step 5: Run the Notebook

See [Running the Notebook](#running-the-notebook) section below.

---

## Local Setup (VS Code Dev Container)

For local development with full control and offline capability.

### Step 1: Clone the Repository

```bash
git clone https://github.com/lproux/Azure-AI-Gateway-Easy-Deploy.git
cd Azure-AI-Gateway-Easy-Deploy/AI-Gateway/labs/master-lab
```

### Step 2: Open in VS Code

```bash
code .
```

Or:
1. Open VS Code
2. File → Open Folder
3. Navigate to `Azure-AI-Gateway-Easy-Deploy/AI-Gateway/labs/master-lab`
4. Click **Select Folder**

### Step 3: Reopen in Container

VS Code will detect the `.devcontainer` configuration:

**Option A: Automatic Prompt**
- VS Code shows notification: **"Folder contains a Dev Container configuration file"**
- Click **Reopen in Container**

**Option B: Manual Command**
1. Press `F1` or `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
2. Type: `Dev Containers: Reopen in Container`
3. Press Enter

**Option C: From Status Bar**
- Click the green **><** icon in bottom-left corner
- Select **Reopen in Container**

### Step 4: Wait for Container Build

First time setup (5-8 minutes):
- Downloads base image (~1GB)
- Installs system dependencies
- Installs Python packages from requirements.txt
- Configures Azure CLI, Bicep, Node.js
- Installs VS Code extensions

**Progress indicators:**
```
Starting Dev Container (show log)
Building image...
Running postCreateCommand...
Installing Python packages...
Configuring environment...
```

**View detailed logs:**
- Click "show log" in the notification
- Or check: `Terminal` → `Dev Containers` output

### Step 5: Authenticate to Azure

Same as Codespaces:

```bash
az login --use-device-code
az account set --subscription <your-subscription-id>
az account show
```

### Step 6: Open the Notebook

1. Navigate to: `master-ai-gateway-easy-deploy.ipynb` in Explorer
2. Click to open
3. Select kernel: **Python 3.11.x** (from `.venv` if created, or system Python)

---

## Running the Notebook

Once your environment is ready (Codespaces or Dev Container):

### Cell 1: Dependency Check

```python
# Cell 1: Check dependencies and attempt installation if needed
```

**Expected Output:**
```
Checking dependencies...
✅ All required packages are already available
   Found: python-dotenv, azure-identity, azure-mgmt-resource and 3 more

✅ Dependency check complete - proceeding with notebook
```

**If packages are missing:**
- The cell will attempt automatic installation
- If in externally-managed environment: Follow prompts to create venv
- Re-run the cell after installation

### Cell 2-4: One-Command Deployment

```python
# Cell 4: Deploy complete infrastructure
```

**What happens:**
1. **Prompts for Subscription ID**
   - Press Enter to auto-detect from Azure CLI
   - Or paste your subscription ID

2. **Deployment Starts** (~35-60 minutes total)
   - Step 1: Core Infrastructure (APIM, App Insights) - 15 min
   - Step 2: AI Foundry Hubs + Models - 30 min
   - Step 3: Supporting Services (Redis, Cosmos, Search) - 10 min
   - Step 4: MCP Servers (Container Apps) - 5 min
   - Post-Deployment: APIM Configuration - 2 min

3. **Progress Updates**
   ```
   🔄 [IN_PROGRESS] Core Infrastructure: Deploying APIM, App Insights, Log Analytics...
   ✅ [COMPLETED] Core Infrastructure: Already deployed (skipped)
   🔄 [IN_PROGRESS] AI Foundry Hubs: Deploying AI Foundry hubs and models...
   ```

**Expected Final Output:**
```
======================================================================
✅ DEPLOYMENT COMPLETE!
======================================================================
```

### Cell 5: Save Configuration

```python
# Cell 5: Save outputs to environment file
```

**Creates:** `master-lab.env` with all resource endpoints and keys

**Expected Output:**
```
✅ Configuration saved to master-lab.env

Key Resources:
  • APIM Gateway: https://apim-xxxxx.azure-api.net
  • Redis Host: redis-xxxxx.uksouth.redis.azure.net
  • Cosmos DB: https://cosmos-xxxxx.documents.azure.com:443/
  ...
```

### Cells 6-33: Lab Exercises

Run cells sequentially:

- **Cell 8**: Initialize shared configuration (quick_init)
- **Cells 10-12**: Lab 1.1 - Access Control
- **Cells 14-16**: Lab 1.2 - Load Balancing
- **Cells 18-20**: Lab 1.3 - Token Metrics
- **Cells 22-24**: Lab 1.4 - Content Safety
- **Cells 26-28**: Lab 2.1 - Semantic Caching
- **Cells 30-32**: Lab 2.2 - Message Storing
- And so on...

**Each lab typically takes 2-5 minutes to run.**

---

## Verification Steps

### 1. Environment Verification

Before deployment, verify your environment:

```bash
# Check Python version
python --version
# Expected: Python 3.11.x or 3.12.x

# Check Azure CLI
az version
# Expected: azure-cli 2.50.0 or later

# Check Azure CLI authentication
az account show
# Expected: Your subscription details

# Check Bicep
az bicep version
# Expected: 0.20.0 or later

# Check installed Python packages
pip list | grep azure
# Expected: Multiple azure-* packages
```

### 2. Deployment Verification

After deployment completes:

**A. Verify Resource Group**

```bash
az group show --name lab-master-lab
# Expected: provisioningState: "Succeeded"
```

**B. List All Resources**

```bash
az resource list --resource-group lab-master-lab --output table
# Expected: ~20 resources including:
# - apim-* (API Management)
# - foundry1/2/3-* (AI Foundry Hubs)
# - redis-* (Redis Enterprise)
# - cosmos-* (Cosmos DB)
# - search-* (AI Search)
# - mcp-* (5 Container Apps)
```

**C. Check APIM Status**

```bash
az apim show --name apim-<suffix> --resource-group lab-master-lab --query "provisioningState"
# Expected: "Succeeded"
```

**D. Verify AI Foundry Models**

```bash
az cognitiveservices account deployment list \
  --name foundry1-<suffix> \
  --resource-group lab-master-lab \
  --output table
# Expected: gpt-4o-mini, gpt-4o, text-embedding-3-small, text-embedding-3-large
```

**E. Test APIM Gateway**

```bash
# Get APIM subscription key
APIM_KEY=$(az rest \
  --method post \
  --uri "/subscriptions/<sub-id>/resourceGroups/lab-master-lab/providers/Microsoft.ApiManagement/service/apim-<suffix>/subscriptions/master/listSecrets?api-version=2022-08-01" \
  --query primaryKey -o tsv)

# Test API call
curl -X POST "https://apim-<suffix>.azure-api.net/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-10-21" \
  -H "api-key: $APIM_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Say hello"}],
    "max_tokens": 10
  }'
# Expected: JSON response with "choices" array
```

### 3. Lab Exercise Verification

**Lab 1.1: Access Control**
- Cell 10 should return: `401 ✅ Expected` (no auth)
- Cell 10 should return: `200 ✅` (with auth)
- Response should be: "Hello from APIM!"

**Lab 1.2: Load Balancing**
- Cell 12 should show distribution across 3 backends
- Each backend should handle ~33% of requests

**Lab 1.3: Token Metrics**
- Cell 14 should query Cosmos DB and show token counts
- Should display: Total Requests, Prompt Tokens, Completion Tokens

**Lab 2.1: Semantic Caching**
- Cell 19 should show cache speedup
- Second call should be faster than first (or <1s)

**Lab 2.2: Message Storing**
- Cell 21 should store 3 messages in Cosmos DB
- Verification should show: "Messages stored: 3/3"

**Lab 2.3: Vector Search (RAG)**
- Cell 23 should embed query and generate RAG response
- Response should reference the retrieved context

---

## Troubleshooting

### Container Issues

**Problem: Container fails to build**

```
Error: Failed to create container
```

**Solution:**
1. Ensure Docker Desktop is running (Dev Container only)
2. Check Docker has sufficient resources (8GB RAM minimum)
3. Clear Docker cache: `docker system prune -a`
4. Retry: `Dev Containers: Rebuild Container`

**Problem: Extensions not installing**

**Solution:**
1. Wait for container to fully start
2. Reload window: `Developer: Reload Window`
3. Manually install: `Extensions` → Search → Install

### Azure Authentication Issues

**Problem: `az login` fails**

```
ERROR: Please run 'az login' to setup account.
```

**Solution:**
1. Use device code flow: `az login --use-device-code`
2. If browser doesn't open, manually navigate to link
3. Ensure cookies/JavaScript enabled in browser
4. Try incognito/private browsing mode

**Problem: Subscription not found**

```
ERROR: Subscription '<name>' not found.
```

**Solution:**
1. List subscriptions: `az account list --output table`
2. Use subscription ID instead of name:
   ```bash
   az account set --subscription "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
   ```
3. Verify access: `az account show`

### Deployment Issues

**Problem: Deployment timeout**

```
ERROR: Deployment exceeded timeout of 3600 seconds.
```

**Solution:**
1. APIM takes 30-45 minutes - this is normal
2. Check status: `az deployment group show --name <deployment> --resource-group lab-master-lab`
3. If "Running", wait longer
4. If "Failed", check error details:
   ```bash
   az deployment group show --name <deployment> --resource-group lab-master-lab --query "properties.error"
   ```

**Problem: Quota exceeded**

```
ERROR: Operation could not be completed as it results in exceeding approved quota.
```

**Solution:**
1. Check quota: `az vm list-usage --location uksouth --output table`
2. Request increase: [Azure Portal → Quotas](https://portal.azure.com/#blade/Microsoft_Azure_Capacity/QuotaMenuBlade/overview)
3. Choose different region with available quota
4. Use smaller SKUs for testing (modify Bicep templates)

**Problem: Model deployment fails**

```
ERROR: (InsufficientQuota) This operation require 50 new capacity
```

**Solution:**
1. This is common for gpt-4o in some regions
2. The notebook continues with other models - this is OK
3. Request quota increase for specific model
4. Or use gpt-4o-mini exclusively (lower quota requirements)

### Notebook Issues

**Problem: Kernel not found**

```
Kernel not found
```

**Solution:**
1. Install kernel: `python -m ipykernel install --user --name=python3`
2. Refresh kernel list: Click kernel selector → Refresh
3. Select: **Python 3.11.x**

**Problem: Module not found**

```
ModuleNotFoundError: No module named 'azure'
```

**Solution:**
1. Verify requirements installed: `pip list | grep azure`
2. Reinstall: `pip install -r requirements.txt`
3. Restart kernel: `Kernel` → `Restart Kernel`
4. Re-run Cell 1 (dependency check)

**Problem: `quick_init()` fails**

```
ERROR: Environment file not found: master-lab.env
```

**Solution:**
1. Ensure Cell 4 (deployment) completed successfully
2. Ensure Cell 5 (save outputs) executed
3. Check file exists: `ls -la master-lab.env`
4. Re-run Cell 5 if needed

### Performance Issues

**Problem: Notebook cells run slowly**

**Solution (Codespaces):**
1. Check machine type: 4-core is recommended
2. Upgrade: Settings → Change machine type → 8-core
3. Monitor resources: `htop` command

**Solution (Dev Container):**
1. Increase Docker memory: Docker Desktop → Settings → Resources
2. Recommended: 12-16GB RAM
3. Close other applications
4. Restart Docker Desktop

**Problem: Deployment takes too long**

**Expected times:**
- Core Infrastructure: 15-20 minutes (APIM is slow)
- AI Foundry Hubs: 25-35 minutes (model deployments)
- Total: 45-60 minutes

**If exceeding 90 minutes:**
1. Check Azure Portal for errors
2. Review deployment logs: `az deployment group show`
3. May need to delete and retry:
   ```bash
   az group delete --name lab-master-lab --yes --no-wait
   # Wait 10 minutes, then re-run deployment
   ```

---

## Common Issues

### Issue: "externally-managed-environment" Error

**Symptoms:**
```
error: externally-managed-environment
This environment is externally managed
```

**Solution (Recommended):**
Create a virtual environment:

```bash
cd AI-Gateway/labs/master-lab
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

Then select the venv kernel in Jupyter:
1. Click kernel selector (top-right)
2. Select **Python 3.11.x** (`.venv/bin/python`)

**Solution (Alternative):**
Install to user directory:
```bash
pip install --user -r requirements.txt
```

### Issue: Unicode Encoding Errors

**Symptoms:**
```
UnicodeEncodeError: 'charmap' codec can't encode character
```

**Solution:**
Already fixed in notebook cells. If you see this:

1. Set environment variable:
   ```bash
   export PYTHONIOENCODING=utf-8
   ```

2. Restart kernel

3. Azure SDK logging is disabled in notebook to prevent this

### Issue: MCP Servers Not Responding

**Symptoms:**
```
⚠️  MCP servers not responding (may be scaled to zero)
Using demo mode to demonstrate the workflow...
```

**Explanation:**
- Container Apps scale to zero when idle (cost optimization)
- First request wakes them up (~10-30 seconds)
- Demo mode simulates MCP workflow

**Solution (to test real MCP):**
1. Wait 30 seconds and retry
2. Or wake up manually:
   ```bash
   curl https://mcp-weather-<suffix>.niceriver-<region>.azurecontainerapps.io/mcp/
   ```
3. Then re-run the cell

### Issue: Token Metrics Show Zero

**Symptoms:**
```
⚠️  No messages in Cosmos DB yet
```

**Explanation:**
- Cell 14 queries Cosmos DB for stored messages
- Messages only exist after running Cell 21 (Message Storing lab)

**Solution:**
1. Run Cell 21 first (stores 3 messages)
2. Then re-run Cell 14
3. Should show: "Total Requests: 3" or more

### Issue: Cost Concerns

**Estimated Monthly Costs:**
- APIM StandardV2: ~$175
- AI Model Usage: ~$500-800 (varies by usage)
- Redis Enterprise: ~$20
- AI Search: ~$75
- Cosmos DB: ~$25
- Container Apps: ~$30
- Log Analytics: ~$50
- **Total: ~$890-1,190/month**

**Cost Optimization:**
1. **Delete resources when not in use:**
   ```bash
   az group delete --name lab-master-lab --yes --no-wait
   ```

2. **Use gpt-4o-mini** (15-20x cheaper than gpt-4o):
   - Already the default in this notebook
   - $0.15 per 1M input tokens
   - $0.60 per 1M output tokens

3. **Enable semantic caching** (Lab 2.1):
   - 50-80% cost reduction for repeated queries
   - Already configured in deployment

4. **Set token limits:**
   - Use `max_tokens` parameter in API calls
   - Prevents runaway costs

5. **Monitor usage:**
   - Cell 14 shows token metrics
   - Azure Portal → Cost Management

6. **Auto-shutdown Codespaces:**
   - Settings → Codespaces → Set timeout (e.g., 30 minutes)
   - Prevents forgetting to stop

---

## Additional Resources

### Documentation
- [Master Lab README](./README.md) - Complete guide
- [Easy Deploy Quick Start](./EASY_DEPLOY_QUICKSTART.md) - Quick reference
- [Easy Deploy README](./EASY_DEPLOY_README.md) - Detailed documentation
- [Dev Container README](./.devcontainer/README.md) - Container configuration

### Tools & Validation
- [Setup Validation Script](./validate-setup.sh) - Run before deployment
- [Requirements](./requirements.txt) - Python dependencies
- [Post-Create Script](./.devcontainer/post-create.sh) - Auto-setup script

### Azure Resources
- [Azure CLI Reference](https://learn.microsoft.com/cli/azure/)
- [Azure OpenAI Quotas](https://learn.microsoft.com/azure/ai-services/openai/quotas-limits)
- [APIM Documentation](https://learn.microsoft.com/azure/api-management/)
- [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)

### Support
- [GitHub Issues](https://github.com/lproux/Azure-AI-Gateway-Easy-Deploy/issues)
- [Azure Support](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade)
- [Dev Containers FAQ](https://code.visualstudio.com/docs/devcontainers/faq)

---

## Next Steps

Once you've successfully run the notebook:

1. **Explore Individual Labs**: Try the Quick Start modular labs in `quick_start/`
2. **Customize Deployment**: Modify `DeploymentConfig` in Cell 4
3. **Production Deployment**: Review [Zero-to-Production Lab](../zero-to-production/)
4. **Advanced Features**: Explore MCP integration, real-time audio, agents
5. **Cost Management**: Implement FinOps framework (Lab 2.4 in full notebook)

---

**Last Updated**: 2025-11-26
**Notebook Version**: Easy Deploy v2.0
**Environment**: Python 3.11+ | Azure CLI 2.50+ | Bicep 0.20+
