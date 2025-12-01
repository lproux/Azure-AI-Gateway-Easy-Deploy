#!/usr/bin/env python3
"""
Excel Analytics MCP Server
A FastMCP-based HTTP server that provides Excel data analysis capabilities.
Exposes tools for analyzing sales, customer, employee, and inventory data.
"""
import json
import uvicorn

try:
    from fastmcp import FastMCP, Context
except ModuleNotFoundError:
    from mcp.server.fastmcp import FastMCP, Context

from starlette.applications import Starlette
from starlette.routing import Mount

mcp = FastMCP("Excel Analytics")

# Sample data embedded (converted from Excel files for reliability)
# This eliminates file I/O complexity and external dependencies

SAMPLE_DATA = {
    "sales_performance": {
        "headers": ["Region", "Product", "Date", "TotalSales", "Quantity", "CustomerID"],
        "rows": [
            ["North America", "Software Licenses", "2024-01-15", 125000.00, 250, "CUST-1001"],
            ["North America", "Cloud Services", "2024-01-15", 89500.00, 178, "CUST-1002"],
            ["North America", "Professional Services", "2024-01-16", 67800.00, 45, "CUST-1003"],
            ["Europe", "Software Licenses", "2024-01-15", 98000.00, 196, "CUST-2001"],
            ["Europe", "Cloud Services", "2024-01-16", 112000.00, 224, "CUST-2002"],
            ["Europe", "Hardware", "2024-01-17", 45600.00, 38, "CUST-2003"],
            ["Asia Pacific", "Software Licenses", "2024-01-15", 156000.00, 312, "CUST-3001"],
            ["Asia Pacific", "Cloud Services", "2024-01-16", 134500.00, 269, "CUST-3002"],
            ["Asia Pacific", "Professional Services", "2024-01-17", 78900.00, 52, "CUST-3003"],
            ["Latin America", "Software Licenses", "2024-01-15", 45000.00, 90, "CUST-4001"],
            ["Latin America", "Cloud Services", "2024-01-16", 38500.00, 77, "CUST-4002"],
            ["Latin America", "Hardware", "2024-01-17", 23400.00, 19, "CUST-4003"],
        ]
    },
    "customer_analytics": {
        "headers": ["CustomerID", "CustomerName", "Industry", "Country", "SignupDate", "LifetimeValue", "ActiveSubscriptions", "SupportTickets"],
        "rows": [
            ["CUST-1001", "Contoso Corp", "Technology", "USA", "2021-03-15", 450000.00, 12, 23],
            ["CUST-1002", "Fabrikam Inc", "Finance", "USA", "2020-07-22", 680000.00, 18, 15],
            ["CUST-1003", "Adventure Works", "Retail", "USA", "2022-01-10", 230000.00, 6, 45],
            ["CUST-2001", "Northwind Traders", "Manufacturing", "Germany", "2021-05-18", 520000.00, 14, 28],
            ["CUST-2002", "Alpine Ski House", "Hospitality", "Switzerland", "2020-11-30", 340000.00, 8, 12],
            ["CUST-2003", "Coho Winery", "Food & Beverage", "France", "2022-04-05", 180000.00, 4, 8],
            ["CUST-3001", "Tailspin Toys", "Retail", "Japan", "2021-08-12", 890000.00, 22, 34],
            ["CUST-3002", "Wide World Importers", "Logistics", "Singapore", "2020-02-28", 720000.00, 16, 19],
            ["CUST-3003", "Graphic Design Institute", "Education", "Australia", "2022-06-20", 150000.00, 3, 7],
        ]
    },
    "employee_performance": {
        "headers": ["EmployeeID", "Name", "Department", "Role", "HireDate", "PerformanceScore", "SalesTarget", "SalesActual", "Region"],
        "rows": [
            ["EMP-001", "Sarah Chen", "Sales", "Account Executive", "2020-03-15", 4.5, 500000, 578000, "North America"],
            ["EMP-002", "Michael Brown", "Sales", "Sales Manager", "2019-01-10", 4.8, 1200000, 1350000, "North America"],
            ["EMP-003", "Emma Wilson", "Sales", "Account Executive", "2021-06-22", 4.2, 450000, 412000, "Europe"],
            ["EMP-004", "James Taylor", "Sales", "Senior Account Executive", "2018-09-05", 4.7, 750000, 823000, "Europe"],
            ["EMP-005", "Yuki Tanaka", "Sales", "Regional Director", "2017-04-18", 4.9, 2000000, 2450000, "Asia Pacific"],
            ["EMP-006", "Carlos Rodriguez", "Sales", "Account Executive", "2022-02-14", 3.9, 400000, 385000, "Latin America"],
            ["EMP-007", "Anna Schmidt", "Engineering", "Software Engineer", "2020-08-01", 4.3, 0, 0, "Europe"],
            ["EMP-008", "David Kim", "Engineering", "Tech Lead", "2019-05-20", 4.6, 0, 0, "Asia Pacific"],
        ]
    },
    "inventory_report": {
        "headers": ["SKU", "ProductName", "Category", "Warehouse", "QuantityOnHand", "ReorderLevel", "UnitCost", "LastRestocked"],
        "rows": [
            ["SKU-001", "Enterprise License Pack", "Software", "Seattle", 1500, 200, 299.99, "2024-01-10"],
            ["SKU-002", "Cloud Starter Bundle", "Services", "Seattle", 9999, 100, 49.99, "2024-01-15"],
            ["SKU-003", "Premium Support Plan", "Services", "Dublin", 9999, 50, 199.99, "2024-01-12"],
            ["SKU-004", "Server Hardware Kit", "Hardware", "Singapore", 250, 50, 1299.99, "2024-01-08"],
            ["SKU-005", "Network Switch Pro", "Hardware", "Seattle", 180, 30, 599.99, "2024-01-05"],
            ["SKU-006", "Developer Tools Suite", "Software", "Dublin", 2500, 300, 149.99, "2024-01-14"],
            ["SKU-007", "Security Appliance", "Hardware", "Singapore", 75, 20, 2499.99, "2024-01-03"],
            ["SKU-008", "Training Credits", "Services", "Seattle", 50000, 5000, 9.99, "2024-01-16"],
        ]
    },
    "azure_resource_costs": {
        "headers": ["ResourceGroup", "ResourceType", "ResourceName", "Region", "MonthlyCost", "Department", "Environment"],
        "rows": [
            ["rg-prod-web", "Virtual Machine", "vm-web-prod-01", "East US", 450.00, "Engineering", "Production"],
            ["rg-prod-web", "Virtual Machine", "vm-web-prod-02", "East US", 450.00, "Engineering", "Production"],
            ["rg-prod-db", "SQL Database", "sql-prod-main", "East US", 890.00, "Engineering", "Production"],
            ["rg-dev-web", "Virtual Machine", "vm-web-dev-01", "West US", 125.00, "Engineering", "Development"],
            ["rg-prod-api", "App Service", "app-api-prod", "East US", 320.00, "Engineering", "Production"],
            ["rg-prod-storage", "Storage Account", "stproddata001", "East US", 180.00, "Engineering", "Production"],
            ["rg-analytics", "Synapse Workspace", "syn-analytics", "East US 2", 1200.00, "Data Science", "Production"],
            ["rg-ml", "Machine Learning", "ml-workspace", "West US 2", 850.00, "Data Science", "Development"],
        ]
    }
}


