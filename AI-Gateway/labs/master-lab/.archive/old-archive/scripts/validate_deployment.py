#!/usr/bin/env python3
"""
Validation script for master-deployment.bicep
This script validates the Bicep file without actually deploying anything
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_ok(text):
    """Print success message"""
    print(f"[OK] {text}")

def print_error(text):
    """Print error message"""
    print(f"[ERROR] {text}")

def print_info(text):
    """Print info message"""
    print(f"[*] {text}")

def run_command(cmd, description):
    """Run a command and return success status"""
    print_info(f"{description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print_ok(f"{description} - Success")
            return True, result.stdout
        else:
            print_error(f"{description} - Failed")
            if result.stderr:
                print(f"    Error: {result.stderr[:200]}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        print_error(f"{description} - Timeout")
        return False, "Timeout"
    except Exception as e:
        print_error(f"{description} - Exception: {str(e)}")
        return False, str(e)

def main():
    print_header("Master Deployment Bicep Validation")

    # Change to master-lab directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    print_info(f"Working directory: {os.getcwd()}")

    all_checks_passed = True

    # ========================================
    # Check 1: File existence
    # ========================================
    print_header("Check 1: Required Files")

    required_files = [
        'master-deployment.bicep',
        'params.template.json',
        'policies/backend-pool-load-balancing-policy.xml',
        '../../modules/operational-insights/v1/workspaces.bicep',
        '../../modules/monitor/v1/appinsights.bicep',
        '../../modules/apim/v2/apim.bicep',
        '../../modules/cognitive-services/v3/foundry.bicep',
        '../../modules/apim/v2/inference-api.bicep'
    ]

    for file in required_files:
        if os.path.exists(file):
            print_ok(f"Found: {file}")
        else:
            print_error(f"Missing: {file}")
            all_checks_passed = False

    # ========================================
    # Check 2: Bicep syntax validation
    # ========================================
    print_header("Check 2: Bicep Syntax Validation")

    success, output = run_command(
        'az bicep build --file master-deployment.bicep',
        'Compiling Bicep to JSON'
    )

    if success:
        if os.path.exists('master-deployment.json'):
            file_size = os.path.getsize('master-deployment.json')
            print_ok(f"Compiled JSON size: {file_size / 1024:.1f} KB")
        else:
            print_error("Compiled JSON not found")
            all_checks_passed = False
    else:
        all_checks_passed = False

    # ========================================
    # Check 3: Parameters validation
    # ========================================
    print_header("Check 3: Parameters File Validation")

    try:
        with open('params.template.json', 'r') as f:
            params = json.load(f)

        print_ok("Parameters file is valid JSON")

        # Check required parameters
        required_params = [
            'location',
            'apimSku',
            'redisCacheSku',
            'searchSku',
            'apimSubscriptionsConfig',
            'foundryProjectName',
            'inferenceAPIPath',
            'inferenceAPIType'
        ]

        params_values = params.get('parameters', {})
        for param in required_params:
            if param in params_values:
                value = params_values[param].get('value', 'N/A')
                print_ok(f"Parameter '{param}': {value}")
            else:
                print_error(f"Missing parameter: {param}")
                all_checks_passed = False

    except json.JSONDecodeError as e:
        print_error(f"Invalid JSON in params.template.json: {e}")
        all_checks_passed = False
    except Exception as e:
        print_error(f"Error reading params.template.json: {e}")
        all_checks_passed = False

    # ========================================
    # Check 4: Resource summary
    # ========================================
    print_header("Check 4: Deployment Resource Summary")

    print_info("This deployment will create:")
    print("  Core Infrastructure:")
    print("    - 1x Log Analytics Workspace")
    print("    - 1x Application Insights")
    print("    - 1x API Management (StandardV2)")
    print("")
    print("  AI Services (3 Regions):")
    print("    - 1x AI Foundry Hub + Project (UK South - Priority 1)")
    print("      * 12 AI models (gpt-4o-mini, gpt-4.1-mini, gpt-4.1, gpt-4o, etc.)")
    print("    - 1x AI Foundry Hub + Project (Sweden Central - Priority 2)")
    print("      * 1 model (gpt-4o-mini)")
    print("    - 1x AI Foundry Hub + Project (West Europe - Priority 2)")
    print("      * 1 model (gpt-4o-mini)")
    print("")
    print("  Supporting Services:")
    print("    - 1x Redis Enterprise (semantic caching)")
    print("    - 1x Azure AI Content Safety")
    print("    - 1x Azure Cognitive Search")
    print("    - 1x Cosmos DB")
    print("    - 1x Container Registry")
    print("    - 1x Container Apps Environment")
    print("    - 7x MCP Server Container Apps")
    print("      * weather, oncall, github, spotify, product-catalog,")
    print("        place-order, ms-learn")
    print("")
    print("  TOTAL: ~35 resources")

    # ========================================
    # Check 5: Estimated deployment time
    # ========================================
    print_header("Check 5: Deployment Estimates")

    print_info("Estimated deployment time: 30-45 minutes")
    print_info("Estimated monthly cost (running 24/7):")
    print("  - API Management StandardV2: ~$300/month")
    print("  - Redis Enterprise: ~$150/month")
    print("  - Cognitive Search (Basic): ~$75/month")
    print("  - AI Foundry (3 hubs): ~$0 (pay-per-use)")
    print("  - Cosmos DB: ~$25/month")
    print("  - Container Apps: ~$50/month")
    print("  - Other services: ~$50/month")
    print("  TOTAL: ~$650-750/month (can be reduced by stopping when not in use)")

    # ========================================
    # Check 6: Azure CLI authentication
    # ========================================
    print_header("Check 6: Azure CLI Authentication")

    success, output = run_command(
        'az account show --query "{user:user.name, subscription:name}" -o json',
        'Checking Azure authentication'
    )

    if success:
        try:
            account_info = json.loads(output)
            print_ok(f"Logged in as: {account_info.get('user', 'N/A')}")
            print_ok(f"Subscription: {account_info.get('subscription', 'N/A')}")
        except:
            print_info("Authenticated (could not parse account details)")
    else:
        print_error("Not authenticated to Azure")
        print_info("Run: az login")
        all_checks_passed = False

    # ========================================
    # Check 7: Recommended next steps
    # ========================================
    print_header("Check 7: Deployment Readiness")

    if all_checks_passed:
        print_ok("All validation checks passed!")
        print("")
        print_header("Ready to Deploy!")
        print("")
        print("You can now deploy using the notebook cells:")
        print("")
        print("  1. Run Cell 11: Set configuration")
        print("  2. Run Cell 13: Check deployment status")
        print("  3. Run Cell 15: Create resource group")
        print("  4. Run Cell 17: Deploy Bicep (30-45 min)")
        print("  5. Run Cell 19: Retrieve outputs")
        print("  6. Run Cell 21: Export to .env")
        print("")
        print("OR deploy manually:")
        print("")
        print("  # Create resource group")
        print("  az group create --name lab-master-lab --location uksouth")
        print("")
        print("  # Deploy")
        print("  az deployment group create \\")
        print("    --name master-lab-deployment \\")
        print("    --resource-group lab-master-lab \\")
        print("    --template-file master-deployment.bicep \\")
        print("    --parameters @params.template.json")
        print("")
        print("  # Monitor in Azure Portal")
        print("  https://portal.azure.com/#view/HubsExtension/DeploymentDetailsBlade")
        print("")
        return 0
    else:
        print_error("Some validation checks failed!")
        print_info("Fix the issues above before deploying")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
