#!/usr/bin/env python3
"""Fix cells 79, 81, 83 - add PlaceOrderMCP helper and refactor cells"""

import json

# First, add PlaceOrderMCP to notebook_mcp_helpers.py
helper_code = '''
class PlaceOrderMCP(StreamableHTTPMCPClient):
    """
    Place Order MCP Server client using Streamable HTTP transport

    Tools:
        - place_order: Place an order for a product
        - get_order_status: Get status of an order
        - list_orders: List all orders
        - cancel_order: Cancel an order
        - update_order_status: Update order status
    """

    def __init__(self, server_url: str):
        super().__init__(server_url, "/place-order")

    def place_order(self, product_id: str, quantity: int, customer_email: str) -> Dict[str, Any]:
        """
        Place an order for a product

        Args:
            product_id: Product ID to order
            quantity: Quantity to order
            customer_email: Customer email address

        Returns:
            Order details
        """
        return self._call_tool("place_order", {
            "product_id": product_id,
            "quantity": quantity,
            "customer_email": customer_email
        })

    def get_order_status(self, order_id: str) -> Dict[str, Any]:
        """
        Get status of an order

        Args:
            order_id: Order ID to check

        Returns:
            Order status and details
        """
        return self._call_tool("get_order_status", {"order_id": order_id})

    def list_orders(self, customer_email: str = None) -> Dict[str, Any]:
        """
        List all orders, optionally filtered by customer email

        Args:
            customer_email: Optional customer email to filter by

        Returns:
            List of orders
        """
        args = {}
        if customer_email:
            args["customer_email"] = customer_email
        return self._call_tool("list_orders", args)

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """
        Cancel an order

        Args:
            order_id: Order ID to cancel

        Returns:
            Cancellation result
        """
        return self._call_tool("cancel_order", {"order_id": order_id})

    def update_order_status(self, order_id: str, new_status: str) -> Dict[str, Any]:
        """
        Update order status

        Args:
            order_id: Order ID to update
            new_status: New status (pending, processing, shipped, delivered, cancelled)

        Returns:
            Update result
        """
        return self._call_tool("update_order_status", {
            "order_id": order_id,
            "new_status": new_status
        })
'''

# Read helper file and add PlaceOrderMCP before MemoryMCP
with open('../notebook_mcp_helpers.py', 'r', encoding='utf-8') as f:
    helper_content = f.read()

# Find where to insert (before MemoryMCP class)
insert_marker = "class MemoryMCP:"
if insert_marker in helper_content:
    helper_content = helper_content.replace(insert_marker, helper_code + "\n\n" + insert_marker)

    with open('../notebook_mcp_helpers.py', 'w', encoding='utf-8') as f:
        f.write(helper_content)
    print("✅ Added PlaceOrderMCP to notebook_mcp_helpers.py")

# Also update MCPClient to include place_order
with open('../notebook_mcp_helpers.py', 'r', encoding='utf-8') as f:
    helper_content = f.read()

old_line = '        self.github = GitHubMCP(self.config.get("GITHUB_MCP_URL", ""))'
new_lines = '''        self.github = GitHubMCP(self.config.get("GITHUB_MCP_URL", ""))
        self.place_order = PlaceOrderMCP(self.config.get("PLACE_ORDER_MCP_URL", ""))'''

if old_line in helper_content and "self.place_order" not in helper_content:
    helper_content = helper_content.replace(old_line, new_lines)

    with open('../notebook_mcp_helpers.py', 'w', encoding='utf-8') as f:
        f.write(helper_content)
    print("✅ Added place_order to MCPClient")

