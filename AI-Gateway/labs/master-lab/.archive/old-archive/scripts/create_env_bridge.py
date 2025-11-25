#!/usr/bin/env python3
"""
Create .env file from master-lab.env for notebook compatibility
Bridges our deployed resources to notebook's expected variable names
"""

import os
import json
from pathlib import Path

print('=' * 80)
print('CREATE .ENV BRIDGE FROM MASTER-LAB.ENV')
print('=' * 80)
print()

# Load master-lab.env
master_env = {}
master_env_path = Path('master-lab.env')

if not master_env_path.exists():
    print('[ERROR] master-lab.env not found!')
    exit(1)

print('[*] Loading master-lab.env...')
for line in master_env_path.read_text(encoding='utf-8').splitlines():
    if '=' in line and not line.strip().startswith('#'):
        key, value = line.split('=', 1)
        master_env[key.strip()] = value.strip()

print(f'[OK] Loaded {len(master_env)} variables')
print()

# Get Azure credentials from environment or step outputs
subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID', '')
tenant_id = os.getenv('AZURE_TENANT_ID', '')
client_id = os.getenv('AZURE_CLIENT_ID', '')
client_secret = os.getenv('AZURE_CLIENT_SECRET', '')

# Try to get from step1-outputs.json if not in environment
if not subscription_id and Path('step1-outputs.json').exists():
    with open('step1-outputs.json') as f:
        step1 = json.load(f)
        # Extract subscription ID from resource IDs
        for key, value in step1.items():
            if isinstance(value, str) and '/subscriptions/' in value:
                subscription_id = value.split('/subscriptions/')[1].split('/')[0]
                break

print(f'[*] Azure credentials:')
print(f'    SUBSCRIPTION_ID: {"[OK] found" if subscription_id else "[!!] missing"}')
print(f'    TENANT_ID: {"[OK] found" if tenant_id else "[!!] missing"}')
print(f'    CLIENT_ID: {"[OK] found" if client_id else "[  ] not set (optional)"}')
print(f'    CLIENT_SECRET: {"[OK] found" if client_secret else "[  ] not set (optional)"}')
print()

# Map our resources to notebook expectations
# Key insight: APIM Gateway IS the Azure OpenAI-compatible endpoint
apim_url = master_env.get('APIM_GATEWAY_URL', '')
apim_key = master_env.get('APIM_API_KEY', '')
inference_path = master_env.get('INFERENCE_API_PATH', 'inference')

# The OpenAI endpoint is APIM + inference path
openai_endpoint = f'{apim_url}/{inference_path}' if apim_url else ''

# Default deployment model (we deployed gpt-4o-mini across all foundries)
default_deployment = 'gpt-4o-mini'

print('[*] Resource mapping:')
print(f'    APIM Gateway: {apim_url}')
print(f'    Inference Path: {inference_path}')
print(f'    OpenAI Endpoint: {openai_endpoint}')
print(f'    Default Model: {default_deployment}')
print()

# Create .env content
env_content = f"""# Auto-generated .env bridge from master-lab.env
# Generated to match notebook's expected variable names

# Azure Authentication (from environment or manual input required)
AZURE_SUBSCRIPTION_ID={subscription_id}
AZURE_TENANT_ID={tenant_id}
AZURE_CLIENT_ID={client_id}
AZURE_CLIENT_SECRET={client_secret}

# Resource Group and Location
AZURE_RG={master_env.get('RESOURCE_GROUP', 'lab-master-lab')}
AZURE_LOCATION={master_env.get('LOCATION', 'uksouth')}

# Azure OpenAI (via APIM Gateway)
AZURE_OPENAI_ENDPOINT={openai_endpoint}
AZURE_OPENAI_API_KEY={apim_key}
AZURE_OPENAI_API_VERSION=2024-10-01-preview
AZURE_OPENAI_DEPLOYMENT={default_deployment}

# Additional AI Foundry info
FOUNDRY_PROJECT_ENDPOINT={master_env.get('FOUNDRY_PROJECT_ENDPOINT', '')}
INFERENCE_API_PATH={inference_path}

# APIM Resources
APIM_GATEWAY_URL={apim_url}
APIM_SERVICE_ID={master_env.get('APIM_SERVICE_ID', '')}
APIM_SERVICE_NAME={master_env.get('APIM_SERVICE_NAME', '')}
APIM_API_KEY={apim_key}

# Supporting Services (from Steps 3)
REDIS_HOST={master_env.get('REDIS_HOST', '')}
REDIS_PORT={master_env.get('REDIS_PORT', '10000')}
REDIS_KEY={master_env.get('REDIS_KEY', '')}

SEARCH_SERVICE_NAME={master_env.get('SEARCH_SERVICE_NAME', '')}
SEARCH_ENDPOINT={master_env.get('SEARCH_ENDPOINT', '')}
SEARCH_ADMIN_KEY={master_env.get('SEARCH_ADMIN_KEY', '')}

COSMOS_ACCOUNT_NAME={master_env.get('COSMOS_ACCOUNT_NAME', '')}
COSMOS_ENDPOINT={master_env.get('COSMOS_ENDPOINT', '')}
COSMOS_KEY={master_env.get('COSMOS_KEY', '')}

CONTENT_SAFETY_ENDPOINT={master_env.get('CONTENT_SAFETY_ENDPOINT', '')}
CONTENT_SAFETY_KEY={master_env.get('CONTENT_SAFETY_KEY', '')}

# MCP Servers (from Step 4)
CONTAINER_REGISTRY={master_env.get('CONTAINER_REGISTRY', '')}
CONTAINER_APP_ENV_ID={master_env.get('CONTAINER_APP_ENV_ID', '')}
"""

# Write .env file
env_path = Path('.env')
env_path.write_text(env_content, encoding='utf-8')

print('[OK] Created .env file')
print()

# Validate critical variables
missing = []
critical_vars = {
    'AZURE_SUBSCRIPTION_ID': subscription_id,
    'AZURE_OPENAI_ENDPOINT': openai_endpoint,
    'AZURE_OPENAI_API_KEY': apim_key,
}

print('[*] Validating critical variables:')
for var, value in critical_vars.items():
    status = '[OK]' if value else '[!!]'
    print(f'    {status} {var}: {value[:50] if value else "MISSING"}...')
    if not value:
        missing.append(var)

print()

if missing:
    print('[WARNING] Missing critical variables:')
    for var in missing:
        print(f'    - {var}')
    print()
    print('[ACTION REQUIRED] Please set these variables:')
    if 'AZURE_SUBSCRIPTION_ID' in missing:
        print('    export AZURE_SUBSCRIPTION_ID="your-subscription-id"')
    if 'AZURE_TENANT_ID' in missing:
        print('    export AZURE_TENANT_ID="your-tenant-id"')
    print()
    print('Or update .env file manually with correct values.')
else:
    print('[OK] All critical variables present!')

print()
print('=' * 80)
print('[DONE] .env bridge created successfully')
print('=' * 80)
