#!/usr/bin/env python3
"""
Add semantic caching policy application cell before cell 53
"""
import json
from pathlib import Path

notebook_path = Path('master-ai-gateway-fix-MCP-clean.ipynb')

print("=" * 80)
print("📝 ADDING SEMANTIC CACHING POLICY CELL")
print("=" * 80)

# Load notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

print(f"\nCurrent notebook has {len(notebook['cells'])} cells")

# Read the cell code
with open('CELL_TO_ADD_SEMANTIC_CACHING.py', 'r') as f:
    cell_code = f.read()

# Create new cell
new_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": cell_code
}

# Insert before cell 53 (so it becomes new cell 52)
insert_position = 52
print(f"\nInserting new cell at position {insert_position}")
print("This will be the policy application cell for semantic caching")

notebook['cells'].insert(insert_position, new_cell)

# Save backup
backup_path = notebook_path.with_suffix('.ipynb.backup-add-policy-cell')
print(f"\nCreating backup: {backup_path}")
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

# Save updated notebook
print(f"Saving updated notebook: {notebook_path}")
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f"\n✅ Cell added successfully!")
print(f"New notebook has {len(notebook['cells'])} cells")
print("\n📋 Changes:")
print(f"   - New Cell 52: Apply Semantic Caching Policy")
print(f"   - Old Cell 53 → New Cell 54: Semantic Caching Test")
print(f"   - Old Cell 54 → New Cell 55: Visualization")
print(f"   - And so on...")

print("\n🎯 Next Steps:")
print("   1. Open the notebook")
print("   2. Run NEW Cell 52 to apply the policy")
print("   3. Wait 10 seconds (automatic)")
print("   4. Run NEW Cell 54 to test semantic caching")
print("   5. Expected: 19/20 requests successful with fast cache hits")

print("\n" + "=" * 80)
