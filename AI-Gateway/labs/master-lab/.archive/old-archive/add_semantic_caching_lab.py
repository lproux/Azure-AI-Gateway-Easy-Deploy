#!/usr/bin/env python3
"""
Add Semantic Caching Lab to master-ai-gateway-fix-MCP-clean.ipynb
Inserts new lab between Lab 08 (Model Routing) and Lab 09 (AI Foundry SDK)
"""
import json
import sys
from pathlib import Path

def find_lab_positions(cells):
    """Find the positions of Lab 08 and Lab 09"""
    lab08_end = None
    lab09_start = None

    for i, cell in enumerate(cells):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if 'Lab 08: Model Routing' in source and '##' in source:
                # Look ahead for the next markdown cell after Lab 08
                for j in range(i+1, len(cells)):
                    if cells[j].get('cell_type') == 'markdown':
                        next_source = ''.join(cells[j].get('source', []))
                        if 'Lab 09' in next_source or 'Lab 10' in next_source:
                            lab08_end = j
                            lab09_start = j
                            break
                break

    return lab08_end, lab09_start

def create_semantic_caching_cells():
    """Create all cells for the semantic caching lab"""

    # Cell 1: Lab Header
    header_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "<a id='lab09'></a>\n",
            "## Lab 09: Semantic Caching\n",
            "\n",
            "**Objective**: Demonstrate APIM's semantic caching capability using vector proximity to cache similar prompts.\n",
            "\n",
            "### What is Semantic Caching?\n",
            "\n",
            "The `azure-openai-semantic-cache-lookup` policy conducts a cache lookup of responses on Azure OpenAI Chat Completion API requests from a pre-configured external cache (Redis). It operates by:\n",
            "\n",
            "1. **Vector Proximity**: Comparing the vector proximity of the prompt to prior requests\n",
            "2. **Similarity Threshold**: Using a specific similarity score threshold (0.8 by default)\n",
            "3. **Cost Reduction**: Reducing bandwidth and processing demands on the backend Azure OpenAI API\n",
            "4. **Latency Improvement**: Reducing latency perceived by API consumers\n",
            "\n",
            "### Architecture\n",
            "\n",
            "```\n",
            "Client Request → APIM Gateway\n",
            "                    ↓\n",
            "                [Semantic Cache Lookup]\n",
            "                    ↓\n",
            "            Cache Hit? ────→ YES → Return Cached Response (fast)\n",
            "                    ↓\n",
            "                   NO\n",
            "                    ↓\n",
            "            [Call Azure OpenAI] → Get Response\n",
            "                    ↓\n",
            "            [Store in Cache with TTL]\n",
            "                    ↓\n",
            "            Return Response to Client\n",
            "```\n",
            "\n",
            "### Resources Used (Already Deployed)\n",
            "\n",
            "✅ **Redis Cache**: For storing embeddings\n",
            "- Host: `{REDIS_HOST}`\n",
            "- Port: `{REDIS_PORT}`\n",
            "\n",
            "✅ **Embedding Model**: `text-embedding-3-small`\n",
            "- Region 1 (UK South)\n",
            "\n",
            "✅ **APIM Service**: API Management gateway\n",
            "\n",
            "✅ **GPT-4o-mini**: For testing\n",
            "\n",
            "---"
        ]
    }

    # Cell 2: Configure Embeddings Backend
    backend_cell = {
        "cell_type": "code",
        "metadata": {},
        "outputs": [],
        "source": [
            "# Lab 09: Semantic Caching - Step 1: Configure Embeddings Backend\n",
            "\n",
            "# Load environment from master-lab.env\n",
            "import os\n",
            "from pathlib import Path\n",
            "from dotenv import load_dotenv\n",
            "\n",
            "env_file = Path('master-lab.env')\n",
            "if env_file.exists():\n",
            "    load_dotenv(env_file)\n",
            "    print(f\"[config] Loaded: {env_file.absolute()}\")\n",
            "else:\n",
            "    print(\"[warn] master-lab.env not found - run Cell 021 first\")\n",
            "\n",
            "# Get required variables\n",
            "apim_service_name = os.environ.get('APIM_SERVICE_NAME')\n",
            "resource_group = os.environ.get('RESOURCE_GROUP')\n",
            "subscription_id = os.environ.get('SUBSCRIPTION_ID')\n",
            "embedding_endpoint_r1 = os.environ.get('MODEL_TEXT_EMBEDDING_3_SMALL_ENDPOINT_R1')\n",
            "\n",
            "if not all([apim_service_name, resource_group, embedding_endpoint_r1]):\n",
            "    print(\"[ERROR] Missing required environment variables\")\n",
            "    print(f\"APIM_SERVICE_NAME: {apim_service_name}\")\n",
            "    print(f\"RESOURCE_GROUP: {resource_group}\")\n",
            "    print(f\"Embedding Endpoint: {embedding_endpoint_r1}\")\n",
            "else:\n",
            "    print(\"\\n[*] Step 1: Creating Embeddings Backend in APIM...\")\n",
            "    print(f\"    APIM Service: {apim_service_name}\")\n",
            "    print(f\"    Embedding Model: text-embedding-3-small\")\n",
            "    print(f\"    Endpoint: {embedding_endpoint_r1}\")\n",
            "    \n",
            "    # Backend configuration\n",
            "    backend_id = \"embeddings-backend\"\n",
            "    backend_url = f\"{embedding_endpoint_r1.rstrip('/')}openai/deployments/text-embedding-3-small/embeddings\"\n",
            "    \n",
            "    import subprocess\n",
            "    import json\n",
            "    \n",
            "    # Check if backend already exists\n",
            "    check_cmd = f\"az apim api versionset list --service-name {apim_service_name} --resource-group {resource_group} || true\"\n",
            "    \n",
            "    # Create or update the embeddings backend\n",
            "    backend_config = {\n",
            "        \"url\": backend_url,\n",
            "        \"protocol\": \"http\",\n",
            "        \"description\": \"Text Embedding Backend for Semantic Caching\",\n",
            "        \"credentials\": {\n",
            "            \"header\": {}\n",
            "        }\n",
            "    }\n",
            "    \n",
            "    # Write backend config to temp file\n",
            "    backend_file = Path('backend-embeddings.json')\n",
            "    with open(backend_file, 'w') as f:\n",
            "        json.dump(backend_config, f, indent=2)\n",
            "    \n",
            "    # Create backend using Azure CLI\n",
            "    cmd = f\"\"\"az apim backend create \\\\\n",
            "        --service-name {apim_service_name} \\\\\n",
            "        --resource-group {resource_group} \\\\\n",
            "        --backend-id {backend_id} \\\\\n",
            "        --url '{backend_url}' \\\\\n",
            "        --protocol http \\\\\n",
            "        --description 'Embeddings Backend for Semantic Caching' \\\\\n",
            "        || az apim backend update \\\\\n",
            "        --service-name {apim_service_name} \\\\\n",
            "        --resource-group {resource_group} \\\\\n",
            "        --backend-id {backend_id} \\\\\n",
            "        --url '{backend_url}' \\\\\n",
            "        --protocol http \\\\\n",
            "        --description 'Embeddings Backend for Semantic Caching'\n",
            "    \"\"\"\n",
            "    \n",
            "    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)\n",
            "    \n",
            "    if result.returncode == 0 or \"already exists\" in result.stderr.lower():\n",
            "        print(f\"\\n✅ Embeddings backend '{backend_id}' configured successfully!\")\n",
            "        print(f\"   URL: {backend_url}\")\n",
            "        print(f\"\\n[OK] Step 1 Complete - Embeddings backend ready\")\n",
            "    else:\n",
            "        print(f\"\\n❌ Failed to create embeddings backend\")\n",
            "        print(f\"   Error: {result.stderr}\")\n",
            "        print(f\"   Command: {cmd}\")\n"
        ]
    }

    # Cell 3: Apply Semantic Caching Policy
    policy_cell = {
        "cell_type": "code",
        "metadata": {},
        "outputs": [],
        "source": [
            "# Lab 09: Semantic Caching - Step 2: Apply Semantic Caching Policy\n",
            "\n",
            "import os\n",
            "from pathlib import Path\n",
            "from dotenv import load_dotenv\n",
            "\n",
            "env_file = Path('master-lab.env')\n",
            "if env_file.exists():\n",
            "    load_dotenv(env_file)\n",
            "\n",
            "# Get required variables\n",
            "apim_service_name = os.environ.get('APIM_SERVICE_NAME')\n",
            "resource_group = os.environ.get('RESOURCE_GROUP')\n",
            "api_id = os.environ.get('APIM_API_ID', 'inference-api')\n",
            "\n",
            "print(\"\\n[*] Step 2: Applying Semantic Caching Policy...\")\n",
            "print(f\"    API ID: {api_id}\")\n",
            "print(f\"    Cache Duration: 120 seconds\")\n",
            "print(f\"    Similarity Threshold: 0.8\")\n",
            "\n",
            "# Semantic caching policy XML\n",
            "policy_xml = \"\"\"<policies>\n",
            "    <inbound>\n",
            "        <base />\n",
            "        <!-- Semantic Cache Lookup: Check Redis for similar prompts (score >= 0.8) -->\n",
            "        <azure-openai-semantic-cache-lookup \n",
            "            score-threshold=\"0.8\" \n",
            "            embeddings-backend-id=\"embeddings-backend\" \n",
            "            embeddings-backend-auth=\"system-assigned\" />\n",
            "    </inbound>\n",
            "    <backend>\n",
            "        <base />\n",
            "    </backend>\n",
            "    <outbound>\n",
            "        <!-- Cache the response in Redis for 2 minutes -->\n",
            "        <azure-openai-semantic-cache-store duration=\"120\" />\n",
            "        <base />\n",
            "    </outbound>\n",
            "    <on-error>\n",
            "        <base />\n",
            "    </on-error>\n",
            "</policies>\"\"\"\n",
            "\n",
            "# Write policy to file\n",
            "policy_file = Path('semantic-caching-policy.xml')\n",
            "with open(policy_file, 'w') as f:\n",
            "    f.write(policy_xml)\n",
            "\n",
            "print(f\"\\n[*] Policy file created: {policy_file.absolute()}\")\n",
            "\n",
            "# Apply policy using Azure CLI\n",
            "import subprocess\n",
            "\n",
            "cmd = f\"\"\"az apim api policy create \\\\\n",
            "    --service-name {apim_service_name} \\\\\n",
            "    --resource-group {resource_group} \\\\\n",
            "    --api-id {api_id} \\\\\n",
            "    --policy-xml \"$(cat {policy_file})\" \\\\\n",
            "    || az apim api policy update \\\\\n",
            "    --service-name {apim_service_name} \\\\\n",
            "    --resource-group {resource_group} \\\\\n",
            "    --api-id {api_id} \\\\\n",
            "    --policy-xml \"$(cat {policy_file})\"\n",
            "\"\"\"\n",
            "\n",
            "print(f\"\\n[*] Applying policy to API '{api_id}'...\")\n",
            "result = subprocess.run(cmd, shell=True, capture_output=True, text=True)\n",
            "\n",
            "if result.returncode == 0:\n",
            "    print(f\"\\n✅ Semantic caching policy applied successfully!\")\n",
            "    print(f\"\\n📋 Policy Details:\")\n",
            "    print(f\"   - Lookup: Checks Redis for similar prompts (score >= 0.8)\")\n",
            "    print(f\"   - Store: Caches responses for 2 minutes\")\n",
            "    print(f\"   - Backend: embeddings-backend (text-embedding-3-small)\")\n",
            "    print(f\"\\n⏳ Wait 30-60 seconds for policy propagation...\")\n",
            "    print(f\"\\n[OK] Step 2 Complete - Semantic caching policy active\")\n",
            "else:\n",
            "    print(f\"\\n❌ Failed to apply policy\")\n",
            "    print(f\"   Error: {result.stderr}\")\n"
        ]
    }

    # Cell 4: Test Semantic Caching
    test_cell = {
        "cell_type": "code",
        "metadata": {},
        "outputs": [],
        "source": [
            "# Lab 09: Semantic Caching - Step 3: Test Semantic Caching Performance\n",
            "\n",
            "import os\n",
            "from pathlib import Path\n",
            "from dotenv import load_dotenv\n",
            "\n",
            "env_file = Path('master-lab.env')\n",
            "if env_file.exists():\n",
            "    load_dotenv(env_file)\n",
            "\n",
            "from openai import AzureOpenAI\n",
            "import time\n",
            "import random\n",
            "\n",
            "# Get configuration\n",
            "apim_gateway_url = os.environ.get('APIM_GATEWAY_URL')\n",
            "apim_api_key = os.environ.get('APIM_API_KEY')\n",
            "inference_api_path = os.environ.get('INFERENCE_API_PATH', 'inference')\n",
            "\n",
            "print(\"\\n[*] Step 3: Testing Semantic Caching Performance...\")\n",
            "print(f\"    Endpoint: {apim_gateway_url}/{inference_api_path}\")\n",
            "print(f\"    Model: gpt-4o-mini\")\n",
            "print(f\"    Runs: 20\")\n",
            "\n",
            "# Similar questions that should trigger semantic cache hits\n",
            "questions = [\n",
            "    \"How to Brew the Perfect Cup of Coffee?\",\n",
            "    \"What are the steps to Craft the Ideal Espresso?\",\n",
            "    \"Tell me how to create the best steaming Java?\",\n",
            "    \"Explain how to make a caffeinated brewed beverage?\"\n",
            "]\n",
            "\n",
            "# Initialize client\n",
            "client = AzureOpenAI(\n",
            "    azure_endpoint=f\"{apim_gateway_url}/{inference_api_path}\",\n",
            "    api_key=\"dummy\",  # Not used - key goes in header\n",
            "    api_version=\"2024-08-01-preview\"\n",
            ")\n",
            "\n",
            "runs = 20\n",
            "sleep_time_ms = 100  # 100ms between requests\n",
            "api_runs = []  # Response times\n",
            "\n",
            "print(f\"\\n{'='*80}\")\n",
            "print(\"🧪 SEMANTIC CACHING TEST\")\n",
            "print(f\"{'='*80}\")\n",
            "\n",
            "for i in range(runs):\n",
            "    random_question = random.choice(questions)\n",
            "    print(f\"\\n▶️  Run {i+1}/{runs}: {random_question[:50]}...\")\n",
            "    \n",
            "    start_time = time.time()\n",
            "    try:\n",
            "        response = client.chat.completions.create(\n",
            "            model=\"gpt-4o-mini\",\n",
            "            messages=[\n",
            "                {\"role\": \"system\", \"content\": \"You are a helpful coffee expert.\"},\n",
            "                {\"role\": \"user\", \"content\": random_question}\n",
            "            ],\n",
            "            max_tokens=100,\n",
            "            extra_headers={'api-key': apim_api_key}\n",
            "        )\n",
            "        response_time = time.time() - start_time\n",
            "        \n",
            "        # Determine if this was likely a cache hit (< 0.5 seconds is very fast)\n",
            "        cache_status = \"🎯 CACHE HIT\" if response_time < 0.5 else \"🔥 BACKEND CALL\"\n",
            "        print(f\"   ⏱️  {response_time:.3f}s - {cache_status}\")\n",
            "        \n",
            "        api_runs.append(response_time)\n",
            "        \n",
            "    except Exception as e:\n",
            "        print(f\"   ❌ Error: {str(e)[:100]}\")\n",
            "        api_runs.append(None)\n",
            "    \n",
            "    time.sleep(sleep_time_ms / 1000)\n",
            "\n",
            "# Calculate statistics\n",
            "valid_runs = [r for r in api_runs if r is not None]\n",
            "if valid_runs:\n",
            "    avg_time = sum(valid_runs) / len(valid_runs)\n",
            "    min_time = min(valid_runs)\n",
            "    max_time = max(valid_runs)\n",
            "    cache_hits = sum(1 for r in valid_runs if r < 0.5)\n",
            "    \n",
            "    print(f\"\\n{'='*80}\")\n",
            "    print(\"📊 PERFORMANCE SUMMARY\")\n",
            "    print(f\"{'='*80}\")\n",
            "    print(f\"Total Requests:     {len(api_runs)}\")\n",
            "    print(f\"Successful:         {len(valid_runs)}\")\n",
            "    print(f\"Average Time:       {avg_time:.3f}s\")\n",
            "    print(f\"Fastest Response:   {min_time:.3f}s\")\n",
            "    print(f\"Slowest Response:   {max_time:.3f}s\")\n",
            "    print(f\"Likely Cache Hits:  {cache_hits}/{len(valid_runs)} ({cache_hits/len(valid_runs)*100:.1f}%)\")\n",
            "    print(f\"{'='*80}\")\n",
            "    \n",
            "    # First request should be slow (backend call)\n",
            "    # Subsequent similar requests should be fast (cache hits)\n",
            "    if len(valid_runs) > 1 and valid_runs[0] > 1.0 and valid_runs[1] < 0.5:\n",
            "        print(\"\\n✅ Semantic caching is working!\")\n",
            "        print(f\"   First request: {valid_runs[0]:.3f}s (backend call)\")\n",
            "        print(f\"   Second request: {valid_runs[1]:.3f}s (cache hit)\")\n",
            "        print(f\"   Speed improvement: {(valid_runs[0]/valid_runs[1]):.1f}x faster!\")\n",
            "    else:\n",
            "        print(\"\\n⚠️  Results may vary. First request should be slow, subsequent similar requests fast.\")\n",
            "else:\n",
            "    print(\"\\n❌ No successful requests completed\")\n",
            "\n",
            "print(\"\\n[OK] Step 3 Complete - Semantic caching test finished\")\n",
            "\n",
            "# Store results for visualization\n",
            "semantic_cache_results = api_runs\n"
        ]
    }

    # Cell 5: Visualize Results
    viz_cell = {
        "cell_type": "code",
        "metadata": {},
        "outputs": [],
        "source": [
            "# Lab 09: Semantic Caching - Step 4: Visualize Performance\n",
            "\n",
            "import pandas as pd\n",
            "import matplotlib.pyplot as plt\n",
            "import matplotlib as mpl\n",
            "\n",
            "print(\"\\n[*] Step 4: Visualizing Semantic Caching Performance...\")\n",
            "\n",
            "if 'semantic_cache_results' in globals() and semantic_cache_results:\n",
            "    # Filter out None values\n",
            "    valid_results = [r for r in semantic_cache_results if r is not None]\n",
            "    \n",
            "    if len(valid_results) > 0:\n",
            "        # Create DataFrame\n",
            "        mpl.rcParams['figure.figsize'] = [15, 5]\n",
            "        df = pd.DataFrame(valid_results, columns=['Response Time (s)'])\n",
            "        df['Run'] = range(1, len(df) + 1)\n",
            "        \n",
            "        # Create bar plot\n",
            "        ax = df.plot(kind='bar', x='Run', y='Response Time (s)', legend=False, color='steelblue')\n",
            "        plt.title('Semantic Caching Performance - Response Times', fontsize=14, fontweight='bold')\n",
            "        plt.xlabel('Run Number', fontsize=12)\n",
            "        plt.ylabel('Response Time (seconds)', fontsize=12)\n",
            "        plt.xticks(rotation=0)\n",
            "        \n",
            "        # Add average line\n",
            "        average = df['Response Time (s)'].mean()\n",
            "        plt.axhline(y=average, color='red', linestyle='--', linewidth=2, label=f'Average: {average:.2f}s')\n",
            "        \n",
            "        # Add cache hit threshold line\n",
            "        plt.axhline(y=0.5, color='green', linestyle=':', linewidth=2, label='Cache Hit Threshold (0.5s)')\n",
            "        \n",
            "        # Highlight first request (typically slowest)\n",
            "        if len(valid_results) > 0:\n",
            "            ax.patches[0].set_facecolor('orange')\n",
            "        \n",
            "        plt.legend(loc='upper right', fontsize=10)\n",
            "        plt.grid(axis='y', alpha=0.3)\n",
            "        plt.tight_layout()\n",
            "        \n",
            "        print(\"\\n📊 Chart Legend:\")\n",
            "        print(\"   🟠 Orange bar = First request (backend call, no cache)\")\n",
            "        print(\"   🔵 Blue bars = Subsequent requests\")\n",
            "        print(\"   🔴 Red dashed line = Average response time\")\n",
            "        print(\"   🟢 Green dotted line = Cache hit threshold (0.5s)\")\n",
            "        print(\"   Bars below green line = Likely cache hits\")\n",
            "        \n",
            "        plt.show()\n",
            "        \n",
            "        # Additional insights\n",
            "        cache_hits = sum(1 for r in valid_results if r < 0.5)\n",
            "        if cache_hits > len(valid_results) * 0.7:  # If >70% cache hits\n",
            "            print(\"\\n✅ Excellent cache hit rate! Semantic caching is highly effective.\")\n",
            "        elif cache_hits > len(valid_results) * 0.5:  # If >50% cache hits\n",
            "            print(\"\\n✅ Good cache hit rate. Semantic caching is working well.\")\n",
            "        else:\n",
            "            print(\"\\n⚠️  Lower cache hit rate. This could be due to:\")\n",
            "            print(\"   - Questions being too different (similarity < 0.8)\")\n",
            "            print(\"   - Cache TTL expired (120 seconds)\")\n",
            "            print(\"   - Redis cache capacity limits\")\n",
            "        \n",
            "        print(\"\\n[OK] Step 4 Complete - Visualization ready\")\n",
            "    else:\n",
            "        print(\"\\n⚠️  No valid results to visualize\")\n",
            "else:\n",
            "    print(\"\\n⚠️  No results available. Run the test cell (Step 3) first.\")\n",
            "\n",
            "print(\"\\n\" + \"=\"*80)\n",
            "print(\"🎉 LAB 09 COMPLETE: SEMANTIC CACHING\")\n",
            "print(\"=\"*80)\n",
            "print(\"\\nWhat you learned:\")\n",
            "print(\"✅ How to configure embeddings backend in APIM\")\n",
            "print(\"✅ How to apply semantic caching policy\")\n",
            "print(\"✅ How semantic similarity reduces API calls\")\n",
            "print(\"✅ How to measure caching performance\")\n",
            "print(\"\\nKey Benefits:\")\n",
            "print(\"💰 Cost savings: Reduced Azure OpenAI API calls\")\n",
            "print(\"⚡ Performance: Faster response times for similar queries\")\n",
            "print(\"📊 Scalability: Better handling of repetitive queries\")\n"
        ]
    }

    # Cell 6: Cleanup/Reset (Optional)
    cleanup_cell = {
        "cell_type": "code",
        "metadata": {},
        "outputs": [],
        "source": [
            "# Lab 09: Semantic Caching - Optional: Reset to Standard Policy\n",
            "\n",
            "import os\n",
            "from pathlib import Path\n",
            "from dotenv import load_dotenv\n",
            "\n",
            "env_file = Path('master-lab.env')\n",
            "if env_file.exists():\n",
            "    load_dotenv(env_file)\n",
            "\n",
            "apim_service_name = os.environ.get('APIM_SERVICE_NAME')\n",
            "resource_group = os.environ.get('RESOURCE_GROUP')\n",
            "api_id = os.environ.get('APIM_API_ID', 'inference-api')\n",
            "\n",
            "print(\"\\n[*] Resetting API to standard policy (removing semantic caching)...\")\n",
            "print(\"    This will restore the API to API Key authentication only.\")\n",
            "\n",
            "# Standard policy without semantic caching\n",
            "standard_policy = \"\"\"<policies>\n",
            "    <inbound>\n",
            "        <base />\n",
            "        <authentication-managed-identity resource=\"https://cognitiveservices.azure.com\" />\n",
            "    </inbound>\n",
            "    <backend>\n",
            "        <base />\n",
            "    </backend>\n",
            "    <outbound>\n",
            "        <base />\n",
            "    </outbound>\n",
            "    <on-error>\n",
            "        <base />\n",
            "    </on-error>\n",
            "</policies>\"\"\"\n",
            "\n",
            "# Write standard policy to file\n",
            "standard_policy_file = Path('standard-policy.xml')\n",
            "with open(standard_policy_file, 'w') as f:\n",
            "    f.write(standard_policy)\n",
            "\n",
            "import subprocess\n",
            "\n",
            "cmd = f\"\"\"az apim api policy update \\\\\n",
            "    --service-name {apim_service_name} \\\\\n",
            "    --resource-group {resource_group} \\\\\n",
            "    --api-id {api_id} \\\\\n",
            "    --policy-xml \"$(cat {standard_policy_file})\"\n",
            "\"\"\"\n",
            "\n",
            "result = subprocess.run(cmd, shell=True, capture_output=True, text=True)\n",
            "\n",
            "if result.returncode == 0:\n",
            "    print(\"\\n✅ Policy reset to standard (no semantic caching)\")\n",
            "    print(\"   You can re-apply semantic caching anytime by running Step 2 again.\")\n",
            "else:\n",
            "    print(f\"\\n❌ Failed to reset policy\")\n",
            "    print(f\"   Error: {result.stderr}\")\n"
        ]
    }

    return [header_cell, backend_cell, policy_cell, test_cell, viz_cell, cleanup_cell]

