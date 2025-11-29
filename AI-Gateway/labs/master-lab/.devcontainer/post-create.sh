#!/bin/bash

# ============================================================================
# Master AI Gateway Lab - Post-Create Script
# ============================================================================
# Runs after the dev container is created
# Sets up Python environment, Azure CLI extensions, and workspace
# ============================================================================

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Master AI Gateway Lab - Environment Setup${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""

# ============================================================================
# Update System
# ============================================================================

echo -e "${BLUE}[1/7]${NC} Updating system packages..."
sudo apt-get update -qq > /dev/null 2>&1
echo -e "${GREEN}✓${NC} System packages updated"

# ============================================================================
# Install System Dependencies
# ============================================================================

echo -e "${BLUE}[2/7]${NC} Installing system dependencies..."
sudo apt-get install -y -qq \
    jq \
    curl \
    wget \
    unzip \
    zip \
    tree \
    htop \
    vim \
    uuid-runtime \
    > /dev/null 2>&1
echo -e "${GREEN}✓${NC} System dependencies installed"

# ============================================================================
# Python Setup
# ============================================================================

echo -e "${BLUE}[3/7]${NC} Setting up Python environment..."

# Upgrade pip
python -m pip install --upgrade pip --quiet

# Install requirements from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "  Installing packages from requirements.txt..."
    pip install -r requirements.txt --quiet
    echo -e "${GREEN}✓${NC} Python packages installed from requirements.txt"
else
    echo -e "${YELLOW}⚠${NC}  requirements.txt not found, skipping pip install"
fi

echo -e "${GREEN}✓${NC} Python environment configured"

# ============================================================================
# Node.js Setup
# ============================================================================

echo -e "${BLUE}[4/7]${NC} Setting up Node.js environment..."

# Install global npm packages for MCP development
npm install -g --silent \
    @modelcontextprotocol/inspector \
    prettier \
    > /dev/null 2>&1

echo -e "${GREEN}✓${NC} Node.js environment configured"

# ============================================================================
# Azure CLI Extensions
# ============================================================================

echo -e "${BLUE}[5/7]${NC} Installing Azure CLI extensions..."

# Install commonly used Azure CLI extensions
az extension add --name application-insights --yes --only-show-errors 2>/dev/null || true
az extension add --name front-door --yes --only-show-errors 2>/dev/null || true
az extension add --name api-center --yes --only-show-errors 2>/dev/null || true

echo -e "${GREEN}✓${NC} Azure CLI extensions installed"

# ============================================================================
# GitHub CLI Setup
# ============================================================================

echo -e "${BLUE}[6/7]${NC} Configuring GitHub CLI..."

# Configure gh to prefer HTTPS
gh config set git_protocol https 2>/dev/null || true

echo -e "${GREEN}✓${NC} GitHub CLI configured"

# ============================================================================
# Workspace Configuration
# ============================================================================

echo -e "${BLUE}[7/7]${NC} Configuring workspace..."

# Create workspace directories
mkdir -p ~/lab-workspace
mkdir -p ~/lab-workspace/policies
mkdir -p ~/lab-workspace/config
mkdir -p ~/lab-workspace/data

# Git configuration (if not already set)
if [ -z "$(git config --global user.name)" ]; then
    git config --global user.name "LP Roux"
fi
if [ -z "$(git config --global user.email)" ]; then
    git config --global user.email "lproux@users.noreply.github.com"
fi
git config --global init.defaultBranch main
git config --global core.editor "code --wait"

# Shell aliases for convenience
cat >> ~/.bashrc <<'EOF'

# ============================================================================
# Master AI Gateway Lab - Shell Aliases
# ============================================================================

# Navigation
alias ll='ls -lah'
alias lab='cd /workspaces/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab'
alias ws='cd ~/lab-workspace'

# Git shortcuts
alias gs='git status'
alias gd='git diff'
alias gl='git log --oneline --graph --decorate'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'

# Python environment
alias venv='source .venv/bin/activate'
alias mkvenv='python -m venv .venv && source .venv/bin/activate'
alias nb='jupyter notebook --ip=0.0.0.0 --no-browser'

# Azure shortcuts
alias azlogin='az login --use-device-code'
alias azaccount='az account show --output table'
alias azgroups='az group list --output table'
alias azregions='az account list-locations --query "[?metadata.regionType=='\''Physical'\''].name" -o table'
alias azapim='az apim list --output table'

