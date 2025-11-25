#!/usr/bin/env python3
"""Refactor cell 59 to use OnCallMCP helper"""

import json

# Load notebook
with open('../master-ai-gateway.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# New cell content using OnCallMCP helper
new_cell_content = """# Lab 10 Example: OnCall MCP Server
# Demonstrates on-call schedule management via MCP

# Approach 1: Using OnCallMCP helper from notebook_mcp_helpers.py
# This approach uses the working StreamableHTTPMCPClient pattern

from notebook_mcp_helpers import OnCallMCP

# Create OnCall client with HTTP server URL
oncall_server_url = "http://20.246.202.123:8080"
oncall = OnCallMCP(oncall_server_url)

print("[*] Connecting to oncall MCP server...")
print(f"[*] Server URL: {oncall_server_url}")

try:
    # Get on-call list
    print()
    print("[*] Getting current on-call list...")
    oncall_list = oncall.get_oncall_list()

    # Display result
    print('[SUCCESS] OnCall data retrieved')
    print('-' * 40)

    # Format output
    import json
    if isinstance(oncall_list, str):
        # Parse string result
        import ast
        try:
            result_parsed = ast.literal_eval(oncall_list)
            output = json.dumps(result_parsed, indent=2)
        except:
            output = oncall_list
    else:
        output = json.dumps(oncall_list, indent=2)

    # Truncate if too long
    if len(output) > 500:
        output = output[:500] + '\\n...\\n(truncated)'
    print(output)

    # Show on-call count
    if isinstance(result_parsed, list):
        active_oncalls = [p for p in result_parsed if p.get('status') == 'on']
        print()
        print(f"[INFO] Total engineers on call: {len(active_oncalls)}")

except Exception as e:
    print(f"[ERROR] oncall: {type(e).__name__}: {e}")
    print("[HINT] Server may be down or URL may be incorrect")

print()
print('[OK] OnCall demo complete')
"""

# Update cell 59
nb['cells'][59]['source'] = new_cell_content.split('\n')

# Save notebook
with open('../master-ai-gateway.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Cell 59 refactored successfully!")
print("Updated to use OnCallMCP helper with Streamable HTTP transport")
