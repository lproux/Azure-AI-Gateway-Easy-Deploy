#!/usr/bin/env python3
"""Analyze cells 57-90 to understand current content"""
import json
from pathlib import Path

notebook_path = Path('master-ai-gateway.ipynb')

print("=" * 80)
print("ANALYZING CELLS 57-90")
print("=" * 80)
print()

with open(notebook_path, encoding='utf-8') as f:
    nb = json.load(f)

# Analyze each batch
batches = [
    (57, 62, "Additional Weather Examples"),
    (63, 68, "OnCall/GitHub Integration"),
    (69, 74, "Spotify Integration"),
    (75, 80, "E-commerce (Product/Order)"),
    (81, 86, "MS Learn Integration"),
    (87, 90, "Advanced MCP Patterns")
]

for start, end, title in batches:
    print(f"\n{'=' * 80}")
    print(f"BATCH: {title} (Cells {start}-{end})")
    print('=' * 80)

    for i in range(start, end + 1):
        if i >= len(nb['cells']):
            print(f"\nCell {i}: [BEYOND NOTEBOOK LENGTH]")
            continue

        cell = nb['cells'][i]
        cell_type = cell.get('cell_type', 'unknown')
        source = ''.join(cell.get('source', []))

        print(f"\nCell {i} ({cell_type}):")
        if cell_type == 'markdown':
            print(f"  {source[:100]}...")
        else:
            # For code cells, show first 150 chars
            preview = source[:150].replace('\n', ' ')
            print(f"  {preview}...")

            # Try to identify key patterns
            if 'MCP' in source or 'mcp' in source:
                print(f"  [Contains MCP references]")
            if 'client' in source.lower():
                print(f"  [Contains client code]")
            if 'async' in source or 'await' in source:
                print(f"  [Contains async code]")
            if 'import' in source:
                print(f"  [Contains imports]")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
