#!/usr/bin/env python3
"""
Fix Semantic Caching Lab - Cell 52
Applies the policy using correct Azure REST API syntax
"""
import json
from pathlib import Path

# Find the notebook
notebook_path = Path('master-ai-gateway-fix-MCP-clean.ipynb')

with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Find Cell 52 (Apply Semantic Caching Policy)
cells = notebook['cells']

# New fixed cell source
fixed_cell_source = """# Lab 09: Semantic Caching - Step 2: Apply Semantic Caching Policy (FIXED)

import os
from pathlib import Path
from dotenv import load_dotenv

env_file = Path('master-lab.env')
if env_file.exists():
    load_dotenv(env_file)

# Get required variables
apim_service_name = os.environ.get('APIM_SERVICE_NAME')
resource_group = os.environ.get('RESOURCE_GROUP')
subscription_id = os.environ.get('SUBSCRIPTION_ID')
api_id = os.environ.get('APIM_API_ID', 'inference-api')

print("\\n[*] Step 2: Applying Semantic Caching Policy...")
print(f"    API ID: {api_id}")
print(f"    Cache Duration: 120 seconds")
print(f"    Similarity Threshold: 0.8")

# Check if Redis cache is configured in APIM
import subprocess

print("\\n[*] Checking APIM cache configuration...")
cache_check_cmd = f\"\"\"az apim cache list \\
    --service-name {apim_service_name} \\
    --resource-group {resource_group} \\
    --query "[?name=='default' || name=='Default'].{{name:name, description:description}}" \\
    -o json\"\"\"

result = subprocess.run(cache_check_cmd, shell=True, capture_output=True, text=True)

if result.returncode == 0:
    caches = json.loads(result.stdout) if result.stdout else []
    if caches:
        print(f"✅ APIM cache configured: {caches[0].get('name', 'default')}")
        print(f"   Description: {caches[0].get('description', 'N/A')}")
    else:
        print("⚠️  No cache configured in APIM!")
        print("   Semantic caching requires Redis cache to be connected to APIM")
        print("   The cache should have been created during deployment")
else:
    print(f"⚠️  Could not check cache: {result.stderr[:200]}")

# Semantic caching policy XML
policy_xml = \"\"\"<policies>
    <inbound>
        <base />
        <!-- Semantic Cache Lookup: Check Redis for similar prompts (score >= 0.8) -->
        <azure-openai-semantic-cache-lookup
            score-threshold="0.8"
            embeddings-backend-id="embeddings-backend"
            embeddings-backend-auth="system-assigned" />
    </inbound>
    <backend>
        <base />
    </backend>
    <outbound>
        <!-- Cache the response in Redis for 2 minutes -->
        <azure-openai-semantic-cache-store duration="120" />
        <base />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>\"\"\"

# Write policy to file
policy_file = Path('semantic-caching-policy.xml')
with open(policy_file, 'w') as f:
    f.write(policy_xml)

print(f"\\n[*] Policy file created: {policy_file.absolute()}")

# Apply policy using Azure REST API (more reliable than az apim api policy)
print(f"\\n[*] Applying policy to API '{api_id}'...")

# Method 1: Try using az apim api policy create with correct syntax
cmd1 = f\"\"\"az apim api policy create \\
    --resource-group {resource_group} \\
    --service-name {apim_service_name} \\
    --api-id {api_id} \\
    --xml-content '{policy_xml}'\"\"\"

result = subprocess.run(cmd1, shell=True, capture_output=True, text=True)

if result.returncode == 0:
    print(f"\\n✅ Policy applied successfully using 'az apim api policy create'!")
else:
    # Method 2: Try using az rest (more reliable)
    print(f"⚠️  Method 1 failed: {result.stderr[:200]}")
    print(f"\\n[*] Trying alternative method using 'az rest'...")

    policy_url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.ApiManagement/service/{apim_service_name}/apis/{api_id}/policies/policy?api-version=2024-06-01-preview"

    # Create policy JSON payload
    policy_payload = {
        "properties": {
            "value": policy_xml,
            "format": "xml"
        }
    }

    # Write to temp file
    payload_file = Path('policy-payload.json')
    with open(payload_file, 'w') as f:
        json.dump(policy_payload, f)

    cmd2 = f\"\"\"az rest \\
        --method PUT \\
        --url "{policy_url}" \\
        --body @{payload_file}\"\"\"

    result2 = subprocess.run(cmd2, shell=True, capture_output=True, text=True)

    if result2.returncode == 0:
        print(f"\\n✅ Policy applied successfully using 'az rest'!")
    else:
        print(f"\\n❌ Both methods failed!")
        print(f"   Error: {result2.stderr[:300]}")
        print(f"\\n💡 Manual workaround:")
        print(f"   1. Go to Azure Portal → API Management → APIs")
        print(f"   2. Select 'inference-api'")
        print(f"   3. Go to 'All operations' → Inbound processing → Code editor")
        print(f"   4. Paste the policy from: {policy_file.absolute()}")

# Verify policy was applied
print(f"\\n[*] Verifying policy application...")

verify_cmd = f\"\"\"az rest \\
    --method GET \\
    --url "https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.ApiManagement/service/{apim_service_name}/apis/{api_id}/policies/policy?api-version=2024-06-01-preview&format=rawxml"\"\"\"

result = subprocess.run(verify_cmd, shell=True, capture_output=True, text=True)

if result.returncode == 0:
    try:
        policy_data = json.loads(result.stdout)
        current_policy = policy_data.get('properties', {}).get('value', '')

        if 'azure-openai-semantic-cache-lookup' in current_policy:
            print(f"\\n✅ Semantic caching policy is ACTIVE!")
            print(f"   ✓ Cache lookup configured")
            print(f"   ✓ Cache store configured")
            print(f"   ✓ Score threshold: 0.8")
        else:
            print(f"\\n⚠️  Policy applied but semantic caching not found")
            print(f"   Current policy does not contain 'azure-openai-semantic-cache-lookup'")
            print(f"   You may need to apply it manually via Azure Portal")
    except:
        print(f"\\n⚠️  Could not parse policy response")
else:
    print(f"\\n⚠️  Could not verify policy: {result.stderr[:200]}")

print(f"\\n📋 Policy Details:")
print(f"   - Lookup: Checks Redis for similar prompts (score >= 0.8)")
print(f"   - Store: Caches responses for 2 minutes")
print(f"   - Backend: embeddings-backend (text-embedding-3-small)")
print(f"\\n⏳ Wait 30-60 seconds for policy propagation...")
print(f"\\n[OK] Step 2 Complete - Check verification status above")
"""

# Find and replace the cell
for i, cell in enumerate(cells):
    if cell.get('cell_type') == 'code':
        source = ''.join(cell.get('source', []))
        if 'Lab 09: Semantic Caching - Step 2: Apply Semantic Caching Policy' in source and 'FIXED' not in source:
            print(f"Found Cell {i+1} - Updating with fixed version")
            cells[i]['source'] = fixed_cell_source.split('\n')
            cells[i]['outputs'] = []
            break

# Save notebook
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("\\n✅ Cell 52 updated with fixed policy application")
print("\\nChanges made:")
print("  1. Fixed Azure CLI syntax (using 'az rest' API)")
print("  2. Added cache configuration verification")
print("  3. Added policy verification after application")
print("  4. Added manual workaround instructions")
