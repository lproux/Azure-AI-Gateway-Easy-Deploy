#!/usr/bin/env python3
"""
Update Cell 72 to use chat_client and embeddings_client from Cell 71
"""
import json
from pathlib import Path

notebook_path = Path('master-ai-gateway-fix-MCP-clean.ipynb')

print("=" * 80)
print("📝 UPDATING CELL 72 TO USE CORRECT CLIENTS")
print("=" * 80)

# Load notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Read current Cell 72
current_cell_72 = ''.join(notebook['cells'][71].get('source', []))

# Replace client with embeddings_client and chat_client
updated_cell_72 = current_cell_72.replace(
    'embedding_response = client.embeddings.create(',
    'embedding_response = embeddings_client.embeddings.create('
).replace(
    'response = client.chat.completions.create(',
    'response = chat_client.chat.completions.create('
)

# Update the cell
notebook['cells'][71]['source'] = updated_cell_72

# Save backup
backup_path = notebook_path.with_suffix('.ipynb.backup-cell72-clients')
print(f"\n[*] Creating backup: {backup_path}")
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

# Save updated notebook
print(f"[*] Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("\n" + "=" * 80)
print("✅ CELL 72 UPDATED TO USE CORRECT CLIENTS!")
print("=" * 80)
print("\nChanges Made:")
print("  ✅ Query embeddings use 'embeddings_client' (direct endpoint)")
print("  ✅ Chat completions use 'chat_client' (APIM with caching)")
print("\n💡 Result:")
print("  - Embeddings: Direct calls, no policy interference")
print("  - Chat: Through APIM with semantic caching")
print("=" * 80)
