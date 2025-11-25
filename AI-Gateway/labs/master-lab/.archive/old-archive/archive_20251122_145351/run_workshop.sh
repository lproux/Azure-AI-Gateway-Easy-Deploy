#!/bin/bash
echo "🚀 AI Gateway Workshop - One-Click Deploy"

if [ -n "$CODESPACE_NAME" ]; then
    echo "📍 Running in GitHub Codespace"
else
    echo "📍 Running in local environment"
fi

if [ ! -f bootstrap.env ]; then
    cp bootstrap.env.template bootstrap.env
    echo "⚠️  Created bootstrap.env - please fill in required values"
    exit 1
fi

echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

echo "🔧 Running deployment notebook..."
jupyter nbconvert --to notebook --execute master-ai-gateway-fix-MCP-clean.ipynb \
    --output output/deployed.ipynb \
    --ExecutePreprocessor.timeout=1800

echo "✅ Deployment complete!"
