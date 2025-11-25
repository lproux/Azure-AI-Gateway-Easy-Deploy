#!/usr/bin/env python3
"""
Test that notebook_mcp_helpers.py can be imported and has weather attribute
"""
import sys
sys.path.insert(0, '.')

print("=" * 70)
print("🧪 Testing MCP Helper Import")
print("=" * 70)
print()

try:
    from notebook_mcp_helpers import MCPClient, MCPError
    print("✅ Successfully imported MCPClient and MCPError")
except Exception as e:
    print(f"❌ Failed to import: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print()
print("🔍 Creating MCPClient instance...")
try:
    mcp = MCPClient()
    print("✅ MCPClient created successfully")
except Exception as e:
    print(f"❌ Failed to create MCPClient: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print()
print("🔍 Checking MCP server attributes...")
attributes = ['excel', 'docs', 'weather']
for attr in attributes:
    if hasattr(mcp, attr):
        server = getattr(mcp, attr)
        print(f"✅ mcp.{attr} exists: {server.server_url}")
    else:
        print(f"❌ mcp.{attr} is MISSING!")
        exit(1)

print()
print("🔍 Checking Weather MCP methods...")
weather_methods = ['get_cities', 'get_weather']
for method in weather_methods:
    if hasattr(mcp.weather, method):
        print(f"✅ mcp.weather.{method}() exists")
    else:
        print(f"❌ mcp.weather.{method}() is MISSING!")
        exit(1)

print()
print("=" * 70)
print("✅ All checks passed! MCP Client is ready.")
print("=" * 70)
print()
print("📝 Summary:")
print("   - MCPClient can be imported ✓")
print("   - All 3 server attributes exist (excel, docs, weather) ✓")
print("   - Weather MCP has both tools (get_cities, get_weather) ✓")
print()
print("🔄 You can now re-run Cell 2 in the notebook!")
