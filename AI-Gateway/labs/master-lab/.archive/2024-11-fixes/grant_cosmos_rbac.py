#!/usr/bin/env python3
"""
Grant Cosmos DB RBAC permissions to the service principal
"""
import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment
env_file = Path('master-lab.env')
load_dotenv(env_file)

cosmos_account = os.environ.get('COSMOS_ACCOUNT_NAME')
resource_group = os.environ.get('RESOURCE_GROUP')
principal_id = "c1a04baa-9221-4490-821b-5968bbf3772b"  # From error message

print("=" * 80)
print("🔐 GRANTING COSMOS DB RBAC PERMISSIONS")
print("=" * 80)
print(f"\nCosmos Account: {cosmos_account}")
print(f"Resource Group: {resource_group}")
print(f"Service Principal: {principal_id}")

# First, get the current user's object ID (they're the one running this)
print("\n[*] Getting current user info...")
result = subprocess.run(
    ["az", "account", "show"],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    import json
    account_info = json.loads(result.stdout)
    current_user = account_info['user']['name']
    print(f"    Current user: {current_user}")

# Get the Cosmos DB Built-in Data Contributor role definition ID
print("\n[*] Getting Cosmos DB role definition ID...")
cmd = [
    "az", "cosmosdb", "sql", "role", "definition", "list",
    "--account-name", cosmos_account,
    "--resource-group", resource_group
]

result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    import json
    roles = json.loads(result.stdout)

    # Find the Data Contributor role
    data_contributor_id = None
    for role in roles:
        if 'Contributor' in role.get('roleName', ''):
            data_contributor_id = role['id']
            print(f"    Role ID: {data_contributor_id}")
            break

    if not data_contributor_id:
        print("    ⚠️  Built-in Data Contributor role not found")
        print("    Using standard role definition ID...")
        data_contributor_id = "00000000-0000-0000-0000-000000000002"

# Grant the role assignment
print(f"\n[*] Granting role assignment to principal {principal_id}...")

cmd = [
    "az", "cosmosdb", "sql", "role", "assignment", "create",
    "--account-name", cosmos_account,
    "--resource-group", resource_group,
    "--scope", "/",
    "--principal-id", principal_id,
    "--role-definition-id", data_contributor_id
]

result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("\n✅ Cosmos DB RBAC permissions granted successfully!")
    print("\n📋 Permissions:")
    print("   - Read/write databases and containers")
    print("   - Create/delete documents")
    print("   - Query data")
    print("\n⏳ Wait 60 seconds for permissions to propagate...")
    print("\n🎯 Next: Re-run Lab 10 cells (58-60) to test Cosmos DB")
elif "already exists" in result.stderr.lower():
    print("\n✅ Role assignment already exists!")
    print("   The service principal already has the required permissions")
else:
    print(f"\n❌ Failed to grant role assignment")
    print(f"   Error: {result.stderr}")
    print(f"\n💡 Manual steps:")
    print(f"   1. Go to Azure Portal > Cosmos DB > {cosmos_account}")
    print(f"   2. Click 'Data Explorer' > 'Permissions (Preview)'")
    print(f"   3. Add role assignment:")
    print(f"      - Role: Cosmos DB Built-in Data Contributor")
    print(f"      - Principal ID: {principal_id}")
    print(f"      - Scope: /")

print("\n" + "=" * 80)
