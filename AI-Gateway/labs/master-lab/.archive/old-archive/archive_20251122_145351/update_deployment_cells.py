#!/usr/bin/env python3
"""
Update deployment cells in clean notebook to properly capture outputs.
"""

import json
from pathlib import Path

# Load notebooks
SOURCE_NB = Path('master-ai-gateway-fix-MCP.ipynb')
CLEAN_NB = Path('master-ai-gateway-fix-MCP-clean.ipynb')

print(f"Loading source notebook: {SOURCE_NB}")
with open(SOURCE_NB, 'r', encoding='utf-8') as f:
    source_nb = json.load(f)

print(f"Loading clean notebook: {CLEAN_NB}")
with open(CLEAN_NB, 'r', encoding='utf-8') as f:
    clean_nb = json.load(f)

print(f"Source: {len(source_nb['cells'])} cells")
print(f"Clean: {len(clean_nb['cells'])} cells")

# Cell indices in clean notebook to update
# Cell 16-19: Deployment cells (currently cells 17-20 in 0-indexed)
# Cell 21: Env generation (currently cell 22 in 0-indexed)

# Get source cells for deployment (26-28 contain the full deployment logic)
print("\nUpdating deployment cells...")

# Replace cells 17-20 with source cells 26-29 (which have the full deployment + output capture)
# Clean notebook structure:
# Cell 15: Deployment Config (0-indexed 16)
# Cell 16: Deploy Infrastructure Header (0-indexed 17)
# Cell 17-20: Deployment code (0-indexed 18-21)

# Source cells:
# Cell 26: Deployment initialization
# Cell 27: Deployment header (skip, we have this)
# Cell 28: Main deployment with output capture
# Cell 29: Additional deployment

# Let's replace clean cells 18-21 with source cells 26, 28, 29
# First, remove old cells 18-21
print("  Removing old deployment cells 18-21...")
for i in range(4):
    if len(clean_nb['cells']) > 18:
        del clean_nb['cells'][18]

# Insert source cells 26, 28, 29
print("  Inserting source cell 26 (auth setup)...")
cell_26 = source_nb['cells'][26].copy()
cell_26['execution_count'] = None
cell_26['outputs'] = []
clean_nb['cells'].insert(18, cell_26)

print("  Inserting source cell 28 (main deployment with output capture)...")
cell_28 = source_nb['cells'][28].copy()
cell_28['execution_count'] = None
cell_28['outputs'] = []
clean_nb['cells'].insert(19, cell_28)

print("  Inserting source cell 29 (additional deployment)...")
cell_29 = source_nb['cells'][29].copy()
cell_29['execution_count'] = None
cell_29['outputs'] = []
clean_nb['cells'].insert(20, cell_29)

# Now update the env generation cell
# Find cell 021 (generate master-lab.env) - should be around index 23-24 now
print("\nUpdating env generation cell...")

# Find the cell with "CRITICAL" and "Generate master-lab.env" in it
env_gen_idx = None
for i, cell in enumerate(clean_nb['cells']):
    if cell['cell_type'] == 'markdown':
        source_text = ''.join(cell.get('source', []))
        if 'CRITICAL' in source_text and 'Generate master-lab.env' in source_text:
            env_gen_idx = i + 1  # The code cell is next
            break

if env_gen_idx:
    print(f"  Found env generation cell at index {env_gen_idx}")

    # Replace with source cell 31 (complete env generation)
    cell_31 = source_nb['cells'][31].copy()
    cell_31['execution_count'] = None
    cell_31['outputs'] = []
    clean_nb['cells'][env_gen_idx] = cell_31
    print("  Replaced with source cell 31 (comprehensive env generation)")
else:
    print("  WARNING: Could not find env generation cell")

# Save updated notebook
print(f"\nSaving updated notebook: {CLEAN_NB}")
with open(CLEAN_NB, 'w', encoding='utf-8') as f:
    json.dump(clean_nb, f, indent=1, ensure_ascii=False)

print(f"\n✓ Clean notebook updated successfully!")
print(f"  Total cells: {len(clean_nb['cells'])}")
print("\nUpdated cells:")
print("  - Cells 17-20: Full deployment with output capture (from source cells 26, 28, 29)")
print("  - Cell 021: Comprehensive env generation (from source cell 31)")
