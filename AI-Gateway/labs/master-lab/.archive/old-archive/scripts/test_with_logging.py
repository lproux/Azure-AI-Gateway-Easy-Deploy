#!/usr/bin/env python3
"""Test with verbose logging"""
import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import os
import logging

# Enable verbose logging
logging.basicConfig(level=logging.DEBUG)

# Load environment
env_path = Path('master-lab.env')
load_dotenv(env_path)

apim_gateway_url = os.getenv('APIM_GATEWAY_URL')
apim_api_key = os.getenv('APIM_API_KEY')

print("=" * 80)
print("TESTING WITH VERBOSE LOGGING")
print("=" * 80)

# Test the exact URL the AzureOpenAI client would use
url = f"{apim_gateway_url}/inference/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-10-01-preview"

headers = {
    "Content-Type": "application/json",
    "api-key": apim_api_key,
}

payload = {
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say 'test' if you can read this."}
    ],
    "max_tokens": 10
}

print(f"URL: {url}")
print(f"Headers: {headers}")
print(f"Payload: {json.dumps(payload, indent=2)}")
print()
print("Making request...")
print("-" * 80)

try:
    response = requests.post(url, headers=headers, json=payload, timeout=30)

    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text}")

    if response.status_code == 200:
        data = response.json()
        print(f"\n[SUCCESS] {data['choices'][0]['message']['content']}")
    else:
        print(f"\n[FAILED] {response.status_code}")

except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()

print("=" * 80)
