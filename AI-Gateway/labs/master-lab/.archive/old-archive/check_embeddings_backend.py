#!/usr/bin/env python3
"""
Check if embeddings-backend exists in APIM
"""
import os
import subprocess
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment
env_file = Path('master-lab.env')
load_dotenv(env_file)

apim_service_name = os.environ.get('APIM_SERVICE_NAME')
resource_group = os.environ.get('RESOURCE_GROUP')
subscription_id = os.environ.get('SUBSCRIPTION_ID')

print("="*80)
print("🔍 Checking Embeddings Backend")
print("="*80)

# Check if embeddings-backend exists
url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.ApiManagement/service/{apim_service_name}/backends/embeddings-backend?api-version=2024-06-01-preview"

cmd = f'az rest --method GET --url "{url}"'

result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

if result.returncode == 0:
    print("\n✅ Embeddings backend EXISTS!")
    backend = json.loads(result.stdout)
    print(f"   URL: {backend.get('properties', {}).get('url', 'N/A')}")
    print(f"   Protocol: {backend.get('properties', {}).get('protocol', 'N/A')}")
else:
    print("\n❌ Embeddings backend DOES NOT EXIST!")
    print(f"   Error: {result.stderr[:200]}")
    print("\n💡 This is why semantic caching isn't working!")
    print("   The policy references 'embeddings-backend' but it doesn't exist.")
    print("\n🔧 FIX: Create it manually (instructions below)")

print("\n" + "="*80)
