#!/usr/bin/env python3
"""
Add missing Cell 71: Index documents with embeddings
"""
import json
from pathlib import Path

notebook_path = Path('master-ai-gateway-fix-MCP-clean.ipynb')

print("=" * 80)
print("📝 ADDING MISSING CELL 71: INDEX DOCUMENTS WITH EMBEDDINGS")
print("=" * 80)

# Load notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# New Cell 71 code - Index sample documents
cell_71_code = """# Lab 11: Vector Searching - Step 1.5: Index Sample Documents

import time
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI

print("\\n[*] Step 1.5: Creating and indexing sample movie documents...")

# Initialize clients
search_client = SearchClient(
    endpoint=search_endpoint,
    index_name=index_name,
    credential=AzureKeyCredential(search_admin_key)
)

# Initialize OpenAI client for embeddings
client = AzureOpenAI(
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
        # Generate embedding for overview
        start_time = time.time()
        embedding_response = client.embeddings.create(
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
    print("\\n[OK] Step 1.5 Complete - Ready for vector search testing")
else:
    print("\\n⚠️  No documents were indexed")
    print("   Check embedding generation errors above")
"""

# Find where to insert (after Cell 70, before current Cell 71)
insert_position = 70  # Insert at position 70 (will become new Cell 71)

print(f"\\nInserting new cell at position {insert_position}")
print("This will shift all subsequent cells by 1")

# Create new cell
new_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": cell_71_code
}

# Insert cell
notebook['cells'].insert(insert_position, new_cell)

# Save backup
backup_path = notebook_path.with_suffix('.ipynb.backup-add-cell71')
print(f"\\n[*] Creating backup: {backup_path}")
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

# Save updated notebook
print(f"[*] Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("\\n" + "=" * 80)
print("✅ CELL 71 ADDED SUCCESSFULLY!")
print("=" * 80)
print("\\nChanges Made:")
print("  ✅ New Cell 71: Index sample movie documents with embeddings")
print("  ✅ Creates 'documents_with_vectors' variable")
print("  ✅ Uploads 5 sample movies to search index")
print("  ✅ Old Cell 71 → New Cell 72 (Test RAG)")
print("\\n💡 What Cell 71 Does:")
print("  - Creates 5 sample movie documents")
print("  - Generates embeddings for each movie overview")
print("  - Uploads documents to Azure AI Search index")
print("  - Creates 'documents_with_vectors' variable for Cell 72")
print("\\n🎯 Next Steps:")
print("  1. Reload notebook in Jupyter")
print("  2. Run Cell 71 (will index 5 movies)")
print("  3. Run Cell 72 (will test vector search)")
print("=" * 80)
