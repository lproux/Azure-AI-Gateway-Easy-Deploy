#!/usr/bin/env python3
"""
Fix all Lab 10 cells to use Azure AD authentication
"""
import json
from pathlib import Path

notebook_path = Path('master-ai-gateway-fix-MCP-clean.ipynb')

with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

cells = notebook['cells']

# Cell for Step 2 (Generate Conversations) - uses Azure AD
step2_source = """# Lab 10: Message Storing - Step 2: Generate Sample Conversations

import os
from pathlib import Path
from dotenv import load_dotenv

env_file = Path('master-lab.env')
if env_file.exists():
    load_dotenv(env_file)

from openai import AzureOpenAI
import time
import uuid
from datetime import datetime
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential

# Get configuration
apim_gateway_url = os.environ.get('APIM_GATEWAY_URL')
apim_api_key = os.environ.get('APIM_API_KEY')
inference_api_path = os.environ.get('INFERENCE_API_PATH', 'inference')
cosmos_endpoint = os.environ.get('COSMOS_ENDPOINT')

print("\\n[*] Step 2: Generating sample conversations and storing in Cosmos DB...")
print(f"    Endpoint: {apim_gateway_url}/{inference_api_path}")
print(f"    Model: gpt-4o-mini")

# Initialize OpenAI client
client = AzureOpenAI(
    azure_endpoint=f"{apim_gateway_url}/{inference_api_path}",
    api_key="dummy",
    api_version="2024-08-01-preview"
)

# Initialize Cosmos client with Azure AD
try:
    credential = DefaultAzureCredential()
    cosmos_client = CosmosClient(cosmos_endpoint, credential)
    database = cosmos_client.get_database_client('llmdb')
    container = database.get_container_client('messages')

    # Sample conversations
    conversations = [
        "What is Azure API Management?",
        "Explain semantic caching in simple terms",
        "How do I optimize AI costs?",
        "What are the benefits of using APIM with Azure OpenAI?",
        "Tell me about vector databases"
    ]

    conversation_id = str(uuid.uuid4())
    stored_messages = []

    print(f"\\n{'='*80}")
    print("💬 GENERATING CONVERSATIONS")
    print(f"{'='*80}")
    print(f"Conversation ID: {conversation_id}")

    for i, question in enumerate(conversations, 1):
        print(f"\\n▶️  Message {i}/{len(conversations)}: {question}")

        start_time = time.time()
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful Azure expert."},
                    {"role": "user", "content": question}
                ],
                max_tokens=100,
                extra_headers={'api-key': apim_api_key}
            )

            response_time = time.time() - start_time
            answer = response.choices[0].message.content

            # Create message document
            message_doc = {
                'id': str(uuid.uuid4()),
                'conversationId': conversation_id,
                'timestamp': datetime.utcnow().isoformat(),
                'model': 'gpt-4o-mini',
                'prompt': question,
                'completion': answer,
                'promptTokens': response.usage.prompt_tokens,
                'completionTokens': response.usage.completion_tokens,
                'totalTokens': response.usage.total_tokens,
                'responseTime': round(response_time, 3)
            }

            # Store in Cosmos DB
            container.create_item(body=message_doc)
            stored_messages.append(message_doc)

            print(f"   💬 Response: {answer[:80]}...")
            print(f"   📊 Tokens: {response.usage.total_tokens} ({response.usage.prompt_tokens} + {response.usage.completion_tokens})")
            print(f"   ⏱️  Time: {response_time:.3f}s")
            print(f"   ✅ Stored in Cosmos DB")

            time.sleep(0.5)  # Rate limiting

        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}")

    print(f"\\n{'='*80}")
    print("📊 CONVERSATION SUMMARY")
    print(f"{'='*80}")
    print(f"Total Messages: {len(stored_messages)}")
    print(f"Conversation ID: {conversation_id}")

    if stored_messages:
        total_tokens = sum(m['totalTokens'] for m in stored_messages)
        avg_response_time = sum(m['responseTime'] for m in stored_messages) / len(stored_messages)
        print(f"Total Tokens: {total_tokens}")
        print(f"Avg Response Time: {avg_response_time:.3f}s")

    print(f"\\n[OK] Step 2 Complete - Conversations stored in Cosmos DB")

except Exception as e:
    print(f"\\n❌ Error: {e}")
    print("\\n💡 Make sure:")
    print("   1. You're logged in: az login")
    print("   2. You ran Step 1 to create the database")
"""

