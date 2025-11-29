#!/usr/bin/env python3
"""
Azure AI Gateway Complete Deployment Module

One-command deployment for all labs:
- Core Infrastructure (APIM, App Insights, Log Analytics)
- AI Foundry (3 regions, multiple models)
- Supporting Services (Redis, Cosmos, Search, Content Safety)
- MCP Servers (Container Apps with 5 servers)
- Private Endpoints (optional)

Usage:
    from util import deploy_complete_infrastructure, DeploymentConfig

    config = DeploymentConfig(
        subscription_id='xxx',
        resource_group='lab-master-lab'
    )

    outputs = deploy_complete_infrastructure(config)
    outputs.to_env_file('master-lab.env')
"""

import os
import sys
import json
import time
import subprocess
import string
import random
import logging
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Callable, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta

# Azure SDKs
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential, AzureCliCredential, DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode, Deployment, DeploymentProperties
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.cognitiveservices.models import (
    Account,
    Sku,
    Deployment as CognitiveDeployment,
    DeploymentModel,
    DeploymentProperties as CognitiveDeploymentProperties
)
from azure.core.exceptions import ResourceNotFoundError

# Configure logging with Unicode-safe handlers for Jupyter compatibility
class UnicodeStreamHandler(logging.StreamHandler):
    """Stream handler that safely handles Unicode errors in Jupyter notebooks"""
    def emit(self, record):
        try:
            msg = self.format(record)
            # Replace problematic characters that cause Jupyter encoding issues
            stream = self.stream
            # Use 'replace' error handling to avoid surrogate errors
            stream.write(msg.encode('utf-8', errors='replace').decode('utf-8', errors='replace') + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('deployment.log', encoding='utf-8', errors='replace'),
        UnicodeStreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Disable verbose Azure SDK logging to prevent Unicode errors in Jupyter
# Azure SDK logs contain special characters that cause Jupyter encoding issues
for azure_logger_name in ['azure', 'azure.core', 'azure.identity', 'azure.mgmt']:
    azure_logger = logging.getLogger(azure_logger_name)
    azure_logger.setLevel(logging.WARNING)  # Only show warnings and errors
    azure_logger.propagate = False

# =============================================================================
# DEFAULT CONFIGURATIONS
# =============================================================================

DEFAULT_PRIMARY_MODELS = [
    {'name': 'gpt-4o-mini', 'format': 'OpenAI', 'version': '2024-07-18', 'sku': 'GlobalStandard', 'capacity': 100},
    {'name': 'gpt-4o', 'format': 'OpenAI', 'version': '2024-08-06', 'sku': 'GlobalStandard', 'capacity': 100},
    {'name': 'text-embedding-3-small', 'format': 'OpenAI', 'version': '1', 'sku': 'GlobalStandard', 'capacity': 20},
    {'name': 'text-embedding-3-large', 'format': 'OpenAI', 'version': '1', 'sku': 'GlobalStandard', 'capacity': 20},
]

DEFAULT_SECONDARY_MODELS = [
    {'name': 'gpt-4o-mini', 'format': 'OpenAI', 'version': '2024-07-18', 'sku': 'GlobalStandard', 'capacity': 100},
    {'name': 'gpt-4o', 'format': 'OpenAI', 'version': '2024-08-06', 'sku': 'GlobalStandard', 'capacity': 50},
    {'name': 'text-embedding-3-small', 'format': 'OpenAI', 'version': '1', 'sku': 'Standard', 'capacity': 120},
]

MCP_SERVERS = [
    {'name': 'weather', 'image': 'mcp/openweather:latest', 'port': 8080},
    {'name': 'github', 'image': 'ghcr.io/github/github-mcp-server:latest', 'port': 8080},
    {'name': 'product-catalog', 'image': 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest', 'port': 8080},
    {'name': 'place-order', 'image': 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest', 'port': 8080},
    {'name': 'ms-learn', 'image': 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest', 'port': 8080},
    {'name': 'excel', 'image': 'acrmcpwksp321028.azurecr.io/excel-analytics-mcp:v4', 'port': 8000},
    {'name': 'docs', 'image': 'acrmcpwksp321028.azurecr.io/research-docs-mcp:v2', 'port': 8000},
]

# External ACR for Excel/Docs MCP images
EXTERNAL_ACR_SERVER = 'acrmcpwksp321028.azurecr.io'

AI_FOUNDRY_REGIONS = [
    {'short_name': 'foundry1', 'location': 'uksouth', 'is_primary': True},
    {'short_name': 'foundry2', 'location': 'swedencentral', 'is_primary': False},
    {'short_name': 'foundry3', 'location': 'westeurope', 'is_primary': False},
]

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class DeploymentConfig:
    """Configuration for deployment"""
    subscription_id: str
    resource_group: str
    location: str = 'uksouth'
    resource_suffix: Optional[str] = None  # Auto-generated if None

    # Optional credential override
    tenant_id: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None

    # Model configurations
    primary_models: List[dict] = None
    secondary_models: List[dict] = None

    # Feature flags
    deploy_private_endpoints: bool = False
    deploy_content_safety: bool = True
    deploy_mcp_servers: bool = True

    # Advanced options
    apim_sku: str = 'Standardv2'
    redis_sku: str = 'Balanced_B0'
    search_sku: str = 'basic'

    def __post_init__(self):
        # Auto-detect subscription ID from Azure CLI if not provided
        if not self.subscription_id or self.subscription_id.strip() == '':
            try:
                result = subprocess.run(
                    ['az', 'account', 'show', '--query', 'id', '-o', 'tsv'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0 and result.stdout.strip():
                    self.subscription_id = result.stdout.strip()
                    logger.info(f"Auto-detected subscription ID: {self.subscription_id[:8]}...")
                else:
                    raise ValueError("Could not auto-detect subscription ID from Azure CLI")
            except Exception as e:
                raise ValueError(
                    f"Subscription ID is required but was not provided and could not be auto-detected. "
                    f"Please provide subscription_id or run 'az login' first. Error: {e}"
                )

        if not self.resource_suffix:
            self.resource_suffix = generate_random_suffix()
        if not self.primary_models:
            self.primary_models = DEFAULT_PRIMARY_MODELS
        if not self.secondary_models:
            self.secondary_models = DEFAULT_SECONDARY_MODELS


@dataclass
class DeploymentProgress:
    """Track deployment progress"""
    step: str
    status: str  # 'pending', 'in_progress', 'completed', 'failed'
    message: str
    elapsed_seconds: float = 0
    error: Optional[str] = None


@dataclass
class ResourceOutputs:
    """All deployed resource outputs"""
    # Core
    apim_gateway_url: str = ''
    apim_subscription_key: str = ''
    apim_service_name: str = ''
    apim_subscriptions: List[dict] = field(default_factory=list)

    # AI Foundry
    foundry1_endpoint: str = ''
    foundry1_key: str = ''
    foundry2_endpoint: str = ''
    foundry2_key: str = ''
    foundry3_endpoint: str = ''
    foundry3_key: str = ''

    # Supporting Services
    redis_host: str = ''
    redis_key: str = ''
    cosmos_endpoint: str = ''
    cosmos_account_name: str = ''
    cosmos_key: str = ''
    search_endpoint: str = ''
    search_service_name: str = ''
    search_api_key: str = ''

    # Optional
    content_safety_endpoint: Optional[str] = None
    content_safety_key: Optional[str] = None
    mcp_server_urls: Optional[Dict[str, str]] = None  # Container Apps URLs
    mcp_aci_urls: Optional[Dict[str, str]] = None     # Container Instances URLs

    # Infrastructure
    log_analytics_workspace_id: str = ''
    log_analytics_customer_id: str = ''
    log_analytics_primary_shared_key: str = ''
    app_insights_connection_string: str = ''
    app_insights_instrumentation_key: str = ''

    # Container Registry (for MCP)
    container_registry_name: str = ''
    container_registry_login_server: str = ''

    # Deployment metadata
    deployment_timestamp: str = ''
    deployment_duration_seconds: float = 0
    resource_suffix: str = ''

    def to_env_file(self, file_path: str):
        """Generate master-lab.env file"""
        env_content = f"""# Azure AI Gateway Lab Environment
# Generated: {self.deployment_timestamp}
# Deployment Duration: {self.deployment_duration_seconds:.1f}s
# Resource Suffix: {self.resource_suffix}

# ===== Subscription & Resource Group =====
SUBSCRIPTION_ID={self.resource_suffix}
RESOURCE_GROUP=lab-master-lab
LOCATION=uksouth

# ===== API Management =====
APIM_SERVICE_NAME={self.apim_service_name}
APIM_GATEWAY_URL={self.apim_gateway_url}
APIM_SUBSCRIPTION_KEY={self.apim_subscription_key}

# ===== AI Foundry Hubs =====
FOUNDRY1_ENDPOINT={self.foundry1_endpoint}
FOUNDRY1_KEY={self.foundry1_key}
FOUNDRY2_ENDPOINT={self.foundry2_endpoint}
FOUNDRY2_KEY={self.foundry2_key}
FOUNDRY3_ENDPOINT={self.foundry3_endpoint}
FOUNDRY3_KEY={self.foundry3_key}

# ===== Redis Cache (Semantic Caching) =====
REDIS_HOST={self.redis_host}
REDIS_KEY={self.redis_key}
REDIS_PORT=10000

# ===== Cosmos DB (Message Storage) =====
COSMOS_ENDPOINT={self.cosmos_endpoint}
COSMOS_ACCOUNT_NAME={self.cosmos_account_name}
COSMOS_KEY={self.cosmos_key}

# ===== Azure AI Search =====
SEARCH_ENDPOINT={self.search_endpoint}
SEARCH_SERVICE_NAME={self.search_service_name}
SEARCH_API_KEY={self.search_api_key}

# ===== Content Safety =====
CONTENT_SAFETY_ENDPOINT={self.content_safety_endpoint or ''}
CONTENT_SAFETY_KEY={self.content_safety_key or ''}

# ===== Monitoring =====
LOG_ANALYTICS_WORKSPACE_ID={self.log_analytics_workspace_id}
LOG_ANALYTICS_CUSTOMER_ID={self.log_analytics_customer_id}
APP_INSIGHTS_INSTRUMENTATION_KEY={self.app_insights_instrumentation_key}
APP_INSIGHTS_CONNECTION_STRING={self.app_insights_connection_string}

# ===== Container Registry (MCP) =====
CONTAINER_REGISTRY_NAME={self.container_registry_name}
CONTAINER_REGISTRY_LOGIN_SERVER={self.container_registry_login_server}
"""

        # Add MCP Server URLs (Container Apps)
        if self.mcp_server_urls:
            env_content += "\n# ===== MCP Server URLs (Container Apps) =====\n"
            for server_name, url in self.mcp_server_urls.items():
                env_var_name = f"MCP_{server_name.upper().replace('-', '_')}_URL"
                env_content += f"{env_var_name}={url}\n"

        # Add MCP ACI URLs (Container Instances)
        if self.mcp_aci_urls:
            env_content += "\n# ===== MCP Server URLs (Container Instances - Redundancy) =====\n"
            for server_name, url in self.mcp_aci_urls.items():
                env_var_name = f"MCP_{server_name.upper().replace('-', '_')}_ACI_URL"
                env_content += f"{env_var_name}={url}\n"

        with open(file_path, 'w') as f:
            f.write(env_content)

        logger.info(f"Environment file written to: {file_path}")

    def to_mcp_config_file(self, file_path: str):
        """Generate .mcp-servers-config file for notebook_mcp_helpers.py"""
        config_content = f"""# MCP Servers Configuration
# Generated: {self.deployment_timestamp}
# This file is read by notebook_mcp_helpers.py for MCP client initialization

"""

        # Map MCP server names to expected config variable names
        # notebook_mcp_helpers.py expects these specific names
        config_mapping = {
            'weather': 'APIM_WEATHER_URL',
            'github': 'APIM_GITHUB_URL',
            'product-catalog': 'PRODUCT_CATALOG_URL',
            'place-order': 'PLACE_ORDER_URL',
            'ms-learn': 'MS_LEARN_URL',
            'excel': 'EXCEL_MCP_URL',
            'docs': 'DOCS_MCP_URL',
        }

        # Write Container Apps URLs (primary)
        config_content += "# ===== Primary MCP Server URLs (Container Apps) =====\n"
        if self.mcp_server_urls:
            for server_name, url in self.mcp_server_urls.items():
                config_var = config_mapping.get(server_name, f"MCP_{server_name.upper().replace('-', '_')}_URL")
                config_content += f"{config_var}={url}\n"

        # Write ACI URLs (redundancy/fallback)
        if self.mcp_aci_urls:
            config_content += "\n# ===== Fallback MCP Server URLs (Container Instances) =====\n"
            for server_name, url in self.mcp_aci_urls.items():
                config_var = config_mapping.get(server_name, f"MCP_{server_name.upper().replace('-', '_')}_URL")
                # Use _ACI suffix for fallback URLs
                config_content += f"{config_var}_ACI={url}\n"

        with open(file_path, 'w') as f:
            f.write(config_content)

        logger.info(f"MCP config file written to: {file_path}")

    def to_json(self, file_path: str):
        """Save outputs to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(asdict(self), f, indent=2)
        logger.info(f"Outputs saved to JSON: {file_path}")


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def generate_random_suffix(length: int = 13) -> str:
    """Generate random suffix for resource names"""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def compile_bicep_template(bicep_file: str) -> Optional[str]:
    """Compile Bicep to JSON ARM template"""
    json_file = bicep_file.replace('.bicep', '.json')

    # Check if JSON is newer than Bicep
    if os.path.exists(json_file):
        bicep_time = os.path.getmtime(bicep_file)
        json_time = os.path.getmtime(json_file)
        if json_time > bicep_time:
            logger.info(f"Using existing compiled template: {json_file}")
            return json_file

    logger.info(f"Compiling Bicep template: {bicep_file}")
    result = subprocess.run(
        f'az bicep build --file {bicep_file}',
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        logger.error(f"Bicep compilation failed: {result.stderr}")
        return None

    logger.info(f"Compiled successfully: {json_file}")
    return json_file


def deploy_arm_template(
    resource_client: ResourceManagementClient,
    resource_group: str,
    deployment_name: str,
    template_path: str,
    parameters: dict,
    progress_callback: Optional[Callable[[DeploymentProgress], None]] = None
) -> Tuple[bool, dict]:
    """Deploy ARM template with progress tracking"""
    logger.info(f"Starting deployment: {deployment_name}")

    # Load template
    with open(template_path) as f:
        template = json.load(f)

    # Create deployment
    deployment_properties = DeploymentProperties(
        mode=DeploymentMode.incremental,
        template=template,
        parameters=parameters or {}
    )

    deployment_async = resource_client.deployments.begin_create_or_update(
        resource_group,
        deployment_name,
        Deployment(properties=deployment_properties)
    )

    # Wait with progress updates
    return wait_for_deployment(deployment_async, deployment_name, progress_callback)


def wait_for_deployment(
    deployment_async,
    deployment_name: str,
    progress_callback: Optional[Callable[[DeploymentProgress], None]] = None
) -> Tuple[bool, dict]:
    """Wait for deployment with progress updates"""
    start_time = time.time()
    last_update = start_time

    while not deployment_async.done():
        time.sleep(30)
        elapsed = time.time() - start_time

        if time.time() - last_update >= 60:
            mins = int(elapsed / 60)
            secs = int(elapsed % 60)
            msg = f"Still deploying... {mins}m {secs}s elapsed"
            logger.info(msg)

            if progress_callback:
                progress = DeploymentProgress(
                    step=deployment_name,
                    status='in_progress',
                    message=msg,
                    elapsed_seconds=elapsed
                )
                progress_callback(progress)

            last_update = time.time()

    # Get result
    deployment_result = deployment_async.result()
    elapsed = time.time() - start_time
    mins = int(elapsed / 60)
    secs = int(elapsed % 60)

    if deployment_result.properties.provisioning_state == 'Succeeded':
        logger.info(f"Deployment succeeded in {mins}m {secs}s")

        # Get outputs
        outputs = {}
        if deployment_result.properties.outputs:
            outputs = {k: v['value'] for k, v in deployment_result.properties.outputs.items()}

        if progress_callback:
            progress = DeploymentProgress(
                step=deployment_name,
                status='completed',
                message=f"Completed in {mins}m {secs}s",
                elapsed_seconds=elapsed
            )
            progress_callback(progress)

        return True, outputs
    else:
        error_msg = f"Deployment failed: {deployment_result.properties.provisioning_state}"
        if deployment_result.properties.error:
            error_msg += f" - {deployment_result.properties.error.message}"

        logger.error(error_msg)

        if progress_callback:
            progress = DeploymentProgress(
                step=deployment_name,
                status='failed',
                message=f"Failed after {mins}m {secs}s",
                elapsed_seconds=elapsed,
                error=error_msg
            )
            progress_callback(progress)

        return False, {}


def create_credential(config: DeploymentConfig):
    """Create Azure credential (Service Principal or Azure CLI)"""
    # Priority 1: Explicit credentials in config
    if all([config.tenant_id, config.client_id, config.client_secret]):
        logger.info("Using Service Principal credentials from config")
        return ClientSecretCredential(
            config.tenant_id,
            config.client_id,
            config.client_secret
        )

    # Priority 2: .azure-credentials.env file
    credentials_file = '.azure-credentials.env'
    if os.path.exists(credentials_file):
        load_dotenv(credentials_file)
        tenant_id = os.getenv('AZURE_TENANT_ID')
        client_id = os.getenv('AZURE_CLIENT_ID')
        client_secret = os.getenv('AZURE_CLIENT_SECRET')

        if all([tenant_id, client_id, client_secret]):
            logger.info("Using Service Principal credentials from .azure-credentials.env")
            return ClientSecretCredential(tenant_id, client_id, client_secret)

    # Priority 3: Azure CLI
    logger.info("Using Azure CLI credentials")
    return AzureCliCredential()


def verify_prerequisites(config: DeploymentConfig):
    """Verify prerequisites before deployment"""
    logger.info("Verifying prerequisites...")

    # Check Azure CLI installed
    result = subprocess.run(['az', '--version'], capture_output=True)
    if result.returncode != 0:
        raise RuntimeError("Azure CLI not installed. Please install from https://aka.ms/azure-cli")

    logger.info("Azure CLI installed")

    # Check Bicep installed
    result = subprocess.run(['az', 'bicep', 'version'], capture_output=True)
    if result.returncode != 0:
        raise RuntimeError("Bicep not installed. Run: az bicep install")

    logger.info("Bicep installed")

    # Verify we can authenticate
    credential = create_credential(config)

    # Test credential by creating resource client
    try:
        resource_client = ResourceManagementClient(credential, config.subscription_id)
        # Try to get subscription info
        resource_client.resource_groups.list()
        logger.info("Successfully authenticated to Azure")
    except Exception as e:
        raise RuntimeError(f"Failed to authenticate: {e}")

    # Check if resource group exists
    try:
        resource_client.resource_groups.get(config.resource_group)
        logger.info(f"Resource group exists: {config.resource_group}")
    except ResourceNotFoundError:
        logger.info(f"Creating resource group: {config.resource_group}")
        resource_client.resource_groups.create_or_update(
            config.resource_group,
            {'location': config.location}
        )

    logger.info("Prerequisites verified")


def check_deployment_exists(
    resource_client: ResourceManagementClient,
    resource_group: str,
    deployment_name: str
) -> bool:
    """Check if deployment exists and succeeded"""
    try:
        deployment = resource_client.deployments.get(resource_group, deployment_name)
        return deployment.properties.provisioning_state == 'Succeeded'
    except:
        return False


# =============================================================================
# DEPLOYMENT STEP FUNCTIONS
# =============================================================================

def _deploy_step1_core(
    config: DeploymentConfig,
    credential,
    resource_client: ResourceManagementClient,
    progress_callback: Optional[Callable]
) -> dict:
    """Deploy Step 1: Core Infrastructure"""
    logger.info("=" * 70)
    logger.info("STEP 1: CORE INFRASTRUCTURE")
    logger.info("=" * 70)
    logger.info("Resources: APIM, App Insights, Log Analytics")
    logger.info("Estimated time: ~15 minutes")

    if progress_callback:
        progress_callback(DeploymentProgress(
            step="Core Infrastructure",
            status="in_progress",
            message="Deploying APIM, App Insights, Log Analytics..."
        ))

    deployment_name = 'master-lab-01-core'

    # Check if already deployed
    if check_deployment_exists(resource_client, config.resource_group, deployment_name):
        logger.info("Step 1 already deployed. Retrieving outputs...")
        deployment = resource_client.deployments.get(config.resource_group, deployment_name)
        outputs = {k: v['value'] for k, v in deployment.properties.outputs.items()} if deployment.properties.outputs else {}

        if progress_callback:
            progress_callback(DeploymentProgress(
                step="Core Infrastructure",
                status="completed",
                message="Already deployed (skipped)"
            ))

        return outputs

    # Find and compile Bicep template
    bicep_path = Path('deploy/deploy-01-core.bicep')
    if not bicep_path.exists():
        raise FileNotFoundError(f"Bicep template not found: {bicep_path}")

    json_path = compile_bicep_template(str(bicep_path))
    if not json_path:
        raise RuntimeError("Failed to compile Bicep template")

    # Deploy
    parameters = {
        'apimSku': {'value': config.apim_sku}
    }

    success, outputs = deploy_arm_template(
        resource_client,
        config.resource_group,
        deployment_name,
        json_path,
        parameters,
        progress_callback
    )

    if not success:
        raise RuntimeError("Step 1 deployment failed")

    # Save outputs
    output_file = 'step1-outputs.json'
    with open(output_file, 'w') as f:
        json.dump(outputs, f, indent=2)
    logger.info(f"Step 1 outputs saved to {output_file}")

    return outputs


def _deploy_step2_ai_foundry(
    config: DeploymentConfig,
    credential,
    resource_client: ResourceManagementClient,
    progress_callback: Optional[Callable]
) -> dict:
    """Deploy Step 2: AI Foundry Hubs + Models"""
    logger.info("=" * 70)
    logger.info("STEP 2: AI FOUNDRY HUBS + MODELS")
    logger.info("=" * 70)
    logger.info("Resources: 3 AI Foundry Hubs + Model Deployments")
    logger.info("Estimated time: ~30 minutes")

    if progress_callback:
        progress_callback(DeploymentProgress(
            step="AI Foundry Hubs",
            status="in_progress",
            message="Deploying AI Foundry hubs and models..."
        ))

    # Create Cognitive Services client
    cog_client = CognitiveServicesManagementClient(credential, config.subscription_id)

    # Phase 1: Create AI Foundry Hubs
    logger.info("Phase 1: Creating AI Foundry Hubs...")

    existing_accounts = {acc.name: acc for acc in cog_client.accounts.list_by_resource_group(config.resource_group)}
    foundry_endpoints = {}
    foundry_keys = {}

    for region_config in AI_FOUNDRY_REGIONS:
        foundry_name = f"{region_config['short_name']}-{config.resource_suffix}"
        location = region_config['location']

        logger.info(f"Checking hub: {foundry_name}")

        if foundry_name in existing_accounts:
            account = existing_accounts[foundry_name]
            logger.info(f"  Hub already exists (State: {account.properties.provisioning_state})")
        else:
            logger.info(f"  Creating hub in {location}...")
            try:
                account_params = Account(
                    location=location,
                    sku=Sku(name='S0'),
                    kind='AIServices',
                    properties={
                        'customSubDomainName': foundry_name.lower(),
                        'publicNetworkAccess': 'Enabled',
                        'allowProjectManagement': True
                    },
                    identity={'type': 'SystemAssigned'}
                )

                poller = cog_client.accounts.begin_create(
                    config.resource_group,
                    foundry_name,
                    account_params
                )
                account = poller.result(timeout=300)
                logger.info(f"  Hub created successfully")
            except Exception as e:
                logger.error(f"  Failed to create hub: {e}")
                raise

        # Get endpoint and key
        foundry_endpoints[region_config['short_name']] = account.properties.endpoint
        keys = cog_client.accounts.list_keys(config.resource_group, foundry_name)
        foundry_keys[region_config['short_name']] = keys.key1

    # Phase 2: Deploy Models
    logger.info("Phase 2: Deploying models...")

    deployment_results = {
        'succeeded': [],
        'failed': [],
        'skipped': []
    }

    for region_config in AI_FOUNDRY_REGIONS:
        foundry_name = f"{region_config['short_name']}-{config.resource_suffix}"
        is_primary = region_config['is_primary']
        models = config.primary_models if is_primary else config.secondary_models

        logger.info(f"Deploying {len(models)} models to {foundry_name}...")

        for model in models:
            model_name = model['name']
            logger.info(f"  Deploying model: {model_name}...")

            try:
                # Check if already deployed
                try:
                    existing = cog_client.deployments.get(
                        config.resource_group,
                        foundry_name,
                        model_name
                    )
                    if existing.properties.provisioning_state == 'Succeeded':
                        logger.info(f"    Already deployed (skipping)")
                        deployment_results['skipped'].append(f"{foundry_name}/{model_name}")
                        continue
                except:
                    pass

                # Create deployment
                deployment_params = CognitiveDeployment(
                    sku=Sku(name=model['sku'], capacity=model['capacity']),
                    properties=CognitiveDeploymentProperties(
                        model=DeploymentModel(
                            format=model['format'],
                            name=model['name'],
                            version=model['version']
                        )
                    )
                )

                poller = cog_client.deployments.begin_create_or_update(
                    config.resource_group,
                    foundry_name,
                    model_name,
                    deployment_params
                )

                result = poller.result(timeout=600)
                logger.info(f"    Deployed successfully")
                deployment_results['succeeded'].append(f"{foundry_name}/{model_name}")

            except Exception as e:
                error_msg = str(e)
                logger.warning(f"    Failed: {error_msg[:100]}")
                deployment_results['failed'].append({
                    'model': f"{foundry_name}/{model_name}",
                    'error': error_msg
                })
                continue

    # Log summary
    logger.info(f"Model deployment summary:")
    logger.info(f"  Succeeded: {len(deployment_results['succeeded'])}")
    logger.info(f"  Skipped: {len(deployment_results['skipped'])}")
    logger.info(f"  Failed: {len(deployment_results['failed'])}")

    if progress_callback:
        progress_callback(DeploymentProgress(
            step="AI Foundry Hubs",
            status="completed",
            message=f"Deployed {len(deployment_results['succeeded']) + len(deployment_results['skipped'])} models"
        ))

    # Build outputs
    outputs = {}
    for region_config in AI_FOUNDRY_REGIONS:
        short_name = region_config['short_name']
        outputs[f'{short_name}Endpoint'] = foundry_endpoints.get(short_name, '')
        outputs[f'{short_name}Key'] = foundry_keys.get(short_name, '')

    # Save outputs
    output_file = 'step2-outputs.json'
    with open(output_file, 'w') as f:
        json.dump(outputs, f, indent=2)
    logger.info(f"Step 2 outputs saved to {output_file}")

    return outputs


def _deploy_step3_supporting(
    config: DeploymentConfig,
    credential,
    resource_client: ResourceManagementClient,
    progress_callback: Optional[Callable]
) -> dict:
    """Deploy Step 3: Supporting Services"""
    logger.info("=" * 70)
    logger.info("STEP 3: SUPPORTING SERVICES")
    logger.info("=" * 70)
    logger.info("Resources: Redis, Search, Cosmos, Content Safety")
    logger.info("Estimated time: ~10 minutes")

    if progress_callback:
        progress_callback(DeploymentProgress(
            step="Supporting Services",
            status="in_progress",
            message="Deploying Redis, Search, Cosmos, Content Safety..."
        ))

    deployment_name = 'master-lab-03-supporting'

    # Check if already deployed
    if check_deployment_exists(resource_client, config.resource_group, deployment_name):
        logger.info("Step 3 already deployed. Retrieving outputs...")
        deployment = resource_client.deployments.get(config.resource_group, deployment_name)
        outputs = {k: v['value'] for k, v in deployment.properties.outputs.items()} if deployment.properties.outputs else {}

        if progress_callback:
            progress_callback(DeploymentProgress(
                step="Supporting Services",
                status="completed",
                message="Already deployed (skipped)"
            ))

        return outputs

    # Find and compile Bicep template
    bicep_path = Path('deploy/deploy-03-supporting.bicep')
    if not bicep_path.exists():
        raise FileNotFoundError(f"Bicep template not found: {bicep_path}")

    json_path = compile_bicep_template(str(bicep_path))
    if not json_path:
        raise RuntimeError("Failed to compile Bicep template")

    # Deploy
    parameters = {
        'location': {'value': config.location},
        'redisCacheSku': {'value': config.redis_sku},
        'searchSku': {'value': config.search_sku}
    }

    success, outputs = deploy_arm_template(
        resource_client,
        config.resource_group,
        deployment_name,
        json_path,
        parameters,
        progress_callback
    )

    if not success:
        raise RuntimeError("Step 3 deployment failed")

    # Save outputs
    output_file = 'step3-outputs.json'
    with open(output_file, 'w') as f:
        json.dump(outputs, f, indent=2)
    logger.info(f"Step 3 outputs saved to {output_file}")

    return outputs


def _deploy_step4_mcp_servers(
    config: DeploymentConfig,
    credential,
    resource_client: ResourceManagementClient,
    step1_outputs: dict,
    progress_callback: Optional[Callable]
) -> dict:
    """Deploy Step 4: MCP Servers"""
    if not config.deploy_mcp_servers:
        logger.info("MCP server deployment disabled. Skipping...")
        return {}

    logger.info("=" * 70)
    logger.info("STEP 4: MCP SERVERS")
    logger.info("=" * 70)
    logger.info("Resources: Container Apps + 5 MCP servers")
    logger.info("Estimated time: ~5 minutes")

    if progress_callback:
        progress_callback(DeploymentProgress(
            step="MCP Servers",
            status="in_progress",
            message="Deploying Container Apps and MCP servers..."
        ))

    deployment_name = 'master-lab-04-mcp'

    # Check if already deployed
    if check_deployment_exists(resource_client, config.resource_group, deployment_name):
        logger.info("Step 4 already deployed. Retrieving outputs...")
        deployment = resource_client.deployments.get(config.resource_group, deployment_name)
        outputs = {k: v['value'] for k, v in deployment.properties.outputs.items()} if deployment.properties.outputs else {}

        if progress_callback:
            progress_callback(DeploymentProgress(
                step="MCP Servers",
                status="completed",
                message="Already deployed (skipped)"
            ))

        return outputs

    # Find and compile Bicep template
    bicep_path = Path('deploy/deploy-04-mcp.bicep')
    if not bicep_path.exists():
        raise FileNotFoundError(f"Bicep template not found: {bicep_path}")

    json_path = compile_bicep_template(str(bicep_path))
    if not json_path:
        raise RuntimeError("Failed to compile Bicep template")

    # Build parameters from Step 1 outputs
    parameters = {
        'location': {'value': config.location},
        'logAnalyticsCustomerId': {'value': step1_outputs.get('logAnalyticsCustomerId', '')},
        'logAnalyticsPrimarySharedKey': {'value': step1_outputs.get('logAnalyticsPrimarySharedKey', '')}
    }

    success, outputs = deploy_arm_template(
        resource_client,
        config.resource_group,
        deployment_name,
        json_path,
        parameters,
        progress_callback
    )

    if not success:
        raise RuntimeError("Step 4 deployment failed")

    # Save outputs
    output_file = 'step4-outputs.json'
    with open(output_file, 'w') as f:
        json.dump(outputs, f, indent=2)
    logger.info(f"Step 4 outputs saved to {output_file}")

    return outputs


# =============================================================================
# POST-DEPLOYMENT CONFIGURATION
# =============================================================================

def _configure_apim_cosmos_rbac(
    config: DeploymentConfig,
    step1_outputs: dict,
    step3_outputs: dict,
    progress_callback: Optional[Callable[[DeploymentProgress], None]] = None
):
    """Configure RBAC for APIM to access Cosmos DB for message storage"""
    logger.info("=" * 70)
    logger.info("POST-DEPLOYMENT: APIM COSMOS DB RBAC")
    logger.info("=" * 70)

    if progress_callback:
        progress_callback(DeploymentProgress(
            step="APIM Configuration",
            status="in_progress",
            message="Configuring APIM access to Cosmos DB..."
        ))

    try:
        # Get APIM and Cosmos DB details
        apim_service_name = step1_outputs.get('apimServiceName')
        cosmos_account_name = step3_outputs.get('cosmosDbAccountName')

        if not apim_service_name or not cosmos_account_name:
            logger.warning("APIM or Cosmos DB not found, skipping RBAC configuration")
            return

        # Use az CLI to configure RBAC (handles API versioning issues)
        logger.info(f"Granting Cosmos DB access to APIM: {apim_service_name}")

        # Get APIM principal ID
        cmd_get_principal = f"""
        az resource show \
          --ids "/subscriptions/{config.subscription_id}/resourceGroups/{config.resource_group}/providers/Microsoft.ApiManagement/service/{apim_service_name}" \
          --query "identity.principalId" \
          -o tsv
        """

        result = subprocess.run(cmd_get_principal, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            logger.warning(f"Failed to get APIM principal ID: {result.stderr}")
            return

        apim_principal_id = result.stdout.strip()
        if not apim_principal_id:
            logger.warning("APIM does not have a managed identity")
            return

        logger.info(f"APIM Principal ID: {apim_principal_id}")

        # Grant Cosmos DB Data Contributor role
        cmd_grant_role = f"""
        az cosmosdb sql role assignment create \
          --account-name {cosmos_account_name} \
          --resource-group {config.resource_group} \
          --role-definition-name "Cosmos DB Built-in Data Contributor" \
          --principal-id {apim_principal_id} \
          --scope "/subscriptions/{config.subscription_id}/resourceGroups/{config.resource_group}/providers/Microsoft.DocumentDB/databaseAccounts/{cosmos_account_name}" \
          2>&1
        """

        result = subprocess.run(cmd_grant_role, shell=True, capture_output=True, text=True, timeout=60)

        # Check if successful or already exists
        if result.returncode == 0 or "already exists" in result.stdout.lower() or "already exists" in result.stderr.lower():
            logger.info("✅ APIM granted Cosmos DB Data Contributor role")

            if progress_callback:
                progress_callback(DeploymentProgress(
                    step="APIM Configuration",
                    status="completed",
                    message="APIM can now access Cosmos DB"
                ))
        else:
            logger.warning(f"Failed to grant Cosmos DB role: {result.stderr}")

            if progress_callback:
                progress_callback(DeploymentProgress(
                    step="APIM Configuration",
                    status="completed",
                    message="RBAC configuration skipped (may require manual setup)"
                ))

    except Exception as e:
        logger.warning(f"RBAC configuration failed: {e}")

        if progress_callback:
            progress_callback(DeploymentProgress(
                step="APIM Configuration",
                status="completed",
                message="RBAC configuration skipped"
            ))


def _apply_message_storage_policy(
    config: DeploymentConfig,
    step1_outputs: dict,
    step3_outputs: dict,
    progress_callback: Optional[Callable[[DeploymentProgress], None]] = None
):
    """Apply message storage policy to APIM inference API"""
    logger.info("=" * 70)
    logger.info("POST-DEPLOYMENT: APPLY MESSAGE STORAGE POLICY")
    logger.info("=" * 70)

    if progress_callback:
        progress_callback(DeploymentProgress(
            step="APIM Policy",
            status="in_progress",
            message="Applying message storage policy..."
        ))

    try:
        # Get APIM and Cosmos DB details
        apim_service_name = step1_outputs.get('apimServiceName')
        cosmos_endpoint = step3_outputs.get('cosmosDbEndpoint')

        if not apim_service_name or not cosmos_endpoint:
            logger.warning("APIM or Cosmos DB not found, skipping policy configuration")
            return

        logger.info(f"Applying policy to APIM: {apim_service_name}")

        # Read policy template
        policy_path = Path('policies/backend-pool-with-message-storage-policy.xml')
        if not policy_path.exists():
            logger.warning(f"Policy file not found: {policy_path}")
            return

        with open(policy_path, 'r') as f:
            policy_content = f.read()

        # Replace placeholders
        policy_content = policy_content.replace('{{CosmosEndpoint}}', cosmos_endpoint)

        # Create JSON body for API
        import json as json_module
        api_body = {
            "properties": {
                "value": policy_content,
                "format": "rawxml"
            }
        }

        # Save JSON body to temp file
        temp_policy_path = Path('/tmp/message-storage-policy.json')
        with open(temp_policy_path, 'w') as f:
            json_module.dump(api_body, f)

        # Apply policy using az CLI
        cmd_apply_policy = f"""
        az rest \
          --method PUT \
          --url "https://management.azure.com/subscriptions/{config.subscription_id}/resourceGroups/{config.resource_group}/providers/Microsoft.ApiManagement/service/{apim_service_name}/apis/inference/policies/policy?api-version=2022-09-01-preview" \
          --body '@{str(temp_policy_path)}' \
          --headers "Content-Type=application/json"
        """

        result = subprocess.run(cmd_apply_policy, shell=True, capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            logger.info("✅ Message storage policy applied successfully")

            if progress_callback:
                progress_callback(DeploymentProgress(
                    step="APIM Policy",
                    status="completed",
                    message="Message storage policy applied"
                ))
        else:
            logger.warning(f"Failed to apply policy: {result.stderr}")

            if progress_callback:
                progress_callback(DeploymentProgress(
                    step="APIM Policy",
                    status="completed",
                    message="Policy application skipped"
                ))

    except Exception as e:
        logger.warning(f"Policy configuration failed: {e}")

        if progress_callback:
            progress_callback(DeploymentProgress(
                step="APIM Policy",
                status="completed",
                message="Policy application skipped"
            ))


def _enable_response_body_logging(
    config: DeploymentConfig,
    step1_outputs: dict,
    step3_outputs: dict,
    progress_callback: Optional[Callable[[DeploymentProgress], None]] = None
):
    """Enable response body logging in APIM for token metrics in Log Analytics"""
    logger.info("=" * 70)
    logger.info("POST-DEPLOYMENT: ENABLE RESPONSE BODY LOGGING")
    logger.info("=" * 70)

    apim_service_name = f"apim-{config.resource_suffix}"

    logger.info("Enabling backend response body logging for inference-api...")
    logger.info("This allows token usage metrics to be captured in Log Analytics")

    # Configuration for Azure Monitor diagnostic with response body logging
    diagnostic_config = {
        "properties": {
            "loggerId": f"/subscriptions/{config.subscription_id}/resourceGroups/{config.resource_group}/providers/Microsoft.ApiManagement/service/{apim_service_name}/loggers/azuremonitor",
            "alwaysLog": "allErrors",
            "sampling": {
                "percentage": 100,
                "samplingType": "fixed"
            },
            "frontend": {
                "request": {"body": {"bytes": 8192}},
                "response": {"body": {"bytes": 8192}}
            },
            "backend": {
                "request": {"body": {"bytes": 8192}},
                "response": {"body": {"bytes": 8192}}  # Captures token usage
            },
            "logClientIp": True,
            "verbosity": "information"
        }
    }

    # Write to temp file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(diagnostic_config, f, indent=2)
        temp_file = f.name

    try:
        url = f"https://management.azure.com/subscriptions/{config.subscription_id}/resourceGroups/{config.resource_group}/providers/Microsoft.ApiManagement/service/{apim_service_name}/apis/inference-api/diagnostics/azuremonitor?api-version=2022-09-01-preview"

        cmd = f'az rest --method PUT --url "{url}" --body @{temp_file}'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            logger.info("✓ Response body logging enabled")
            logger.info("  Backend response bodies will be logged to Log Analytics")
            logger.info("  This enables token metrics in ApiManagementGatewayLogs")

            if progress_callback:
                progress_callback(DeploymentProgress(
                    step="Response Logging",
                    status="completed",
                    message="Backend response body logging enabled"
                ))
        else:
            logger.warning(f"Failed to enable response body logging: {result.stderr[:200]}")
            logger.warning("Token metrics from Log Analytics may not be available")

            if progress_callback:
                progress_callback(DeploymentProgress(
                    step="Response Logging",
                    status="completed",
                    message="Response logging skipped (non-critical)"
                ))

    except Exception as e:
        logger.warning(f"Could not enable response body logging: {e}")
        logger.warning("This is not critical - token metrics are still available from Cosmos DB")

        if progress_callback:
            progress_callback(DeploymentProgress(
                step="Response Logging",
                status="completed",
                message="Response logging skipped (non-critical)"
            ))

    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


# =============================================================================
# MAIN DEPLOYMENT FUNCTION
# =============================================================================

def deploy_complete_infrastructure(
    config: DeploymentConfig,
    progress_callback: Optional[Callable[[DeploymentProgress], None]] = None
) -> ResourceOutputs:
    """
    Deploy complete Azure AI Gateway infrastructure in one command.

    Deploys in order:
    1. Core Infrastructure (APIM, App Insights, Log Analytics)
    2. AI Foundry Hubs + Models (3 regions)
    3. Supporting Services (Redis, Cosmos, Search, Content Safety)
    4. MCP Servers (Container Apps with 5 servers)
    5. Private Endpoints (optional)

    Args:
        config: Deployment configuration
        progress_callback: Optional callback for progress updates

    Returns:
        ResourceOutputs with all deployed resource details

    Example:
        >>> config = DeploymentConfig(
        ...     subscription_id='xxx',
        ...     resource_group='lab-master-lab'
        ... )
        >>> outputs = deploy_complete_infrastructure(config)
        >>> outputs.to_env_file('master-lab.env')
    """
    start_time = time.time()
    logger.info("=" * 70)
    logger.info("AZURE AI GATEWAY COMPLETE DEPLOYMENT")
    logger.info("=" * 70)
    logger.info(f"Subscription: {config.subscription_id}")
    logger.info(f"Resource Group: {config.resource_group}")
    logger.info(f"Location: {config.location}")
    logger.info(f"Resource Suffix: {config.resource_suffix}")
    logger.info("=" * 70)

    try:
        # Verify prerequisites
        verify_prerequisites(config)

        # Create clients
        credential = create_credential(config)
        resource_client = ResourceManagementClient(credential, config.subscription_id)

        # Deploy each step
        step1_outputs = _deploy_step1_core(config, credential, resource_client, progress_callback)
        step2_outputs = _deploy_step2_ai_foundry(config, credential, resource_client, progress_callback)
        step3_outputs = _deploy_step3_supporting(config, credential, resource_client, progress_callback)
        step4_outputs = _deploy_step4_mcp_servers(config, credential, resource_client, step1_outputs, progress_callback)

        # Post-deployment: Configure RBAC for APIM to access Cosmos DB
        _configure_apim_cosmos_rbac(config, step1_outputs, step3_outputs, progress_callback)

        # Post-deployment: Apply message storage policy
        _apply_message_storage_policy(config, step1_outputs, step3_outputs, progress_callback)

        # Post-deployment: Enable response body logging for token metrics
        _enable_response_body_logging(config, step1_outputs, step3_outputs, progress_callback)

        # Build ResourceOutputs
        outputs = ResourceOutputs(
            # Core
            apim_gateway_url=step1_outputs.get('apimGatewayUrl', ''),
            apim_service_name=step1_outputs.get('apimServiceName', ''),
            apim_subscriptions=step1_outputs.get('apimSubscriptions', []),
            apim_subscription_key=step1_outputs.get('apimSubscriptions', [{}])[0].get('primaryKey', ''),

            # AI Foundry
            foundry1_endpoint=step2_outputs.get('foundry1Endpoint', ''),
            foundry1_key=step2_outputs.get('foundry1Key', ''),
            foundry2_endpoint=step2_outputs.get('foundry2Endpoint', ''),
            foundry2_key=step2_outputs.get('foundry2Key', ''),
            foundry3_endpoint=step2_outputs.get('foundry3Endpoint', ''),
            foundry3_key=step2_outputs.get('foundry3Key', ''),

            # Supporting Services
            redis_host=step3_outputs.get('redisCacheHost', ''),
            redis_key=step3_outputs.get('redisCacheKey', ''),
            cosmos_endpoint=step3_outputs.get('cosmosDbEndpoint', ''),
            cosmos_account_name=step3_outputs.get('cosmosDbAccountName', ''),
            cosmos_key=step3_outputs.get('cosmosDbKey', ''),
            search_endpoint=step3_outputs.get('searchServiceEndpoint', ''),
            search_service_name=step3_outputs.get('searchServiceName', ''),
            search_api_key=step3_outputs.get('searchServiceAdminKey', ''),
            content_safety_endpoint=step3_outputs.get('contentSafetyEndpoint'),
            content_safety_key=step3_outputs.get('contentSafetyKey'),

            # Infrastructure
            log_analytics_workspace_id=step1_outputs.get('logAnalyticsWorkspaceId', ''),
            log_analytics_customer_id=step1_outputs.get('logAnalyticsCustomerId', ''),
            log_analytics_primary_shared_key=step1_outputs.get('logAnalyticsPrimarySharedKey', ''),
            app_insights_connection_string=step1_outputs.get('appInsightsConnectionString', ''),
            app_insights_instrumentation_key=step1_outputs.get('appInsightsInstrumentationKey', ''),

            # Container Registry
            container_registry_name=step4_outputs.get('containerRegistryName', ''),
            container_registry_login_server=step4_outputs.get('containerRegistryLoginServer', ''),

            # MCP Server URLs (Container Apps)
            mcp_server_urls={
                item['name']: item['url']
                for item in step4_outputs.get('mcpServerUrls', [])
            } if step4_outputs else None,

            # MCP Server URLs (Container Instances - ACI)
            mcp_aci_urls={
                item['name']: item['url']
                for item in step4_outputs.get('mcpAciUrls', [])
            } if step4_outputs and step4_outputs.get('mcpAciUrls') else None,

            # Metadata
            deployment_timestamp=datetime.now().isoformat(),
            deployment_duration_seconds=time.time() - start_time,
            resource_suffix=config.resource_suffix
        )

        # Save complete outputs
        outputs.to_json('deployment-outputs.json')

        # Save MCP config file for notebook_mcp_helpers.py
        outputs.to_mcp_config_file('.mcp-servers-config')

        elapsed = time.time() - start_time
        logger.info("=" * 70)
        logger.info("DEPLOYMENT COMPLETE")
        logger.info("=" * 70)
        logger.info(f"Total time: {elapsed:.1f}s ({elapsed/60:.1f} minutes)")
        logger.info(f"Outputs saved to: deployment-outputs.json")
        logger.info("=" * 70)

        if progress_callback:
            progress_callback(DeploymentProgress(
                step="Complete",
                status="completed",
                message="All resources deployed successfully",
                elapsed_seconds=elapsed
            ))

        return outputs

    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"Deployment failed after {elapsed:.1f}s: {e}")

        if progress_callback:
            progress_callback(DeploymentProgress(
                step="Deployment",
                status="failed",
                message=f"Deployment failed",
                elapsed_seconds=elapsed,
                error=str(e)
            ))

        raise


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Deploy Azure AI Gateway infrastructure')
    parser.add_argument('--subscription-id', required=True, help='Azure subscription ID')
    parser.add_argument('--resource-group', default='lab-master-lab', help='Resource group name')
    parser.add_argument('--location', default='uksouth', help='Primary location')
    parser.add_argument('--suffix', help='Resource name suffix (auto-generated if not provided)')
    parser.add_argument('--skip-mcp', action='store_true', help='Skip MCP server deployment')
    parser.add_argument('--output', default='master-lab.env', help='Output environment file')

    args = parser.parse_args()

    config = DeploymentConfig(
        subscription_id=args.subscription_id,
        resource_group=args.resource_group,
        location=args.location,
        resource_suffix=args.suffix,
        deploy_mcp_servers=not args.skip_mcp
    )

    def print_progress(progress: DeploymentProgress):
        status_icons = {
            'pending': '⏳',
            'in_progress': '🔄',
            'completed': '✅',
            'failed': '❌'
        }
        icon = status_icons.get(progress.status, '•')
        print(f"{icon} [{progress.status.upper()}] {progress.step}: {progress.message}")

    outputs = deploy_complete_infrastructure(config, progress_callback=print_progress)
    outputs.to_env_file(args.output)

    print()
    print(f"✅ Deployment complete! Environment saved to {args.output}")


if __name__ == '__main__':
    main()
