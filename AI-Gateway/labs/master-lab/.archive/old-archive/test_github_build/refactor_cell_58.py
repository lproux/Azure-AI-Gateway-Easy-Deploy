#!/usr/bin/env python3
"""Refactor cell 58 to use GitHubMCP helper"""

import json

# Load notebook
with open('../master-ai-gateway.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# New cell content using GitHubMCP helper
new_cell_content = """# Lab 10 Example: GitHub MCP Server
# Demonstrates GitHub repository operations via MCP

# Approach 1: Using GitHubMCP helper from notebook_mcp_helpers.py
# This approach uses the working StreamableHTTPMCPClient pattern

from notebook_mcp_helpers import GitHubMCP

# Create GitHub client with HTTP server URL
github_server_url = "http://4.158.206.99:8080"
github = GitHubMCP(github_server_url)

print("[*] Connecting to github MCP server...")
print(f"[*] Server URL: {github_server_url}")

try:
    # Search for AI repositories
    print()
    print("[*] Searching for AI repositories...")
    search_result = github.search_repositories("AI language:python")

    # Display result
    print('[SUCCESS] Search results retrieved')
    print('-' * 40)

    # Format output
    import json
    if isinstance(search_result, str):
        # Parse string result
        import ast
        try:
            result_parsed = ast.literal_eval(search_result)
            output = json.dumps(result_parsed, indent=2)
        except:
            output = search_result
    else:
        output = json.dumps(search_result, indent=2)

    # Truncate if too long
    if len(output) > 1000:
        output = output[:1000] + '\\n...\\n(truncated)'
    print(output)

    # Get specific repository details
    print()
    print("[*] Getting repository details for aidevs/awesome-ai...")
    repo = github.get_repository("aidevs", "awesome-ai")
    print(f"[SUCCESS] Repository: {repo}")

    # List repository issues
    print()
    print("[*] Listing open issues for aidevs/awesome-ai...")
    issues = github.list_repository_issues("aidevs", "awesome-ai", "open")
    print(f"[SUCCESS] Issues: {issues}")

except Exception as e:
    print(f"[ERROR] github: {type(e).__name__}: {e}")
    print("[HINT] Server may be down or URL may be incorrect")

print()
print('[OK] GitHub demo complete')
"""

# Update cell 58
nb['cells'][58]['source'] = new_cell_content.split('\n')

# Save notebook
with open('../master-ai-gateway.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Cell 58 refactored successfully!")
print("Updated to use GitHubMCP helper with Streamable HTTP transport")
