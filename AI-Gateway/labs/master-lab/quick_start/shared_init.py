"""
Shared Initialization Module for Azure AI Gateway Quick Start Labs

This module provides minimal, reusable initialization code for all lab notebooks.
Uses Azure CLI authentication (easiest method - just run `az login`).

Usage in notebooks:
    import sys
    sys.path.append('..')
    from quick_start.shared_init import *
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path for accessing master-lab resources
sys.path.append(str(Path(__file__).parent.parent))

# ============================================================================
# Configuration
# ============================================================================

def load_environment():
    """
    Load environment variables from master-lab.env
    Returns: dict of loaded environment variables

    Searches for master-lab.env in these locations (in order):
    1. Notebook directory (AI-Gateway/labs/master-lab/)
    2. Repository root (/workspaces/Azure-AI-Gateway-Easy-Deploy/)
    3. Current working directory
    """
    # Define search locations
    notebook_dir = Path(__file__).parent.parent
    repo_root = notebook_dir.parent.parent.parent  # AI-Gateway -> labs -> master-lab -> repo root

    search_paths = [
        notebook_dir / 'master-lab.env',                    # Notebook directory
        repo_root / 'master-lab.env',                       # Repository root
        Path.cwd() / 'master-lab.env',                      # Current working directory
    ]

    # Find the first existing env file
    env_file = None
    for path in search_paths:
        if path.exists():
            env_file = path
            break

    if env_file and env_file.exists():
        load_dotenv(env_file)
        print(f"✅ Loaded environment from: {env_file}")

        # Check if APIM_SUBSCRIPTION_KEY is missing and try to retrieve it
        if not os.getenv('APIM_SUBSCRIPTION_KEY') and os.getenv('APIM_SERVICE_NAME'):
            print("   ⚠️  APIM_SUBSCRIPTION_KEY is empty, attempting to retrieve...")
            try:
                from util.deploy_all import refresh_env_file_with_apim_key
                if refresh_env_file_with_apim_key(str(env_file)):
                    # Reload the updated env file
                    load_dotenv(env_file, override=True)
                    print("   ✅ APIM_SUBSCRIPTION_KEY retrieved and saved")
            except Exception as e:
                print(f"   ⚠️  Could not auto-retrieve key: {e}")
                print("   You may need to manually add APIM_SUBSCRIPTION_KEY to master-lab.env")

        return {
            'SUBSCRIPTION_ID': os.getenv('SUBSCRIPTION_ID'),
            'RESOURCE_GROUP': os.getenv('RESOURCE_GROUP'),
            'LOCATION': os.getenv('LOCATION', 'uksouth'),
            'APIM_SERVICE_NAME': os.getenv('APIM_SERVICE_NAME'),
            'APIM_GATEWAY_URL': os.getenv('APIM_GATEWAY_URL'),
            'APIM_SUBSCRIPTION_KEY': os.getenv('APIM_SUBSCRIPTION_KEY'),
            'AZURE_OPENAI_ENDPOINT': os.getenv('AZURE_OPENAI_ENDPOINT'),
            'COSMOS_ENDPOINT': os.getenv('COSMOS_ENDPOINT'),
            'COSMOS_ACCOUNT_NAME': os.getenv('COSMOS_ACCOUNT_NAME'),
            'REDIS_HOST': os.getenv('REDIS_HOST'),
            'SEARCH_ENDPOINT': os.getenv('SEARCH_ENDPOINT'),
            'SEARCH_SERVICE_NAME': os.getenv('SEARCH_SERVICE_NAME'),
            'LOG_ANALYTICS_WORKSPACE_ID': os.getenv('LOG_ANALYTICS_WORKSPACE_ID'),
            'LOG_ANALYTICS_CUSTOMER_ID': os.getenv('LOG_ANALYTICS_CUSTOMER_ID'),
        }
    else:
        print(f"⚠️  Environment file not found: {env_file}")
        print("   Run the main deployment notebook first to create master-lab.env")
        return {}


def check_azure_cli_auth():
    """
    Verify Azure CLI is installed and user is authenticated.
    Returns: dict with account info or None if not authenticated
    """
    try:
        result = subprocess.run(
            ['az', 'account', 'show', '--output', 'json'],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            import json
            account = json.loads(result.stdout)
            print(f"✅ Authenticated to Azure")
            print(f"   Account: {account['user']['name']}")
            print(f"   Subscription: {account['name']} ({account['id'][:8]}...)")
            return account
        else:
            print("❌ Not authenticated to Azure")
            print("   Run: az login")
            return None

    except FileNotFoundError:
        print("❌ Azure CLI not installed")
        print("   Install: https://learn.microsoft.com/cli/azure/install-azure-cli")
        return None
    except Exception as e:
        print(f"❌ Error checking authentication: {e}")
        return None


def get_azure_openai_client(endpoint=None, api_version="2024-10-21"):
    """
    Create Azure OpenAI client using APIM subscription key or Azure CLI credentials.

    Args:
        endpoint: Azure OpenAI endpoint (from APIM or direct)
        api_version: API version to use

    Returns:
        AzureOpenAI client instance
    """
    from openai import AzureOpenAI
    from azure.identity import AzureCliCredential, get_bearer_token_provider

    if endpoint is None:
        # Try OPENAI_ENDPOINT first (has /inference path), then fall back to APIM_GATEWAY_URL
        endpoint = os.getenv('OPENAI_ENDPOINT') or os.getenv('AZURE_OPENAI_ENDPOINT')

        # If using APIM_GATEWAY_URL, append /inference path
        if not endpoint:
            apim_url = os.getenv('APIM_GATEWAY_URL')
            if apim_url:
                endpoint = apim_url.rstrip('/') + '/inference'

    if not endpoint:
        raise ValueError("No Azure OpenAI endpoint found. Set OPENAI_ENDPOINT, AZURE_OPENAI_ENDPOINT, or APIM_GATEWAY_URL")

    # Check if APIM subscription key is available (try both naming conventions)
    apim_key = os.getenv('APIM_SUBSCRIPTION_KEY') or os.getenv('APIM_API_KEY')
    
    if apim_key:
        # Use APIM subscription key authentication
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=apim_key,
            api_version=api_version,
            default_headers={"Ocp-Apim-Subscription-Key": apim_key}
        )
        
        print(f"✅ Azure OpenAI client created")
        print(f"   Endpoint: {endpoint}")
        print(f"   Auth: APIM Subscription Key ({apim_key[:8]}...)")
    else:
        # Use Azure CLI credentials
        credential = AzureCliCredential()
        token_provider = get_bearer_token_provider(
            credential,
            "https://cognitiveservices.azure.com/.default"
        )

        client = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider,
            api_version=api_version
        )

        print(f"✅ Azure OpenAI client created")
        print(f"   Endpoint: {endpoint}")
        print(f"   Auth: Azure CLI (AzureCliCredential)")

    return client


def get_cosmos_client(endpoint=None):
    """
    Create Cosmos DB client using Azure CLI credentials.

    Args:
        endpoint: Cosmos DB endpoint

    Returns:
        CosmosClient instance
    """
    from azure.cosmos import CosmosClient
    from azure.identity import AzureCliCredential

    if endpoint is None:
        endpoint = os.getenv('COSMOS_ENDPOINT')

    if not endpoint:
        raise ValueError("No Cosmos DB endpoint found. Set COSMOS_ENDPOINT")

    credential = AzureCliCredential()
    client = CosmosClient(endpoint, credential)

    print(f"✅ Cosmos DB client created")
    print(f"   Endpoint: {endpoint}")
    print(f"   Auth: Azure CLI (AzureCliCredential)")

    return client


def get_search_client(endpoint=None, index_name="products-index"):
    """
    Create Azure AI Search client using Azure CLI credentials.

    Args:
        endpoint: Azure Search endpoint
        index_name: Name of the search index

    Returns:
        SearchClient instance
    """
    from azure.search.documents import SearchClient
    from azure.identity import AzureCliCredential

    if endpoint is None:
        endpoint = os.getenv('SEARCH_ENDPOINT')

    if not endpoint:
        raise ValueError("No Search endpoint found. Set SEARCH_ENDPOINT")

    credential = AzureCliCredential()
    client = SearchClient(
        endpoint=endpoint,
        index_name=index_name,
        credential=credential
    )

    print(f"✅ Azure AI Search client created")
    print(f"   Endpoint: {endpoint}")
    print(f"   Index: {index_name}")
    print(f"   Auth: Azure CLI (AzureCliCredential)")

    return client


def verify_resources():
    """
    Verify all required Azure resources exist in the resource group.
    Returns: dict with resource status
    """
    resource_group = os.getenv('RESOURCE_GROUP')

    if not resource_group:
        print("⚠️  RESOURCE_GROUP not set")
        return {}

    try:
        # Check if resource group exists
        result = subprocess.run(
            ['az', 'group', 'exists', '--name', resource_group],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.stdout.strip().lower() == 'true':
            print(f"✅ Resource group exists: {resource_group}")

            # List resources
            result = subprocess.run(
                ['az', 'resource', 'list', '--resource-group', resource_group,
                 '--query', '[].{name:name, type:type}', '--output', 'json'],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                import json
                resources = json.loads(result.stdout)

                resource_types = {}
                for resource in resources:
                    resource_type = resource['type'].split('/')[-1]
                    resource_types[resource_type] = resource['name']

                print(f"\n📋 Resources found ({len(resources)} total):")
                for rtype, name in sorted(resource_types.items()):
                    print(f"   • {rtype}: {name}")

                return resource_types
        else:
            print(f"❌ Resource group not found: {resource_group}")
            print("   Run the main deployment notebook first")
            return {}

    except Exception as e:
        print(f"❌ Error verifying resources: {e}")
        return {}


# ============================================================================
# Quick Initialization Function
# ============================================================================

def quick_init(verbose=True):
    """
    One-line initialization for lab notebooks.

    Returns:
        dict with initialized clients and config

    Usage:
        from quick_start.shared_init import quick_init
        config = quick_init()
        client = config['openai_client']
    """
    if verbose:
        print("=" * 70)
        print("Azure AI Gateway - Quick Start Initialization")
        print("=" * 70)
        print()

    # Load environment
    env = load_environment()
    print()

    # Check Azure CLI auth
    account = check_azure_cli_auth()
    if not account:
        raise RuntimeError("Azure CLI authentication required. Run: az login")
    print()

    # Verify resources
    if verbose:
        resources = verify_resources()
        print()

    if verbose:
        print("=" * 70)
        print("✅ Initialization Complete - Ready for Lab Exercises")
        print("=" * 70)

    return {
        'env': env,
        'account': account,
        'subscription_id': env.get('SUBSCRIPTION_ID'),
        'resource_group': env.get('RESOURCE_GROUP'),
        'location': env.get('LOCATION'),
    }


# ============================================================================
# Export commonly used modules
# ============================================================================

# Standard library
import json
import time
from datetime import datetime

# Azure core
from azure.identity import AzureCliCredential

# Azure OpenAI
from openai import AzureOpenAI

# Azure services
try:
    from azure.cosmos import CosmosClient
except ImportError:
    CosmosClient = None

try:
    from azure.search.documents import SearchClient
except ImportError:
    SearchClient = None

# Utilities
import requests

print("✅ Shared initialization module loaded")
print("   Available functions:")
print("   - quick_init() - One-line initialization")
print("   - load_environment() - Load master-lab.env")
print("   - check_azure_cli_auth() - Verify authentication")
print("   - get_azure_openai_client() - Create OpenAI client")
print("   - get_cosmos_client() - Create Cosmos DB client")
print("   - get_search_client() - Create Search client")
print("   - verify_resources() - Check deployed resources")
