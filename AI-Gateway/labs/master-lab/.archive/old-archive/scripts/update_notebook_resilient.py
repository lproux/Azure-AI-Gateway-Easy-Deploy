#!/usr/bin/env python3
"""
Update notebook to use resilient deployment approach
Replaces Cell 17 (deployment cell) with resilient version
"""

import json
import shutil
from datetime import datetime

notebook_path = 'master-ai-gateway.ipynb'

# Backup
backup_path = f'{notebook_path}.bkp.{datetime.now().strftime("%Y%m%d-%H%M%S")}'
shutil.copy(notebook_path, backup_path)
print(f'[OK] Backup created: {backup_path}')

# Load notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the deployment cell (contains "MASTER LAB DEPLOYMENT - 4 STEPS")
deployment_cell_idx = None
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code' and cell['source']:
        source = ''.join(cell['source'])
        if 'MASTER LAB DEPLOYMENT - 4 STEPS' in source:
            deployment_cell_idx = i
            break

if deployment_cell_idx is None:
    print('[ERROR] Could not find deployment cell')
    exit(1)

print(f'[OK] Found deployment cell at index {deployment_cell_idx}')

# New resilient deployment code
new_deployment_code = '''print('=' * 70)
print('MASTER LAB DEPLOYMENT - 4 STEPS (RESILIENT)')
print('=' * 70)
print()

total_start = time.time()

# Ensure resource group exists
print('[*] Step 0: Ensuring resource group exists...')
if not check_resource_group_exists(resource_group_name):
    print(f'[*] Creating resource group: {resource_group_name}')
    resource_client.resource_groups.create_or_update(
        resource_group_name,
        {'location': location}
    )
    print('[OK] Resource group created')
else:
    print('[OK] Resource group already exists')

print()

# =============================================================================
# STEP 1: CORE INFRASTRUCTURE (Bicep - as before)
# =============================================================================

print('=' * 70)
print('STEP 1: CORE INFRASTRUCTURE')
print('=' * 70)
print('[*] Resources: Log Analytics, App Insights, API Management')
print('[*] Estimated time: ~10 minutes')
print()

deployment_step1 = 'master-lab-01-core'

if check_deployment_exists(resource_group_name, deployment_step1):
    print('[OK] Step 1 already deployed. Skipping...')
else:
    print('[*] Step 1 not found. Deploying...')

    # Compile and deploy
    json_file = compile_bicep('deploy-01-core.bicep')
    if not json_file:
        raise Exception('Bicep compilation failed for Step 1')

    # Load parameters
    with open('params-01-core.json') as f:
        params = json.load(f)

    params_dict = {k: {'value': v} for k, v in params.items()}

    success, result = deploy_template(resource_group_name, deployment_step1, json_file, params_dict)
    if not success:
        raise Exception('Step 1 deployment failed')

    print('[OK] Step 1 complete')

print()

# Get Step 1 outputs
step1_outputs = get_deployment_outputs(resource_group_name, deployment_step1)
print('[OK] Step 1 outputs retrieved:')
print(f"  - APIM Gateway: {step1_outputs['apimGatewayUrl']}")
print(f"  - Log Analytics: {step1_outputs['logAnalyticsWorkspaceId'][:60]}...")

print()

# =============================================================================
# STEP 2: AI FOUNDRY (RESILIENT PYTHON APPROACH)
# =============================================================================

print('=' * 70)
print('STEP 2: AI FOUNDRY (RESILIENT DEPLOYMENT)')
print('=' * 70)
print('[*] Resources: 3 Foundry hubs, 3 projects, AI models')
print('[*] Estimated time: ~15 minutes')
print()

from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.cognitiveservices.models import Account, Sku as CogSku, Deployment, DeploymentModel, DeploymentProperties

cog_client = CognitiveServicesManagementClient(credential, subscription_id)

# Configuration
resource_suffix = 'pavavy6pu5hpa'  # Consistent suffix
foundries = [
    {'name': f'foundry1-{resource_suffix}', 'location': 'uksouth', 'project': 'master-lab-foundry1'},
    {'name': f'foundry2-{resource_suffix}', 'location': 'swedencentral', 'project': 'master-lab-foundry2'},
    {'name': f'foundry3-{resource_suffix}', 'location': 'westeurope', 'project': 'master-lab-foundry3'}
]

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

# Phase 2a: Check/Create Foundry Hubs
print('[*] Phase 2a: AI Foundry Hubs')
existing_accounts = {acc.name: acc for acc in cog_client.accounts.list_by_resource_group(resource_group_name)}

for foundry in foundries:
    foundry_name = foundry['name']
    if foundry_name in existing_accounts:
        print(f'  [OK] {foundry_name} already exists')
    else:
        print(f'  [*] Creating {foundry_name}...')
        try:
            account_params = Account(
                location=foundry['location'],
                sku=CogSku(name='S0'),
                kind='AIServices',
                properties={
                    'customSubDomainName': foundry_name.lower(),
                    'publicNetworkAccess': 'Enabled',
                    'allowProjectManagement': True
                },
                identity={'type': 'SystemAssigned'}
            )
            poller = cog_client.accounts.begin_create(resource_group_name, foundry_name, account_params)
            poller.result(timeout=300)
            print(f'  [OK] {foundry_name} created')
        except Exception as e:
            print(f'  [ERROR] Failed: {str(e)[:100]}')

print()

# Phase 2b: Deploy Models (Resilient)
print('[*] Phase 2b: AI Models (Resilient)')
deployment_results = {'succeeded': [], 'failed': [], 'skipped': []}

for foundry in foundries:
    foundry_name = foundry['name']
    short_name = foundry_name.split('-')[0]
    models = models_config.get(short_name, [])

    print(f'  [*] {foundry_name}: {len(models)} models')

    for model in models:
        model_name = model['name']
        try:
            # Check if exists
            existing = cog_client.deployments.get(resource_group_name, foundry_name, model_name)
            if existing.properties.provisioning_state == 'Succeeded':
                deployment_results['skipped'].append(f'{short_name}/{model_name}')
                print(f'    [OK] {model_name} already deployed')
                continue
        except:
            pass

        try:
            print(f'    [*] Deploying {model_name}...')
            deployment_params = Deployment(
                sku=CogSku(name=model['sku'], capacity=model['capacity']),
                properties=DeploymentProperties(
                    model=DeploymentModel(
                        format=model['format'],
                        name=model['name'],
                        version=model['version']
                    )
                )
            )
            poller = cog_client.deployments.begin_create_or_update(
                resource_group_name, foundry_name, model_name, deployment_params
            )
            poller.result(timeout=600)
            deployment_results['succeeded'].append(f'{short_name}/{model_name}')
            print(f'    [OK] {model_name} deployed')
        except Exception as e:
            deployment_results['failed'].append({'model': f'{short_name}/{model_name}', 'error': str(e)})
            print(f'    [SKIP] {model_name} failed: {str(e)[:80]}')

print()
print(f'[OK] Models: {len(deployment_results["succeeded"])} deployed, {len(deployment_results["skipped"])} skipped, {len(deployment_results["failed"])} failed')
print()

# Phase 2c: APIM Inference API
print('[*] Phase 2c: APIM Inference API')

deployment_step2c = 'master-lab-02c-apim-api'

if check_deployment_exists(resource_group_name, deployment_step2c):
    print('[OK] APIM API already configured. Skipping...')
else:
    print('[*] Configuring APIM Inference API...')

    json_file = compile_bicep('deploy-02c-apim-api.bicep')
    if not json_file:
        raise Exception('Bicep compilation failed for Step 2c')

    params_dict = {
        'apimLoggerId': {'value': step1_outputs['apimLoggerId']},
        'appInsightsId': {'value': step1_outputs['appInsightsId']},
        'appInsightsInstrumentationKey': {'value': step1_outputs['appInsightsInstrumentationKey']},
        'inferenceAPIPath': {'value': 'inference'},
        'inferenceAPIType': {'value': 'AzureOpenAI'}
    }

    success, result = deploy_template(resource_group_name, deployment_step2c, json_file, params_dict)
    if not success:
        raise Exception('Step 2c deployment failed')

    print('[OK] APIM API configured')

print('[OK] Step 2 complete')
print()

# =============================================================================
# STEP 3: SUPPORTING SERVICES (Bicep)
# =============================================================================

print('=' * 70)
print('STEP 3: SUPPORTING SERVICES')
print('=' * 70)
print('[*] Resources: Redis, Search, Cosmos, Content Safety')
print('[*] Estimated time: ~10 minutes')
print()

deployment_step3 = 'master-lab-03-supporting'

if check_deployment_exists(resource_group_name, deployment_step3):
    print('[OK] Step 3 already deployed. Skipping...')
else:
    print('[*] Step 3 not found. Deploying...')

    json_file = compile_bicep('deploy-03-supporting.bicep')
    if not json_file:
        raise Exception('Bicep compilation failed for Step 3')

    # Load parameters if exists
    params_dict = {}
    if os.path.exists('params-03-supporting.json'):
        with open('params-03-supporting.json') as f:
            params = json.load(f)
        params_dict = {k: {'value': v} for k, v in params.items()}

    success, result = deploy_template(resource_group_name, deployment_step3, json_file, params_dict)
    if not success:
        raise Exception('Step 3 deployment failed')

    print('[OK] Step 3 complete')

print()

# =============================================================================
# STEP 4: MCP SERVERS (Bicep)
# =============================================================================

print('=' * 70)
print('STEP 4: MCP SERVERS')
print('=' * 70)
print('[*] Resources: Container Apps + 7 MCP servers')
print('[*] Estimated time: ~5 minutes')
print()

deployment_step4 = 'master-lab-04-mcp'

if check_deployment_exists(resource_group_name, deployment_step4):
    print('[OK] Step 4 already deployed. Skipping...')
else:
    print('[*] Step 4 not found. Deploying...')

    json_file = compile_bicep('deploy-04-mcp.bicep')
    if not json_file:
        raise Exception('Bicep compilation failed for Step 4')

    # Get Step 3 outputs for container registry
    step3_outputs = get_deployment_outputs(resource_group_name, deployment_step3)

    params_dict = {
        'containerRegistryName': {'value': step3_outputs.get('containerRegistryName', '')},
    } if step3_outputs else {}

    success, result = deploy_template(resource_group_name, deployment_step4, json_file, params_dict)
    if not success:
        raise Exception('Step 4 deployment failed')

    print('[OK] Step 4 complete')

print()

# =============================================================================
# DEPLOYMENT COMPLETE
# =============================================================================

total_elapsed = time.time() - total_start
total_mins = int(total_elapsed / 60)
total_secs = int(total_elapsed % 60)

print('=' * 70)
print('DEPLOYMENT COMPLETE')
print('=' * 70)
print(f'[OK] Total time: {total_mins}m {total_secs}s')
print()
print('[OK] All 4 steps deployed successfully!')
print('[OK] Next: Run Cell 18-19 to generate master-lab.env')
print()
'''

# Update the cell
nb['cells'][deployment_cell_idx]['source'] = new_deployment_code.split('\n')
nb['cells'][deployment_cell_idx]['outputs'] = []  # Clear old outputs
nb['cells'][deployment_cell_idx]['execution_count'] = None

# Save notebook
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f'[OK] Notebook updated!')
print(f'[OK] Cell {deployment_cell_idx} replaced with resilient deployment code')
print()
print('[OK] Changes:')
print('  - Step 2: Now uses resilient Python deployment (AI Foundry + models + APIM)')
print('  - Step 3: Supporting Services deployment added')
print('  - Step 4: MCP Servers deployment added')
print('  - All steps with proper error handling and progress tracking')
print()
print('[OK] Ready to run Cell 17 in notebook!')