# MCP development
alias mcprun='uvicorn server:app --reload --host 0.0.0.0 --port 8000'
alias mcpinspect='npx @modelcontextprotocol/inspector'
alias mcptest='pytest -v'

# Policy management
alias policies='cd ~/lab-workspace/policies'
alias policyls='ls -lh ~/lab-workspace/policies/'

# Quick testing
alias testapi='curl -X POST'
alias testjwt='python -c "import jwt; print(jwt.__version__)"'

# Lab shortcuts
alias notebook='code master-ai-gateway-easy-deploy.ipynb'
alias notebook-full='code master-ai-gateway-fix-MCP-clean-documented-final.ipynb'
alias readme='code README.md'
alias testing='code TESTING.md'
alias docs='code NOTEBOOK_DOCUMENTATION_README.md'

EOF

# Create lab workspace README
cat > ~/lab-workspace/README.md <<'EOF'
# Master AI Gateway Lab - Workspace

This workspace directory is for your lab exercises and experimentation.

## Directory Structure

```
~/lab-workspace/
├── policies/       # APIM policy XML files
├── config/         # Configuration files (.env, settings)
└── data/           # Data files (Excel, CSV, etc.)
```

## Quick Commands

### Navigation
- `lab` - Go to lab directory
- `ws` - Go to workspace directory
- `policies` - Go to policies directory

### Azure
- `azlogin` - Login to Azure (device code)
- `azaccount` - Show current Azure account
- `azgroups` - List resource groups
- `azapim` - List API Management instances

### Jupyter
- `nb` - Start Jupyter notebook server
- `notebook` - Open master notebook in VS Code

### Git
- `gs` - Git status
- `gd` - Git diff
- `gl` - Git log (pretty format)

### MCP Development
- `mcprun` - Run MCP HTTP server
- `mcpinspect` - Launch MCP Inspector
- `mcptest` - Run pytest

## Main Notebooks

**Easy Deploy (Recommended)**: `master-ai-gateway-easy-deploy.ipynb`
- Total cells: 34 (78% reduction from full version)
- One-command deployment with modular utilities
- Covers all 7 labs with minimal code

**Full Version**: `master-ai-gateway-fix-MCP-clean-documented-final.ipynb`
- Total cells: 152
- Detailed step-by-step deployment
- Comprehensive documentation and examples

## Documentation

- `NOTEBOOK_DOCUMENTATION_README.md` - Complete documentation guide
- `DOCUMENTATION_SUMMARY.md` - Documentation coverage report

## Getting Started

1. Open the main notebook (fully documented):
   ```bash
   lab
   notebook
   ```

2. Login to Azure:
   ```bash
   azlogin
   ```

3. Run the notebook cells sequentially

Happy learning! 🚀
EOF

echo -e "${GREEN}✓${NC} Workspace configured"

# ============================================================================
# Final Message
# ============================================================================

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Setup Complete!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Master AI Gateway Lab Environment Ready${NC}"
echo ""
echo "Quick Start:"
echo "  1. Navigate to lab: ${GREEN}lab${NC}"
echo "  2. Login to Azure: ${GREEN}azlogin${NC}"
echo "  3. Open easy deploy: ${GREEN}notebook${NC}"
echo ""
echo "Available Commands:"
echo "  • ${GREEN}lab${NC}           - Go to lab directory"
echo "  • ${GREEN}notebook${NC}      - Open master-ai-gateway-easy-deploy.ipynb (34 cells)"
echo "  • ${GREEN}notebook-full${NC} - Open full version (152 cells)"
echo "  • ${GREEN}testing${NC}       - Open TESTING.md guide"
echo "  • ${GREEN}azlogin${NC}       - Login to Azure"
echo "  • ${GREEN}mcprun${NC}        - Run MCP HTTP server"
echo "  • ${GREEN}nb${NC}            - Start Jupyter server"
echo ""
echo "Documentation:"
echo "  • TESTING.md - Comprehensive testing guide"
echo "  • README.md - Lab overview"
echo "  • ~/lab-workspace/README.md - Workspace commands"
echo ""
echo -e "Easy Deploy notebook: ${GREEN}34 cells${NC} (78% reduction)"
echo -e "Full notebook: ${GREEN}152 cells${NC}"
echo -e "7 labs consolidated: ${GREEN}✓${NC}"
echo ""
