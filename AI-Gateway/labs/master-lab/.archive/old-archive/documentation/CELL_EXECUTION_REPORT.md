# 📊 Notebook Cell Execution Report

**Generated**: 2025-10-28 02:25:34
**Notebook**: master-ai-gateway.ipynb
**Total Cells**: 808
**Code Cells**: 411

---

## 🎯 Summary

| Metric | Count | Percentage |
|--------|-------|------------|
| ✅ Successful | 387 | 94.2% |
| ❌ Failed | 24 | 5.8% |
| ⏭️ Skipped (Markdown) | 397 | N/A |

---

## 📈 Success Rate by Attempt

- **Attempt 1**: 91 cells
- **Attempt 5**: 296 cells

---

## ⚠️ Error Patterns Detected

- **NameError**: 1148 occurrences
- **SyntaxError**: 116 occurrences
- **ModuleNotFoundError**: 36 occurrences
- **IndentationError**: 4 occurrences

---

## 📋 Cell-by-Cell Results

### Cell 1 ✅

**Preview**: `# Cell 2: MCP Client Initialization (Updated for 2 Real Servers)import syssys.path.append('.')from n...`

**Status**: Success (Attempt 1/5)

### Cell 2 ✅

**Preview**: `# Cell 2: MCP Client Initialization (Updated for 3 Real Servers: Excel, Docs, Weather) import sys sy...`

**Status**: Success (Attempt 1/5)

### Cell 5 ✅

**Preview**: `# Environment / Dependencies Setup (run once) # Installs Python packages listed in the lab-specific ...`

**Status**: Success (Attempt 1/5)

### Cell 8 ✅

**Preview**: `import os, sys, json, time, asyncio, random, base64 import requests import pandas as pd import matpl...`

**Status**: Success (Attempt 5/5)

### Cell 10 ✅

**Preview**: `from dotenv import load_dotenv import os  # Load environment variables from deployment env_file = 'm...`

**Status**: Success (Attempt 1/5)

### Cell 11 ✅

**Preview**: `output = utils.run('az account show', 'Retrieved account', 'Failed') if output.success and output.js...`

**Status**: Success (Attempt 5/5)

### Cell 13 ✅

**Preview**: `import os import json import subprocess from datetime import datetime  # Check if already exists if ...`

**Status**: Success (Attempt 1/5)

### Cell 15 ✅

**Preview**: `# Master Lab Configuration  # IMPORTANT: Set your Azure subscription ID # Get this from: Azure Porta...`

**Status**: Success (Attempt 1/5)

### Cell 17 ✅

**Preview**: `import json import time import os import shutil from pathlib import Path from dotenv import load_dot...`

**Status**: Success (Attempt 5/5)

### Cell 19 ✅

**Preview**: `print('=' * 70) print('MASTER LAB DEPLOYMENT - 4 STEPS (RESILIENT)') print('=' * 70) print()  total_...`

**Status**: Success (Attempt 5/5)

### Cell 21 ✅

**Preview**: `import os from datetime import datetime  print('[*] Generating master-lab.env...')  # Ensure step2_o...`

**Status**: Success (Attempt 5/5)

### Cell 22 ✅

**Preview**: `# Unified Configuration Loader Cell """ Loads all required environment and configuration variables f...`

**Status**: Success (Attempt 1/5)

### Cell 25 ✅

**Preview**: `# Lab 01: Test 1 - Basic Chat Completion # This cell initializes the AzureOpenAI client and tests ba...`

**Status**: Success (Attempt 5/5)

### Cell 27 ✅

**Preview**: `# Lab 01: Test 2 - Streaming Response  print('[*] Testing streaming...') stream = client.chat.comple...`

**Status**: Success (Attempt 5/5)

### Cell 29 ✅

**Preview**: `for i in range(5):     response = client.chat.completions.create(         model='gpt-4o-mini',      ...`

**Status**: Success (Attempt 5/5)

### Cell 32 ✅

**Preview**: `print('Testing load balancing across 3 regions...') responses = [] for i in range(20):     start = t...`

**Status**: Success (Attempt 5/5)

### Cell 34 ✅

**Preview**: `df = pd.DataFrame({'Request': range(1, len(responses)+1), 'Time (s)': responses}) df.plot(kind='line...`

**Status**: Success (Attempt 5/5)

### Cell 36 ✅

**Preview**: `for i in range(10):     client.chat.completions.create(         model='gpt-4o-mini',         message...`

**Status**: Success (Attempt 5/5)

### Cell 38 ✅

**Preview**: `total_tokens = 0 for i in range(5):     response = client.chat.completions.create(         model='gp...`

**Status**: Success (Attempt 5/5)

### Cell 40 ✅

**Preview**: `print('Testing rate limiting...') for i in range(10):     try:         response = client.chat.comple...`

**Status**: Success (Attempt 5/5)

### Cell 42 ✅

**Preview**: `# Using API key for now (OAuth requires app registration) response = client.chat.completions.create(...`

**Status**: Success (Attempt 5/5)

### Cell 44 ✅

**Preview**: `# Test with safe content response = client.chat.completions.create(     model='gpt-4o-mini',     mes...`

**Status**: Success (Attempt 5/5)

### Cell 46 ✅

**Preview**: `models_to_test = ['gpt-4o-mini', 'gpt-4.1-mini'] for model in models_to_test:     response = client....`

**Status**: Success (Attempt 5/5)

### Cell 49 ✅

**Preview**: `# Lab 09: AI Foundry SDK - Chat Completion via APIM # CRITICAL: ChatCompletionsClient requires the F...`

**Status**: Success (Attempt 5/5)

### Cell 53 ❌

**Preview**: `!python3 test_mcp_servers.py`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `IndentationError` - unexpected indent (<string>, line 1)
- Attempt 2: `IndentationError` - unexpected indent (<string>, line 1)
- Attempt 3: `IndentationError` - unexpected indent (<string>, line 1)
- Attempt 4: `IndentationError` - unexpected indent (<string>, line 1)
- Attempt 5: `SyntaxError` - invalid syntax (<string>, line 2)

### Cell 55 ❌

**Preview**: `# Lab 10: MCP Server Integration - Enhanced Initialization # Based on working pattern from workshop ...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 233)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 233)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 233)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 233)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 234)

### Cell 56 ❌

**Preview**: `# Lab 10 Example: Product Catalog MCP Server # Demonstrates e-commerce product catalog access via MC...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 64)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 64)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 64)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 64)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 65)

### Cell 57 ❌

**Preview**: `# Lab 10 Example: Weather MCP Server # Demonstrates weather data retrieval via MCP  async def demo_w...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 57)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 57)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 57)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 57)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 58)

### Cell 58 ❌

**Preview**: `# Lab 10 Example: GitHub MCP Server # Demonstrates GitHub repository operations via MCP  async def d...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 40)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 40)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 40)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 40)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 41)

### Cell 59 ❌

**Preview**: `# Lab 10 Example: OnCall MCP Server # Demonstrates on-call schedule management via MCP  async def de...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 42)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 42)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 42)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 42)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 43)

### Cell 61 ❌

**Preview**: `# Lab 11: Spotify MCP Integration # Demonstrates music service integration via MCP  async def demo_s...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 40)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 40)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 40)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 40)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 41)

### Cell 63 ❌

**Preview**: `# Lab 12: Weather + AI Travel Advisor # Get weather data via MCP and use AI to provide recommendatio...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 45)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 45)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 45)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 45)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 46)

### Cell 65 ❌

**Preview**: `# Lab 13: OnCall Schedule Access # Query on-call schedules via MCP server  async def oncall_schedule...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 33)

### Cell 67 ❌

**Preview**: `# Lab 14: GitHub Repository Query # Access GitHub data via MCP server  async def github_repos():    ...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 33)

### Cell 69 ❌

**Preview**: `# Lab 15: GitHub + AI Code Analysis # Use GitHub MCP + AI to analyze code quality  async def github_...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 35)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 35)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 35)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 35)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 36)

### Cell 70 ✅

**Preview**: `# Lab 17: Additional GitHub/OnCall examples # (Reserved for future examples)`

**Status**: Success (Attempt 1/5)

### Cell 73 ❌

**Preview**: `# Lab 16: Spotify Music Search # Query music data via Spotify MCP server  async def spotify_search()...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 33)

### Cell 75 ❌

**Preview**: `# Lab 17: AI-Powered Music Recommendations # Combine Spotify data with AI for personalized recommend...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 35)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 35)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 35)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 35)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 36)

### Cell 77 ✅

**Preview**: `# Lab 24: Additional Spotify examples # (Reserved for future examples)`

**Status**: Success (Attempt 1/5)

### Cell 79 ❌

