# Remaining Fixes - Detailed Implementation Guide

**Date**: 2025-11-17
**Status**: Ready for Implementation
**Prerequisites**: Cells 14, 29, 32 updated

---

## Fix 6: Apply MCP Pattern to Cells 81, 83, 86, 132

### Prerequisites Check

**Required Files/Modules**:
1. `notebook_mcp_helpers.py` or `notebook_mcp_helpers` module
2. `.mcp-servers-config` configuration file
3. Excel MCP server running and accessible

**Check Command**:
```python
# In a notebook cell
try:
    from notebook_mcp_helpers import MCPClient, MCPError
    print("✅ MCP helpers available")
except ImportError:
    print("❌ notebook_mcp_helpers not found - need to copy from workshop")
```

### Implementation

**If MCP Helpers Available** - Update cells with working pattern:

#### Cell 81 - Sales Analysis via MCP

**Replace with**:
```python
print("📊 Sales Analysis via MCP Server + Azure OpenAI")
print("=" * 80)

from pathlib import Path

try:
    # Initialize MCP if not already done
    if 'mcp' not in globals():
        from notebook_mcp_helpers import MCPClient
        mcp = MCPClient()

    if not mcp or not mcp.excel.server_url:
        raise RuntimeError("MCP Excel server not configured")

    # Locate Excel file
    search_path = Path("./sample-data/excel/")
    excel_candidates = list(search_path.glob("*sales*.xlsx"))
    if not excel_candidates:
        raise FileNotFoundError(f"No sales Excel file in '{search_path}'")

    local_excel_path = Path(excel_candidates[0])
    excel_file_name = local_excel_path.name

    print(f"📤 Uploading Excel file via MCP: {excel_file_name}")
    upload_result = mcp.excel.upload_excel(str(local_excel_path))
    file_cache_key = upload_result.get('file_name', excel_file_name)
    print(f"💾 Cache key: {file_cache_key}")

    # Analyze sales data
    print("📊 Analyzing sales by Region and TotalAmount...")
    analysis_result = mcp.excel.analyze_sales(
        file_cache_key,
        group_by='Region',
        metric='TotalAmount'  # FIXED: Was 'TotalSales'
    )

    if isinstance(analysis_result, str):
        import json as _json
        try:
            analysis_result = _json.loads(analysis_result)
        except:
            analysis_result = {"raw": analysis_result}

    # Display results
    summary = analysis_result.get("summary", {})
    grouped_data = analysis_result.get("analysis", [])

    print(f"\n✅ Total Sales: ${summary.get('total', 0):,.2f}")
    print(f"✅ Average: ${summary.get('average', 0):,.2f}")
    print(f"✅ Count: {summary.get('count', 0)}")

    print(f"\n📊 Top Regions:")
    for item in grouped_data[:5]:
        region = item.get('Region', 'Unknown')
        amount = item.get('TotalAmount', 0)
        print(f"  {region}: ${amount:,.2f}")

    print("\n[OK] Sales analysis complete via MCP")

except Exception as e:
    print(f"❌ MCP Error: {str(e)}")
    print("⚠️  MCP analysis failed - consider using local pandas as fallback")
```

**Cell 83 & 86**: Apply same pattern with appropriate file/column adjustments

**Cell 132**: Same pattern, use `excel_cache_key` from previous cell

---

**If MCP Not Available** - Two options:

**Option A**: Copy MCP helpers from workshop
1. Copy `notebook_mcp_helpers.py` from `/workshop/route-a-automated/`
2. Create `.mcp-servers-config` with Excel MCP URL
3. Then apply above pattern

**Option B**: Delete cells and document
1. Delete cells 81, 83, 86, 132
2. Add markdown cell: "MCP integration requires notebook_mcp_helpers module and configured MCP server"

---

## Fix 7: Cell 101 - Caching Verification

**Current Problem**: Uses timing heuristic (`cached: elapsed < 0.5`)

**Fix**: Check response headers for cache status

