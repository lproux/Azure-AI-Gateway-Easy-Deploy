#!/usr/bin/env python3
"""Test Azure AI Inference SDK (ChatCompletionsClient) with different endpoints"""
from pathlib import Path
from dotenv import load_dotenv
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference.models import SystemMessage, UserMessage

# Load environment
env_path = Path('master-lab.env')
load_dotenv(env_path)

apim_gateway_url = os.getenv('APIM_GATEWAY_URL')
apim_api_key = os.getenv('APIM_API_KEY')
inference_api_path = os.getenv('INFERENCE_API_PATH', 'inference')

print("=" * 80)
print("TESTING AZURE AI INFERENCE SDK (ChatCompletionsClient)")
print("=" * 80)
print()

# Test different endpoint configurations
configs = [
    {
        "name": "Config 1: gateway + /inference/models",
        "endpoint": f"{apim_gateway_url}/inference/models"
    },
    {
        "name": "Config 2: gateway + /inference/openai",
        "endpoint": f"{apim_gateway_url}/inference/openai"
    },
    {
        "name": "Config 3: gateway + /inference",
        "endpoint": f"{apim_gateway_url}/inference"
    },
    {
        "name": "Config 4: gateway + /inference/openai/deployments/gpt-4o-mini",
        "endpoint": f"{apim_gateway_url}/inference/openai/deployments/gpt-4o-mini"
    }
]

for config in configs:
    print(f"\nTesting: {config['name']}")
    print("-" * 80)
    print(f"  Endpoint: {config['endpoint']}")

    try:
        client = ChatCompletionsClient(
            endpoint=config['endpoint'],
            credential=AzureKeyCredential(apim_api_key)
        )

        print("  Client created successfully")

        response = client.complete(
            messages=[
                SystemMessage(content="You are a helpful assistant."),
                UserMessage(content="Say 'OK' if this works.")
            ],
            model="gpt-4o-mini"  # Try with model parameter
        )

        content = response.choices[0].message.content
        print(f"  [SUCCESS!] Response: {content}")
        print()
        print("  *** THIS CONFIGURATION WORKS! ***")
        print()

    except Exception as e:
        error_str = str(e)
        if 'Resource not found' in error_str or 'not found' in error_str.lower():
            print(f"  [FAILED] Resource Not Found")
        else:
            print(f"  [FAILED] {error_str[:150]}")

print()
print("=" * 80)
print("TEST COMPLETE")
print("=" * 80)