@mcp.tool()
async def list_workbooks(ctx: Context) -> str:
    """List all available Excel workbooks/datasets for analysis."""
    workbooks = []
    for name, data in SAMPLE_DATA.items():
        workbooks.append({
            "name": name,
            "display_name": name.replace("_", " ").title(),
            "columns": len(data["headers"]),
            "rows": len(data["rows"])
        })
    return json.dumps({"workbooks": workbooks, "count": len(workbooks)}, indent=2)


@mcp.tool()
async def get_workbook_summary(ctx: Context, workbook_name: str) -> str:
    """Get detailed summary of a workbook including column names and sample data.

    Args:
        workbook_name: Name of the workbook (e.g., 'sales_performance', 'customer_analytics')
    """
    if workbook_name not in SAMPLE_DATA:
        available = list(SAMPLE_DATA.keys())
        return json.dumps({"error": f"Workbook '{workbook_name}' not found. Available: {available}"})

    data = SAMPLE_DATA[workbook_name]
    headers = data["headers"]
    rows = data["rows"]

    # Create sample rows as dicts
    sample_data = []
    for row in rows[:3]:
        sample_data.append(dict(zip(headers, row)))

    return json.dumps({
        "workbook": workbook_name,
        "columns": headers,
        "total_rows": len(rows),
        "sample_data": sample_data
    }, indent=2)


