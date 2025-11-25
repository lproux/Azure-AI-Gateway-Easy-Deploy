#!/usr/bin/env python3
"""
Fix Azure CLI PATH detection issues in master-ai-gateway.ipynb

This script updates cells that use subprocess with Azure CLI to:
1. Properly detect Azure CLI location (WSL /usr/bin/az vs Windows path)
2. Use explicit PATH with /usr/bin included
3. Add MSAL cache clearing functionality
4. Add diagnostic output for troubleshooting
"""

import json
import sys
from pathlib import Path
from datetime import datetime

NOTEBOOK_PATH = Path(__file__).parent / "master-ai-gateway.ipynb"
BACKUP_PATH = NOTEBOOK_PATH.parent / "archive" / "backups" / f"master-ai-gateway.ipynb.backup-azure-cli-fix-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

# Ensure backup directory exists
BACKUP_PATH.parent.mkdir(parents=True, exist_ok=True)

def load_notebook():
    """Load the notebook"""
    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_notebook(nb):
    """Save the notebook"""
    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f"[SAVE] Notebook saved to {NOTEBOOK_PATH}")

def backup_notebook(nb):
    """Create a backup of the notebook"""
    with open(BACKUP_PATH, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f"[BACKUP] Created backup at {BACKUP_PATH}")

def get_cell_source(cell):
    """Get cell source as string"""
    return ''.join(cell.get('source', []))

def set_cell_source(cell, source):
    """Set cell source from string"""
    # Split into lines but preserve line endings
    lines = source.split('\n')
    # Add newlines back except for last line
    cell['source'] = [line + '\n' for line in lines[:-1]] + ([lines[-1]] if lines[-1] else [])

# New cell sources with fixes

CELL_13_FIXED = '''import os
import json
import subprocess
import shutil
from datetime import datetime

# Azure CLI PATH detection helper
def get_az_cli():
    """Find Azure CLI executable - handles WSL vs Windows paths"""
    # Try shutil.which first (works for WSL /usr/bin/az)
    az_path = shutil.which('az')
    if az_path:
        return az_path

    # Fallback to common locations
    common_paths = [
        '/usr/bin/az',  # WSL/Linux
        r'C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd',  # Windows
    ]

    for path in common_paths:
        if os.path.exists(path):
            return path

    return 'az'  # Fallback to system PATH

def clear_msal_cache():
    """Clear MSAL token cache to fix authentication issues"""
    cache_files = [
        os.path.expanduser('~/.azure/msal_token_cache.json'),
        os.path.expanduser('~/.msal_token_cache.json'),
        os.path.expanduser('~/.azure/msal_http_cache')
    ]

    cleared = []
    for cache_file in cache_files:
        if os.path.exists(cache_file):
            try:
                os.remove(cache_file)
                cleared.append(cache_file)
            except Exception as e:
                print(f'[WARN] Could not remove {cache_file}: {e}')

    if cleared:
        print(f'[INFO] Cleared MSAL cache: {", ".join(cleared)}')

    return len(cleared) > 0

# Prepare environment for subprocess calls
az_cli = get_az_cli()
env = os.environ.copy()
# Ensure /usr/bin is in PATH for WSL
if '/usr/bin' not in env.get('PATH', ''):
    env['PATH'] = f"/usr/bin:{env['PATH']}"

print(f'[INFO] Azure CLI: {az_cli}')
print(f'[INFO] PATH includes /usr/bin: {"/usr/bin" in env.get("PATH", "")}')

# Check if already exists
if os.path.exists('.azure-credentials.env'):
    print('[OK] .azure-credentials.env already exists!')
    print('[OK] Skipping Service Principal creation')
    print('[INFO] Delete .azure-credentials.env if you want to create a new one')
else:
    print('[*] Creating Service Principal...')
    print()

    # Clear MSAL cache before Azure operations
    if clear_msal_cache():
        print('[INFO] Cleared stale MSAL tokens')
        print()

    # Get subscription
    print(f'[*] Running: {az_cli} account show')
    result = subprocess.run(
        [az_cli, 'account', 'show', '--output', 'json'],
        capture_output=True,
        text=True,
        env=env
    )

    if result.returncode != 0:
        print('[ERROR] Failed to get subscription. Make sure you are logged in:')
        print('        az login')
        print(f'[ERROR] {result.stderr}')
    else:
        sub_info = json.loads(result.stdout)
        subscription_id = sub_info['id']

        print(f'[OK] Using subscription: {sub_info["name"]}')
        print()

        # Create Service Principal
        sp_name = f'master-lab-sp-{datetime.now().strftime("%Y%m%d-%H%M%S")}'
        print(f'[*] Creating Service Principal: {sp_name}')
        print('[*] Role: Contributor')
        print()

        result = subprocess.run(
            [
                az_cli, 'ad', 'sp', 'create-for-rbac',
                '--name', sp_name,
                '--role', 'Contributor',
                '--scopes', f'/subscriptions/{subscription_id}',
                '--output', 'json'
            ],
            capture_output=True,
            text=True,
            env=env
        )

        if result.returncode != 0:
            print('[ERROR] Failed to create Service Principal')
            print(f'[ERROR] {result.stderr}')
            print('[INFO] You need permissions to create App Registrations')
        else:
            sp_output = json.loads(result.stdout)

            tenant_id = sp_output['tenant']
            client_id = sp_output['appId']
            client_secret = sp_output['password']

            print('[OK] Service Principal created successfully!')
            print()
            print('Credentials:')
            print(f'  Tenant ID:     {tenant_id}')
            print(f'  Client ID:     {client_id}')
            print(f'  Client Secret: {client_secret[:8]}...')
            print()

            # Create .azure-credentials.env
            env_content = f\'\'\'# Azure Service Principal Credentials
# Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Service Principal: {sp_name}

AZURE_TENANT_ID={tenant_id}
AZURE_CLIENT_ID={client_id}
AZURE_CLIENT_SECRET={client_secret}
AZURE_SUBSCRIPTION_ID={subscription_id}
\'\'\'

            with open('.azure-credentials.env', 'w') as f:
                f.write(env_content)

            print('[OK] Created .azure-credentials.env')
            print('[OK] This file is in .gitignore (safe from commits)')
            print()
            print('[OK] Next: Run Cell 11 (Configuration), then Cell 13 (Helper Functions)')
            print()
            print('To delete this Service Principal later:')
            print(f'  az ad sp delete --id {client_id}')
'''

