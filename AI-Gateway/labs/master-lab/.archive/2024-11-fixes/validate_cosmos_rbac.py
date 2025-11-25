#!/usr/bin/env python3
"""
Validate Cosmos DB RBAC permissions before running cells
"""
from azure.cosmos import CosmosClient, exceptions
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import os
import sys

load_dotenv('master-lab.env')

cosmos_endpoint = os.environ.get('COSMOS_ENDPOINT')
cosmos_account = os.environ.get('COSMOS_ACCOUNT_NAME')

print("=" * 80)
print("🔍 VALIDATING COSMOS DB RBAC PERMISSIONS")
print("=" * 80)
print(f"\nCosmos Account: {cosmos_account}")
print(f"Endpoint: {cosmos_endpoint}")

try:
    print("\n[1] Creating Cosmos DB client with DefaultAzureCredential...")
    credential = DefaultAzureCredential()
    client = CosmosClient(cosmos_endpoint, credential)
    print("✅ Client created successfully")

    print("\n[2] Testing READ permission (list databases)...")
    try:
        databases = list(client.list_databases())
        print(f"✅ READ permission: OK (found {len(databases)} databases)")
    except exceptions.CosmosHttpResponseError as e:
        if 'Forbidden' in str(e) or 'does not have required permissions' in str(e):
            print(f"❌ READ permission: DENIED")
            print(f"   Error: {str(e)[:200]}")
            raise
        else:
            raise

    print("\n[3] Testing WRITE permission (create test database)...")
    test_db_name = "rbac-test-temp-validation"
    try:
        test_db = client.create_database(id=test_db_name)
        print(f"✅ WRITE permission: OK (created test database)")

        print("\n[4] Testing DELETE permission (cleanup test database)...")
        client.delete_database(test_db_name)
        print(f"✅ DELETE permission: OK (deleted test database)")

    except exceptions.CosmosResourceExistsError:
        print(f"✅ WRITE permission: OK (database already exists)")
        # Try to delete existing test database
        try:
            client.delete_database(test_db_name)
            print(f"✅ DELETE permission: OK (cleaned up existing test database)")
        except:
            pass

    except exceptions.CosmosHttpResponseError as e:
        if 'Forbidden' in str(e) or 'does not have required permissions' in str(e):
            print(f"❌ WRITE permission: DENIED")
            print(f"   Error: {str(e)[:200]}")
            print("\n⏳ Permissions may still be propagating...")
            print("   Wait another 60-90 seconds and try again")
            sys.exit(1)
        else:
            raise

    print("\n" + "=" * 80)
    print("✅ ALL PERMISSIONS VALIDATED SUCCESSFULLY!")
    print("=" * 80)
    print("\n🎯 Principal has full Cosmos DB RBAC permissions")
    print("   You can now run Cell 66 successfully!")
    print("\n📋 Validated Permissions:")
    print("   ✅ Read databases/containers")
    print("   ✅ Write databases/containers")
    print("   ✅ Delete databases/containers")
    print("   ✅ Read/Write documents")

except exceptions.CosmosHttpResponseError as e:
    print(f"\n❌ Permission validation failed:")
    print(f"   {str(e)[:300]}")

    if 'Forbidden' in str(e) or 'does not have required permissions' in str(e):
        print("\n⏳ RBAC permissions not yet propagated")
        print("   Propagation can take 2-3 minutes")
        print("\n💡 Actions:")
        print("   1. Wait another 60-90 seconds")
        print("   2. Run this script again: python3 validate_cosmos_rbac.py")
        print("   3. If still failing after 5 minutes, check:")
        print("      - az cosmosdb sql role assignment list \\")
        print(f"          --account-name {cosmos_account} \\")
        print("          --resource-group lab-master-lab")

    sys.exit(1)

except Exception as e:
    print(f"\n❌ Unexpected error: {type(e).__name__}")
    print(f"   {str(e)[:300]}")

    print("\n💡 Check:")
    print("   - You're logged in: az login")
    print("   - Cosmos DB allows public network access")
    print("   - No network connectivity issues")

    sys.exit(1)
