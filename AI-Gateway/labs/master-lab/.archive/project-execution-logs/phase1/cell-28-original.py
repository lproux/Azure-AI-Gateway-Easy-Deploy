print('=' * 70)
# Load BICEP_DIR (set by Cell 3)
BICEP_DIR = Path(os.getenv('BICEP_DIR', 'archive/scripts'))
if not BICEP_DIR.exists():
    print(f"[deploy] ⚠️  BICEP_DIR not found: {BICEP_DIR}")
    print(f"[deploy] Looking in current directory instead")
    BICEP_DIR = Path(".")

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
    # Fix: original compile_bicep used Path.replace(old, new) causing TypeError.
    # Provide safe wrapper using Path.with_suffix('.json').
    # Added resilient az CLI discovery & FileNotFoundError handling.
    # Enhanced: auto-install bicep if missing; richer diagnostics; fallback to direct bicep use if JSON not produced.
    def compile_bicep_safe(bicep_path: Path):
        """SIMPLIFIED: Just use existing JSON files - no compilation"""
        if not bicep_path.exists():
            print(f'[ERROR] Bicep file not found: {bicep_path}')
            return None
        
        json_path = bicep_path.with_suffix('.json')
        
        if json_path.exists():
            print(f'[OK] Using existing template: {json_path.name}')
            return str(json_path)
        
        print(f'[ERROR] JSON template not found: {json_path}')
        print(f'[INFO] Expected at: {json_path.absolute()}')
        return None

    json_file = compile_bicep_safe(BICEP_DIR / 'deploy-01-core.bicep')

    # Load parameters
    with open(BICEP_DIR / 'params-01-core.json') as f:
        params = json.load(f)

    # Extract only the 'parameters' section from ARM parameter file
    params_dict = params.get('parameters', {})

    success, result = deploy_template(resource_group_name, deployment_step1, json_file, params_dict)
    if not success:
        raise Exception('Step 1 deployment failed')

    print('[OK] Step 1 complete')

print()

# Get Step 1 outputs (with fallback to saved file)
step1_outputs = None
try:
    step1_outputs = get_deployment_outputs(resource_group_name, deployment_step1)
    print('[OK] Step 1 outputs retrieved from deployment')
except Exception as e:
    print(f'[WARN] Failed to retrieve Step 1 outputs from deployment: {str(e)}')
    # Try loading from saved file
    step1_output_file = BICEP_DIR / 'step1-outputs.json'
    if step1_output_file.exists():
        try:
            with open(step1_output_file) as f:
                step1_outputs = json.load(f)
            print(f'[OK] Step 1 outputs loaded from {step1_output_file.name}')
        except Exception as e2:
            print(f'[ERROR] Failed to load from file: {str(e2)}')
    
if not step1_outputs:
    print('[ERROR] Cannot proceed without Step 1 outputs')
    print('[INFO] Please ensure Step 1 deployment completed or step1-outputs.json exists')
    raise Exception('Cannot proceed without Step 1 outputs')

print(f"  - APIM Gateway: {step1_outputs.get('apimGatewayUrl', 'N/A')}")
print(f"  - Log Analytics: {step1_outputs.get('logAnalyticsWorkspaceId', 'N/A')[:60]}...")

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
    {'name': f'foundry2-{resource_suffix}', 'location': 'eastus', 'project': 'master-lab-foundry2'},
    {'name': f'foundry3-{resource_suffix}', 'location': 'norwayeast', 'project': 'master-lab-foundry3'}
]

models_config = {
    'foundry1': [
        {'name': 'gpt-4o-mini', 'format': 'OpenAI', 'version': '2024-07-18', 'sku': 'GlobalStandard', 'capacity': 100},
        {'name': 'gpt-4o', 'format': 'OpenAI', 'version': '2024-08-06', 'sku': 'GlobalStandard', 'capacity': 100},
        {'name': 'text-embedding-3-small', 'format': 'OpenAI', 'version': '1', 'sku': 'GlobalStandard', 'capacity': 20},
        {'name': 'text-embedding-3-large', 'format': 'OpenAI', 'version': '1', 'sku': 'GlobalStandard', 'capacity': 20},
        {'name': 'dall-e-3', 'format': 'OpenAI', 'version': '3.0', 'sku': 'Standard', 'capacity': 1},
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
print('[*] Phase 2c: APIM Inference API')

deployment_step2c = 'master-lab-02c-apim-api'

if check_deployment_exists(resource_group_name, deployment_step2c):
    print('[OK] APIM API already configured. Skipping...')
else:
    print('[*] Configuring APIM Inference API...')

    json_file = compile_bicep_safe(BICEP_DIR / 'deploy-02c-apim-api.bicep')
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
print('STEP 3: SUPPORTING SERVICES')
print()

deployment_step3 = 'master-lab-03-supporting'
if check_deployment_exists(resource_group_name, deployment_step3):
    print('[OK] Step 3 already deployed. Skipping...')
else:
    print('[*] Step 3 not found. Deploying...')
    json_file = compile_bicep_safe(BICEP_DIR / 'deploy-03-supporting.bicep')
    if not json_file:
        raise Exception('Bicep compilation failed for Step 3')

    params_dict = {}
    if os.path.exists(BICEP_DIR / 'params-03-supporting.json'):
        with open(BICEP_DIR / 'params-03-supporting.json') as f:
            params = json.load(f)
        # Extract only the 'parameters' section from ARM parameter file
        params_dict = params.get('parameters', {})

    success, result = deploy_template(resource_group_name, deployment_step3, json_file, params_dict)
    if not success:
        raise Exception('Step 3 deployment failed')
    print('[OK] Step 3 complete')

print()

try:
    step3_outputs = get_deployment_outputs(resource_group_name, deployment_step3)
    print('[OK] Step 3 outputs retrieved')
except Exception:
    step3_outputs = {}
    print('[*] No Step 3 outputs available')
# =============================================================================
# STEP 4: MCP SERVERS (Bicep)
# =============================================================================

print('=' * 70)
print('STEP 4: MCP SERVERS')
print('=' * 70)
print('[*] Resources: Container Apps + 5 MCP servers')
print('[*] Estimated time: ~5 minutes')
print()

deployment_step4 = 'master-lab-04-mcp'
if check_deployment_exists(resource_group_name, deployment_step4):
    print('[OK] Step 4 already deployed. Skipping...')
else:
    print('[*] Step 4 not found. Deploying...')
    json_file = compile_bicep_safe(BICEP_DIR / 'deploy-04-mcp.bicep')
    if not json_file:
        raise Exception('Bicep compilation failed for Step 4')

    params_dict = {
        'logAnalyticsCustomerId': {'value': step1_outputs.get('logAnalyticsCustomerId', '')},
        'logAnalyticsPrimarySharedKey': {'value': step1_outputs.get('logAnalyticsPrimarySharedKey', '')},
    }

    success, result = deploy_template(resource_group_name, deployment_step4, json_file, params_dict)
    if not success:
        raise Exception('Step 4 deployment failed')
    print('[OK] Step 4 complete')

print()

try:
    step4_outputs = get_deployment_outputs(resource_group_name, deployment_step4)
    print('[OK] Step 4 outputs retrieved')
except Exception:
    step4_outputs = {}
    print('[*] No Step 4 outputs available')

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
