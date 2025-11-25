#!/usr/bin/env python3
print('Step 1')
import json
print('Step 2')
import time
print('Step 3')
from pathlib import Path
print('Step 4')

NOTEBOOK_INPUT = 'master-ai-gateway.ipynb'
print(f'Step 5: {NOTEBOOK_INPUT}')

REPORT_DIR = Path('test_results')
print(f'Step 6: {REPORT_DIR}')

REPORT_DIR.mkdir(exist_ok=True)
print('Step 7: Directory created')

print('All steps passed!')
