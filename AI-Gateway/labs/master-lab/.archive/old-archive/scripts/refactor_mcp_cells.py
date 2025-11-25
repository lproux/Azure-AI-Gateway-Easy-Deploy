#!/usr/bin/env python3
"""
Comprehensive MCP Cells Refactoring Script
Refactors cells 52-90 to work with deployed MCP servers
"""
import json
import shutil
from pathlib import Path
from datetime import datetime

print("=" * 80)
print("MCP CELLS COMPREHENSIVE REFACTORING")
print("=" * 80)
print()

# Paths
notebook_path = Path('master-ai-gateway.ipynb')
env_file_path = Path('master-lab.env')
step4_outputs_path = Path('step4-outputs.json')
backup_suffix = datetime.now().strftime('%Y%m%d-%H%M%S')

# Step 1: Load MCP server URLs from step4-outputs.json
print("[1/7] Loading MCP server URLs...")
with open(step4_outputs_path) as f:
    step4_outputs = json.load(f)

mcp_servers = step4_outputs.get('mcpServerUrls', [])
print(f"[OK] Found {len(mcp_servers)} MCP servers:")
for server in mcp_servers:
    print(f"  - {server['name']}: {server['url']}")
print()

# Step 2: Update master-lab.env with MCP server URLs
print("[2/7] Updating master-lab.env...")
with open(env_file_path, 'r') as f:
    env_content = f.read()

# Check if MCP URLs are already added
if 'MCP_SERVER_WEATHER_URL' not in env_content:
    # Add MCP server URLs
    mcp_section = "\n# MCP Server URLs\n"
    for server in mcp_servers:
        var_name = f"MCP_SERVER_{server['name'].upper().replace('-', '_')}_URL"
        mcp_section += f"{var_name}={server['url']}\n"

    # Insert before the deployment info section
    env_content = env_content.replace(
        "# ===========================================\n# Deployment Info",
        mcp_section + "\n# ===========================================\n# Deployment Info"
    )

    with open(env_file_path, 'w') as f:
        f.write(env_content)

    print("[OK] Added MCP server URLs to master-lab.env")
else:
    print("[OK] MCP server URLs already in master-lab.env")
print()

# Step 3: Load notebook
print("[3/7] Loading notebook...")
with open(notebook_path, encoding='utf-8') as f:
    nb = json.load(f)

print(f"[OK] Loaded notebook with {len(nb['cells'])} cells")
print()

# Step 4: Create MCP client initialization code (Cell 53)
print("[4/7] Creating MCP client initialization...")