@mcp.tool()
async def analyze_sales_by_region(ctx: Context) -> str:
    """Analyze sales performance data grouped by region. Returns total sales, quantity, and transaction count per region."""
    data = SAMPLE_DATA["sales_performance"]
    headers = data["headers"]
    rows = data["rows"]

    # Find column indices
    region_idx = headers.index("Region")
    sales_idx = headers.index("TotalSales")
    qty_idx = headers.index("Quantity")

    # Group by region
    region_stats = {}
    for row in rows:
        region = row[region_idx]
        if region not in region_stats:
            region_stats[region] = {"total_sales": 0, "quantity": 0, "transactions": 0}
        region_stats[region]["total_sales"] += row[sales_idx]
        region_stats[region]["quantity"] += row[qty_idx]
        region_stats[region]["transactions"] += 1

    # Format results
    results = []
    for region, stats in region_stats.items():
        results.append({
            "region": region,
            "total_sales": round(stats["total_sales"], 2),
            "total_quantity": stats["quantity"],
            "transaction_count": stats["transactions"],
            "avg_sale_value": round(stats["total_sales"] / stats["transactions"], 2)
        })

    results.sort(key=lambda x: x["total_sales"], reverse=True)

    return json.dumps({
        "analysis": "Sales by Region",
        "results": results,
        "grand_total": round(sum(r["total_sales"] for r in results), 2)
    }, indent=2)


@mcp.tool()
async def analyze_sales_by_product(ctx: Context) -> str:
    """Analyze sales performance data grouped by product type. Returns total sales and quantity per product."""
    data = SAMPLE_DATA["sales_performance"]
    headers = data["headers"]
    rows = data["rows"]

    product_idx = headers.index("Product")
    sales_idx = headers.index("TotalSales")
    qty_idx = headers.index("Quantity")

    product_stats = {}
    for row in rows:
        product = row[product_idx]
        if product not in product_stats:
            product_stats[product] = {"total_sales": 0, "quantity": 0, "transactions": 0}
        product_stats[product]["total_sales"] += row[sales_idx]
        product_stats[product]["quantity"] += row[qty_idx]
        product_stats[product]["transactions"] += 1

    results = []
    for product, stats in product_stats.items():
        results.append({
            "product": product,
            "total_sales": round(stats["total_sales"], 2),
            "total_quantity": stats["quantity"],
            "transaction_count": stats["transactions"],
            "avg_sale_value": round(stats["total_sales"] / stats["transactions"], 2)
        })

    results.sort(key=lambda x: x["total_sales"], reverse=True)

    return json.dumps({
        "analysis": "Sales by Product",
        "results": results,
        "grand_total": round(sum(r["total_sales"] for r in results), 2)
    }, indent=2)


@mcp.tool()
async def get_top_customers(ctx: Context, limit: int = 5) -> str:
    """Get top customers ranked by lifetime value.

    Args:
        limit: Number of top customers to return (default: 5)
    """
    data = SAMPLE_DATA["customer_analytics"]
    headers = data["headers"]
    rows = data["rows"]

    customers = []
    for row in rows:
        customer = dict(zip(headers, row))
        customers.append({
            "customer_id": customer["CustomerID"],
            "name": customer["CustomerName"],
            "industry": customer["Industry"],
            "country": customer["Country"],
            "lifetime_value": customer["LifetimeValue"],
            "active_subscriptions": customer["ActiveSubscriptions"],
            "support_tickets": customer["SupportTickets"]
        })

    customers.sort(key=lambda x: x["lifetime_value"], reverse=True)
    top_customers = customers[:limit]

    return json.dumps({
        "analysis": f"Top {limit} Customers by Lifetime Value",
        "results": top_customers,
        "total_lifetime_value": round(sum(c["lifetime_value"] for c in top_customers), 2)
    }, indent=2)


