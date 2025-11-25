#!/usr/bin/env python3
"""
Fix Lab 10 (Message Storing) to use Azure AD authentication for Cosmos DB
"""
import json
from pathlib import Path

notebook_path = Path('master-ai-gateway-fix-MCP-clean.ipynb')

with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# New cell source with Azure AD authentication
fixed_cell_source = """# Lab 10: Message Storing - Step 1: Setup Cosmos DB Database and Container (FIXED)

# Load environment from master-lab.env
import os
from pathlib import Path
from dotenv import load_dotenv

env_file = Path('master-lab.env')
if env_file.exists():
    load_dotenv(env_file)
    print(f"[config] Loaded: {env_file.absolute()}")

# Get Cosmos DB configuration
cosmos_endpoint = os.environ.get('COSMOS_ENDPOINT')
cosmos_account = os.environ.get('COSMOS_ACCOUNT_NAME')

if not cosmos_endpoint:
    print("[ERROR] Missing Cosmos DB environment variables")
    print(f"COSMOS_ENDPOINT: {cosmos_endpoint}")
else:
    print(f"\\n[*] Step 1: Setting up Cosmos DB for message storage...")
    print(f"    Cosmos Account: {cosmos_account}")
    print(f"    Endpoint: {cosmos_endpoint}")

    try:
        from azure.cosmos import CosmosClient, PartitionKey, exceptions
        from azure.identity import DefaultAzureCredential

        # Use Azure AD authentication (required when local auth is disabled)
        print(f"\\n[*] Authenticating with Azure AD...")
        credential = DefaultAzureCredential()

        # Create Cosmos client with Azure AD auth
        client = CosmosClient(cosmos_endpoint, credential)
        print(f"✅ Authenticated successfully with Azure AD")

        # Database configuration
        database_name = 'llmdb'
        container_name = 'messages'

        # Create database if it doesn't exist
        try:
            database = client.create_database(id=database_name)
            print(f"\\n✅ Database '{database_name}' created")
        except exceptions.CosmosResourceExistsError:
            database = client.get_database_client(database_name)
            print(f"\\n✅ Database '{database_name}' already exists")

        # Create container if it doesn't exist
        try:
            container = database.create_container(
                id=container_name,
                partition_key=PartitionKey(path="/conversationId"),
                offer_throughput=400
            )
            print(f"✅ Container '{container_name}' created")
            print(f"   Partition Key: /conversationId")
            print(f"   Throughput: 400 RU/s")
        except exceptions.CosmosResourceExistsError:
            container = database.get_container_client(container_name)
            print(f"✅ Container '{container_name}' already exists")

        print(f"\\n[OK] Step 1 Complete - Cosmos DB ready for message storage")

        # Store for later use
        cosmos_database_name = database_name
        cosmos_container_name = container_name

    except ImportError:
        print("\\n⚠️  Required packages not installed")
        print("   Run: pip install azure-cosmos azure-identity")
    except Exception as e:
        print(f"\\n❌ Error setting up Cosmos DB: {e}")
        print("\\n💡 Note: Make sure you're logged in with 'az login'")
        print("   Cosmos DB requires Azure AD authentication (local auth is disabled)")
"""

# Find and update Cell 57 (Lab 10 - Step 1)
cells = notebook['cells']
updated = False

for i, cell in enumerate(cells):
    if cell.get('cell_type') == 'code':
        source = ''.join(cell.get('source', []))
        if 'Lab 10: Message Storing - Step 1' in source and 'Setup Cosmos DB' in source:
            print(f"Found Cell {i+1} - Updating with Azure AD authentication")
            cells[i]['source'] = fixed_cell_source.split('\n')
            cells[i]['outputs'] = []
            updated = True
            break

if updated:
    # Save notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)

    print("\n✅ Cell 57 updated with Azure AD authentication")
    print("\nChanges made:")
    print("  1. Uses DefaultAzureCredential instead of cosmos_key")
    print("  2. Removed dependency on COSMOS_KEY environment variable")
    print("  3. Added helpful error message about 'az login'")
    print("\nNext steps:")
    print("  1. Make sure you're logged in: az login")
    print("  2. Restart your kernel")
    print("  3. Run Cell 57 again")
else:
    print("❌ Could not find Cell 57 (Lab 10 - Step 1)")
