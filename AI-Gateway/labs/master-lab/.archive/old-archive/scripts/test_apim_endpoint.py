#!/usr/bin/env python3
"""
Direct HTTP test of APIM endpoint to diagnose 404 errors
"""
import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import os

# Load master-lab.env
env_path = Path('master-lab.env')
if env_path.exists():
    load_dotenv(env_path)
    print(f"[OK] Loaded environment from {env_path}")
else:
    print(f"[ERROR] {env_path} not found")
    exit(1)

# Get configuration
apim_gateway_url = os.getenv('APIM_GATEWAY_URL')
apim_api_key = os.getenv('APIM_API_KEY')
inference_api_path = os.getenv('INFERENCE_API_PATH', 'inference')

print(f"\n{'='*80}")
print(f"CONFIGURATION")
print(f"{'='*80}")
print(f"APIM Gateway URL: {apim_gateway_url}")
print(f"API Key: {apim_api_key[:20]}..." if apim_api_key else "API Key: MISSING")
print(f"Inference Path: {inference_api_path}")

# Test different endpoint formats
test_configs = [
    {
        "name": "Format 1: gateway + /inference + /chat/completions",
        "url": f"{apim_gateway_url}/{inference_api_path}/chat/completions"
    },
    {
        "name": "Format 2: gateway + /chat/completions (no inference path)",
        "url": f"{apim_gateway_url}/chat/completions"
    },
    {
        "name": "Format 3: gateway + /inference/openai/deployments/.../chat/completions",
        "url": f"{apim_gateway_url}/{inference_api_path}/openai/deployments/gpt-4o-mini/chat/completions"
    },
    {
        "name": "Format 4: gateway/openai/deployments/.../chat/completions",
        "url": f"{apim_gateway_url}/openai/deployments/gpt-4o-mini/chat/completions"
    }
]

headers = {
    "Content-Type": "application/json",
    "api-key": apim_api_key
}

payload = {
    "messages": [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Say 'test successful' if you can read this."}
    ],
    "max_tokens": 50
}

print(f"\n{'='*80}")
print(f"TESTING ENDPOINTS")
print(f"{'='*80}\n")

for idx, config in enumerate(test_configs, 1):
    print(f"\n{idx}. {config['name']}")
    print(f"   URL: {config['url']}")

    try:
        response = requests.post(
            config['url'],
            headers=headers,
            json=payload,
            timeout=30
        )

        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            print(f"   [SUCCESS!]")
            try:
                data = response.json()
                if 'choices' in data and len(data['choices']) > 0:
                    content = data['choices'][0].get('message', {}).get('content', '')
                    print(f"   Response: {content[:100]}")
                print(f"\n   *** THIS IS THE CORRECT ENDPOINT FORMAT! ***\n")
            except:
                print(f"   Response body: {response.text[:200]}")
        elif response.status_code == 404:
            print(f"   [NOT FOUND (404)]")
            print(f"   Response: {response.text[:200]}")
        else:
            print(f"   [Error {response.status_code}]")
            print(f"   Response: {response.text[:200]}")

    except requests.exceptions.RequestException as e:
        print(f"   [Request failed: {e}]")

print(f"\n{'='*80}")
print(f"DIAGNOSIS COMPLETE")
print(f"{'='*80}\n")
