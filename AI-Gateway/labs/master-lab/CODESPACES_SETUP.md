# Codespaces Setup Guide for Azure AI Gateway Easy Deploy

This guide documents all steps needed to run the `master-ai-gateway-easy-deploy.ipynb` notebook in GitHub Codespaces.

## Quick Setup (TL;DR)

Run this in the terminal after opening Codespaces:

```bash
# 1. Install Python dependencies
pip install --user python-dotenv azure-identity azure-mgmt-resource azure-cosmos openai requests

# 2. Login to Azure
az login --use-device-code

# 3. Set subscription (replace with your subscription ID)
az account set --subscription "YOUR_SUBSCRIPTION_ID"

# 4. Add your Codespace IP to Cosmos DB firewall (if deployed)
./setup-codespace.sh
```

Then restart the Jupyter kernel and run the notebook.

---

## Detailed Setup Steps

### 1. Python Dependencies

The notebook requires several Python packages that may not be pre-installed in Codespaces:

```bash
# Install via pip (user directory to avoid system Python restrictions)
pip install --user python-dotenv azure-identity azure-mgmt-resource azure-cosmos openai requests

# Or install from requirements.txt
pip install --user -r AI-Gateway/labs/master-lab/requirements.txt
```

**After installing, restart the Jupyter kernel** for changes to take effect.

### 2. Azure CLI Authentication

```bash
# Login to Azure (use device code for Codespaces)
az login --use-device-code

# Set your subscription
az account set --subscription "YOUR_SUBSCRIPTION_ID"

# Verify
az account show
```

### 3. Cosmos DB Firewall Configuration

Codespaces runs from dynamic IPs that need to be allowed in Cosmos DB firewall:

```bash
# Get your current IP
CURRENT_IP=$(curl -s ifconfig.me)
echo "Your Codespace IP: $CURRENT_IP"

# Add to Cosmos DB firewall (replace with your values)
az cosmosdb update \
  --name YOUR_COSMOS_ACCOUNT \
  --resource-group YOUR_RESOURCE_GROUP \
  --ip-range-filter "$CURRENT_IP,104.42.195.92,40.76.54.131,52.176.6.30,52.169.50.45,52.187.184.26,0.0.0.0"

# Enable public network access (if disabled)
az cosmosdb update \
  --name YOUR_COSMOS_ACCOUNT \
  --resource-group YOUR_RESOURCE_GROUP \
  --public-network-access Enabled
```

### 4. Environment File

Ensure `master-lab.env` contains all required variables. Key ones that are sometimes missing:

```bash
# Log Analytics (required for cell 26)
LOG_ANALYTICS_CUSTOMER_ID=your-workspace-id

# MCP Weather URL alias (required for cell 33)
MCP_WEATHER_URL=https://your-mcp-weather-url
```

To get Log Analytics workspace ID:
```bash
az monitor log-analytics workspace show \
  --resource-group YOUR_RESOURCE_GROUP \
  --workspace-name YOUR_WORKSPACE \
  --query "customerId" --output tsv
```

---

## Common Issues & Fixes

### Issue: `ModuleNotFoundError: No module named 'dotenv'`

**Fix:** Install python-dotenv and restart kernel:
```bash
pip install --user python-dotenv
# Then restart Jupyter kernel
```

### Issue: `StdinNotImplementedError`

**Cause:** Codespaces notebooks don't support `input()` prompts in some configurations.

**Fix:** Set environment variables before running, or modify the cell to skip the input.

### Issue: `CosmosHttpResponseError: Forbidden`

**Cause:** Codespace IP not in Cosmos DB firewall.

**Fix:** Add your IP to the firewall:
```bash
CURRENT_IP=$(curl -s ifconfig.me)
az cosmosdb update --name YOUR_COSMOS --resource-group YOUR_RG --ip-range-filter "$CURRENT_IP,0.0.0.0"
```

### Issue: `LOG_ANALYTICS_CUSTOMER_ID not found`

**Fix:** Add to master-lab.env:
```bash
# Get workspace ID
WORKSPACE_ID=$(az monitor log-analytics workspace show --resource-group YOUR_RG --workspace-name YOUR_WORKSPACE --query customerId -o tsv)

# Add to env file
echo "LOG_ANALYTICS_CUSTOMER_ID=$WORKSPACE_ID" >> AI-Gateway/labs/master-lab/master-lab.env
```

