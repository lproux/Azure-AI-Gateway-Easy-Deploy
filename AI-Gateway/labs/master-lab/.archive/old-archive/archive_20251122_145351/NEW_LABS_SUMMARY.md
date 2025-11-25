# New Labs Added to Master Notebook

**Date**: 2025-11-22
**Total New Labs**: 3
**Total New Cells**: 13 (6 + 4 + 3)
**Notebook**: master-ai-gateway-fix-MCP-clean.ipynb

---

## 📋 Overview

Three new advanced labs have been added to your master notebook, all using **existing deployed resources** - no additional Azure deployments required!

### New Lab Structure

```
Lab 08: Model Routing
Lab 09: Semantic Caching (NEW) ✨
Lab 10: Message Storing (NEW) ✨
Lab 11: Vector Searching with RAG (NEW) ✨
Lab 12: AI Foundry SDK (previously Lab 10)
Lab 13: AI Foundry DeepSeek (previously Lab 11)
```

---

## 🎯 Lab 09: Semantic Caching

### What It Does

Demonstrates APIM's semantic caching capability that uses **vector proximity** to cache similar prompts, dramatically reducing costs and latency for repetitive queries.

### Key Features

- **Intelligent Caching**: Caches responses based on semantic similarity (not exact matches)
- **Similarity Threshold**: 0.8 (80% similarity triggers cache hit)
- **Cache Duration**: 120 seconds (2 minutes)
- **Performance Gains**: 10-50x faster responses for similar queries

### Resources Used (Already Deployed)

✅ **Redis Cache**
- Host: `REDIS_HOST` from master-lab.env
- Port: `REDIS_PORT` (10000)
- Key: `REDIS_KEY`

✅ **Embedding Model**: `text-embedding-3-small`
- Endpoint: `MODEL_TEXT_EMBEDDING_3_SMALL_ENDPOINT_R1`
- Region: UK South

✅ **APIM Service**: Your existing API Management gateway

✅ **GPT-4o-mini**: For testing

### Lab Cells (6 Total)

1. **Header Cell**: Introduction and architecture explanation
2. **Configure Embeddings Backend**: Creates embeddings-backend in APIM
3. **Apply Semantic Caching Policy**: Updates APIM policy with cache lookup/store
4. **Test Performance**: Runs 20 similar queries to demonstrate caching
5. **Visualize Results**: Plots response times showing cache hits
6. **Reset Policy** (Optional): Removes semantic caching

### Example Test

```python
# Sample questions (semantically similar)
questions = [
    "How to Brew the Perfect Cup of Coffee?",
    "What are the steps to Craft the Ideal Espresso?",
    "Tell me how to create the best steaming Java?",
]

# First request: ~1-2 seconds (backend call)
# Subsequent similar requests: ~0.1-0.2 seconds (cache hit)
# Speed improvement: 10-20x faster!
```

### Expected Output

```
▶️  Run 1/20: How to Brew the Perfect Cup of Coffee?
   ⏱️  1.234s - 🔥 BACKEND CALL

▶️  Run 2/20: What are the steps to Craft the Ideal Espresso?
   ⏱️  0.156s - 🎯 CACHE HIT

▶️  Run 3/20: Tell me how to create the best steaming Java?
   ⏱️  0.143s - 🎯 CACHE HIT

📊 PERFORMANCE SUMMARY
Average Time:       0.298s
Likely Cache Hits:  17/20 (85%)
```

---

## 📊 Lab 10: Message Storing with Cosmos DB

### What It Does

Captures and stores AI conversation data (prompts, completions, token counts) in Cosmos DB for analytics, auditing, and cost tracking.

### Key Features

- **Conversation History**: Complete record of all AI interactions
- **Token Usage Tracking**: Monitor costs and usage patterns
- **Analytics Dashboard**: Query and analyze stored data
- **Compliance Ready**: Maintain audit trail for regulatory requirements

### Resources Used (Already Deployed)

✅ **Cosmos DB**
- Account: `COSMOS_ACCOUNT_NAME` from master-lab.env
- Endpoint: `COSMOS_ENDPOINT`
- Key: `COSMOS_KEY`
- Database: `llmdb` (created automatically)
- Container: `messages` (created automatically)

✅ **APIM Gateway**: For routing API calls

✅ **GPT-4o-mini**: For generating conversations

### Lab Cells (4 Total)

1. **Header Cell**: Introduction and architecture explanation
2. **Setup Cosmos DB**: Creates database and container
3. **Generate Sample Conversations**: Stores 5 conversations in Cosmos DB
4. **Query and Analyze**: Retrieves and displays analytics

### Data Schema

