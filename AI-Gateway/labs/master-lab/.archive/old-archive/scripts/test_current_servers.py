#!/usr/bin/env python3
"""
Independent test of the 2 deployed MCP servers (Excel + Docs)
"""
import httpx
import json

SERVERS = {
    "Excel MCP": "http://excel-mcp-72998.eastus.azurecontainer.io:8000",
    "Docs MCP": "http://docs-mcp-72998.eastus.azurecontainer.io:8000"
}

def test_health(name, url):
    """Test health endpoint"""
    try:
        response = httpx.get(f"{url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {name}: Healthy")
            print(f"   Service: {data.get('service', 'N/A')}")
            print(f"   Version: {data.get('version', 'N/A')}")
            if 'documents_available' in data:
                print(f"   Documents: {data['documents_available']}")
            return True
        else:
            print(f"❌ {name}: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {name}: {type(e).__name__} - {e}")
        return False

def test_mcp_tools_list(name, url):
    """Test MCP tools/list endpoint"""
    try:
        response = httpx.post(
            f"{url}/mcp/",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            },
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if 'result' in data and 'tools' in data['result']:
                tools = data['result']['tools']
                print(f"✅ {name}: {len(tools)} tools available")
                for tool in tools[:3]:  # Show first 3
                    print(f"   - {tool.get('name', 'unknown')}")
                if len(tools) > 3:
                    print(f"   ... and {len(tools) - 3} more")
                return True
        print(f"⚠️  {name}: Unexpected response format")
        return False
    except Exception as e:
        print(f"❌ {name}: {type(e).__name__} - {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("🧪 Testing Deployed MCP Servers")
    print("=" * 70)
    print()
    
    results = {"health": {}, "tools": {}}
    
    # Test 1: Health checks
    print("📡 Test 1: Health Endpoints")
    print("-" * 70)
    for name, url in SERVERS.items():
        results["health"][name] = test_health(name, url)
    print()
    
    # Test 2: MCP tools/list
    print("🔧 Test 2: MCP Tools List")
    print("-" * 70)
    for name, url in SERVERS.items():
        results["tools"][name] = test_mcp_tools_list(name, url)
    print()
    
    # Summary
    print("=" * 70)
    print("📊 Test Summary")
    print("=" * 70)
    health_pass = sum(results["health"].values())
    tools_pass = sum(results["tools"].values())
    total = len(SERVERS)
    
    print(f"Health Checks: {health_pass}/{total} passed")
    print(f"Tools List: {tools_pass}/{total} passed")
    print()
    
    if health_pass == total and tools_pass == total:
        print("✅ All tests passed! Servers are ready.")
        exit(0)
    else:
        print("⚠️  Some tests failed. Review output above.")
        exit(1)
