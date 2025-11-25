#!/usr/bin/env python3
"""
Update Cell 2 in master-ai-gateway.ipynb to include Weather MCP
"""
import json

NOTEBOOK_PATH = "master-ai-gateway.ipynb"

# New Cell 2 content with 3 deployed servers (Excel, Docs, Weather)
CELL_2_SOURCE = """# Cell 2: MCP Client Initialization (Updated for 3 Real Servers: Excel, Docs, Weather)
import sys
sys.path.append('.')

from notebook_mcp_helpers import MCPClient, MCPError

# Check if already initialized (prevent re-initialization)
if 'mcp' in globals() and hasattr(mcp, 'excel'):
    print("⚠️  MCP Client already initialized. Skipping re-initialization.")
    print(f"   Excel MCP: {mcp.excel.server_url}")
    print(f"   Docs MCP: {mcp.docs.server_url}")
    print(f"   Weather MCP: {mcp.weather.server_url}")
else:
    print("🔄 Initializing MCP Client...")
    try:
        mcp = MCPClient()
        print("✅ MCP Client initialized successfully!")
        print()
        print(f"📡 Deployed MCP Servers:")
        print(f"   1. Excel Analytics: {mcp.excel.server_url}")
        print(f"   2. Research Documents: {mcp.docs.server_url}")
        print(f"   3. Weather: {mcp.weather.server_url}")
        print()
        print(f"💡 Note: 3 real MCP servers are deployed.")
        print(f"   - Excel & Docs: JSON-RPC on port 8000")
        print(f"   - Weather: SSE transport on port 8080")
    except Exception as e:
        print(f"❌ Failed to initialize MCP Client: {e}")
        raise
"""

# Load notebook
with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Update Cell 2 (index 2 since cells are 0-indexed)
if len(nb['cells']) > 2:
    nb['cells'][2]['source'] = CELL_2_SOURCE.splitlines(keepends=True)
    print(f"✅ Updated Cell 2 in {NOTEBOOK_PATH}")
else:
    print(f"⚠️  Notebook has fewer than 3 cells, cannot update Cell 2")
    exit(1)

# Save notebook
with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"✅ Notebook saved successfully!")
print()
print(f"📝 Updated Cell 2 to show 3 deployed servers:")
print(f"   - Excel MCP (JSON-RPC, port 8000)")
print(f"   - Docs MCP (JSON-RPC, port 8000)")
print(f"   - Weather MCP (SSE transport, port 8080)")
