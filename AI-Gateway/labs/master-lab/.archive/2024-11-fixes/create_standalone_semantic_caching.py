#!/usr/bin/env python3
"""
Create standalone semantic-caching notebook using master-lab resources
Based on the WORKING semantic-caching.ipynb structure
"""
import json
from pathlib import Path

print("Creating standalone semantic-caching notebook...")

# Create notebook structure
notebook = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.12.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

# Cell 0: Title
notebook["cells"].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# Semantic Caching Lab - Standalone\n",
        "\n",
        "**Using master-lab resources**\n",
        "\n",
        "This notebook demonstrates Azure API Management semantic caching using the proven working approach.\n",
        "\n",
        "## How it Works\n",
        "\n",
        "1. **Request arrives** at APIM\n",
        "2. **APIM creates embedding** of the prompt using text-embedding-3-small\n",
        "3. **Checks Redis cache** for similar embeddings (>80% match)\n",
        "4. **If match found**: Returns cached response (~0.1-0.3s)\n",
        "5. **If no match**: Calls Azure OpenAI, stores in cache (~3-10s)\n",
        "\n",
        "## Expected Results\n",
        "\n",
        "- First similar request: Slow (~3-10s)\n",
        "- Subsequent similar requests: **15-100x faster!** (~0.1-0.3s)\n",
        "- Cache TTL: 20 minutes\n",
        "\n",
        "---"
    ]
})

# Cell 1: Setup and Imports
notebook["cells"].append({
    "cell_type": "code",
    "metadata": {},
    "execution_count": None,
    "outputs": [],
    "source": [
        "# Cell 1: Setup and Imports\n",
        "import os\n",
        "from pathlib import Path\n",
        "from dotenv import load_dotenv\n",
        "from openai import AzureOpenAI\n",
        "import time\n",
        "import random\n",
        "\n",
        "# Load master-lab environment\n",
        "env_file = Path('master-lab.env')\n",
        "if env_file.exists():\n",
        "    load_dotenv(env_file)\n",
        "    print(\"✅ Loaded master-lab.env\")\n",
        "else:\n",
        "    print(\"❌ master-lab.env not found!\")\n",
        "\n",
        "# Get configuration\n",
        "apim_gateway_url = os.environ.get('APIM_GATEWAY_URL')\n",
        "apim_api_key = os.environ.get('APIM_API_KEY')\n",
        "inference_api_path = os.environ.get('INFERENCE_API_PATH', 'inference')\n",
        "\n",
        "print(f\"\\nEndpoint: {apim_gateway_url}/{inference_api_path}\")\n",
        "print(f\"API Key: ****{apim_api_key[-4:]}\")\n",
        "print(\"\\n✅ Setup complete\")"
    ]
})

