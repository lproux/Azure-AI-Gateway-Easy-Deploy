#!/bin/bash
# Deploy Real Containerized MCP Servers (OnCall & Spotify)

set -e

DEPLOYMENT_ID=72998
ACR_NAME="acrmcp${DEPLOYMENT_ID}"
ACR_SERVER="${ACR_NAME}.azurecr.io"
RESOURCE_GROUP="lab-master-lab"
LOCATION="eastus"

BASE_PATH="/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs"

echo "========================================================================"
echo "🚀 Deploying Real Containerized MCP Servers"
echo "========================================================================"
echo ""
echo "Servers: oncall, spotify"
echo ""

deploy_server() {
    local name=$1
    local source_path=$2
    local port=${3:-8080}

    echo ""
    echo "========================================================================"
    echo "📦 Deploying ${name} MCP"
    echo "========================================================================"
    
    if [ ! -f "${source_path}/Dockerfile" ]; then
        echo "❌ Dockerfile not found"
        return 1
    fi

    echo "Step 1/4: Building image..."
    (cd "${source_path}" && az acr build \
        --registry "${ACR_NAME}" \
        --image "${name}-mcp:latest" \
        --file ./Dockerfile \
        .) || return 1
    echo "✅ Built"

    echo "Step 2/4: Deploying..."
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
        --memory 1.5 || return 1
    echo "✅ Deployed"

    echo "Step 3/4: Waiting 15s..."
    sleep 15

    echo "Step 4/4: Testing..."
    SERVER_URL="http://${name}-mcp-${DEPLOYMENT_ID}.${LOCATION}.azurecontainer.io:${port}"
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${SERVER_URL}/" --max-time 10 || echo "000")

    echo "   URL: ${SERVER_URL}"
    echo "   HTTP: ${HTTP_CODE}"
    
    echo "${name^^}_MCP_URL=${SERVER_URL}" >> "${BASE_PATH}/master-lab/master-lab.env"
    echo "${name^^}_MCP_URL=${SERVER_URL}" >> "${BASE_PATH}/master-lab/.mcp-servers-config"
    echo "✅ Config updated"
}

cd "${BASE_PATH}/master-lab"

deploy_server "oncall" "${BASE_PATH}/mcp-a2a-agents/src/oncall/mcp-server" 8080
deploy_server "spotify" "${BASE_PATH}/realtime-mcp-agents/src/spotify/mcp-server" 8080

echo ""
echo "✅ Complete!"
