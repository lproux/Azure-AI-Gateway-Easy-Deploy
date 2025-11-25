# Test Cell 21 - APIM policy helper with autodiscovery
import shutil, subprocess, os, sys, textwrap, tempfile
from pathlib import Path

AZ_CANDIDATES = [
    shutil.which("az"),
    str(Path(sys.prefix) / "bin" / "az"),
]

AZ_CANDIDATES += [c for c in [os.getenv("AZURE_CLI_PATH"), os.getenv("AZ_PATH")] if c]
az_cli = next((c for c in AZ_CANDIDATES if c and Path(c).exists()), None)

if not az_cli:
    raise SystemExit("[FATAL] Azure CLI 'az' not found. Install it before continuing.")

print(f"[INFO] Azure CLI resolved: {az_cli}")

# Ensure ENV is defined
ENV = os.environ
RESOURCE_GROUP = ENV.get("RESOURCE_GROUP") or os.getenv("RESOURCE_GROUP") or "lab-master-lab"
APIM_SERVICE = ENV.get("APIM_SERVICE_NAME") or os.getenv("APIM_SERVICE_NAME") or "apim-pavavy6pu5hpa"

# Autodiscover API_ID from APIM service
def autodiscover_api_id():
    """Auto-discover the inference API ID from APIM service."""
    try:
        # Get subscription ID
        subscription_id_local = globals().get("subscription_id")
        if not subscription_id_local:
            result_sub = subprocess.run([az_cli, "account", "show"], capture_output=True, text=True, timeout=30)
            if result_sub.returncode != 0:
                return None
            import json as json_module
            sub_info = json_module.loads(result_sub.stdout)
            subscription_id_local = sub_info.get("id")
        
        if not subscription_id_local:
            return None
        
        # Query APIM for APIs
        url = (f'https://management.azure.com/subscriptions/{subscription_id_local}'
               f'/resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.ApiManagement'
               f'/service/{APIM_SERVICE}/apis?api-version=2022-08-01')
        
        result = subprocess.run([az_cli, "rest", "--method", "get", "--url", url], 
                               capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            return None
        
        import json as json_module
        apis_data = json_module.loads(result.stdout)
        apis = apis_data.get('value', [])
        
        # Find inference API
        for api in apis:
            api_id = api.get('name', '')
            api_props = api.get('properties', {})
            api_name = api_props.get('displayName', '').lower()
            api_path = api_props.get('path', '').lower()
            
            if 'inference' in api_id.lower() or 'inference' in api_name or 'inference' in api_path:
                return api_id
        
        # Fallback to inference-api if exists
        for api in apis:
            if api.get('name') == 'inference-api':
                return 'inference-api'
        
        return None
    except Exception:
        return None

# Try to autodiscover, fallback to env or default
API_ID = ENV.get("APIM_API_ID") or os.getenv("APIM_API_ID")

if not API_ID:
    print("[*] Auto-discovering API_ID from APIM service...")
    discovered_api_id = autodiscover_api_id()
    if discovered_api_id:
        API_ID = discovered_api_id
        os.environ['APIM_API_ID'] = API_ID
        print(f"[OK] API_ID auto-discovered: {API_ID}")
    else:
        # Fallback to default
        API_ID = "inference-api"
        os.environ['APIM_API_ID'] = API_ID
        print(f"[!] Could not auto-discover API_ID, using default: {API_ID}")
else:
    print(f"[OK] API_ID from environment: {API_ID}")

print()
print(f"FINAL API_ID: {API_ID}")
print(f"Environment variable APIM_API_ID: {os.getenv('APIM_API_ID')}")