# Cell 2: Test Semantic Caching
notebook["cells"].append({
    "cell_type": "code",
    "metadata": {},
    "execution_count": None,
    "outputs": [],
    "source": [
        "# Cell 2: Test Semantic Caching with 20 Similar Questions\n",
        "\n",
        "# These questions are semantically similar (>80% match)\n",
        "# So they should all return cached responses after the first one\n",
        "questions = [\n",
        "    \"How to Brew the Perfect Cup of Coffee?\",\n",
        "    \"What are the steps to Craft the Ideal Espresso?\",\n",
        "    \"Tell me how to create the best steaming Java?\",\n",
        "    \"Explain how to make a caffeinated brewed beverage?\"\n",
        "]\n",
        "\n",
        "# Initialize OpenAI client\n",
        "client = AzureOpenAI(\n",
        "    azure_endpoint=f\"{apim_gateway_url}/{inference_api_path}\",\n",
        "    api_key=apim_api_key,\n",
        "    api_version=\"2025-03-01-preview\"\n",
        ")\n",
        "\n",
        "runs = 20\n",
        "sleep_time_ms = 10  # 10ms between requests\n",
        "api_runs = []  # Response times\n",
        "\n",
        "print(\"=\" * 80)\n",
        "print(\"🧪 SEMANTIC CACHING TEST\")\n",
        "print(\"=\" * 80)\n",
        "print(f\"\\nMaking {runs} requests with similar questions...\")\n",
        "print(\"Expected: First request slow, subsequent requests FAST\\n\")\n",
        "\n",
        "for i in range(runs):\n",
        "    random_question = random.choice(questions)\n",
        "    print(f\"\\n▶️ Run {i+1}/{runs}:\")\n",
        "    print(f\"💬  {random_question}\")\n",
        "\n",
        "    start_time = time.time()\n",
        "    try:\n",
        "        response = client.chat.completions.create(\n",
        "            model=\"gpt-4o-mini\",\n",
        "            messages=[\n",
        "                {\"role\": \"system\", \"content\": \"You are a sarcastic, unhelpful assistant.\"},\n",
        "                {\"role\": \"user\", \"content\": random_question}\n",
        "            ]\n",
        "        )\n",
        "        response_time = time.time() - start_time\n",
        "\n",
        "        status = \"🎯 CACHE HIT\" if response_time < 1.0 else \"🔥 BACKEND CALL\"\n",
        "        print(f\"⌚ {response_time:.2f} seconds - {status}\")\n",
        "\n",
        "        # Uncomment to see responses:\n",
        "        # print(f\"💬 {response.choices[0].message.content}\\n\")\n",
        "\n",
        "        api_runs.append(response_time)\n",
        "\n",
        "    except Exception as e:\n",
        "        print(f\"❌ Error: {str(e)[:150]}\")\n",
        "        api_runs.append(None)\n",
        "\n",
        "    time.sleep(sleep_time_ms / 1000)\n",
        "\n",
        "# Calculate statistics\n",
        "valid_runs = [r for r in api_runs if r is not None]\n",
        "\n",
        "if valid_runs:\n",
        "    avg_time = sum(valid_runs) / len(valid_runs)\n",
        "    min_time = min(valid_runs)\n",
        "    max_time = max(valid_runs)\n",
        "    cache_hits = sum(1 for r in valid_runs if r < 1.0)\n",
        "\n",
        "    print(f\"\\n{'='*80}\")\n",
        "    print(\"📊 PERFORMANCE SUMMARY\")\n",
        "    print(f\"{'='*80}\")\n",
        "    print(f\"Total Requests:     {len(api_runs)}\")\n",
        "    print(f\"Successful:         {len(valid_runs)}\")\n",
        "    print(f\"Average Time:       {avg_time:.2f}s\")\n",
        "    print(f\"Fastest Response:   {min_time:.2f}s\")\n",
        "    print(f\"Slowest Response:   {max_time:.2f}s\")\n",
        "    print(f\"Likely Cache Hits:  {cache_hits}/{len(valid_runs)} ({cache_hits/len(valid_runs)*100:.1f}%)\")\n",
        "    print(f\"{'='*80}\")\n",
        "\n",
        "    if max_time > 1.0 and min_time < 1.0:\n",
        "        speedup = max_time / min_time\n",
        "        print(f\"\\n✅ SEMANTIC CACHING IS WORKING!\")\n",
        "        print(f\"   Slowest request: {max_time:.2f}s (backend call)\")\n",
        "        print(f\"   Fastest request: {min_time:.2f}s (cache hit)\")\n",
        "        print(f\"   Speed improvement: {speedup:.1f}x faster!\")\n",
        "    else:\n",
        "        print(f\"\\n⚠️  Results may vary. Expected: first request slow, subsequent fast.\")\n",
        "else:\n",
        "    print(\"\\n❌ No successful requests\")\n",
        "\n",
        "print(\"\\n✅ Test complete - See visualization next\")"
    ]
})

# Cell 3: Visualization
notebook["cells"].append({
    "cell_type": "code",
    "metadata": {},
    "execution_count": None,
    "outputs": [],
    "source": [
        "# Cell 3: Visualize Semantic Caching Performance\n",
        "\n",
        "import pandas as pd\n",
        "import matplotlib.pyplot as plt\n",
        "import matplotlib as mpl\n",
        "\n",
        "if 'api_runs' in globals() and api_runs:\n",
        "    valid_results = [r for r in api_runs if r is not None]\n",
        "\n",
        "    if len(valid_results) > 0:\n",
        "        # Create DataFrame\n",
        "        mpl.rcParams['figure.figsize'] = [15, 5]\n",
        "        df = pd.DataFrame(valid_results, columns=['Response Time'])\n",
        "        df['Run'] = range(1, len(df) + 1)\n",
        "\n",
        "        # Create bar plot\n",
        "        ax = df.plot(kind='bar', x='Run', y='Response Time', legend=False, color='steelblue')\n",
        "        plt.title('Semantic Caching Performance', fontsize=14, fontweight='bold')\n",
        "        plt.xlabel('Runs', fontsize=12)\n",
        "        plt.ylabel('Response Time (s)', fontsize=12)\n",
        "        plt.xticks(rotation=0)\n",
        "\n",
        "        # Add average line\n",
        "        average = df['Response Time'].mean()\n",
        "        plt.axhline(y=average, color='r', linestyle='--', label=f'Average: {average:.2f}s')\n",
        "\n",
        "        # Add cache hit threshold line\n",
        "        plt.axhline(y=1.0, color='green', linestyle=':', linewidth=2, label='Cache Hit Threshold (1.0s)')\n",
        "\n",
        "        plt.legend(loc='upper right')\n",
        "        plt.grid(axis='y', alpha=0.3)\n",
        "        plt.tight_layout()\n",
        "        plt.show()\n",
        "\n",
        "        print(\"\\n📊 Chart Legend:\")\n",
        "        print(\"   🔵 Blue bars = Individual response times\")\n",
        "        print(\"   🔴 Red dashed line = Average response time\")\n",
        "        print(\"   🟢 Green dotted line = Cache hit threshold (1.0s)\")\n",
        "        print(\"   Bars below green line = Likely cache hits (fast!)\")\n",
        "        print(\"\\n✅ Visualization complete\")\n",
        "    else:\n",
        "        print(\"⚠️  No valid results to visualize\")\n",
        "else:\n",
        "    print(\"⚠️  Run Cell 2 first to generate test results\")"
    ]
})

