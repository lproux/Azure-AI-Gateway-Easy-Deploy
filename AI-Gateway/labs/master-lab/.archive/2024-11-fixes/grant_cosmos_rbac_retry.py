#!/usr/bin/env python3
"""
Grant Cosmos DB RBAC permissions with retry and better error handling
"""
import subprocess
import os
import time
from dotenv import load_dotenv

load_dotenv('master-lab.env')

cosmos_account = os.environ.get('COSMOS_ACCOUNT_NAME')
resource_group = 'lab-master-lab'  # Your RG

print("=" * 80)
print("🔑 GRANTING COSMOS DB RBAC PERMISSIONS")
print("=" * 80)

# Try to get principal ID
print("\n[1] Getting your Azure AD user ID...")
max_retries = 3
principal_id = None

for attempt in range(max_retries):
    try:
        result = subprocess.run(
            ['az', 'ad', 'signed-in-user', 'show', '--query', 'id', '-o', 'tsv'],
            capture_output=True,
            text=True,
            timeout=15
        )

        if result.returncode == 0:
            principal_id = result.stdout.strip()
            print(f"✅ Principal ID: {principal_id}")
            break
        else:
            print(f"⚠️  Attempt {attempt+1}/{max_retries} failed: {result.stderr[:200]}")
            if attempt < max_retries - 1:
                print("   Retrying in 3 seconds...")
                time.sleep(3)
    except Exception as e:
        print(f"⚠️  Attempt {attempt+1}/{max_retries} error: {str(e)[:200]}")
        if attempt < max_retries - 1:
            print("   Retrying in 3 seconds...")
            time.sleep(3)

if not principal_id:
    print("\n❌ Could not retrieve principal ID due to network issues")
    print("\n💡 Manual workaround:")
    print("   1. Wait for network to stabilize")
    print("   2. Run in Azure Portal Cloud Shell:")
    print(f"      az cosmosdb sql role assignment create \\")
    print(f"        --account-name {cosmos_account} \\")
    print(f"        --resource-group {resource_group} \\")
    print(f"        --role-definition-id 00000000-0000-0000-0000-000000000002 \\")
    print(f"        --principal-id $(az ad signed-in-user show --query id -o tsv) \\")
    print(f"        --scope /")
    print("\n   OR get your principal ID from:")
    print("      az ad signed-in-user show --query id -o tsv")
    print("   Then run:")
    print(f"      az cosmosdb sql role assignment create \\")
    print(f"        --account-name {cosmos_account} \\")
    print(f"        --resource-group {resource_group} \\")
    print(f"        --role-definition-id 00000000-0000-0000-0000-000000000002 \\")
    print(f"        --principal-id <YOUR-PRINCIPAL-ID> \\")
    print(f"        --scope /")
    exit(1)

# Grant permission
print(f"\n[2] Granting 'Cosmos DB Built-in Data Contributor' role...")
print(f"    Account: {cosmos_account}")
print(f"    Resource Group: {resource_group}")
print(f"    Principal ID: {principal_id}")

cmd = [
    'az', 'cosmosdb', 'sql', 'role', 'assignment', 'create',
    '--account-name', cosmos_account,
    '--resource-group', resource_group,
    '--role-definition-id', '00000000-0000-0000-0000-000000000002',
    '--principal-id', principal_id,
    '--scope', '/'
]

try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

    if result.returncode == 0:
        print("\n✅ RBAC permissions granted successfully!")
        print("\n⏳ Permissions may take 60-90 seconds to propagate")
        print("   Wait before running Cosmos DB cells")
    elif 'already exists' in result.stderr.lower() or 'conflict' in result.stderr.lower():
        print("\n✅ RBAC permissions already exist (no change needed)")
    else:
        print(f"\n❌ Error granting permissions:")
        print(result.stderr)
        print("\n💡 If this fails, use Azure Portal Cloud Shell instead")
        exit(1)

except subprocess.TimeoutExpired:
    print("\n⚠️  Command timed out (network issue)")
    print("   Try running directly in Azure Portal Cloud Shell")
    exit(1)
except Exception as e:
    print(f"\n❌ Unexpected error: {e}")
    exit(1)

print("\n" + "=" * 80)
print("✅ DONE")
print("=" * 80)
print("\nNext Steps:")
print("  1. Wait 60-90 seconds for permissions to propagate")
print("  2. Run Cell 65 (Cosmos DB setup)")
print("  3. Should work without authorization errors")
print("=" * 80)
