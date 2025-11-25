#!/usr/bin/env python3
"""Test the CORRECT endpoint format based on Bicep configuration"""
import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment
env_path = Path('master-lab.env')
load_dotenv(env_path)

apim_gateway_url = os.getenv('APIM_GATEWAY_URL')
apim_api_key = os.getenv('APIM_API_KEY')

print("=" * 80)
print("TESTING CORRECT ENDPOINT FORMAT")
print("=" * 80)
print(f"APIM Gateway: {apim_gateway_url}")
print(f"API Key: {apim_api_key[:20]}...")
print()

# Based on Bicep: path = 'inference/openai'
# The AzureOpenAI client will append the rest

# Test 1: Using AzureOpenAI SDK with correct endpoint
print("TEST 1: AzureOpenAI SDK with correct endpoint")
print("-" * 80)

from openai import AzureOpenAI

# The endpoint should be: gateway_url + /inference/openai
# The SDK will append /deployments/{model}/chat/completions
endpoint = f"{apim_gateway_url}/inference/openai"
print(f"Endpoint: {endpoint}")

try:
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=apim_api_key,
        api_version="2024-10-01-preview"
    )

    print("Client created successfully")
    print("Making chat completion request...")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": "Say 'SUCCESS' if you can read this."}
        ],
        max_tokens=50
    )

    print(f"[SUCCESS] Response: {response.choices[0].message.content}")
    print()
    print("=" * 80)
    print("ENDPOINT FORMAT CONFIRMED WORKING!")
    print("=" * 80)
    print(f"Correct endpoint: {endpoint}")
    print("Usage in notebook:")
    print("  client = AzureOpenAI(")
    print(f"      azure_endpoint='{endpoint}',")
    print(f"      api_key='{apim_api_key[:10]}...',")
    print("      api_version='2024-10-01-preview'")
    print("  )")

except Exception as e:
    print(f"[ERROR] Failed: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 80)
print("TEST COMPLETE")
print("=" * 80)
