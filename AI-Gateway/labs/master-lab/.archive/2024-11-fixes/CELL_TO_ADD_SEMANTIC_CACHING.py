# CELL TO ADD: Apply Semantic Caching Policy
# Insert this cell BEFORE cell 53 (semantic caching test)
# This applies the semantic caching policy directly in the notebook

import os, subprocess, json
from pathlib import Path
from dotenv import load_dotenv

env_file = Path('master-lab.env')
if env_file.exists():
    load_dotenv(env_file)

apim_service_id = os.environ.get('APIM_SERVICE_ID')

print("=" * 80)
print("🔧 APPLYING SEMANTIC CACHING POLICY (from notebook)")
print("=" * 80)

# Policy WITHOUT embeddings-backend-auth (uses API key from backend config)
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

uri = f"https://management.azure.com{apim_service_id}/apis/inference-api/policies/policy?api-version=2023-09-01-preview"

body = {
    "properties": {
        "value": policy_xml,
        "format": "xml"
    }
}

body_file = '/tmp/semantic-cache-from-notebook.json'
with open(body_file, 'w', encoding='utf-8') as f:
    json.dump(body, f, indent=2)

print("\n[*] Applying semantic caching policy to APIM...")

cmd = ['az', 'rest', '--method', 'put', '--uri', uri, '--body', f'@{body_file}']
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("\n✅ Semantic caching policy applied successfully!\n")
    print("📋 Policy Configuration:")
    print("   - Similarity Threshold: 0.8 (80% match)")
    print("   - Cache Duration: 1200s (20 minutes)")
    print("   - Embeddings Backend: embeddings-backend")
    print("   - Auth: API Key (from backend credentials)")
    print("   - Backend Pool: inference-backend-pool\n")
    print("⏳ Waiting 10 seconds for propagation...")
    import time
    time.sleep(10)
    print("✅ Ready to test!\n")
else:
    print(f"\n❌ Error applying policy:")
    print(result.stderr)
    raise Exception("Failed to apply policy")

print("=" * 80)
