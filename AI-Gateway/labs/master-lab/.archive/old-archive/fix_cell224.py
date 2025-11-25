#!/usr/bin/env python3
"""
Fix Cell 224 - Add safety check to prevent applying broken policies
"""

import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

notebook_path = 'MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab/master-ai-gateway-fix-MCP.ipynb'

# Safety check to prepend to cell 224
safety_check = '''# ============================================================================
# SAFETY CHECK: This cell applies OAuth 2.0 JWT validation policy
# This requires proper Azure Entra ID configuration
# ============================================================================
print('='*80)
print('Cell 224: OAuth 2.0 Policy Configuration')
print('='*80)
print()
print('[WARNING] This cell applies an OAuth 2.0 JWT validation policy.')
print('          If you have not configured Azure Entra ID, this will break your APIM.')
print()

# Check if OAuth is properly configured
import os
tenant_id_env = os.getenv('AZURE_TENANT_ID', '')
backend_id_env = os.getenv('BACKEND_ID', '')

if not tenant_id_env or tenant_id_env == 'your-tenant-id':
    print('[SKIPPING] AZURE_TENANT_ID not configured.')
    print('          To enable OAuth 2.0, configure Azure Entra ID first.')
    print('          See: labs/access-controlling/ for reference.')
    print()
    print('[INFO] Your APIM currently uses the minimal policy (API Key only).')
    print('       This is sufficient for most scenarios.')
    raise SystemExit(0)  # Exit cell without error

print('[INFO] OAuth 2.0 configuration detected. Proceeding with policy application...')
print()

'''

# Load notebook
print(f'Loading notebook: {notebook_path}')
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f'Current cell count: {len(nb["cells"])}')

# Fix cell 224 (index 223)
if len(nb['cells']) > 223:
    print('Updating cell 224 (index 223)...')

    cell224 = nb['cells'][223]
    old_source = ''.join(cell224['source']) if isinstance(cell224['source'], list) else cell224['source']

    # Prepend safety check
    new_source = safety_check + old_source

    nb['cells'][223]['source'] = new_source.split('\n')
    print('[OK] Cell 224 updated with safety check')
else:
    print('[ERROR] Cell 224 does not exist')
    sys.exit(1)

# Save notebook
print(f'Saving notebook...')
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print('[SUCCESS] Notebook updated!')
print()
print('='*80)
print('Cell 224 now has a safety check that will:')
print('1. Check if Azure Entra ID (AZURE_TENANT_ID) is configured')
print('2. Skip the cell if not configured (preventing 500 errors)')
print('3. Keep your minimal policy intact (API Key authentication)')
print('='*80)
