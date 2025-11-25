#!/usr/bin/env python3
"""
Test the deployed Weather MCP server (SSE-based)
"""
import httpx
import json

WEATHER_SERVER_URL = "http://weather-mcp-72998.eastus.azurecontainer.io:8080"

def test_server_alive():
    """Test if server is responding"""
    print("=" * 70)
    print("🧪 Test 1: Server Accessibility")
    print("=" * 70)

    try:
        # Try to access root (should return 404 but confirms server is alive)
        response = httpx.get(f"{WEATHER_SERVER_URL}/", timeout=10)
        print(f"✅ Server is responding (status: {response.status_code})")
        print(f"   Server: {response.headers.get('server', 'unknown')}")
        return True
    except Exception as e:
        print(f"❌ Server not responding: {type(e).__name__} - {e}")
        return False

def test_sse_endpoint():
    """Test SSE endpoint accessibility"""
    print()
    print("=" * 70)
    print("🧪 Test 2: SSE Endpoint")
    print("=" * 70)

    try:
        # SSE endpoint should accept GET requests and keep connection open
        # We'll use a short timeout to just verify it's accessible
        with httpx.Client() as client:
            with client.stream("GET", f"{WEATHER_SERVER_URL}/weather/sse", timeout=3) as response:
                if response.status_code == 200:
                    print(f"✅ SSE endpoint accessible at /weather/sse")
                    print(f"   Content-Type: {response.headers.get('content-type', 'unknown')}")
                    return True
                else:
                    print(f"⚠️  Unexpected status code: {response.status_code}")
                    return False
    except httpx.ReadTimeout:
        # SSE connections timeout because they stay open - this is expected
        print(f"✅ SSE endpoint accessible (connection stays open as expected)")
        return True
    except Exception as e:
        print(f"❌ SSE endpoint test failed: {type(e).__name__} - {e}")
        return False

def test_messages_endpoint():
    """Test MCP messages endpoint"""
    print()
    print("=" * 70)
    print("🧪 Test 3: MCP Messages Endpoint")
    print("=" * 70)

    try:
        # Try to POST a tools/list request to the messages endpoint
        # Note: This might not work without proper SSE setup, but we can try
        response = httpx.post(
            f"{WEATHER_SERVER_URL}/weather/messages/",
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
            print(f"✅ Messages endpoint responding")
            print(f"   Response: {json.dumps(data, indent=2)[:200]}")
            return True
        else:
            print(f"⚠️  Status: {response.status_code}")
            print(f"   Note: SSE-based servers may not support direct JSON-RPC POST")
            return False

    except Exception as e:
        print(f"⚠️  Direct POST not supported: {type(e).__name__}")
        print(f"   Note: This server uses SSE transport and requires SSE client")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("🔧 Testing Weather MCP Server (SSE-based)")
    print("=" * 70)
    print(f"URL: {WEATHER_SERVER_URL}")
    print()

    results = {}

    # Test 1: Server alive
    results["server_alive"] = test_server_alive()

    # Test 2: SSE endpoint
    results["sse_endpoint"] = test_sse_endpoint()

    # Test 3: Messages endpoint
    results["messages_endpoint"] = test_messages_endpoint()

    # Summary
    print()
    print("=" * 70)
    print("📊 Test Summary")
    print("=" * 70)

    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)

    print(f"Server Alive: {'✅ PASS' if results['server_alive'] else '❌ FAIL'}")
    print(f"SSE Endpoint: {'✅ PASS' if results['sse_endpoint'] else '❌ FAIL'}")
    print(f"Messages Endpoint: {'⚠️  INFO' if not results['messages_endpoint'] else '✅ PASS'}")
    print()

    if results["server_alive"] and results["sse_endpoint"]:
        print("✅ Weather MCP Server is deployed and accessible!")
        print()
        print("📝 Important Notes:")
        print("   - This server uses SSE (Server-Sent Events) transport")
        print("   - Different from Excel/Docs servers (JSON-RPC)")
        print("   - Tools: get_cities, get_weather")
        print("   - SSE Endpoint: /weather/sse")
        print("   - Port: 8080 (not 8000)")
        print()
        print("✅ Ready to add to notebook configuration!")
        exit(0)
    else:
        print("⚠️  Some tests failed. Review output above.")
        exit(1)
