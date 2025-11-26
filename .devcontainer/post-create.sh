#!/bin/bash

# ============================================================================
# Azure AI Gateway Repository - Post-Create Script
# ============================================================================
# Runs after the dev container is created at the repository root
# Sets up environment for exploring all labs and implementations
# ============================================================================

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Azure AI Gateway Repository - Environment Setup${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""

# ============================================================================
# Update System
# ============================================================================

echo -e "${BLUE}[1/6]${NC} Updating system packages..."
sudo apt-get update -qq > /dev/null 2>&1
echo -e "${GREEN}✓${NC} System packages updated"

# ============================================================================
# Install System Dependencies
# ============================================================================

echo -e "${BLUE}[2/6]${NC} Installing system dependencies..."
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
# Python Setup (Master Lab Requirements)
# ============================================================================

echo -e "${BLUE}[3/6]${NC} Setting up Python environment..."

# Upgrade pip
python -m pip install --upgrade pip --quiet

# Install requirements from master-lab (primary notebook)
if [ -f "AI-Gateway/labs/master-lab/requirements.txt" ]; then
    echo "  Installing packages from master-lab/requirements.txt..."
    pip install -r AI-Gateway/labs/master-lab/requirements.txt --quiet
    echo -e "${GREEN}✓${NC} Python packages installed"
else
    echo -e "${YELLOW}⚠${NC}  master-lab requirements.txt not found"
fi

echo -e "${GREEN}✓${NC} Python environment configured"

# ============================================================================
# Node.js Setup
# ============================================================================

echo -e "${BLUE}[4/6]${NC} Setting up Node.js environment..."

# Install global npm packages for MCP development
npm install -g --silent \
    @modelcontextprotocol/inspector \
    prettier \
    > /dev/null 2>&1

echo -e "${GREEN}✓${NC} Node.js environment configured"

# ============================================================================
# Azure CLI Extensions
# ============================================================================

echo -e "${BLUE}[5/6]${NC} Installing Azure CLI extensions..."

# Install commonly used Azure CLI extensions
az extension add --name application-insights --yes --only-show-errors 2>/dev/null || true
az extension add --name front-door --yes --only-show-errors 2>/dev/null || true
az extension add --name api-center --yes --only-show-errors 2>/dev/null || true

echo -e "${GREEN}✓${NC} Azure CLI extensions installed"

# ============================================================================
# Workspace Configuration
# ============================================================================

echo -e "${BLUE}[6/6]${NC} Configuring workspace..."

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
# Azure AI Gateway Repository - Shell Aliases
# ============================================================================

# Navigation
alias ll='ls -lah'
alias masterlab='cd /workspaces/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab'
alias labs='cd /workspaces/MCP-servers-internalMSFT-and-external/AI-Gateway/labs'
alias apim='cd /workspaces/MCP-servers-internalMSFT-and-external/AzureOpenAI-with-APIM'

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

# Quick navigation to key files
alias readme='code README.md'
alias testing='code AI-Gateway/labs/master-lab/TESTING.md'
alias notebook='code AI-Gateway/labs/master-lab/master-ai-gateway-easy-deploy.ipynb'
alias notebookfull='code AI-Gateway/labs/master-lab/master-ai-gateway-fix-MCP-clean-documented-final.ipynb'

# Validation
alias validate='bash AI-Gateway/labs/master-lab/validate-setup.sh'

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
echo -e "${YELLOW}Azure AI Gateway Repository Environment Ready${NC}"
echo ""
echo "Quick Start Paths:"
echo ""
echo "1. ${GREEN}Easy Deploy (Recommended)${NC}"
echo "   cd AI-Gateway/labs/master-lab"
echo "   Open: master-ai-gateway-easy-deploy.ipynb"
echo "   - 34 cells, ~1 hour setup"
echo ""
echo "2. ${GREEN}Full Master Lab${NC}"
echo "   cd AI-Gateway/labs/master-lab"
echo "   Open: master-ai-gateway-fix-MCP-clean-documented-final.ipynb"
echo "   - 152 cells, comprehensive experience"
echo ""
echo "3. ${GREEN}Individual Labs${NC}"
echo "   cd AI-Gateway/labs/<lab-name>"
echo "   - Modular, focused learning"
echo ""
echo "4. ${GREEN}APIM Integration${NC}"
echo "   cd AzureOpenAI-with-APIM"
echo "   - Production-ready patterns"
echo ""
echo "Available Commands:"
echo "  • ${GREEN}masterlab${NC}    - Go to Master Lab directory"
echo "  • ${GREEN}labs${NC}         - Browse all labs"
echo "  • ${GREEN}notebook${NC}     - Open easy deploy notebook (34 cells)"
echo "  • ${GREEN}notebookfull${NC} - Open full notebook (152 cells)"
echo "  • ${GREEN}testing${NC}      - Open testing guide"
echo "  • ${GREEN}validate${NC}     - Run setup validation"
echo "  • ${GREEN}azlogin${NC}      - Login to Azure"
echo ""
echo "Documentation:"
echo "  • README.md - Repository overview"
echo "  • AI-Gateway/labs/master-lab/TESTING.md - Complete testing guide"
echo "  • AI-Gateway/labs/master-lab/README.md - Master Lab documentation"
echo ""
echo "Before starting:"
echo "  1. Run: ${GREEN}azlogin${NC}"
echo "  2. Run: ${GREEN}validate${NC} (optional but recommended)"
echo "  3. Choose your path above"
echo ""
