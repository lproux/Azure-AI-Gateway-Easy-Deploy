#!/usr/bin/env python3
"""Test OnCall and Spotify MCP servers"""
import httpx

servers = [
    ("OnCall", "http://oncall-mcp-72998.eastus.azurecontainer.io:8080"),
    ("Spotify", "http://spotify-mcp-72998.eastus.azurecontainer.io:8080")
]

print("=" * 70)
print("Testing New MCP Servers")
print("=" * 70)
print()

for name, url in servers:
    print(f"Testing {name} MCP...")
    print(f"  URL: {url}")
    
    # Test root endpoint
    try:
        response = httpx.get(f"{url}/", timeout=10)
        print(f"  Root: HTTP {response.status_code}")
    except Exception as e:
        print(f"  Root: {type(e).__name__}")
    
    # Test SSE endpoint (these are SSE-based servers)
    try:
        response = httpx.get(f"{url}/sse", timeout=3)
        print(f"  SSE: HTTP {response.status_code}")
    except httpx.ReadTimeout:
        print(f"  SSE: ✅ Accessible (connection stays open)")
    except Exception as e:
        print(f"  SSE: {type(e).__name__}")
    
    print()

print("=" * 70)
print("✅ Test complete")
print("=" * 70)