### Issue: `MCP server 'weather' not configured`

**Fix:** Add MCP_WEATHER_URL to master-lab.env:
```bash
echo "MCP_WEATHER_URL=https://your-mcp-weather-url" >> AI-Gateway/labs/master-lab/master-lab.env
```

### Issue: Tool calling returns response instead of calling tool

**Cause:** Model may respond directly for simple queries.

**Fix:** The notebook now uses `tool_choice="required"` to force tool calling.

---

## Automated Setup Script

Create `setup-codespace.sh` in the repo root:

```bash
#!/bin/bash
set -e

echo "=== Azure AI Gateway Codespaces Setup ==="

# 1. Install dependencies
echo "Installing Python dependencies..."
pip install --user -q python-dotenv azure-identity azure-mgmt-resource azure-cosmos openai requests

# 2. Check Azure login
if ! az account show &>/dev/null; then
    echo "Please login to Azure:"
    az login --use-device-code
fi

# 3. Get current IP and update Cosmos DB
CURRENT_IP=$(curl -s ifconfig.me)
echo "Codespace IP: $CURRENT_IP"

# Read env file for resource names
ENV_FILE="AI-Gateway/labs/master-lab/master-lab.env"
if [ -f "$ENV_FILE" ]; then
    COSMOS_ACCOUNT=$(grep COSMOS_ACCOUNT_NAME "$ENV_FILE" | cut -d'=' -f2)
    RESOURCE_GROUP=$(grep RESOURCE_GROUP "$ENV_FILE" | cut -d'=' -f2)

    if [ -n "$COSMOS_ACCOUNT" ] && [ -n "$RESOURCE_GROUP" ]; then
        echo "Updating Cosmos DB firewall..."
        az cosmosdb update \
          --name "$COSMOS_ACCOUNT" \
          --resource-group "$RESOURCE_GROUP" \
          --ip-range-filter "$CURRENT_IP,104.42.195.92,40.76.54.131,52.176.6.30,52.169.50.45,52.187.184.26,0.0.0.0" \
          --public-network-access Enabled \
          --output none && echo "✅ Cosmos DB firewall updated"
    fi

    # Add Log Analytics if missing
    if ! grep -q "LOG_ANALYTICS_CUSTOMER_ID" "$ENV_FILE"; then
        WORKSPACE_NAME=$(grep WORKSPACE "$ENV_FILE" | head -1 | cut -d'=' -f2 | sed 's/.*\///')
        if [ -n "$WORKSPACE_NAME" ]; then
            WORKSPACE_ID=$(az monitor log-analytics workspace show --resource-group "$RESOURCE_GROUP" --workspace-name "workspace-*" --query customerId -o tsv 2>/dev/null || true)
            if [ -n "$WORKSPACE_ID" ]; then
                echo "LOG_ANALYTICS_CUSTOMER_ID=$WORKSPACE_ID" >> "$ENV_FILE"
                echo "✅ Added LOG_ANALYTICS_CUSTOMER_ID"
            fi
        fi
    fi
fi

echo ""
echo "=== Setup Complete ==="
echo "Now restart the Jupyter kernel and run the notebook!"
```

---

## Required Environment Variables

The notebook expects these in `master-lab.env`:

| Variable | Description | Required For |
|----------|-------------|--------------|
| `APIM_GATEWAY_URL` | APIM Gateway base URL | All cells |
| `APIM_API_KEY` | APIM subscription key | All API calls |
| `OPENAI_ENDPOINT` | Full OpenAI endpoint with /inference | OpenAI calls |
| `COSMOS_ENDPOINT` | Cosmos DB endpoint | Message storing |
| `LOG_ANALYTICS_CUSTOMER_ID` | Log Analytics workspace ID | Cell 26 |
| `MCP_WEATHER_URL` | MCP Weather server URL | Cell 33 |

---

## Post-Deployment Checklist

After running the deployment cell, verify:

- [ ] `master-lab.env` was created with all variables
- [ ] Azure resources are accessible (run `quick_init()`)
- [ ] Cosmos DB firewall includes your Codespace IP
- [ ] Cosmos DB public network access is enabled
- [ ] Log Analytics workspace ID is in env file
- [ ] MCP server URLs are in env file
