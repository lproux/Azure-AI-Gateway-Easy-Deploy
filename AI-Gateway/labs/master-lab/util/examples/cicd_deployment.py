#!/usr/bin/env python3
"""
CI/CD Pipeline Deployment Example

This example shows how to use the deployment module in a CI/CD pipeline
with proper error handling, logging, and artifact generation.
"""

import os
import sys
import json
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from util import deploy_complete_infrastructure, DeploymentConfig, DeploymentProgress


# Configure logging for CI/CD
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cicd-deployment.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def validate_environment():
    """Validate required environment variables"""
    required_vars = [
        'AZURE_SUBSCRIPTION_ID',
        'AZURE_TENANT_ID',
        'AZURE_CLIENT_ID',
        'AZURE_CLIENT_SECRET',
        'RESOURCE_GROUP',
        'LOCATION'
    ]

    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        logger.error(f"Missing required environment variables: {', '.join(missing)}")
        return False

    logger.info("All required environment variables present")
    return True


def log_progress(progress: DeploymentProgress):
    """Log deployment progress in CI/CD friendly format"""
    level_map = {
        'pending': logging.INFO,
        'in_progress': logging.INFO,
        'completed': logging.INFO,
        'failed': logging.ERROR
    }

    level = level_map.get(progress.status, logging.INFO)

    msg = f"[{progress.status.upper()}] {progress.step}: {progress.message}"

    if progress.elapsed_seconds > 0:
        mins = int(progress.elapsed_seconds / 60)
        secs = int(progress.elapsed_seconds % 60)
        msg += f" ({mins}m {secs}s)"

    logger.log(level, msg)

    if progress.error:
        logger.error(f"Error details: {progress.error}")


def save_artifacts(outputs, output_dir='artifacts'):
    """Save deployment artifacts for CI/CD pipeline"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Save environment file
    env_file = output_path / 'master-lab.env'
    outputs.to_env_file(str(env_file))
    logger.info(f"Saved environment file: {env_file}")

    # Save JSON outputs
    json_file = output_path / 'deployment-outputs.json'
    outputs.to_json(str(json_file))
    logger.info(f"Saved JSON outputs: {json_file}")

    # Save summary for pipeline
    summary_file = output_path / 'deployment-summary.json'
    summary = {
        'status': 'success',
        'timestamp': outputs.deployment_timestamp,
        'duration_seconds': outputs.deployment_duration_seconds,
        'duration_minutes': round(outputs.deployment_duration_seconds / 60, 1),
        'resource_suffix': outputs.resource_suffix,
        'apim_gateway_url': outputs.apim_gateway_url,
        'apim_service_name': outputs.apim_service_name,
        'foundry_endpoints': {
            'foundry1': outputs.foundry1_endpoint,
            'foundry2': outputs.foundry2_endpoint,
            'foundry3': outputs.foundry3_endpoint
        },
        'mcp_servers_deployed': len(outputs.mcp_server_urls) if outputs.mcp_server_urls else 0
    }

    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)

    logger.info(f"Saved deployment summary: {summary_file}")

    # Create Azure DevOps / GitHub Actions compatible outputs
    if os.getenv('GITHUB_OUTPUT'):
        # GitHub Actions
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"apim_gateway_url={outputs.apim_gateway_url}\n")
            f.write(f"apim_service_name={outputs.apim_service_name}\n")
            f.write(f"resource_suffix={outputs.resource_suffix}\n")
        logger.info("Wrote outputs to GITHUB_OUTPUT")

    elif os.getenv('SYSTEM_TEAMPROJECT'):
        # Azure DevOps
        print(f"##vso[task.setvariable variable=ApimGatewayUrl;isOutput=true]{outputs.apim_gateway_url}")
        print(f"##vso[task.setvariable variable=ApimServiceName;isOutput=true]{outputs.apim_service_name}")
        print(f"##vso[task.setvariable variable=ResourceSuffix;isOutput=true]{outputs.resource_suffix}")
        logger.info("Wrote outputs to Azure DevOps variables")


def deploy_for_cicd():
    """Main deployment function for CI/CD"""
    logger.info("=" * 70)
    logger.info("AZURE AI GATEWAY - CI/CD DEPLOYMENT")
    logger.info("=" * 70)

    # Validate environment
    if not validate_environment():
        logger.error("Environment validation failed")
        return 1

    # Create configuration from environment variables
    config = DeploymentConfig(
        subscription_id=os.environ['AZURE_SUBSCRIPTION_ID'],
        resource_group=os.environ['RESOURCE_GROUP'],
        location=os.environ.get('LOCATION', 'uksouth'),
        tenant_id=os.environ['AZURE_TENANT_ID'],
        client_id=os.environ['AZURE_CLIENT_ID'],
        client_secret=os.environ['AZURE_CLIENT_SECRET'],
        # Optional configurations from environment
        deploy_content_safety=os.getenv('DEPLOY_CONTENT_SAFETY', 'true').lower() == 'true',
        deploy_mcp_servers=os.getenv('DEPLOY_MCP_SERVERS', 'true').lower() == 'true',
        apim_sku=os.getenv('APIM_SKU', 'Standardv2')
    )

    logger.info("Configuration:")
    logger.info(f"  Subscription ID: {config.subscription_id}")
    logger.info(f"  Resource Group: {config.resource_group}")
    logger.info(f"  Location: {config.location}")
    logger.info(f"  Resource Suffix: {config.resource_suffix}")
    logger.info(f"  Deploy Content Safety: {config.deploy_content_safety}")
    logger.info(f"  Deploy MCP Servers: {config.deploy_mcp_servers}")

    try:
        # Deploy infrastructure
        logger.info("Starting deployment...")
        outputs = deploy_complete_infrastructure(
            config,
            progress_callback=log_progress
        )

        # Save artifacts
        logger.info("Saving deployment artifacts...")
        save_artifacts(outputs)

        # Log summary
        logger.info("=" * 70)
        logger.info("DEPLOYMENT SUCCESSFUL")
        logger.info("=" * 70)
        logger.info(f"Duration: {outputs.deployment_duration_seconds/60:.1f} minutes")
        logger.info(f"APIM Gateway: {outputs.apim_gateway_url}")
        logger.info(f"Resource Suffix: {outputs.resource_suffix}")
        logger.info("=" * 70)

        return 0

    except Exception as e:
        logger.error("=" * 70)
        logger.error("DEPLOYMENT FAILED")
        logger.error("=" * 70)
        logger.error(f"Error: {e}", exc_info=True)
        logger.error("=" * 70)

        # Save failure summary
        failure_summary = {
            'status': 'failed',
            'error': str(e),
            'timestamp': str(Path('deployment.log').stat().st_mtime) if Path('deployment.log').exists() else None
        }

        output_path = Path('artifacts')
        output_path.mkdir(exist_ok=True)

        with open(output_path / 'deployment-summary.json', 'w') as f:
            json.dump(failure_summary, f, indent=2)

        return 1


if __name__ == '__main__':
    sys.exit(deploy_for_cicd())
