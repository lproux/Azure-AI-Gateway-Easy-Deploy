# Exercise 2.1: Sales Analysis via Local Pandas (NO MCP upload)
print(" Sales Analysis via Local Pandas + Azure OpenAI")
print("=" * 80)

from pathlib import Path
import pandas as pd
import json

try:
    # Identify local Excel source relative to the notebook's location
    search_path = Path("./sample-data/excel/")
    excel_candidates = list(search_path.glob("*sales*.xlsx"))
    if not excel_candidates:
        raise FileNotFoundError(f"Could not locate a local Excel sales file in '{search_path.resolve()}'")

    local_excel_path = Path(excel_candidates[0])
    excel_file_name = local_excel_path.name

    print(f" Reading Excel file locally: {excel_file_name}")
    
    # Read Excel file using pandas with openpyxl engine (fixes xlrd and zip errors)
    df = pd.read_excel(local_excel_path, engine='openpyxl')
    
    print(f" File loaded successfully: {len(df)} rows, {len(df.columns)} columns")

    # Display column information
    columns = df.columns.tolist()
    print("\n Columns:")
    print(columns)
    
    # Display preview
    print("\n Preview (first 5 rows):")
    for idx, row in df.head(5).iterrows():
        print(f"  Row {idx + 1}: {dict(row)}")

    # Perform sales analysis (group by Region, sum TotalSales)
    print("\n Running sales analysis (group by 'Region', metric 'TotalSales')...")
    
    # Determine the correct column names (case-insensitive search)
    region_col = None
    sales_col = None
    
    for col in df.columns:
        if 'region' in col.lower():
            region_col = col
        if 'total' in col.lower() and 'sales' in col.lower():
            sales_col = col
    
    if not region_col or not sales_col:
        print(f" Warning: Could not find Region or TotalSales columns. Using first two columns.")
        region_col = df.columns[0]
        sales_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
    
    print(f" Using columns: group_by='{region_col}', metric='{sales_col}'")
    
    # Group by region and sum sales
    grouped = df.groupby(region_col)[sales_col].agg(['sum', 'mean', 'count']).reset_index()
    grouped.columns = ['Region', 'Total', 'Average', 'Count']
    grouped = grouped.sort_values('Total', ascending=False)
    
    # Calculate totals
    total_sales = grouped['Total'].sum()
    avg_sales = df[sales_col].mean()
    num_transactions = len(df)

    print("\n Sales Analysis Summary:")
    print("=" * 80)
    print(f" Total Sales: ${total_sales:,.2f}")
    print(f" Average Sale: ${avg_sales:,.2f}")
    print(f" Number of Transactions: {num_transactions}")
    
    print("\n Sales by Region (Top 10):")
    for i, row in grouped.head(10).iterrows():
        print(f"  {i+1:02d}. {row['Region']}: ${row['Total']:,.2f} (Avg: ${row['Average']:,.2f}, Count: {row['Count']})")

    # Create compact summary for AI prompts
    sales_data_info = f"""Columns: {columns}
Total Sales: ${total_sales:,.2f} | Avg Sale: ${avg_sales:,.2f} | Transactions: {num_transactions}
Regional breakdown available (Top region: {grouped.iloc[0]['Region']} with ${grouped.iloc[0]['Total']:,.2f})"""

    print("\n Compact sales_data_info for AI prompts:")
    print(sales_data_info)

    # Export for later cells
    excel_cache_key = str(local_excel_path)  # For compatibility

except Exception as e:
    print(f" ERROR (Sales Analysis): {e}")
    print(" Troubleshooting:")
    print("  • Verify Excel file exists at './sample-data/excel/*sales*.xlsx'")
    print("  • Ensure the file is a valid .xlsx format")
    print("  • Check that openpyxl is installed: pip install openpyxl")
    import traceback
    traceback.print_exc()
