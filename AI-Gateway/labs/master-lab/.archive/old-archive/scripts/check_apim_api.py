#!/usr/bin/env python3
"""
Check if APIM inference API exists and is configured
"""

import json
from pathlib import Path
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.mgmt.apimanagement import ApiManagementClient
import os

# Load credentials from environment
subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
tenant_id = os.getenv('AZURE_TENANT_ID', '')
client_id = os.getenv('AZURE_CLIENT_ID', '')
client_secret = os.getenv('AZURE_CLIENT_SECRET', '')

# Load from step1 outputs if not in env
if not subscription_id and Path('step1-outputs.json').exists():
    with open('step1-outputs.json') as f:
        step1 = json.load(f)
        for key, value in step1.items():
            if isinstance(value, str) and '/subscriptions/' in value:
                subscription_id = value.split('/subscriptions/')[1].split('/')[0]
                break

print(f'Subscription ID: {subscription_id}')

# Get credentials
if client_id and client_secret and tenant_id:
    credential = ClientSecretCredential(tenant_id, client_id, client_secret)
    print('Using Service Principal')
else:
    credential = DefaultAzureCredential()
    print('Using DefaultAzureCredential')

# APIM details
resource_group = 'lab-master-lab'
apim_name = 'apim-pavavy6pu5hpa'

# Create client
apim_client = ApiManagementClient(credential, subscription_id)

print()
print('=' * 80)
print(f'CHECKING APIM APIs IN {apim_name}')
print('=' * 80)
print()

try:
    # List all APIs
    apis = list(apim_client.api.list_by_service(resource_group, apim_name))

    if not apis:
        print('[!] NO APIS FOUND in APIM!')
        print()
        print('This explains the 404 error!')
        print()
        print('The inference API was NOT deployed to APIM.')
        print('We need to deploy it using the deploy_apim_api.py script.')
    else:
        print(f'[OK] Found {len(apis)} API(s):')
        print()

        for api in apis:
            print(f'API: {api.name}')
            print(f'  Display Name: {api.display_name}')
            print(f'  Path: {api.path}')
            print(f'  Service URL: {api.service_url}')
            print(f'  Protocols: {api.protocols}')
            print()

            # Check if this is the inference API
            if api.path == 'inference' or 'inference' in api.name.lower():
                print('[OK] Found inference API!')
                print(f'  Full URL: https://{apim_name}.azure-api.net/{api.path}')

except Exception as e:
    print(f'[ERROR] Failed to list APIs: {e}')
    import traceback
    traceback.print_exc()

print()
print('=' * 80)
print('DIAGNOSIS')
print('=' * 80)
print()

if not apis:
    print('[ISSUE] The APIM inference API is missing!')
    print()
    print('[FIX STRATEGY]')
    print('  1. Run deploy_apim_api.py to create the inference API')
    print('  2. Configure it to route to the 3 AI Foundry backends')
    print('  3. Set up load balancing and retry policies')
    print()
    print('[COMMAND]')
    print('  python deploy_apim_api.py')
else:
    print('[OK] APIM has APIs configured')
    print('Check if the inference API path matches what the notebook expects')
