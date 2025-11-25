#!/usr/bin/env python3
"""
Basic Deployment Example

This example shows the simplest way to deploy all Azure AI Gateway resources.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from util import deploy_complete_infrastructure, DeploymentConfig, DeploymentProgress


def show_progress(progress: DeploymentProgress):
    """Display progress updates with colored status icons"""
    status_icons = {
        'pending': '⏳',
        'in_progress': '🔄',
        'completed': '✅',
        'failed': '❌'
    }

    icon = status_icons.get(progress.status, '•')
    print(f"\n{icon} [{progress.status.upper()}] {progress.step}")
    print(f"   {progress.message}")

    if progress.elapsed_seconds > 0:
        mins = int(progress.elapsed_seconds / 60)
        secs = int(progress.elapsed_seconds % 60)
        print(f"   Time: {mins}m {secs}s")

    if progress.error:
        print(f"   ❌ Error: {progress.error}")


def main():
    """Main deployment function"""
    print("=" * 70)
    print("AZURE AI GATEWAY - BASIC DEPLOYMENT")
    print("=" * 70)
    print()

    # Get subscription ID from environment or prompt
    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    if not subscription_id:
        subscription_id = input("Enter your Azure Subscription ID: ").strip()

    # Create deployment configuration
    config = DeploymentConfig(
        subscription_id=subscription_id,
        resource_group='lab-master-lab',
        location='uksouth'
    )

    print(f"Subscription ID: {config.subscription_id}")
    print(f"Resource Group: {config.resource_group}")
    print(f"Location: {config.location}")
    print(f"Resource Suffix: {config.resource_suffix}")
    print()

    # Confirm deployment
    response = input("Proceed with deployment? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Deployment cancelled.")
        return 1

    print()
    print("Starting deployment...")
    print("This will take approximately 60 minutes.")
    print()

    try:
        # Deploy all infrastructure
        outputs = deploy_complete_infrastructure(
            config,
            progress_callback=show_progress
        )

        # Save outputs
        outputs.to_env_file('master-lab.env')
        outputs.to_json('deployment-outputs.json')

        # Display summary
        print()
        print("=" * 70)
        print("DEPLOYMENT COMPLETE")
        print("=" * 70)
        print(f"Duration: {outputs.deployment_duration_seconds/60:.1f} minutes")
        print(f"Timestamp: {outputs.deployment_timestamp}")
        print()
        print("Key Resources:")
        print(f"  • APIM Gateway URL: {outputs.apim_gateway_url}")
        print(f"  • APIM Service Name: {outputs.apim_service_name}")
        print(f"  • AI Foundry Hub 1: {outputs.foundry1_endpoint}")
        print(f"  • Redis Cache: {outputs.redis_host}")
        print(f"  • Search Service: {outputs.search_service_name}")
        print()
        print("Output Files:")
        print("  • master-lab.env (environment variables)")
        print("  • deployment-outputs.json (complete outputs)")
        print("  • deployment.log (detailed log)")
        print()
        print("=" * 70)
        print("✅ All resources deployed successfully!")
        print("=" * 70)

        return 0

    except Exception as e:
        print()
        print("=" * 70)
        print("❌ DEPLOYMENT FAILED")
        print("=" * 70)
        print(f"Error: {e}")
        print()
        print("Check deployment.log for detailed error information.")
        print("You can re-run this script to resume the deployment.")
        print("=" * 70)

        return 1


if __name__ == '__main__':
    sys.exit(main())
