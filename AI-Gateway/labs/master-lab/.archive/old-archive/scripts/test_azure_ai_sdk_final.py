#!/usr/bin/env python3
"""Verify the exact configuration for ChatCompletionsClient"""
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
deployment_name = "gpt-4o-mini"  # This should be a variable in the notebook

print("=" * 80)
print("FINAL VERIFICATION - ChatCompletionsClient Configuration")
print("=" * 80)
print()

# The working configuration
endpoint = f"{apim_gateway_url}/inference/openai/deployments/{deployment_name}"
print(f"Endpoint: {endpoint}")
print()

# Test 1: With model parameter (might fail)
print("Test 1: WITH model parameter")
print("-" * 80)
try:
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(apim_api_key)
    )

    response = client.complete(
        model=deployment_name,  # Include model parameter
        messages=[
            SystemMessage(content="You are helpful."),
            UserMessage(content="What is Azure AI Foundry? Answer in one sentence.")
        ]
    )

    print(f"[SUCCESS] Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"[FAILED] {e}")

print()

# Test 2: WITHOUT model parameter (should work)
print("Test 2: WITHOUT model parameter")
print("-" * 80)
try:
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(apim_api_key)
    )

    response = client.complete(
        messages=[
            SystemMessage(content="You are helpful."),
            UserMessage(content="What is Azure AI Foundry? Answer in one sentence.")
        ]
        # NO model parameter
    )

    print(f"[SUCCESS] Response: {response.choices[0].message.content}")
    print()
    print("*** USE THIS CONFIGURATION (no model parameter) ***")
except Exception as e:
    print(f"[FAILED] {e}")

print()
print("=" * 80)