**Preview**: `# Lab 18: E-Commerce Product Catalog # Access product catalog via MCP server  async def product_cata...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 33)

### Cell 81 ❌

**Preview**: `# Lab 19: E-Commerce Order Placement # Place orders via MCP server  async def place_order():     if ...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 38)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 38)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 38)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 38)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 39)

### Cell 83 ❌

**Preview**: `# Lab 20: AI-Powered Shopping Assistant # Combine product catalog with AI for shopping recommendatio...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 35)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 35)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 35)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 35)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 36)

### Cell 85 ❌

**Preview**: `# Lab 21: MS Learn Documentation Search # Query Microsoft Learn via MCP server  async def mslearn_se...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 32)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 33)

### Cell 87 ✅

**Preview**: `### Lab 22: MS Learn + AI Learning Assistant`

**Status**: Success (Attempt 1/5)

### Cell 89 ✅

**Preview**: `# Lab 25: Additional MS Learn examples # (Reserved for future examples)`

**Status**: Success (Attempt 1/5)

### Cell 91 ❌

**Preview**: `### Lab 23: Multi-Server Orchestration Coordinate multiple MCP servers for complex workflows`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - invalid syntax (<string>, line 2)
- Attempt 2: `SyntaxError` - invalid syntax (<string>, line 2)
- Attempt 3: `SyntaxError` - invalid syntax (<string>, line 2)
- Attempt 4: `SyntaxError` - invalid syntax (<string>, line 2)
- Attempt 5: `SyntaxError` - invalid syntax (<string>, line 3)

### Cell 92 ❌

**Preview**: `# Lab 23: Multi-Server Orchestration # Use multiple MCP servers together for a complete workflow  as...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 52)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 52)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 52)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 52)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 53)

### Cell 93 ❌

**Preview**: `### Lab 24: Error Handling & Resilience Handle MCP server errors gracefully`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - invalid syntax (<string>, line 2)
- Attempt 2: `SyntaxError` - invalid syntax (<string>, line 2)
- Attempt 3: `SyntaxError` - invalid syntax (<string>, line 2)
- Attempt 4: `SyntaxError` - invalid syntax (<string>, line 2)
- Attempt 5: `SyntaxError` - invalid syntax (<string>, line 3)

### Cell 96 ✅

**Preview**: `import redis.asyncio as redis  questions = [     'How to make coffee?',     'What is the best way to...`

**Status**: Success (Attempt 5/5)

### Cell 99 ✅

**Preview**: `image_url = f'{apim_gateway_url}/{inference_api_path}/openai/deployments/dall-e-3/images/generations...`

**Status**: Success (Attempt 5/5)

### Cell 100 ✅

**Preview**: `print('Master Lab Testing Complete!') print(f'Tested {31} labs successfully.') print('To cleanup: Ru...`

**Status**: Success (Attempt 5/5)

### Cell 102 ✅

**Preview**: `# Test invalid model try:     client.chat.completions.create(         model='invalid-model',        ...`

**Status**: Success (Attempt 1/5)

### Cell 104 ✅

**Preview**: `for max_tokens in [10, 50, 100]:     response = client.chat.completions.create(         model='gpt-4...`

**Status**: Success (Attempt 5/5)

### Cell 106 ✅

**Preview**: `for temp in [0.0, 0.5, 1.0, 1.5, 2.0]:     response = client.chat.completions.create(         model=...`

**Status**: Success (Attempt 5/5)

### Cell 108 ✅

**Preview**: `system_prompts = [     'You are a helpful assistant.',     'You are a sarcastic comedian.',     'You...`

**Status**: Success (Attempt 5/5)

### Cell 110 ✅

**Preview**: `conversation = [     {'role': 'system', 'content': 'You are a helpful assistant.'},     {'role': 'us...`

**Status**: Success (Attempt 5/5)

### Cell 112 ✅

**Preview**: `import concurrent.futures  def make_request(i):     start = time.time()     response = client.chat.c...`

**Status**: Success (Attempt 5/5)

### Cell 114 ✅

**Preview**: `print('Testing failover behavior...') for i in range(15):     try:         response = client.chat.co...`

**Status**: Success (Attempt 1/5)

### Cell 116 ✅

**Preview**: `# Simulate high load load_results = [] for i in range(50):     start = time.time()     response = cl...`

**Status**: Success (Attempt 5/5)

### Cell 118 ✅

**Preview**: `cache_stats = {'hits': 0, 'misses': 0} test_questions = [     'What is Python?',     'Explain Python...`

**Status**: Success (Attempt 5/5)

### Cell 120 ❌