@mcp.tool()
async def get_top_performers(ctx: Context, limit: int = 5) -> str:
    """Get top performing employees by performance score and sales achievement.

    Args:
        limit: Number of top performers to return (default: 5)
    """
    data = SAMPLE_DATA["employee_performance"]
    headers = data["headers"]
    rows = data["rows"]

    employees = []
    for row in rows:
        emp = dict(zip(headers, row))
        target = emp["SalesTarget"]
        actual = emp["SalesActual"]
        achievement = (actual / target * 100) if target > 0 else 0

        employees.append({
            "employee_id": emp["EmployeeID"],
            "name": emp["Name"],
            "department": emp["Department"],
            "role": emp["Role"],
            "region": emp["Region"],
            "performance_score": emp["PerformanceScore"],
            "sales_target": target,
            "sales_actual": actual,
            "achievement_pct": round(achievement, 1)
        })

    # Sort by performance score, then by achievement
    employees.sort(key=lambda x: (x["performance_score"], x["achievement_pct"]), reverse=True)
    top_performers = employees[:limit]

    return json.dumps({
        "analysis": f"Top {limit} Performers",
        "results": top_performers
    }, indent=2)


@mcp.tool()
async def get_inventory_alerts(ctx: Context) -> str:
    """Get inventory items that are at or below reorder level."""
    data = SAMPLE_DATA["inventory_report"]
    headers = data["headers"]
    rows = data["rows"]

    alerts = []
    for row in rows:
        item = dict(zip(headers, row))
        qty = item["QuantityOnHand"]
        reorder = item["ReorderLevel"]

        if qty <= reorder:
            alerts.append({
                "sku": item["SKU"],
                "product": item["ProductName"],
                "category": item["Category"],
                "warehouse": item["Warehouse"],
                "quantity_on_hand": qty,
                "reorder_level": reorder,
                "status": "CRITICAL" if qty < reorder * 0.5 else "LOW"
            })

    return json.dumps({
        "analysis": "Inventory Reorder Alerts",
        "alert_count": len(alerts),
        "items": alerts
    }, indent=2)


@mcp.tool()
async def analyze_azure_costs(ctx: Context) -> str:
    """Analyze Azure resource costs grouped by department and environment."""
    data = SAMPLE_DATA["azure_resource_costs"]
    headers = data["headers"]
    rows = data["rows"]

    # Group by department
    dept_costs = {}
    env_costs = {}

    for row in rows:
        item = dict(zip(headers, row))
        dept = item["Department"]
        env = item["Environment"]
        cost = item["MonthlyCost"]

        if dept not in dept_costs:
            dept_costs[dept] = 0
        dept_costs[dept] += cost

        if env not in env_costs:
            env_costs[env] = 0
        env_costs[env] += cost

    dept_results = [{"department": k, "monthly_cost": round(v, 2)} for k, v in sorted(dept_costs.items(), key=lambda x: x[1], reverse=True)]
    env_results = [{"environment": k, "monthly_cost": round(v, 2)} for k, v in sorted(env_costs.items(), key=lambda x: x[1], reverse=True)]

    total_cost = sum(dept_costs.values())

    return json.dumps({
        "analysis": "Azure Resource Cost Analysis",
        "by_department": dept_results,
        "by_environment": env_results,
        "total_monthly_cost": round(total_cost, 2)
    }, indent=2)


@mcp.tool()
async def query_data(ctx: Context, workbook_name: str, filter_column: str = None, filter_value: str = None) -> str:
    """Query data from a workbook with optional filtering.

    Args:
        workbook_name: Name of the workbook to query
        filter_column: Column name to filter by (optional)
        filter_value: Value to filter for (optional)
    """
    if workbook_name not in SAMPLE_DATA:
        available = list(SAMPLE_DATA.keys())
        return json.dumps({"error": f"Workbook '{workbook_name}' not found. Available: {available}"})

    data = SAMPLE_DATA[workbook_name]
    headers = data["headers"]
    rows = data["rows"]

    # Apply filter if specified
    if filter_column and filter_value:
        if filter_column not in headers:
            return json.dumps({"error": f"Column '{filter_column}' not found. Available: {headers}"})

        col_idx = headers.index(filter_column)
        filtered_rows = [row for row in rows if str(row[col_idx]).lower() == str(filter_value).lower()]
    else:
        filtered_rows = rows

    # Convert to list of dicts
    results = [dict(zip(headers, row)) for row in filtered_rows]

    return json.dumps({
        "workbook": workbook_name,
        "filter": {"column": filter_column, "value": filter_value} if filter_column else None,
        "row_count": len(results),
        "data": results
    }, indent=2)


# Expose ASGI app
mcp_asgi = mcp.http_app()
app = Starlette(
    routes=[Mount("/excel", app=mcp_asgi)],
    lifespan=mcp_asgi.lifespan,
)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Excel Analytics MCP Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
    args = parser.parse_args()
    print(f"Starting Excel Analytics MCP Server on {args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port)
