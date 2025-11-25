#!/usr/bin/env python3
"""
Grant User Access Administrator role to Service Principal
Simple version that clears cache and uses Azure CLI
"""

import os
import shutil
import subprocess
from pathlib import Path
from dotenv import load_dotenv

print('=' * 70)
print('GRANT USER ACCESS ADMINISTRATOR TO SERVICE PRINCIPAL')
print('=' * 70)
print()

# Load Service Principal credentials
credentials_file = '.azure-credentials.env'
if not os.path.exists(credentials_file):
    print('[ERROR] .azure-credentials.env not found!')
    print('[*] Please run Cell 11 first to create Service Principal')
    exit(1)

load_dotenv(credentials_file)
client_id = os.getenv('AZURE_CLIENT_ID')
subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')

if not client_id or not subscription_id:
    print('[ERROR] Missing credentials in .azure-credentials.env')
    exit(1)

print(f'[*] Service Principal Client ID: {client_id}')
print(f'[*] Subscription ID: {subscription_id}')
print()

# Clear Azure CLI cache (fixes MSAL cache corruption)
print('[*] Clearing Azure CLI cache to fix any corruption...')
azure_dir = Path.home() / '.azure'
msal_cache_file = azure_dir / 'msal_http_cache'

if msal_cache_file.exists():
    try:
        msal_cache_file.unlink()
        print('[OK] MSAL HTTP cache cleared')
    except Exception as e:
        print(f'[WARNING] Could not delete cache: {e}')
else:
    print('[OK] No cache to clear')

# Also clear token cache
msal_token_cache = azure_dir / 'msal_token_cache.bin'
if msal_token_cache.exists():
    try:
        msal_token_cache.unlink()
        print('[OK] MSAL token cache cleared')
    except Exception as e:
        print(f'[WARNING] Could not delete token cache: {e}')

print()

# Check if role already exists
print('[*] Checking current role assignments...')
result = subprocess.run(
    f'az role assignment list --assignee {client_id} --subscription {subscription_id} --query "[].{{role:roleDefinitionName,scope:scope}}" --output json',
    shell=True,
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print(f'[ERROR] Failed to check roles: {result.stderr}')
    print()
    print('[*] Please run this command manually:')
    print(f'    az role assignment create --assignee {client_id} --role "User Access Administrator" --scope /subscriptions/{subscription_id}')
    exit(1)

import json
assignments = json.loads(result.stdout)
print(f'[OK] Found {len(assignments)} existing role(s):')
for assignment in assignments:
    print(f'  - {assignment["role"]}')
print()

# Check if User Access Administrator already exists
has_uaa = any(a['role'] == 'User Access Administrator' for a in assignments)

if has_uaa:
    print('[OK] Service Principal already has User Access Administrator role')
    print('[OK] No action needed - you can re-run the deployment (Cell 17)')
else:
    print('[*] Granting User Access Administrator role...')
    print('[*] This allows the Service Principal to create role assignments during deployment')
    print()

    # Grant the role
    result = subprocess.run(
        f'az role assignment create '
        f'--assignee {client_id} '
        f'--role "User Access Administrator" '
        f'--scope /subscriptions/{subscription_id}',
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f'[ERROR] Failed to grant role: {result.stderr}')
        print()
        print('[*] You may need higher privileges. Try this command manually:')
        print(f'    az role assignment create --assignee {client_id} --role "User Access Administrator" --scope /subscriptions/{subscription_id}')
        print()
        print('[*] Note: You need Owner or User Access Administrator permission on the subscription')
        exit(1)

    print('[OK] User Access Administrator role granted successfully!')
    print()
    print('[OK] Next step: Re-run the deployment (Cell 17)')
    print('[*] The deployment should now succeed without permission errors')
