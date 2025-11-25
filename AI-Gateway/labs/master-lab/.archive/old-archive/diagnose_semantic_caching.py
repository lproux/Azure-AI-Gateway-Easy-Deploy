#!/usr/bin/env python3
"""
Diagnose Semantic Caching Setup
Checks all prerequisites for semantic caching to work
"""
import os
import subprocess
import json
from pathlib import Path
from dotenv import load_dotenv

print("="*80)
print("🔍 SEMANTIC CACHING DIAGNOSTICS")
print("="*80)

# Load environment
env_file = Path('master-lab.env')
if not env_file.exists():
    print("\n❌ master-lab.env not found!")
    print("   Run Cell 021 to generate it")
    exit(1)

load_dotenv(env_file)

# Get variables
apim_service_name = os.environ.get('APIM_SERVICE_NAME')
resource_group = os.environ.get('RESOURCE_GROUP')
subscription_id = os.environ.get('SUBSCRIPTION_ID')
redis_host = os.environ.get('REDIS_HOST')
redis_port = os.environ.get('REDIS_PORT')
redis_key = os.environ.get('REDIS_KEY')
api_id = os.environ.get('APIM_API_ID', 'inference-api')

print(f"\n📋 Configuration:")
print(f"   APIM Service: {apim_service_name}")
print(f"   Resource Group: {resource_group}")
print(f"   Redis Host: {redis_host}")
print(f"   Redis Port: {redis_port}")
print(f"   API ID: {api_id}")

# Check 1: Redis deployment
print(f"\n{'='*80}")
print("✓ CHECK 1: Redis Deployment")
print(f"{'='*80}")

if redis_host and redis_port and redis_key:
    print("✅ Redis credentials found in environment")
    print(f"   Host: {redis_host}")
    print(f"   Port: {redis_port}")
    print(f"   Key: ***{redis_key[-8:] if redis_key else 'None'}")
else:
    print("❌ Redis credentials missing!")
    print("   Semantic caching requires Redis to be deployed")

# Check 2: APIM Cache Resource
print(f"\n{'='*80}")
print("✓ CHECK 2: APIM Cache Configuration")
print(f"{'='*80}")

cmd = f"""az apim cache list \
    --service-name {apim_service_name} \
    --resource-group {resource_group} \
    -o json"""

result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

cache_configured = False
if result.returncode == 0:
    caches = json.loads(result.stdout) if result.stdout else []
    if caches:
        print(f"✅ APIM cache found:")
        for cache in caches:
            print(f"   Name: {cache.get('name', 'N/A')}")
            print(f"   Description: {cache.get('description', 'N/A')}")
            print(f"   Connection String: {cache.get('connectionString', 'N/A')[:50]}...")
            cache_configured = True
    else:
        print("❌ No cache configured in APIM!")
        print("\n💡 FIX: Redis needs to be connected to APIM as a cache resource")
        print("   Run this command:")
        print(f"""
   az apim cache create \\
       --service-name {apim_service_name} \\
       --resource-group {resource_group} \\
       --cache-id default \\
       --connection-string "{redis_host}:{redis_port},password={redis_key[:10]}***,ssl=True,abortConnect=False" \\
       --description "Redis cache for semantic caching"
        """)
else:
    print(f"⚠️  Could not check cache: {result.stderr[:200]}")

# Check 3: Embeddings Backend
print(f"\n{'='*80}")
print("✓ CHECK 3: Embeddings Backend")
print(f"{'='*80}")

cmd = f"""az apim backend show \
    --service-name {apim_service_name} \
    --resource-group {resource_group} \
    --backend-id embeddings-backend \
    -o json"""

result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

backend_configured = False
if result.returncode == 0:
    backend = json.loads(result.stdout) if result.stdout else {}
    if backend:
        print(f"✅ Embeddings backend found:")
        print(f"   Backend ID: embeddings-backend")
        print(f"   URL: {backend.get('url', 'N/A')}")
        print(f"   Protocol: {backend.get('protocol', 'N/A')}")
        backend_configured = True
    else:
        print("❌ Embeddings backend not found!")
else:
    print("❌ Embeddings backend not configured!")
    print("\n💡 FIX: Run Cell 51 (Configure Embeddings Backend)")

# Check 4: API Policy
print(f"\n{'='*80}")
print("✓ CHECK 4: Semantic Caching Policy")
print(f"{'='*80}")

cmd = f"""az rest \
    --method GET \
    --url "https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.ApiManagement/service/{apim_service_name}/apis/{api_id}/policies/policy?api-version=2024-06-01-preview&format=rawxml" """

result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

policy_configured = False
if result.returncode == 0:
    try:
        policy_data = json.loads(result.stdout)
        current_policy = policy_data.get('properties', {}).get('value', '')

        if 'azure-openai-semantic-cache-lookup' in current_policy:
            print("✅ Semantic caching policy is ACTIVE!")
            print("   ✓ azure-openai-semantic-cache-lookup found")
            print("   ✓ azure-openai-semantic-cache-store found" if 'azure-openai-semantic-cache-store' in current_policy else "   ⚠️  cache-store not found")
            policy_configured = True
        else:
            print("❌ Semantic caching policy NOT found in API policy")
            print("\n💡 FIX: Run Cell 52 (Apply Semantic Caching Policy)")
            print("   Or manually add via Azure Portal")
    except Exception as e:
        print(f"⚠️  Could not parse policy: {e}")
else:
    print(f"❌ Could not retrieve policy: {result.stderr[:200]}")

# Final Summary
print(f"\n{'='*80}")
print("📊 DIAGNOSTIC SUMMARY")
print(f"{'='*80}")

checks = {
    "Redis Deployed": bool(redis_host and redis_port and redis_key),
    "APIM Cache Configured": cache_configured,
    "Embeddings Backend": backend_configured,
    "Semantic Cache Policy": policy_configured
}

all_ok = all(checks.values())

for check, status in checks.items():
    icon = "✅" if status else "❌"
    print(f"{icon} {check}")

print(f"\n{'='*80}")
if all_ok:
    print("✅ ALL CHECKS PASSED - Semantic caching should work!")
    print("\nIf you're still not seeing cache hits:")
    print("  1. Ensure questions are semantically similar (>80% similarity)")
    print("  2. Wait 60 seconds for policy propagation")
    print("  3. Check that first request completes successfully")
    print("  4. Verify Redis has enough capacity (not returning 429)")
else:
    print("❌ SEMANTIC CACHING NOT FULLY CONFIGURED")
    print("\nRequired fixes:")

    if not cache_configured:
        print("\n🔧 FIX 1: Connect Redis to APIM")
        print(f"""
Run this command:

az apim cache create \\
    --service-name {apim_service_name} \\
    --resource-group {resource_group} \\
    --cache-id default \\
    --connection-string "{redis_host}:{redis_port},password={redis_key},ssl=True,abortConnect=False" \\
    --description "Redis cache for semantic caching"
        """)

    if not backend_configured:
        print("\n🔧 FIX 2: Configure Embeddings Backend")
        print("   Run Cell 51 in the notebook")

    if not policy_configured:
        print("\n🔧 FIX 3: Apply Semantic Caching Policy")
        print("   Run Cell 52 in the notebook (now fixed)")

print(f"\n{'='*80}")
