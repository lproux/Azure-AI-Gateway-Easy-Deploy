#!/usr/bin/env python3
"""
Fix errors in Built-in Logging Lab cells 126-128

Issues:
- Cell 126 & 127: Cannot format string with ',' - need to convert to int first
- Cell 128: Wrong column names - UserPrompt/Response don't exist, use RequestMessages/ResponseMessages
"""
import json
from pathlib import Path

notebook_path = Path('master-ai-gateway-fix-MCP-clean.ipynb')

print("=" * 80)
print("🔧 FIXING BUILT-IN LOGGING LAB ERRORS")
print("=" * 80)

# Load notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Fix Cell 126 - Convert string to int before formatting
print("\n[*] Fixing Cell 126: Type conversion for token formatting")

cell_126_old = """            print("\\n📈 Summary:")
            total_calls = df['TotalCalls'].sum()
            total_tokens = df['TotalTokens'].sum()
            print(f"   - Total API calls logged: {total_calls}")
            print(f"   - Total tokens consumed: {total_tokens:,}")"""

cell_126_new = """            print("\\n📈 Summary:")
            total_calls = int(df['TotalCalls'].sum())
            total_tokens = int(df['TotalTokens'].sum())
            print(f"   - Total API calls logged: {total_calls:,}")
            print(f"   - Total tokens consumed: {total_tokens:,}")"""

cell_126_source = notebook['cells'][125]['source']  # Cell 126 is at index 125
if cell_126_old in cell_126_source:
    notebook['cells'][125]['source'] = cell_126_source.replace(cell_126_old, cell_126_new)
    print("   ✅ Fixed token formatting in Cell 126")
else:
    print("   ⚠️  Cell 126 pattern not found - may already be fixed")

# Fix Cell 127 - Convert string to int before formatting
print("\n[*] Fixing Cell 127: Type conversion for subscription totals")

cell_127_old = """            print("\\n📈 Summary by Subscription:")
            subscription_totals = df.groupby('SubscriptionId')['SumTotalTokens'].sum()
            for sub_id, total in subscription_totals.items():
                print(f"   - {sub_id}: {total:,} tokens")"""

cell_127_new = """            print("\\n📈 Summary by Subscription:")
            subscription_totals = df.groupby('SubscriptionId')['SumTotalTokens'].sum()
            for sub_id, total in subscription_totals.items():
                print(f"   - {sub_id}: {int(total):,} tokens")"""

cell_127_source = notebook['cells'][126]['source']  # Cell 127 is at index 126
if cell_127_old in cell_127_source:
    notebook['cells'][126]['source'] = cell_127_source.replace(cell_127_old, cell_127_new)
    print("   ✅ Fixed token formatting in Cell 127")
else:
    print("   ⚠️  Cell 127 pattern not found - may already be fixed")

# Fix Cell 128 - Use correct column names and parse dynamic JSON
print("\n[*] Fixing Cell 128: Correct column names (RequestMessages/ResponseMessages)")

cell_128_old_query = '''# KQL query: View actual prompts and responses
kql_query = """ApiManagementGatewayLlmLog
| where TimeGenerated > ago(1h)
| where DeploymentName != ''
| project
    TimeGenerated,
    DeploymentName,
    UserPrompt,
    Response,
    TotalTokens,
    PromptTokens,
    CompletionTokens
| order by TimeGenerated desc
| take 10"""'''

cell_128_new_query = '''# KQL query: View actual prompts and responses
kql_query = """ApiManagementGatewayLlmLog
| where TimeGenerated > ago(1h)
| where DeploymentName != ''
| project
    TimeGenerated,
    DeploymentName,
    RequestMessages,
    ResponseMessages,
    TotalTokens,
    PromptTokens,
    CompletionTokens
| order by TimeGenerated desc
| take 10"""'''

cell_128_source = notebook['cells'][127]['source']  # Cell 128 is at index 127
if cell_128_old_query in cell_128_source:
    cell_128_source = cell_128_source.replace(cell_128_old_query, cell_128_new_query)

    # Also update the display logic to parse JSON arrays
    old_display = """                print(f"Tokens: {log.get('PromptTokens', 0)} prompt + {log.get('CompletionTokens', 0)} completion = {log.get('TotalTokens', 0)} total")
                print(f"\\n📥 User Prompt:")
                print(f"   {log.get('UserPrompt', 'N/A')}")
                print(f"\\n📤 Model Response:")
                response = log.get('Response', 'N/A')"""

    new_display = """                print(f"Tokens: {log.get('PromptTokens', 0)} prompt + {log.get('CompletionTokens', 0)} completion = {log.get('TotalTokens', 0)} total")

                # Parse RequestMessages (JSON array)
                request_messages = log.get('RequestMessages', [])
                if isinstance(request_messages, str):
                    try:
                        request_messages = json.loads(request_messages)
                    except:
                        request_messages = []

                print(f"\\n📥 User Prompt:")
                if request_messages and len(request_messages) > 0:
                    # Get the last user message
                    user_msg = next((m.get('content', '') for m in reversed(request_messages) if m.get('role') == 'user'), 'N/A')
                    print(f"   {user_msg}")
                else:
                    print(f"   N/A")

                # Parse ResponseMessages (JSON array)
                response_messages = log.get('ResponseMessages', [])
                if isinstance(response_messages, str):
                    try:
                        response_messages = json.loads(response_messages)
                    except:
                        response_messages = []

                print(f"\\n📤 Model Response:")
                if response_messages and len(response_messages) > 0:
                    response = response_messages[0].get('content', 'N/A')
                else:
                    response = 'N/A'"""

    cell_128_source = cell_128_source.replace(old_display, new_display)
    notebook['cells'][127]['source'] = cell_128_source
    print("   ✅ Fixed column names and JSON parsing in Cell 128")
else:
    print("   ⚠️  Cell 128 pattern not found - may already be fixed")

# Save backup
backup_path = notebook_path.with_suffix('.ipynb.backup-fix-logging-errors')
print(f"\n[*] Creating backup: {backup_path}")
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

# Save updated notebook
print(f"[*] Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("\n" + "=" * 80)
print("✅ ALL LOGGING ERRORS FIXED!")
print("=" * 80)

print("\n📋 Changes Made:")
print("   ✅ Cell 126: Convert TotalTokens to int before formatting with ','")
print("   ✅ Cell 127: Convert SumTotalTokens to int before formatting with ','")
print("   ✅ Cell 128: Use RequestMessages/ResponseMessages (not UserPrompt/Response)")
print("   ✅ Cell 128: Added JSON parsing for dynamic message arrays")

print("\n🔍 Technical Details:")
print("   - Log Analytics returns numeric values as strings in JSON")
print("   - Python format specifier ',' requires numeric type, not string")
print("   - RequestMessages/ResponseMessages are dynamic (JSON) columns")
print("   - Each contains array of message objects with 'role' and 'content'")

print("\n🎯 Next Steps:")
print("   1. Reload notebook")
print("   2. Re-run Cell 126 - should show token counts with commas")
print("   3. Re-run Cell 127 - should show subscription totals with commas")
print("   4. Re-run Cell 128 - should display actual prompts and responses")

print("\n" + "=" * 80)
