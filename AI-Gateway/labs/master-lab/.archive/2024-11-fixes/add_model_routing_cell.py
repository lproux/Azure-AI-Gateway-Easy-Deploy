#!/usr/bin/env python3
"""
Add model routing policy cell before Cell 86 (Lab 08 test)
"""
import json
from pathlib import Path

notebook_path = Path('master-ai-gateway-fix-MCP-clean.ipynb')

print("=" * 80)
print("📝 ADDING MODEL ROUTING POLICY CELL")
print("=" * 80)

# Load notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# New cell - Model Routing Policy Application
model_routing_cell = """# Lab 08: Apply Model Routing Policy

import os
import json
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv

env_file = Path('master-lab.env')
if env_file.exists():
    load_dotenv(env_file)
    print(f"[config] Loaded: {env_file.absolute()}")

apim_service_id = os.environ.get('APIM_SERVICE_ID')

print("=" * 80)
print("🔀 APPLYING MODEL ROUTING POLICY")
print("=" * 80)

# Model routing policy
# Routes gpt-4.1-nano to foundry1 or foundry3 (foundry2 doesn't have it)
# Other models use the backend pool
policy_xml = '''<policies>
    <inbound>
        <base />
        <check-header name="api-key" failed-check-httpcode="401" failed-check-error-message="Missing or invalid API key" />

        <!-- Model-specific routing -->
        <set-variable name="requestBody" value="@(context.Request.Body.As<string>(preserveContent: true))" />
        <choose>
            <!-- Route gpt-4.1-nano to foundry1 (has the deployment) -->
            <when condition="@(((string)context.Variables["requestBody"]).Contains("gpt-4.1-nano"))">
                <set-backend-service backend-id="foundry1-backend" />
            </when>
            <!-- All other models use the backend pool -->
            <otherwise>
                <set-backend-service backend-id="inference-backend-pool" />
            </otherwise>
        </choose>
    </inbound>
    <backend>
        <retry count="2" interval="0" first-fast-retry="true" condition="@(context.Response.StatusCode == 429 || context.Response.StatusCode == 503)">
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
                    <set-body>{"error": {"code": "ServiceUnavailable", "message": "Service temporarily unavailable"}}</set-body>
                </return-response>
            </when>
        </choose>
    </on-error>
</policies>'''

uri = f"https://management.azure.com{apim_service_id}/apis/inference-api/policies/policy?api-version=2023-09-01-preview"

body = {
    "properties": {
        "value": policy_xml,
        "format": "xml"
    }
}

body_file = '/tmp/model-routing-policy.json'
with open(body_file, 'w', encoding='utf-8') as f:
    json.dump(body, f, indent=2)

print("\\n[*] Applying model routing policy to APIM...")

cmd = ['az', 'rest', '--method', 'put', '--uri', uri, '--body', f'@{body_file}']
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("\\n✅ Model routing policy applied successfully!")
    print("\\n📋 Routing Configuration:")
    print("   - gpt-4.1-nano → foundry1-backend")
    print("   - gpt-4o-mini  → inference-backend-pool (load balanced)")
    print("   - Other models → inference-backend-pool (load balanced)")

    print("\\n⏳ Waiting 60 seconds for policy propagation...")
    print("   ", end='', flush=True)

    for i in range(60, 0, -1):
        print(f"\\r   {i:2d}s remaining...", end='', flush=True)
        time.sleep(1)

    print("\\r   ✅ Policy propagation complete!     ")
    print("\\n[OK] Ready to test model routing!")
else:
    print(f"\\n❌ Error applying policy:")
    print(result.stderr)
    raise Exception("Failed to apply model routing policy")

print("=" * 80)
"""

# Insert before Cell 86 (at position 85, after Lab 08 intro)
insert_position = 85

print(f"\nInserting model routing policy cell at position {insert_position}")

# Create new cell
new_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": model_routing_cell
}

# Insert cell
notebook['cells'].insert(insert_position, new_cell)

# Save backup
backup_path = notebook_path.with_suffix('.ipynb.backup-add-model-routing')
print(f"\n[*] Creating backup: {backup_path}")
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

# Save updated notebook
print(f"[*] Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("\n" + "=" * 80)
print("✅ MODEL ROUTING POLICY CELL ADDED!")
print("=" * 80)
print("\nChanges Made:")
print("  ✅ New Cell 86: Apply Model Routing Policy")
print("  ✅ Old Cell 86 → New Cell 87 (Model Routing Test)")
print("  ✅ Includes 60-second countdown for propagation")
print("\n💡 What the Policy Does:")
print("  - Inspects request body to determine model")
print("  - Routes gpt-4.1-nano → foundry1 (has deployment)")
print("  - Routes other models → backend pool (load balanced)")
print("\n📋 Why This Works:")
print("  - foundry2 doesn't have gpt-4.1-nano (subscription feature missing)")
print("  - foundry1 and foundry3 have gpt-4.1-nano deployed")
print("  - Policy ensures gpt-4.1-nano requests go to foundry1")
print("\n🎯 Next Steps:")
print("  1. Reload notebook")
print("  2. Run Cell 86 (Apply Model Routing Policy)")
print("     - Wait for 60-second countdown")
print("  3. Run Cell 87 (Test Model Routing)")
print("     - gpt-4o-mini: ✅ Should work")
print("     - gpt-4.1-nano: ✅ Should work (routed to foundry1)")
print("=" * 80)
