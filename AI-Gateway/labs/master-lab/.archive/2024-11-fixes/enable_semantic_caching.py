#!/usr/bin/env python3
"""
Re-enable semantic caching with corrected embeddings backend URL
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
api_id = 'inference-api'

# Get embedding model endpoint from master-lab.env
embedding_endpoint = os.environ.get('MODEL_TEXT_EMBEDDING_3_SMALL_ENDPOINT_R1')
embedding_key = os.environ.get('MODEL_TEXT_EMBEDDING_3_SMALL_KEY_R1')
redis_host = os.environ.get('REDIS_HOST')
redis_port = os.environ.get('REDIS_PORT')
redis_key = os.environ.get('REDIS_KEY')

print("=" * 80)
print("🔧 ENABLING SEMANTIC CACHING")
print("=" * 80)
print(f"\nAPIM Service: {apim_service_name}")
print(f"Resource Group: {resource_group}")
print(f"API ID: {api_id}")

# Step 1: Create embeddings backend with CORRECT URL
print("\n" + "=" * 80)
print("STEP 1: Creating Embeddings Backend")
print("=" * 80)

# Correct URL format (note the /openai/ part)
backend_url = f"{embedding_endpoint}openai/deployments/text-embedding-3-small/embeddings"
print(f"\nBackend URL: {backend_url}")
print(f"Backend ID: embeddings-backend")

# Check if backend exists
check_cmd = [
    'az', 'apim', 'backend', 'show',
    '--service-name', apim_service_name,
    '--resource-group', resource_group,
    '--backend-id', 'embeddings-backend'
]

print("\n[*] Checking if backend exists...")
result = subprocess.run(check_cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("   Backend already exists, updating...")
    cmd = [
        'az', 'apim', 'backend', 'update',
        '--service-name', apim_service_name,
        '--resource-group', resource_group,
        '--backend-id', 'embeddings-backend',
        '--url', backend_url,
        '--protocol', 'http',
        '--description', 'Embeddings Backend for Semantic Caching'
    ]
else:
    print("   Creating new backend...")
    cmd = [
        'az', 'apim', 'backend', 'create',
        '--service-name', apim_service_name,
        '--resource-group', resource_group,
        '--backend-id', 'embeddings-backend',
        '--url', backend_url,
        '--protocol', 'http',
        '--description', 'Embeddings Backend for Semantic Caching'
    ]

result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("\n✅ Embeddings backend created/updated successfully!")
else:
    print(f"\n❌ Failed to create backend")
    print(f"   Error: {result.stderr}")
    exit(1)

# Step 2: Create semantic caching policy
print("\n" + "=" * 80)
print("STEP 2: Creating Semantic Caching Policy")
print("=" * 80)

# Create the policy XML with semantic caching
policy_xml = f"""<policies>
    <inbound>
        <base />
        <check-header name="api-key" failed-check-httpcode="401" failed-check-error-message="Missing or invalid API key" />
        <azure-openai-semantic-cache-lookup score-threshold="0.8" embeddings-backend-id="embeddings-backend" ignore-system-messages="true" max-message-count="10">
            <vary-by>@(context.Subscription.Id)</vary-by>
        </azure-openai-semantic-cache-lookup>
        <set-backend-service backend-id="inference-backend-pool" />
    </inbound>
    <backend>
        <retry count="2" interval="0" first-fast-retry="true" condition="@(context.Response.StatusCode == 429 || context.Response.StatusCode == 503)">
            <forward-request buffer-request-body="true" />
        </retry>
    </backend>
    <outbound>
        <base />
        <azure-openai-semantic-cache-store duration="120" />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>"""

# Save policy to file
policy_file = Path('semantic-caching-policy-corrected.xml')
with open(policy_file, 'w') as f:
    f.write(policy_xml)

print(f"\n[*] Policy file created: {policy_file}")

# Apply policy using az rest
print("\n[*] Applying semantic caching policy...")

# Get APIM service ID
apim_service_id = os.environ.get('APIM_SERVICE_ID')

# Create request body
body = {
    "properties": {
        "value": policy_xml,
        "format": "xml"
    }
}

# Write body to temp file
with open('/tmp/semantic-policy-body.json', 'w') as f:
    json.dump(body, f)

# Use az rest to update policy
uri = f"https://management.azure.com{apim_service_id}/apis/{api_id}/policies/policy?api-version=2023-09-01-preview"

cmd = [
    'az', 'rest',
    '--method', 'put',
    '--uri', uri,
    '--body', '@/tmp/semantic-policy-body.json',
    '--headers', 'Content-Type=application/json'
]

result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("\n✅ Semantic caching policy applied successfully!")
    print("\n📋 Policy Configuration:")
    print("   - Similarity Threshold: 0.8 (80% match required)")
    print("   - Cache Duration: 120 seconds (2 minutes)")
    print("   - Embeddings Model: text-embedding-3-small")
    print("   - Redis Cache: Enabled")
    print("\n⏳ Wait 30-60 seconds for policy to propagate...")
    print("\n🎯 Next: Run cells 53-54 to test semantic caching!")
else:
    print(f"\n❌ Failed to apply policy")
    print(f"   Error: {result.stderr}")
    exit(1)

print("\n" + "=" * 80)
print("✅ SEMANTIC CACHING ENABLED!")
print("=" * 80)
print("\nHow it works:")
print("1. First similar request: ~3-10s (backend call + embedding + cache store)")
print("2. Subsequent similar requests: ~0.1-0.3s (cache hit)")
print("3. Similar questions (>80% match) return cached responses")
print("\nExample similar questions:")
print("  • 'How to brew coffee?'")
print("  • 'What are the steps to make coffee?'")
print("  • 'Explain how to create coffee'")
print("  → All return the same cached response!")
print("\n" + "=" * 80)