CELL_42_FIXED = '''# Lab 05: Token-Based Rate Limiting
# This lab demonstrates proper APIM token rate limiting using azure-openai-token-limit policy

import os
import subprocess
import shutil
import time

# Azure CLI PATH detection helper
def get_az_cli():
    """Find Azure CLI executable - handles WSL vs Windows paths"""
    az_path = shutil.which('az')
    if az_path:
        return az_path

    common_paths = [
        '/usr/bin/az',
        r'C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd',
    ]

    for path in common_paths:
        if os.path.exists(path):
            return path

    return 'az'

# Prepare environment
az_cli = get_az_cli()
env = os.environ.copy()
if '/usr/bin' not in env.get('PATH', ''):
    env['PATH'] = f"/usr/bin:{env['PATH']}"

print(f'[INFO] Azure CLI: {az_cli}')

# APIM configuration
apim_service_name = os.getenv('APIM_SERVICE_NAME', 'apim-pavavy6pu5hpa')
resource_group = os.getenv('RESOURCE_GROUP', 'lab-master-lab')
api_id = 'azure-openai-api'

# Token rate limiting policy (50 TPM for testing)
policy_xml = \'\'\'<policies>
    <inbound>
        <base />
        <azure-openai-token-limit
            tokens-per-minute="50"
            counter-key="@(context.Subscription.Id)"
            estimate-prompt-tokens="true"
            tokens-consumed-header-name="consumed-tokens"
            remaining-tokens-header-name="remaining-tokens" />
    </inbound>
    <backend>
        <base />
    </backend>
    <outbound>
        <base />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>\'\'\'

# Save policy to temporary file
policy_file = '/tmp/apim-token-limit-policy.xml'
with open(policy_file, 'w') as f:
    f.write(policy_xml)

# Apply policy using Azure CLI
print('[*] Applying token rate limiting policy to APIM...')
print(f'    Service: {apim_service_name}')
print(f'    Resource Group: {resource_group}')
print(f'    API: {api_id}')
print(f'    Limit: 50 tokens per minute (for testing)')
print()

try:
    # Test Azure CLI availability
    test_result = subprocess.run(
        [az_cli, '--version'],
        capture_output=True,
        text=True,
        env=env,
        timeout=10
    )

    if test_result.returncode != 0:
        raise FileNotFoundError('Azure CLI not working properly')

    print(f'[OK] Azure CLI version check passed')
    print()

    # Apply the policy
    cmd = [
        az_cli, 'apim', 'api', 'policy', 'create',
        '--resource-group', resource_group,
        '--service-name', apim_service_name,
        '--api-id', api_id,
        '--xml-policy', policy_file
    ]

    print(f'[*] Running: {" ".join(cmd)}')
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, env=env)

    if result.returncode == 0:
        print('[SUCCESS] Token rate limiting policy applied!')
        print('[INFO] Policy will take ~30-60 seconds to propagate')
        print('[INFO] Waiting 60 seconds for policy propagation...')
        time.sleep(60)
        print('[OK] Policy should now be active')
    else:
        print(f'[ERROR] Failed to apply policy: {result.stderr}')
        print('[HINT] You may need to apply the policy manually via Azure Portal')
        print('[HINT] Go to: APIM > APIs > azure-openai-api > Policies > Inbound processing')

except FileNotFoundError:
    print('[ERROR] Azure CLI not found')
    print(f'[INFO] Attempted to use: {az_cli}')
    print('[INFO] Falling back to manual policy configuration...')
    print()
    print('Please apply this policy manually via Azure Portal or Azure CLI:')
    print('=' * 80)
    print(policy_xml)
    print('=' * 80)
    print()
    print('Steps:')
    print('1. Go to Azure Portal > API Management')
    print('2. Select your APIM instance')
    print('3. Go to APIs > azure-openai-api')
    print('4. Click "All operations"')
    print('5. In "Inbound processing", click "Code view"')
    print('6. Replace the <inbound> section with the policy above')
    print('7. Save and wait 60 seconds for propagation')
except Exception as e:
    print(f'[ERROR] Unexpected error: {e}')
    print('[HINT] Please apply the policy manually')

print()
print('[NEXT] Run the cell below to test token rate limiting')
'''

