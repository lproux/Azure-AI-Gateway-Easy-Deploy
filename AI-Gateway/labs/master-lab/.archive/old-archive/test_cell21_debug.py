# Debug version - Test Cell 21
import shutil, subprocess, os, sys
from pathlib import Path

az_cli = shutil.which("az")
print(f"[DEBUG] Azure CLI: {az_cli}")

# Set subscription_id (normally from cell 26 in notebook)
subscription_id = 'd334f2cd-3efd-494e-9fd3-2470b1a13e4c'
RESOURCE_GROUP = "lab-master-lab"
APIM_SERVICE = "apim-pavavy6pu5hpa"

print(f"[DEBUG] Subscription: {subscription_id}")
print(f"[DEBUG] Resource Group: {RESOURCE_GROUP}")
print(f"[DEBUG] APIM Service: {APIM_SERVICE}")

# Query APIM for APIs
url = (f'https://management.azure.com/subscriptions/{subscription_id}'
       f'/resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.ApiManagement'
       f'/service/{APIM_SERVICE}/apis?api-version=2022-08-01')

print(f"[DEBUG] URL: {url[:100]}...")

result = subprocess.run([az_cli, "rest", "--method", "get", "--url", url], 
                       capture_output=True, text=True, timeout=60)

print(f"[DEBUG] Return code: {result.returncode}")
if result.returncode == 0:
    print(f"[DEBUG] Success! Output length: {len(result.stdout)}")
    import json
    apis_data = json.loads(result.stdout)
    apis = apis_data.get('value', [])
    print(f"[DEBUG] Found {len(apis)} APIs")
    for api in apis:
        print(f"  - {api.get('name')}: {api.get('properties', {}).get('displayName')}")
else:
    print(f"[DEBUG] Error: {result.stderr[:500]}")
