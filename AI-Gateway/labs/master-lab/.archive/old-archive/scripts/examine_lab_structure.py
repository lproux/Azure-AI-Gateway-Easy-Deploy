#!/usr/bin/env python3
"""
Examine notebook structure around lab markers
"""

import json

with open('master-ai-gateway.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Find lab markers
lab_markers = []
for i, cell in enumerate(cells):
    source = ''.join(cell.get('source', []))
    if '<a id=' in source and 'lab' in source.lower():
        lab_id = source.split("'")[1] if "'" in source else source.split('"')[1]
        lab_markers.append((i, lab_id))

print(f'Found {len(lab_markers)} lab markers')
print()

# Show structure around first 5 lab markers
for idx, (cell_idx, lab_id) in enumerate(lab_markers[:5]):
    print(f'\n{"=" * 70}')
    print(f'Lab Marker {idx+1}: {lab_id} at cell {cell_idx}')
    print("=" * 70)

    # Show 5 cells after the marker
    for offset in range(0, 6):
        if cell_idx + offset < len(cells):
            cell = cells[cell_idx + offset]
            cell_type = cell['cell_type']
            source = ''.join(cell.get('source', []))
            preview = source[:150].replace('\n', ' ')

            print(f'\nCell {cell_idx + offset} [{cell_type}]:')
            print(f'  {preview}')

            # For code cells, show first few lines
            if cell_type == 'code' and source:
                lines = source.split('\n')[:3]
                print(f'  First 3 lines:')
                for line in lines:
                    print(f'    {line}')
