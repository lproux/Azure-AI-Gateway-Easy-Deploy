#!/usr/bin/env python3
"""
Fix Vector Search cells (62-63) to use APIM for embeddings
Based on working vector-searching.ipynb pattern
"""
import json
from pathlib import Path

print("=" * 80)
print("🔧 FIXING VECTOR SEARCH CELLS (62-63)")
print("=" * 80)
print("\nUsing: APIM for embeddings (via corrected semantic caching policy)")

# Load master notebook
notebook_path = Path('master-ai-gateway-fix-MCP-clean.ipynb')
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

print(f"\nLoaded notebook with {len(notebook['cells'])} cells")

# Cell 62: Setup Azure AI Search and Generate Embeddings
cell_62_code = """# Lab 11: Vector Searching - Step 1: Setup and Generate Embeddings
# FIXED: Using APIM for embeddings (with corrected semantic caching policy)

import os
from pathlib import Path
from dotenv import load_dotenv

env_file = Path('master-lab.env')
if env_file.exists():
    load_dotenv(env_file)
    print("[config] Loaded: master-lab.env")

from azure.search.documents import SearchClient
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
from openai import AzureOpenAI
import time

# Get configuration
search_endpoint = os.environ.get('SEARCH_ENDPOINT')
search_admin_key = os.environ.get('SEARCH_ADMIN_KEY')
apim_gateway_url = os.environ.get('APIM_GATEWAY_URL')
apim_api_key = os.environ.get('APIM_API_KEY')
inference_api_path = os.environ.get('INFERENCE_API_PATH', 'inference')

index_name = "movies-rag"

print("\\n[*] Step 1: Setting up Azure AI Search for vector searching...")
print(f"    Search Endpoint: {search_endpoint}")
print(f"    Index Name: {index_name}")
print(f"    Embeddings via: {apim_gateway_url}/{inference_api_path}")

# Create search index client
index_client = SearchIndexClient(
    endpoint=search_endpoint,
    credential=AzureKeyCredential(search_admin_key)
)

# Define index schema with vector field
fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="title", type=SearchFieldDataType.String),
    SearchableField(name="genre", type=SearchFieldDataType.String),
    SearchableField(name="overview", type=SearchFieldDataType.String),
    SearchField(
        name="vector",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=1536,  # text-embedding-3-small
        vector_search_profile_name="movies-vector-profile"
    ),
]

# Configure vector search
vector_search = VectorSearch(
    profiles=[VectorSearchProfile(
        name="movies-vector-profile",
        algorithm_configuration_name="movies-hnsw"
    )],
    algorithms=[HnswAlgorithmConfiguration(name="movies-hnsw")]
)

# Create or update index
index = SearchIndex(
    name=index_name,
    fields=fields,
    vector_search=vector_search
)

try:
    print(f"\\n[*] Creating/updating search index '{index_name}'...")
    result = index_client.create_or_update_index(index)
    print(f"✅ Search index '{index_name}' created/updated")
except Exception as e:
    print(f"❌ Error creating index: {e}")
    raise

# Sample movie data
movies = [
    {"id": "1", "title": "The Dark Knight", "genre": "Action, Crime, Drama", "overview": "Batman raises the stakes in his war on crime with the help of Lt. Jim Gordon and District Attorney Harvey Dent."},
    {"id": "2", "title": "Inception", "genre": "Action, Science Fiction", "overview": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea."},
    {"id": "3", "title": "The Matrix", "genre": "Action, Science Fiction", "overview": "A computer hacker learns about the true nature of his reality and his role in the war against its controllers."},
    {"id": "4", "title": "Interstellar", "genre": "Adventure, Drama, Science Fiction", "overview": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."},
    {"id": "5", "title": "The Shawshank Redemption", "genre": "Drama, Crime", "overview": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."},
    {"id": "6", "title": "Pulp Fiction", "genre": "Crime, Drama", "overview": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption."},
    {"id": "7", "title": "Forrest Gump", "genre": "Comedy, Drama, Romance", "overview": "The presidencies of Kennedy and Johnson unfold through the perspective of an Alabama man with an IQ of 75."},
    {"id": "8", "title": "The Godfather", "genre": "Crime, Drama", "overview": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."},
]

# Initialize OpenAI client for embeddings (via APIM)
print(f"\\n[*] Generating embeddings via APIM...")
client = AzureOpenAI(
    azure_endpoint=f"{apim_gateway_url}/{inference_api_path}",
    api_key=apim_api_key,
    api_version="2025-03-01-preview"
)

# Create search client for uploading
search_client = SearchClient(
    endpoint=search_endpoint,
    index_name=index_name,
    credential=AzureKeyCredential(search_admin_key)
)

# Generate embeddings and upload documents
documents_with_vectors = []
print(f"\\n{'='*80}")
print("🔄 GENERATING EMBEDDINGS FOR MOVIES")
print(f"{'='*80}\\n")

for i, movie in enumerate(movies, 1):
    # Create text to embed (combine title, genre, and overview)
    text_to_embed = f"{movie['title']} {movie['genre']} {movie['overview']}"

    print(f"▶️  {i}/{len(movies)}: {movie['title']}")

    try:
        # Generate embedding via APIM
        start_time = time.time()
        embedding_response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text_to_embed
        )
        embedding_time = time.time() - start_time

        vector = embedding_response.data[0].embedding
        print(f"   ✅ Embedding generated ({embedding_time:.2f}s, {len(vector)} dimensions)")

        # Add vector to document
        doc = {
            "id": movie["id"],
            "title": movie["title"],
            "genre": movie["genre"],
            "overview": movie["overview"],
            "vector": vector
        }
        documents_with_vectors.append(doc)

    except Exception as e:
        print(f"   ❌ Error generating embedding: {str(e)[:100]}")

# Upload documents to index
if documents_with_vectors:
    print(f"\\n[*] Uploading {len(documents_with_vectors)} documents to index...")
    try:
        result = search_client.upload_documents(documents=documents_with_vectors)
        print(f"✅ Uploaded {len(documents_with_vectors)} documents successfully")
    except Exception as e:
        print(f"❌ Error uploading documents: {e}")
else:
    print("\\n⚠️  No documents to upload")

print(f"\\n{'='*80}")
print("📊 SUMMARY")
print(f"{'='*80}")
print(f"Index Name: {index_name}")
print(f"Documents Indexed: {len(documents_with_vectors)}")
print(f"Vector Dimensions: 1536 (text-embedding-3-small)")
print(f"Embeddings via: APIM with corrected semantic caching policy")
print("\\n[OK] Step 1 Complete - Index ready for vector search")
"""

