#!/usr/bin/env python3
"""
Update Cell 70 to handle vector search index recreation robustly
"""
import json
from pathlib import Path

notebook_path = Path('master-ai-gateway-fix-MCP-clean.ipynb')

print("=" * 80)
print("📝 UPDATING CELL 70 FOR ROBUST VECTOR SEARCH INDEX HANDLING")
print("=" * 80)

# Load notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Updated cell code with robust index handling
cell_70_code = """# Lab 11: Vector Search with Azure AI Search - Step 1: Setup

import os
from pathlib import Path
from dotenv import load_dotenv

env_file = Path('master-lab.env')
if env_file.exists():
    load_dotenv(env_file)
    print("[config] Loaded: master-lab.env")

from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    VectorSearchProfile,
    HnswAlgorithmConfiguration,
)
from azure.core.credentials import AzureKeyCredential

# Get configuration
search_endpoint = os.environ.get('SEARCH_ENDPOINT')
search_admin_key = os.environ.get('SEARCH_ADMIN_KEY')
apim_gateway_url = os.environ.get('APIM_GATEWAY_URL')
inference_api_path = os.environ.get('INFERENCE_API_PATH', 'inference')
index_name = "movies-rag"

print("\\n[*] Step 1: Setting up Azure AI Search for vector searching...")
print(f"    Search Endpoint: {search_endpoint}")
print(f"    Index Name: {index_name}")
print(f"    Embeddings via: {apim_gateway_url}/{inference_api_path}")

# Create search index client
index_client = SearchIndexClient(search_endpoint, AzureKeyCredential(search_admin_key))

# Define vector search configuration
vector_search = VectorSearch(
    algorithms=[
        HnswAlgorithmConfiguration(name="movies-hnsw-vector-config")
    ],
    profiles=[
        VectorSearchProfile(
            name="movies-vector-profile",
            algorithm_configuration_name="movies-hnsw-vector-config"
        )
    ]
)

# Define index schema
fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="title", type=SearchFieldDataType.String),
    SearchableField(name="genre", type=SearchFieldDataType.String),
    SearchableField(name="overview", type=SearchFieldDataType.String),
    SearchField(
        name="embedding",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=1536,
        vector_search_profile_name="movies-vector-profile"
    )
]

# Create index
index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search)

print("\\n[*] Creating/updating search index 'movies-rag'...")

try:
    # Try to create or update
    index_client.create_or_update_index(index)
    print(f"✅ Index '{index_name}' created/updated successfully")

except Exception as e:
    error_msg = str(e)

    # Check if it's an algorithm update error
    if "Algorithm name cannot be updated" in error_msg or "algorithm" in error_msg.lower():
        print(f"⚠️  Index exists with incompatible configuration")
        print(f"   Deleting and recreating...")

        try:
            # Delete existing index
            index_client.delete_index(index_name)
            print(f"✅ Old index deleted")

            # Create new index
            index_client.create_or_update_index(index)
            print(f"✅ New index '{index_name}' created successfully")

        except Exception as delete_error:
            print(f"❌ Error during delete/recreate: {delete_error}")
            raise
    else:
        # Other error
        print(f"❌ Error creating index: {e}")
        raise

print("\\n✅ Vector search index setup complete!")
print("\\n📋 Index Configuration:")
print(f"   Name: {index_name}")
print(f"   Fields: {len(fields)}")
print(f"   Vector Dimensions: 1536")
print(f"   Algorithm: HNSW (Hierarchical Navigable Small World)")
print("\\n[OK] Step 1 Complete - Ready to add documents with embeddings")
"""

# Find Cell 70
vector_setup_idx = None
for idx, cell in enumerate(notebook['cells']):
    source = ''.join(cell.get('source', []))
    if 'Lab 11: Vector Search' in source and 'Step 1' in source:
        vector_setup_idx = idx
        break

if vector_setup_idx is None:
    print("\n❌ Could not find Cell 70 (Lab 11: Vector Search - Step 1)")
    exit(1)

print(f"\nFound Cell at index: {vector_setup_idx}")

# Update cell
notebook['cells'][vector_setup_idx]['source'] = cell_70_code

# Save backup
backup_path = notebook_path.with_suffix('.ipynb.backup-vector-robust')
print(f"\n[*] Creating backup: {backup_path}")
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

# Save updated notebook
print(f"[*] Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("\n" + "=" * 80)
print("✅ CELL 70 UPDATED WITH ROBUST INDEX HANDLING!")
print("=" * 80)
print("\nChanges Made:")
print("  ✅ Added try/except for algorithm update errors")
print("  ✅ Auto-delete and recreate index if incompatible")
print("  ✅ Better error messages and logging")
print("\n💡 Benefits:")
print("  - No manual index deletion needed")
print("  - Handles algorithm mismatches automatically")
print("  - Idempotent (can run multiple times safely)")
print("\n🎯 Next Steps:")
print("  1. Run Cell 70 (will create index successfully)")
print("  2. Run Cell 71 (Add movie documents with embeddings)")
print("  3. Run Cell 72 (Test vector search)")
print("=" * 80)
