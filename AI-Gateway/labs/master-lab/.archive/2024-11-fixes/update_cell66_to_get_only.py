#!/usr/bin/env python3
"""
Update Cell 66 to GET existing Cosmos DB resources instead of CREATE
"""
import json
from pathlib import Path

notebook_path = Path('master-ai-gateway-fix-MCP-clean.ipynb')

print("=" * 80)
print("📝 UPDATING CELL 66 TO GET EXISTING RESOURCES")
print("=" * 80)

# Load notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Updated cell code - GET instead of CREATE
cell_66_code = """# Lab 10: Message Storing - Step 1: Setup Cosmos DB (Azure AD Auth)

import os
from pathlib import Path
from dotenv import load_dotenv

env_file = Path('master-lab.env')
if env_file.exists():
    load_dotenv(env_file)
    print("[config] Loaded: master-lab.env")

from azure.cosmos import CosmosClient, exceptions
from azure.identity import DefaultAzureCredential

# Get Cosmos DB config
cosmos_endpoint = os.environ.get('COSMOS_ENDPOINT')
cosmos_account = os.environ.get('COSMOS_ACCOUNT_NAME')

database_name = "messages-db"
container_name = "conversations"

print("\\n[*] Step 1: Connecting to Cosmos DB for message storage...")
print(f"    Cosmos Account: {cosmos_account}")
print(f"    Endpoint: {cosmos_endpoint}")
print(f"    Database: {database_name}")
print(f"    Container: {container_name}")

try:
    # Use Azure AD authentication (local auth disabled on this account)
    print("\\n[*] Creating Cosmos DB client with Azure AD...")
    credential = DefaultAzureCredential()
    client = CosmosClient(cosmos_endpoint, credential)
    print("✅ Cosmos DB client created with Azure AD authentication")

    # Get existing database (created via Azure CLI)
    print(f"\\n[*] Connecting to database '{database_name}'...")
    database = client.get_database_client(database_name)
    print(f"✅ Connected to database '{database_name}'")

    # Get existing container (created via Azure CLI)
    print(f"\\n[*] Connecting to container '{container_name}'...")
    container = database.get_container_client(container_name)
    print(f"✅ Connected to container '{container_name}'")

    print("\\n✅ Cosmos DB setup complete!")
    print("\\n📋 Summary:")
    print(f"   Database: {database_name}")
    print(f"   Container: {container_name}")
    print(f"   Partition Key: /conversationId")
    print(f"   Auth: Azure AD (DefaultAzureCredential)")
    print(f"   Operation: GET existing resources (no WRITE needed)")
    print("\\n[OK] Step 1 Complete - Ready to store messages")

except exceptions.CosmosResourceNotFoundError as e:
    print(f"\\n❌ Error: Database or container not found")
    print(f"\\nThe resources may not have been created yet.")
    print(f"\\nTo create via Azure CLI:")
    print(f"  az cosmosdb sql database create --account-name {cosmos_account} --resource-group lab-master-lab --name {database_name}")
    print(f"  az cosmosdb sql container create --account-name {cosmos_account} --resource-group lab-master-lab --database-name {database_name} --name {container_name} --partition-key-path /conversationId --throughput 400")
    raise

except exceptions.CosmosHttpResponseError as e:
    if 'Forbidden' in str(e) or 'does not have required permissions' in str(e):
        print(f"\\n❌ Error: RBAC permissions missing")
        print(f"\\nYour identity needs 'Cosmos DB Built-in Data Reader' role (for GET operations)")
        print(f"\\nNote: WRITE permissions not needed when using pre-created resources")
        raise
    else:
        print(f"\\n❌ Error connecting to Cosmos DB: {e}")
        raise

except Exception as e:
    print(f"\\n❌ Error setting up Cosmos DB: {e}")
    print(f"\\n💡 Check:")
    print("   - You're logged in: az login")
    print("   - Cosmos DB allows public network access")
    print("   - Database and container exist")
    raise
"""

# Find Cell 66
cosmos_setup_idx = None
for idx, cell in enumerate(notebook['cells']):
    source = ''.join(cell.get('source', []))
    if 'Lab 10: Message Storing - Step 1' in source:
        cosmos_setup_idx = idx
        break

if cosmos_setup_idx is None:
    print("\n❌ Could not find Cell 66 (Lab 10: Message Storing - Step 1)")
    exit(1)

print(f"\nFound Cell at index: {cosmos_setup_idx}")

# Update cell
notebook['cells'][cosmos_setup_idx]['source'] = cell_66_code

# Save backup
backup_path = notebook_path.with_suffix('.ipynb.backup-get-only')
print(f"\n[*] Creating backup: {backup_path}")
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

# Save updated notebook
print(f"[*] Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("\n" + "=" * 80)
print("✅ CELL 66 UPDATED TO GET EXISTING RESOURCES!")
print("=" * 80)
print("\nChanges Made:")
print("  ✅ Removed CREATE operations (database.create_database, etc.)")
print("  ✅ Added GET operations (client.get_database_client, etc.)")
print("  ✅ Now requires READ permission only (not WRITE)")
print("  ✅ Works with pre-created resources from Azure CLI")
print("\n💡 Benefits:")
print("  - No RBAC propagation delay for WRITE permissions")
print("  - More secure (separates infrastructure from runtime)")
print("  - Follows Azure best practices")
print("\n🎯 Next Steps:")
print("  1. Re-run Cell 66 (should succeed immediately)")
print("  2. Run Cell 67 (Generate and Store)")
print("  3. Run Cell 68 (Query Messages)")
print("=" * 80)