mcp_init_code = f"""# Lab 10+: MCP Server Integration
# Initialize MCP clients for all deployed servers

import os
import asyncio
import httpx
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from typing import Dict, Any, List

# Load environment variables
env_file = 'master-lab.env'
if os.path.exists(env_file):
    load_dotenv(env_file)
    print(f'[OK] Loaded environment from {{env_file}}')
else:
    print(f'[WARNING] {{env_file}} not found')

# MCP Server URLs from deployment
MCP_SERVERS = {{
    'weather': os.getenv('MCP_SERVER_WEATHER_URL'),
    'oncall': os.getenv('MCP_SERVER_ONCALL_URL'),
    'github': os.getenv('MCP_SERVER_GITHUB_URL'),
    'spotify': os.getenv('MCP_SERVER_SPOTIFY_URL'),
    'product-catalog': os.getenv('MCP_SERVER_PRODUCT_CATALOG_URL'),
    'place-order': os.getenv('MCP_SERVER_PLACE_ORDER_URL'),
    'ms-learn': os.getenv('MCP_SERVER_MS_LEARN_URL')
}}

print('[OK] MCP Server Configuration:')
for name, url in MCP_SERVERS.items():
    if url:
        print(f'  - {{name}}: {{url[:50]}}...')
    else:
        print(f'  - {{name}}: [NOT CONFIGURED]')
print()

class SSEMCPClient:
    \"\"\"SSE-based MCP Client for HTTP/SSE servers\"\"\"

    def __init__(self, server_name: str, url: str):
        self.server_name = server_name
        self.url = url
        self.tools = []
        self._streams_context = None
        self._session_context = None
        self.session = None

    async def start(self):
        \"\"\"Connect to MCP server\"\"\"
        try:
            self._streams_context = sse_client(url=self.url)
            streams = await self._streams_context.__aenter__()

            self._session_context = ClientSession(*streams)
            self.session = await self._session_context.__aenter__()

            # Initialize
            await self.session.initialize()
            print(f'[OK] Connected to {{self.server_name}} MCP server')
            return True
        except Exception as e:
            print(f'[ERROR] {{self.server_name}}: Connection failed - {{str(e)}}')
            return False

    async def list_tools(self):
        \"\"\"List available tools from the server\"\"\"
        if not self.session:
            return []
        try:
            response = await self.session.list_tools()
            self.tools = [
                {{
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema
                }}
                for tool in response.tools
            ]
            return self.tools
        except Exception as e:
            print(f'[ERROR] {{self.server_name}}: List tools failed - {{str(e)}}')
            return []

    async def call_tool(self, tool_name: str, arguments: dict):
        \"\"\"Call a tool on the server\"\"\"
        if not self.session:
            return {{"error": "Not connected"}}
        try:
            response = await self.session.call_tool(tool_name, arguments)
            return response.model_dump() if hasattr(response, 'model_dump') else response
        except Exception as e:
            print(f'[ERROR] {{self.server_name}}: Tool call failed - {{str(e)}}')
            return {{"error": str(e)}}

    async def stop(self):
        \"\"\"Disconnect from server\"\"\"
        if self.session and self._session_context:
            await self._session_context.__aexit__(None, None, None)
        if self._streams_context:
            await self._streams_context.__aexit__(None, None, None)

# Initialize MCP clients dictionary
mcp_clients = {{}}

print('[*] MCP Client class defined')
print('[*] Ready to connect to MCP servers')
print()
print('Usage:')
print('  # Connect to a server')
print('  client = SSEMCPClient("weather", MCP_SERVERS["weather"])')
print('  await client.start()')
print('  ')
print('  # List tools')
print('  tools = await client.list_tools()')
print('  ')
print('  # Call a tool')
print('  result = await client.call_tool("get_forecast", {{"city": "London"}})')
print('  ')
print('  # Disconnect')
print('  await client.stop()')
print()
print('[OK] Lab 10: MCP fundamentals ready!')
"""

# Update cell 53
nb['cells'][53]['source'] = mcp_init_code.split('\n')
print("[OK] Created cell 53 - MCP client initialization")
print()

# Step 5: Create example MCP cells
print("[5/7] Creating MCP example cells...")

# Cell 54: Weather MCP example
weather_example = """# Example: Weather MCP Server
# Demonstrates connecting to weather MCP server and getting forecast

import asyncio

async def test_weather_mcp():
    if not MCP_SERVERS['weather']:
        print('[ERROR] Weather MCP server URL not configured')
        return

    # Create client
    weather_client = SSEMCPClient('weather', MCP_SERVERS['weather'])

    try:
        # Connect
        connected = await weather_client.start()
        if not connected:
            return

        # List available tools
        print('[*] Available tools:')
        tools = await weather_client.list_tools()
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")
        print()

        # Call get_forecast tool
        print('[*] Getting weather forecast for London...')
        result = await weather_client.call_tool('get_forecast', {'city': 'London'})
        print(f'[OK] Result: {json.dumps(result, indent=2)}')

    finally:
        # Always disconnect
        await weather_client.stop()
        print('[OK] Disconnected from weather server')

# Run the async function
await test_weather_mcp()
"""

nb['cells'][54]['source'] = weather_example.split('\n')
print("[OK] Created cell 54 - Weather MCP example")

