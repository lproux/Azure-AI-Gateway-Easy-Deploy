# ============================================================================
# FIX: Create Backend Pool for Load Balancing
# ============================================================================
# This cell creates the missing backend pool configuration that enables
# load balancing across multiple Azure OpenAI instances

print("\n" + "="*80)
print("FIX: Creating Backend Pool for Load Balancing")
print("="*80 + "\n")

from azure.mgmt.apimanagement import ApiManagementClient
from azure.mgmt.apimanagement.models import (
    BackendContract,
    BackendPool,
    BackendPoolItem
)

# Initialize APIM client
apim_client = ApiManagementClient(credential, subscription_id)

# Configuration
resource_suffix = 'pavavy6pu5hpa'
backends_config = [
    {'id': 'foundry1', 'url': f'https://foundry1-{resource_suffix}.openai.azure.com/openai',
     'location': 'uksouth', 'priority': 1, 'weight': 100},
    {'id': 'foundry2', 'url': f'https://foundry2-{resource_suffix}.openai.azure.com/openai',
     'location': 'eastus', 'priority': 2, 'weight': 50},
    {'id': 'foundry3', 'url': f'https://foundry3-{resource_suffix}.openai.azure.com/openai',
     'location': 'norwayeast', 'priority': 2, 'weight': 50}
]

print("[*] Step 1: Creating individual backends...")
backend_arm_ids = []

for config in backends_config:
    backend_id = config['id']
    try:
        # Check if backend exists
        existing = apim_client.backend.get(resource_group, apim_service_name, backend_id)
        print(f"  [OK] Backend '{backend_id}' already exists")
    except:
        # Create backend
        print(f"  [*] Creating backend '{backend_id}'...")
        backend = BackendContract(
            url=config['url'],
            protocol="http",
            description=f"Azure OpenAI - {config['location']}",
            tls={"validateCertificateChain": True, "validateCertificateName": True}
        )
        try:
            apim_client.backend.create_or_update(
                resource_group, apim_service_name, backend_id, backend
            )
            print(f"  [OK] Backend '{backend_id}' created")
        except Exception as e:
            print(f"  [ERROR] Failed to create '{backend_id}': {str(e)[:100]}")
            continue

    # Track for pool
    backend_arm_ids.append({
        'id': f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.ApiManagement/service/{apim_service_name}/backends/{backend_id}",
        'priority': config['priority'],
        'weight': config['weight']
    })

print("\n[*] Step 2: Creating backend pool...")
pool_id = "inference-backend-pool"

# Build pool configuration
pool_items = [
    BackendPoolItem(id=b['id'], priority=b['priority'], weight=b['weight'])
    for b in backend_arm_ids
]

backend_pool = BackendContract(
    url="http://localhost",  # Pool URL (not used)
    protocol="http",
    type="Pool",
    description="Load-balanced pool with priority routing",
    pool=BackendPool(services=pool_items)
)

try:
    apim_client.backend.create_or_update(
        resource_group, apim_service_name, pool_id, backend_pool
    )
    print(f"[OK] Backend pool '{pool_id}' created successfully")
    print("\nPool configuration:")
    print("  - foundry1 (UK South):     Priority 1, Weight 100 (primary)")
    print("  - foundry2 (East US):      Priority 2, Weight 50  (fallback)")
    print("  - foundry3 (Norway East):  Priority 2, Weight 50  (fallback)")
except Exception as e:
    print(f"[ERROR] Failed to create pool: {str(e)[:200]}")

print("\n[OK] Backend pool configuration complete!")
print("[NEXT] Run Cell 43 to apply the load balancing policy")
print("[THEN] Run Cell 44 to test load balancing\n")