#!/bin/bash

# ============================================================================
# Master AI Gateway Lab - Deployment Script (Bash Wrapper)
# ============================================================================
# Simple wrapper around az_up.py for easier invocation
# ============================================================================

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Master AI Gateway Lab - Automated Deployment${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python is not installed or not in PATH"
    echo "  Please install Python 3.11 or later"
    exit 1
fi

# Determine Python command
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# Check if Azure SDK is installed
if ! $PYTHON_CMD -c "import azure.identity" 2>/dev/null; then
    echo -e "${YELLOW}[WARN]${NC} Azure SDK not detected"
    echo "  Installing required packages..."
    echo ""
    $PYTHON_CMD -m pip install azure-identity azure-mgmt-resource --quiet
    echo -e "${GREEN}[OK]${NC} Azure SDK installed"
    echo ""
fi

# Check if Azure CLI is authenticated
if ! az account show &> /dev/null; then
    echo -e "${YELLOW}[WARN]${NC} Not authenticated with Azure CLI"
    echo "  Running: az login"
    echo ""
    az login
    echo ""
fi

# Show current subscription
CURRENT_SUB=$(az account show --query "name" -o tsv 2>/dev/null || echo "Unknown")
CURRENT_SUB_ID=$(az account show --query "id" -o tsv 2>/dev/null || echo "Unknown")

echo -e "${BLUE}[*]${NC} Current Azure Subscription:"
echo "    Name: ${CURRENT_SUB}"
echo "    ID: ${CURRENT_SUB_ID}"
echo ""

# Confirm before proceeding
read -p "Deploy to this subscription? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled"
    exit 0
fi

# Run Python deployment script
echo ""
echo -e "${GREEN}[*]${NC} Starting deployment..."
echo ""

$PYTHON_CMD az_up.py "$@"

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  Deployment Successful!${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Source the environment file: source master-lab.env"
    echo "  2. Open the notebook: jupyter notebook master-ai-gateway.ipynb"
    echo "  3. Run cells sequentially"
    echo ""
else
    echo ""
    echo -e "${RED}════════════════════════════════════════════════════════${NC}"
    echo -e "${RED}  Deployment Failed${NC}"
    echo -e "${RED}════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "Check the error messages above for details"
    echo "You can re-run this script to resume from failed steps"
    echo ""
    exit 1
fi