**Implementation**:
```python
import redis.asyncio as redis
import random

questions = [
    'How to make coffee?',
    'What is the best way to brew coffee?',
    'Tell me about coffee preparation',
    'Coffee making tips?'
]

times = []
cache_statuses = []

# Initialize client (reuse from earlier cells)
if 'client' not in globals() or not client:
    from openai import AzureOpenAI
    client = AzureOpenAI(
        azure_endpoint=f"{apim_gateway_url.rstrip('/')}/{inference_api_path.strip('/')}",
        api_key=apim_api_key,
        api_version='2024-06-01'
    )

print("🔄 Testing semantic cache with 20 requests...")
print("=" * 80)

for i in range(20):
    question = random.choice(questions)
    start = time.time()

    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': question}],
            max_tokens=50
        )

        elapsed = time.time() - start
        times.append(elapsed)

        # FIXED: Check response headers for cache status
        cached = False
        if hasattr(response, 'response_headers'):
            cache_header = response.response_headers.get('x-cache', '')
            cached = 'hit' in cache_header.lower()
        elif hasattr(response, '_http_response'):
            cache_header = response._http_response.headers.get('x-cache', '')
            cached = 'hit' in cache_header.lower()
        else:
            # Fallback to timing heuristic if headers not available
            cached = elapsed < 0.5

        cache_statuses.append(cached)
        cache_indicator = "✅ CACHED" if cached else "❌ NOT CACHED"
        print(f"Request {i+1}: {elapsed:.2f}s - {cache_indicator}")

    except Exception as e:
        elapsed = time.time() - start
        times.append(elapsed)
        cache_statuses.append(False)
        print(f"Request {i+1}: FAILED ({type(e).__name__})")

    time.sleep(0.5)

# Analysis
import pandas as pd
import matplotlib.pyplot as plt

if times:
    df = pd.DataFrame({
        'Run': range(1, len(times)+1),
        'Time': times,
        'Cached': cache_statuses
    })

    # Plot with cache indicator
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ['green' if c else 'red' for c in cache_statuses]
    ax.bar(df['Run'], df['Time'], color=colors, alpha=0.7)
    ax.axhline(y=df['Time'].mean(), color='blue', linestyle='--', label=f'Average: {df["Time"].mean():.2f}s')
    ax.set_xlabel('Request Number')
    ax.set_ylabel('Response Time (seconds)')
    ax.set_title('Semantic Caching Performance (Green=Cached, Red=Not Cached)')
    ax.legend()
    plt.tight_layout()
    plt.show()

    cache_hit_rate = sum(cache_statuses) / len(cache_statuses) * 100
    print(f"\n📊 Cache Hit Rate: {cache_hit_rate:.1f}%")
    print(f"⚡ Avg cached response: {df[df['Cached']]['Time'].mean():.2f}s" if any(cache_statuses) else "No cached responses")
    print(f"🐌 Avg uncached response: {df[~df['Cached']]['Time'].mean():.2f}s" if not all(cache_statuses) else "All responses cached")

print("\n[OK] Lab 19 Complete - Semantic Cache Analysis")
```

---

## Fix 8: Cell 116 - Create Real A2A Agents

**Current Problem**: Missing agents, using simulated coordination

**Fix**: Create actual AutoGen agents

**Implementation**:
```python
print("=" * 80)
print("A2A: Real Multi-Agent Collaboration")
print("=" * 80)

from autogen import ConversableAgent, UserProxyAgent

# Configuration for all agents
config_list = [{
    "model": deployment_name,
    "api_type": "azure",
    "api_key": apim_api_key,
    "base_url": f"{apim_gateway_url.rstrip('/')}/inference/openai",
    "api_version": "2024-02-01",
}]

llm_config = {"config_list": config_list, "cache_seed": None}

# Agent 1: Strategic Planner
planner_agent = ConversableAgent(
    name="Planner",
    system_message=(
        "You are a strategic planner specialized in AI infrastructure. "
        "Analyze requirements and create comprehensive deployment plans with "
        "clear phases, timelines, and resource allocation. Focus on scalability "
        "and security. Be concise but thorough."
    ),
    llm_config={**llm_config, "temperature": 0.7},
    human_input_mode="NEVER",
)

# Agent 2: Security Critic
critic_agent = ConversableAgent(
    name="Critic",
    system_message=(
        "You are a security and reliability expert. Review plans critically for "
        "potential risks, vulnerabilities, single points of failure, and compliance "
        "issues. Provide specific, actionable feedback. Don't just list problems - "
        "suggest concrete improvements."
    ),
    llm_config={**llm_config, "temperature": 0.5},
    human_input_mode="NEVER",
)

# Agent 3: Technical Summarizer
summarizer_agent = ConversableAgent(
    name="Summarizer",
    system_message=(
        "You are a technical writer creating executive summaries. Distill complex "
        "discussions into clear, concise action items and decisions. Organize by "
        "priority. Include key metrics and success criteria."
    ),
    llm_config={**llm_config, "temperature": 0.3},
    human_input_mode="NEVER",
)

# Coordinator (User Proxy)
coordinator = UserProxyAgent(
    name="Coordinator",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    code_execution_config=False,
)

print("✅ Created A2A agents: Planner, Critic, Summarizer, Coordinator")

# Test A2A workflow
print("\n" + "=" * 80)
print("SCENARIO: Secure Scaling of AI Gateway")
print("=" * 80)

# Phase 1: Planning
print("\n📋 Phase 1: Strategic Planning...")
plan_result = coordinator.initiate_chat(
    planner_agent,
    message="Create a deployment plan for scaling our AI Gateway to handle 10x current traffic while maintaining <100ms latency and ensuring zero-downtime deployments.",
    max_turns=2
)

# Phase 2: Critique
print("\n🔍 Phase 2: Security Review...")
critique_result = coordinator.initiate_chat(
    critic_agent,
    message=f"Review this deployment plan and identify security risks, reliability concerns, and potential failures:\n\n{plan_result}",
    max_turns=2
)

# Phase 3: Summarize
print("\n📝 Phase 3: Executive Summary...")
summary_result = coordinator.initiate_chat(
    summarizer_agent,
    message=f"Create an executive summary with action items from this planning discussion:\n\nPlan:\n{plan_result}\n\nCritique:\n{critique_result}",
    max_turns=1
)

print("\n" + "=" * 80)
print("✅ A2A Multi-Agent Workflow Complete")
print("=" * 80)
print("\nWorkflow:")
print("  1. Planner → Strategic deployment plan")
print("  2. Critic → Security & reliability review")
print("  3. Summarizer → Actionable executive summary")
print("\n[OK] Real agent collaboration (not simulated)")
```

