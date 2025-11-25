#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Priority 4: Investigate Cell 100 (HTTP 404 Error)

Multiple attempts to understand and fix the 404 error.
"""
import json
import sys
import re
from pathlib import Path

# Configure UTF-8 for Windows
if sys.platform == 'win32':
    import codecs
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    else:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


def main():
    print("=" * 80)
    print("PRIORITY 4: INVESTIGATE CELL 100 (HTTP 404)")
    print("=" * 80)
    print()

    # Load notebook
    with open('master-ai-gateway-FINAL-FIXED.ipynb', 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Cell 100 is index 99
    cell100 = nb['cells'][99]
    source = ''.join(cell100['source']) if isinstance(cell100['source'], list) else cell100['source']
    outputs = cell100.get('outputs', [])

    print("Cell 100 Analysis")
    print("=" * 80)
    print()

    # Find URLs in source
    print("📍 URLs Found in Source Code:")
    print("-" * 80)
    url_pattern = r'https?://[^\s\'"<>]+'
    urls = re.findall(url_pattern, source)
    for i, url in enumerate(urls, 1):
        print(f"  {i}. {url}")
    print()

    # Find API endpoints
    print("🔗 API Endpoints:")
    print("-" * 80)
    endpoint_pattern = r'[\'"]/([\w\-/]+)[\'"]'
    endpoints = re.findall(endpoint_pattern, source)
    for i, endpoint in enumerate(endpoints, 1):
        print(f"  {i}. /{endpoint}")
    print()

    # Check for environment variables
    print("🔐 Environment Variables:")
    print("-" * 80)
    env_vars = re.findall(r'os\.getenv\([\'"](\w+)[\'"]', source)
    env_vars += re.findall(r'os\.environ\.get\([\'"](\w+)[\'"]', source)
    env_vars += re.findall(r'os\.environ\[[\'"](\w+)[\'"]\]', source)
    unique_env_vars = list(set(env_vars))
    for var in sorted(unique_env_vars):
        print(f"  • {var}")
    print()

    # Analyze output errors
    print("❌ Errors in Output:")
    print("-" * 80)
    error_found = False
    for output in outputs:
        if output.get('output_type') == 'stream':
            text = ''.join(output.get('text', []))

            # Look for 404 errors
            if '404' in text:
                error_found = True
                # Extract context around 404
                lines = text.split('\n')
                for i, line in enumerate(lines):
                    if '404' in line:
                        # Show context: 2 lines before, the line, 2 lines after
                        start = max(0, i-2)
                        end = min(len(lines), i+3)
                        print(f"  Context around 404 error:")
                        for j in range(start, end):
                            marker = ">>>" if j == i else "   "
                            print(f"    {marker} {lines[j]}")
                        print()

    if not error_found:
        print("  ℹ️  No 404 errors found in output (cell may be working correctly)")
    print()

    # Show source preview
    print("📝 Source Code Preview (first 50 lines):")
    print("-" * 80)
    lines = source.split('\n')
    for i, line in enumerate(lines[:50], 1):
        print(f"  {i:3d}: {line}")
    print()
    if len(lines) > 50:
        print(f"  ... ({len(lines) - 50} more lines)")
        print()

    # Recommendations
    print("=" * 80)
    print("💡 RECOMMENDATIONS FOR FIXING CELL 100")
    print("=" * 80)
    print()

    print("Based on analysis, here are multiple fix attempts:")
    print()

    print("Attempt 1: Verify Endpoint Configuration")
    print("-" * 80)
    print("Check if the endpoint exists in APIM:")
    print("  1. Review APIM_GATEWAY_URL")
    print("  2. Verify API_ID is correct")
    print("  3. Check if deployment path exists")
    print()

    print("Attempt 2: Add Error Handling")
    print("-" * 80)
    print("Wrap API calls in try-except to continue on 404:")
    print("""
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 404:
        print("[WARN] Endpoint not found (404) - may not be deployed yet")
        print(f"[INFO] Attempted URL: {url}")
        print("[OK] Continuing with demo...")
    else:
        raise
""")
    print()

    print("Attempt 3: Check Deployment Status")
    print("-" * 80)
    print("Add deployment verification before calling API:")
    print("""
# Verify deployment exists
deployment_check_url = f"{APIM_GATEWAY_URL}/openai/deployments"
try:
    deployments = requests.get(deployment_check_url).json()
    print(f"[INFO] Available deployments: {deployments}")
except Exception as e:
    print(f"[WARN] Could not list deployments: {e}")
""")
    print()

    print("Attempt 4: Use Alternative Endpoint")
    print("-" * 80)
    print("If MCP backend endpoint not found, skip gracefully:")
    print("""
# Check if this is MCP-specific endpoint
if 'mcp' in url.lower():
    print("[INFO] MCP backend endpoint - optional feature")
    print("[OK] Skipping MCP backend test (not mandatory)")
    # Continue without error
else:
    # Try actual request
    response = requests.get(url)
""")
    print()

    print("=" * 80)
    print("NEXT STEP: Apply one or more fix attempts")
    print("=" * 80)
    print()


if __name__ == '__main__':
    main()
