#!/usr/bin/env python3
"""
Update Cell 57 with corrected authentication tests
"""

import json
import sys
import io

# Set UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

notebook_path = 'MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab/master-ai-gateway-fix-MCP.ipynb'

# New cell 57 content - simplified to fix 500 errors
new_cell_57_content = '''# Lab 06: Access Control - Multi-Mode Authentication Test
# After running the policy reset (cell 55 or fix_apim_policy.py), test authentication modes

import os
import json
import requests
from openai import AzureOpenAI

# Configuration from environment
apim_gateway_url = os.getenv('APIM_GATEWAY_URL')
apim_api_key = os.getenv('APIM_API_KEY')
inference_api_path = os.getenv('INFERENCE_API_PATH', 'inference')
api_version = '2024-02-15-preview'
deployment = 'gpt-4o-mini'

# Validate
if not apim_gateway_url or not apim_api_key:
    raise ValueError('Required env vars not set: APIM_GATEWAY_URL, APIM_API_KEY')

print('='*80)
print('AUTHENTICATION MODE TESTING')
print('='*80)
print(f'Gateway: {apim_gateway_url}')
print(f'API Key: ...{apim_api_key[-4:]}')
print()

# Build endpoint
rest_url = f"{apim_gateway_url}/{inference_api_path}/openai/deployments/{deployment}/chat/completions?api-version={api_version}"

# Test payload
test_messages = {
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say 'Hello, authentication works!' in one sentence."}
    ],
    "max_tokens": 50
}

def test_authentication(mode_name, headers):
    """Test a specific authentication mode"""
    print(f"\\n[TEST] {mode_name}")
    print(f"Headers: {', '.join(h + '=***' if 'key' in h.lower() or 'auth' in h.lower() else h + '=' + headers[h] for h in headers)}")

    try:
        response = requests.post(rest_url, headers=headers, json=test_messages, timeout=30)

        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            message = data.get("choices", [{}])[0].get("message", {}).get("content", "No content")
            print(f"✅ SUCCESS: {message}")
            return True
        else:
            print(f"❌ FAILED")
            print(f"Response: {response.text[:500]}")
            return False

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

# =============================================================================
# TEST 1: API Key Only (Standard APIM subscription key)
# =============================================================================
print('\\n' + '='*80)
print('TEST 1: API Key Only (Standard APIM)')
print('='*80)

headers_apikey_only = {
    "api-key": apim_api_key,
    "Content-Type": "application/json"
}

apikey_works = test_authentication("API Key Only", headers_apikey_only)

if not apikey_works:
    print('\\n❌ CRITICAL: Basic API Key authentication is failing!')
    print('This indicates the APIM policy or backend is misconfigured.')
    print('\\nRECOMMENDED ACTIONS:')
    print('1. Run the policy reset script: .venv/Scripts/python.exe fix_apim_policy.py')
    print('2. Or run cell 55 (COMPREHENSIVE APIM DIAGNOSTIC)')
    print('3. Verify APIM backend is correctly configured')
    print('4. Check APIM backend Azure OpenAI service is deployed and accessible')
else:
    print('\\n✅ Basic authentication working! APIM is functional.')

# =============================================================================
# TEST 2: OAuth 2.0 with Azure Entra ID (Optional - requires setup)
# =============================================================================
print('\\n' + '='*80)
print('TEST 2: OAuth 2.0 with Azure Entra ID (Optional)')
print('='*80)

print('\\nℹ️  OAuth 2.0 Configuration Status:')

# Check if OAuth is configured
oauth_configured = False
try:
    from azure.identity import DefaultAzureCredential

    # Try to get a token
    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)

    # Try multiple scopes
    token = None
    for scope in ['https://cognitiveservices.azure.com/.default',
                  'https://management.azure.com/.default']:
        try:
            token_response = credential.get_token(scope)
            token = token_response.token
            print(f'✅ Got token with scope: {scope}')
            oauth_configured = True
            break
        except Exception as e:
            print(f'⚠️  Could not get token with scope {scope}: {e}')

    if oauth_configured and token:
        # Test Bearer only
        print('\\n[TEST] JWT Bearer Token Only')
        headers_bearer_only = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        bearer_works = test_authentication("Bearer Only", headers_bearer_only)

        # Test Combined
        print('\\n[TEST] Combined (Bearer + API Key)')
        headers_combined = {
            "Authorization": f"Bearer {token}",
            "api-key": apim_api_key,
            "Content-Type": "application/json"
        }
        combined_works = test_authentication("Combined Auth", headers_combined)

        if bearer_works or combined_works:
            print('\\n✅ OAuth 2.0 is working!')
        else:
            print('\\n⚠️  OAuth 2.0 failed. This may be expected if APIM policy does not validate JWT.')
            print('To enable OAuth 2.0:')
            print('1. Create App Registration in Azure Entra ID')
            print('2. Apply APIM policy with validate-azure-ad-token')
            print('3. See reference: labs/access-controlling/policy.xml')
    else:
        print('\\n⚠️  Could not obtain OAuth token.')
        print('OAuth 2.0 is optional. API Key authentication should be sufficient.')

except ImportError:
    print('\\n⚠️  azure-identity library not installed. OAuth testing skipped.')
    print('Install with: pip install azure-identity')
except Exception as e:
    print(f'\\n⚠️  OAuth configuration error: {e}')
    print('OAuth 2.0 is optional. API Key authentication should be sufficient.')

# =============================================================================
# TEST 3: OpenAI SDK with API Key
# =============================================================================
print('\\n' + '='*80)
print('TEST 3: OpenAI SDK with API Key')
print('='*80)

try:
    client = AzureOpenAI(
        azure_endpoint=f"{apim_gateway_url}/{inference_api_path}",
        api_key=apim_api_key,
        api_version=api_version
    )

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'SDK authentication works!' in one sentence."}
        ],
        max_tokens=50
    )

    print(f"✅ SUCCESS: {response.choices[0].message.content}")

except Exception as e:
    print(f"❌ ERROR: {e}")

# =============================================================================
# SUMMARY
# =============================================================================
print('\\n' + '='*80)
print('AUTHENTICATION TEST SUMMARY')
print('='*80)

if apikey_works:
    print('✅ Your APIM Gateway is working correctly with API Key authentication')
    print('✅ You can proceed with the workshop')
    print('\\nFor OAuth 2.0 setup, see: labs/access-controlling/')
else:
    print('❌ APIM Gateway has issues - fix required before proceeding')
    print('\\nRun fix_apim_policy.py to reset the policy')

print('='*80)
'''

# Load notebook
print(f'Loading notebook: {notebook_path}')
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f'Current cell count: {len(nb["cells"])}')

# Update cell 57 (index 56)
if len(nb['cells']) > 56:
    print('Updating cell 57 (index 56)...')
    nb['cells'][56]['source'] = new_cell_57_content.split('\\n')
    print('[OK] Cell 57 updated')
else:
    print('[ERROR] Cell 57 does not exist')
    sys.exit(1)

# Save notebook
print(f'Saving notebook...')
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print('[SUCCESS] Notebook updated successfully!')
print()
print('='*80)
print('NEXT STEPS FOR USER:')
print('='*80)
print('1. Close and reopen the notebook in VS Code')
print('2. Run fix_apim_policy.py OR run cell 55 to reset the broken policy')
print('3. Run the updated cell 57 to test authentication')
print('='*80)