# Cell 4: Redis Cache Statistics
notebook["cells"].append({
    "cell_type": "code",
    "metadata": {},
    "execution_count": None,
    "outputs": [],
    "source": [
        "# Cell 4: View Redis Cache Statistics (Optional)\n",
        "\n",
        "import redis.asyncio as redis\n",
        "import pandas as pd\n",
        "import matplotlib.pyplot as plt\n",
        "\n",
        "# Get Redis configuration from master-lab.env\n",
        "redis_host = os.environ.get('REDIS_HOST')\n",
        "redis_port = int(os.environ.get('REDIS_PORT', 10000))\n",
        "redis_key = os.environ.get('REDIS_KEY')\n",
        "\n",
        "async def get_redis_info():\n",
        "    r = await redis.from_url(\n",
        "        f\"rediss://:{redis_key}@{redis_host}:{redis_port}\"\n",
        "    )\n",
        "\n",
        "    info = await r.info()\n",
        "\n",
        "    print(\"📊 Redis Server Information:\")\n",
        "    print(f\"   Used Memory: {info['used_memory_human']}\")\n",
        "    print(f\"   Cache Hits: {info['keyspace_hits']}\")\n",
        "    print(f\"   Cache Misses: {info['keyspace_misses']}\")\n",
        "    print(f\"   Evicted Keys: {info['evicted_keys']}\")\n",
        "    print(f\"   Expired Keys: {info['expired_keys']}\")\n",
        "\n",
        "    # Calculate hit rate\n",
        "    total = info['keyspace_hits'] + info['keyspace_misses']\n",
        "    if total > 0:\n",
        "        hit_rate = (info['keyspace_hits'] / total) * 100\n",
        "        print(f\"   Hit Rate: {hit_rate:.1f}%\")\n",
        "\n",
        "    # Create visualization\n",
        "    redis_info = {\n",
        "        'Metric': ['Cache Hits', 'Cache Misses', 'Evicted Keys', 'Expired Keys'],\n",
        "        'Value': [info['keyspace_hits'], info['keyspace_misses'], info['evicted_keys'], info['expired_keys']]\n",
        "    }\n",
        "\n",
        "    df_redis_info = pd.DataFrame(redis_info)\n",
        "    df_redis_info.plot(kind='barh', x='Metric', y='Value', legend=False, color='teal')\n",
        "\n",
        "    plt.title('Redis Cache Statistics')\n",
        "    plt.xlabel('Count')\n",
        "    plt.ylabel('Metric')\n",
        "    plt.tight_layout()\n",
        "    plt.show()\n",
        "\n",
        "    await r.aclose()\n",
        "    print(\"\\n✅ Redis statistics retrieved successfully\")\n",
        "\n",
        "try:\n",
        "    await get_redis_info()\n",
        "except Exception as e:\n",
        "    print(f\"⚠️  Could not connect to Redis: {str(e)[:100]}\")\n",
        "    print(\"   Make sure Redis is configured in master-lab.env\")"
    ]
})

# Cell 5: Summary
notebook["cells"].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# 🎉 Semantic Caching Lab Complete!\n",
        "\n",
        "## What You Learned\n",
        "\n",
        "✅ How semantic caching reduces API calls for similar queries  \n",
        "✅ How to measure caching performance  \n",
        "✅ How vector embeddings enable semantic similarity matching  \n",
        "\n",
        "## Key Benefits\n",
        "\n",
        "💰 **Cost savings**: Reduced Azure OpenAI API calls (up to 90% reduction!)  \n",
        "⚡ **Performance**: Faster response times (15-100x faster for cached requests)  \n",
        "📊 **Scalability**: Better handling of repetitive queries  \n",
        "\n",
        "## Configuration\n",
        "\n",
        "- **Similarity Threshold**: 0.8 (80% match required)\n",
        "- **Cache TTL**: 20 minutes (1200 seconds)\n",
        "- **Embeddings Model**: text-embedding-3-small\n",
        "- **Cache Storage**: Redis\n",
        "\n",
        "---\n",
        "\n",
        "**Next Steps**: Integrate semantic caching into your production APIs to reduce costs and improve performance!"
    ]
})

# Save notebook
output_path = Path('semantic-caching-standalone.ipynb')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f"✅ Created standalone semantic-caching notebook:")
print(f"   {output_path}")
print("\nNotebook structure:")
print("   Cell 0: Title and explanation")
print("   Cell 1: Setup and imports (loads master-lab.env)")
print("   Cell 2: Test semantic caching (20 requests)")
print("   Cell 3: Visualization (performance chart)")
print("   Cell 4: Redis statistics (optional)")
print("   Cell 5: Summary")
print("\n🎯 To use:")
print("   1. Open semantic-caching-standalone.ipynb in Jupyter")
print("   2. Select Python 3.12 kernel")
print("   3. Run Cell 1 to load master-lab.env")
print("   4. Run Cell 2 to test semantic caching")
print("   5. Run Cell 3 to see performance chart")
