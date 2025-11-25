#!/usr/bin/env python3
"""
Standalone Authentication Test - Does not modify APIM policies
Run this AFTER fix_apim_policy.py to test if authentication works
"""

import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_file = Path(__file__).parent / 'master-lab.env'
if env_file.exists():
    load_dotenv(env_file)
    print(f'[OK] Loaded environment from: {env_file}')
else:
    print('[WARNING] master-lab.env not found, using system environment')

# Configuration
apim_gateway_url = os.getenv('APIM_GATEWAY_URL')
apim_api_key = os.getenv('APIM_API_KEY')
inference_api_path = os.getenv('INFERENCE_API_PATH', 'inference')
api_version = '2024-02-15-preview'
deployment = 'gpt-4o-mini'

print('='*80)
print('STANDALONE AUTHENTICATION TEST')
print('='*80)
print(f'Gateway: {apim_gateway_url}')
print(f'API Key: ...{apim_api_key[-4:] if apim_api_key else "NOT SET"}')
print()

if not apim_gateway_url or not apim_api_key:
    print('[ERROR] Missing required environment variables')
    print('Make sure master-lab.env contains:')
    print('  - APIM_GATEWAY_URL')
    print('  - APIM_API_KEY')
    exit(1)

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

print('='*80)
print('TEST 1: API Key Authentication')
print('='*80)
print()

headers = {
    "api-key": apim_api_key,
    "Content-Type": "application/json"
}

try:
    print(f'Sending request to: {rest_url}')
    response = requests.post(rest_url, headers=headers, json=test_messages, timeout=30)

    print(f'Status Code: {response.status_code}')
    print()

    if response.status_code == 200:
        data = response.json()
        message = data.get("choices", [{}])[0].get("message", {}).get("content", "No content")
        print('[SUCCESS] Authentication works!')
        print(f'Response: {message}')
        print()
        print('='*80)
        print('RESULT: Your APIM is working correctly!')
        print('='*80)
        print('You can now proceed with your workshop.')
    else:
        print('[FAILED] Authentication failed')
        print()
        print('Response body:')
        print(response.text)
        print()
        print('='*80)
        print('DIAGNOSIS:')
        print('='*80)

        if response.status_code == 500:
            print('[ERROR] 500 Internal Server Error')
            print()
            print('Possible causes:')
            print('1. A broken APIM policy was applied (most likely)')
            print('2. Backend Azure OpenAI service is not configured')
            print('3. Backend is not responding')
            print()
            print('RECOMMENDED ACTIONS:')
            print('1. Run fix_apim_policy.py again to reset the policy')
            print('2. Do NOT run cells 16, 22, 38, 45 (they apply complex policies)')
            print('3. Test again with this script')
            print()
            print('If the issue persists after reset:')
            print('- Check APIM backend configuration in Azure Portal')
            print('- Verify Azure OpenAI deployment exists and is accessible')
        elif response.status_code == 401:
            print('[ERROR] 401 Unauthorized')
            print('The API key is invalid or not configured in APIM')
        elif response.status_code == 404:
            print('[ERROR] 404 Not Found')
            print('The API endpoint or deployment does not exist')

except requests.exceptions.Timeout:
    print('[ERROR] Request timed out')
    print('The APIM gateway or backend is not responding')
except Exception as e:
    print(f'[ERROR] Exception: {e}')

print()
print('='*80)
