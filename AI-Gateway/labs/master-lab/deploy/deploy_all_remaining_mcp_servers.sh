#!/bin/bash
# Sequential Deployment of All 6 Remaining MCP Servers
# Following user's systematic approach: deploy → test → consolidate

set -e  # Exit on error

DEPLOYMENT_ID=72998
ACR_NAME="acrmcp${DEPLOYMENT_ID}"
ACR_SERVER="${ACR_NAME}.azurecr.io"
RESOURCE_GROUP="lab-master-lab"
LOCATION="eastus"

BASE_PATH="/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs"

echo "========================================================================"
echo "🚀 Sequential MCP Server Deployment - 6 Remaining Servers"
echo "========================================================================"
echo ""
echo "Following systematic approach:"
echo "  1. Deploy each server separately"
echo "  2. Test each individually"
echo "  3. Update configuration after each success"
echo "  4. Create consolidated deployment cell at the end"
echo ""
echo "Servers to deploy:"
echo "  1. oncall      (priority: 5 labs)"
echo "  2. spotify     (priority: 2 labs)"
echo "  3. github      (priority: 4 labs)"
echo "  4. product-catalog"
echo "  5. place-order"
echo "  6. ms-learn"
echo ""
read -p "Press Enter to start sequential deployment..."

# Function to deploy a server
deploy_server() {
    local name=$1
    local source_path=$2
    local port=${3:-8080}  # Default port 8080

    echo ""
    echo "========================================================================"
    echo "📦 Server $SERVER_COUNT/6: Deploying ${name} MCP"
    echo "========================================================================"
    echo "Source: ${source_path}"
    echo "Port: ${port}"
    echo ""

    # Check if source exists
    if [ ! -d "${source_path}" ]; then
        echo "❌ Error: Source path not found: ${source_path}"
        return 1
    fi

    # Check for required files
    if [ ! -f "${source_path}/Dockerfile" ]; then
        echo "❌ Error: Dockerfile not found in ${source_path}"
        return 1
    fi

    echo "Step 1/4: Building Docker image..."
    az acr build \
        --registry "${ACR_NAME}" \
        --image "${name}-mcp:latest" \
        --file Dockerfile \
        "${source_path}" || {
        echo "❌ Build failed for ${name}"
        return 1
    }
    echo "✅ Image built successfully"

    echo ""
    echo "Step 2/4: Deploying to Azure Container Instances..."
    az container create \
        --resource-group "${RESOURCE_GROUP}" \
        --name "${name}-mcp-${DEPLOYMENT_ID}" \
        --image "${ACR_SERVER}/${name}-mcp:latest" \
        --registry-login-server "${ACR_SERVER}" \
        --registry-username "${ACR_NAME}" \
        --registry-password "$(az acr credential show --name ${ACR_NAME} --query 'passwords[0].value' -o tsv)" \
        --dns-name-label "${name}-mcp-${DEPLOYMENT_ID}" \
        --ports ${port} \
        --os-type Linux \
        --location "${LOCATION}" \
        --cpu 1 \
        --memory 1.5 || {
        echo "❌ Deployment failed for ${name}"
        return 1
    }
    echo "✅ Deployed successfully"

    echo ""
    echo "Step 3/4: Waiting for container to start (15 seconds)..."
    sleep 15

    echo ""
    echo "Step 4/4: Testing server health..."
    SERVER_URL="http://${name}-mcp-${DEPLOYMENT_ID}.${LOCATION}.azurecontainer.io:${port}"

    # Test root endpoint
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${SERVER_URL}/" --max-time 10 || echo "000")

    if [ "${HTTP_CODE}" != "000" ]; then
        echo "✅ Server responding! HTTP ${HTTP_CODE}"
        echo "   URL: ${SERVER_URL}"

        # Add to config
        echo ""
        echo "Updating configuration..."
        echo "${name^^}_MCP_URL=${SERVER_URL}" >> master-lab.env
        echo "${name^^}_MCP_URL=${SERVER_URL}" >> .mcp-servers-config
        echo "✅ Configuration updated"

        # Log success
        echo "${name},${SERVER_URL},${port},deployed" >> deployment_log.csv

        return 0
    else
        echo "⚠️  Server not responding on root endpoint"
        echo "   (This may be normal for SSE-only servers)"
        echo "   URL: ${SERVER_URL}"

        # Still add to config (server may be running but no root endpoint)
        echo "${name^^}_MCP_URL=${SERVER_URL}" >> master-lab.env
        echo "${name^^}_MCP_URL=${SERVER_URL}" >> .mcp-servers-config
        echo "✅ Added to configuration (needs manual verification)"

        # Log as needs-verification
        echo "${name},${SERVER_URL},${port},needs-verification" >> deployment_log.csv

        return 0
    fi
}

# Initialize deployment log
cd "${BASE_PATH}/master-lab"
echo "server,url,port,status" > deployment_log.csv

# Deploy each server sequentially
SERVER_COUNT=1

# 1. OnCall MCP (Priority: 5 labs)
deploy_server "oncall" "${BASE_PATH}/mcp-a2a-agents/src/oncall/mcp-server" 8080
SERVER_COUNT=$((SERVER_COUNT + 1))

# 2. Spotify MCP (Priority: 2 labs)
deploy_server "spotify" "${BASE_PATH}/realtime-mcp-agents/src/spotify/mcp-server" 8080
SERVER_COUNT=$((SERVER_COUNT + 1))

# 3. GitHub MCP (Priority: 4 labs)
deploy_server "github" "${BASE_PATH}/model-context-protocol/src/github/mcp-server" 8080
SERVER_COUNT=$((SERVER_COUNT + 1))

# 4. Product Catalog MCP
deploy_server "product-catalog" "${BASE_PATH}/mcp-from-api/src/product-catalog/mcp-server" 8080
SERVER_COUNT=$((SERVER_COUNT + 1))

# 5. Place Order MCP
deploy_server "place-order" "${BASE_PATH}/mcp-from-api/src/place-order/mcp-server" 8080
SERVER_COUNT=$((SERVER_COUNT + 1))

# 6. MS Learn MCP
deploy_server "ms-learn" "${BASE_PATH}/mcp-from-api/src/ms-learn/mcp-server" 8080

echo ""
echo "========================================================================"
echo "✅ Sequential Deployment Complete!"
echo "========================================================================"
echo ""
echo "Deployment Summary:"
cat deployment_log.csv | column -t -s ','
echo ""
echo "📝 Next Steps:"
echo "  1. Review deployment log above"
echo "  2. Test each server individually (test_all_mcp_servers.py)"
echo "  3. Update notebook_mcp_helpers.py with new MCP classes"
echo "  4. Create consolidated initialization cell"
echo "  5. Run full notebook test"
echo ""
echo "Configuration files updated:"
echo "  ✅ master-lab.env"
echo "  ✅ .mcp-servers-config"
echo ""
