#!/usr/bin/env python3
"""
Master AI Gateway Lab - Automated Deployment (az up style)

This script automates the complete deployment of all Azure resources needed for the
Master AI Gateway Lab. It mimics the behavior of 'az up' by deploying infrastructure,
configuring services, and generating environment files in one command.

Usage:
    python az_up.py [--subscription-id ID] [--location LOCATION] [--resource-group NAME]

Example:
    python az_up.py --subscription-id "your-sub-id" --location "uksouth"

Features:
    - 4-step deployment process
    - Resilient (checks existing resources, skips if already deployed)
    - Progress tracking with color output
    - Automatic environment file generation
    - Comprehensive error handling
    - Can resume from failed steps
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Tuple

try:
    from azure.identity import AzureCliCredential, ClientSecretCredential
    from azure.mgmt.resource import ResourceManagementClient
    from azure.mgmt.resource.resources.models import DeploymentMode
except ImportError:
    print('[ERROR] Azure SDK not installed. Run: pip install azure-identity azure-mgmt-resource')
    sys.exit(1)

# ============================================================================
# Color Output (cross-platform)
# ============================================================================

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

    @staticmethod
    def disable():
        """Disable colors (for Windows cmd or file output)"""
        Colors.GREEN = Colors.BLUE = Colors.YELLOW = Colors.RED = Colors.CYAN = Colors.BOLD = Colors.NC = ''

# Enable colors by default (can be disabled for Windows cmd)
if os.name == 'nt' and not os.environ.get('WT_SESSION'):
    Colors.disable()

# ============================================================================
# Deployment Configuration
# ============================================================================

class DeploymentConfig:
    """Configuration for deployment"""

    def __init__(self, subscription_id: str, location: str = 'uksouth',
                 resource_group: str = 'lab-master-lab', prefix: str = 'master-lab'):
        self.subscription_id = subscription_id
        self.location = location
        self.resource_group = resource_group
        self.prefix = prefix

        # Deployment names
        self.step1 = f'{prefix}-01-core'
        self.step2 = f'{prefix}-02-ai-foundry'
        self.step3 = f'{prefix}-03-supporting'
        self.step4 = f'{prefix}-04-mcp'

        # Bicep file paths (relative to lab directory)
        self.lab_dir = Path(__file__).parent
        self.bicep_dir = self.lab_dir / 'bicep'

    def validate(self) -> bool:
        """Validate configuration"""
        if not self.subscription_id:
            print(f'{Colors.RED}[ERROR]{Colors.NC} Subscription ID is required')
            return False

        if not self.bicep_dir.exists():
            print(f'{Colors.YELLOW}[WARN]{Colors.NC} Bicep directory not found: {self.bicep_dir}')
            print(f'  Deployment may fail if Bicep templates are not available')

        return True

# ============================================================================
# Azure Client Setup
# ============================================================================

def get_azure_credential():
    """Get Azure credential (try Service Principal, fallback to Azure CLI)"""
    # Try Service Principal from .azure-credentials.env
    creds_file = Path('.azure-credentials.env')
    if creds_file.exists():
        print(f'{Colors.BLUE}[*]{Colors.NC} Using Service Principal authentication')

        # Parse .env file manually (no external dependencies)
        env_vars = {}
        for line in creds_file.read_text().splitlines():
            if '=' in line and not line.strip().startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()

        tenant_id = env_vars.get('AZURE_TENANT_ID')
        client_id = env_vars.get('AZURE_CLIENT_ID')
        client_secret = env_vars.get('AZURE_CLIENT_SECRET')

        if tenant_id and client_id and client_secret:
            return ClientSecretCredential(tenant_id, client_id, client_secret)

    # Fallback to Azure CLI
    print(f'{Colors.BLUE}[*]{Colors.NC} Using Azure CLI authentication')
    return AzureCliCredential()

def create_resource_client(credential, subscription_id: str) -> ResourceManagementClient:
    """Create Azure Resource Management client"""
    return ResourceManagementClient(credential, subscription_id)

# ============================================================================
# Deployment Functions
# ============================================================================

def ensure_resource_group(client: ResourceManagementClient, name: str, location: str) -> bool:
    """Ensure resource group exists, create if not"""
    try:
        client.resource_groups.get(name)
        print(f'{Colors.GREEN}[OK]{Colors.NC} Resource group already exists: {name}')
        return True
    except:
        print(f'{Colors.BLUE}[*]{Colors.NC} Creating resource group: {name}')
        client.resource_groups.create_or_update(name, {'location': location})
        print(f'{Colors.GREEN}[OK]{Colors.NC} Resource group created')
        return True

def check_deployment_exists(client: ResourceManagementClient, resource_group: str,
                           deployment_name: str) -> Tuple[bool, Optional[str]]:
    """Check if deployment exists and get its status"""
    try:
        deployment = client.deployments.get(resource_group, deployment_name)
        provisioning_state = deployment.properties.provisioning_state
        return True, provisioning_state
    except:
        return False, None

def run_deployment_step(client: ResourceManagementClient, config: DeploymentConfig,
                       step_num: int, step_name: str, deployment_name: str,
                       bicep_file: str, parameters: Dict = None,
                       estimated_minutes: int = 10) -> Tuple[bool, Dict]:
    """
    Run a single deployment step

    Returns:
        (success: bool, outputs: dict)
    """
    print('=' * 80)
    print(f'{Colors.BOLD}STEP {step_num}: {step_name}{Colors.NC}')
    print('=' * 80)
    print(f'Deployment: {deployment_name}')
    print(f'Bicep Template: {bicep_file}')
    print(f'Estimated Time: ~{estimated_minutes} minutes')
    print()

    # Check if already deployed successfully
    exists, status = check_deployment_exists(client, config.resource_group, deployment_name)
    if exists and status == 'Succeeded':
        print(f'{Colors.GREEN}[OK]{Colors.NC} Deployment already succeeded, skipping')

        # Get outputs
        try:
            deployment = client.deployments.get(config.resource_group, deployment_name)
            outputs = deployment.properties.outputs or {}
            return True, {k: v['value'] for k, v in outputs.items()}
        except:
            return True, {}

    # Construct Bicep file path
    bicep_path = config.bicep_dir / bicep_file
    if not bicep_path.exists():
        print(f'{Colors.RED}[ERROR]{Colors.NC} Bicep file not found: {bicep_path}')
        return False, {}

    # Prepare deployment parameters
    with open(bicep_path, 'r') as f:
        template_content = f.read()

    deployment_properties = {
        'mode': DeploymentMode.incremental,
        'template': json.loads(template_content) if bicep_path.suffix == '.json' else None,
        'parameters': parameters or {}
    }

    # If Bicep file, need to compile first (use Azure CLI)
    if bicep_path.suffix == '.bicep':
        print(f'{Colors.BLUE}[*]{Colors.NC} Compiling Bicep template...')
        import subprocess
        result = subprocess.run(
            ['az', 'bicep', 'build', '--file', str(bicep_path), '--stdout'],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f'{Colors.RED}[ERROR]{Colors.NC} Bicep compilation failed: {result.stderr}')
            return False, {}

        deployment_properties['template'] = json.loads(result.stdout)

    # Start deployment
    print(f'{Colors.BLUE}[*]{Colors.NC} Starting deployment...')
    start_time = time.time()

    try:
        # Begin deployment (async)
        deploy_async = client.deployments.begin_create_or_update(
            config.resource_group,
            deployment_name,
            {'properties': deployment_properties}
        )

        # Wait for completion with progress updates
        last_update = time.time()
        while not deploy_async.done():
            elapsed = time.time() - start_time
            if time.time() - last_update > 30:  # Update every 30 seconds
                print(f'{Colors.CYAN}[*]{Colors.NC} Deployment in progress... ({int(elapsed/60)}m {int(elapsed%60)}s elapsed)')
                last_update = time.time()
            time.sleep(5)

        # Get result
        deployment = deploy_async.result()
        elapsed_time = time.time() - start_time

        if deployment.properties.provisioning_state == 'Succeeded':
            print(f'{Colors.GREEN}[OK]{Colors.NC} Deployment succeeded in {int(elapsed_time/60)}m {int(elapsed_time%60)}s')

            # Extract outputs
            outputs = deployment.properties.outputs or {}
            return True, {k: v['value'] for k, v in outputs.items()}
        else:
            print(f'{Colors.RED}[ERROR]{Colors.NC} Deployment failed: {deployment.properties.provisioning_state}')
            return False, {}

    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f'{Colors.RED}[ERROR]{Colors.NC} Deployment failed after {int(elapsed_time/60)}m {int(elapsed_time%60)}s')
        print(f'  Error: {str(e)}')
        return False, {}

def generate_env_file(config: DeploymentConfig, outputs: Dict[str, Dict]) -> str:
    """
    Generate .env file with deployment outputs

    Args:
        outputs: Dict with step outputs (step1, step2, step3, step4)

    Returns:
        Path to generated .env file
    """
    env_file = config.lab_dir / 'master-lab.env'

    print(f'{Colors.BLUE}[*]{Colors.NC} Generating environment file: {env_file}')

    content = f"""# Master AI Gateway Lab - Environment Variables