# Cell 63: Test Vector Search with RAG Pattern
cell_63_code = """# Lab 11: Vector Searching - Step 2: Test RAG Pattern

from azure.search.documents.models import VectorizedQuery

print("\\n[*] Step 2: Testing vector search with RAG pattern...")

# Sample query
query = "What are the best superhero movies?"

print(f"\\n{'='*80}")
print("🔍 TESTING VECTOR SEARCH + RAG PATTERN")
print(f"{'='*80}")
print(f"\\nQuery: '{query}'\\n")

try:
    # Step 1: Convert query to embedding
    print("▶️  Step 1: Generating query embedding...")
    start_time = time.time()
    embedding_response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_vector = embedding_response.data[0].embedding
    embedding_time = time.time() - start_time
    print(f"   ✅ Query embedding generated ({embedding_time:.2f}s, {len(query_vector)} dimensions)")

    # Step 2: Vector search
    print("\\n▶️  Step 2: Performing vector search...")
    vector_query = VectorizedQuery(vector=query_vector, k_nearest_neighbors=3, fields="vector")

    start_time = time.time()
    results = search_client.search(
        search_text=None,
        vector_queries=[vector_query],
        select=["id", "title", "genre", "overview"]
    )
    search_time = time.time() - start_time

    # Collect results
    search_results = []
    for result in results:
        search_results.append({
            'title': result['title'],
            'genre': result['genre'],
            'overview': result['overview'],
            'score': result['@search.score']
        })

    print(f"   ✅ Vector search complete ({search_time:.2f}s)")
    print(f"   Found {len(search_results)} relevant movies\\n")

    # Display results
    print("   Top Matches:")
    for i, r in enumerate(search_results, 1):
        print(f"   {i}. {r['title']} (Score: {r['score']:.4f})")
        print(f"      Genre: {r['genre']}")
        print(f"      Overview: {r['overview'][:80]}...\\n")

    # Step 3: RAG - Use search results as context for LLM
    print("\\n▶️  Step 3: Generating answer with RAG pattern...")

    # Build context from search results
    context = "\\n\\n".join([
        f"Movie: {r['title']}\\n"
        f"Genre: {r['genre']}\\n"
        f"Overview: {r['overview']}"
        for r in search_results
    ])

    # Call LLM with context
    start_time = time.time()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful movie recommendation assistant. Use the provided movie context to answer questions."
            },
            {
                "role": "user",
                "content": f"Context (from vector search):\\n{context}\\n\\nQuestion: {query}"
            }
        ],
        max_tokens=300
    )
    llm_time = time.time() - start_time

    answer = response.choices[0].message.content

    print(f"   ✅ Answer generated ({llm_time:.2f}s)\\n")

    # Display RAG result
    print(f"{'='*80}")
    print("🎬 RAG ANSWER")
    print(f"{'='*80}")
    print(f"\\n{answer}\\n")

    print(f"{'='*80}")
    print("📊 PERFORMANCE METRICS")
    print(f"{'='*80}")
    print(f"Query Embedding Time: {embedding_time:.2f}s")
    print(f"Vector Search Time:   {search_time:.2f}s")
    print(f"LLM Generation Time:  {llm_time:.2f}s")
    print(f"Total Time:           {embedding_time + search_time + llm_time:.2f}s")

    print("\\n[OK] Step 2 Complete - RAG pattern successful")

except Exception as e:
    print(f"\\n❌ Error during vector search: {e}")

print("\\n" + "="*80)
print("🎉 LAB 11 COMPLETE: VECTOR SEARCHING + RAG")
print("="*80)
print("\\nWhat you learned:")
print("✅ How to create vector search indexes in Azure AI Search")
print("✅ How to generate embeddings via APIM")
print("✅ How to perform vector similarity search")
print("✅ How to implement RAG (Retrieval-Augmented Generation)")
print("\\nKey Benefits:")
print("🔍 Semantic Search: Find content by meaning, not just keywords")
print("🎯 RAG Pattern: Provide relevant context to improve LLM answers")
print("📊 Better Answers: Grounded in your actual data")
print("💰 Cost Efficient: Only retrieve what's needed")
"""

# Update cells
print("\n[*] Updating cells 62-63...")
notebook['cells'][62]['source'] = cell_62_code
notebook['cells'][63]['source'] = cell_63_code

# Save notebook
backup_path = notebook_path.with_suffix('.ipynb.backup-vector-fix')
print(f"\n[*] Creating backup: {backup_path}")
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f"[*] Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("\n" + "=" * 80)
print("✅ VECTOR SEARCH CELLS FIXED!")
print("=" * 80)
print("\nChanges Made:")
print("  📝 Cell 62: Setup Azure AI Search + Generate Embeddings")
print("             - Creates vector index with 1536 dimensions")
print("             - Uses APIM for embeddings (via corrected policy)")
print("             - Indexes 8 sample movies with vector embeddings")
print("  📝 Cell 63: Test Vector Search + RAG Pattern")
print("             - Converts query to embedding via APIM")
print("             - Performs vector similarity search")
print("             - Uses search results as context for LLM (RAG)")
print("\n🎯 Next: Run cells 62-63 in the notebook!")
print("=" * 80)
