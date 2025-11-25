#!/usr/bin/env python3
"""Refactor cell 56 to use ProductCatalogMCP helper"""

import json
import sys

# Load notebook
with open('../master-ai-gateway.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# New cell content using ProductCatalogMCP helper
new_cell_content = """# Lab 10 Example: Product Catalog MCP Server
# Demonstrates e-commerce product catalog access via MCP

# Approach 1: Using ProductCatalogMCP helper from notebook_mcp_helpers.py
# This approach uses the working StreamableHTTPMCPClient pattern

from notebook_mcp_helpers import ProductCatalogMCP

# Create ProductCatalog client with HTTP server URL
product_catalog_server_url = "http://145.133.116.26:8080"
product_catalog = ProductCatalogMCP(product_catalog_server_url)

print("[*] Connecting to product-catalog MCP server...")
print(f"[*] Server URL: {product_catalog_server_url}")

try:
    # Fetch all products
    print()
    print("[*] Fetching all products...")
    result = product_catalog.get_products()

    # Display result
    print('[SUCCESS] Products retrieved:')
    print('-' * 40)

    # Format output
    import json
    if isinstance(result, str):
        # Parse string result
        import ast
        try:
            result_parsed = ast.literal_eval(result)
            output = json.dumps(result_parsed, indent=2)
        except:
            output = result
    else:
        output = json.dumps(result, indent=2)

    # Truncate if too long
    if len(output) > 1000:
        output = output[:1000] + '\\n...\\n(truncated)'
    print(output)

    # Test get_product_by_id
    print()
    print("[*] Fetching product with ID 1...")
    product = product_catalog.get_product_by_id(1)
    print(f"[SUCCESS] Product details: {product}")

    # Test search_products
    print()
    print("[*] Searching for 'laptop'...")
    search_results = product_catalog.search_products("laptop")
    print(f"[SUCCESS] Search results: {search_results}")

except Exception as e:
    print(f"[ERROR] product-catalog: {type(e).__name__}: {e}")
    print("[HINT] Server may be down or URL may be incorrect")

print()
print('[OK] Product Catalog demo complete')
"""

# Update cell 56
nb['cells'][56]['source'] = new_cell_content.split('\n')

# Save notebook
with open('../master-ai-gateway.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Cell 56 refactored successfully!")
print("Updated to use ProductCatalogMCP helper with Streamable HTTP transport")