CELL_89_FIXED = '''# Azure OpenAI image model deployment via CLI
import os
import re
import json
import subprocess
import shutil
from pathlib import Path

# Azure CLI PATH detection helper
def get_az_cli():
    """Find Azure CLI executable - handles WSL vs Windows paths"""
    az_path = shutil.which('az')
    if az_path:
        return az_path

    common_paths = [
        '/usr/bin/az',
        r'C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd',
    ]

    for path in common_paths:
        if os.path.exists(path):
            return path

    return 'az'

# Prepare environment
az_cli = get_az_cli()
env = os.environ.copy()
if '/usr/bin' not in env.get('PATH', ''):
    env['PATH'] = f"/usr/bin:{env['PATH']}"

print(f'[INFO] Azure CLI: {az_cli}')

# Get configuration
RESOURCE_GROUP = os.getenv("RESOURCE_GROUP", RESOURCE_GROUP if 'RESOURCE_GROUP' in globals() else "")
LOCATION = os.getenv("LOCATION", LOCATION if 'LOCATION' in globals() else "")
endpoint = (os.getenv("azure_endpoint") or os.getenv("OPENAI_ENDPOINT") or globals().get("azure_endpoint") or "").strip()

if not endpoint:
    print("[deploy] Cannot infer Azure OpenAI endpoint (variable 'azure_endpoint' or 'OPENAI_ENDPOINT' missing). Aborting.")
else:
    # Extract resource name: https://<name>.openai.azure.com -> <name>
    m = re.match(r"https?://([^\\.]+)\\.openai\\.azure\\.com", endpoint)
    if not m:
        print(f"[deploy] Endpoint format unexpected: {endpoint}")
        resource_name = ""
    else:
        resource_name = m.group(1)
        print(f"[deploy] Inferred resource name: {resource_name}")

# Helper to run CLI safely
def run_cli(cmd_list: list, timeout: int = 120):
    """Run Azure CLI command with proper PATH and error handling"""
    print(f"\\n[cli] $ {' '.join(cmd_list)}")
    try:
        proc = subprocess.run(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            text=True,
            env=env
        )
        print(f"[cli] exit={proc.returncode}")
        if proc.stdout:
            print(proc.stdout[:800])
        if proc.stderr:
            print(proc.stderr[:800])
        return proc.returncode, proc.stdout, proc.stderr
    except FileNotFoundError:
        print(f"[cli] az CLI not found at: {az_cli}")
        print("[cli] Install Azure CLI or run in an environment with it available.")
        return 127, "", "az not found"
    except Exception as e:
        print(f"[cli] Exception: {e}")
        return 1, "", str(e)

# 1. Verify az present
rc_version, _, _ = run_cli([az_cli, "--version"])
if rc_version != 0:
    print("[deploy] Azure CLI unavailable; cannot proceed.")
else:
    # 2. Verify login
    rc_login, out_login, err_login = run_cli([az_cli, "account", "show"])
    if rc_login != 0:
        print("[deploy] Not logged in. Run: az login (device/browser) before retry.")
    elif not resource_name or not RESOURCE_GROUP:
        print("[deploy] Missing resource_name or RESOURCE_GROUP; cannot deploy.")
    else:
        # 3. Attempt dall-e-3 deployment
        print("[deploy] Attempting deployment for 'dall-e-3'...")
        cmd_dalle = [
            az_cli, "cognitiveservices", "account", "deployment", "create",
            "--name", resource_name,
            "--resource-group", RESOURCE_GROUP,
            "--deployment-name", "dall-e-3",
            "--model-name", "dall-e-3",
            "--model-format", "OpenAI"
        ]
        rc_dalle, out_dalle, err_dalle = run_cli(cmd_dalle)
        unsupported_markers = ["Unsupported", "not found", "Invalid", "BadRequest", "The model name is invalid"]
        needs_fallback = rc_dalle != 0 and any(marker.lower() in (out_dalle+err_dalle).lower() for marker in unsupported_markers)

        if rc_dalle == 0:
            print("[deploy] Success: dall-e-3 deployment created (or already exists).")
        elif needs_fallback:
            print("[deploy] dall-e-3 unsupported; trying 'gpt-image-1' deployment...")
            cmd_image = [
                az_cli, "cognitiveservices", "account", "deployment", "create",
                "--name", resource_name,
                "--resource-group", RESOURCE_GROUP,
                "--deployment-name", "gpt-image-1",
                "--model-name", "gpt-image-1",
                "--model-format", "OpenAI"
            ]
            rc_img, out_img, err_img = run_cli(cmd_image)
            if rc_img == 0:
                print("[deploy] Success: gpt-image-1 deployment created (or already exists).")
            else:
                print("[deploy] Failed to create gpt-image-1 deployment.")
        else:
            print("[deploy] dall-e-3 deployment failed for non-unsupported reason; not attempting fallback.")

print("[deploy] Done.")
'''

