#!/bin/bash
# Fix MCP Server Port Mismatch
# Issue: Container Apps configured for port 8080, but containers listen on port 80

echo "=========================================="
echo "MCP SERVER PORT FIX"
echo "=========================================="
echo ""

RESOURCE_GROUP="lab-master-lab"
SERVERS=("weather" "oncall" "github" "spotify" "product-catalog" "place-order" "ms-learn")

echo "📋 Fixing port configuration for ${#SERVERS[@]} MCP servers..."
echo ""

for server in "${SERVERS[@]}"; do
  APP_NAME="mcp-${server}-pavavy6pu5"

  echo "🔧 Fixing: ${APP_NAME}"

  # Update ingress to use port 80 (the actual listening port)
  az containerapp ingress update \
    --name "${APP_NAME}" \
    --resource-group "${RESOURCE_GROUP}" \
    --target-port 80 \
    --output none

  if [ $? -eq 0 ]; then
    echo "  ✅ Port updated to 80"
  else
    echo "  ❌ Failed to update port"
  fi

  echo "---"
done

echo ""
echo "=========================================="
echo "✅ PORT FIX COMPLETE"
echo "=========================================="
echo ""
echo "⏳ Wait 30-60 seconds for replicas to start..."
echo ""
echo "Then test connectivity:"
echo "  python3 test_mcp_servers.py"
