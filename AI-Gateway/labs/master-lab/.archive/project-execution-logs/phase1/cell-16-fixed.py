# ============================================================================
# LAB 01: Semantic Caching with Azure Redis
# ============================================================================
# FIXED 2025-11-17: Enhanced validation and error handling
# Changes:
# 1. Added environment variable validation
# 2. Added policy verification after application
# 3. Better error messages and diagnostics
# 4. Added backend validation

print("\n" + "="*80)
print("LAB 01: Semantic Caching Configuration")
print("="*80 + "\n")

import requests
from azure.identity import DefaultAzureCredential
import os

# Configuration with validation
required_vars = {
    'SUBSCRIPTION_ID': os.environ.get('SUBSCRIPTION_ID'),
    'RESOURCE_GROUP': os.environ.get('RESOURCE_GROUP'),
    'APIM_SERVICE_NAME': os.environ.get('APIM_SERVICE_NAME')
}

# Validate required environment variables
missing_vars = [k for k, v in required_vars.items() if not v]
if missing_vars:
    print(f"[ERROR] Missing required environment variables: {', '.join(missing_vars)}")
    print("[INFO] Please ensure these are set in your environment")
    raise ValueError(f"Missing environment variables: {missing_vars}")

subscription_id = required_vars['SUBSCRIPTION_ID']
resource_group = required_vars['RESOURCE_GROUP']
apim_service_name = required_vars['APIM_SERVICE_NAME']

# Optional variables with defaults
backend_id = os.environ.get('APIM_BACKEND_ID', 'inference-backend-pool')
embeddings_backend_id = os.environ.get('EMBEDDINGS_BACKEND_ID', 'foundry1')
api_id = os.environ.get('APIM_API_ID', 'inference-api')

print(f"[config] Backend ID: {backend_id}")
print(f"[config] Embeddings Backend ID: {embeddings_backend_id}")
print(f"[config] Subscription ID: {subscription_id[:8]}...")
print(f"[config] Resource Group: {resource_group}")
print(f"[config] APIM Service: {apim_service_name}")
print(f"[config] API ID: {api_id}")
print()

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
print("[policy] Applying semantic-cache policy via Azure Management API...")

try:
    # Get Azure credentials
    credential = DefaultAzureCredential()
    token = credential.get_token("https://management.azure.com/.default")

    # Construct API Management URL
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

    # Apply policy
    response = requests.put(url, headers=headers, json=body, timeout=60)

    if response.status_code in [200, 201]:
        print(f"[policy] ✅ Status: {response.status_code} - Policy applied successfully")

        # ADDED: Verify policy was applied
        print("[policy] Verifying policy application...")
        verify_response = requests.get(url, headers=headers, timeout=30)

        if verify_response.status_code == 200:
            applied_policy = verify_response.json()
            if 'azure-openai-semantic-cache-lookup' in applied_policy.get('properties', {}).get('value', ''):
                print("[policy] ✅ Verification: Semantic caching policy confirmed active")
            else:
                print("[policy] ⚠️  Verification: Policy applied but semantic caching not found")
        else:
            print(f"[policy] ⚠️  Verification failed: {verify_response.status_code}")

    elif response.status_code == 404:
        print(f"[policy] ❌ Status: 404 - API not found")
        print(f"[policy] API ID '{api_id}' does not exist in APIM service '{apim_service_name}'")
        print(f"[policy] Available APIs can be listed with Cell 21 (API discovery)")

    elif response.status_code == 401:
        print(f"[policy] ❌ Status: 401 - Authentication failed")
        print(f"[policy] Ensure DefaultAzureCredential has access to the subscription")

    elif response.status_code == 400:
        print(f"[policy] ❌ Status: 400 - Bad request")
        print(f"[policy] Error: {response.text[:500]}")
        print(f"[policy] Check that backend IDs exist:")
        print(f"[policy]   - Backend pool: {backend_id}")
        print(f"[policy]   - Embeddings backend: {embeddings_backend_id}")

    else:
        print(f"[policy] ❌ Status: {response.status_code} - Failed")
        print(f"[policy] Error: {response.text[:500]}")

except Exception as e:
    print(f"[policy] ❌ ERROR: {type(e).__name__}: {str(e)}")
    print("\n[TROUBLESHOOTING]")
    print("  1. Ensure Azure credentials are configured (az login)")
    print("  2. Verify you have Contributor access to the APIM resource")
    print("  3. Check that APIM service name and resource group are correct")
    print(f"  4. Verify API ID '{api_id}' exists (run Cell 21 for API discovery)")
    print("  5. Ensure embeddings backend exists in APIM")

print("\n[INFO] Policy propagation takes ~30-60 seconds")
print("[NEXT] Run the test cells below to verify semantic caching behavior")
print("       - First request: Cache MISS (full latency)")
print("       - Second request: Cache HIT (near-instant response)")
print()
