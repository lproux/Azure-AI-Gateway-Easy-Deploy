#!/bin/bash
# Azure AI Gateway - Codespaces Setup Script
# Run this after opening a new Codespace to prepare for the notebook

set -e

echo "=============================================================="
echo "Azure AI Gateway - Codespaces Setup"
echo "=============================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Install Python dependencies
echo -e "${YELLOW}[1/5] Installing Python dependencies...${NC}"
pip install --user -q python-dotenv azure-identity azure-mgmt-resource azure-cosmos openai requests 2>/dev/null
echo -e "${GREEN}✅ Dependencies installed${NC}"
echo ""

# 2. Check Azure login
echo -e "${YELLOW}[2/5] Checking Azure authentication...${NC}"
if az account show &>/dev/null; then
    ACCOUNT=$(az account show --query "user.name" -o tsv 2>/dev/null)
    SUBSCRIPTION=$(az account show --query "name" -o tsv 2>/dev/null)
    echo -e "${GREEN}✅ Logged in as: $ACCOUNT${NC}"
    echo -e "   Subscription: $SUBSCRIPTION"
else
    echo -e "${RED}⚠️  Not logged in to Azure${NC}"
    echo "   Please run: az login --use-device-code"
    echo ""
    read -p "Login now? (y/N): " login_choice
    if [[ "$login_choice" =~ ^[Yy]$ ]]; then
        az login --use-device-code
    else
        echo "Skipping Azure login. Some features may not work."
    fi
fi
echo ""

# 3. Get current IP
echo -e "${YELLOW}[3/5] Detecting Codespace IP...${NC}"
CURRENT_IP=$(curl -s ifconfig.me 2>/dev/null || echo "unknown")
echo -e "${GREEN}✅ Codespace IP: $CURRENT_IP${NC}"
echo ""

# 4. Update Cosmos DB firewall if env file exists
ENV_FILE="AI-Gateway/labs/master-lab/master-lab.env"
echo -e "${YELLOW}[4/5] Configuring Cosmos DB access...${NC}"

if [ -f "$ENV_FILE" ]; then
    COSMOS_ACCOUNT=$(grep "^COSMOS_ACCOUNT_NAME=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2)
    RESOURCE_GROUP=$(grep "^RESOURCE_GROUP=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2)

    if [ -n "$COSMOS_ACCOUNT" ] && [ -n "$RESOURCE_GROUP" ] && [ "$CURRENT_IP" != "unknown" ]; then
        echo "   Cosmos Account: $COSMOS_ACCOUNT"
        echo "   Resource Group: $RESOURCE_GROUP"
        echo "   Adding IP to firewall (this takes 2-5 minutes)..."

        az cosmosdb update \
          --name "$COSMOS_ACCOUNT" \
          --resource-group "$RESOURCE_GROUP" \
          --ip-range-filter "$CURRENT_IP,104.42.195.92,40.76.54.131,52.176.6.30,52.169.50.45,52.187.184.26,0.0.0.0" \
          --public-network-access Enabled \
          --output none 2>/dev/null && echo -e "${GREEN}✅ Cosmos DB firewall updated${NC}" || echo -e "${YELLOW}⚠️  Could not update Cosmos DB (may not be deployed yet)${NC}"
    else
        echo -e "${YELLOW}⚠️  Cosmos DB not configured (deploy first using the notebook)${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Environment file not found${NC}"
    echo "   Run the deployment cell in the notebook first"
fi
echo ""

# 5. Add missing environment variables
echo -e "${YELLOW}[5/5] Checking environment variables...${NC}"

if [ -f "$ENV_FILE" ]; then
    MISSING_VARS=0

    # Check LOG_ANALYTICS_CUSTOMER_ID
    if ! grep -q "^LOG_ANALYTICS_CUSTOMER_ID=" "$ENV_FILE" 2>/dev/null; then
        WORKSPACE_NAME=$(grep "workspace-" "$ENV_FILE" 2>/dev/null | head -1 | grep -oP 'workspace-[a-z0-9]+' || true)
        if [ -n "$WORKSPACE_NAME" ] && [ -n "$RESOURCE_GROUP" ]; then
            WORKSPACE_ID=$(az monitor log-analytics workspace show --resource-group "$RESOURCE_GROUP" --workspace-name "$WORKSPACE_NAME" --query customerId -o tsv 2>/dev/null || true)
            if [ -n "$WORKSPACE_ID" ]; then
                echo "LOG_ANALYTICS_CUSTOMER_ID=$WORKSPACE_ID" >> "$ENV_FILE"
                echo "LOG_ANALYTICS_WORKSPACE_NAME=$WORKSPACE_NAME" >> "$ENV_FILE"
                echo -e "${GREEN}✅ Added LOG_ANALYTICS_CUSTOMER_ID${NC}"
            else
                echo -e "${YELLOW}⚠️  Could not find Log Analytics workspace${NC}"
                MISSING_VARS=1
            fi
        fi
    else
        echo -e "${GREEN}✅ LOG_ANALYTICS_CUSTOMER_ID present${NC}"
    fi

    # Check MCP_WEATHER_URL
    if ! grep -q "^MCP_WEATHER_URL=" "$ENV_FILE" 2>/dev/null; then
        MCP_URL=$(grep "^MCP_SERVER_WEATHER_URL=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2)
        if [ -n "$MCP_URL" ]; then
            echo "MCP_WEATHER_URL=$MCP_URL" >> "$ENV_FILE"
            echo -e "${GREEN}✅ Added MCP_WEATHER_URL${NC}"
        else
            echo -e "${YELLOW}⚠️  MCP_WEATHER_URL not found${NC}"
            MISSING_VARS=1
        fi
    else
        echo -e "${GREEN}✅ MCP_WEATHER_URL present${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  No environment file to check${NC}"
fi

echo ""
echo "=============================================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=============================================================="
echo ""
echo "Next steps:"
echo "  1. Restart the Jupyter kernel (if already open)"
echo "  2. Run the notebook cells in order"
echo ""
echo "If Cosmos DB firewall update is running in background,"
echo "wait 2-5 minutes before running cell 22 (Message Storing)."
echo ""
