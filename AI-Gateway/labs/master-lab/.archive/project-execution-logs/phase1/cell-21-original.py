# APIM policy apply helper (patched Azure CLI resolution with autodiscovery)
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

policy_xml = """<policies>
  <inbound>
    <base />
    <set-header name="X-Policy-Applied" exists-action="override">
      <value>content-safety</value>
    </set-header>
  </inbound>
  <backend>
    <base />
  </backend>
  <outbound>
    <base />
  </outbound>
  <on-error>
    <base />
  </on-error>
</policies>"""

def apply_policy(xml_str: str, label: str):
    """Apply APIM policy using Azure REST API."""
    import json as json_module
    import tempfile
    from pathlib import Path

    # Prefer existing subscription_id if already defined in notebook
    subscription_id_local = globals().get("subscription_id")
    if not subscription_id_local:
        result_sub = subprocess.run([az_cli, "account", "show"], capture_output=True, text=True, timeout=30)
        if result_sub.returncode != 0:
            print(f"[ERROR] Failed to get subscription ID")
            return

        try:
            sub_info = json_module.loads(result_sub.stdout)
            subscription_id_local = sub_info["id"]
        except Exception:
            print(f"[ERROR] Could not parse subscription info")
            return

    # Azure REST API endpoint for APIM policy
    url = (f'https://management.azure.com/subscriptions/{subscription_id_local}'
           f'/resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.ApiManagement'
           f'/service/{APIM_SERVICE}/apis/{API_ID}/policies/policy?api-version=2022-08-01')
    # Policy payload in Azure format
    policy_payload = {
        "properties": {
            "value": xml_str.strip(),
            "format": "xml"
        }
    }

    # Write JSON payload to temp file
    payload_file = Path(tempfile.gettempdir()) / f'apim-{label}-payload.json'
    with open(payload_file, 'w', encoding='utf-8') as f:
        json_module.dump(policy_payload, f, indent=2)

    # Build az rest command
    cmd = [az_cli, "rest", "--method", "put", "--url", url, "--body", f"@{payload_file}", "--headers", "Content-Type=application/json"]
    print(f"[*] Applying {label} policy via REST API")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        print(f"[ERROR] {label} policy timed out after 120 seconds")
        try:
            payload_file.unlink()
        except Exception:
            pass
        return
    except Exception as e:
        print(f"[ERROR] {label} policy failed: {e}")
        try:
            payload_file.unlink()
        except Exception:
            pass
        return
    else:
        # Clean up temp file
        try:
            payload_file.unlink()
        except Exception:
            pass
        if result.returncode == 0:
            print(f"[SUCCESS] {label} policy applied")
        else:
            print(f"[ERROR] {label} policy failed rc={result.returncode}\nSTDERR: {result.stderr[:400]}")