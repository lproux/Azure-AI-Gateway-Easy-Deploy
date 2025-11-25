#!/usr/bin/env python3
"""Fix cell 50 - Azure AI Inference SDK configuration"""
import json
import shutil
from pathlib import Path

notebook_path = Path('master-ai-gateway.ipynb')
backup_path = Path('master-ai-gateway.ipynb.backup-before-cell50-fix')

print("=" * 80)
print("FIXING CELL 50 - Azure AI Inference SDK")
print("=" * 80)
print()

# Create backup
shutil.copy2(notebook_path, backup_path)
print(f"[OK] Created backup: {backup_path}")

# Load notebook
with open(notebook_path, encoding='utf-8') as f:
    nb = json.load(f)

print(f"[OK] Loaded notebook with {len(nb['cells'])} cells")
print()

# Fixed cell 50 content
fixed_cell_50 = """# Lab 09: AI Foundry SDK - Chat Completion via APIM
# CRITICAL: ChatCompletionsClient requires the FULL endpoint path including deployment

# Import required libraries
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference.models import SystemMessage, UserMessage

# Use deployment name (gpt-4o-mini is available in all 3 foundry hubs)
deployment_name = "gpt-4o-mini"

# CRITICAL FIX: ChatCompletionsClient needs the FULL path including deployment
# This is different from AzureOpenAI SDK!
# Format: {gateway}/{inference_path}/openai/deployments/{deployment_name}
inference_endpoint = f"{apim_gateway_url}/{inference_api_path}/openai/deployments/{deployment_name}"

print(f'[OK] Inference Endpoint: {inference_endpoint}')

# Create the ChatCompletionsClient
inference_client = ChatCompletionsClient(
    endpoint=inference_endpoint,
    credential=AzureKeyCredential(api_key)
)

print('[OK] ChatCompletionsClient created successfully')
print()

# Make the request
# NOTE: No 'model' parameter needed since deployment is in the endpoint URL
print('[*] Testing chat completion with Azure AI Inference SDK...')
response = inference_client.complete(
    messages=[
        SystemMessage(content='You are helpful.'),
        UserMessage(content='What is Azure AI Foundry?')
    ]
)

print(f'[SUCCESS] Response: {response.choices[0].message.content}')
print()
print('[OK] Lab 09 Complete!')
"""

# Update cell 50
print("Updating cell 50:")
print("-" * 80)

nb['cells'][50]['source'] = fixed_cell_50.split('\n')
print("[OK] Fixed cell 50 (Lab 09 - AI Foundry SDK)")
print()

# Save updated notebook
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print(f"[OK] Saved updated notebook")
print()
print("=" * 80)
print("CELL 50 FIX APPLIED SUCCESSFULLY")
print("=" * 80)
print()
print("Key changes:")
print("  1. Added all required imports (ChatCompletionsClient, etc.)")
print("  2. Fixed endpoint to include FULL path with deployment:")
print("     {gateway}/inference/openai/deployments/gpt-4o-mini")
print("  3. Removed 'model' parameter from complete() call")
print("  4. Added helpful comments explaining the difference from AzureOpenAI SDK")
print()
print(f"Original backed up to: {backup_path}")
print()
print("You can now run cell 50 in the notebook!")
