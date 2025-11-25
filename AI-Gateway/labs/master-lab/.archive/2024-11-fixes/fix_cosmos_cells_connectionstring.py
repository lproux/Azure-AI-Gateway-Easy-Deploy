#!/usr/bin/env python3
"""
Fix Cosmos DB cells (58-61) to use connection string/key auth like the working message-storing notebook
Instead of Azure AD which requires complex RBAC setup
"""
import json
from pathlib import Path

print("=" * 80)
print("🔧 FIXING COSMOS DB CELLS (58-61)")
print("=" * 80)
print("\nChanging from: Azure AD (DefaultAzureCredential)")
print("Changing to: Connection String / API Key (like working notebook)")

# Load master notebook
notebook_path = Path('master-ai-gateway-fix-MCP-clean.ipynb')
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

print(f"\nLoaded notebook with {len(notebook['cells'])} cells")

# Cell 58: Setup Cosmos DB using Key Authentication
cell_58_code = """# Lab 10: Message Storing - Step 1: Setup Cosmos DB
# FIXED: Using connection string/key auth (like working message-storing notebook)

import os
from pathlib import Path
from dotenv import load_dotenv

env_file = Path('master-lab.env')
if env_file.exists():
    load_dotenv(env_file)
    print("[config] Loaded: master-lab.env")

from azure.cosmos import CosmosClient, PartitionKey, exceptions

# Get Cosmos DB config
cosmos_endpoint = os.environ.get('COSMOS_ENDPOINT')
cosmos_key = os.environ.get('COSMOS_KEY')  # Using KEY instead of Azure AD
cosmos_account = os.environ.get('COSMOS_ACCOUNT_NAME')

database_name = "messages-db"
container_name = "conversations"

print("\\n[*] Step 1: Setting up Cosmos DB for message storage...")
print(f"    Cosmos Account: {cosmos_account}")
print(f"    Endpoint: {cosmos_endpoint}")
print(f"    Database: {database_name}")
print(f"    Container: {container_name}")

try:
    # Use KEY authentication (simpler, like working notebook)
    print("\\n[*] Creating Cosmos DB client with API key...")
    client = CosmosClient(cosmos_endpoint, cosmos_key)
    print("✅ Cosmos DB client created successfully")

    # Create database
    print(f"\\n[*] Creating database '{database_name}'...")
    try:
        database = client.create_database(id=database_name)
        print(f"✅ Database '{database_name}' created")
    except exceptions.CosmosResourceExistsError:
        database = client.get_database_client(database_name)
        print(f"✅ Database '{database_name}' already exists")

    # Create container
    print(f"\\n[*] Creating container '{container_name}'...")
    try:
        container = database.create_container(
            id=container_name,
            partition_key=PartitionKey(path="/conversationId"),
            offer_throughput=400
        )
        print(f"✅ Container '{container_name}' created")
    except exceptions.CosmosResourceExistsError:
        container = database.get_container_client(container_name)
        print(f"✅ Container '{container_name}' already exists")

    print("\\n✅ Cosmos DB setup complete!")
    print("\\n📋 Summary:")
    print(f"   Database: {database_name}")
    print(f"   Container: {container_name}")
    print(f"   Partition Key: /conversationId")
    print("\\n[OK] Step 1 Complete - Ready to store messages")

except Exception as e:
    print(f"\\n❌ Error setting up Cosmos DB: {e}")
    print(f"\\n💡 Check:")
    print("   - COSMOS_ENDPOINT is correct in master-lab.env")
    print("   - COSMOS_KEY is correct in master-lab.env")
    print("   - Cosmos DB allows public network access")
"""

