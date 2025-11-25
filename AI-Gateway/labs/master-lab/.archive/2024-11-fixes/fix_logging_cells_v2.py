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

cell_126_source = notebook['cells'][125]['source']  # Cell 126 is at index 125
cell_126_str = ''.join(cell_126_source) if isinstance(cell_126_source, list) else cell_126_source

# Find and replace the problematic lines
old_lines_126 = [
    "            total_calls = df['TotalCalls'].sum()\n",
    "            total_tokens = df['TotalTokens'].sum()\n",
    "            print(f\"   - Total API calls logged: {total_calls}\")\n",
    "            print(f\"   - Total tokens consumed: {total_tokens:,}\")\n"
]

new_lines_126 = [
    "            total_calls = int(df['TotalCalls'].sum())\n",
    "            total_tokens = int(df['TotalTokens'].sum())\n",
    "            print(f\"   - Total API calls logged: {total_calls:,}\")\n",
    "            print(f\"   - Total tokens consumed: {total_tokens:,}\")\n"
]

# Replace in the source array
if isinstance(cell_126_source, list):
    for i, line in enumerate(cell_126_source):
        if line == old_lines_126[0]:
            # Replace the 4 lines
            for j in range(4):
                if i+j < len(cell_126_source):
                    cell_126_source[i+j] = new_lines_126[j]
            break
    notebook['cells'][125]['source'] = cell_126_source
    print("   ✅ Fixed token formatting in Cell 126")

# Fix Cell 127 - Convert string to int before formatting
print("\n[*] Fixing Cell 127: Type conversion for subscription totals")

cell_127_source = notebook['cells'][126]['source']  # Cell 127 is at index 126

# Find and replace
old_line_127 = "                print(f\"   - {sub_id}: {total:,} tokens\")\n"
new_line_127 = "                print(f\"   - {sub_id}: {int(total):,} tokens\")\n"

if isinstance(cell_127_source, list):
    for i, line in enumerate(cell_127_source):
        if line == old_line_127:
            cell_127_source[i] = new_line_127
            break
    notebook['cells'][126]['source'] = cell_127_source
    print("   ✅ Fixed token formatting in Cell 127")

# Fix Cell 128 - Use correct column names
print("\n[*] Fixing Cell 128: Correct column names and JSON parsing")

cell_128_source = notebook['cells'][127]['source']  # Cell 128 is at index 127

# Replace column names in KQL query
replacements_128 = [
    ("    UserPrompt,\n", "    RequestMessages,\n"),
    ("    Response,\n", "    ResponseMessages,\n"),
]

if isinstance(cell_128_source, list):
    for i, line in enumerate(cell_128_source):
        for old, new in replacements_128:
            if line == old:
                cell_128_source[i] = new
                print(f"   ✅ Replaced '{old.strip()}' with '{new.strip()}'")

    # Replace the display logic - find the section that prints UserPrompt and Response
    for i, line in enumerate(cell_128_source):
        if 'print(f"Tokens: {log.get' in line:
            # Found the start - replace the next several lines
            # This is complex, so let's rebuild this section
            new_section = [
                "                print(f\"Tokens: {log.get('PromptTokens', 0)} prompt + {log.get('CompletionTokens', 0)} completion = {log.get('TotalTokens', 0)} total\")\n",
                "\n",
                "                # Parse RequestMessages (JSON array)\n",
                "                request_messages = log.get('RequestMessages', [])\n",
                "                if isinstance(request_messages, str):\n",
                "                    try:\n",
                "                        request_messages = json.loads(request_messages)\n",
                "                    except:\n",
                "                        request_messages = []\n",
                "\n",
                "                print(f\"\\n📥 User Prompt:\")\n",
                "                if request_messages and len(request_messages) > 0:\n",
                "                    # Get the last user message\n",
                "                    user_msg = next((m.get('content', '') for m in reversed(request_messages) if m.get('role') == 'user'), 'N/A')\n",
                "                    print(f\"   {user_msg}\")\n",
                "                else:\n",
                "                    print(f\"   N/A\")\n",
                "\n",
                "                # Parse ResponseMessages (JSON array)\n",
                "                response_messages = log.get('ResponseMessages', [])\n",
                "                if isinstance(response_messages, str):\n",
                "                    try:\n",
                "                        response_messages = json.loads(response_messages)\n",
                "                    except:\n",
                "                        response_messages = []\n",
                "\n",
                "                print(f\"\\n📤 Model Response:\")\n",
                "                if response_messages and len(response_messages) > 0:\n",
                "                    response = response_messages[0].get('content', 'N/A')\n",
                "                else:\n",
                "                    response = 'N/A'\n",
            ]

            # Find where to end replacement (the line with "Truncate long responses")
            end_idx = i + 1
            for j in range(i+1, len(cell_128_source)):
                if "# Truncate long responses" in cell_128_source[j]:
                    end_idx = j
                    break

            # Replace the section
            cell_128_source = cell_128_source[:i] + new_section + cell_128_source[end_idx:]
            break

    notebook['cells'][127]['source'] = cell_128_source
    print("   ✅ Fixed JSON parsing in Cell 128")

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
print("   ✅ Cell 126: int(total_calls) and int(total_tokens) before formatting")
print("   ✅ Cell 127: int(total) before formatting")
print("   ✅ Cell 128: UserPrompt → RequestMessages, Response → ResponseMessages")
print("   ✅ Cell 128: Added JSON parsing for dynamic message arrays")

print("\n🎯 Next Steps:")
print("   1. Reload notebook")
print("   2. Re-run Cells 126-128 - all errors should be resolved")

print("\n" + "=" * 80)
