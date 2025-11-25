#!/usr/bin/env python3
"""
Update Cell 71 to call embeddings directly (not through APIM)
"""
import json
from pathlib import Path

notebook_path = Path('master-ai-gateway-fix-MCP-clean.ipynb')

print("=" * 80)
print("📝 UPDATING CELL 71 TO USE DIRECT EMBEDDINGS ENDPOINT")
print("=" * 80)

# Load notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Updated Cell 71 code - Direct embeddings
cell_71_code = """# Lab 11: Vector Searching - Step 1.5: Index Sample Documents

import time
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI

print("\\n[*] Step 1.5: Creating and indexing sample movie documents...")

# Initialize search client
search_client = SearchClient(
    endpoint=search_endpoint,
    index_name=index_name,
    credential=AzureKeyCredential(search_admin_key)
)

# Initialize OpenAI client for embeddings - DIRECT endpoint (bypass APIM)
# Embeddings don't need semantic caching (deterministic)
embeddings_endpoint = os.environ.get('MODEL_TEXT_EMBEDDING_3_SMALL_ENDPOINT_R1')
embeddings_key = os.environ.get('MODEL_TEXT_EMBEDDING_3_SMALL_KEY_R1')

embeddings_client = AzureOpenAI(
    azure_endpoint=embeddings_endpoint,
    api_key=embeddings_key,
    api_version="2024-08-01-preview"
)

print(f"   Using direct embeddings endpoint: {embeddings_endpoint}")

# Initialize chat client for RAG (through APIM with caching)
chat_client = AzureOpenAI(
    azure_endpoint=f"{apim_gateway_url}/{inference_api_path}",
    api_key=os.environ.get('APIM_API_KEY'),
    api_version="2024-08-01-preview"
)

# Sample movie documents
sample_movies = [
    {
        "id": "1",
        "title": "The Avengers",
        "genre": "Action, Superhero",
        "overview": "Earth's mightiest heroes must come together to stop Loki and his alien army from enslaving humanity."
    },
    {
        "id": "2",
        "title": "The Dark Knight",
        "genre": "Action, Crime, Drama",
        "overview": "Batman faces the Joker, a criminal mastermind who wants to plunge Gotham City into anarchy."
    },
    {
        "id": "3",
        "title": "Inception",
        "genre": "Sci-Fi, Thriller",
        "overview": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea."
    },
    {
        "id": "4",
        "title": "Interstellar",
        "genre": "Sci-Fi, Drama",
        "overview": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."
    },
    {
        "id": "5",
        "title": "The Matrix",
        "genre": "Sci-Fi, Action",
        "overview": "A computer hacker learns about the true nature of his reality and his role in the war against its controllers."
    }
]

print(f"\\n{'='*80}")
print("📚 INDEXING SAMPLE DOCUMENTS")
print(f"{'='*80}")
print(f"\\nTotal movies to index: {len(sample_movies)}\\n")

documents_with_vectors = []
total_start = time.time()

for i, movie in enumerate(sample_movies, 1):
    print(f"▶️  Processing movie {i}/{len(sample_movies)}: {movie['title']}")

    try:
        # Generate embedding using DIRECT endpoint (bypass APIM)
        start_time = time.time()
        embedding_response = embeddings_client.embeddings.create(
            model="text-embedding-3-small",
            input=movie['overview']
        )
        embedding_vector = embedding_response.data[0].embedding
        embedding_time = time.time() - start_time

        print(f"   ✅ Embedding generated ({embedding_time:.2f}s, {len(embedding_vector)} dimensions)")

        # Create document with embedding
        doc = {
            "id": movie["id"],
            "title": movie["title"],
            "genre": movie["genre"],
            "overview": movie["overview"],
            "embedding": embedding_vector
        }

        documents_with_vectors.append(doc)

    except Exception as e:
        print(f"   ❌ Error generating embedding: {e}")

# Upload all documents to search index
if documents_with_vectors:
    print(f"\\n▶️  Uploading {len(documents_with_vectors)} documents to search index...")
    start_time = time.time()

    try:
        result = search_client.upload_documents(documents=documents_with_vectors)
        upload_time = time.time() - start_time

        # Count successes
        succeeded = sum(1 for r in result if r.succeeded)
        failed = len(result) - succeeded

        if succeeded == len(documents_with_vectors):
            print(f"   ✅ All {succeeded} documents uploaded successfully ({upload_time:.2f}s)")
        else:
            print(f"   ⚠️  {succeeded} documents uploaded, {failed} failed ({upload_time:.2f}s)")

    except Exception as e:
        print(f"   ❌ Error uploading documents: {e}")

total_time = time.time() - total_start

print(f"\\n{'='*80}")
print("📊 INDEXING SUMMARY")
print(f"{'='*80}")
print(f"Documents processed:  {len(sample_movies)}")
print(f"Documents indexed:    {len(documents_with_vectors)}")
print(f"Total time:           {total_time:.2f}s")

if documents_with_vectors:
    print("\\n✅ Index populated with sample movie data!")
    print(f"   Variable 'documents_with_vectors' created with {len(documents_with_vectors)} items")
    print(f"   Variable 'chat_client' created for RAG queries (with APIM caching)")
    print("\\n💡 Note: Embeddings use direct endpoint (no caching needed)")
    print("         Chat completions use APIM endpoint (with semantic caching)")
    print("\\n[OK] Step 1.5 Complete - Ready for vector search testing")
else:
    print("\\n⚠️  No documents were indexed")
    print("   Check embedding generation errors above")
"""

# Find Cell 71
cell_71_idx = 70  # Cell 71 is at index 70

print(f"\nUpdating Cell at index: {cell_71_idx}")

# Update cell
notebook['cells'][cell_71_idx]['source'] = cell_71_code

# Save backup
backup_path = notebook_path.with_suffix('.ipynb.backup-direct-embeddings')
print(f"\n[*] Creating backup: {backup_path}")
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

# Save updated notebook
print(f"[*] Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("\n" + "=" * 80)
print("✅ CELL 71 UPDATED TO USE DIRECT EMBEDDINGS!")
print("=" * 80)
print("\nChanges Made:")
print("  ✅ Embeddings now use direct Azure OpenAI endpoint")
print("  ✅ Bypasses APIM semantic caching policy")
print("  ✅ Chat client still uses APIM (for semantic caching)")
print("  ✅ No policy changes needed")
print("\n💡 Why This Works:")
print("  - Embeddings are deterministic (same input = same output)")
print("  - Semantic caching not needed for embeddings")
print("  - Direct calls avoid 500 errors from policy mismatch")
print("  - Chat completions still benefit from semantic caching")
print("\n🎯 Next Steps:")
print("  1. Reload notebook")
print("  2. Run Cell 71 (will index successfully)")
print("  3. Run Cell 72 (will test vector search + RAG)")
print("=" * 80)
