#!/usr/bin/env python3
"""
Fix cells 16, 38, 45 - Add safety checks to skip advanced policies by default
This allows cells 1-57 to run without breaking the APIM
"""

import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

notebook_path = 'MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab/master-ai-gateway-fix-MCP.ipynb'

# Safety check to prepend to cells
safety_check_semantic_cache = '''# ============================================================================
# OPTIONAL: Semantic Caching (Advanced Feature)
# ============================================================================
import os

ENABLE_SEMANTIC_CACHE = os.getenv('ENABLE_SEMANTIC_CACHE', 'false').lower() == 'true'

if not ENABLE_SEMANTIC_CACHE:
    print('[SKIPPED] Semantic caching is disabled (advanced feature)')
    print('          Set ENABLE_SEMANTIC_CACHE=true in .env to enable')
    print('          Your APIM uses the basic policy (API Key authentication)')
    raise SystemExit(0)

print('[INFO] Semantic caching enabled. Applying policy...')

'''

safety_check_token_metrics = '''# ============================================================================
# OPTIONAL: Token Metrics (Advanced Feature)
# ============================================================================
import os

ENABLE_TOKEN_METRICS = os.getenv('ENABLE_TOKEN_METRICS', 'false').lower() == 'true'

if not ENABLE_TOKEN_METRICS:
    print('[SKIPPED] Token metrics is disabled (advanced feature)')
    print('          Set ENABLE_TOKEN_METRICS=true in .env to enable')
    print('          Your APIM uses the basic policy (API Key authentication)')
    raise SystemExit(0)

print('[INFO] Token metrics enabled. Applying policy...')

'''

safety_check_load_balancing = '''# ============================================================================
# OPTIONAL: Load Balancing (Advanced Feature)
# ============================================================================
import os

ENABLE_LOAD_BALANCING = os.getenv('ENABLE_LOAD_BALANCING', 'false').lower() == 'true'

if not ENABLE_LOAD_BALANCING:
    print('[SKIPPED] Load balancing is disabled (advanced feature)')
    print('          Set ENABLE_LOAD_BALANCING=true in .env to enable')
    print('          Your APIM uses the basic policy (API Key authentication)')
    raise SystemExit(0)

print('[INFO] Load balancing enabled. Applying policy...')

'''

# Load notebook
print(f'Loading notebook: {notebook_path}')
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f'Current cell count: {len(nb["cells"])}')

# Fix cells 16, 38, 45 (indices 15, 37, 44)
fixes = [
    (15, 'Cell 16 - Semantic Caching', safety_check_semantic_cache),
    (37, 'Cell 38 - Token Metrics', safety_check_token_metrics),
    (44, 'Cell 45 - Load Balancing', safety_check_load_balancing)
]

for cell_idx, name, safety_check in fixes:
    if len(nb['cells']) > cell_idx:
        print(f'\nUpdating {name} (index {cell_idx})...')

        cell = nb['cells'][cell_idx]
        old_source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']

        # Check if already has safety check
        if 'ENABLE_SEMANTIC_CACHE' in old_source or 'ENABLE_TOKEN_METRICS' in old_source or 'ENABLE_LOAD_BALANCING' in old_source:
            print(f'  [SKIP] {name} already has safety check')
            continue

        # Prepend safety check
        new_source = safety_check + old_source

        nb['cells'][cell_idx]['source'] = new_source.split('\n')
        print(f'  [OK] {name} updated with safety check')
    else:
        print(f'  [ERROR] {name} does not exist')

# Save notebook
print(f'\nSaving notebook...')
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print('[SUCCESS] Notebook updated!')
print()
print('='*80)
print('RESULT:')
print('='*80)
print('Cells 16, 38, 45 will now SKIP by default')
print('This prevents advanced policies from breaking your APIM')
print('')
print('Your APIM will use the minimal policy (API Key authentication only)')
print('This matches your "working before" configuration')
print()
print('To enable advanced features (optional):')
print('  - Add to master-lab.env:')
print('    ENABLE_SEMANTIC_CACHE=true')
print('    ENABLE_TOKEN_METRICS=true')
print('    ENABLE_LOAD_BALANCING=true')
print('='*80)