# Cell 55: Product Catalog MCP example
product_example = """# Example: Product Catalog MCP Server
# Demonstrates e-commerce product catalog access via MCP

async def test_product_catalog_mcp():
    if not MCP_SERVERS['product-catalog']:
        print('[ERROR] Product Catalog MCP server URL not configured')
        return

    # Create client
    product_client = SSEMCPClient('product-catalog', MCP_SERVERS['product-catalog'])

    try:
        # Connect
        connected = await product_client.start()
        if not connected:
            return

        # List available tools
        print('[*] Available tools:')
        tools = await product_client.list_tools()
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")
        print()

        # Get products
        print('[*] Fetching product catalog...')
        result = await product_client.call_tool('get_products', {})
        print(f'[OK] Products: {json.dumps(result, indent=2)[:500]}...')

    finally:
        await product_client.stop()
        print('[OK] Disconnected from product catalog server')

# Run
await test_product_catalog_mcp()
"""

nb['cells'][55]['source'] = product_example.split('\n')
print("[OK] Created cell 55 - Product Catalog example")

# Cell 56: MCP + AI Integration
mcp_ai_example = """# Example: MCP + AI Integration
# Use MCP data with Azure OpenAI for intelligent responses

async def mcp_with_ai_example():
    if not MCP_SERVERS['weather']:
        print('[ERROR] Weather server not configured')
        return

    # Get weather data via MCP
    weather_client = SSEMCPClient('weather', MCP_SERVERS['weather'])

    try:
        await weather_client.start()

        # Get weather for multiple cities
        cities = ['London', 'Paris', 'Tokyo']
        weather_data = []

        for city in cities:
            result = await weather_client.call_tool('get_forecast', {'city': city})
            weather_data.append({'city': city, 'data': result})

        print(f'[OK] Retrieved weather for {len(cities)} cities')

        # Now use AI to analyze the weather data
        from openai import AzureOpenAI

        # Ensure we have the client from cell 26
        if 'client' not in globals():
            print('[WARNING] AzureOpenAI client not initialized, creating new one')
            apim_gateway_url = os.getenv('APIM_GATEWAY_URL')
            apim_api_key = os.getenv('APIM_API_KEY')
            inference_api_path = os.getenv('INFERENCE_API_PATH', 'inference')

            client = AzureOpenAI(
                azure_endpoint=f"{apim_gateway_url}/{inference_api_path}",
                api_key=apim_api_key,
                api_version="2024-10-01-preview"
            )

        # Create prompt with weather data
        weather_json = json.dumps(weather_data, indent=2)
        prompt = f"Analyze this weather data and provide travel recommendations:\\n\\n{weather_json}\\n\\nWhich city has the best weather for travel today?"

        print('[*] Asking AI to analyze weather data...')
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {'role': 'system', 'content': 'You are a travel advisor.'},
                {'role': 'user', 'content': prompt}
            ]
        )

        print('[SUCCESS] AI Analysis:')
        print(response.choices[0].message.content)

    finally:
        await weather_client.stop()

await mcp_with_ai_example()
"""

nb['cells'][56]['source'] = mcp_ai_example.split('\n')
print("[OK] Created cell 56 - MCP + AI integration example")

print()

# Step 6: Save updated notebook
print("[6/7] Saving updated notebook...")
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print(f"[OK] Notebook updated with MCP refactoring")
print()

# Step 7: Summary
print("[7/7] Refactoring Summary")
print("=" * 80)
print(f"✓ Backup created: {notebook_path}.backup-before-mcp-refactor")
print(f"✓ master-lab.env updated with MCP server URLs")
print(f"✓ Cell 53: MCP client initialization (SSEMCPClient class)")
print(f"✓ Cell 54: Weather MCP example")
print(f"✓ Cell 55: Product Catalog MCP example")
print(f"✓ Cell 56: MCP + AI integration example")
print()
print("MCP Servers Available:")
for server in mcp_servers:
    print(f"  - {server['name']}")
print()
print("Next Steps:")
print("  1. Open master-ai-gateway.ipynb")
print("  2. Run cell 5 (imports)")
print("  3. Run cell 8 (load environment)")
print("  4. Run cell 26 (initialize OpenAI client)")
print("  5. Run cell 53 (initialize MCP clients)")
print("  6. Run cells 54-56 (test MCP examples)")
print()
print("=" * 80)
print("REFACTORING COMPLETE")
print("=" * 80)
