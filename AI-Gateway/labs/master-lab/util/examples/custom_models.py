#!/usr/bin/env python3
"""
Custom Model Configuration Example

This example shows how to deploy with custom AI model configurations.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from util import deploy_complete_infrastructure, DeploymentConfig


def main():
    """Deploy with custom model configuration"""
    print("=" * 70)
    print("AZURE AI GATEWAY - CUSTOM MODEL DEPLOYMENT")
    print("=" * 70)
    print()

    # Custom model configurations
    # These will be deployed to the primary region (uksouth)
    primary_models = [
        {
            'name': 'gpt-4o-mini',
            'format': 'OpenAI',
            'version': '2024-07-18',
            'sku': 'GlobalStandard',
            'capacity': 150  # Higher capacity
        },
        {
            'name': 'gpt-4o',
            'format': 'OpenAI',
            'version': '2024-08-06',
            'sku': 'GlobalStandard',
            'capacity': 150  # Higher capacity
        },
        {
            'name': 'text-embedding-3-small',
            'format': 'OpenAI',
            'version': '1',
            'sku': 'GlobalStandard',
            'capacity': 30  # Higher capacity for embeddings
        },
        # Add more models as needed
    ]

    # Models for secondary regions (swedencentral, westeurope)
    secondary_models = [
        {
            'name': 'gpt-4o-mini',
            'format': 'OpenAI',
            'version': '2024-07-18',
            'sku': 'GlobalStandard',
            'capacity': 100
        },
        {
            'name': 'gpt-4o',
            'format': 'OpenAI',
            'version': '2024-08-06',
            'sku': 'GlobalStandard',
            'capacity': 50  # Lower capacity for failover regions
        }
    ]

    # Create deployment configuration
    config = DeploymentConfig(
        subscription_id=os.getenv('AZURE_SUBSCRIPTION_ID'),
        resource_group='lab-master-lab',
        location='uksouth',
        primary_models=primary_models,
        secondary_models=secondary_models,
        # Optional: Skip Content Safety to save costs
        deploy_content_safety=False
    )

    print("Configuration:")
    print(f"  Primary models: {len(config.primary_models)}")
    print(f"  Secondary models: {len(config.secondary_models)}")
    print()

    print("Primary Models:")
    for model in config.primary_models:
        print(f"  • {model['name']} v{model['version']} (capacity: {model['capacity']})")
    print()

    print("Secondary Models:")
    for model in config.secondary_models:
        print(f"  • {model['name']} v{model['version']} (capacity: {model['capacity']})")
    print()

    # Deploy
    outputs = deploy_complete_infrastructure(
        config,
        progress_callback=lambda p: print(f"[{p.status}] {p.step}: {p.message}")
    )

    # Save outputs
    outputs.to_env_file('master-lab.env')

    print()
    print("✅ Deployment complete with custom model configuration!")


if __name__ == '__main__':
    main()
