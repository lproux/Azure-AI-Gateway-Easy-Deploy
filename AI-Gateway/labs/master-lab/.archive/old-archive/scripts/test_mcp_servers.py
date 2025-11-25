"""
Test all MCP servers independently
This script tests each MCP server defined in master-lab.env
and reports on their status, errors, and response times.
"""

import os
import sys
import time
import urllib.request
import urllib.error
import socket
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_file = Path(__file__).parent / "master-lab.env"
load_dotenv(env_file)

# MCP Server definitions
MCP_SERVERS = {
    "WEATHER": os.getenv("MCP_SERVER_WEATHER_URL"),
    "ONCALL": os.getenv("MCP_SERVER_ONCALL_URL"),
    "GITHUB": os.getenv("MCP_SERVER_GITHUB_URL"),
    "SPOTIFY": os.getenv("MCP_SERVER_SPOTIFY_URL"),
    "PRODUCT_CATALOG": os.getenv("MCP_SERVER_PRODUCT_CATALOG_URL"),
    "PLACE_ORDER": os.getenv("MCP_SERVER_PLACE_ORDER_URL"),
    "MS_LEARN": os.getenv("MCP_SERVER_MS_LEARN_URL"),
}

def classify_exception(e: Exception) -> str:
    """Classify exception types for better error reporting"""
    if isinstance(e, urllib.error.HTTPError):
        return f'http-status:{e.code}'
    if isinstance(e, urllib.error.URLError):
        if isinstance(getattr(e, 'reason', None), socket.timeout):
            return 'timeout'
        if isinstance(getattr(e, 'reason', None), socket.gaierror):
            return 'dns-error'
        return 'connection-error'
    if isinstance(e, socket.timeout):
        return 'timeout'
    if isinstance(e, socket.gaierror):
        return 'dns-error'
    return f'unexpected:{type(e).__name__}'

def test_server(name: str, url: str, timeout: float = 5.0) -> dict:
    """Test a single MCP server"""
    if not url:
        return {
            "name": name,
            "url": url,
            "status": "MISSING",
            "error": "URL not configured",
            "latency_ms": None,
            "category": "config-error"
        }

    start_time = time.time()
    try:
        # Test basic connectivity
        req = urllib.request.Request(url, method='GET')
        with urllib.request.urlopen(req, timeout=timeout) as response:
            latency_ms = (time.time() - start_time) * 1000
            status_code = response.getcode()
            return {
                "name": name,
                "url": url,
                "status": f"OK:{status_code}" if 200 <= status_code < 400 else f"BAD:{status_code}",
                "error": None,
                "latency_ms": round(latency_ms, 2),
                "category": "success"
            }
    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        category = classify_exception(e)
        return {
            "name": name,
            "url": url,
            "status": "ERROR",
            "error": str(e),
            "latency_ms": round(latency_ms, 2),
            "category": category
        }

def main():
    """Test all MCP servers and print results"""
    print("=" * 80)
    print("MCP SERVER CONNECTIVITY TEST")
    print("=" * 80)
    print(f"\nTesting {len(MCP_SERVERS)} MCP servers...\n")

    results = []
    for name, url in MCP_SERVERS.items():
        print(f"Testing {name}...", end=" ")
        sys.stdout.flush()
        result = test_server(name, url)
        results.append(result)
        print(f"{result['status']} ({result['latency_ms']}ms)")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    success_count = sum(1 for r in results if r['category'] == 'success')
    timeout_count = sum(1 for r in results if r['category'] == 'timeout')
    http_404_count = sum(1 for r in results if r['category'] == 'http-status:404')
    http_error_count = sum(1 for r in results if 'http-status:' in r['category'] and r['category'] != 'http-status:404')
    connection_error_count = sum(1 for r in results if r['category'] == 'connection-error')
    dns_error_count = sum(1 for r in results if r['category'] == 'dns-error')
    config_error_count = sum(1 for r in results if r['category'] == 'config-error')

    print(f"\nTotal Servers: {len(results)}")
    print(f"  Success (200-399): {success_count}")
    print(f"  Timeout: {timeout_count}")
    print(f"  HTTP 404: {http_404_count}")
    print(f"  Other HTTP Errors: {http_error_count}")
    print(f"  Connection Errors: {connection_error_count}")
    print(f"  DNS Errors: {dns_error_count}")
    print(f"  Configuration Errors: {config_error_count}")

    # Detailed errors
    print("\n" + "=" * 80)
    print("DETAILED RESULTS")
    print("=" * 80)

    for result in results:
        print(f"\n{result['name']}:")
        print(f"  URL: {result['url']}")
        print(f"  Status: {result['status']}")
        print(f"  Category: {result['category']}")
        print(f"  Latency: {result['latency_ms']}ms")
        if result['error']:
            print(f"  Error: {result['error'][:200]}")

    # Recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)

    if timeout_count > 0:
        print("\nTIMEOUT ISSUES:")
        print("  - Check if Container Apps are running: az containerapp list --resource-group lab-master-lab")
        print("  - Verify ingress is enabled and public")
        print("  - Check Container App logs for startup issues")

    if http_404_count > 0:
        print("\nHTTP 404 ISSUES:")
        print("  - Verify the /mcp/ endpoint exists in the server implementation")
        print("  - Check Container App deployment logs")
        print("  - Ensure the correct image was deployed")

    if connection_error_count > 0:
        print("\nCONNECTION ERROR ISSUES:")
        print("  - Check if URLs are correct in master-lab.env")
        print("  - Verify network connectivity")
        print("  - Check if Container Apps Environment is healthy")

    if dns_error_count > 0:
        print("\nDNS ERROR ISSUES:")
        print("  - Verify the domain names in master-lab.env are correct")
        print("  - Check DNS resolution: nslookup <domain>")

    return 0 if success_count == len(results) else 1

if __name__ == "__main__":
    sys.exit(main())
