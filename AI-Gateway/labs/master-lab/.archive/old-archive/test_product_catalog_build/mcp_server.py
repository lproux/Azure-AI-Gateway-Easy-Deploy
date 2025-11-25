import uvicorn
from fastmcp import FastMCP, Context

mcp = FastMCP("ProductCatalog")

@mcp.tool()
async def get_products(ctx: Context, category: str = "all") -> str:
    """Get list of products from the catalog, optionally filtered by category."""
    products = [
        {
            "id": 1,
            "name": "Laptop Pro X1",
            "category": "electronics",
            "price": 1299.99,
            "stock": 45,
            "description": "High-performance laptop with 16GB RAM"
        },
        {
            "id": 2,
            "name": "Wireless Mouse",
            "category": "electronics",
            "price": 29.99,
            "stock": 150,
            "description": "Ergonomic wireless mouse with USB receiver"
        },
        {
            "id": 3,
            "name": "Office Chair Deluxe",
            "category": "furniture",
            "price": 399.99,
            "stock": 22,
            "description": "Ergonomic office chair with lumbar support"
        },
        {
            "id": 4,
            "name": "Desk Lamp LED",
            "category": "furniture",
            "price": 49.99,
            "stock": 78,
            "description": "Adjustable LED desk lamp with touch control"
        },
        {
            "id": 5,
            "name": "Notebook Set",
            "category": "stationery",
            "price": 12.99,
            "stock": 200,
            "description": "Pack of 5 ruled notebooks"
        },
        {
            "id": 6,
            "name": "Pen Collection",
            "category": "stationery",
            "price": 8.99,
            "stock": 350,
            "description": "Set of 10 ballpoint pens in assorted colors"
        },
        {
            "id": 7,
            "name": "USB-C Hub",
            "category": "electronics",
            "price": 59.99,
            "stock": 95,
            "description": "7-in-1 USB-C hub with HDMI and card readers"
        },
        {
            "id": 8,
            "name": "Standing Desk",
            "category": "furniture",
            "price": 599.99,
            "stock": 15,
            "description": "Electric height-adjustable standing desk"
        }
    ]

    # Filter by category if specified
    if category and category.lower() != "all":
        products = [p for p in products if p["category"].lower() == category.lower()]

    return str(products)

@mcp.tool()
async def get_product_by_id(ctx: Context, product_id: int) -> str:
    """Get detailed information about a specific product by ID."""
    products = {
        1: {"id": 1, "name": "Laptop Pro X1", "category": "electronics", "price": 1299.99, "stock": 45, "description": "High-performance laptop with 16GB RAM", "specs": {"ram": "16GB", "storage": "512GB SSD", "screen": "15.6 inch"}},
        2: {"id": 2, "name": "Wireless Mouse", "category": "electronics", "price": 29.99, "stock": 150, "description": "Ergonomic wireless mouse with USB receiver", "specs": {"connectivity": "2.4GHz wireless", "battery": "AA battery", "buttons": 5}},
        3: {"id": 3, "name": "Office Chair Deluxe", "category": "furniture", "price": 399.99, "stock": 22, "description": "Ergonomic office chair with lumbar support", "specs": {"weight_capacity": "300 lbs", "adjustable_height": "Yes", "material": "Mesh back"}},
        4: {"id": 4, "name": "Desk Lamp LED", "category": "furniture", "price": 49.99, "stock": 78, "description": "Adjustable LED desk lamp with touch control", "specs": {"brightness_levels": 5, "color_temperature": "3000K-6000K", "power": "12W"}},
        5: {"id": 5, "name": "Notebook Set", "category": "stationery", "price": 12.99, "stock": 200, "description": "Pack of 5 ruled notebooks", "specs": {"pages": 100, "size": "A5", "binding": "spiral"}},
        6: {"id": 6, "name": "Pen Collection", "category": "stationery", "price": 8.99, "stock": 350, "description": "Set of 10 ballpoint pens in assorted colors", "specs": {"ink_color": "assorted", "tip_size": "0.7mm", "quantity": 10}},
        7: {"id": 7, "name": "USB-C Hub", "category": "electronics", "price": 59.99, "stock": 95, "description": "7-in-1 USB-C hub with HDMI and card readers", "specs": {"ports": 7, "hdmi_resolution": "4K@30Hz", "usb_speed": "USB 3.0"}},
        8: {"id": 8, "name": "Standing Desk", "category": "furniture", "price": 599.99, "stock": 15, "description": "Electric height-adjustable standing desk", "specs": {"size": "60x30 inches", "height_range": "28-48 inches", "motor": "dual motor"}}
    }

    product = products.get(product_id)
    if product:
        return str(product)
    else:
        return str({"error": f"Product with ID {product_id} not found"})

@mcp.tool()
async def search_products(ctx: Context, query: str) -> str:
    """Search for products by name or description."""
    all_products = [
        {"id": 1, "name": "Laptop Pro X1", "category": "electronics", "price": 1299.99, "description": "High-performance laptop with 16GB RAM"},
        {"id": 2, "name": "Wireless Mouse", "category": "electronics", "price": 29.99, "description": "Ergonomic wireless mouse with USB receiver"},
        {"id": 3, "name": "Office Chair Deluxe", "category": "furniture", "price": 399.99, "description": "Ergonomic office chair with lumbar support"},
        {"id": 4, "name": "Desk Lamp LED", "category": "furniture", "price": 49.99, "description": "Adjustable LED desk lamp with touch control"},
        {"id": 5, "name": "Notebook Set", "category": "stationery", "price": 12.99, "description": "Pack of 5 ruled notebooks"},
        {"id": 6, "name": "Pen Collection", "category": "stationery", "price": 8.99, "description": "Set of 10 ballpoint pens in assorted colors"},
        {"id": 7, "name": "USB-C Hub", "category": "electronics", "price": 59.99, "description": "7-in-1 USB-C hub with HDMI and card readers"},
        {"id": 8, "name": "Standing Desk", "category": "furniture", "price": 599.99, "description": "Electric height-adjustable standing desk"}
    ]

    # Simple search in name and description
    query_lower = query.lower()
    results = [p for p in all_products if query_lower in p["name"].lower() or query_lower in p["description"].lower()]

    return str(results)

if __name__ == "__main__":
    # Use mcp.run() with HTTP transport
    mcp.run(transport="http", host="0.0.0.0", port=8080, path="/product-catalog")
