#!/usr/bin/env python3
"""
Analyze notebook structure to identify all lab cells for testing
"""

import json
import os

notebook_path = 'master-ai-gateway.ipynb'

print('=' * 70)
print('NOTEBOOK STRUCTURE ANALYSIS')
print('=' * 70)
print()

# Load notebook
with open(notebook_path, encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']
print(f'[*] Total cells: {len(cells)}')
print()

# Find lab cells
lab_cells = {}
current_lab = None

for i, cell in enumerate(cells):
    source = ''.join(cell.get('source', []))

    # Check if this is a lab header
    if source.startswith('# Lab '):
        # Extract lab number
        lines = source.split('\n')
        first_line = lines[0]

        # Parse lab number (e.g., "# Lab 01:", "# Lab 1:")
        if ':' in first_line:
            lab_part = first_line.split(':')[0].strip()
            lab_num = lab_part.replace('# Lab ', '').strip()
            current_lab = f'Lab {lab_num}'

            if current_lab not in lab_cells:
                lab_cells[current_lab] = {
                    'header_cell': i,
                    'title': first_line.replace('#', '').strip(),
                    'cells': []
                }

            print(f'[*] Found {current_lab} at cell {i}')
            print(f'    Title: {lab_cells[current_lab]["title"]}')

    # If we're in a lab section, track the cell
    elif current_lab:
        # Check if we've moved to a new section (e.g., "# Deployment", "# Configuration")
        if source.startswith('# ') and not source.startswith('## '):
            # Only break if it's a major section, not a subsection
            if any(keyword in source.lower() for keyword in ['deployment', 'configuration', 'setup', 'prerequisites']):
                if not source.startswith('# Lab'):
                    current_lab = None
                    continue

        # Add this cell to current lab
        lab_cells[current_lab]['cells'].append({
            'index': i,
            'type': cell['cell_type'],
            'source_preview': source[:100] if source else '(empty)'
        })

print()
print('=' * 70)
print('LAB SUMMARY')
print('=' * 70)

for lab_name in sorted(lab_cells.keys(), key=lambda x: int(x.split()[1])):
    lab_info = lab_cells[lab_name]
    code_cells = [c for c in lab_info['cells'] if c['type'] == 'code']
    markdown_cells = [c for c in lab_info['cells'] if c['type'] == 'markdown']

    print(f'\n{lab_name}:')
    print(f'  Title: {lab_info["title"]}')
    print(f'  Header cell: {lab_info["header_cell"]}')
    print(f'  Total cells: {len(lab_info["cells"])} ({len(code_cells)} code, {len(markdown_cells)} markdown)')

    if code_cells:
        print(f'  Code cells: {[c["index"] for c in code_cells[:5]]}{"..." if len(code_cells) > 5 else ""}')

print()
print('=' * 70)
print('DETAILED CELL LIST FOR LABS 1-10')
print('=' * 70)

for lab_num in range(1, 11):
    lab_name = f'Lab {lab_num:02d}'
    if lab_name not in lab_cells:
        lab_name = f'Lab {lab_num}'

    if lab_name in lab_cells:
        lab_info = lab_cells[lab_name]
        print(f'\n{lab_name}: {lab_info["title"]}')
        print(f'  Header: Cell {lab_info["header_cell"]}')

        for cell_info in lab_info['cells']:
            cell_type = cell_info['type']
            cell_idx = cell_info['index']
            preview = cell_info['source_preview'].replace('\n', ' ')[:80]

            if cell_type == 'code':
                print(f'  [{cell_idx:3d}] CODE: {preview}')

# Save structure to JSON for programmatic testing
output = {
    'total_cells': len(cells),
    'labs': {}
}

for lab_name, lab_info in lab_cells.items():
    output['labs'][lab_name] = {
        'title': lab_info['title'],
        'header_cell': lab_info['header_cell'],
        'code_cells': [c['index'] for c in lab_info['cells'] if c['type'] == 'code'],
        'markdown_cells': [c['index'] for c in lab_info['cells'] if c['type'] == 'markdown']
    }

with open('notebook_structure.json', 'w') as f:
    json.dump(output, f, indent=2)

print()
print('[OK] Structure saved to notebook_structure.json')