```json
{
  "id": "uuid",
  "conversationId": "conversation-uuid",
  "timestamp": "2025-11-22T10:30:00Z",
  "model": "gpt-4o-mini",
  "prompt": "What is Azure API Management?",
  "completion": "Azure API Management is...",
  "promptTokens": 42,
  "completionTokens": 156,
  "totalTokens": 198,
  "responseTime": 1.234
}
```

### Example Analytics Output

```
📊 MESSAGE ANALYTICS
══════════════════════════════════════════════════════════════

📈 Token Usage:
   Total Tokens: 1,234
   Avg Tokens per Message: 247
   Max Tokens: 312
   Min Tokens: 189

⏱️  Response Times:
   Avg Response Time: 0.856s
   Fastest: 0.234s
   Slowest: 1.456s

💬 Conversations:
   Unique Conversations: 1
   Total Messages: 5

💰 Token Usage by Conversation:
   conversation-id    totalTokens    messageCount
   abc-123-def        1,234          5
```

### Use Cases

- **Cost Optimization**: Track token usage to optimize prompts
- **Quality Monitoring**: Analyze response quality over time
- **Compliance**: Maintain audit trail for regulated industries
- **Insights**: Understand user interaction patterns

---

## 🔍 Lab 11: Vector Searching with RAG Pattern

### What It Does

Implements **Retrieval Augmented Generation (RAG)** using Azure AI Search and embeddings to provide accurate, context-aware responses based on your own data.

### Key Features

- **Vector Embeddings**: Convert text to 1536-dimensional vectors
- **Semantic Search**: Find similar documents using vector similarity
- **Context Injection**: Add retrieved documents to LLM prompts
- **Grounded Responses**: Answers based on your data, not LLM training

### Resources Used (Already Deployed)

✅ **Azure AI Search**
- Service: `SEARCH_SERVICE_NAME` from master-lab.env
- Endpoint: `SEARCH_ENDPOINT`
- Admin Key: `SEARCH_ADMIN_KEY`
- Index: `movies-rag` (created automatically)

✅ **Embedding Model**: `text-embedding-3-small`
- For vectorizing queries and documents

✅ **GPT-4o-mini**: For generating augmented responses

✅ **APIM Gateway**: Routes all requests

### Lab Cells (3 Total)

1. **Header Cell**: Introduction to RAG and architecture
2. **Create Search Index**: Sets up vector index and loads movie data
3. **Test RAG Pattern**: Demonstrates end-to-end RAG workflow

### RAG Workflow

```
1. User Query: "What are the best superhero movies?"
   ↓
2. Convert to Embedding (1536 dimensions)
   ↓
3. Vector Search in Azure AI Search
   → Find 3 most similar movie descriptions
   ↓
4. Build Context from Results
   → Movie: The Avengers
   → Movie: The Dark Knight
   → Movie: The Matrix
   ↓
5. Inject into LLM Prompt
   → "Based on these movies, answer the question..."
   ↓
6. Generate Response
   → "The best superhero movies include..."
```

### Sample Movie Data (8 Movies Included)

- The Avengers (Action, Sci-Fi)
- The Dark Knight (Action, Crime, Drama)
- Inception (Action, Sci-Fi, Thriller)
- Interstellar (Adventure, Drama, Sci-Fi)
- The Matrix (Action, Sci-Fi)
- Pulp Fiction (Crime, Drama)
- Forrest Gump (Drama, Romance)
- The Shawshank Redemption (Drama)

### Example Output

```
❓ Query: What are the best superhero movies?

[1] Converting query to embedding...
    ✅ Query vectorized (1536 dimensions)

[2] Searching for similar movies...
    ✅ Found 3 relevant movies:
       1. The Avengers (Action, Sci-Fi)
       2. The Dark Knight (Action, Crime, Drama)
       3. The Matrix (Action, Sci-Fi)

[3] Generating AI response with context...

💡 AI Response:
   Based on the provided movie data, the best superhero movies are:

   1. **The Avengers** - Earth's mightiest heroes unite to fight
      the alien invasion led by Loki. Classic superhero team-up.

   2. **The Dark Knight** - Batman faces his greatest psychological
      challenge against the Joker. Widely considered one of the best
      superhero films ever made.

   Both films showcase heroic characters facing extraordinary threats
   and exemplify the superhero genre at its finest.

📊 Tokens used: 187
```

---

## 🚀 How to Use the New Labs

### Prerequisites

All labs use existing resources from master-lab.env. Make sure you've run:

1. **Cell 021**: Generate master-lab.env (contains all required credentials)

### Additional Python Packages Needed

```bash
# For Lab 10 (Message Storing)
pip install azure-cosmos pandas

# For Lab 11 (Vector Searching)
pip install azure-search-documents
```

