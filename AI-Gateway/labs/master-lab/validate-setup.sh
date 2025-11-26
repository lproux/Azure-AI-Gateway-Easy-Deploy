#!/bin/bash

# ============================================================================
# Azure AI Gateway Easy Deploy - Setup Validation Script
# ============================================================================
# Validates that the environment is properly configured before running
# the master-ai-gateway-easy-deploy.ipynb notebook
# ============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0
WARNINGS=0

# ============================================================================
# Helper Functions
# ============================================================================

print_header() {
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
    echo ""
}

print_section() {
    echo ""
    echo -e "${BLUE}[CHECK]${NC} $1"
    echo "────────────────────────────────────────────────────────"
}

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

check_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# ============================================================================
# Validation Checks
# ============================================================================

print_header "Azure AI Gateway Easy Deploy - Setup Validation"

# ----------------------------------------------------------------------------
# 1. System Tools
# ----------------------------------------------------------------------------

print_section "System Tools & Dependencies"

# Check Python
if command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 11 ]; then
        check_pass "Python $PYTHON_VERSION (>= 3.11 required)"
    else
        check_fail "Python $PYTHON_VERSION (>= 3.11 required, found $PYTHON_VERSION)"
    fi
else
    check_fail "Python not found"
fi

# Check pip
if command -v pip &> /dev/null; then
    PIP_VERSION=$(pip --version 2>&1 | awk '{print $2}')
    check_pass "pip $PIP_VERSION"
else
    check_fail "pip not found"
fi

# Check Azure CLI
if command -v az &> /dev/null; then
    AZ_VERSION=$(az version -o json 2>&1 | jq -r '."azure-cli"')
    check_pass "Azure CLI $AZ_VERSION"
else
    check_fail "Azure CLI not found"
fi

# Check Bicep
if az bicep version &> /dev/null; then
    BICEP_VERSION=$(az bicep version 2>&1 | grep -oP 'Bicep CLI version \K[0-9.]+')
    check_pass "Bicep $BICEP_VERSION"
else
    check_fail "Bicep not found (run: az bicep install)"
fi

# Check jq
if command -v jq &> /dev/null; then
    JQ_VERSION=$(jq --version 2>&1 | cut -d- -f2)
    check_pass "jq $JQ_VERSION"
else
    check_warn "jq not found (optional but recommended)"
fi

# Check git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version 2>&1 | awk '{print $3}')
    check_pass "git $GIT_VERSION"
else
    check_warn "git not found (optional but recommended)"
fi

# ----------------------------------------------------------------------------
# 2. Python Packages
# ----------------------------------------------------------------------------

print_section "Required Python Packages"

# Key packages for the notebook
REQUIRED_PACKAGES=(
    "azure-identity"
    "azure-mgmt-resource"
    "azure-mgmt-apimanagement"
    "azure-mgmt-cognitiveservices"
    "azure-cosmos"
    "openai"
    "requests"
    "python-dotenv"
)

for package in "${REQUIRED_PACKAGES[@]}"; do
    if pip show "$package" &> /dev/null; then
        VERSION=$(pip show "$package" 2>&1 | grep "^Version:" | awk '{print $2}')
        check_pass "$package ($VERSION)"
    else
        check_fail "$package not installed"
    fi
done

# Optional but useful packages
OPTIONAL_PACKAGES=(
    "jupyter"
    "ipykernel"
    "pandas"
    "matplotlib"
)

echo ""
echo "Optional Packages:"
for package in "${OPTIONAL_PACKAGES[@]}"; do
    if pip show "$package" &> /dev/null; then
        VERSION=$(pip show "$package" 2>&1 | grep "^Version:" | awk '{print $2}')
        check_info "$package ($VERSION) - installed"
    else
        check_info "$package - not installed (optional)"
    fi
done

# ----------------------------------------------------------------------------
# 3. Azure Authentication
# ----------------------------------------------------------------------------

print_section "Azure Authentication & Access"