# Generated: {datetime.now().isoformat()}
# Subscription: {config.subscription_id}
# Resource Group: {config.resource_group}
# Location: {config.location}

# ============================================================================
# Azure Configuration
# ============================================================================
AZURE_SUBSCRIPTION_ID={config.subscription_id}
AZURE_RESOURCE_GROUP={config.resource_group}
AZURE_LOCATION={config.location}

# ============================================================================
# Step 1: Core Infrastructure Outputs
# ============================================================================
"""

    # Add step 1 outputs
    for key, value in outputs.get('step1', {}).items():
        content += f"{key.upper()}={value}\n"

    content += "\n# ============================================================================\n"
    content += "# Step 2: AI Foundry Outputs\n"
    content += "# ============================================================================\n"

    # Add step 2 outputs
    for key, value in outputs.get('step2', {}).items():
        content += f"{key.upper()}={value}\n"

    content += "\n# ============================================================================\n"
    content += "# Step 3: Supporting Services Outputs\n"
    content += "# ============================================================================\n"

    # Add step 3 outputs
    for key, value in outputs.get('step3', {}).items():
        content += f"{key.upper()}={value}\n"

    content += "\n# ============================================================================\n"
    content += "# Step 4: MCP Servers Outputs\n"
    content += "# ============================================================================\n"

    # Add step 4 outputs
    for key, value in outputs.get('step4', {}).items():
        content += f"{key.upper()}={value}\n"

    # Write to file
    env_file.write_text(content)
    print(f'{Colors.GREEN}[OK]{Colors.NC} Environment file generated')

    return str(env_file)

# ============================================================================
# Main Deployment Orchestration
# ============================================================================

def run_full_deployment(config: DeploymentConfig) -> bool:
    """Run complete 4-step deployment"""

    print(f'{Colors.BOLD}{"=" * 80}{Colors.NC}')
    print(f'{Colors.BOLD}MASTER AI GATEWAY LAB - AUTOMATED DEPLOYMENT{Colors.NC}')
    print(f'{Colors.BOLD}{"=" * 80}{Colors.NC}')
    print()
    print(f'Subscription: {config.subscription_id}')
    print(f'Resource Group: {config.resource_group}')
    print(f'Location: {config.location}')
    print(f'Deployment Prefix: {config.prefix}')
    print()
    print(f'{Colors.YELLOW}Estimated Total Time: ~40 minutes{Colors.NC}')
    print()

    total_start = time.time()

    # Initialize Azure client
    try:
        credential = get_azure_credential()
        client = create_resource_client(credential, config.subscription_id)
        print(f'{Colors.GREEN}[OK]{Colors.NC} Azure authentication successful')
        print()
    except Exception as e:
        print(f'{Colors.RED}[ERROR]{Colors.NC} Azure authentication failed: {e}')
        return False

    # Ensure resource group exists
    if not ensure_resource_group(client, config.resource_group, config.location):
        return False
    print()

    # Track outputs from each step
    all_outputs = {}

    # STEP 1: Core Infrastructure
    success, outputs = run_deployment_step(
        client, config, 1,
        'CORE INFRASTRUCTURE (APIM, Log Analytics, App Insights)',
        config.step1,
        'main-step1-core.bicep',
        parameters={},
        estimated_minutes=10
    )
    if not success:
        print(f'{Colors.RED}[ERROR]{Colors.NC} Step 1 failed. Stopping deployment.')
        return False
    all_outputs['step1'] = outputs
    print()

    # STEP 2: AI Foundry
    success, outputs = run_deployment_step(
        client, config, 2,
        'AI FOUNDRY (3 hubs + 14 models)',
        config.step2,
        'main-step2-ai-foundry.bicep',
        parameters={},
        estimated_minutes=15
    )
    if not success:
        print(f'{Colors.YELLOW}[WARN]{Colors.NC} Step 2 failed. Continuing with remaining steps...')
    all_outputs['step2'] = outputs
    print()

    # STEP 3: Supporting Services
    success, outputs = run_deployment_step(
        client, config, 3,
        'SUPPORTING SERVICES (Redis, Search, Cosmos, Content Safety)',
        config.step3,
        'main-step3-supporting.bicep',
        parameters={},
        estimated_minutes=10
    )
    if not success:
        print(f'{Colors.YELLOW}[WARN]{Colors.NC} Step 3 failed. Continuing with remaining steps...')
    all_outputs['step3'] = outputs
    print()

    # STEP 4: MCP Servers
    success, outputs = run_deployment_step(
        client, config, 4,
        'MCP SERVERS (Container Apps + 7 servers)',
        config.step4,
        'main-step4-mcp.bicep',
        parameters={},
        estimated_minutes=5
    )
    if not success:
        print(f'{Colors.YELLOW}[WARN]{Colors.NC} Step 4 failed.')
    all_outputs['step4'] = outputs
    print()

    # Generate environment file
    print('=' * 80)
    print(f'{Colors.BOLD}GENERATING ENVIRONMENT FILE{Colors.NC}')
    print('=' * 80)
    env_file = generate_env_file(config, all_outputs)
    print()

    # Final summary
    total_time = time.time() - total_start
    print('=' * 80)
    print(f'{Colors.GREEN}{Colors.BOLD}DEPLOYMENT COMPLETE{Colors.NC}')
    print('=' * 80)
    print(f'Total Time: {int(total_time/60)}m {int(total_time%60)}s')
    print(f'Environment File: {env_file}')
    print()
    print('Next Steps:')
    print(f'  1. Load environment: {Colors.CYAN}source {env_file}{Colors.NC}')
    print(f'  2. Open notebook: {Colors.CYAN}jupyter notebook master-ai-gateway.ipynb{Colors.NC}')
    print(f'  3. Run cells sequentially')
    print()

    return True

# ============================================================================
# CLI Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Master AI Gateway Lab - Automated Deployment',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Deploy with default settings (uses Azure CLI subscription)
  python az_up.py

  # Deploy to specific subscription and location
  python az_up.py --subscription-id "your-sub-id" --location "eastus"

  # Deploy with custom resource group
  python az_up.py --resource-group "my-lab-rg" --location "westus2"

  # Check what would be deployed (dry-run not yet implemented)
  python az_up.py --dry-run
        """
    )

    parser.add_argument('--subscription-id', '-s',
                       help='Azure subscription ID (defaults to current Azure CLI subscription)')
    parser.add_argument('--location', '-l', default='uksouth',
                       help='Azure region for deployment (default: uksouth)')
    parser.add_argument('--resource-group', '-g', default='lab-master-lab',
                       help='Resource group name (default: lab-master-lab)')
    parser.add_argument('--prefix', '-p', default='master-lab',
                       help='Deployment name prefix (default: master-lab)')
    parser.add_argument('--no-color', action='store_true',
                       help='Disable color output')

    args = parser.parse_args()

    # Disable colors if requested
    if args.no_color:
        Colors.disable()

    # Get subscription ID (from args or Azure CLI)
    subscription_id = args.subscription_id
    if not subscription_id:
        try:
            import subprocess
            result = subprocess.run(['az', 'account', 'show', '--query', 'id', '-o', 'tsv'],
                                  capture_output=True, text=True)
            subscription_id = result.stdout.strip()
            print(f'{Colors.BLUE}[*]{Colors.NC} Using current Azure CLI subscription: {subscription_id}')
        except:
            print(f'{Colors.RED}[ERROR]{Colors.NC} Could not determine subscription ID')
            print('  Either login with Azure CLI or provide --subscription-id')
            sys.exit(1)

    # Create configuration
    config = DeploymentConfig(
        subscription_id=subscription_id,
        location=args.location,
        resource_group=args.resource_group,
        prefix=args.prefix
    )

    # Validate configuration
    if not config.validate():
        sys.exit(1)

    # Run deployment
    success = run_full_deployment(config)

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