**Preview**: `import redis.asyncio as redis  async def test_redis():     r = await redis.from_url(         f'redis...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 13)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 13)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 13)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 13)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 14)

### Cell 122 ✅

**Preview**: `prompts = [     'A serene mountain landscape at dawn',     'Abstract geometric patterns in blue and ...`

**Status**: Success (Attempt 5/5)

### Cell 124 ✅

**Preview**: `# Use GPT-4o (multimodal) to analyze generated image # (assuming we have a generated image from prev...`

**Status**: Success (Attempt 5/5)

### Cell 126 ✅

**Preview**: `# Query logs print('Check Azure Portal -> Log Analytics for detailed logs')`

**Status**: Success (Attempt 1/5)

### Cell 128 ✅

**Preview**: `usage_data = [] for i in range(20):     response = client.chat.completions.create(         model='gp...`

**Status**: Success (Attempt 5/5)

### Cell 130 ✅

**Preview**: `for delay in [0.1, 0.5, 1.0]:     print(f'Testing with {delay}s delay...')     for i in range(5):   ...`

**Status**: Success (Attempt 5/5)

### Cell 132 ❌

**Preview**: `# Test with different API keys for i, sub in enumerate(apim_subscriptions[:2]):     test_client = Az...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - invalid syntax. Perhaps you forgot a comma? (<string>, line 4)
- Attempt 2: `SyntaxError` - invalid syntax. Perhaps you forgot a comma? (<string>, line 4)
- Attempt 3: `SyntaxError` - invalid syntax. Perhaps you forgot a comma? (<string>, line 4)
- Attempt 4: `SyntaxError` - invalid syntax. Perhaps you forgot a comma? (<string>, line 4)
- Attempt 5: `SyntaxError` - invalid syntax. Perhaps you forgot a comma? (<string>, line 5)

### Cell 134 ✅

**Preview**: `test_prompts = [     ('Safe: Weather question', 'What is the weather today?'),     ('Safe: Recipe', ...`

**Status**: Success (Attempt 1/5)

### Cell 136 ✅

**Preview**: `models = ['gpt-4o-mini', 'gpt-4.1-mini', 'gpt-4.1'] results = []  for model in models:     start = t...`

**Status**: Success (Attempt 5/5)

### Cell 138 ✅

**Preview**: `print('Testing Foundry SDK streaming...') response = inference_client.complete(     messages=[UserMe...`

**Status**: Success (Attempt 5/5)

### Cell 140 ✅

**Preview**: `reasoning_prompts = [     'Solve: If 5 workers take 10 days to build a house, how long for 10 worker...`

**Status**: Success (Attempt 5/5)

### Cell 142 ❌

**Preview**: `async def list_mcp_tools(server_url):     async with streamablehttp_client(server_url) as (read, wri...`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 12)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 12)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 12)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 12)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 13)

### Cell 144 ✅

**Preview**: `mcp_urls = [s['url'] for s in mcp_servers] print(f'Testing {len(mcp_urls)} MCP servers...') for i, u...`

**Status**: Success (Attempt 5/5)

### Cell 146 ✅

**Preview**: `print('MCP OAuth authorization configured')`

**Status**: Success (Attempt 1/5)

### Cell 148 ✅

**Preview**: `# Test agent-to-agent communication print('Testing A2A agent communication...') # (Requires agent de...`

**Status**: Success (Attempt 1/5)

### Cell 150 ✅

**Preview**: `# Using Azure AI Agents agents_client = project_client.agents  # Create agent agent = agents_client....`

**Status**: Success (Attempt 5/5)

### Cell 152 ✅

**Preview**: `# Test multiple agent scenarios print('AI Agent Service testing...') # (Requires full agent deployme...`

**Status**: Success (Attempt 1/5)

### Cell 154 ✅

**Preview**: `print('Realtime MCP agents configured')`

**Status**: Success (Attempt 1/5)

### Cell 156 ✅

**Preview**: `functions = [     {         'name': 'get_weather',         'description': 'Get weather for a locatio...`

**Status**: Success (Attempt 5/5)

### Cell 158 ✅

**Preview**: `# Test cache with varying prompts base_prompt = 'Explain machine learning' variations = [     'Expla...`

**Status**: Success (Attempt 5/5)

### Cell 160 ✅

**Preview**: `# Store messages in Cosmos DB print(f'Cosmos DB endpoint: {cosmos_endpoint}') print('[OK] Message st...`

**Status**: Success (Attempt 5/5)

### Cell 162 ✅

**Preview**: `from azure.search.documents.indexes.models import SearchIndex, SearchField  # Create search index in...`

**Status**: Success (Attempt 5/5)

### Cell 164 ✅

**Preview**: `prompts = [     'A peaceful zen garden',     'Abstract art with vibrant colors',     'Futuristic tec...`

**Status**: Success (Attempt 5/5)

### Cell 166 ✅

**Preview**: `print('Realtime audio model: gpt-4o-realtime-preview') # Test realtime audio capabilities print('[OK...`

**Status**: Success (Attempt 1/5)

### Cell 168 ✅

**Preview**: `# Simulate cost tracking costs = [] for i in range(10):     response = client.chat.completions.creat...`

**Status**: Success (Attempt 5/5)

### Cell 170 ✅

**Preview**: `# Test secure response handling response = client.chat.completions.create(     model='gpt-4o-mini', ...`

**Status**: Success (Attempt 5/5)

### Cell 172 ✅

**Preview**: `print('='*60) print('MASTER LAB TESTING COMPLETE') print('='*60) print('\nSummary:') print('  - 31 l...`

**Status**: Success (Attempt 1/5)

### Cell 174 ✅

**Preview**: `# Test scenario 1 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=[...`

**Status**: Success (Attempt 5/5)

### Cell 176 ✅

**Preview**: `# Test scenario 2 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=[...`

**Status**: Success (Attempt 5/5)

### Cell 178 ✅

**Preview**: `# Test scenario 3 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=[...`

**Status**: Success (Attempt 5/5)

### Cell 180 ✅

**Preview**: `# Test scenario 4 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=[...`

**Status**: Success (Attempt 5/5)

### Cell 182 ✅

**Preview**: `# Test scenario 5 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=[...`

**Status**: Success (Attempt 5/5)

### Cell 184 ✅

**Preview**: `# Test scenario 6 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=[...`

**Status**: Success (Attempt 5/5)

### Cell 186 ✅

**Preview**: `# Test scenario 7 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=[...`

**Status**: Success (Attempt 5/5)

### Cell 188 ✅

**Preview**: `# Test scenario 8 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=[...`

**Status**: Success (Attempt 5/5)

### Cell 190 ✅

**Preview**: `# Test scenario 9 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=[...`

**Status**: Success (Attempt 5/5)

### Cell 192 ✅

**Preview**: `# Test scenario 10 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=...`

**Status**: Success (Attempt 5/5)

### Cell 194 ✅

**Preview**: `# Test scenario 11 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=...`

**Status**: Success (Attempt 5/5)

### Cell 196 ✅

**Preview**: `# Test scenario 12 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=...`

**Status**: Success (Attempt 5/5)

### Cell 198 ✅

**Preview**: `# Test scenario 13 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=...`

**Status**: Success (Attempt 5/5)

### Cell 200 ✅

**Preview**: `# Test scenario 14 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=...`

**Status**: Success (Attempt 5/5)

### Cell 202 ✅

**Preview**: `# Test scenario 15 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=...`

**Status**: Success (Attempt 5/5)

### Cell 204 ✅

**Preview**: `# Test scenario 16 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=...`

**Status**: Success (Attempt 5/5)

### Cell 206 ✅

**Preview**: `# Test scenario 17 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=...`

**Status**: Success (Attempt 5/5)

### Cell 208 ✅

**Preview**: `# Test scenario 18 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=...`

**Status**: Success (Attempt 5/5)

### Cell 210 ✅

**Preview**: `# Test scenario 19 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=...`

**Status**: Success (Attempt 5/5)

### Cell 212 ✅

**Preview**: `# Test scenario 20 response = client.chat.completions.create(     model='gpt-4o-mini',     messages=...`

**Status**: Success (Attempt 5/5)

### Cell 214 ✅

**Preview**: `# Region failover test 1 results = [] for i in range(10):     start = time.time()     response = cli...`

**Status**: Success (Attempt 5/5)

### Cell 216 ✅

**Preview**: `# Region failover test 2 results = [] for i in range(10):     start = time.time()     response = cli...`

**Status**: Success (Attempt 5/5)

### Cell 218 ✅

**Preview**: `# Region failover test 3 results = [] for i in range(10):     start = time.time()     response = cli...`

**Status**: Success (Attempt 5/5)

### Cell 220 ✅

**Preview**: `# Region failover test 4 results = [] for i in range(10):     start = time.time()     response = cli...`

**Status**: Success (Attempt 5/5)

### Cell 222 ✅

**Preview**: `# Region failover test 5 results = [] for i in range(10):     start = time.time()     response = cli...`

**Status**: Success (Attempt 5/5)

### Cell 224 ✅

**Preview**: `# Region failover test 6 results = [] for i in range(10):     start = time.time()     response = cli...`

**Status**: Success (Attempt 5/5)

### Cell 226 ✅

**Preview**: `# Region failover test 7 results = [] for i in range(10):     start = time.time()     response = cli...`

**Status**: Success (Attempt 5/5)

### Cell 228 ✅

**Preview**: `# Region failover test 8 results = [] for i in range(10):     start = time.time()     response = cli...`

**Status**: Success (Attempt 5/5)

### Cell 230 ✅

**Preview**: `# Region failover test 9 results = [] for i in range(10):     start = time.time()     response = cli...`

**Status**: Success (Attempt 5/5)

### Cell 232 ✅

**Preview**: `# Region failover test 10 results = [] for i in range(10):     start = time.time()     response = cl...`

**Status**: Success (Attempt 5/5)

### Cell 234 ✅

**Preview**: `# Region failover test 11 results = [] for i in range(10):     start = time.time()     response = cl...`

**Status**: Success (Attempt 5/5)

### Cell 236 ✅

**Preview**: `# Region failover test 12 results = [] for i in range(10):     start = time.time()     response = cl...`

**Status**: Success (Attempt 5/5)

### Cell 238 ✅

**Preview**: `# Region failover test 13 results = [] for i in range(10):     start = time.time()     response = cl...`

**Status**: Success (Attempt 5/5)

### Cell 240 ✅

**Preview**: `# Region failover test 14 results = [] for i in range(10):     start = time.time()     response = cl...`

**Status**: Success (Attempt 5/5)

### Cell 242 ✅

**Preview**: `# Region failover test 15 results = [] for i in range(10):     start = time.time()     response = cl...`

**Status**: Success (Attempt 5/5)

### Cell 244 ✅

**Preview**: `# Region failover test 16 results = [] for i in range(10):     start = time.time()     response = cl...`

**Status**: Success (Attempt 5/5)

### Cell 246 ✅

**Preview**: `# Region failover test 17 results = [] for i in range(10):     start = time.time()     response = cl...`

**Status**: Success (Attempt 5/5)

### Cell 248 ✅

**Preview**: `# Region failover test 18 results = [] for i in range(10):     start = time.time()     response = cl...`

**Status**: Success (Attempt 5/5)

### Cell 250 ✅

**Preview**: `# Region failover test 19 results = [] for i in range(10):     start = time.time()     response = cl...`

**Status**: Success (Attempt 5/5)

### Cell 252 ✅

**Preview**: `# Region failover test 20 results = [] for i in range(10):     start = time.time()     response = cl...`

**Status**: Success (Attempt 5/5)

### Cell 254 ✅

**Preview**: `# Generate logs for test 1 for i in range(5):     client.chat.completions.create(         model='gpt...`

**Status**: Success (Attempt 5/5)

### Cell 256 ✅

**Preview**: `# Generate logs for test 2 for i in range(5):     client.chat.completions.create(         model='gpt...`

**Status**: Success (Attempt 5/5)

### Cell 258 ✅

**Preview**: `# Generate logs for test 3 for i in range(5):     client.chat.completions.create(         model='gpt...`

**Status**: Success (Attempt 5/5)

### Cell 260 ✅

**Preview**: `# Generate logs for test 4 for i in range(5):     client.chat.completions.create(         model='gpt...`

**Status**: Success (Attempt 5/5)

### Cell 262 ✅

**Preview**: `# Generate logs for test 5 for i in range(5):     client.chat.completions.create(         model='gpt...`

**Status**: Success (Attempt 5/5)

### Cell 264 ✅

**Preview**: `# Generate logs for test 6 for i in range(5):     client.chat.completions.create(         model='gpt...`

**Status**: Success (Attempt 5/5)

### Cell 266 ✅

**Preview**: `# Generate logs for test 7 for i in range(5):     client.chat.completions.create(         model='gpt...`

**Status**: Success (Attempt 5/5)

### Cell 268 ✅

**Preview**: `# Generate logs for test 8 for i in range(5):     client.chat.completions.create(         model='gpt...`

**Status**: Success (Attempt 5/5)

### Cell 270 ✅

**Preview**: `# Generate logs for test 9 for i in range(5):     client.chat.completions.create(         model='gpt...`

**Status**: Success (Attempt 5/5)

### Cell 272 ✅

**Preview**: `# Generate logs for test 10 for i in range(5):     client.chat.completions.create(         model='gp...`

**Status**: Success (Attempt 5/5)

### Cell 274 ✅

**Preview**: `# Token usage analysis 1 tokens_used = [] for i in range(5):     response = client.chat.completions....`

**Status**: Success (Attempt 5/5)

### Cell 276 ✅

**Preview**: `# Token usage analysis 2 tokens_used = [] for i in range(5):     response = client.chat.completions....`

**Status**: Success (Attempt 5/5)

### Cell 278 ✅

**Preview**: `# Token usage analysis 3 tokens_used = [] for i in range(5):     response = client.chat.completions....`

**Status**: Success (Attempt 5/5)

### Cell 280 ✅

**Preview**: `# Token usage analysis 4 tokens_used = [] for i in range(5):     response = client.chat.completions....`

**Status**: Success (Attempt 5/5)

### Cell 282 ✅

**Preview**: `# Token usage analysis 5 tokens_used = [] for i in range(5):     response = client.chat.completions....`

**Status**: Success (Attempt 5/5)

### Cell 284 ✅

**Preview**: `# Token usage analysis 6 tokens_used = [] for i in range(5):     response = client.chat.completions....`

**Status**: Success (Attempt 5/5)

### Cell 286 ✅

**Preview**: `# Token usage analysis 7 tokens_used = [] for i in range(5):     response = client.chat.completions....`

**Status**: Success (Attempt 5/5)

### Cell 288 ✅

**Preview**: `# Token usage analysis 8 tokens_used = [] for i in range(5):     response = client.chat.completions....`

**Status**: Success (Attempt 5/5)

### Cell 290 ✅

**Preview**: `# Token usage analysis 9 tokens_used = [] for i in range(5):     response = client.chat.completions....`

**Status**: Success (Attempt 5/5)

### Cell 292 ✅

**Preview**: `# Token usage analysis 10 tokens_used = [] for i in range(5):     response = client.chat.completions...`

**Status**: Success (Attempt 5/5)

### Cell 294 ✅

**Preview**: `# Token usage analysis 11 tokens_used = [] for i in range(5):     response = client.chat.completions...`

**Status**: Success (Attempt 5/5)

### Cell 296 ✅

**Preview**: `# Token usage analysis 12 tokens_used = [] for i in range(5):     response = client.chat.completions...`

**Status**: Success (Attempt 5/5)

### Cell 298 ✅

**Preview**: `# Token usage analysis 13 tokens_used = [] for i in range(5):     response = client.chat.completions...`

**Status**: Success (Attempt 5/5)

### Cell 300 ✅

**Preview**: `# Token usage analysis 14 tokens_used = [] for i in range(5):     response = client.chat.completions...`

**Status**: Success (Attempt 5/5)

### Cell 302 ✅

**Preview**: `# Token usage analysis 15 tokens_used = [] for i in range(5):     response = client.chat.completions...`

**Status**: Success (Attempt 5/5)

### Cell 304 ✅

**Preview**: `# Rate limiting scenario 1 for i in range(5):     try:         response = client.chat.completions.cr...`

**Status**: Success (Attempt 1/5)

### Cell 306 ✅

**Preview**: `# Rate limiting scenario 2 for i in range(5):     try:         response = client.chat.completions.cr...`

**Status**: Success (Attempt 1/5)

### Cell 308 ✅

**Preview**: `# Rate limiting scenario 3 for i in range(5):     try:         response = client.chat.completions.cr...`

**Status**: Success (Attempt 1/5)

### Cell 310 ✅

**Preview**: `# Rate limiting scenario 4 for i in range(5):     try:         response = client.chat.completions.cr...`

**Status**: Success (Attempt 1/5)

### Cell 312 ✅

**Preview**: `# Rate limiting scenario 5 for i in range(5):     try:         response = client.chat.completions.cr...`

**Status**: Success (Attempt 1/5)

### Cell 314 ✅

**Preview**: `# Rate limiting scenario 6 for i in range(5):     try:         response = client.chat.completions.cr...`

**Status**: Success (Attempt 1/5)

### Cell 316 ✅

**Preview**: `# Rate limiting scenario 7 for i in range(5):     try:         response = client.chat.completions.cr...`

**Status**: Success (Attempt 1/5)

### Cell 318 ✅

**Preview**: `# Rate limiting scenario 8 for i in range(5):     try:         response = client.chat.completions.cr...`

**Status**: Success (Attempt 1/5)

### Cell 320 ✅

**Preview**: `# Rate limiting scenario 9 for i in range(5):     try:         response = client.chat.completions.cr...`

**Status**: Success (Attempt 1/5)

### Cell 322 ✅

**Preview**: `# Rate limiting scenario 10 for i in range(5):     try:         response = client.chat.completions.c...`

**Status**: Success (Attempt 1/5)

### Cell 324 ✅

**Preview**: `# Lab 6 - Test scenario 1 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 326 ✅

**Preview**: `# Lab 6 - Test scenario 2 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 328 ✅

**Preview**: `# Lab 6 - Test scenario 3 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 330 ✅

**Preview**: `# Lab 6 - Test scenario 4 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 332 ✅

**Preview**: `# Lab 6 - Test scenario 5 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 334 ✅

**Preview**: `# Lab 6 - Test scenario 6 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 336 ✅

**Preview**: `# Lab 6 - Test scenario 7 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 338 ✅

**Preview**: `# Lab 6 - Test scenario 8 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 340 ✅

**Preview**: `# Lab 6 - Test scenario 9 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 342 ✅

**Preview**: `# Lab 6 - Test scenario 10 response = client.chat.completions.create(     model='gpt-4o-mini',     m...`

**Status**: Success (Attempt 5/5)

### Cell 344 ✅

**Preview**: `# Lab 7 - Test scenario 1 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 346 ✅

**Preview**: `# Lab 7 - Test scenario 2 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 348 ✅

**Preview**: `# Lab 7 - Test scenario 3 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 350 ✅

**Preview**: `# Lab 7 - Test scenario 4 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 352 ✅

**Preview**: `# Lab 7 - Test scenario 5 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 354 ✅

**Preview**: `# Lab 7 - Test scenario 6 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 356 ✅

**Preview**: `# Lab 7 - Test scenario 7 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 358 ✅

**Preview**: `# Lab 7 - Test scenario 8 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 360 ✅

**Preview**: `# Lab 7 - Test scenario 9 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 362 ✅

**Preview**: `# Lab 7 - Test scenario 10 response = client.chat.completions.create(     model='gpt-4o-mini',     m...`

**Status**: Success (Attempt 5/5)

### Cell 364 ✅

**Preview**: `# Lab 8 - Test scenario 1 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 366 ✅

**Preview**: `# Lab 8 - Test scenario 2 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 368 ✅

**Preview**: `# Lab 8 - Test scenario 3 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 370 ✅

**Preview**: `# Lab 8 - Test scenario 4 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 372 ✅

**Preview**: `# Lab 8 - Test scenario 5 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 374 ✅

**Preview**: `# Lab 8 - Test scenario 6 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 376 ✅

**Preview**: `# Lab 8 - Test scenario 7 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 378 ✅

**Preview**: `# Lab 8 - Test scenario 8 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 380 ✅

**Preview**: `# Lab 8 - Test scenario 9 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 382 ✅

**Preview**: `# Lab 8 - Test scenario 10 response = client.chat.completions.create(     model='gpt-4o-mini',     m...`

**Status**: Success (Attempt 5/5)

### Cell 384 ✅

**Preview**: `# Lab 9 - Test scenario 1 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 386 ✅

**Preview**: `# Lab 9 - Test scenario 2 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 388 ✅

**Preview**: `# Lab 9 - Test scenario 3 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 390 ✅

**Preview**: `# Lab 9 - Test scenario 4 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 392 ✅

**Preview**: `# Lab 9 - Test scenario 5 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 394 ✅

**Preview**: `# Lab 9 - Test scenario 6 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 396 ✅

**Preview**: `# Lab 9 - Test scenario 7 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 398 ✅

**Preview**: `# Lab 9 - Test scenario 8 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 400 ✅

**Preview**: `# Lab 9 - Test scenario 9 response = client.chat.completions.create(     model='gpt-4o-mini',     me...`

**Status**: Success (Attempt 5/5)

### Cell 402 ✅

**Preview**: `# Lab 9 - Test scenario 10 response = client.chat.completions.create(     model='gpt-4o-mini',     m...`

**Status**: Success (Attempt 5/5)

### Cell 404 ✅

**Preview**: `# Lab 10 - Test scenario 1 response = client.chat.completions.create(     model='gpt-4o-mini',     m...`

**Status**: Success (Attempt 5/5)

### Cell 406 ✅

**Preview**: `# Lab 10 - Test scenario 2 response = client.chat.completions.create(     model='gpt-4o-mini',     m...`

**Status**: Success (Attempt 5/5)

### Cell 408 ✅

**Preview**: `# Lab 10 - Test scenario 3 response = client.chat.completions.create(     model='gpt-4o-mini',     m...`

**Status**: Success (Attempt 5/5)

### Cell 410 ✅

**Preview**: `# Lab 10 - Test scenario 4 response = client.chat.completions.create(     model='gpt-4o-mini',     m...`

**Status**: Success (Attempt 5/5)

### Cell 412 ✅

**Preview**: `# Lab 10 - Test scenario 5 response = client.chat.completions.create(     model='gpt-4o-mini',     m...`

**Status**: Success (Attempt 5/5)

### Cell 414 ✅

**Preview**: `# Lab 10 - Test scenario 6 response = client.chat.completions.create(     model='gpt-4o-mini',     m...`

**Status**: Success (Attempt 5/5)

### Cell 416 ✅

**Preview**: `# Lab 10 - Test scenario 7 response = client.chat.completions.create(     model='gpt-4o-mini',     m...`

**Status**: Success (Attempt 5/5)

### Cell 418 ✅

**Preview**: `# Lab 10 - Test scenario 8 response = client.chat.completions.create(     model='gpt-4o-mini',     m...`

**Status**: Success (Attempt 5/5)

### Cell 420 ✅

**Preview**: `# Lab 10 - Test scenario 9 response = client.chat.completions.create(     model='gpt-4o-mini',     m...`

**Status**: Success (Attempt 5/5)

### Cell 422 ✅

**Preview**: `# Lab 10 - Test scenario 10 response = client.chat.completions.create(     model='gpt-4o-mini',     ...`

**Status**: Success (Attempt 5/5)

### Cell 424 ✅

**Preview**: `# Lab 11 MCP/Agent scenario 1 print(f'Lab 11 Agent Test 1: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 426 ✅

**Preview**: `# Lab 11 MCP/Agent scenario 2 print(f'Lab 11 Agent Test 2: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 428 ✅

**Preview**: `# Lab 11 MCP/Agent scenario 3 print(f'Lab 11 Agent Test 3: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 430 ✅

**Preview**: `# Lab 11 MCP/Agent scenario 4 print(f'Lab 11 Agent Test 4: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 432 ✅

**Preview**: `# Lab 11 MCP/Agent scenario 5 print(f'Lab 11 Agent Test 5: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 434 ✅

**Preview**: `# Lab 11 MCP/Agent scenario 6 print(f'Lab 11 Agent Test 6: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 436 ✅

**Preview**: `# Lab 11 MCP/Agent scenario 7 print(f'Lab 11 Agent Test 7: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 438 ✅

**Preview**: `# Lab 11 MCP/Agent scenario 8 print(f'Lab 11 Agent Test 8: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 440 ✅

**Preview**: `# Lab 11 MCP/Agent scenario 9 print(f'Lab 11 Agent Test 9: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 442 ✅

**Preview**: `# Lab 11 MCP/Agent scenario 10 print(f'Lab 11 Agent Test 10: Configured') # Agent/MCP specific tests...`

**Status**: Success (Attempt 1/5)

### Cell 444 ✅

**Preview**: `# Lab 12 MCP/Agent scenario 1 print(f'Lab 12 Agent Test 1: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 446 ✅

**Preview**: `# Lab 12 MCP/Agent scenario 2 print(f'Lab 12 Agent Test 2: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 448 ✅

**Preview**: `# Lab 12 MCP/Agent scenario 3 print(f'Lab 12 Agent Test 3: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 450 ✅

**Preview**: `# Lab 12 MCP/Agent scenario 4 print(f'Lab 12 Agent Test 4: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 452 ✅

**Preview**: `# Lab 12 MCP/Agent scenario 5 print(f'Lab 12 Agent Test 5: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 454 ✅

**Preview**: `# Lab 12 MCP/Agent scenario 6 print(f'Lab 12 Agent Test 6: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 456 ✅

**Preview**: `# Lab 12 MCP/Agent scenario 7 print(f'Lab 12 Agent Test 7: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 458 ✅

**Preview**: `# Lab 12 MCP/Agent scenario 8 print(f'Lab 12 Agent Test 8: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 460 ✅

**Preview**: `# Lab 12 MCP/Agent scenario 9 print(f'Lab 12 Agent Test 9: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 462 ✅

**Preview**: `# Lab 12 MCP/Agent scenario 10 print(f'Lab 12 Agent Test 10: Configured') # Agent/MCP specific tests...`

**Status**: Success (Attempt 1/5)

### Cell 464 ✅

**Preview**: `# Lab 13 MCP/Agent scenario 1 print(f'Lab 13 Agent Test 1: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 466 ✅

**Preview**: `# Lab 13 MCP/Agent scenario 2 print(f'Lab 13 Agent Test 2: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 468 ✅

**Preview**: `# Lab 13 MCP/Agent scenario 3 print(f'Lab 13 Agent Test 3: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 470 ✅

**Preview**: `# Lab 13 MCP/Agent scenario 4 print(f'Lab 13 Agent Test 4: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 472 ✅

**Preview**: `# Lab 13 MCP/Agent scenario 5 print(f'Lab 13 Agent Test 5: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 474 ✅

**Preview**: `# Lab 13 MCP/Agent scenario 6 print(f'Lab 13 Agent Test 6: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 476 ✅

**Preview**: `# Lab 13 MCP/Agent scenario 7 print(f'Lab 13 Agent Test 7: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 478 ✅

**Preview**: `# Lab 13 MCP/Agent scenario 8 print(f'Lab 13 Agent Test 8: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 480 ✅

**Preview**: `# Lab 13 MCP/Agent scenario 9 print(f'Lab 13 Agent Test 9: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 482 ✅

**Preview**: `# Lab 13 MCP/Agent scenario 10 print(f'Lab 13 Agent Test 10: Configured') # Agent/MCP specific tests...`

**Status**: Success (Attempt 1/5)

### Cell 484 ✅

**Preview**: `# Lab 14 MCP/Agent scenario 1 print(f'Lab 14 Agent Test 1: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 486 ✅

**Preview**: `# Lab 14 MCP/Agent scenario 2 print(f'Lab 14 Agent Test 2: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 488 ✅

**Preview**: `# Lab 14 MCP/Agent scenario 3 print(f'Lab 14 Agent Test 3: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 490 ✅

**Preview**: `# Lab 14 MCP/Agent scenario 4 print(f'Lab 14 Agent Test 4: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 492 ✅

**Preview**: `# Lab 14 MCP/Agent scenario 5 print(f'Lab 14 Agent Test 5: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 494 ✅

**Preview**: `# Lab 14 MCP/Agent scenario 6 print(f'Lab 14 Agent Test 6: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 496 ✅

**Preview**: `# Lab 14 MCP/Agent scenario 7 print(f'Lab 14 Agent Test 7: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 498 ✅

**Preview**: `# Lab 14 MCP/Agent scenario 8 print(f'Lab 14 Agent Test 8: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 500 ✅

**Preview**: `# Lab 14 MCP/Agent scenario 9 print(f'Lab 14 Agent Test 9: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 502 ✅

**Preview**: `# Lab 14 MCP/Agent scenario 10 print(f'Lab 14 Agent Test 10: Configured') # Agent/MCP specific tests...`

**Status**: Success (Attempt 1/5)

### Cell 504 ✅

**Preview**: `# Lab 15 MCP/Agent scenario 1 print(f'Lab 15 Agent Test 1: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 506 ✅

**Preview**: `# Lab 15 MCP/Agent scenario 2 print(f'Lab 15 Agent Test 2: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 508 ✅

**Preview**: `# Lab 15 MCP/Agent scenario 3 print(f'Lab 15 Agent Test 3: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 510 ✅

**Preview**: `# Lab 15 MCP/Agent scenario 4 print(f'Lab 15 Agent Test 4: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 512 ✅

**Preview**: `# Lab 15 MCP/Agent scenario 5 print(f'Lab 15 Agent Test 5: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 514 ✅

**Preview**: `# Lab 15 MCP/Agent scenario 6 print(f'Lab 15 Agent Test 6: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 516 ✅

**Preview**: `# Lab 15 MCP/Agent scenario 7 print(f'Lab 15 Agent Test 7: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 518 ✅

**Preview**: `# Lab 15 MCP/Agent scenario 8 print(f'Lab 15 Agent Test 8: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 520 ✅

**Preview**: `# Lab 15 MCP/Agent scenario 9 print(f'Lab 15 Agent Test 9: Configured') # Agent/MCP specific tests p...`

**Status**: Success (Attempt 1/5)

### Cell 522 ✅

**Preview**: `# Lab 15 MCP/Agent scenario 10 print(f'Lab 15 Agent Test 10: Configured') # Agent/MCP specific tests...`

**Status**: Success (Attempt 1/5)

### Cell 524 ✅

**Preview**: `# Lab 16 advanced feature test 1 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 526 ✅

**Preview**: `# Lab 16 advanced feature test 2 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 528 ✅

**Preview**: `# Lab 16 advanced feature test 3 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 530 ✅

**Preview**: `# Lab 16 advanced feature test 4 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 532 ✅

**Preview**: `# Lab 16 advanced feature test 5 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 534 ✅

**Preview**: `# Lab 16 advanced feature test 6 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 536 ✅

**Preview**: `# Lab 16 advanced feature test 7 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 538 ✅

**Preview**: `# Lab 16 advanced feature test 8 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 540 ✅

**Preview**: `# Lab 16 advanced feature test 9 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 542 ✅

**Preview**: `# Lab 16 advanced feature test 10 response = client.chat.completions.create(     model='gpt-4o-mini'...`

**Status**: Success (Attempt 5/5)

### Cell 544 ✅

**Preview**: `# Lab 17 advanced feature test 1 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 546 ✅

**Preview**: `# Lab 17 advanced feature test 2 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 548 ✅

**Preview**: `# Lab 17 advanced feature test 3 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 550 ✅

**Preview**: `# Lab 17 advanced feature test 4 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 552 ✅

**Preview**: `# Lab 17 advanced feature test 5 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 554 ✅

**Preview**: `# Lab 17 advanced feature test 6 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 556 ✅

**Preview**: `# Lab 17 advanced feature test 7 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 558 ✅

**Preview**: `# Lab 17 advanced feature test 8 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 560 ✅

**Preview**: `# Lab 17 advanced feature test 9 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 562 ✅

**Preview**: `# Lab 17 advanced feature test 10 response = client.chat.completions.create(     model='gpt-4o-mini'...`

**Status**: Success (Attempt 5/5)

### Cell 564 ✅

**Preview**: `# Lab 18 advanced feature test 1 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 566 ✅

**Preview**: `# Lab 18 advanced feature test 2 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 568 ✅

**Preview**: `# Lab 18 advanced feature test 3 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 570 ✅

**Preview**: `# Lab 18 advanced feature test 4 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 572 ✅

**Preview**: `# Lab 18 advanced feature test 5 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 574 ✅

**Preview**: `# Lab 18 advanced feature test 6 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 576 ✅

**Preview**: `# Lab 18 advanced feature test 7 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 578 ✅

**Preview**: `# Lab 18 advanced feature test 8 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 580 ✅

**Preview**: `# Lab 18 advanced feature test 9 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 582 ✅

**Preview**: `# Lab 18 advanced feature test 10 response = client.chat.completions.create(     model='gpt-4o-mini'...`

**Status**: Success (Attempt 5/5)

### Cell 584 ✅

**Preview**: `# Lab 19 advanced feature test 1 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 586 ✅

**Preview**: `# Lab 19 advanced feature test 2 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 588 ✅

**Preview**: `# Lab 19 advanced feature test 3 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 590 ✅

**Preview**: `# Lab 19 advanced feature test 4 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 592 ✅

**Preview**: `# Lab 19 advanced feature test 5 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 594 ✅

**Preview**: `# Lab 19 advanced feature test 6 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 596 ✅

**Preview**: `# Lab 19 advanced feature test 7 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 598 ✅

**Preview**: `# Lab 19 advanced feature test 8 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 600 ✅

**Preview**: `# Lab 19 advanced feature test 9 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 602 ✅

**Preview**: `# Lab 19 advanced feature test 10 response = client.chat.completions.create(     model='gpt-4o-mini'...`

**Status**: Success (Attempt 5/5)

### Cell 604 ✅

**Preview**: `# Lab 20 advanced feature test 1 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 606 ✅

**Preview**: `# Lab 20 advanced feature test 2 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 608 ✅

**Preview**: `# Lab 20 advanced feature test 3 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 610 ✅

**Preview**: `# Lab 20 advanced feature test 4 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 612 ✅

**Preview**: `# Lab 20 advanced feature test 5 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 614 ✅

**Preview**: `# Lab 20 advanced feature test 6 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 616 ✅

**Preview**: `# Lab 20 advanced feature test 7 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 618 ✅

**Preview**: `# Lab 20 advanced feature test 8 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 620 ✅

**Preview**: `# Lab 20 advanced feature test 9 response = client.chat.completions.create(     model='gpt-4o-mini',...`

**Status**: Success (Attempt 5/5)

### Cell 622 ✅

**Preview**: `# Lab 20 advanced feature test 10 response = client.chat.completions.create(     model='gpt-4o-mini'...`

**Status**: Success (Attempt 5/5)

### Cell 624 ✅

**Preview**: `# Semantic caching test 1 cache_times = [] for i in range(10):     start = time.time()     response ...`

**Status**: Success (Attempt 5/5)

### Cell 626 ✅

**Preview**: `# Semantic caching test 2 cache_times = [] for i in range(10):     start = time.time()     response ...`

**Status**: Success (Attempt 5/5)

### Cell 628 ✅

**Preview**: `# Semantic caching test 3 cache_times = [] for i in range(10):     start = time.time()     response ...`

**Status**: Success (Attempt 5/5)

### Cell 630 ✅

**Preview**: `# Semantic caching test 4 cache_times = [] for i in range(10):     start = time.time()     response ...`

**Status**: Success (Attempt 5/5)

### Cell 632 ✅

**Preview**: `# Semantic caching test 5 cache_times = [] for i in range(10):     start = time.time()     response ...`

**Status**: Success (Attempt 5/5)

### Cell 634 ✅

**Preview**: `# Semantic caching test 6 cache_times = [] for i in range(10):     start = time.time()     response ...`

**Status**: Success (Attempt 5/5)

### Cell 636 ✅

**Preview**: `# Semantic caching test 7 cache_times = [] for i in range(10):     start = time.time()     response ...`

**Status**: Success (Attempt 5/5)

### Cell 638 ✅

**Preview**: `# Semantic caching test 8 cache_times = [] for i in range(10):     start = time.time()     response ...`

**Status**: Success (Attempt 5/5)

### Cell 640 ✅

**Preview**: `# Semantic caching test 9 cache_times = [] for i in range(10):     start = time.time()     response ...`

**Status**: Success (Attempt 5/5)

### Cell 642 ✅

**Preview**: `# Semantic caching test 10 cache_times = [] for i in range(10):     start = time.time()     response...`

**Status**: Success (Attempt 5/5)

### Cell 644 ✅

**Preview**: `# Semantic caching test 11 cache_times = [] for i in range(10):     start = time.time()     response...`

**Status**: Success (Attempt 5/5)

### Cell 646 ✅

**Preview**: `# Semantic caching test 12 cache_times = [] for i in range(10):     start = time.time()     response...`

**Status**: Success (Attempt 5/5)

### Cell 648 ✅

**Preview**: `# Semantic caching test 13 cache_times = [] for i in range(10):     start = time.time()     response...`

**Status**: Success (Attempt 5/5)

### Cell 650 ✅

**Preview**: `# Semantic caching test 14 cache_times = [] for i in range(10):     start = time.time()     response...`

**Status**: Success (Attempt 5/5)

### Cell 652 ✅

**Preview**: `# Semantic caching test 15 cache_times = [] for i in range(10):     start = time.time()     response...`

**Status**: Success (Attempt 5/5)

### Cell 654 ✅

**Preview**: `# Lab 21 final test 1 if {lab} == 22:     # Image generation test     print(f'Lab 21 Image Test 1: C...`

**Status**: Success (Attempt 5/5)

### Cell 656 ✅

**Preview**: `# Lab 21 final test 2 if {lab} == 22:     # Image generation test     print(f'Lab 21 Image Test 2: C...`

**Status**: Success (Attempt 5/5)

### Cell 658 ✅

**Preview**: `# Lab 21 final test 3 if {lab} == 22:     # Image generation test     print(f'Lab 21 Image Test 3: C...`

**Status**: Success (Attempt 5/5)

### Cell 660 ✅

**Preview**: `# Lab 21 final test 4 if {lab} == 22:     # Image generation test     print(f'Lab 21 Image Test 4: C...`

**Status**: Success (Attempt 5/5)

### Cell 662 ✅

**Preview**: `# Lab 21 final test 5 if {lab} == 22:     # Image generation test     print(f'Lab 21 Image Test 5: C...`

**Status**: Success (Attempt 5/5)

### Cell 664 ✅

**Preview**: `# Lab 21 final test 6 if {lab} == 22:     # Image generation test     print(f'Lab 21 Image Test 6: C...`

**Status**: Success (Attempt 5/5)

### Cell 666 ✅

**Preview**: `# Lab 21 final test 7 if {lab} == 22:     # Image generation test     print(f'Lab 21 Image Test 7: C...`

**Status**: Success (Attempt 5/5)

### Cell 668 ✅

**Preview**: `# Lab 21 final test 8 if {lab} == 22:     # Image generation test     print(f'Lab 21 Image Test 8: C...`

**Status**: Success (Attempt 5/5)

### Cell 670 ✅

**Preview**: `# Lab 21 final test 9 if {lab} == 22:     # Image generation test     print(f'Lab 21 Image Test 9: C...`

**Status**: Success (Attempt 5/5)

### Cell 672 ✅

**Preview**: `# Lab 21 final test 10 if {lab} == 22:     # Image generation test     print(f'Lab 21 Image Test 10:...`

**Status**: Success (Attempt 5/5)

### Cell 674 ✅

**Preview**: `# Lab 22 final test 1 if {lab} == 22:     # Image generation test     print(f'Lab 22 Image Test 1: C...`

**Status**: Success (Attempt 5/5)

### Cell 676 ✅

**Preview**: `# Lab 22 final test 2 if {lab} == 22:     # Image generation test     print(f'Lab 22 Image Test 2: C...`

**Status**: Success (Attempt 5/5)

### Cell 678 ✅

**Preview**: `# Lab 22 final test 3 if {lab} == 22:     # Image generation test     print(f'Lab 22 Image Test 3: C...`

**Status**: Success (Attempt 5/5)

### Cell 680 ✅

**Preview**: `# Lab 22 final test 4 if {lab} == 22:     # Image generation test     print(f'Lab 22 Image Test 4: C...`

**Status**: Success (Attempt 5/5)

### Cell 682 ✅

**Preview**: `# Lab 22 final test 5 if {lab} == 22:     # Image generation test     print(f'Lab 22 Image Test 5: C...`

**Status**: Success (Attempt 5/5)

### Cell 684 ✅

**Preview**: `# Lab 22 final test 6 if {lab} == 22:     # Image generation test     print(f'Lab 22 Image Test 6: C...`

**Status**: Success (Attempt 5/5)

### Cell 686 ✅

**Preview**: `# Lab 22 final test 7 if {lab} == 22:     # Image generation test     print(f'Lab 22 Image Test 7: C...`

**Status**: Success (Attempt 5/5)

### Cell 688 ✅

**Preview**: `# Lab 22 final test 8 if {lab} == 22:     # Image generation test     print(f'Lab 22 Image Test 8: C...`

**Status**: Success (Attempt 5/5)

### Cell 690 ✅

**Preview**: `# Lab 22 final test 9 if {lab} == 22:     # Image generation test     print(f'Lab 22 Image Test 9: C...`

**Status**: Success (Attempt 5/5)

### Cell 692 ✅

**Preview**: `# Lab 22 final test 10 if {lab} == 22:     # Image generation test     print(f'Lab 22 Image Test 10:...`

**Status**: Success (Attempt 5/5)

### Cell 694 ✅

**Preview**: `# Lab 23 final test 1 if {lab} == 22:     # Image generation test     print(f'Lab 23 Image Test 1: C...`

**Status**: Success (Attempt 5/5)

### Cell 696 ✅

**Preview**: `# Lab 23 final test 2 if {lab} == 22:     # Image generation test     print(f'Lab 23 Image Test 2: C...`

**Status**: Success (Attempt 5/5)

### Cell 698 ✅

**Preview**: `# Lab 23 final test 3 if {lab} == 22:     # Image generation test     print(f'Lab 23 Image Test 3: C...`

**Status**: Success (Attempt 5/5)

### Cell 700 ✅

**Preview**: `# Lab 23 final test 4 if {lab} == 22:     # Image generation test     print(f'Lab 23 Image Test 4: C...`

**Status**: Success (Attempt 5/5)

### Cell 702 ✅

**Preview**: `# Lab 23 final test 5 if {lab} == 22:     # Image generation test     print(f'Lab 23 Image Test 5: C...`

**Status**: Success (Attempt 5/5)

### Cell 704 ✅

**Preview**: `# Lab 23 final test 6 if {lab} == 22:     # Image generation test     print(f'Lab 23 Image Test 6: C...`

**Status**: Success (Attempt 5/5)

### Cell 706 ✅

**Preview**: `# Lab 23 final test 7 if {lab} == 22:     # Image generation test     print(f'Lab 23 Image Test 7: C...`

**Status**: Success (Attempt 5/5)

### Cell 708 ✅

**Preview**: `# Lab 23 final test 8 if {lab} == 22:     # Image generation test     print(f'Lab 23 Image Test 8: C...`

**Status**: Success (Attempt 5/5)

### Cell 710 ✅

**Preview**: `# Lab 23 final test 9 if {lab} == 22:     # Image generation test     print(f'Lab 23 Image Test 9: C...`

**Status**: Success (Attempt 5/5)

### Cell 712 ✅

**Preview**: `# Lab 23 final test 10 if {lab} == 22:     # Image generation test     print(f'Lab 23 Image Test 10:...`

**Status**: Success (Attempt 5/5)

### Cell 714 ✅

**Preview**: `# Lab 24 final test 1 if {lab} == 22:     # Image generation test     print(f'Lab 24 Image Test 1: C...`

**Status**: Success (Attempt 5/5)

### Cell 716 ✅

**Preview**: `# Lab 24 final test 2 if {lab} == 22:     # Image generation test     print(f'Lab 24 Image Test 2: C...`

**Status**: Success (Attempt 5/5)

### Cell 718 ✅

**Preview**: `# Lab 24 final test 3 if {lab} == 22:     # Image generation test     print(f'Lab 24 Image Test 3: C...`

**Status**: Success (Attempt 5/5)

### Cell 720 ✅

**Preview**: `# Lab 24 final test 4 if {lab} == 22:     # Image generation test     print(f'Lab 24 Image Test 4: C...`

**Status**: Success (Attempt 5/5)

### Cell 722 ✅

**Preview**: `# Lab 24 final test 5 if {lab} == 22:     # Image generation test     print(f'Lab 24 Image Test 5: C...`

**Status**: Success (Attempt 5/5)

### Cell 724 ✅

**Preview**: `# Lab 24 final test 6 if {lab} == 22:     # Image generation test     print(f'Lab 24 Image Test 6: C...`

**Status**: Success (Attempt 5/5)

### Cell 726 ✅

**Preview**: `# Lab 24 final test 7 if {lab} == 22:     # Image generation test     print(f'Lab 24 Image Test 7: C...`

**Status**: Success (Attempt 5/5)

### Cell 728 ✅

**Preview**: `# Lab 24 final test 8 if {lab} == 22:     # Image generation test     print(f'Lab 24 Image Test 8: C...`

**Status**: Success (Attempt 5/5)

### Cell 730 ✅

**Preview**: `# Lab 24 final test 9 if {lab} == 22:     # Image generation test     print(f'Lab 24 Image Test 9: C...`

**Status**: Success (Attempt 5/5)

### Cell 732 ✅

**Preview**: `# Lab 24 final test 10 if {lab} == 22:     # Image generation test     print(f'Lab 24 Image Test 10:...`

**Status**: Success (Attempt 5/5)

### Cell 734 ✅

**Preview**: `# Lab 25 final test 1 if {lab} == 22:     # Image generation test     print(f'Lab 25 Image Test 1: C...`

**Status**: Success (Attempt 5/5)

### Cell 736 ✅

**Preview**: `# Lab 25 final test 2 if {lab} == 22:     # Image generation test     print(f'Lab 25 Image Test 2: C...`

**Status**: Success (Attempt 5/5)

### Cell 738 ✅

**Preview**: `# Lab 25 final test 3 if {lab} == 22:     # Image generation test     print(f'Lab 25 Image Test 3: C...`

**Status**: Success (Attempt 5/5)

### Cell 740 ✅

**Preview**: `# Lab 25 final test 4 if {lab} == 22:     # Image generation test     print(f'Lab 25 Image Test 4: C...`

**Status**: Success (Attempt 5/5)

### Cell 742 ✅

**Preview**: `# Lab 25 final test 5 if {lab} == 22:     # Image generation test     print(f'Lab 25 Image Test 5: C...`

**Status**: Success (Attempt 5/5)

### Cell 744 ✅

**Preview**: `# Lab 25 final test 6 if {lab} == 22:     # Image generation test     print(f'Lab 25 Image Test 6: C...`

**Status**: Success (Attempt 5/5)

### Cell 746 ✅

**Preview**: `# Lab 25 final test 7 if {lab} == 22:     # Image generation test     print(f'Lab 25 Image Test 7: C...`

**Status**: Success (Attempt 5/5)

### Cell 748 ✅

**Preview**: `# Lab 25 final test 8 if {lab} == 22:     # Image generation test     print(f'Lab 25 Image Test 8: C...`

**Status**: Success (Attempt 5/5)

### Cell 750 ✅

**Preview**: `# Lab 25 final test 9 if {lab} == 22:     # Image generation test     print(f'Lab 25 Image Test 9: C...`

**Status**: Success (Attempt 5/5)

### Cell 752 ✅

**Preview**: `# Lab 25 final test 10 if {lab} == 22:     # Image generation test     print(f'Lab 25 Image Test 10:...`

**Status**: Success (Attempt 5/5)

### Cell 754 ✅

**Preview**: `# Performance benchmark 1 times = [] for i in range(20):     start = time.time()     response = clie...`

**Status**: Success (Attempt 5/5)

### Cell 756 ✅

**Preview**: `# Performance benchmark 2 times = [] for i in range(20):     start = time.time()     response = clie...`

**Status**: Success (Attempt 5/5)

### Cell 758 ✅

**Preview**: `# Performance benchmark 3 times = [] for i in range(20):     start = time.time()     response = clie...`

**Status**: Success (Attempt 5/5)

### Cell 760 ✅

**Preview**: `# Performance benchmark 4 times = [] for i in range(20):     start = time.time()     response = clie...`

**Status**: Success (Attempt 5/5)

### Cell 762 ✅

**Preview**: `# Performance benchmark 5 times = [] for i in range(20):     start = time.time()     response = clie...`

**Status**: Success (Attempt 5/5)

### Cell 764 ✅

**Preview**: `# Performance benchmark 6 times = [] for i in range(20):     start = time.time()     response = clie...`

**Status**: Success (Attempt 5/5)

### Cell 766 ✅

**Preview**: `# Performance benchmark 7 times = [] for i in range(20):     start = time.time()     response = clie...`

**Status**: Success (Attempt 5/5)

### Cell 768 ✅

**Preview**: `# Performance benchmark 8 times = [] for i in range(20):     start = time.time()     response = clie...`

**Status**: Success (Attempt 5/5)

### Cell 770 ✅

**Preview**: `# Performance benchmark 9 times = [] for i in range(20):     start = time.time()     response = clie...`

**Status**: Success (Attempt 5/5)

### Cell 772 ✅

**Preview**: `# Performance benchmark 10 times = [] for i in range(20):     start = time.time()     response = cli...`

**Status**: Success (Attempt 5/5)

### Cell 774 ✅

**Preview**: `# Stress test 1 print(f'Running stress test {stress}...') for i in range(30):     response = client....`

**Status**: Success (Attempt 5/5)

### Cell 776 ✅

**Preview**: `# Stress test 2 print(f'Running stress test {stress}...') for i in range(30):     response = client....`

**Status**: Success (Attempt 5/5)

### Cell 778 ✅

**Preview**: `# Stress test 3 print(f'Running stress test {stress}...') for i in range(30):     response = client....`

**Status**: Success (Attempt 5/5)

### Cell 780 ✅

**Preview**: `# Stress test 4 print(f'Running stress test {stress}...') for i in range(30):     response = client....`

**Status**: Success (Attempt 5/5)

### Cell 782 ✅

**Preview**: `# Stress test 5 print(f'Running stress test {stress}...') for i in range(30):     response = client....`

**Status**: Success (Attempt 5/5)

### Cell 784 ✅

**Preview**: `# Stress test 6 print(f'Running stress test {stress}...') for i in range(30):     response = client....`

**Status**: Success (Attempt 5/5)

### Cell 786 ✅

**Preview**: `# Stress test 7 print(f'Running stress test {stress}...') for i in range(30):     response = client....`

**Status**: Success (Attempt 5/5)

### Cell 788 ✅

**Preview**: `# Stress test 8 print(f'Running stress test {stress}...') for i in range(30):     response = client....`

**Status**: Success (Attempt 5/5)

### Cell 790 ✅

**Preview**: `# Stress test 9 print(f'Running stress test {stress}...') for i in range(30):     response = client....`

**Status**: Success (Attempt 5/5)

### Cell 792 ✅

**Preview**: `# Stress test 10 print(f'Running stress test {stress}...') for i in range(30):     response = client...`

**Status**: Success (Attempt 5/5)

### Cell 794 ✅

**Preview**: `# SDK Fallback: Install required Azure SDK packages (identity + resource mgmt) import sys, subproces...`

**Status**: Success (Attempt 1/5)

### Cell 795 ✅

**Preview**: `# SDK Fallback: Provider registration + What-If via Azure SDK (bypasses az CLI MSAL issue) import os...`

**Status**: Success (Attempt 5/5)

### Cell 796 ✅

**Preview**: `# Deployment Operations Inspector: derive subscription id, list operations, summarize failures impor...`

**Status**: Success (Attempt 1/5)

### Cell 797 ✅

**Preview**: `# Set Subscription ID Environment Variable (Auto-Injected from Cell 10) import os, json, re, pathlib...`

**Status**: Success (Attempt 1/5)

### Cell 798 ✅

**Preview**: `# Azure CLI Health Check & Repair Suggestions import subprocess, shutil, os  az_bin = shutil.which("...`

**Status**: Success (Attempt 1/5)

### Cell 799 ✅

**Preview**: `# Staged Deployment Utility (SDK) - filter resource types and deploy incrementally import os, json, ...`

**Status**: Success (Attempt 5/5)

### Cell 800 ✅

**Preview**: ``

**Status**: Success (Attempt 1/5)

### Cell 801 ✅

**Preview**: `import os, pathlib TENANT_ID = "2b9d9f47-1fb6-400a-a438-39fe7d768649" os.environ["AZURE_TENANT_ID"] ...`

**Status**: Success (Attempt 1/5)

### Cell 802 ✅

**Preview**: `# Deployment Operations Fetch (Latest or Specific Stage) """ Fetches and summarizes deployment opera...`

**Status**: Success (Attempt 5/5)

### Cell 803 ✅

**Preview**: `# Improved MCP initialization & diagnostics (override previous definitions) import os, time, socket,...`

**Status**: Success (Attempt 1/5)

### Cell 804 ✅

**Preview**: `# Improved MCP initialization v2 (expanded patterns & robust search) import os, time, socket, reques...`

**Status**: Success (Attempt 1/5)

### Cell 805 ✅

**Preview**: `# Weather MCP disconnect logic fix # Adds safe disconnect handling so a success message only appears...`

**Status**: Success (Attempt 1/5)

### Cell 806 ❌

**Preview**: `await safe_weather_forecast("London") # or await weather_demo("Seattle")`

**Status**: Failed (All 5 attempts failed)

**Errors**:
- Attempt 1: `SyntaxError` - 'await' outside function (<string>, line 1)
- Attempt 2: `SyntaxError` - 'await' outside function (<string>, line 1)
- Attempt 3: `SyntaxError` - 'await' outside function (<string>, line 1)
- Attempt 4: `SyntaxError` - 'await' outside function (<string>, line 1)
- Attempt 5: `SyntaxError` - 'await' outside function (<string>, line 2)

### Cell 807 ✅

**Preview**: ``

**Status**: Success (Attempt 1/5)


---

## 🔍 Common Issues Found

No major issues detected! 🎉

---

## 🎯 Next Steps

### Priority Fixes:

1. **SyntaxError** (Cells: 53, 55, 56, 57, 58, 59, 61, 63, 65, 67, 69, 73, 75, 79, 81, 83, 85, 91, 92, 93, 120, 132, 142, 806)
   - Review and fix 24 cells with this error

### Recommendations:

1. Review error patterns above
2. Focus on most common error types first
3. Check MCP server availability for AttributeErrors
4. Verify all required data files exist
5. Consider increasing timeouts for slow operations
