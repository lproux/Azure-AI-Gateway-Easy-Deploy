#!/usr/bin/env python3
"""
Create embeddings backend in APIM manually
Since Azure CLI is broken, we'll use direct REST API calls
"""
import os
import subprocess
import json
from pathlib import Path
from dotenv import load_dotenv

print("="*80)
print("🔧 Creating Embeddings Backend in APIM")
print("="*80)

# Load environment
env_file = Path('master-lab.env')
load_dotenv(env_file)

# Get configuration
apim_service_name = os.environ.get('APIM_SERVICE_NAME')
resource_group = os.environ.get('RESOURCE_GROUP')
subscription_id = os.environ.get('SUBSCRIPTION_ID')
embedding_endpoint = os.environ.get('MODEL_TEXT_EMBEDDING_3_SMALL_ENDPOINT_R1')

print(f"\n📋 Configuration:")
print(f"   APIM: {apim_service_name}")
print(f"   Resource Group: {resource_group}")
print(f"   Subscription: {subscription_id}")
print(f"   Embedding Endpoint: {embedding_endpoint}")

if not all([apim_service_name, resource_group, subscription_id, embedding_endpoint]):
    print("\n❌ Missing required environment variables!")
    exit(1)

# Create backend URL
backend_url = f"{embedding_endpoint.rstrip('/')}openai/deployments/text-embedding-3-small/embeddings"

print(f"\n[*] Creating embeddings backend...")
print(f"    Backend ID: embeddings-backend")
print(f"    URL: {backend_url}")

# Backend configuration
api_url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.ApiManagement/service/{apim_service_name}/backends/embeddings-backend?api-version=2024-06-01-preview"

backend_payload = {
    "properties": {
        "url": backend_url,
        "protocol": "http",
        "description": "Text Embedding Backend for Semantic Caching",
        "tls": {
            "validateCertificateChain": True,
            "validateCertificateName": True
        }
    }
}

# Write to temp file
payload_file = Path('/tmp/embeddings-backend-payload.json')
with open(payload_file, 'w') as f:
    json.dump(backend_payload, f, indent=2)

print(f"\n[*] Payload:")
print(json.dumps(backend_payload, indent=2))

# Create backend using Azure REST API
cmd = f"""az rest \
    --method PUT \
    --url "{api_url}" \
    --body @{payload_file}"""

print(f"\n[*] Executing REST API call...")

result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

if result.returncode == 0:
    print(f"\n✅ Embeddings backend created successfully!")
    try:
        response = json.loads(result.stdout)
        print(f"\n📋 Backend Details:")
        print(f"   Name: {response.get('name', 'embeddings-backend')}")
        print(f"   Type: {response.get('type', 'N/A')}")
        print(f"   URL: {response.get('properties', {}).get('url', 'N/A')}")
    except:
        print(f"   Backend created")

    print(f"\n✨ Next steps:")
    print(f"  1. The embeddings backend is now configured")
    print(f"  2. The semantic caching policy should now work")
    print(f"  3. Restart your kernel to reload master-lab.env with SUBSCRIPTION_ID")
    print(f"  4. Run Cell 53 again to test semantic caching")
    print(f"\n📊 Expected results:")
    print(f"  - First request: 1-2 seconds")
    print(f"  - Similar requests: 0.1-0.3 seconds (CACHE HITS!)")
    print(f"  - Cache hit rate: 70-90%")

else:
    print(f"\n❌ Failed to create embeddings backend")
    print(f"   Error: {result.stderr[:500]}")

    print(f"\n💡 MANUAL WORKAROUND (Azure Portal):")
    print(f"  1. Go to: https://portal.azure.com")
    print(f"  2. Navigate to: API Management → {apim_service_name}")
    print(f"  3. Go to: Backends → + Add")
    print(f"  4. Fill in:")
    print(f"     - Type: HTTP(S)")
    print(f"     - Name: embeddings-backend")
    print(f"     - Runtime URL: {backend_url}")
    print(f"     - Protocol: HTTP")
    print(f"  5. Click Create")
    print(f"\n  Then run Cell 53 again!")

# Cleanup
try:
    payload_file.unlink()
except:
    pass

print(f"\n{'='*80}")