# Cell for Step 3 (Query) - uses Azure AD
step3_source = """# Lab 10: Message Storing - Step 3: Query and Analyze Stored Messages

import os
from pathlib import Path
from dotenv import load_dotenv

env_file = Path('master-lab.env')
if env_file.exists():
    load_dotenv(env_file)

cosmos_endpoint = os.environ.get('COSMOS_ENDPOINT')

print("\\n[*] Step 3: Querying stored messages from Cosmos DB...")

try:
    from azure.cosmos import CosmosClient
    from azure.identity import DefaultAzureCredential
    import pandas as pd

    # Connect to Cosmos DB with Azure AD
    credential = DefaultAzureCredential()
    cosmos_client = CosmosClient(cosmos_endpoint, credential)
    database = cosmos_client.get_database_client('llmdb')
    container = database.get_container_client('messages')

    # Query all messages
    query = \"\"\"
        SELECT
            c.timestamp,
            c.conversationId,
            c.model,
            c.prompt,
            c.promptTokens,
            c.completionTokens,
            c.totalTokens,
            c.responseTime
        FROM c
        ORDER BY c.timestamp DESC
    \"\"\"

    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))

    print(f"\\n✅ Found {len(items)} messages in Cosmos DB")

    if items:
        # Display as DataFrame
        df = pd.DataFrame(items)

        print(f"\\n{'='*80}")
        print("📊 MESSAGE ANALYTICS")
        print(f"{'='*80}")

        # Summary statistics
        print(f"\\n📈 Token Usage:")
        print(f"   Total Tokens: {df['totalTokens'].sum()}")
        print(f"   Avg Tokens per Message: {df['totalTokens'].mean():.1f}")
        print(f"   Max Tokens: {df['totalTokens'].max()}")
        print(f"   Min Tokens: {df['totalTokens'].min()}")

        print(f"\\n⏱️  Response Times:")
        print(f"   Avg Response Time: {df['responseTime'].mean():.3f}s")
        print(f"   Fastest: {df['responseTime'].min():.3f}s")
        print(f"   Slowest: {df['responseTime'].max():.3f}s")

        print(f"\\n💬 Conversations:")
        print(f"   Unique Conversations: {df['conversationId'].nunique()}")
        print(f"   Total Messages: {len(df)}")

        # Display recent messages
        print(f"\\n📝 Recent Messages:")
        print(df[['timestamp', 'prompt', 'totalTokens', 'responseTime']].head(10).to_string(index=False))

        # Token distribution by conversation
        if 'conversationId' in df.columns:
            print(f"\\n💰 Token Usage by Conversation:")
            conv_summary = df.groupby('conversationId').agg({
                'totalTokens': 'sum',
                'prompt': 'count'
            }).rename(columns={'prompt': 'messageCount'})
            print(conv_summary.to_string())

        print(f"\\n[OK] Step 3 Complete - Message analytics displayed")
    else:
        print("\\n⚠️  No messages found in database")
        print("   Run Step 2 to generate sample conversations")

except ImportError as e:
    print(f"\\n⚠️  Missing package: {e}")
    print("   Run: pip install azure-cosmos azure-identity pandas")
except Exception as e:
    print(f"\\n❌ Error querying Cosmos DB: {e}")
    print("\\n💡 Make sure you're logged in: az login")

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
updates = [
    ("Lab 10: Message Storing - Step 2", step2_source),
    ("Lab 10: Message Storing - Step 3", step3_source)
]

for search_text, new_source in updates:
    for i, cell in enumerate(cells):
        if cell.get('cell_type') == 'code':
            source = ''.join(cell.get('source', []))
            if search_text in source:
                print(f"Updating: {search_text}")
                cells[i]['source'] = new_source.split('\n')
                cells[i]['outputs'] = []
                break

# Save notebook
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("\n✅ All Lab 10 cells updated to use Azure AD authentication")
print("\nNext steps:")
print("  1. Make sure you're logged in: az login")
print("  2. Restart your kernel")
print("  3. Run Lab 10 cells (57, 58, 59)")
