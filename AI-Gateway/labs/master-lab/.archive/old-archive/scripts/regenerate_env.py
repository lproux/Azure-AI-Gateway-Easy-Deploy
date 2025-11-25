#!/usr/bin/env python3
"""
Regenerate master-lab.env from all deployment outputs
"""

import json
import os
from datetime import datetime

print('=' * 70)
print('REGENERATE MASTER-LAB.ENV')
print('=' * 70)
print()

# Load all output files
step1_outputs = {}
step2_outputs = {}
step2c_outputs = {}
step3_outputs = {}
step4_outputs = {}

if os.path.exists('step1-outputs.json'):
    with open('step1-outputs.json') as f:
        step1_outputs = json.load(f)
    print('[OK] Loaded Step 1 outputs')

if os.path.exists('step2-outputs.json'):
    with open('step2-outputs.json') as f:
        step2_outputs = json.load(f)
    print('[OK] Loaded Step 2 outputs')

if os.path.exists('step2c-outputs.json'):
    with open('step2c-outputs.json') as f:
        step2c_outputs = json.load(f)
    print('[OK] Loaded Step 2c outputs')

if os.path.exists('step3-outputs.json'):
    with open('step3-outputs.json') as f:
        step3_outputs = json.load(f)
    print('[OK] Loaded Step 3 outputs')

if os.path.exists('step4-outputs.json'):
    with open('step4-outputs.json') as f:
        step4_outputs = json.load(f)
    print('[OK] Loaded Step 4 outputs')

print()

# Build env file content
env_content = f"""# Master AI Gateway Lab - Deployment Outputs
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Resource Group: lab-master-lab

# ===========================================
# APIM (API Management)
# ===========================================
APIM_GATEWAY_URL={step1_outputs.get('apimGatewayUrl', '')}
APIM_SERVICE_ID={step1_outputs.get('apimServiceId', '')}
APIM_SERVICE_NAME={step1_outputs.get('apimServiceName', '')}
APIM_API_KEY={step1_outputs.get('apimSubscriptions', [{}])[0].get('key', '')}

# ===========================================
# AI Foundry
# ===========================================
FOUNDRY_PROJECT_ENDPOINT={step2c_outputs.get('aiServicesConfig', [{}])[0].get('foundryProjectEndpoint', '')}
INFERENCE_API_PATH={step2c_outputs.get('inferenceAPIPath', 'inference')}

# ===========================================
# Supporting Services
# ===========================================

# Redis (Semantic Caching)
REDIS_HOST={step3_outputs.get('redisCacheHost', '')}
REDIS_PORT={step3_outputs.get('redisCachePort', '10000')}
REDIS_KEY={step3_outputs.get('redisCacheKey', '')}

# Azure Cognitive Search
SEARCH_SERVICE_NAME={step3_outputs.get('searchServiceName', '')}
SEARCH_ENDPOINT={step3_outputs.get('searchServiceEndpoint', '')}
SEARCH_ADMIN_KEY={step3_outputs.get('searchServiceAdminKey', '')}

# Cosmos DB
COSMOS_ACCOUNT_NAME={step3_outputs.get('cosmosDbAccountName', '')}
COSMOS_ENDPOINT={step3_outputs.get('cosmosDbEndpoint', '')}
COSMOS_KEY={step3_outputs.get('cosmosDbKey', '')}

# Content Safety
CONTENT_SAFETY_ENDPOINT={step3_outputs.get('contentSafetyEndpoint', '')}
CONTENT_SAFETY_KEY={step3_outputs.get('contentSafetyKey', '')}

# ===========================================
# MCP Servers
# ===========================================
CONTAINER_REGISTRY={step4_outputs.get('containerRegistryName', '')}
CONTAINER_APP_ENV_ID={step4_outputs.get('containerAppEnvId', '')}

# ===========================================
# Deployment Info
# ===========================================
RESOURCE_GROUP=lab-master-lab
LOCATION=uksouth
DEPLOYMENT_PREFIX=master-lab
"""

# Write env file
with open('master-lab.env', 'w') as f:
    f.write(env_content)

print('[OK] Generated master-lab.env')
print()

# Show summary
print('=' * 70)
print('ENV FILE SUMMARY')
print('=' * 70)
filled_vars = []
empty_vars = []

for line in env_content.split('\n'):
    if '=' in line and not line.startswith('#'):
        key, value = line.split('=', 1)
        if value and value != '':
            filled_vars.append(key)
        else:
            empty_vars.append(key)

print(f'[*] Filled variables: {len(filled_vars)}')
print(f'[*] Empty variables: {len(empty_vars)}')

if empty_vars:
    print()
    print('[!] Empty variables:')
    for var in empty_vars:
        print(f'    - {var}')

print()
print('[OK] master-lab.env is ready!')
