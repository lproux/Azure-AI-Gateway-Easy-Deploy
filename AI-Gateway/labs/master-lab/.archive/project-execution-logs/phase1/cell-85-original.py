# Exercise 2.3: Azure Cost Analysis via Local Pandas
print("💰 Azure Cost Analysis via Local Pandas + Azure OpenAI")
print("=" * 80)

from pathlib import Path
import pandas as pd

try:
    # FIXED: Use CSV file instead of encrypted Excel file
    cost_file_path = Path("./sample-data/csv/azure_resource_costs.csv")
    if not cost_file_path.exists():
        raise FileNotFoundError(f"Cost file not found at '{cost_file_path.resolve()}'")

    print(f"✅ Reading cost file locally: {cost_file_path.name}")
    
    # Read CSV file using pandas
    df = pd.read_csv(cost_file_path)
    
    print(f"✅ File loaded successfully: {len(df)} rows, {len(df.columns)} columns")
    
    # Display columns
    print(f"\n📊 Columns: {df.columns.tolist()}")
    
    # Preview data
    print("\n👀 Preview (first 3 rows):")
    print(df.head(3).to_string())

    # Determine column names (case-insensitive search)
    group_by_col = None
    metric_col = None
    
    # Look for ResourceType or ResourceName for grouping
    for col in df.columns:
        if 'resourcetype' in col.lower() or ('resource' in col.lower() and 'type' in col.lower()):
            group_by_col = col
        if 'cost' in col.lower():
            metric_col = col
    
    if not group_by_col:
        # Try ResourceName as fallback
        for col in df.columns:
            if 'resourcename' in col.lower() or 'resource' in col.lower():
                group_by_col = col
                break
    
    if not group_by_col or not metric_col:
        print(f"⚠️ Warning: Could not auto-detect columns. Available: {df.columns.tolist()}")
        # Use defaults if detection fails
        group_by_col = group_by_col or df.columns[0]
        metric_col = metric_col or df.columns[1] if len(df.columns) > 1 else df.columns[0]

    print(f"\n📈 Analyzing costs with group_by='{group_by_col}' and metric='{metric_col}'")

    # Group by service and sum costs
    cost_breakdown = df.groupby(group_by_col)[metric_col].agg(['sum', 'mean', 'count']).reset_index()
    cost_breakdown.columns = ['ServiceName', 'Total', 'Average', 'Count']
    cost_breakdown = cost_breakdown.sort_values('Total', ascending=False)
    
    # Calculate totals
    total_cost = cost_breakdown['Total'].sum()

    # Assuming the data represents daily costs, calculate a monthly projection
    monthly_projection = total_cost * 30

    print("\n💵 Cost Analysis Summary:")
    print("=" * 80)
    print("📊 Cost Breakdown by Service Name:")
    for idx, row in cost_breakdown.iterrows():
        print(f"  - {row['ServiceName']}: ${row['Total']:,.2f} (Avg: ${row['Average']:,.2f}, Count: {row['Count']})")

    print(f"\n💰 Total Daily Cost: ${total_cost:,.2f}")
    print(f"📅 Projected Monthly Cost: ${monthly_projection:,.2f}")

    # Create a compact summary for AI analysis
    cost_data_info = f"""Total Daily Cost: ${total_cost:,.2f}
Projected Monthly Cost: ${monthly_projection:,.2f}
Top Service: {cost_breakdown.iloc[0]['ServiceName']} (${cost_breakdown.iloc[0]['Total']:,.2f})
Number of Services: {len(cost_breakdown)}"""

    print("\n📋 Compact cost_data_info for AI prompts:")
    print(cost_data_info)

except Exception as e:
    print(f"❌ ERROR (Cost Analysis): {e}")
    print("🔍 Troubleshooting:")
    print("  • Ensure the cost file exists at './sample-data/csv/azure_resource_costs.csv'")
    print("  • Verify the file is a valid CSV format")
    print("  • Check that pandas is installed: pip install pandas")
    import traceback
    traceback.print_exc()
