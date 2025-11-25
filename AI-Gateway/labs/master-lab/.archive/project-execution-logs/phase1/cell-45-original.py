# Verification Helper (Optional): List all backends to confirm pool presence
import requests, json
POOL_API_VERSION = "2023-05-01-preview"
list_url = (
    f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/"
    f"Microsoft.ApiManagement/service/{apim_service_name}/backends?api-version={POOL_API_VERSION}"
)
try:
    token = credential.get_token("https://management.azure.com/.default")
    r = requests.get(list_url, headers={"Authorization": f"Bearer {token.token}"}, timeout=30)
    print("[LIST] status:", r.status_code)
    if r.status_code == 200:
        items = r.json().get('value', [])
        print(f"[LIST] {len(items)} backends returned (including pool if successful):")
        for it in items:
            pid = it.get('name') or it.get('id','').split('/')[-1]
            ptype = it.get('properties', {}).get('type', 'Standard')
            if ptype == 'Pool':
                services = (it.get('properties', {}).get('pool', {}) or {}).get('services', [])
                print(f"  [POOL] {pid}: services={len(services)}")
            else:
                print(f"  [BACKEND] {pid}: type={ptype}")
    else:
        print(r.text[:800])
except Exception as e:
    print("[ERROR] Backend list failed:", str(e)[:200])