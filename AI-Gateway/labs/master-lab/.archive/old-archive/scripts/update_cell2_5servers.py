#!/usr/bin/env python3
"""Update Cell 2 to initialize all 5 MCP servers"""
import json

NOTEBOOK_PATH = "master-ai-gateway.ipynb"

print("=" * 80)
print("🔧 Updating Cell 2 - Initialize All 5 MCP Servers")
print("=" * 80)
print()

# Load notebook
with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# New Cell 2 source
new_source = """# Cell 2: MCP Client Initialization (Updated for 5 Real Servers)
import sys
sys.path.append('.')

from notebook_mcp_helpers import MCPClient, MCPError

# Check if already initialized with ALL 5 servers (prevent re-initialization)
if 'mcp' in globals() and hasattr(mcp, 'excel') and hasattr(mcp, 'docs') and hasattr(mcp, 'weather') and hasattr(mcp, 'oncall') and hasattr(mcp, 'spotify'):
    print("⚠️  MCP Client already initialized with all 5 servers. Skipping re-initialization.")
    print(f"   Excel MCP: {mcp.excel.server_url}")
    print(f"   Docs MCP: {mcp.docs.server_url}")
    print(f"   Weather MCP: {mcp.weather.server_url}")
    print(f"   OnCall MCP: {mcp.oncall.server_url}")
    print(f"   Spotify MCP: {mcp.spotify.server_url}")
else:
    if 'mcp' in globals():
        print("🔄 MCP Client needs update (adding OnCall & Spotify MCPs)...")
        del mcp  # Delete old instance
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
        print(f"   4. OnCall: {mcp.oncall.server_url}")
        print(f"   5. Spotify: {mcp.spotify.server_url}")
        print()
        print(f"💡 Note: 5 real MCP servers are deployed.")
        print(f"   - Excel & Docs: JSON-RPC on port 8000")
        print(f"   - Weather, OnCall & Spotify: SSE transport on port 8080")
    except Exception as e:
        print(f"❌ Failed to initialize MCP Client: {e}")
        import traceback
        traceback.print_exc()
        raise
"""

# Update Cell 2
nb['cells'][2]['source'] = new_source.splitlines(keepends=True)

# Save notebook
with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("✅ Updated Cell 2 to initialize 5 MCP servers")
print()
print("Changes:")
print("   - Now checks for 5 servers: excel, docs, weather, oncall, spotify")
print("   - Added OnCall MCP URL display")
print("   - Added Spotify MCP URL display")
print("   - Updated server count: 3 → 5")
print()
print("=" * 80)
print("✅ Cell 2 update complete!")
print("=" * 80)