def fix_notebook():
    """Apply all fixes to the notebook"""
    print("="*80)
    print("AZURE CLI PATH FIX SCRIPT")
    print("="*80)
    print()

    # Load notebook
    print(f"[LOAD] Loading notebook from {NOTEBOOK_PATH}")
    nb = load_notebook()
    print(f"[LOAD] Loaded {len(nb['cells'])} cells")
    print()

    # Create backup
    backup_notebook(nb)
    print()

    # Track changes
    changes = []

    # Fix Cell 13 - Service Principal creation
    if len(nb['cells']) > 13:
        print("[FIX] Updating Cell 13 (Service Principal creation)")
        old_source = get_cell_source(nb['cells'][13])
        if 'subprocess' in old_source and 'az account' in old_source:
            set_cell_source(nb['cells'][13], CELL_13_FIXED)
            changes.append("Cell 13: Added Azure CLI PATH detection, MSAL cache clearing, and proper subprocess usage")
            print("[OK] Cell 13 updated")
        else:
            print("[SKIP] Cell 13 doesn't match expected pattern")
        print()

    # Fix Cell 42 - Token rate limiting
    if len(nb['cells']) > 42:
        print("[FIX] Updating Cell 42 (Token rate limiting)")
        old_source = get_cell_source(nb['cells'][42])
        if 'az apim' in old_source or 'azure-openai-token-limit' in old_source:
            set_cell_source(nb['cells'][42], CELL_42_FIXED)
            changes.append("Cell 42: Added Azure CLI PATH detection and proper subprocess usage")
            print("[OK] Cell 42 updated")
        else:
            print("[SKIP] Cell 42 doesn't match expected pattern")
        print()

    # Fix Cell 89 - Image model deployment
    if len(nb['cells']) > 89:
        print("[FIX] Updating Cell 89 (Image model deployment)")
        old_source = get_cell_source(nb['cells'][89])
        if 'dall-e-3' in old_source or 'cognitiveservices' in old_source:
            set_cell_source(nb['cells'][89], CELL_89_FIXED)
            changes.append("Cell 89: Added Azure CLI PATH detection and fixed subprocess calls to use lists instead of shlex")
            print("[OK] Cell 89 updated")
        else:
            print("[SKIP] Cell 89 doesn't match expected pattern")
        print()

    # Save notebook
    if changes:
        save_notebook(nb)
        print()
        print("="*80)
        print("SUMMARY OF CHANGES")
        print("="*80)
        for i, change in enumerate(changes, 1):
            print(f"{i}. {change}")
        print()
        print("[SUCCESS] All fixes applied successfully!")
        print(f"[BACKUP] Backup saved to: {BACKUP_PATH}")
        print()
        print("NEXT STEPS:")
        print("1. Open the notebook in Jupyter")
        print("2. Restart the kernel")
        print("3. Run the updated cells")
        print("4. Verify Azure CLI is detected correctly")
        print()
        print("DIAGNOSTIC INFO TO CHECK:")
        print("- Each cell should print: [INFO] Azure CLI: /usr/bin/az")
        print("- Cell 13 should clear MSAL cache if stale tokens exist")
        print("- All subprocess calls now use proper PATH environment")
    else:
        print("[INFO] No changes were needed")

    return len(changes) > 0

if __name__ == "__main__":
    try:
        success = fix_notebook()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[ERROR] Failed to fix notebook: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
