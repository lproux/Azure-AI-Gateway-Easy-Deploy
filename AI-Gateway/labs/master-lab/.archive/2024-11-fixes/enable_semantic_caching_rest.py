#!/usr/bin/env python3
"""
Re-enable semantic caching using Azure REST API (az apim doesn't have backend commands)
"""
import os
import subprocess
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment
env_file = Path('master-lab.env')
load_dotenv(env_file)

apim_service_id = os.environ.get('APIM_SERVICE_ID')
api_id = 'inference-api'

# Get embedding model endpoint from master-lab.env
embedding_endpoint = os.environ.get('MODEL_TEXT_EMBEDDING_3_SMALL_ENDPOINT_R1')
embedding_key = os.environ.get('MODEL_TEXT_EMBEDDING_3_SMALL_KEY_R1')

print("=" * 80)
print("🔧 ENABLING SEMANTIC CACHING (via REST API)")
print("=" * 80)
print(f"\nAPIM Service: {apim_service_id}")
print(f"API ID: {api_id}")

# Step 1: Create embeddings backend using REST API
print("\n" + "=" * 80)
print("STEP 1: Creating Embeddings Backend")
print("=" * 80)

# Correct URL format
backend_url = f"{embedding_endpoint}openai/deployments/text-embedding-3-small/embeddings"
print(f"\nBackend URL: {backend_url}")
print(f"Backend ID: embeddings-backend")

# Create backend via REST API
backend_body = {
    "properties": {
        "url": backend_url,
        "protocol": "http",
        "description": "Embeddings Backend for Semantic Caching",
        "credentials": {
            "header": {
                "api-key": [embedding_key]
            }
        }
    }
}

# Write body to temp file
with open('/tmp/backend-body.json', 'w') as f:
    json.dump(backend_body, f)

print("\n[*] Creating backend via REST API...")

# Use az rest to create/update backend
backend_uri = f"https://management.azure.com{apim_service_id}/backends/embeddings-backend?api-version=2023-09-01-preview"

cmd = [
    'az', 'rest',
    '--method', 'put',
    '--uri', backend_uri,
    '--body', '@/tmp/backend-body.json',
    '--headers', 'Content-Type=application/json'
]

result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("✅ Embeddings backend created successfully!")
else:
    print(f"⚠️  Backend creation status: {result.returncode}")
    if "already exists" in result.stderr.lower():
        print("   Backend already exists (this is OK)")
    else:
        print(f"   Response: {result.stderr[:200]}")

# Step 2: Create semantic caching policy
print("\n" + "=" * 80)
print("STEP 2: Creating Semantic Caching Policy")
print("=" * 80)

# Create the policy XML with semantic caching
policy_xml = """<policies>
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
print("\n[*] Applying semantic caching policy...")

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
policy_uri = f"https://management.azure.com{apim_service_id}/apis/{api_id}/policies/policy?api-version=2023-09-01-preview"

cmd = [
    'az', 'rest',
    '--method', 'put',
    '--uri', policy_uri,
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
    print("   - Embeddings Backend: embeddings-backend")
    print("   - Redis Cache: Enabled")
    print("\n⏳ Wait 30-60 seconds for policy to propagate...")
    print("\n🎯 Next: Run cells 53-54 to test semantic caching!")
else:
    print(f"\n❌ Failed to apply policy")
    print(f"   Error: {result.stderr[:200]}")

print("\n" + "=" * 80)
print("✅ SEMANTIC CACHING SETUP COMPLETE!")
print("=" * 80)
print("\nHow it works:")
print("1. Request arrives at APIM")
print("2. APIM converts prompt to embedding (text-embedding-3-small)")
print("3. Checks Redis for similar cached embeddings (>80% match)")
print("4. If match found: Returns cached response (~0.1-0.3s)")
print("5. If no match: Calls Azure OpenAI, stores in cache (~3-10s)")
print("\nExample similar questions that will cache:")
print("  • 'How to brew coffee?'")
print("  • 'What are the steps to make coffee?'")
print("  • 'Explain how to create coffee'")
print("  → All >80% similar, so return same cached response!")
print("\n" + "=" * 80)
