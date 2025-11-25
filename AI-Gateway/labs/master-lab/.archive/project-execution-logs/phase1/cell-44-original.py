# ============================================================================
# FIX: Create Backend Pool for Load Balancing (Preview API)
# ============================================================================
# Ensure backend pool uses API version >= 2023-05-01-preview and omits
# unsupported properties (url/protocol) when type = 'Pool'.
# If you still get validation errors complaining about API version,
# double‑check:
#   1. Region of APIM service supports backend pools (feature rollout).
#   2. API version string EXACTLY matches '2023-05-01-preview'.
#   3. No stale variable pool_url from a prior run (restart kernel if needed).
#   4. You removed old cell output using lower API version.
#
# Added: Verification of existing pool, conditional PUT only if absent, and
# GET after creation. Debug prints trimmed for clarity.

print("\n" + "="*80)
print("FIX: Creating Backend Pool for Load Balancing (Preview API)")
print("="*80 + "\n")

from azure.mgmt.apimanagement import ApiManagementClient
from azure.mgmt.apimanagement.models import BackendContract
import requests, json

apim_client = ApiManagementClient(credential, subscription_id)

resource_suffix = 'pavavy6pu5hpa'
backends_config = [
    {'id': 'foundry1', 'url': f'https://foundry1-{resource_suffix}.openai.azure.com/openai', 'location': 'uksouth', 'priority': 1, 'weight': 100},
    {'id': 'foundry2', 'url': f'https://foundry2-{resource_suffix}.openai.azure.com/openai', 'location': 'eastus', 'priority': 2, 'weight': 50},
    {'id': 'foundry3', 'url': f'https://foundry3-{resource_suffix}.openai.azure.com/openai', 'location': 'norwayeast', 'priority': 2, 'weight': 50},
]

print("[*] Step 1: Ensuring individual backends...")
backend_arm_ids = []
for cfg in backends_config:
    bid = cfg['id']
    try:
        apim_client.backend.get(resource_group, apim_service_name, bid)
        print(f"  [OK] Backend '{bid}' exists")
    except Exception:
        print(f"  [*] Creating backend '{bid}'...")
        backend = BackendContract(
            url=cfg['url'],
            protocol="http",
            description=f"Azure OpenAI - {cfg['location']}",
            tls={"validateCertificateChain": True, "validateCertificateName": True}
        )
        try:
            apim_client.backend.create_or_update(resource_group, apim_service_name, bid, backend)
            print(f"  [OK] Backend '{bid}' created")
        except Exception as e:
            print(f"  [ERROR] Backend create failed '{bid}': {str(e)[:160]}")
            continue
    backend_arm_ids.append({
        'id': f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.ApiManagement/service/{apim_service_name}/backends/{bid}",
        'priority': cfg['priority'],
        'weight': cfg['weight']
    })

print("\n[*] Step 2: Ensuring backend POOL (preview)...")
POOL_API_VERSION = "2023-05-01-preview"
pool_id = "inference-backend-pool"
services = [{"id": b['id'], "priority": b['priority'], "weight": b['weight']} for b in backend_arm_ids]

# Build URL with preview version (must match exactly)
pool_url = (
    f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/"
    f"Microsoft.ApiManagement/service/{apim_service_name}/backends/{pool_id}?api-version={POOL_API_VERSION}"
)

# Check if pool already exists
try:
    token = credential.get_token("https://management.azure.com/.default")
    existing_resp = requests.get(pool_url, headers={"Authorization": f"Bearer {token.token}"}, timeout=30)
    if existing_resp.status_code == 200:
        print(f"  [OK] Pool '{pool_id}' already exists (GET 200)")
    else:
        print(f"  [*] Pool '{pool_id}' not found (status {existing_resp.status_code}); creating...")
        pool_body = {
            "properties": {
                "description": "Load-balanced pool with priority routing",
                "type": "Pool",
                "pool": {"services": services}
            }
        }
        put_resp = requests.put(
            pool_url,
            headers={"Authorization": f"Bearer {token.token}", "Content-Type": "application/json"},
            json=pool_body,
            timeout=60
        )
        if put_resp.status_code in (200, 201):
            print(f"  [OK] Pool '{pool_id}' created/updated (status {put_resp.status_code})")
        else:
            print(f"  [ERROR] Pool create/update failed: {put_resp.status_code}")
            try:
                print(json.dumps(put_resp.json(), indent=2)[:1500])
            except Exception:
                print(put_resp.text[:1500])
            if "Backend Type and Pool properties" in put_resp.text:
                print("  [HINT] Preview feature may not be enabled in this region or API version mismatch.")
except Exception as e:
    print(f"[ERROR] Exception during pool ensure: {str(e)[:200]}")

# Final verification GET
try:
    verify = requests.get(pool_url, headers={"Authorization": f"Bearer {token.token}"}, timeout=30)
    print("\n[*] Verification GET status:", verify.status_code)
    if verify.status_code == 200:
        data = verify.json()
        services_out = (data.get('properties', {}).get('pool', {}) or {}).get('services', [])
        print(f"  [OK] Pool has {len(services_out)} services:")
        for s in services_out:
            name = s.get('id','').split('/')[-1]
            print(f"    - {name}: P{s.get('priority')} W{s.get('weight')}")
    else:
        print("  [WARN] Could not verify pool; status", verify.status_code)
except Exception as e:
    print(f"[ERROR] Verification failed: {str(e)[:160]}")

print("\n[OK] Backend pool ensure process complete.")
print("[NEXT] Run Cell 43 to (re)apply the load balancing policy")
print("[THEN] Run Cell 44 to test load balancing\n")