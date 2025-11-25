#!/usr/bin/env python3
"""
Check for failed model deployments that might be blocking deployment
"""

import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential, AzureCliCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient

print('=' * 70)
print('CHECK FAILED MODEL DEPLOYMENTS')
print('=' * 70)
print()

# Load credentials
credentials_file = '.azure-credentials.env'
credential = None

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

# Create client
client = CognitiveServicesManagementClient(credential, subscription_id)
resource_group = 'lab-master-lab'

print(f'[*] Checking resource group: {resource_group}')
print()

# Get all Cognitive Services accounts
try:
    accounts = list(client.accounts.list_by_resource_group(resource_group))
    foundry_accounts = [a for a in accounts if a.name.startswith('foundry')]

    print(f'[OK] Found {len(foundry_accounts)} AI Foundry account(s)')
    print()

    for account in foundry_accounts:
        print(f'[*] Checking: {account.name}')
        print(f'    Location: {account.location}')
        print(f'    State: {account.properties.provisioning_state}')

        # Get model deployments
        try:
            deployments = list(client.deployments.list(resource_group, account.name))
            print(f'    Deployments: {len(deployments)} found')

            if deployments:
                for dep in deployments:
                    state = dep.properties.provisioning_state
                    model = dep.properties.model.name if dep.properties.model else 'unknown'
                    status_icon = '✓' if state == 'Succeeded' else '✗' if state == 'Failed' else '⏳'
                    print(f'      {status_icon} {dep.name}: {model} ({state})')

                    if state == 'Failed':
                        print(f'         [WARNING] Failed deployment detected!')
                        print(f'         [*] To fix: Delete this deployment and re-run Cell 17')
                        print(f'         [*] Command: az cognitiveservices account deployment delete \\')
                        print(f'                        --name {account.name} \\')
                        print(f'                        --resource-group {resource_group} \\')
                        print(f'                        --deployment-name {dep.name}')
        except Exception as e:
            print(f'    [ERROR] Could not list deployments: {e}')

        print()

except Exception as e:
    print(f'[ERROR] Failed to check accounts: {e}')
    print()
    import traceback
    traceback.print_exc()
