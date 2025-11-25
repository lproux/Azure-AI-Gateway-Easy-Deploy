# ============================================================================
# LAB 03: Load Balancing with Retry Logic
# ============================================================================

print("\n" + "="*80)
print("LAB 03: Load Balancing Configuration")
print("="*80 + "\n")

import requests
from azure.identity import DefaultAzureCredential

# Configuration
backend_id = "inference-backend-pool"
subscription_id = os.environ.get('SUBSCRIPTION_ID')
resource_group = os.environ.get('RESOURCE_GROUP')
apim_service_name = os.environ.get('APIM_SERVICE_NAME')
api_id = os.environ.get('APIM_API_ID', 'inference-api')

print(f"[policy] Backend Pool: {backend_id}")
print(f"[policy] Subscription ID: {subscription_id}")
print(f"[policy] Using API ID: {api_id}")

# Load balancing policy with API-KEY authentication and retry logic
policy_xml = f"""<policies>
    <inbound>
        <base />
        <check-header name="api-key" failed-check-httpcode="401"
                      failed-check-error-message="Missing or invalid API key" />
        <set-backend-service backend-id="{backend_id}" />
    </inbound>
    <backend>
        <retry count="2" interval="0" first-fast-retry="true"
               condition="@(context.Response.StatusCode == 429 || context.Response.StatusCode == 503)">
            <forward-request buffer-request-body="true" />
        </retry>
    </backend>
    <outbound>
        <base />
    </outbound>
    <on-error>
        <base />
        <choose>
            <when condition="@(context.Response.StatusCode == 503)">
                <return-response>
                    <set-status code="503" reason="Service Unavailable" />
                    <set-header name="Content-Type" exists-action="override">
                        <value>application/json</value>
                    </set-header>
                    <set-body>{{"error": {{"code": "ServiceUnavailable", "message": "Service temporarily unavailable"}}}}</set-body>
                </return-response>
            </when>
        </choose>
    </on-error>
</policies>"""

# Apply policy using direct REST API
print("[policy] Applying load-balancing via REST API...")

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
print("[INFO] Load balancing will distribute requests across backend pool")
print("[INFO] Retry logic will handle 429 (rate limit) and 503 (unavailable) errors")
print("[NEXT] Run load balancing tests in cells below\n")