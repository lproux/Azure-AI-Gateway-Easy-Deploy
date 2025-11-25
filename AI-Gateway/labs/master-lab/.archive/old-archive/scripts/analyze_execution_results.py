#!/usr/bin/env python3
"""
Analyze the executed notebook and generate comprehensive error report
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

print('=' * 80)
print('COMPREHENSIVE ERROR ANALYSIS')
print('=' * 80)
print(f'Started: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print()

# Load executed notebook
NOTEBOOK_OUTPUT = 'master-ai-gateway-executed.ipynb'

if not Path(NOTEBOOK_OUTPUT).exists():
    print(f'[ERROR] {NOTEBOOK_OUTPUT} not found!')
    sys.exit(1)

print(f'[*] Loading {NOTEBOOK_OUTPUT}...')
with open(NOTEBOOK_OUTPUT, encoding='utf-8') as f:
    executed_nb = json.load(f)

cells = executed_nb['cells']
total_cells = len(cells)
code_cells = [i for i, c in enumerate(cells) if c['cell_type'] == 'code']

print(f'[OK] Loaded {total_cells} cells ({len(code_cells)} code cells)')
print()

# Analyze each cell for errors
cell_results = {
    'passed': [],
    'failed': [],
    'skipped': [],
    'errors': []
}

print('[*] Analyzing cell outputs...')
for i, cell in enumerate(cells):
    if cell['cell_type'] != 'code':
        continue

    # Check outputs for errors
    outputs = cell.get('outputs', [])
    has_error = False
    has_output = False

    for output in outputs:
        if output.get('output_type') == 'error':
            has_error = True
            error_info = {
                'cell_index': i,
                'error_name': output.get('ename', 'Unknown'),
                'error_value': output.get('evalue', ''),
                'traceback': output.get('traceback', [])
            }
            cell_results['errors'].append(error_info)
            cell_results['failed'].append(i)
            break
        elif output.get('output_type') in ['stream', 'execute_result', 'display_data']:
            has_output = True

    if not has_error and has_output:
        cell_results['passed'].append(i)
    elif not has_error and not has_output:
        cell_results['skipped'].append(i)

# Print summary
print()
print('=' * 80)
print('EXECUTION SUMMARY')
print('=' * 80)
print()
print(f'Total Cells:     {total_cells}')
print(f'Code Cells:      {len(code_cells)}')
print(f'Passed:          {len(cell_results["passed"])} cells ({len(cell_results["passed"])/len(code_cells)*100:.1f}%)')
print(f'Failed:          {len(cell_results["failed"])} cells ({len(cell_results["failed"])/len(code_cells)*100:.1f}%)')
print(f'Skipped/Empty:   {len(cell_results["skipped"])} cells')
print(f'Total Errors:    {len(cell_results["errors"])}')
print()

# Categorize errors by type
error_types = defaultdict(list)
for err in cell_results['errors']:
    ename = err['error_name']
    error_types[ename].append(err)

print('=' * 80)
print('ERROR BREAKDOWN BY TYPE')
print('=' * 80)
print()
for ename, errors in sorted(error_types.items(), key=lambda x: len(x[1]), reverse=True):
    print(f'{ename}: {len(errors)} occurrences')

print()

# Analyze error patterns
print('=' * 80)
print('ERROR PATTERN ANALYSIS')
print('=' * 80)
print()

# Common error patterns
patterns = {
    'NameError': {
        'likely_cause': 'Variable/module not defined',
        'cells': [],
        'fix_strategy': 'Add missing imports or variable declarations'
    },
    'ModuleNotFoundError': {
        'likely_cause': 'Missing package/module',
        'cells': [],
        'fix_strategy': 'Install missing package or fix import path'
    },
    'AttributeError': {
        'likely_cause': 'Object doesn\'t have expected attribute',
        'cells': [],
        'fix_strategy': 'Check object type and available attributes'
    },
    'KeyError': {
        'likely_cause': 'Missing dictionary key',
        'cells': [],
        'fix_strategy': 'Add missing config value or use .get() with default'
    },
    'FileNotFoundError': {
        'likely_cause': 'File/path doesn\'t exist',
        'cells': [],
        'fix_strategy': 'Create missing file or fix path'
    },
    'TypeError': {
        'likely_cause': 'Wrong type for operation',
        'cells': [],
        'fix_strategy': 'Fix type conversion or check None values'
    },
}

for err in cell_results['errors']:
    ename = err['error_name']
    if ename in patterns:
        patterns[ename]['cells'].append(err['cell_index'])

for ename, info in patterns.items():
    if info['cells']:
        print(f'[{ename}] {len(info["cells"])} occurrences')
        print(f'  Cause: {info["likely_cause"]}')
        print(f'  Fix: {info["fix_strategy"]}')
        print(f'  Affected cells: {info["cells"][:10]}{"..." if len(info["cells"]) > 10 else ""}')
        print()

# Detailed error analysis - first 20 errors
print('=' * 80)
print('FIRST 20 ERRORS (DETAILED)')
print('=' * 80)
print()

for i, err in enumerate(cell_results['errors'][:20], 1):
    cell_idx = err['cell_index']
    cell_source = ''.join(cells[cell_idx].get('source', []))[:200]

    print(f'Error #{i}: Cell {cell_idx}')
    print(f'  Type: {err["error_name"]}')
    print(f'  Message: {err["error_value"][:100]}')
    print(f'  Cell preview: {cell_source.replace(chr(10), " ")[:80]}...')

    # Extract key info from traceback
    if err['traceback']:
        # Last line usually has the most relevant info
        last_line = err['traceback'][-1] if err['traceback'] else ''
        print(f'  Traceback: {last_line[:100]}')
    print()

# Save detailed report
report_dir = Path('test_results')
report_dir.mkdir(exist_ok=True)

report = {
    'timestamp': datetime.now().isoformat(),
    'total_cells': total_cells,
    'code_cells': len(code_cells),
    'summary': {
        'passed': len(cell_results['passed']),
        'failed': len(cell_results['failed']),
        'skipped': len(cell_results['skipped']),
        'total_errors': len(cell_results['errors'])
    },
    'error_types': {k: len(v) for k, v in error_types.items()},
    'error_patterns': {k: {'count': len(v['cells']), 'cells': v['cells'],
                           'cause': v['likely_cause'], 'fix': v['fix_strategy']}
                       for k, v in patterns.items() if v['cells']},
    'detailed_errors': []
}

# Add all errors to report
for err in cell_results['errors']:
    cell_idx = err['cell_index']
    cell_source = ''.join(cells[cell_idx].get('source', []))

    report['detailed_errors'].append({
        'cell_index': cell_idx,
        'cell_source': cell_source,
        'error_name': err['error_name'],
        'error_value': err['error_value'],
        'traceback': err['traceback']
    })

report_file = report_dir / f'error_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
with open(report_file, 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)

print('=' * 80)
print(f'[OK] Detailed report saved: {report_file}')
print('=' * 80)
print()

# Generate fix recommendations
print('=' * 80)
print('TOP PRIORITY FIXES')
print('=' * 80)
print()

# Find cells that need fixes
fix_priorities = []

# Priority 1: Early cells (affect all subsequent cells)
early_errors = [e for e in cell_results['errors'] if e['cell_index'] < 30]
if early_errors:
    print('[PRIORITY 1] Early Setup Cells (<30)')
    print(f'  {len(early_errors)} errors in early cells')
    print(f'  These affect all subsequent cells!')
    print(f'  Cells: {sorted(set(e["cell_index"] for e in early_errors))}')
    print()

# Priority 2: NameError (missing variables/imports)
name_errors = [e for e in cell_results['errors'] if e['error_name'] == 'NameError']
if name_errors:
    print('[PRIORITY 2] NameErrors (Missing Definitions)')
    print(f'  {len(name_errors)} cells with undefined variables')
    # Extract what's missing
    missing_names = set()
    for e in name_errors:
        # Parse "name 'xxx' is not defined"
        evalue = e['error_value']
        if "'" in evalue:
            name = evalue.split("'")[1]
            missing_names.add(name)
    print(f'  Missing: {", ".join(sorted(missing_names)[:10])}')
    print()

# Priority 3: ModuleNotFoundError
module_errors = [e for e in cell_results['errors'] if e['error_name'] == 'ModuleNotFoundError']
if module_errors:
    print('[PRIORITY 3] Missing Modules')
    print(f'  {len(module_errors)} cells with missing modules')
    missing_modules = set()
    for e in module_errors:
        if "'" in e['error_value']:
            module = e['error_value'].split("'")[1]
            missing_modules.add(module)
    print(f'  Missing: {", ".join(sorted(missing_modules))}')
    print()

print('=' * 80)
print('[DONE] Analysis complete!')
print('=' * 80)
print()
print('Next steps:')
print('  1. Review the error report above')
print('  2. Fix Priority 1 errors first (early cells)')
print('  3. Fix Priority 2 errors (NameErrors)')
print('  4. Fix Priority 3 errors (missing modules)')
print(f'  5. See detailed JSON report: {report_file}')
