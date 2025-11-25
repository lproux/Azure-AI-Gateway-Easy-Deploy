from pathlib import Path

# --- OPTIONAL BICEP-BASED STEP 2 (AI FOUNDRY ACCOUNTS) ---
print("\n" + "="*70)
print("BICEP STEP 2: AI Foundry Accounts (Infra-as-Code Option)")
print("="*70 + "\n")

# Fallbacks if prior cell not executed
if 'resource_group_name' not in globals():
    resource_group_name = os.getenv('RESOURCE_GROUP', 'lab-master-lab')
if 'foundry_suffix' not in globals():
    foundry_suffix = 'pavavy6pu5hpa'
if 'BICEP_DIR' not in globals():
    BICEP_DIR = Path(os.getenv('BICEP_DIR', 'archive/scripts'))

# WSL path normalization (if running under /mnt and windows-style root was set)
if 'LAB_ROOT' in globals():
    try:
        lr = str(LAB_ROOT)
        if lr[1:3] == ':\\':  # windows drive
            drive = lr[0].lower()
            wsl_path = "/mnt/" + drive + "/" + lr[3:].replace("\\", "/")
            if not BICEP_DIR.exists():
                alt = Path(wsl_path) / 'archive/scripts'
                if alt.exists():
                    BICEP_DIR = alt
    except Exception:
        pass

if 'compile_bicep_safe' not in globals():
    def compile_bicep_safe(bicep_path):
        b = Path(bicep_path)
        if not b.exists():
            print(f'[ERROR] Missing bicep: {b}')
            return None
        json_path = b.with_suffix('.json')
        if json_path.exists():
            print(f'[OK] Using precompiled: {json_path.name}')
            return str(json_path)
        if 'compile_bicep' in globals():
            try:
                print('[*] Precompiled JSON not found; fallback compile_bicep()')
                return compile_bicep(str(b))
            except Exception as e:
                print(f'[ERROR] compile_bicep() failed: {e}')
        print(f'[ERROR] No JSON + no fallback: {json_path}')
        return None

bicep_foundry_deployment = 'master-lab-02-foundry'

if check_deployment_exists(resource_group_name, bicep_foundry_deployment):
    print('[OK] Foundry Bicep deployment already exists – skipping.')
else:
    print('[*] Deploying foundry accounts via Bicep...')
    template_candidate = BICEP_DIR / 'deploy-02-foundry.bicep'
    template_file = compile_bicep_safe(template_candidate)
    if not template_file:
        print(f"[WARN] Bicep template or precompiled JSON not found at: {template_candidate}")
        print("[WARN] Skipping Bicep deployment and relying on previously created Python-based foundry resources.")
    else:
        params_dict = {
            'resourceSuffix': {'value': foundry_suffix},
            # Optional custom config example:
            # 'foundryConfig': {'value': [
            #     {'name': 'foundry1', 'location': 'uksouth'},
            #     {'name': 'foundry2', 'location': 'eastus'},
            #     {'name': 'foundry3', 'location': 'norwayeast'}
            # ]}
        }
        success, _ = deploy_template(resource_group_name, bicep_foundry_deployment, template_file, params_dict)
        if not success:
            print('[WARN] Foundry Bicep deployment failed – continuing without Bicep deployment.')
        else:
            print('[OK] Foundry accounts deployed via Bicep')

# Outputs (graceful fallback to existing_accounts if Bicep outputs unavailable)
try:
    foundry_outputs = get_deployment_outputs(resource_group_name, bicep_foundry_deployment)
    print('[OK] Foundry outputs retrieved')
    accounts = foundry_outputs.get('foundryAccounts', [])
    if isinstance(accounts, list):
        print('\n[Foundry Accounts]')
        for a in accounts:
            print(f"  - {a.get('name')} @ {a.get('location')} -> {a.get('endpoint')}")
    else:
        print('[WARN] foundryAccounts output missing or wrong type')
except Exception as e:
    print('[WARN] Could not retrieve foundry outputs:', str(e)[:160])
    if 'existing_accounts' in globals() and existing_accounts:
        print('[INFO] Falling back to existing_accounts already provisioned:')
        for name, acct_obj in existing_accounts.items():
            try:
                loc = getattr(acct_obj, 'location', 'unknown')
                endpoint = getattr(acct_obj.properties, 'endpoint', None) or getattr(acct_obj.properties, 'apiEndpoint', '')
                print(f"  - {name} @ {loc} -> {endpoint}")
            except Exception:
                print(f"  - {name}")
    else:
        print('[INFO] No existing_accounts fallback available.')