def main():
    notebook_path = Path('master-ai-gateway-fix-MCP-clean.ipynb')

    if not notebook_path.exists():
        print(f"ERROR: Notebook not found: {notebook_path}")
        return 1

    print(f"Reading notebook: {notebook_path}")

    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    cells = notebook.get('cells', [])
    print(f"Total cells in notebook: {len(cells)}")

    # Find insertion point
    lab08_end, lab09_start = find_lab_positions(cells)

    if lab08_end is None:
        print("ERROR: Could not find Lab 08 end position")
        return 1

    print(f"Found Lab 08 end at cell index: {lab08_end}")
    print(f"Will insert Semantic Caching Lab at position: {lab08_end}")

    # Create new cells
    new_cells = create_semantic_caching_cells()
    print(f"Created {len(new_cells)} new cells for Semantic Caching Lab")

    # Insert new cells
    notebook['cells'] = cells[:lab08_end] + new_cells + cells[lab08_end:]

    print(f"New total cells: {len(notebook['cells'])}")

    # Backup original
    backup_path = notebook_path.with_suffix('.ipynb.backup-before-semantic-caching')
    print(f"Creating backup: {backup_path}")

    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(json.load(open(notebook_path, 'r', encoding='utf-8')), f, indent=2)

    # Write updated notebook
    print(f"Writing updated notebook: {notebook_path}")

    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)

    print("\\n" + "="*80)
    print("✅ SUCCESS: Semantic Caching Lab added to notebook!")
    print("="*80)
    print(f"\\nNew lab inserted between Lab 08 and Lab 09 (now Lab 10)")
    print(f"Total cells added: {len(new_cells)}")
    print(f"\\nBackup created: {backup_path}")
    print(f"\\nNew lab structure:")
    print(f"  - Lab 08: Model Routing")
    print(f"  - Lab 09: Semantic Caching (NEW)")
    print(f"  - Lab 10: AI Foundry SDK (previously Lab 09)")
    print(f"  - Lab 11: AI Foundry DeepSeek (previously Lab 10)")

    return 0

if __name__ == '__main__':
    sys.exit(main())
