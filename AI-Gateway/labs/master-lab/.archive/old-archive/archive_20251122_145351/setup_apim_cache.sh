#!/bin/bash
# Connect Redis to APIM as a cache resource for semantic caching

# Load environment variables
source <(grep -v '^#' master-lab.env | sed 's/^/export /')

echo "============================================================"
echo "🔧 Connecting Redis to APIM for Semantic Caching"
echo "============================================================"

echo ""
echo "📋 Configuration:"
echo "   APIM: $APIM_SERVICE_NAME"
echo "   Redis: $REDIS_HOST:$REDIS_PORT"
echo "   Resource Group: $RESOURCE_GROUP"
echo "   Subscription: $SUBSCRIPTION_ID"

# Create cache using Azure REST API
CACHE_URL="https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.ApiManagement/service/$APIM_SERVICE_NAME/caches/default?api-version=2024-06-01-preview"

CACHE_PAYLOAD=$(cat <<EOF
{
  "properties": {
    "connectionString": "$REDIS_HOST:$REDIS_PORT,password=$REDIS_KEY,ssl=True,abortConnect=False",
    "useFromLocation": "default",
    "description": "Redis cache for semantic caching"
  }
}
EOF
)

echo ""
echo "[*] Connecting Redis to APIM..."

# Write payload to temp file
echo "$CACHE_PAYLOAD" > /tmp/cache-payload.json

# Create cache
az rest \
    --method PUT \
    --url "$CACHE_URL" \
    --body @/tmp/cache-payload.json

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Redis cache connected to APIM successfully!"
    echo ""
    echo "Next steps:"
    echo "  1. Reopen your notebook"
    echo "  2. Run Cell 51 (Configure Embeddings Backend)"
    echo "  3. Run Cell 52 (Apply Semantic Caching Policy)"
    echo "  4. Run Cell 53 (Test Semantic Caching)"
    echo ""
    echo "Expected results:"
    echo "  - First request: 1-2 seconds (backend call)"
    echo "  - Similar requests: 0.1-0.3 seconds (cache hits)"
else
    echo ""
    echo "❌ Failed to connect Redis cache"
    echo ""
    echo "💡 Manual workaround:"
    echo "  1. Go to Azure Portal"
    echo "  2. Navigate to: API Management → Caches"
    echo "  3. Click '+ Add'"
    echo "  4. Enter:"
    echo "     Name: default"
    echo "     Connection string: $REDIS_HOST:$REDIS_PORT,password=***,ssl=True,abortConnect=False"
fi

rm -f /tmp/cache-payload.json

echo ""
echo "============================================================"
