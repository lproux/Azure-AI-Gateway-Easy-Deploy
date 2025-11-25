#!/usr/bin/env python3
"""
Deploy Steps 3 & 4: Supporting Services and MCP Servers
"""

import os
import json
import subprocess
import time
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential, AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode, Deployment, DeploymentProperties

print('=' * 70)
print('DEPLOY STEPS 3 & 4')
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

resource_client = ResourceManagementClient(credential, subscription_id)
resource_group = 'lab-master-lab'

def compile_bicep(bicep_file):
    """Compile Bicep to JSON"""
    json_file = bicep_file.replace('.bicep', '.json')

    # Check if JSON is newer than Bicep
    if os.path.exists(json_file):
        bicep_time = os.path.getmtime(bicep_file)
        json_time = os.path.getmtime(json_file)
        if json_time > bicep_time:
            print(f'[OK] Using existing {json_file}')
            return json_file

    print(f'[*] Compiling {bicep_file}...')
    result = subprocess.run(
        f'az bicep build --file {bicep_file}',
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f'[ERROR] Compilation failed: {result.stderr}')
        return None

    print(f'[OK] Compiled to {json_file}')
    return json_file

def deploy_template(deployment_name, template_file, parameters_dict=None):
    """Deploy ARM template"""
    print(f'[*] Deploying {deployment_name}...')

    # Load template
    with open(template_file) as f:
        template = json.load(f)

    # Create deployment
    deployment_properties = DeploymentProperties(
        mode=DeploymentMode.incremental,
        template=template,
        parameters=parameters_dict or {}
    )

    deployment_async = resource_client.deployments.begin_create_or_update(
        resource_group,
        deployment_name,
        Deployment(properties=deployment_properties)
    )

    print('[*] Deployment in progress...')

    # Poll with progress updates
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

        # Get outputs
        outputs = {}
        if deployment_result.properties.outputs:
            outputs = {k: v['value'] for k, v in deployment_result.properties.outputs.items()}

        return True, outputs
    else:
        print(f'[ERROR] Deployment failed: {deployment_result.properties.provisioning_state}')
        if deployment_result.properties.error:
            print(f'[ERROR] Error: {deployment_result.properties.error.message}')
        return False, {}

def check_deployment_exists(deployment_name):
    """Check if deployment exists and succeeded"""
    try:
        deployment = resource_client.deployments.get(resource_group, deployment_name)
        return deployment.properties.provisioning_state == 'Succeeded'
    except:
        return False

print()

# =============================================================================
# STEP 3: SUPPORTING SERVICES
# =============================================================================

print('=' * 70)
print('STEP 3: SUPPORTING SERVICES')
print('=' * 70)
print('[*] Resources: Redis, Search, Cosmos, Content Safety')
print('[*] Estimated time: ~10 minutes')
print()

deployment_step3 = 'master-lab-03-supporting'

if check_deployment_exists(deployment_step3):
    print('[OK] Step 3 already deployed. Skipping...')
    step3_deployment = resource_client.deployments.get(resource_group, deployment_step3)
    step3_outputs = {k: v['value'] for k, v in step3_deployment.properties.outputs.items()} if step3_deployment.properties.outputs else {}
else:
    print('[*] Step 3 not found. Deploying...')

    json_file = compile_bicep('deploy-03-supporting.bicep')
    if not json_file:
        print('[ERROR] Bicep compilation failed for Step 3')
        exit(1)

    # Load parameters if exists
    params_dict = {}
    if os.path.exists('params-03-supporting.json'):
        with open('params-03-supporting.json') as f:
            params_file = json.load(f)

        # Handle Azure parameter file format
        if 'parameters' in params_file:
            params_dict = params_file['parameters']
        else:
            params_dict = {k: {'value': v} for k, v in params_file.items()}

    success, step3_outputs = deploy_template(deployment_step3, json_file, params_dict)
    if not success:
        print('[ERROR] Step 3 deployment failed')
        exit(1)

    print('[OK] Step 3 complete')

# Save Step 3 outputs
with open('step3-outputs.json', 'w') as f:
    json.dump(step3_outputs, f, indent=2)
print('[OK] Step 3 outputs saved')

print()

# =============================================================================
# STEP 4: MCP SERVERS
# =============================================================================

print('=' * 70)
print('STEP 4: MCP SERVERS')
print('=' * 70)
print('[*] Resources: Container Apps + 7 MCP servers')
print('[*] Estimated time: ~5 minutes')
print()

deployment_step4 = 'master-lab-04-mcp'

if check_deployment_exists(deployment_step4):
    print('[OK] Step 4 already deployed. Skipping...')
    step4_deployment = resource_client.deployments.get(resource_group, deployment_step4)
    step4_outputs = {k: v['value'] for k, v in step4_deployment.properties.outputs.items()} if step4_deployment.properties.outputs else {}
else:
    print('[*] Step 4 not found. Deploying...')

    json_file = compile_bicep('deploy-04-mcp.bicep')
    if not json_file:
        print('[ERROR] Bicep compilation failed for Step 4')
        exit(1)

    # Load Step 1 outputs for Log Analytics credentials
    step1_outputs = {}
    if os.path.exists('step1-outputs.json'):
        with open('step1-outputs.json') as f:
            step1_outputs = json.load(f)
        print('[OK] Loaded Step 1 outputs')
    else:
        print('[ERROR] step1-outputs.json not found')
        exit(1)

    # Build parameters from Step 1 and Step 3 outputs
    params_dict = {}

    # Required parameters from Step 1
    if 'logAnalyticsCustomerId' in step1_outputs:
        params_dict['logAnalyticsCustomerId'] = {'value': step1_outputs['logAnalyticsCustomerId']}
    if 'logAnalyticsPrimarySharedKey' in step1_outputs:
        params_dict['logAnalyticsPrimarySharedKey'] = {'value': step1_outputs['logAnalyticsPrimarySharedKey']}

    # Optional parameters from Step 3
    if step3_outputs:
        if 'containerRegistryName' in step3_outputs:
            params_dict['containerRegistryName'] = {'value': step3_outputs['containerRegistryName']}

    success, step4_outputs = deploy_template(deployment_step4, json_file, params_dict)
    if not success:
        print('[ERROR] Step 4 deployment failed')
        exit(1)

    print('[OK] Step 4 complete')

# Save Step 4 outputs
with open('step4-outputs.json', 'w') as f:
    json.dump(step4_outputs, f, indent=2)
print('[OK] Step 4 outputs saved')

print()
print('=' * 70)
print('DEPLOYMENT COMPLETE')
print('=' * 70)
print('[OK] Step 3: Supporting Services - DEPLOYED')
print('[OK] Step 4: MCP Servers - DEPLOYED')
print()
print('[NEXT] Run regenerate_env.py to update master-lab.env with all values')
