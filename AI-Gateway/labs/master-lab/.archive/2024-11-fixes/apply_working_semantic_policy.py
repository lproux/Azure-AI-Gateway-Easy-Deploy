#!/usr/bin/env python3
"""
Apply semantic caching policy WITHOUT embeddings-backend-auth
Since the backend already has API key credentials configured
"""
import subprocess
import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('master-lab.env')

apim_service_id = os.environ.get('APIM_SERVICE_ID')

if not apim_service_id:
    print("❌ APIM_SERVICE_ID not found in master-lab.env")
    exit(1)

print("=" * 80)
print("🔧 APPLYING SEMANTIC CACHING POLICY (API KEY AUTH)")
print("=" * 80)
print("\n🔑 Key Fix: Remove embeddings-backend-auth attribute")
print("   Backend already has API key credentials configured")
print("   Let APIM use the configured credentials automatically\n")

# Corrected policy WITHOUT embeddings-backend-auth
policy_xml = """<policies>
    <inbound>
        <base />
        <check-header name="api-key" failed-check-httpcode="401" failed-check-error-message="Missing or invalid API key" />
        <azure-openai-semantic-cache-lookup
            score-threshold="0.8"
            embeddings-backend-id="embeddings-backend" />
        <set-backend-service backend-id="inference-backend-pool" />
    </inbound>
    <backend>
        <retry count="2" interval="0" first-fast-retry="true"
               condition="@(context.Response.StatusCode == 429 || context.Response.StatusCode == 503)">
            <forward-request buffer-request-body="true" />
        </retry>
    </backend>
    <outbound>
        <base />
        <azure-openai-semantic-cache-store duration="1200" />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>"""

# Save policy to file
policy_file = Path('semantic-caching-policy-API-KEY.xml')
with open(policy_file, 'w', encoding='utf-8') as f:
    f.write(policy_xml)

print(f"[*] Policy file created: {policy_file}\n")

print("📋 Key Differences from Previous Attempt:")
print("   ❌ Removed: embeddings-backend-auth=\"system-assigned\"")
print("   ✅ Using: Configured API key credentials from backend")
print("   ✅ Cache duration: 1200s (20 minutes)")
print("   ✅ Backend routing: inference-backend-pool")
print("   ✅ Retry logic: For 429/503 errors\n")

# Apply policy using Azure REST API
uri = f"https://management.azure.com{apim_service_id}/apis/inference-api/policies/policy?api-version=2023-09-01-preview"

body = {
    "properties": {
        "value": policy_xml,
        "format": "xml"
    }
}

# Save body to temp file
body_file = Path('/tmp/semantic-policy-apikey.json')
with open(body_file, 'w', encoding='utf-8') as f:
    json.dump(body, f, indent=2)

print(f"[*] Applying semantic caching policy...")

cmd = [
    'az', 'rest',
    '--method', 'put',
    '--uri', uri,
    '--body', f'@{body_file}'
]

result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("\n✅ Semantic caching policy applied successfully!\n")

    print("📋 Policy Configuration:")
    print("   - Similarity Threshold: 0.8 (80% match required)")
    print("   - Cache Duration: 1200 seconds (20 minutes)")
    print("   - Embeddings Backend: embeddings-backend")
    print("   - Embeddings Auth: API Key (from backend credentials)")
    print("   - Backend Pool: inference-backend-pool")
    print("   - Redis Cache: Enabled\n")

    print("⏳ Wait 30-60 seconds for policy to propagate...\n")

    print("🎯 Expected Results:")
    print("   ✅ Cell 53: First request slow, subsequent FAST")
    print("   ✅ Cell 54: 15-20x speed improvement")
    print("   ✅ Cell 62: Embeddings generate without 500 errors")
    print("   ✅ Cell 63: Vector search works")
    print("   ✅ No more 500 internal server errors\n")

else:
    print(f"\n❌ Error applying policy:")
    print(result.stderr)
    exit(1)

print("=" * 80)
print("Next Steps:")
print("1. Wait 60 seconds for policy propagation")
print("2. Re-run Cell 53 (semantic caching test)")
print("3. Expected: 19/20 requests should succeed with cache hits")
print("4. Re-run Cell 62 (vector search)")
print("5. Expected: All embeddings should generate successfully")
print("=" * 80)
