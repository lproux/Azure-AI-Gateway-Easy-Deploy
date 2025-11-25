#!/usr/bin/env python3
"""
Comprehensive Cell Testing Framework
Executes all 754 cells in master-ai-gateway.ipynb and documents issues
"""

import json
import os
import sys
import subprocess
import time
from datetime import datetime
from pathlib import Path

print('=' * 80)
print('MASTER AI GATEWAY LAB - COMPREHENSIVE CELL TESTING')
print('=' * 80)
print(f'Started: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print()

# Configuration
NOTEBOOK_PATH = 'master-ai-gateway.ipynb'
TEST_OUTPUT_DIR = 'test_results'
VENV_PYTHON = r'C:\Users\lproux\OneDrive - Microsoft\bkp\Documents\GitHub\.venv\Scripts\python.exe'

# Create output directory
os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

# Load notebook
print('[*] Loading notebook...')
with open(NOTEBOOK_PATH, encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']
total_cells = len(cells)

print(f'[OK] Loaded {total_cells} total cells')
print()

# Analyze cell types
code_cells = [i for i, c in enumerate(cells) if c['cell_type'] == 'code']
markdown_cells = [i for i, c in enumerate(cells) if c['cell_type'] == 'markdown']

print(f'[*] Cell breakdown:')
print(f'    - Code cells: {len(code_cells)}')
print(f'    - Markdown cells: {len(markdown_cells)}')
print()

# Categorize cells by lab
print('[*] Categorizing cells by lab...')
lab_structure = {}
current_lab = None

for i, cell in enumerate(cells):
    source = ''.join(cell.get('source', []))

    # Check for lab markers
    if '<a id=' in source and 'lab' in source.lower():
        if "id='lab" in source or 'id="lab' in source:
            # Extract lab ID
            if "'" in source:
                lab_id = source.split("id='")[1].split("'")[0]
            else:
                lab_id = source.split('id="')[1].split('"')[0]

            current_lab = lab_id

            # Get lab title from next part of cell
            lines = source.split('\n')
            title = lines[0] if lines else f'Lab {lab_id}'

            lab_structure[current_lab] = {
                'title': title.replace('<a id=', '').replace('</a>', '').strip(),
                'start_cell': i,
                'cells': []
            }

    # Add cell to current lab
    if current_lab and cell['cell_type'] == 'code':
        lab_structure[current_lab]['cells'].append(i)

print(f'[OK] Found {len(lab_structure)} labs')
for lab_id, lab_info in sorted(lab_structure.items()):
    print(f'    - {lab_id}: {len(lab_info["cells"])} code cells')
print()

# Test execution strategy
print('=' * 80)
print('TEST EXECUTION STRATEGY')
print('=' * 80)
print()
print('[*] Testing approach:')
print('    1. Execute cells in order (preserve state)')
print('    2. Capture stdout, stderr, and exceptions')
print('    3. Validate outputs match expected patterns')
print('    4. Document all failures with context')
print('    5. Generate comprehensive report')
print()

# Initialize test results
test_results = {
    'notebook': NOTEBOOK_PATH,
    'timestamp': datetime.now().isoformat(),
    'total_cells': total_cells,
    'code_cells': len(code_cells),
    'markdown_cells': len(markdown_cells),
    'labs': lab_structure,
    'execution_results': [],
    'issues': [],
    'summary': {
        'passed': 0,
        'failed': 0,
        'skipped': 0,
        'errors': []
    }
}

# Questions for user
print('=' * 80)
print('BEFORE STARTING - QUESTIONS')
print('=' * 80)
print()
print('[?] Testing Mode Selection:')
print('    A. Execute ALL 754 cells sequentially (comprehensive, ~2-3 hours)')
print('    B. Execute code cells only (~350 cells, ~1 hour)')
print('    C. Execute sample cells from each lab (validation, ~30 mins)')
print('    D. Dry run - analyze only, no execution (~2 mins)')
print()
print('[?] Error Handling:')
print('    1. Stop on first error (debug mode)')
print('    2. Continue on errors, document all (comprehensive mode)')
print()
print('[?] Output Level:')
print('    - Verbose: Show all outputs')
print('    - Summary: Show only errors and summary')
print()

# Save initial analysis
analysis_file = os.path.join(TEST_OUTPUT_DIR, 'notebook_analysis.json')
with open(analysis_file, 'w') as f:
    json.dump({
        'total_cells': total_cells,
        'code_cells': len(code_cells),
        'markdown_cells': len(markdown_cells),
        'labs': {k: {'title': v['title'], 'cell_count': len(v['cells'])}
                 for k, v in lab_structure.items()}
    }, f, indent=2)

print(f'[OK] Analysis saved to {analysis_file}')
print()

# Cell structure breakdown
print('=' * 80)
print('CELL STRUCTURE BREAKDOWN')
print('=' * 80)
print()

# Group cells by type and purpose
setup_cells = []
deployment_cells = []
config_cells = []
lab_cells = []
test_cells = []

for i, cell in enumerate(cells):
    if cell['cell_type'] != 'code':
        continue

    source = ''.join(cell.get('source', []))

    # Categorize by content
    if any(keyword in source.lower() for keyword in ['import ', 'from ', '%pip', '%load_ext']):
        if i < 10:  # Setup cells are usually at the beginning
            setup_cells.append(i)

    if any(keyword in source.lower() for keyword in ['deploy', 'create_or_update', 'bicep']):
        deployment_cells.append(i)

    if any(keyword in source.lower() for keyword in ['config', 'dotenv', 'load_dotenv', 'os.getenv']):
        config_cells.append(i)

    if any(keyword in source.lower() for keyword in ['client.chat.completions', 'openai', 'test']):
        if i > 20:  # Lab cells start after setup
            lab_cells.append(i)

print(f'[*] Cell categorization:')
print(f'    - Setup/Import cells: {len(setup_cells)} (cells 0-10 typically)')
print(f'    - Configuration cells: {len(config_cells)}')
print(f'    - Deployment cells: {len(deployment_cells)}')
print(f'    - Lab test cells: {len(lab_cells)}')
print()

print('[*] Critical cells to validate:')
print(f'    - Cell 3: Environment loading (must work for all labs)')
print(f'    - Cell 11-17: Deployment cells (already completed)')
print(f'    - Cells {lab_cells[0]}-{lab_cells[-1] if lab_cells else "N/A"}: Lab tests')
print()

print('=' * 80)
print('READY TO START TESTING')
print('=' * 80)
print()
print('[!] This script analyzed the notebook structure.')
print('[!] To execute cells, we need to use Jupyter kernel execution.')
print()
print('[RECOMMENDATION]')
print('Use nbconvert or papermill to execute the notebook:')
print(f'  jupyter nbconvert --to notebook --execute {NOTEBOOK_PATH}')
print()
print('[ALTERNATIVE]')
print('Or create individual test scripts for each lab and execute with Python.')
print()

print('[OK] Analysis complete. See test_results/notebook_analysis.json for details.')