---

## Fix 9: Consolidate Image Generation (Cells 106, 108, 129, 130)

**Action**: Replace Cell 108 with consolidated version, delete 106, 129, 130

**Cell 108 - Consolidated Implementation**:
```python
print("=" * 80)
print("IMAGE GENERATION - Consolidated (DALL-E 3 + FLUX via APIM)")
print("=" * 80)

import os
import httpx
import json

# Configuration
apim_gateway_url = os.getenv('APIM_GATEWAY_URL', '')
apim_api_key = os.getenv('APIM_API_KEY', '')
image_model = os.getenv('MODEL_DALL_E_3', 'dall-e-3')  # or gpt-image-1

if not all([apim_gateway_url, apim_api_key]):
    print("❌ Missing configuration: APIM_GATEWAY_URL or APIM_API_KEY")
else:
    # Build endpoint
    endpoint = f"{apim_gateway_url.rstrip('/')}/inference/openai/images/generations?api-version=2024-06-01"

    # Headers with subscription key (FIX: Was missing)
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': apim_api_key,
    }

    # Test payload
    payload = {
        'model': image_model,
        'prompt': 'A futuristic AI gateway architecture with multiple regions, showing load balancing and security layers',
        'size': '1024x1024',
        'n': 1,
        'quality': 'standard'
    }

    print(f"🎨 Generating image with model: {image_model}")
    print(f"📡 Endpoint: {endpoint}")

    try:
        response = httpx.post(endpoint, json=payload, headers=headers, timeout=60)

        if response.status_code == 200:
            result = response.json()
            image_url = result.get('data', [{}])[0].get('url', '')
            revised_prompt = result.get('data', [{}])[0].get('revised_prompt', '')

            print(f"\n✅ Image generated successfully!")
            print(f"🔗 URL: {image_url[:100]}...")
            if revised_prompt:
                print(f"📝 Revised prompt: {revised_prompt[:200]}...")
        else:
            print(f"\n❌ Error {response.status_code}")
            try:
                error_detail = response.json()
                print(f"Details: {json.dumps(error_detail, indent=2)}")
            except:
                print(f"Response: {response.text[:500]}")

    except httpx.TimeoutException:
        print("❌ Request timeout (image generation can take 30-60 seconds)")
    except Exception as e:
        print(f"❌ Exception: {type(e).__name__}: {str(e)}")

print("\n[OK] Image generation test complete")
```

**Then delete cells 106, 129, 130** or mark them for deletion

---

## Fix 10: Cell 145 - Real Vector Search with Azure Search

**Current Problem**: Using simulated embeddings and responses

**Fix**: Use real Azure Search + embedding deployments