# Cell 59: Generate and Store Conversations
cell_59_code = """# Lab 10: Message Storing - Step 2: Generate and Store Conversations

from openai import AzureOpenAI
import time
import uuid
from datetime import datetime

# Get API config
apim_gateway_url = os.environ.get('APIM_GATEWAY_URL')
apim_api_key = os.environ.get('APIM_API_KEY')
inference_api_path = os.environ.get('INFERENCE_API_PATH', 'inference')

print("\\n[*] Step 2: Generating sample conversations and storing in Cosmos DB...")
print(f"    Endpoint: {apim_gateway_url}/{inference_api_path}")
print(f"    Model: gpt-4o-mini")

# Initialize OpenAI client
client_openai = AzureOpenAI(
    azure_endpoint=f"{apim_gateway_url}/{inference_api_path}",
    api_key=apim_api_key,
    api_version="2025-03-01-preview"
)

# Sample questions for conversation
questions = [
    "What is Azure API Management?",
    "Explain semantic caching in simple terms",
    "How do I optimize AI costs?",
    "What are the benefits of using APIM with Azure OpenAI?",
    "Tell me about vector databases"
]

conversation_id = str(uuid.uuid4())
messages_stored = []

print(f"\\n{'='*80}")
print("💬 GENERATING CONVERSATIONS")
print(f"{'='*80}")
print(f"Conversation ID: {conversation_id}\\n")

for i, question in enumerate(questions, 1):
    print(f"▶️  Message {i}/{len(questions)}: {question}")

    try:
        # Call OpenAI
        start_time = time.time()
        response = client_openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": question}
            ],
            max_tokens=150
        )
        response_time = time.time() - start_time

        # Extract response
        assistant_message = response.choices[0].message.content
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens

        print(f"   ✅ Response received ({response_time:.2f}s, {total_tokens} tokens)")

        # Store in Cosmos DB
        message_doc = {
            "id": str(uuid.uuid4()),
            "conversationId": conversation_id,
            "messageNumber": i,
            "timestamp": datetime.utcnow().isoformat(),
            "userMessage": question,
            "assistantMessage": assistant_message,
            "model": "gpt-4o-mini",
            "promptTokens": prompt_tokens,
            "completionTokens": completion_tokens,
            "totalTokens": total_tokens,
            "responseTime": response_time
        }

        container.create_item(body=message_doc)
        messages_stored.append(message_doc)
        print(f"   💾 Stored in Cosmos DB\\n")

    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}\\n")

print(f"{'='*80}")
print("📊 CONVERSATION SUMMARY")
print(f"{'='*80}")
print(f"Total Messages: {len(messages_stored)}")
print(f"Conversation ID: {conversation_id}")

if messages_stored:
    total_tokens_used = sum(m['totalTokens'] for m in messages_stored)
    print(f"Total Tokens Used: {total_tokens_used}")
    print(f"\\n✅ All messages stored successfully!")
else:
    print("\\n⚠️  No messages were stored")

print("\\n[OK] Step 2 Complete - Conversations stored in Cosmos DB")
"""

# Cell 60: Query and Display Stored Messages
cell_60_code = """# Lab 10: Message Storing - Step 3: Query Stored Messages

import pandas as pd

print("\\n[*] Step 3: Querying stored messages from Cosmos DB...")

try:
    # Query all messages (limit to recent 20)
    query = "SELECT * FROM c ORDER BY c.timestamp DESC OFFSET 0 LIMIT 20"

    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))

    print(f"\\n✅ Found {len(items)} messages")

    if items:
        # Create DataFrame for better visualization
        df = pd.DataFrame(items)

        # Select relevant columns
        if 'timestamp' in df.columns:
            display_cols = ['timestamp', 'conversationId', 'messageNumber',
                          'userMessage', 'totalTokens', 'responseTime']
            # Only show columns that exist
            display_cols = [col for col in display_cols if col in df.columns]

            print("\\n📋 Recent Messages:")
            print(df[display_cols].to_string(index=False, max_colwidth=50))

            # Summary statistics
            print(f"\\n📊 Statistics:")
            print(f"   Total messages: {len(df)}")
            print(f"   Unique conversations: {df['conversationId'].nunique()}")
            if 'totalTokens' in df.columns:
                print(f"   Total tokens: {df['totalTokens'].sum()}")
                print(f"   Average tokens per message: {df['totalTokens'].mean():.1f}")
            if 'responseTime' in df.columns:
                print(f"   Average response time: {df['responseTime'].mean():.2f}s")
        else:
            print("\\nMessages found but unexpected format")
            print(df.head())
    else:
        print("\\n⚠️  No messages found in database")
        print("   Run Step 2 first to generate and store conversations")

    print("\\n[OK] Step 3 Complete - Query successful")

except Exception as e:
    print(f"\\n❌ Error querying Cosmos DB: {e}")

print("\\n" + "="*80)
print("🎉 LAB 10 COMPLETE: MESSAGE STORING")
print("="*80)
print("\\nWhat you learned:")
print("✅ How to set up Cosmos DB for storing AI conversations")
print("✅ How to capture prompts, completions, and token counts")
print("✅ How to query and analyze stored conversation data")
print("✅ How to track usage patterns and costs")
print("\\nKey Benefits:")
print("📊 Analytics: Understand usage patterns and trends")
print("💰 Cost Tracking: Monitor token usage and costs")
print("🔍 Auditing: Maintain complete conversation history")
print("📈 Insights: Analyze response quality and performance")
"""

# Update cells
print("\\n[*] Updating cells 58-60...")
notebook['cells'][58]['source'] = cell_58_code
notebook['cells'][59]['source'] = cell_59_code
notebook['cells'][60]['source'] = cell_60_code

# Save notebook
backup_path = notebook_path.with_suffix('.ipynb.backup-cosmos-fix')
print(f"\\n[*] Creating backup: {backup_path}")
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f"[*] Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("\\n" + "=" * 80)
print("✅ COSMOS DB CELLS FIXED!")
print("=" * 80)
print("\\nChanges Made:")
print("  📝 Cell 58: Setup using API key (instead of Azure AD)")
print("             - Uses COSMOS_KEY from master-lab.env")
print("             - No RBAC permissions needed!")
print("             - Simpler and matches working notebook")
print("  📝 Cell 59: Generate and store conversations")
print("             - Stores messages with full metadata")
print("             - Tracks tokens and response times")
print("  📝 Cell 60: Query and display stored messages")
print("             - Shows recent messages with statistics")
print("             - Analyzes token usage and performance")
print("\\n🎯 Next: Run cells 58-60 in the notebook!")
print("=" * 80)
