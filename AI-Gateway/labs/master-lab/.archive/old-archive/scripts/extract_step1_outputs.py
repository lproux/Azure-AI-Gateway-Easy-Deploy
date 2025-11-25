#!/usr/bin/env python3
"""Extract Step 1 outputs from deployment"""

import os
import json
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential, AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient

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
else:
    credential = AzureCliCredential()
    subscription_id = 'd334f2cd-3efd-494e-9fd3-2470b1a13e4c'

resource_client = ResourceManagementClient(credential, subscription_id)
resource_group = 'lab-master-lab'

print('[*] Retrieving Step 1 outputs...')
step1_deployment = resource_client.deployments.get(resource_group, 'master-lab-01-core')
step1_outputs = {k: v['value'] for k, v in step1_deployment.properties.outputs.items()}

with open('step1-outputs.json', 'w') as f:
    json.dump(step1_outputs, f, indent=2)

print('[OK] Step 1 outputs saved to step1-outputs.json')
print()
for key, value in step1_outputs.items():
    print(f'  - {key}: {str(value)[:60]}...')
