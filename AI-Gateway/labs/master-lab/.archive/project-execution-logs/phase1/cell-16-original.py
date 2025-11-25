# ============================================================================
# LAB 01: Semantic Caching with Azure Redis
# ============================================================================

print("\n" + "="*80)
print("LAB 01: Semantic Caching Configuration")
print("="*80 + "\n")

import requests
from azure.identity import DefaultAzureCredential

# Configuration
backend_id = "inference-backend-pool"
embeddings_backend_id = "foundry1"
subscription_id = os.environ.get('SUBSCRIPTION_ID')
resource_group = os.environ.get('RESOURCE_GROUP')
apim_service_name = os.environ.get('APIM_SERVICE_NAME')
api_id = os.environ.get('APIM_API_ID', 'inference-api')

print(f"[policy] Backend ID: {backend_id}")
print(f"[policy] Embeddings Backend ID: {embeddings_backend_id}")
print(f"[policy] Subscription ID: {subscription_id}")
print(f"[policy] Using API ID: {api_id}")

# Semantic caching policy with API-KEY authentication
policy_xml = f"""<policies>
    <inbound>
        <base />
        <check-header name="api-key" failed-check-httpcode="401"
                      failed-check-error-message="Missing or invalid API key" />
        <azure-openai-semantic-cache-lookup
            score-threshold="0.8"
            embeddings-backend-id="{embeddings_backend_id}"
            embeddings-backend-auth="system-assigned" />
        <set-backend-service backend-id="{backend_id}" />
    </inbound>
    <backend>
        <base />
    </backend>
    <outbound>
        <azure-openai-semantic-cache-store duration="120" />
        <base />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>"""

# Apply policy using direct REST API
print("[policy] Applying semantic-cache via REST API...")

try:
    credential = DefaultAzureCredential()
    token = credential.get_token("https://management.azure.com/.default")

    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.ApiManagement/service/{apim_service_name}/apis/{api_id}/policies/policy?api-version=2022-08-01"

    headers = {
        "Authorization": f"Bearer {token.token}",
        "Content-Type": "application/json"
    }

    body = {
        "properties": {
            "value": policy_xml,
            "format": "xml"
        }
    }

    response = requests.put(url, headers=headers, json=body, timeout=60)

    if response.status_code in [200, 201]:
        print(f"[policy] Status: {response.status_code} - SUCCESS")
    else:
        print(f"[policy] Status: {response.status_code} - FAILED")
        print(f"[policy] Error: {response.text[:500]}")

except Exception as e:
    print(f"[policy] ERROR: {str(e)}")

print("\n[OK] Policy application complete")
print("[INFO] Policy will take ~30-60 seconds to propagate")
print("[NEXT] Run the cells below to test semantic caching behavior\n")