#!/usr/bin/env python3
"""
APIM Policy Reset Script
This script resets the APIM policy to a minimal working configuration
to resolve 500 Internal Server errors.
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path

# Load .env file if it exists (override shell environment)
try:
    from dotenv import load_dotenv
    env_file = Path(__file__).parent / 'master-lab.env'
    if env_file.exists():
        load_dotenv(env_file, override=True)
        print(f'[OK] Loaded environment from: {env_file} (override=True)\n')
except ImportError:
    pass  # dotenv not required

# Load environment variables
APIM_SERVICE_NAME = os.getenv('APIM_SERVICE_NAME', 'apim-pavavy6pu5hpa')
RESOURCE_GROUP = os.getenv('RESOURCE_GROUP', 'lab-master-lab')
API_ID = os.getenv('APIM_API_ID', 'inference-api')

print('='*80)
print('APIM POLICY RESET - Fixing 500 Errors')
print('='*80)
print(f'APIM Service: {APIM_SERVICE_NAME}')
print(f'Resource Group: {RESOURCE_GROUP}')
print(f'API ID: {API_ID}')
print()

# Step 1: Get current policy to diagnose the issue
print('[STEP 1] Retrieving current APIM policy...')
get_policy_url = (
    f"https://management.azure.com/subscriptions/d334f2cd-3efd-494e-9fd3-2470b1a13e4c/"
    f"resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.ApiManagement/service/{APIM_SERVICE_NAME}/"
    f"apis/{API_ID}/policies/policy?api-version=2023-05-01-preview"
)

try:
    # Windows: use 'az.cmd' instead of 'az'
    az_cmd = 'az.cmd' if os.name == 'nt' else 'az'
    result = subprocess.run(
        [az_cmd, 'rest', '--method', 'get', '--url', get_policy_url],
        capture_output=True,
        text=True,
        timeout=30,
        shell=False
    )

    if result.returncode == 0:
        policy_data = json.loads(result.stdout)
        current_policy = policy_data.get('properties', {}).get('value', 'Not found')
        print('[OK] Current policy retrieved')
        print('Current policy XML (first 500 chars):')
        print(current_policy[:500])
        print()

        # Check for common issues
        if 'validate-azure-ad-token' in current_policy and '{tenant-id}' in current_policy:
            print('[ERROR] Policy contains placeholder tokens: {tenant-id}, {client-application-id}')
            print('This will cause 500 errors!')
        if 'set-backend-service' in current_policy and '{backend-id}' in current_policy:
            print('[ERROR] Policy contains placeholder backend-id: {backend-id}')
            print('This will cause 500 errors!')
    else:
        print(f'[WARNING] Could not retrieve policy: {result.stderr}')
except Exception as e:
    print(f'[WARNING] Error retrieving policy: {e}')

print()

# Step 2: Reset to minimal working policy
print('[STEP 2] Resetting to minimal working policy...')

minimal_policy = '''<policies>
    <inbound>
        <base />
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
</policies>'''

# Create the policy payload
policy_payload = {
    "properties": {
        "value": minimal_policy,
        "format": "xml"
    }
}

# Write to temp file
temp_dir = Path(tempfile.gettempdir())
payload_file = temp_dir / 'apim-minimal-policy.json'

with open(payload_file, 'w', encoding='utf-8') as f:
    json.dump(policy_payload, f, indent=2)

print(f'Policy payload written to: {payload_file}')

# Apply the policy using Azure REST API
put_policy_url = (
    f"https://management.azure.com/subscriptions/d334f2cd-3efd-494e-9fd3-2470b1a13e4c/"
    f"resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.ApiManagement/service/{APIM_SERVICE_NAME}/"
    f"apis/{API_ID}/policies/policy?api-version=2023-05-01-preview"
)

print(f'Applying minimal policy to API: {API_ID}...')

try:
    # Windows: use 'az.cmd' instead of 'az'
    az_cmd = 'az.cmd' if os.name == 'nt' else 'az'
    result = subprocess.run(
        [az_cmd, 'rest', '--method', 'put', '--url', put_policy_url,
         '--body', f'@{payload_file}'],
        capture_output=True,
        text=True,
        timeout=60,
        shell=False
    )

    if result.returncode == 0:
        print('[SUCCESS] Minimal policy applied!')
        print('The API should now accept requests with just the api-key header.')
        print()
        print('Next steps:')
        print('1. Test API Key authentication (should work now)')
        print('2. If OAuth 2.0 is needed, configure Azure Entra ID properly')
        print('3. Apply OAuth policy with correct tenant-id and client-application-id')
    else:
        print(f'[ERROR] Failed to apply policy: {result.stderr}')
        print(f'Return code: {result.returncode}')
except Exception as e:
    print(f'[ERROR] Exception applying policy: {e}')

print()
print('='*80)
print('POLICY RESET COMPLETE')
print('='*80)
