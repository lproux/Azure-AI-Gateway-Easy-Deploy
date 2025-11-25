#!/usr/bin/env python3
"""
Add OpenAI client initialization to Cell 79 and subsequent test cells
"""
import json
from pathlib import Path

notebook_path = Path('master-ai-gateway-fix-MCP-clean.ipynb')

print("=" * 80)
print("📝 FIXING CELL 79+ TO REINITIALIZE OPENAI CLIENT")
print("=" * 80)

# Load notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Client initialization code to prepend
client_init = """# Reinitialize OpenAI client (overwritten by Cosmos DB cells)
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=f"{apim_gateway_url}/{inference_api_path}",
    api_key=apim_api_key,
    api_version="2024-08-01-preview"
)

"""

# Find Cell 79 (index 78) - Streaming test
cell_79_idx = 78
current_source = ''.join(notebook['cells'][cell_79_idx].get('source', []))

# Check if client initialization already exists
if 'client = AzureOpenAI' not in current_source:
    # Prepend client initialization
    updated_source = client_init + current_source
    notebook['cells'][cell_79_idx]['source'] = updated_source
    print(f"\n✅ Cell 79 (index {cell_79_idx}): Added OpenAI client initialization")
else:
    print(f"\n✓ Cell 79 (index {cell_79_idx}): Already has client initialization")

# Check subsequent cells that might also need the client
cells_to_check = [
    (79, "Test 3"),
    (80, "Test 4"),
    (81, "Test 5"),
]

for idx, name in cells_to_check:
    if idx < len(notebook['cells']):
        source = ''.join(notebook['cells'][idx].get('source', []))
        # Check if this cell uses 'client.' and doesn't initialize it
        if 'client.' in source and 'client = AzureOpenAI' not in source:
            updated_source = client_init + source
            notebook['cells'][idx]['source'] = updated_source
            print(f"✅ Cell {idx+1} ({name}): Added OpenAI client initialization")

# Save backup
backup_path = notebook_path.with_suffix('.ipynb.backup-fix-cell79')
print(f"\n[*] Creating backup: {backup_path}")
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

# Save updated notebook
print(f"[*] Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("\n" + "=" * 80)
print("✅ CELLS UPDATED WITH OPENAI CLIENT INITIALIZATION!")
print("=" * 80)
print("\nChanges Made:")
print("  ✅ Cell 79+ now reinitialize OpenAI client")
print("  ✅ Fixes 'CosmosClient' has no attribute 'chat' error")
print("\n💡 Why This Works:")
print("  - CosmosClient overwrote 'client' variable in Cell 65")
print("  - Lab 01 test cells now recreate OpenAI client")
print("  - Each test section is now self-contained")
print("\n🎯 Next Steps:")
print("  1. Reload notebook")
print("  2. Run Cell 79 (streaming test)")
print("  3. Should work without errors")
print("=" * 80)