# Check if logged in
if az account show &> /dev/null; then
    ACCOUNT_NAME=$(az account show --query "user.name" -o tsv 2>&1)
    SUBSCRIPTION_NAME=$(az account show --query "name" -o tsv 2>&1)
    SUBSCRIPTION_ID=$(az account show --query "id" -o tsv 2>&1)

    check_pass "Authenticated as: $ACCOUNT_NAME"
    check_info "Subscription: $SUBSCRIPTION_NAME"
    check_info "Subscription ID: ${SUBSCRIPTION_ID:0:8}..."

    # Check subscription role
    ROLE_ASSIGNMENTS=$(az role assignment list --assignee $(az account show --query "user.name" -o tsv) --output json 2>&1)
    if echo "$ROLE_ASSIGNMENTS" | jq -e '.[] | select(.roleDefinitionName == "Owner")' &> /dev/null; then
        check_pass "Has Owner role"
    elif echo "$ROLE_ASSIGNMENTS" | jq -e '.[] | select(.roleDefinitionName == "Contributor")' &> /dev/null; then
        check_warn "Has Contributor role (may need RBAC Administrator for some operations)"
    else
        check_warn "Could not verify role assignments"
    fi
else
    check_fail "Not authenticated to Azure (run: az login)"
fi

# Check Azure OpenAI provider registration
if az provider show --namespace Microsoft.CognitiveServices --query "registrationState" -o tsv 2>&1 | grep -q "Registered"; then
    check_pass "Microsoft.CognitiveServices provider registered"
else
    check_fail "Microsoft.CognitiveServices provider not registered"
fi

# ----------------------------------------------------------------------------
# 4. Notebook Files
# ----------------------------------------------------------------------------

print_section "Notebook & Configuration Files"

# Check for main notebook
if [ -f "master-ai-gateway-easy-deploy.ipynb" ]; then
    check_pass "master-ai-gateway-easy-deploy.ipynb exists"
else
    check_fail "master-ai-gateway-easy-deploy.ipynb not found"
fi

# Check for requirements.txt
if [ -f "requirements.txt" ]; then
    check_pass "requirements.txt exists"
    PACKAGE_COUNT=$(grep -v "^#" requirements.txt | grep -v "^$" | wc -l)
    check_info "  Declares $PACKAGE_COUNT packages"
else
    check_warn "requirements.txt not found"
fi

# Check for util module
if [ -d "util" ]; then
    check_pass "util/ module directory exists"

    if [ -f "util/deploy_all.py" ]; then
        check_pass "util/deploy_all.py exists"
    else
        check_fail "util/deploy_all.py not found"
    fi
else
    check_fail "util/ module directory not found"
fi

# Check for quick_start module
if [ -d "quick_start" ]; then
    check_pass "quick_start/ module directory exists"

    if [ -f "quick_start/shared_init.py" ]; then
        check_pass "quick_start/shared_init.py exists"
    else
        check_fail "quick_start/shared_init.py not found"
    fi
else
    check_fail "quick_start/ module directory not found"
fi

# Check for documentation
if [ -f "README.md" ]; then
    check_pass "README.md exists"
else
    check_warn "README.md not found"
fi

if [ -f "TESTING.md" ]; then
    check_pass "TESTING.md exists"
else
    check_warn "TESTING.md not found"
fi

# ----------------------------------------------------------------------------
# 5. Azure Quotas (Basic Check)
# ----------------------------------------------------------------------------

print_section "Azure Quotas & Limits"

if az account show &> /dev/null; then
    # Check API Management quota (requires specific location)
    DEFAULT_LOCATION="uksouth"

    check_info "Checking quotas in region: $DEFAULT_LOCATION"

    # Note: Quota checks require specific providers and are region-specific
    # This is a basic check - actual quotas should be verified in Azure Portal

    check_info "API Management StandardV2: Verify in Azure Portal"
    check_info "Azure OpenAI PTU quota: Verify in Azure Portal"
    check_info "Container Apps cores: Verify in Azure Portal"

    echo ""
    check_info "💡 To check quotas:"
    check_info "   Portal: https://portal.azure.com/#blade/Microsoft_Azure_Capacity/QuotaMenuBlade"
    check_info "   CLI: az vm list-usage --location $DEFAULT_LOCATION -o table"
else
    check_warn "Not authenticated - cannot check quotas"
fi

# ----------------------------------------------------------------------------
# 6. Jupyter Kernel
# ----------------------------------------------------------------------------

print_section "Jupyter Notebook Environment"

