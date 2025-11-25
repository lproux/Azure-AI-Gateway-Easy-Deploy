#!/usr/bin/env python3
"""
Apply the CORRECT semantic caching policy based on working semantic-caching.ipynb
Key fix: Use embeddings-backend-auth="system-assigned" for managed identity
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

print("=" * 80)
print("🔧 APPLYING CORRECT SEMANTIC CACHING POLICY")
print("=" * 80)
print("\n🔑 Key Fix: Using system-assigned managed identity for embeddings backend")
print("   (from working semantic-caching.ipynb)")

# Create the CORRECT policy XML matching working notebook
policy_xml = """<policies>
    <inbound>
        <base />
        <check-header name="api-key" failed-check-httpcode="401" failed-check-error-message="Missing or invalid API key" />
        <!-- FIXED: Added embeddings-backend-auth="system-assigned" -->
        <azure-openai-semantic-cache-lookup
            score-threshold="0.8"
            embeddings-backend-id="embeddings-backend"
            embeddings-backend-auth="system-assigned" />
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
        <!-- UPDATED: 20 minutes (1200 seconds) as requested -->
        <azure-openai-semantic-cache-store duration="1200" />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>"""

# Save policy to file
policy_file = Path('semantic-caching-policy-CORRECT.xml')
with open(policy_file, 'w') as f:
    f.write(policy_xml)

print(f"\n[*] Policy file created: {policy_file}")
print("\n📋 Key Changes from Previous Policy:")
print("   ✅ Added: embeddings-backend-auth=\"system-assigned\"")
print("   ✅ Removed: ignore-system-messages attribute")
print("   ✅ Removed: max-message-count attribute")
print("   ✅ Removed: <vary-by> child element")
print("   ✅ Updated: Cache duration from 120s to 1200s (20 minutes)")

print("\n[*] Applying corrected semantic caching policy...")

# Create request body
body = {
    "properties": {
        "value": policy_xml,
        "format": "xml"
    }
}

# Write body to temp file
with open('/tmp/semantic-policy-correct.json', 'w') as f:
    json.dump(body, f)

# Use az rest to update policy
policy_uri = f"https://management.azure.com{apim_service_id}/apis/{api_id}/policies/policy?api-version=2023-09-01-preview"

cmd = [
    'az', 'rest',
    '--method', 'put',
    '--uri', policy_uri,
    '--body', '@/tmp/semantic-policy-correct.json',
    '--headers', 'Content-Type=application/json'
]

result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("\n✅ Corrected semantic caching policy applied successfully!")
    print("\n📋 Policy Configuration:")
    print("   - Similarity Threshold: 0.8 (80% match required)")
    print("   - Cache Duration: 1200 seconds (20 minutes)")
    print("   - Embeddings Backend: embeddings-backend")
    print("   - Embeddings Auth: system-assigned (Managed Identity)")
    print("   - Redis Cache: Enabled")
    print("\n⏳ Wait 30-60 seconds for policy to propagate...")
    print("\n🎯 Expected Fixes:")
    print("   ✅ Cell 53-54: Semantic caching should work without 500 errors")
    print("   ✅ Cell 62-63: Vector search embeddings should work")
    print("   ✅ Cache hits should be much more frequent")
    print("   ✅ Fewer expired keys (20min TTL instead of 2min)")
else:
    print(f"\n❌ Failed to apply policy")
    print(f"   Error: {result.stderr[:200]}")

print("\n" + "=" * 80)
print("Next Steps:")
print("1. Wait 60 seconds for policy propagation")
print("2. Re-run Cell 53 (semantic caching test)")
print("3. Re-run Cell 62 (vector search setup)")
print("4. Check if 500 errors are gone")
print("=" * 80)
