import uvicorn
from fastmcp import FastMCP, Context
from datetime import datetime

mcp = FastMCP("PlaceOrder")

# Mock order storage
orders = []
order_counter = 1000

@mcp.tool()
async def place_order(ctx: Context, product_id: str, quantity: int, customer_email: str) -> str:
    """
    Place an order for a product

    Args:
        product_id: Product ID to order
        quantity: Quantity to order
        customer_email: Customer email address
    """
    global order_counter

    order = {
        "order_id": f"ORD-{order_counter}",
        "product_id": product_id,
        "quantity": quantity,
        "customer_email": customer_email,
        "status": "pending",
        "order_date": datetime.now().isoformat(),
        "total_amount": quantity * 99.99  # Mock price calculation
    }

    orders.append(order)
    order_counter += 1

    return str(order)

@mcp.tool()
async def get_order_status(ctx: Context, order_id: str) -> str:
    """
    Get status of an order

    Args:
        order_id: Order ID to check
    """
    for order in orders:
        if order["order_id"] == order_id:
            return str(order)

    return str({"error": f"Order {order_id} not found"})

@mcp.tool()
async def list_orders(ctx: Context, customer_email: str = None) -> str:
    """
    List all orders, optionally filtered by customer email

    Args:
        customer_email: Optional customer email to filter by
    """
    if customer_email:
        filtered_orders = [o for o in orders if o["customer_email"] == customer_email]
        return str(filtered_orders)

    return str(orders)

@mcp.tool()
async def cancel_order(ctx: Context, order_id: str) -> str:
    """
    Cancel an order

    Args:
        order_id: Order ID to cancel
    """
    for order in orders:
        if order["order_id"] == order_id:
            if order["status"] == "pending":
                order["status"] = "cancelled"
                return str({"success": True, "message": f"Order {order_id} cancelled", "order": order})
            else:
                return str({"success": False, "message": f"Cannot cancel order in {order['status']} status"})

    return str({"success": False, "error": f"Order {order_id} not found"})

@mcp.tool()
async def update_order_status(ctx: Context, order_id: str, new_status: str) -> str:
    """
    Update order status

    Args:
        order_id: Order ID to update
        new_status: New status (pending, processing, shipped, delivered, cancelled)
    """
    valid_statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]

    if new_status not in valid_statuses:
        return str({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})

    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = new_status
            return str({"success": True, "message": f"Order {order_id} updated to {new_status}", "order": order})

    return str({"error": f"Order {order_id} not found"})

if __name__ == "__main__":
    # Use mcp.run() with HTTP transport
    mcp.run(transport="http", host="0.0.0.0", port=8080, path="/place-order")