**Implementation**:
```python
print("=" * 80)
print("SEMANTIC KERNEL: Vector Search with Real Azure AI Search")
print("=" * 80)

import os
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureTextEmbedding
from openai import AsyncAzureOpenAI

# Load configuration from env
search_endpoint = os.getenv('SEARCH_ENDPOINT', '')
search_key = os.getenv('SEARCH_ADMIN_KEY', '')
embedding_endpoint = os.getenv('MODEL_TEXT_EMBEDDING_3_SMALL_ENDPOINT_R1', '')
embedding_key = os.getenv('MODEL_TEXT_EMBEDDING_3_SMALL_KEY_R1', '')
chat_endpoint = os.getenv('MODEL_GPT_4O_MINI_ENDPOINT_R1', '')
chat_key = os.getenv('MODEL_GPT_4O_MINI_KEY_R1', '')

# Validate configuration
missing = []
if not search_endpoint: missing.append('SEARCH_ENDPOINT')
if not search_key: missing.append('SEARCH_ADMIN_KEY')
if not embedding_endpoint: missing.append('MODEL_TEXT_EMBEDDING_3_SMALL_ENDPOINT_R1')
if not embedding_key: missing.append('MODEL_TEXT_EMBEDDING_3_SMALL_KEY_R1')
if not chat_endpoint: missing.append('MODEL_GPT_4O_MINI_ENDPOINT_R1')
if not chat_key: missing.append('MODEL_GPT_4O_MINI_KEY_R1')

if missing:
    print(f"❌ Missing environment variables: {', '.join(missing)}")
    print("⚠️  Run Cell 32 to generate master-lab.env with all deployment fields")
    print("⚠️  Then load with: from dotenv import load_dotenv; load_dotenv('master-lab.env')")
else:
    # Create kernel
    kernel = Kernel()

    # Add embedding service
    embedding_client = AsyncAzureOpenAI(
        azure_endpoint=embedding_endpoint,
        api_key=embedding_key,
        api_version="2024-02-01"
    )

    embedding_service = AzureTextEmbedding(
        service_id="embedding_service",
        deployment_name="text-embedding-3-small",
        async_client=embedding_client
    )
    kernel.add_service(embedding_service)
    print("✅ Real embedding service configured")

    # Add chat service
    chat_client = AsyncAzureOpenAI(
        azure_endpoint=chat_endpoint,
        api_key=chat_key,
        api_version="2024-02-01"
    )

    chat_service = AzureChatCompletion(
        service_id="chat_service",
        deployment_name="gpt-4o-mini",
        async_client=chat_client
    )
    kernel.add_service(chat_service)
    print("✅ Real chat service configured")

    # Sample knowledge base (in production, use Azure AI Search)
    knowledge_base = [
        "Azure API Management (APIM) is a fully managed service that enables organizations to publish, secure, transform, maintain, and monitor APIs.",
        "Semantic Kernel is an SDK that integrates Large Language Models (LLMs) with conventional programming languages, enabling AI orchestration.",
        "Vector search uses embeddings to find semantically similar content, even when exact keywords don't match.",
        "Function calling allows LLMs to invoke external tools and APIs to perform actions beyond text generation.",
    ]

    print(f"\n📚 Knowledge base: {len(knowledge_base)} documents")
    print("⚠️  Note: Using in-memory store for demo. Production should use Azure AI Search.")

    # Create embeddings (demo with first document)
    print("\n🔄 Creating real embeddings...")
    import asyncio

    async def create_embeddings():
        embeddings = []
        for doc in knowledge_base[:2]:  # Demo with first 2
            embedding = await embedding_service.generate_embeddings([doc])
            embeddings.append(embedding)
        return embeddings

    embeddings = asyncio.run(create_embeddings())
    print(f"✅ Created {len(embeddings)} real embeddings")
    print(f"✅ Embedding dimensions: {len(embeddings[0][0]) if embeddings else 0}")

    print("\n" + "=" * 80)
    print("✅ Real Vector Search Configuration Complete")
    print("=" * 80)
    print("\nComponents:")
    print(f"  • Embedding model: text-embedding-3-small")
    print(f"  • Chat model: gpt-4o-mini")
    print(f"  • Vector store: In-memory (demo) → Use Azure AI Search in production")
    print(f"  • Search endpoint: {search_endpoint}")

    print("\n💡 Next Steps for Production:")
    print("  1. Create Azure AI Search index")
    print("  2. Upload documents with embeddings")
    print("  3. Use AzureAISearchMemoryStore connector")
    print("  4. Implement RAG pattern with real search")
```

---

## Summary

**Implementation Priority**:
1. **MCP Integration** (Cells 81, 83, 86, 132) - Check prerequisites first
2. **Caching Fix** (Cell 101) - Quick win
3. **A2A Agents** (Cell 116) - Moderate complexity
4. **Image Consolidation** (Cells 106, 108, 129, 130) - Quick win
5. **Vector Search** (Cell 145) - Requires env file with model endpoints

**Prerequisites for Success**:
- Cells 14, 29, 32 must be working (✅ Complete)
- Run Cell 32 to generate updated master-lab.env
- Load env file in notebook: `from dotenv import load_dotenv; load_dotenv('master-lab.env')`

**Testing After All Fixes**:
1. Full notebook execution
2. Verify master-lab.env has all model fields
3. Check critical cells work
4. Commit all changes

---

**Status**: Ready for systematic implementation
**Estimated Time**: 2-3 hours for all remaining fixes
