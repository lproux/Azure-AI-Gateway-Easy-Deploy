#!/bin/bash
# Start Jupyter Notebook without authentication

cd "$(dirname "$0")"

echo "🚀 Starting Jupyter Notebook (no authentication)..."
echo "📁 Working directory: $(pwd)"
echo ""

# Start Jupyter with explicit settings
python3 -m jupyter notebook \
    --ServerApp.token='' \
    --ServerApp.password='' \
    --ServerApp.disable_check_xsrf=True \
    --ServerApp.allow_origin='*' \
    --no-browser \
    --ip=127.0.0.1 \
    --port=8888

