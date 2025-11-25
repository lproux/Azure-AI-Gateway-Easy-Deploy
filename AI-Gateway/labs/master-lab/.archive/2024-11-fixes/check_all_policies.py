#!/usr/bin/env python3
"""
Check ALL policy levels in APIM to find what might be overriding
"""
import subprocess
import json
import os
from dotenv import load_dotenv

load_dotenv('master-lab.env')

apim_service_id = os.environ.get('APIM_SERVICE_ID')

print("=" * 80)
print("🔍 CHECKING ALL APIM POLICY LEVELS")
print("=" * 80)

# Check API-level policy
print("\n1. API-LEVEL POLICY (inference-api)")
print("-" * 80)
uri = f"https://management.azure.com{apim_service_id}/apis/inference-api/policies/policy?api-version=2023-09-01-preview"
cmd = ['az', 'rest', '--method', 'get', '--uri', uri]
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    policy = result.stdout.strip()
    print(policy[:500] if len(policy) > 500 else policy)
    if 'azure-openai-semantic-cache' in policy:
        print("\n✅ Semantic caching IS in API-level policy")
    else:
        print("\n❌ Semantic caching NOT in API-level policy")
else:
    print(f"❌ Error: {result.stderr}")

# List operations in the API
print("\n\n2. OPERATIONS IN inference-api")
print("-" * 80)
uri = f"https://management.azure.com{apim_service_id}/apis/inference-api/operations?api-version=2023-09-01-preview"
cmd = ['az', 'rest', '--method', 'get', '--uri', uri]
result = subprocess.run(cmd, capture_output=True, text=True)

operations = []
if result.returncode == 0:
    try:
        data = json.loads(result.stdout.encode('utf-8').decode('utf-8-sig').strip())
        operations = data.get('value', [])
        print(f"\nFound {len(operations)} operation(s):\n")
        for op in operations:
            op_id = op.get('name', 'unknown')
            op_name = op.get('properties', {}).get('displayName', 'N/A')
            op_method = op.get('properties', {}).get('method', 'N/A')
            op_url = op.get('properties', {}).get('urlTemplate', 'N/A')
            print(f"  - {op_id}")
            print(f"    Display Name: {op_name}")
            print(f"    Method: {op_method}")
            print(f"    URL: {op_url}\n")
    except Exception as e:
        print(f"Error parsing: {e}")

# Check operation-level policies
print("\n3. OPERATION-LEVEL POLICIES")
print("-" * 80)

for op in operations:
    op_id = op.get('name')
    print(f"\nOperation: {op_id}")
    print("-" * 40)

    uri = f"https://management.azure.com{apim_service_id}/apis/inference-api/operations/{op_id}/policies/policy?api-version=2023-09-01-preview"
    cmd = ['az', 'rest', '--method', 'get', '--uri', uri]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        policy = result.stdout.strip()
        if policy and len(policy) > 10:
            print("✅ HAS operation-level policy:")
            print(policy[:300])
            print("...")
            if 'azure-openai-semantic-cache' in policy:
                print("\n✅ Contains semantic caching")
            else:
                print("\n⚠️  DOES NOT contain semantic caching - THIS OVERRIDES API-LEVEL!")
        else:
            print("✅ No operation-level policy (inherits from API level)")
    else:
        # 404 means no operation-level policy, which is good
        if "404" in result.stderr or "Not Found" in result.stderr:
            print("✅ No operation-level policy (inherits from API level)")
        else:
            print(f"❌ Error checking: {result.stderr[:200]}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print("\nIf an operation has its own policy WITHOUT semantic caching,")
print("it will OVERRIDE the API-level policy and semantic caching won't work!")
print("\nSolution: Remove operation-level policies or add semantic caching to them")
print("=" * 80)
