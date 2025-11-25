# Test Notebook Cell - Validate Deployment

## Add this cell to your notebook to validate the Bicep deployment before running it

You can insert this as a new cell **before Cell 17** (Deploy Bicep) to validate everything is ready.

---

## Option 1: Quick Validation Cell

Add this markdown cell:

```markdown
### Optional: Validate Deployment Before Running

Run this cell to validate the Bicep file before deploying (recommended for first-time users).
```

Then add this code cell:

```python
# Validate deployment configuration
import subprocess

print('[*] Validating master-deployment.bicep...')
print('')

# Run validation script
result = subprocess.run(
    ['python', 'validate_deployment.py'],
    capture_output=True,
    text=True
)

print(result.stdout)

if result.returncode == 0:
    print('')
    print('[OK] Validation passed! Ready to deploy.')
else:
    print('')
    print('[ERROR] Validation failed! Fix issues before deploying.')
    raise Exception('Validation failed')
```

---

## Option 2: Inline Validation (More Detailed)

Add this code cell:

```python
# Detailed deployment validation
import os
import json
import subprocess
from pathlib import Path

def validate_deployment():
    """Validate all deployment prerequisites"""

    print('=' * 70)
    print('  Deployment Validation')
    print('=' * 70)
    print('')

    all_ok = True

    # Check 1: Required files
    print('[*] Checking required files...')
    required_files = [
        'master-deployment.bicep',
        'params.template.json',
        'policies/backend-pool-load-balancing-policy.xml'
    ]

    for file in required_files:
        if os.path.exists(file):
            print(f'  [OK] {file}')
        else:
            print(f'  [ERROR] Missing: {file}')
            all_ok = False
    print('')

    # Check 2: Bicep compilation
    print('[*] Compiling Bicep file...')
    result = subprocess.run(
        ['az', 'bicep', 'build', '--file', 'master-deployment.bicep'],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        if os.path.exists('master-deployment.json'):
            size = os.path.getsize('master-deployment.json') / 1024
            print(f'  [OK] Compiled successfully ({size:.1f} KB)')
        else:
            print('  [ERROR] Compiled JSON not found')
            all_ok = False
    else:
        print(f'  [ERROR] Compilation failed')
        print(f'  {result.stderr[:200]}')
        all_ok = False
    print('')

    # Check 3: Parameters
    print('[*] Validating parameters...')
    try:
        with open('params.template.json', 'r') as f:
            params = json.load(f)

        params_values = params.get('parameters', {})
        print(f'  [OK] Location: {params_values.get("location", {}).get("value")}')
        print(f'  [OK] APIM SKU: {params_values.get("apimSku", {}).get("value")}')
        print(f'  [OK] Redis SKU: {params_values.get("redisCacheSku", {}).get("value")}')
    except Exception as e:
        print(f'  [ERROR] Invalid params: {e}')
        all_ok = False
    print('')

    # Check 4: Azure authentication
    print('[*] Checking Azure authentication...')
    result = subprocess.run(
        ['az', 'account', 'show', '--query', 'name', '-o', 'tsv'],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f'  [OK] Logged in to: {result.stdout.strip()}')
    else:
        print('  [ERROR] Not authenticated. Run: az login')
        all_ok = False
    print('')

    # Summary
    print('=' * 70)
    if all_ok:
        print('[OK] All validation checks passed!')
        print('[OK] Ready to deploy')
        print('')
        print('Deployment will create:')
        print('  - 1x API Management (StandardV2)')
        print('  - 3x AI Foundry (UK South, Sweden Central, West Europe)')
        print('  - 14 AI models total')
        print('  - Redis, Search, Cosmos, Content Safety')
        print('  - 7 MCP servers')
        print('')
        print('Estimated time: 30-45 minutes')
        print('Estimated cost: ~$650-750/month')
    else:
        print('[ERROR] Validation failed!')
        print('[ERROR] Fix issues above before deploying')
        raise Exception('Validation failed')
    print('=' * 70)

    return all_ok

# Run validation
validate_deployment()
```

---

## Option 3: Just Run the Script

Simplest option - add this code cell:

```python
# Validate deployment using validation script
!python validate_deployment.py
```

---

## Recommended Placement

Insert the validation cell **between Cell 16 and Cell 17**:

```
Cell 16: [Markdown] Step 3: Deploy Infrastructure (Bicep)

>>> INSERT VALIDATION CELL HERE <<<

Cell 17: [Code] Deploy Bicep (only if deployment doesn't exist)
```

This gives you a chance to validate before the long 30-45 minute deployment starts.

---

## What Gets Validated

The validation checks:

1. ✅ **File Existence**
   - master-deployment.bicep
   - params.template.json
   - All policy files
   - All module dependencies

2. ✅ **Bicep Syntax**
   - Compiles without errors
   - Generates valid JSON (1.1 MB)

3. ✅ **Parameters**
   - Valid JSON format
   - All required parameters present
   - Values are correct

4. ✅ **Azure Authentication**
   - Logged in to Azure
   - Subscription is set
   - Has permissions

5. ✅ **Resource Summary**
   - Shows what will be deployed
   - Estimated time: 30-45 minutes
   - Estimated cost: ~$650-750/month

6. ✅ **Deployment Readiness**
   - All prerequisites met
   - Ready to run

---

## Example Output

When you run the validation cell, you'll see:

```
======================================================================
  Master Deployment Bicep Validation
======================================================================

======================================================================
  Check 1: Required Files
======================================================================
[OK] Found: master-deployment.bicep
[OK] Found: params.template.json
...

======================================================================
  Check 2: Bicep Syntax Validation
======================================================================
[OK] Compiling Bicep to JSON - Success
[OK] Compiled JSON size: 1055.0 KB

======================================================================
  Check 3: Parameters File Validation
======================================================================
[OK] Parameters file is valid JSON
[OK] Parameter 'location': uksouth
[OK] Parameter 'apimSku': Standardv2
...

======================================================================
  Check 7: Deployment Readiness
======================================================================
[OK] All validation checks passed!

Ready to Deploy!
```

---

## Summary

**Before deploying** (Cell 17), insert a validation cell to:
- Catch errors early
- See what will be deployed
- Understand time and cost
- Confirm you're ready

**Takes**: ~5 seconds
**Saves**: Potentially 30-45 minutes if there's an issue!

**Recommended**: Add Option 3 (simplest) or Option 2 (most detailed)