# Check if jupyter is installed
if command -v jupyter &> /dev/null; then
    JUPYTER_VERSION=$(jupyter --version 2>&1 | head -1 | awk '{print $3}')
    check_pass "Jupyter installed"

    # Check for Python kernel
    if jupyter kernelspec list 2>&1 | grep -q "python3"; then
        check_pass "Python 3 kernel available"
    else
        check_warn "Python 3 kernel not found (run: python -m ipykernel install --user)"
    fi
else
    check_warn "Jupyter not found (optional, but needed for running notebooks)"
fi

# Check ipykernel
if pip show ipykernel &> /dev/null; then
    VERSION=$(pip show ipykernel 2>&1 | grep "^Version:" | awk '{print $2}')
    check_pass "ipykernel ($VERSION)"
else
    check_warn "ipykernel not installed"
fi

# ----------------------------------------------------------------------------
# 7. Network Connectivity
# ----------------------------------------------------------------------------

print_section "Network Connectivity"

# Check Azure connectivity
if curl -s --connect-timeout 5 https://management.azure.com &> /dev/null; then
    check_pass "Can reach Azure management endpoint"
else
    check_fail "Cannot reach Azure management endpoint"
fi

# Check GitHub connectivity
if curl -s --connect-timeout 5 https://api.github.com &> /dev/null; then
    check_pass "Can reach GitHub API"
else
    check_warn "Cannot reach GitHub API (may affect some operations)"
fi

# Check PyPI connectivity
if curl -s --connect-timeout 5 https://pypi.org &> /dev/null; then
    check_pass "Can reach PyPI (pip package index)"
else
    check_warn "Cannot reach PyPI (may affect package installation)"
fi

# ----------------------------------------------------------------------------
# 8. Disk Space
# ----------------------------------------------------------------------------

print_section "System Resources"

# Check available disk space
AVAILABLE_GB=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
if [ "$AVAILABLE_GB" -ge 10 ]; then
    check_pass "Available disk space: ${AVAILABLE_GB}GB (>= 10GB recommended)"
else
    check_warn "Available disk space: ${AVAILABLE_GB}GB (< 10GB, may run out during deployment)"
fi

# Check memory (if free command exists)
if command -v free &> /dev/null; then
    TOTAL_MEM_GB=$(free -g | awk 'NR==2 {print $2}')
    if [ "$TOTAL_MEM_GB" -ge 8 ]; then
        check_pass "Total memory: ${TOTAL_MEM_GB}GB (>= 8GB recommended)"
    else
        check_warn "Total memory: ${TOTAL_MEM_GB}GB (< 8GB, may affect performance)"
    fi
else
    check_info "Memory check skipped (free command not available)"
fi

# ============================================================================
# Summary
# ============================================================================

print_header "Validation Summary"

echo -e "${GREEN}Passed:${NC}   $PASSED checks"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS checks"
echo -e "${RED}Failed:${NC}   $FAILED checks"
echo ""

if [ $FAILED -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}✓ All checks passed!${NC}"
        echo ""
        echo "Your environment is ready to run the notebook."
        echo ""
        echo "Next steps:"
        echo "  1. Open: master-ai-gateway-easy-deploy.ipynb"
        echo "  2. Select kernel: Python 3.11+"
        echo "  3. Run cells sequentially"
        echo ""
        echo "Documentation:"
        echo "  • TESTING.md - Complete testing guide"
        echo "  • README.md - Lab overview"
        echo ""
        exit 0
    else
        echo -e "${YELLOW}⚠ All critical checks passed, but there are warnings.${NC}"
        echo ""
        echo "You can proceed, but some features may not work as expected."
        echo "Review warnings above and install missing optional components if needed."
        echo ""
        echo "To fix warnings:"
        echo "  • Install optional packages: pip install jupyter ipykernel pandas"
        echo "  • Install system tools: sudo apt-get install jq git"
        echo ""
        exit 0
    fi
else
    echo -e "${RED}✗ Some critical checks failed.${NC}"
    echo ""
    echo "Please fix the failed checks before running the notebook."
    echo ""
    echo "Common fixes:"
    echo "  • Install Python 3.11+: https://www.python.org/downloads/"
    echo "  • Install Azure CLI: https://learn.microsoft.com/cli/azure/install-azure-cli"
    echo "  • Login to Azure: az login"
    echo "  • Install Python packages: pip install -r requirements.txt"
    echo "  • Install Bicep: az bicep install"
    echo ""
    echo "For detailed help, see TESTING.md"
    echo ""
    exit 1
fi
