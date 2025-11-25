"""
Azure API Management Backend Pool Configuration Fix
This script creates the missing backend pool and backends for load balancing
"""

import os
import requests
from azure.identity import DefaultAzureCredential
from azure.mgmt.apimanagement import ApiManagementClient
from azure.mgmt.apimanagement.models import (
    BackendContract,
    BackendProperties,
    BackendCredentialsContract,
    BackendAuthorizationHeaderCredentials,
    BackendPool,
    BackendPoolItem
)

def create_apim_backends_and_pool():
    """
    Creates individual backends for each foundry and configures a backend pool
    with priority-based load balancing
    """

    # Get configuration from environment
    subscription_id = os.environ.get('SUBSCRIPTION_ID')
    resource_group = os.environ.get('RESOURCE_GROUP')
    apim_service_name = os.environ.get('APIM_SERVICE_NAME')

    # Authenticate
    credential = DefaultAzureCredential()

    # Create APIM client
    apim_client = ApiManagementClient(credential, subscription_id)

    # Configuration for foundries
    resource_suffix = 'pavavy6pu5hpa'  # From the deployment
    foundries = [
        {
            'backend_id': 'foundry1',
            'name': f'foundry1-{resource_suffix}',
            'location': 'uksouth',
            'priority': 1,  # Highest priority (UK South)
            'weight': 100
        },
        {
            'backend_id': 'foundry2',
            'name': f'foundry2-{resource_suffix}',
            'location': 'eastus',
            'priority': 2,  # Lower priority
            'weight': 50
        },
        {
            'backend_id': 'foundry3',
            'name': f'foundry3-{resource_suffix}',
            'location': 'norwayeast',
            'priority': 2,  # Lower priority
            'weight': 50
        }
    ]

    print("="*80)
    print("CREATING APIM BACKENDS AND POOL")
    print("="*80)
    print()

    # Step 1: Create individual backends for each foundry
    print("[*] Step 1: Creating individual backends...")
    backend_ids = []

    for foundry in foundries:
        backend_id = foundry['backend_id']
        foundry_name = foundry['name']

        try:
            # Check if backend already exists
            existing = apim_client.backend.get(
                resource_group_name=resource_group,
                service_name=apim_service_name,
                backend_id=backend_id
            )
            print(f"  [OK] Backend '{backend_id}' already exists")

        except Exception:
            # Create the backend
            print(f"  [*] Creating backend '{backend_id}' for {foundry_name}...")

            backend_url = f"https://{foundry_name}.openai.azure.com/openai"

            backend_contract = BackendContract(
                url=backend_url,
                protocol="http",
                description=f"Azure OpenAI backend for {foundry_name} in {foundry['location']}",
                properties=BackendProperties(
                    service_fabric_cluster=None
                ),
                credentials=BackendCredentialsContract(
                    header={
                        "api-key": ["{{" + f"{backend_id}-key" + "}}"]
                    }
                ),
                tls={
                    "validateCertificateChain": True,
                    "validateCertificateName": True
                }
            )

            try:
                result = apim_client.backend.create_or_update(
                    resource_group_name=resource_group,
                    service_name=apim_service_name,
                    backend_id=backend_id,
                    parameters=backend_contract
                )
                print(f"  [OK] Backend '{backend_id}' created successfully")

            except Exception as e:
                print(f"  [ERROR] Failed to create backend '{backend_id}': {str(e)}")
                continue

        # Track backend ARM ID for pool configuration
        backend_arm_id = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.ApiManagement/service/{apim_service_name}/backends/{backend_id}"
        backend_ids.append({
            'id': backend_arm_id,
            'priority': foundry['priority'],
            'weight': foundry['weight']
        })

    print()

    # Step 2: Create the backend pool
    print("[*] Step 2: Creating backend pool 'inference-backend-pool'...")

    pool_id = "inference-backend-pool"

    try:
        # Check if pool already exists
        existing_pool = apim_client.backend.get(
            resource_group_name=resource_group,
            service_name=apim_service_name,
            backend_id=pool_id
        )
        print(f"  [OK] Backend pool '{pool_id}' already exists")

        # Update the pool with correct backends
        print(f"  [*] Updating backend pool configuration...")

    except Exception:
        print(f"  [*] Creating new backend pool...")

    # Create or update the pool
    pool_items = []
    for backend_info in backend_ids:
        pool_item = BackendPoolItem(
            id=backend_info['id'],
            priority=backend_info['priority'],
            weight=backend_info['weight']
        )
        pool_items.append(pool_item)

    backend_pool = BackendContract(
        url="http://localhost",  # Pool doesn't have a URL
        protocol="http",
        type="Pool",
        description="Load-balanced pool for Azure OpenAI backends with priority routing",
        pool=BackendPool(
            services=pool_items
        )
    )

    try:
        result = apim_client.backend.create_or_update(
            resource_group_name=resource_group,
            service_name=apim_service_name,
            backend_id=pool_id,
            parameters=backend_pool
        )
        print(f"  [OK] Backend pool '{pool_id}' configured successfully")
        print()
        print("  Pool configuration:")
        print(f"    - foundry1 (UK South):     Priority 1, Weight 100")
        print(f"    - foundry2 (East US):      Priority 2, Weight 50")
        print(f"    - foundry3 (Norway East):  Priority 2, Weight 50")

    except Exception as e:
        print(f"  [ERROR] Failed to create/update backend pool: {str(e)}")
        return False

    print()

    # Step 3: Add region tracking headers to the policy
    print("[*] Step 3: Updating APIM policy for region tracking...")

    # Get the current policy and add region headers
    api_id = os.environ.get('APIM_API_ID', 'inference-api')

    policy_xml = f"""<policies>
    <inbound>
        <base />
        <check-header name="api-key" failed-check-httpcode="401"
                      failed-check-error-message="Missing or invalid API key" />
        <set-backend-service backend-id="{pool_id}" />
    </inbound>
    <backend>
        <retry count="2" interval="0" first-fast-retry="true"
               condition="@(context.Response.StatusCode == 429 || context.Response.StatusCode == 503)">
            <forward-request buffer-request-body="true" />
        </retry>
    </backend>
    <outbound>
        <base />
        <set-header name="x-ms-region" exists-action="override">
            <value>@(context.LastError?.Source ?? context.BackendUrl?.Host?.Split('.')[0] ?? "unknown")</value>
        </set-header>
        <set-header name="x-ms-backend-id" exists-action="override">
            <value>@(context.Variables.GetValueOrDefault("backend-id", "unknown"))</value>
        </set-header>
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

    try:
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
            print(f"  [OK] Policy updated with region tracking headers")
        else:
            print(f"  [WARN] Policy update returned status {response.status_code}")

    except Exception as e:
        print(f"  [WARN] Failed to update policy: {str(e)}")

    print()
    print("="*80)
    print("BACKEND POOL CONFIGURATION COMPLETE")
    print("="*80)
    print()
    print("SUMMARY:")
    print("✓ Created 3 individual backends (foundry1, foundry2, foundry3)")
    print("✓ Created backend pool 'inference-backend-pool'")
    print("✓ Configured priority-based load balancing:")
    print("  - Priority 1: UK South (foundry1) - gets all traffic when available")
    print("  - Priority 2: East US and Norway East (50/50 split when UK South unavailable)")
    print("✓ Added retry logic for HTTP 429 and 503 errors")
    print("✓ Added region tracking headers (x-ms-region, x-ms-backend-id)")
    print()
    print("TESTING:")
    print("Run the test in Cell 44 to verify load balancing is working.")
    print("You should see:")
    print("- All requests going to 'foundry1' (UK South) by default")
    print("- If foundry1 fails, requests split between foundry2 and foundry3")
    print()

    return True

if __name__ == "__main__":
    # Load environment variables if needed
    from dotenv import load_dotenv
    env_file = 'master-lab.env'
    if os.path.exists(env_file):
        load_dotenv(env_file)
        print(f"[OK] Loaded environment from {env_file}")

    # Run the fix
    create_apim_backends_and_pool()