# Now load and update notebook
with open('../master-ai-gateway.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Cell 79: Product catalog
cell_79_content = """# Lab 18: E-Commerce Product Catalog
# Access product catalog via MCP server

from notebook_mcp_helpers import ProductCatalogMCP

product_catalog_url = "http://145.133.116.26:8080"
product_catalog = ProductCatalogMCP(product_catalog_url)

print("[*] Connecting to product catalog...")

try:
    # Get all products
    print("[*] Fetching product catalog...")
    products = product_catalog.get_products()

    print('[SUCCESS] Products:')
    print('-' * 40)

    import json
    if isinstance(products, str):
        import ast
        try:
            result_parsed = ast.literal_eval(products)
            output = json.dumps(result_parsed, indent=2)
        except:
            output = products
    else:
        output = json.dumps(products, indent=2)

    if len(output) > 1000:
        output = output[:1000] + '\\n...\\n(truncated)'
    print(output)

    # Get products by category
    print()
    print("[*] Fetching electronics...")
    electronics = product_catalog.get_products("electronics")
    print(f"[SUCCESS] Electronics: {electronics}")

except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")

print()
print('[OK] Product catalog complete')
"""

# Cell 81: Place order
cell_81_content = """# Lab 19: E-Commerce Order Placement
# Place orders via MCP server

from notebook_mcp_helpers import PlaceOrderMCP

place_order_url = "http://4.250.92.120:8080"
place_order = PlaceOrderMCP(place_order_url)

print("[*] Connecting to place-order service...")

try:
    # Place a test order
    order_data = {
        'product_id': 'PROD-001',
        'quantity': 2,
        'customer_email': 'test@example.com'
    }

    print(f"[*] Placing order: {order_data}")
    order_result = place_order.place_order(
        product_id=order_data['product_id'],
        quantity=order_data['quantity'],
        customer_email=order_data['customer_email']
    )

    print('[SUCCESS] Order placed:')
    print('-' * 40)

    import json
    if isinstance(order_result, str):
        import ast
        try:
            result_parsed = ast.literal_eval(order_result)
            output = json.dumps(result_parsed, indent=2)
            order_id = result_parsed.get('order_id', 'N/A')
            print(f"Order ID: {order_id}")
        except:
            output = order_result
    else:
        output = json.dumps(order_result, indent=2)

    print(output)

    # Check order status
    if 'order_id' in locals() and order_id != 'N/A':
        print()
        print(f"[*] Checking order status for {order_id}...")
        status = place_order.get_order_status(order_id)
        print(f"[SUCCESS] Order status: {status}")

except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")

print()
print('[OK] Order placement complete')
"""

# Cell 83: Shopping assistant
cell_83_content = """# Lab 20: AI-Powered Shopping Assistant
# Combine product catalog with AI for shopping recommendations

from notebook_mcp_helpers import ProductCatalogMCP
import json

product_catalog_url = "http://145.133.116.26:8080"
product_catalog = ProductCatalogMCP(product_catalog_url)

print("[*] Getting products for AI recommendations...")

try:
    # Get products
    products = product_catalog.get_products()

    print('[SUCCESS] Retrieved product catalog')

    # Parse products for AI
    if isinstance(products, str):
        import ast
        try:
            products_parsed = ast.literal_eval(products)
        except:
            products_parsed = products
    else:
        products_parsed = products

    # Get AI shopping recommendations
    prompt = f"Based on these products, recommend the best items for a home office setup:\\n\\n{json.dumps(products_parsed, indent=2)[:1000]}"

    print()
    print("[*] Getting AI recommendations...")
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': 'You are a helpful shopping assistant.'},
            {'role': 'user', 'content': prompt}
        ],
        max_tokens=500
    )

    recommendation = response.choices[0].message.content

    print('[SUCCESS] AI Shopping Recommendations:')
    print('-' * 40)
    print(recommendation)

except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")

print()
print('[OK] Shopping assistant complete')
"""

# Update cells
nb['cells'][79]['source'] = cell_79_content.split('\n')
nb['cells'][81]['source'] = cell_81_content.split('\n')
nb['cells'][83]['source'] = cell_83_content.split('\n')

# Save notebook
with open('../master-ai-gateway.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("✅ Cells 79, 81, 83 refactored successfully!")
print("All cells updated to use working MCP helpers with Streamable HTTP transport")
print()
print("Summary:")
print("- Cell 79: Uses ProductCatalogMCP (existing server)")
print("- Cell 81: Uses PlaceOrderMCP (NEW server at 4.250.92.120)")
print("- Cell 83: Uses ProductCatalogMCP with AI integration")
