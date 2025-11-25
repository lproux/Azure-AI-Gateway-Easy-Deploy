#!/usr/bin/env python3
"""
Deploy APIM Inference API Configuration
Step 2c: Configure APIM API for AI Foundry backend pool
"""

import os
import json
import subprocess
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential, AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode, Deployment, DeploymentProperties

print('=' * 70)
print('DEPLOY APIM INFERENCE API CONFIGURATION')
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
deployment_name = 'master-lab-02c-apim-api'
bicep_file = 'deploy-02c-apim-api.bicep'
json_file = 'deploy-02c-apim-api.json'

# Step 1 outputs (from previous deployment)
step1_outputs_file = 'step1-outputs.json'
if os.path.exists(step1_outputs_file):
    with open(step1_outputs_file) as f:
        step1_outputs = json.load(f)
    print('[OK] Loaded Step 1 outputs from file')
else:
    # Get from deployment if file doesn't exist
    print('[*] Retrieving Step 1 outputs...')
    resource_client = ResourceManagementClient(credential, subscription_id)
    step1_deployment = resource_client.deployments.get(resource_group, 'master-lab-01-core')
    step1_outputs = {k: v['value'] for k, v in step1_deployment.properties.outputs.items()}

    # Save for future use
    with open(step1_outputs_file, 'w') as f:
        json.dump(step1_outputs, f, indent=2)
    print('[OK] Step 1 outputs saved to file')

print()
print('[*] APIM Logger ID:', step1_outputs['apimLoggerId'][:60] + '...')
print('[*] App Insights ID:', step1_outputs['appInsightsId'][:60] + '...')
print()

# Compile Bicep to JSON
print('[*] Compiling Bicep file...')
result = subprocess.run(
    f'az bicep build --file {bicep_file}',
    shell=True,
    capture_output=True,
    text=True,
    cwd=os.getcwd()
)

if result.returncode != 0:
    print(f'[ERROR] Bicep compilation failed: {result.stderr}')
    exit(1)

print('[OK] Compiled successfully')

# Load template
with open(json_file) as f:
    template = json.load(f)

# Build parameters
parameters = {
    'apimLoggerId': {'value': step1_outputs['apimLoggerId']},
    'appInsightsId': {'value': step1_outputs['appInsightsId']},
    'appInsightsInstrumentationKey': {'value': step1_outputs['appInsightsInstrumentationKey']},
    'inferenceAPIPath': {'value': 'inference'},
    'inferenceAPIType': {'value': 'AzureOpenAI'}
}

print()
print('[*] Starting deployment...')
print(f'    Deployment: {deployment_name}')
print(f'    Resource Group: {resource_group}')
print()

# Create deployment
resource_client = ResourceManagementClient(credential, subscription_id)

deployment_properties = DeploymentProperties(
    mode=DeploymentMode.incremental,
    template=template,
    parameters=parameters
)

deployment_async = resource_client.deployments.begin_create_or_update(
    resource_group,
    deployment_name,
    Deployment(properties=deployment_properties)
)

print('[*] Deployment in progress...')

# Poll with progress updates
import time
start_time = time.time()
last_update = start_time

while not deployment_async.done():
    time.sleep(30)
    elapsed = time.time() - start_time

    if time.time() - last_update >= 60:
        mins = int(elapsed / 60)
        secs = int(elapsed % 60)
        print(f'[*] Still deploying... {mins}m {secs}s elapsed')
        last_update = time.time()

# Get result
deployment_result = deployment_async.result()
elapsed = time.time() - start_time
mins = int(elapsed / 60)
secs = int(elapsed % 60)

if deployment_result.properties.provisioning_state == 'Succeeded':
    print(f'[OK] Deployment succeeded in {mins}m {secs}s')
    print()
    print('=' * 70)
    print('APIM INFERENCE API CONFIGURED SUCCESSFULLY')
    print('=' * 70)
    print()
    print('[OK] API Path: /inference')
    print('[OK] Backend: 3 AI Foundry hubs with priority-based load balancing')
    print('[OK] Priority 1: UK South (weight: 100)')
    print('[OK] Priority 2: Sweden Central + West Europe (weight: 50 each)')
    print()

    # Save outputs
    if deployment_result.properties.outputs:
        outputs = {k: v['value'] for k, v in deployment_result.properties.outputs.items()}
        with open('step2c-outputs.json', 'w') as f:
            json.dump(outputs, f, indent=2)
        print('[OK] Outputs saved to step2c-outputs.json')
else:
    print(f'[ERROR] Deployment failed: {deployment_result.properties.provisioning_state}')
    if deployment_result.properties.error:
        print(f'[ERROR] Error: {deployment_result.properties.error.message}')
    exit(1)
