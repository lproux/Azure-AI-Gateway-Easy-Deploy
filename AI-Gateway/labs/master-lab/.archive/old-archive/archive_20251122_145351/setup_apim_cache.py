#!/usr/bin/env python3
"""
Connect Redis to APIM as a cache resource for semantic caching
"""
import os
import subprocess
import json
from pathlib import Path
from dotenv import load_dotenv

print("="*80)
print("🔧 Connecting Redis to APIM for Semantic Caching")
print("="*80)

# Load environment
env_file = Path('master-lab.env')
if not env_file.exists():
    print("\n❌ master-lab.env not found!")
    exit(1)

load_dotenv(env_file)

# Get variables
apim_service_name = os.environ.get('APIM_SERVICE_NAME')
resource_group = os.environ.get('RESOURCE_GROUP')
subscription_id = os.environ.get('SUBSCRIPTION_ID')
redis_host = os.environ.get('REDIS_HOST')
redis_port = os.environ.get('REDIS_PORT')
redis_key = os.environ.get('REDIS_KEY')

print(f"\n📋 Configuration:")
print(f"   APIM: {apim_service_name}")
print(f"   Redis: {redis_host}:{redis_port}")
print(f"   Resource Group: {resource_group}")
print(f"   Subscription: {subscription_id}")

if not all([apim_service_name, resource_group, subscription_id, redis_host, redis_port, redis_key]):
    print("\n❌ Missing required environment variables!")
    exit(1)

# Create cache payload
cache_url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.ApiManagement/service/{apim_service_name}/caches/default?api-version=2024-06-01-preview"

cache_payload = {
    "properties": {
        "connectionString": f"{redis_host}:{redis_port},password={redis_key},ssl=True,abortConnect=False",
        "useFromLocation": "default",
        "description": "Redis cache for semantic caching"
    }
}

# Write to temp file
payload_file = Path('/tmp/apim-cache-payload.json')
with open(payload_file, 'w') as f:
    json.dump(cache_payload, f, indent=2)

print(f"\n[*] Connecting Redis to APIM...")

# Create cache using Azure REST API
cmd = f"""az rest \
    --method PUT \
    --url "{cache_url}" \
    --body @{payload_file}"""

result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

if result.returncode == 0:
    print(f"\n✅ Redis cache connected to APIM successfully!")
    print(f"\n📋 Cache Details:")
    try:
        response = json.loads(result.stdout)
        print(f"   Name: {response.get('name', 'default')}")
        print(f"   Type: {response.get('type', 'N/A')}")
        print(f"   Connection: {redis_host}:{redis_port}")
    except:
        print(f"   Cache created successfully")

    print(f"\n✨ Next steps:")
    print(f"  1. Reopen your notebook (to reload env with SUBSCRIPTION_ID)")
    print(f"  2. Run Cell 51 (Configure Embeddings Backend)")
    print(f"  3. Run Cell 52 (Apply Semantic Caching Policy) - now fixed!")
    print(f"  4. Run Cell 53 (Test Semantic Caching)")
    print(f"\n📊 Expected results:")
    print(f"  - First request: 1-2 seconds (backend call, generates embedding)")
    print(f"  - Similar requests: 0.1-0.3 seconds (cache hits)")
    print(f"  - Cache hit rate: 70-90% for similar questions")

else:
    print(f"\n❌ Failed to connect Redis cache")
    print(f"   Error: {result.stderr[:300]}")
    print(f"\n💡 Manual workaround:")
    print(f"  1. Go to Azure Portal → API Management")
    print(f"  2. Select '{apim_service_name}'")
    print(f"  3. Navigate to: External cache → Caches")
    print(f"  4. Click '+ Add'")
    print(f"  5. Enter:")
    print(f"     Cache instance identifier: default")
    print(f"     Use from: Default")
    print(f"     Connection string: {redis_host}:{redis_port},password=***,ssl=True,abortConnect=False")

# Cleanup
try:
    payload_file.unlink()
except:
    pass

print(f"\n{'='*80}")
