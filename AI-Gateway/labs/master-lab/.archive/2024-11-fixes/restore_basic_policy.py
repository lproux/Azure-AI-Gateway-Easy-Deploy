#!/usr/bin/env python3
"""
Restore basic policy to fix 500 errors caused by broken semantic caching policy
"""
import os
import subprocess
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment
env_file = Path('master-lab.env')
load_dotenv(env_file)

apim_service_id = os.environ.get('APIM_SERVICE_ID')
api_id = 'inference-api'

# Read the basic policy
with open('restore-basic-policy.xml', 'r') as f:
    policy_xml = f.read()

print("=" * 80)
print("🔧 RESTORING BASIC POLICY TO FIX 500 ERRORS")
print("=" * 80)
print(f"\nAPIM Service: {apim_service_id}")
print(f"API ID: {api_id}")
print("\n[*] Removing broken semantic caching policy...")

# Create the request body
body = {
    "properties": {
        "value": policy_xml,
        "format": "xml"
    }
}

# Write body to temp file
with open('/tmp/policy-body.json', 'w') as f:
    json.dump(body, f)

# Use az rest to update policy
uri = f"https://management.azure.com{apim_service_id}/apis/{api_id}/policies/policy?api-version=2023-09-01-preview"

cmd = [
    'az', 'rest',
    '--method', 'put',
    '--uri', uri,
    '--body', '@/tmp/policy-body.json',
    '--headers', 'Content-Type=application/json'
]

print(f"\n[*] Applying basic policy via az rest...")
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("\n✅ Basic policy restored successfully!")
    print("\n📋 New Policy:")
    print("   - API key authentication")
    print("   - Backend pool routing")
    print("   - Retry logic (429, 503)")
    print("   - NO semantic caching")
    print("\n⏳ Wait 10-30 seconds for policy to propagate...")
    print("\n🎯 Next: Test API with a simple request to confirm 500 errors are gone")
else:
    print(f"\n❌ Failed to restore policy")
    print(f"   Error: {result.stderr}")
    print(f"\n💡 Try manually in Azure Portal:")
    print(f"   1. Go to APIM service > APIs > inference-api")
    print(f"   2. Click 'Policies' > 'Code editor'")
    print(f"   3. Paste content from restore-basic-policy.xml")
    print(f"   4. Click 'Save'")

print("\n" + "=" * 80)
