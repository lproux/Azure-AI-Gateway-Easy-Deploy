#!/usr/bin/env python3
"""Test different SDK configurations to find what works"""
from pathlib import Path
from dotenv import load_dotenv
import os
from openai import AzureOpenAI

# Load environment
env_path = Path('master-lab.env')
load_dotenv(env_path)

apim_gateway_url = os.getenv('APIM_GATEWAY_URL')
apim_api_key = os.getenv('APIM_API_KEY')

print("=" * 80)
print("TESTING AZUREOPENAI SDK CONFIGURATIONS")
print("=" * 80)
print()

# Test different endpoint configurations
configs = [
    {
        "name": "Config 1: gateway + /inference/openai",
        "endpoint": f"{apim_gateway_url}/inference/openai",
        "api_version": "2024-10-01-preview"
    },
    {
        "name": "Config 2: gateway + /inference",
        "endpoint": f"{apim_gateway_url}/inference",
        "api_version": "2024-10-01-preview"
    },
    {
        "name": "Config 3: gateway only",
        "endpoint": apim_gateway_url,
        "api_version": "2024-10-01-preview"
    },
    {
        "name": "Config 4: different api_version",
        "endpoint": f"{apim_gateway_url}/inference/openai",
        "api_version": "2024-07-18"
    }
]

for config in configs:
    print(f"\nTesting: {config['name']}")
    print("-" * 80)
    print(f"  Endpoint: {config['endpoint']}")
    print(f"  API Version: {config['api_version']}")

    try:
        client = AzureOpenAI(
            azure_endpoint=config['endpoint'],
            api_key=apim_api_key,
            api_version=config['api_version']
        )

        print("  Client created successfully")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Say 'OK' if this works."}
            ],
            max_tokens=10
        )

        content = response.choices[0].message.content
        print(f"  [SUCCESS!] Response: {content}")
        print()
        print("  *** THIS CONFIGURATION WORKS! ***")
        print()

    except Exception as e:
        error_str = str(e)
        if '404' in error_str:
            print(f"  [FAILED] 404 Not Found")
        else:
            print(f"  [FAILED] {error_str[:100]}")

print()
print("=" * 80)
print("TEST COMPLETE")
print("=" * 80)
