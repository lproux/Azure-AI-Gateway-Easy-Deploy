#!/usr/bin/env python3
"""
Resilient AI Foundry Deployment
Deploys hubs first, then models one-by-one with error handling
"""

import os
import json
import time
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential, AzureCliCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.cognitiveservices.models import (
    Account,
    Sku,
    Deployment,
    DeploymentModel,
    DeploymentProperties
)

print('=' * 70)
print('RESILIENT AI FOUNDRY DEPLOYMENT')
print('=' * 70)
print()

# Load credentials
credentials_file = '.azure-credentials.env'
credential = None
subscription_id = None

if os.path.exists(credentials_file):
    load_dotenv(credentials_file)
    tenant_id = os.getenv('AZURE_TENANT_ID')
    client_id = os.getenv('AZURE_CLIENT_ID')
    client_secret = os.getenv('AZURE_CLIENT_SECRET')
    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')

    if all([tenant_id, client_id, client_secret, subscription_id]):
        credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        print('[OK] Using Service Principal credentials')
else:
    credential = AzureCliCredential()
    subscription_id = 'd334f2cd-3efd-494e-9fd3-2470b1a13e4c'
    print('[OK] Using Azure CLI credentials')

# Configuration
resource_group = 'lab-master-lab'
resource_suffix = 'pavavy6pu5hpa'  # Use existing suffix

# AI Foundry Hubs Configuration
foundries = [
    {'name': f'foundry1-{resource_suffix}', 'location': 'uksouth'},
    {'name': f'foundry2-{resource_suffix}', 'location': 'swedencentral'},
    {'name': f'foundry3-{resource_suffix}', 'location': 'westeurope'}
]

# Model Configuration - ONLY stable, widely available models
models_config = {
    'foundry1': [
        {'name': 'gpt-4o-mini', 'format': 'OpenAI', 'version': '2024-07-18', 'sku': 'GlobalStandard', 'capacity': 100},
        {'name': 'gpt-4o', 'format': 'OpenAI', 'version': '2024-08-06', 'sku': 'GlobalStandard', 'capacity': 100},
        {'name': 'text-embedding-3-small', 'format': 'OpenAI', 'version': '1', 'sku': 'GlobalStandard', 'capacity': 20},
        {'name': 'text-embedding-3-large', 'format': 'OpenAI', 'version': '1', 'sku': 'GlobalStandard', 'capacity': 20},
    ],
    'foundry2': [
        {'name': 'gpt-4o-mini', 'format': 'OpenAI', 'version': '2024-07-18', 'sku': 'GlobalStandard', 'capacity': 100},
    ],
    'foundry3': [
        {'name': 'gpt-4o-mini', 'format': 'OpenAI', 'version': '2024-07-18', 'sku': 'GlobalStandard', 'capacity': 100},
    ]
}

# Create Cognitive Services client
client = CognitiveServicesManagementClient(credential, subscription_id)

print()
print('=' * 70)
print('PHASE 1: CHECK/CREATE AI FOUNDRY HUBS')
print('=' * 70)
print()

# Check existing accounts
existing_accounts = {acc.name: acc for acc in client.accounts.list_by_resource_group(resource_group)}

for foundry in foundries:
    foundry_name = foundry['name']
    location = foundry['location']

    print(f'[*] Checking: {foundry_name}')

    if foundry_name in existing_accounts:
        account = existing_accounts[foundry_name]
        state = account.properties.provisioning_state
        print(f'    [OK] Already exists (State: {state})')
    else:
        print(f'    [*] Creating in {location}...')
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

            poller = client.accounts.begin_create(resource_group, foundry_name, account_params)
            account = poller.result(timeout=300)
            print(f'    [OK] Created successfully')
        except Exception as e:
            print(f'    [ERROR] Failed to create: {e}')
            continue

print()
print('=' * 70)
print('PHASE 2: DEPLOY MODELS (RESILIENT)')
print('=' * 70)
print()

deployment_results = {
    'succeeded': [],
    'failed': [],
    'skipped': []
}

for foundry in foundries:
    foundry_name = foundry['name']
    short_name = foundry_name.split('-')[0]  # foundry1, foundry2, foundry3
    models = models_config.get(short_name, [])

    print(f'[*] Foundry: {foundry_name} ({len(models)} models)')
    print()

    for model in models:
        model_name = model['name']
        print(f'  [*] Deploying: {model_name}...')

        try:
            # Check if deployment already exists
            try:
                existing = client.deployments.get(resource_group, foundry_name, model_name)
                if existing.properties.provisioning_state == 'Succeeded':
                    print(f'      [OK] Already deployed (skipping)')
                    deployment_results['skipped'].append(f'{foundry_name}/{model_name}')
                    continue
            except:
                pass  # Doesn't exist, proceed with deployment

            # Create deployment
            deployment_params = Deployment(
                sku=Sku(name=model['sku'], capacity=model['capacity']),
                properties=DeploymentProperties(
                    model=DeploymentModel(
                        format=model['format'],
                        name=model['name'],
                        version=model['version']
                    )
                )
            )

            poller = client.deployments.begin_create_or_update(
                resource_group,
                foundry_name,
                model_name,
                deployment_params
            )

            # Poll with timeout
            result = poller.result(timeout=600)  # 10 minute timeout per model

            print(f'      [OK] Deployed successfully')
            deployment_results['succeeded'].append(f'{foundry_name}/{model_name}')

        except Exception as e:
            error_msg = str(e)
            print(f'      [SKIP] Failed: {error_msg[:100]}...')
            deployment_results['failed'].append({
                'model': f'{foundry_name}/{model_name}',
                'error': error_msg
            })
            continue  # Continue with next model

    print()

print()
print('=' * 70)
print('DEPLOYMENT SUMMARY')
print('=' * 70)
print()

print(f'[OK] Succeeded: {len(deployment_results["succeeded"])} models')
for model in deployment_results['succeeded']:
    print(f'  + {model}')

print()
print(f'[*] Skipped: {len(deployment_results["skipped"])} models (already deployed)')
for model in deployment_results['skipped']:
    print(f'  o {model}')

if deployment_results['failed']:
    print()
    print(f'[!] Failed: {len(deployment_results["failed"])} models')
    for item in deployment_results['failed']:
        print(f'  x {item["model"]}')
        print(f'    Error: {item["error"][:150]}')

print()
print('=' * 70)
print(f'Total: {len(deployment_results["succeeded"]) + len(deployment_results["skipped"])} models deployed')
print(f'Failed: {len(deployment_results["failed"])} models')
print('=' * 70)

# Save results to file
results_file = 'deployment-results.json'
with open(results_file, 'w') as f:
    json.dump(deployment_results, f, indent=2)
print(f'[OK] Results saved to {results_file}')