### Recommended Execution Order

1. **Lab 09: Semantic Caching** (Independent)
   - Tests caching performance
   - Can reset policy when done

2. **Lab 10: Message Storing** (Independent)
   - Creates Cosmos DB database
   - Stores sample conversations
   - Queries and analyzes data

3. **Lab 11: Vector Searching** (Independent)
   - Creates search index
   - Loads movie vectors
   - Demonstrates RAG pattern

**All labs are independent** - you can run them in any order!

---

## 📊 Benefits Summary

### Lab 09: Semantic Caching

**Cost Savings**: 💰💰💰💰💰
- Reduce Azure OpenAI API calls by 70-90%
- Save on token costs for repetitive queries
- Lower latency improves user experience

**Complexity**: ⭐⭐ (Easy to implement)

### Lab 10: Message Storing

**Value**: 📊📊📊📊
- Complete audit trail for compliance
- Understand usage patterns
- Optimize prompts based on token analytics
- Track costs per conversation

**Complexity**: ⭐⭐ (Easy to implement)

### Lab 11: Vector Searching (RAG)

**Accuracy**: 🎯🎯🎯🎯🎯
- Responses grounded in your data
- Reduces hallucinations
- Enables enterprise AI applications
- Semantic search > keyword search

**Complexity**: ⭐⭐⭐ (Moderate - vector concepts)

---

## 🔧 Troubleshooting

### Lab 09 (Semantic Caching)

**Issue**: "embeddings-backend not found"
- **Solution**: Run Step 1 (Configure Embeddings Backend) first

**Issue**: Low cache hit rate
- **Solution**: Questions may be too different (< 80% similarity)
- Try more similar phrasings
- Check cache TTL (120 seconds)

### Lab 10 (Message Storing)

**Issue**: "ModuleNotFoundError: No module named 'azure.cosmos'"
- **Solution**: `pip install azure-cosmos`

**Issue**: "Database/container already exists"
- **Solution**: This is normal - lab will reuse existing resources

### Lab 11 (Vector Searching)

**Issue**: "ModuleNotFoundError: No module named 'azure.search'"
- **Solution**: `pip install azure-search-documents`

**Issue**: No search results found
- **Solution**: Run Step 1 (Create Search Index) first to load movie data

---

## 📁 Files Created/Modified

### Created Files

1. `add_semantic_caching_lab.py` - Script that added Lab 09
2. `add_message_and_vector_labs.py` - Script that added Labs 10 & 11
3. `semantic-caching-policy.xml` - APIM policy for semantic caching (auto-generated)
4. `backend-embeddings.json` - Backend config for embeddings (auto-generated)

### Modified Files

1. `master-ai-gateway-fix-MCP-clean.ipynb` - Main notebook (3 labs added)

### Backup Files

1. `master-ai-gateway-fix-MCP-clean.ipynb.backup-before-semantic-caching`
2. `master-ai-gateway-fix-MCP-clean.ipynb.backup-before-message-vector-labs`

---

## 🎯 Next Steps

### 1. Open Your Notebook

```bash
# Navigate to the lab directory
cd /mnt/c/Users/lproux/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab

# Open in Jupyter
jupyter notebook master-ai-gateway-fix-MCP-clean.ipynb
```

### 2. Install Additional Packages (if needed)

```bash
pip install azure-cosmos azure-search-documents pandas
```

### 3. Run the Labs

- **Lab 09**: Start at cell labeled "Lab 09: Semantic Caching"
- **Lab 10**: Start at cell labeled "Lab 10: Message Storing"
- **Lab 11**: Start at cell labeled "Lab 11: Vector Searching"

### 4. Explore and Experiment

- Modify similarity thresholds in Lab 09
- Add your own conversation data in Lab 10
- Load your own documents in Lab 11

---

## 💡 Key Takeaways

### What You Now Have

✅ **13 New Cells** across 3 comprehensive labs
✅ **Zero New Deployments** - uses existing infrastructure
✅ **Production-Ready Patterns** - semantic caching, RAG, analytics
✅ **Complete Documentation** - inline explanations and troubleshooting

### Skills Gained

1. **Semantic Caching**: Optimize costs with intelligent caching
2. **Data Analytics**: Track and analyze AI usage patterns
3. **RAG Pattern**: Build enterprise AI with your own data
4. **Vector Search**: Understand embeddings and similarity

---

**🎉 All three labs are ready to use! No additional Azure resources required!**

**Last Updated**: 2025-11-22
**Total Development Time**: ~45 minutes
**Total New Cells**: 13
**Azure Cost**: $0 (uses existing resources)
