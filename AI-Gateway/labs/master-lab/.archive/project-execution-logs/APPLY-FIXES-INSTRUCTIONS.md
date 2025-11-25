# How to Apply Fixes - 2025-11-17

## Overview

This document provides step-by-step instructions for applying the verified fixes to the master notebook.

**Created**: 2025-11-17 03:15 UTC
**Notebook**: master-ai-gateway-fix-MCP.ipynb (158 cells)
**Fix Files Location**: `project-execution-logs/fixes/`

---

## QUICK START - Apply All Fixes

### Option 1: Automated Application (Recommended)

Run the automated fix script that applies all changes:

```bash
cd /mnt/c/Users/lproux/OneDrive\ -\ Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab

# Create backup first
cp master-ai-gateway-fix-MCP.ipynb master-ai-gateway-fix-MCP.ipynb.backup-$(date +%Y%m%d-%H%M%S)

# Apply all fixes
python project-execution-logs/apply-all-fixes.py
```

### Option 2: Manual Application (Cell by Cell)

Follow instructions below for each cell.

---

## FIXES TO APPLY

### Fix 1: Cell 148 - Undefined Variable (HIGH PRIORITY)

**Issue**: `NameError: name 'image_model' is not defined`
**Fix File**: `fixes/FIX-CELL-148-image-model.py`
**Estimated Time**: 2 minutes

**Manual Steps**:
1. Open `master-ai-gateway-fix-MCP.ipynb` in Jupyter or VS Code
2. Navigate to Cell 148
3. Replace entire cell content with content from `FIX-CELL-148-image-model.py`
4. Save notebook

**Changes Summary**:
- Line 2: `image_model` → `IMAGE_MODEL`
- Line 5: `image_model` → `IMAGE_MODEL`
- Line 17: `image_model` → `IMAGE_MODEL`
- Line 25: `image_model` → `IMAGE_MODEL`

**Test**:
```python
# Run Cell 147 first (initialization)
# Then run Cell 148
# Should succeed without NameError
```

---

### Fix 2: Cell 125 - MCP OAuth Retry Logic (MEDIUM PRIORITY)

**Issue**: Timeout errors when MCP servers are scaled to zero
**Fix File**: `fixes/FIX-CELL-125-mcp-oauth-retry.py`
**Estimated Time**: 3 minutes

**Manual Steps**:
1. Navigate to Cell 125
2. Replace entire cell content with content from `FIX-CELL-125-mcp-oauth-retry.py`
3. Save notebook

**Changes Summary**:
- Added `post_with_retry()` function with exponential backoff
- Changed timeout from 8s/10s → 15-35s with retries
- Added retry logic for both unauthorized and authorized requests
- Added progress messages during retries

**Test**:
```python
# Ensure earlier cells defining 'credential' and 'MCP_SERVERS' have run
# Run Cell 125
# Should retry on timeout instead of immediate failure
```

---

### Fix 3: Cell 121 - Redis Graceful Degradation (LOW PRIORITY)

**Issue**: Raises ValueError and stops execution if Redis not configured
**Fix File**: `fixes/FIX-CELL-121-redis-graceful.py`
**Estimated Time**: 2 minutes

**Manual Steps**:
1. Navigate to Cell 121
2. Replace entire cell content with content from `FIX-CELL-121-redis-graceful.py`
3. Save notebook

**Changes Summary**:
- Changed `raise ValueError()` → graceful degradation with `redis_enabled = False`
- Added socket timeouts (5s connection, 5s socket)
- Added comprehensive error messages
- Exports `redis_enabled` variable for other cells to check
- Allows notebook to continue even if Redis unavailable

**Test**:
```python
# Run Cell 121
# If Redis unavailable, should print warning and continue (not raise error)
# If Redis available, should connect successfully
```

---

### Fix 4: Cell 147 - Simplify Image Endpoint (MEDIUM PRIORITY)

**Issue**: Complex endpoint discovery logic with potential auth issues
**Fix File**: `fixes/FIX-CELL-147-simplify-apim.py`
**Estimated Time**: 3 minutes

**Manual Steps**:
1. Navigate to Cell 147
2. Replace entire cell content with content from `FIX-CELL-147-simplify-apim.py`
3. Save notebook

**Changes Summary**:
- Removed direct Azure OpenAI endpoint logic
- Always uses APIM gateway (simpler, more consistent)
- Reuses existing `headers_both` or `final_headers` from earlier cells
- Better error messages if APIM not configured
- Simplified `generate_image()` function

**Test**:
```python
# Ensure APIM_GATEWAY_URL is in environment
# Run Cell 147
# Should initialize with APIM gateway URL
# Run Cell 148 to test image generation
```

---

### Fix 5: Cell 135 - Cosmos DB Firewall (USER ACTION REQUIRED)

**Issue**: Firewall blocks access from current IP
**Status**: ✅ Cell already has excellent error handling and fix instructions
**Action**: NO CODE CHANGES NEEDED

**User Must Do**:
1. Run Cell 135
2. If you see `[WARN] Cosmos DB access forbidden (likely firewall)`, follow the printed instructions:

**Option A - CLI (Recommended)**:
```bash
# Get your current IP
export CLIENT_IP=$(curl -s ifconfig.me)

# Add IP to Cosmos DB firewall
COSMOS_ACCOUNT=$(az cosmosdb list --resource-group lab-master-lab --query "[0].name" -o tsv)
az cosmosdb update \
  --resource-group lab-master-lab \
  --name $COSMOS_ACCOUNT \
  --ip-range-filter "$CLIENT_IP"
```

**Option B - Azure Portal**:
1. Go to Azure Portal → Cosmos DB → cosmos-pavavy6pu5hpa
2. Settings → Networking
3. Click "Add my current IP (xxx.xxx.xxx.xxx)"
4. Click "Save"
5. Wait 1-2 minutes for propagation
6. Re-run Cell 135

---

## AUTOMATED FIX SCRIPT

Create `project-execution-logs/apply-all-fixes.py`:

```python
#!/usr/bin/env python3
"""
Automated fix application for master-ai-gateway-fix-MCP.ipynb
Applies all verified fixes to notebook cells
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def apply_fixes():
    """Apply all fixes to notebook"""

    NOTEBOOK_PATH = Path("master-ai-gateway-fix-MCP.ipynb")
    FIXES_DIR = Path("project-execution-logs/fixes")

    if not NOTEBOOK_PATH.exists():
        print(f"❌ Notebook not found: {NOTEBOOK_PATH}")
        return False

    # Create backup
    backup_path = f"{NOTEBOOK_PATH}.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    print(f"📦 Creating backup: {backup_path}")
    import shutil
    shutil.copy2(NOTEBOOK_PATH, backup_path)

    # Load notebook
    print(f"📖 Loading notebook: {NOTEBOOK_PATH}")
    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    fixes_applied = 0

    # Fix 1: Cell 148 - image_model variable
    print("\n[1/4] Applying Fix to Cell 148 (image_model → IMAGE_MODEL)...")
    fix_file = FIXES_DIR / "FIX-CELL-148-image-model.py"
    if fix_file.exists():
        with open(fix_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract just the code (skip docstring)
            lines = content.split('\n')
            code_start = next(i for i, line in enumerate(lines) if line.startswith('# Test Image Generation'))
            new_source = '\n'.join(lines[code_start:])
            nb['cells'][148]['source'] = new_source.split('\n')
            fixes_applied += 1
            print("  ✅ Cell 148 updated")
    else:
        print(f"  ⚠️ Fix file not found: {fix_file}")

    # Fix 2: Cell 125 - MCP OAuth retry
    print("\n[2/4] Applying Fix to Cell 125 (MCP OAuth retry logic)...")
    fix_file = FIXES_DIR / "FIX-CELL-125-mcp-oauth-retry.py"
    if fix_file.exists():
        with open(fix_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            code_start = next(i for i, line in enumerate(lines) if line.startswith('# MCP OAuth authorization'))
            new_source = '\n'.join(lines[code_start:])
            nb['cells'][125]['source'] = new_source.split('\n')
            fixes_applied += 1
            print("  ✅ Cell 125 updated")
    else:
        print(f"  ⚠️ Fix file not found: {fix_file}")

    # Fix 3: Cell 121 - Redis graceful degradation
    print("\n[3/4] Applying Fix to Cell 121 (Redis graceful degradation)...")
    fix_file = FIXES_DIR / "FIX-CELL-121-redis-graceful.py"
    if fix_file.exists():
        with open(fix_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            code_start = next(i for i, line in enumerate(lines) if line.startswith('import redis.asyncio'))
            new_source = '\n'.join(lines[code_start:])
            nb['cells'][121]['source'] = new_source.split('\n')
            fixes_applied += 1
            print("  ✅ Cell 121 updated")
    else:
        print(f"  ⚠️ Fix file not found: {fix_file}")

    # Fix 4: Cell 147 - Simplify image endpoint
    print("\n[4/4] Applying Fix to Cell 147 (Simplify to APIM-only)...")
    fix_file = FIXES_DIR / "FIX-CELL-147-simplify-apim.py"
    if fix_file.exists():
        with open(fix_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            code_start = next(i for i, line in enumerate(lines) if line.startswith('import base64'))
            new_source = '\n'.join(lines[code_start:])
            nb['cells'][147]['source'] = new_source.split('\n')
            fixes_applied += 1
            print("  ✅ Cell 147 updated")
    else:
        print(f"  ⚠️ Fix file not found: {fix_file}")

    # Save modified notebook
    print(f"\n💾 Saving modified notebook...")
    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"✅ Successfully applied {fixes_applied}/4 fixes")
    print(f"{'='*60}")
    print(f"\nBackup saved to: {backup_path}")
    print(f"Modified notebook: {NOTEBOOK_PATH}")
    print("\nNext steps:")
    print("1. Review changes in notebook")
    print("2. Test each fixed cell individually")
    print("3. Run full notebook execution")

    return True

if __name__ == "__main__":
    success = apply_fixes()
    sys.exit(0 if success else 1)
```

---

## TESTING PLAN

### Phase 1: Individual Cell Testing (10 minutes)

```python
# Test each fixed cell in isolation

# 1. Test Cell 147 (image initialization)
# Should print: [image-init] Using APIM gateway: ...
# Should print: [image-init] ✅ Image generation initialized via APIM gateway

# 2. Test Cell 148 (image generation)
# Should NOT raise NameError
# Should attempt to generate image (may fail if model not deployed, but no code error)

# 3. Test Cell 121 (Redis)
# Should either connect successfully OR print warning and continue (not raise error)

# 4. Test Cell 125 (MCP OAuth)
# Should retry on timeout
# Should eventually succeed or timeout gracefully with detailed error messages
```

### Phase 2: Full Notebook Execution (30 minutes)

```bash
cd /mnt/c/Users/lproux/OneDrive\ -\ Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab

# Execute entire notebook
jupyter nbconvert \
  --to notebook \
  --execute \
  --allow-errors \
  --ExecutePreprocessor.timeout=600 \
  --output executed-notebook-with-fixes.ipynb \
  master-ai-gateway-fix-MCP.ipynb
```

### Phase 3: Validation (10 minutes)

```bash
# Check for specific errors that should now be fixed
grep -A 5 "NameError.*image_model" executed-notebook-with-fixes.ipynb
# Should return nothing (error should be gone)

grep -A 5 "ValueError.*Redis" executed-notebook-with-fixes.ipynb
# Should return nothing (error should be gone)
```

---

## ROLLBACK PROCEDURE

If fixes cause issues:

```bash
# List backups
ls -lh master-ai-gateway-fix-MCP.ipynb.backup-*

# Restore most recent backup
LATEST_BACKUP=$(ls -t master-ai-gateway-fix-MCP.ipynb.backup-* | head -1)
cp $LATEST_BACKUP master-ai-gateway-fix-MCP.ipynb

echo "Restored from: $LATEST_BACKUP"
```

---

## SUCCESS CRITERIA

✅ Cell 148 executes without `NameError: name 'image_model' is not defined`
✅ Cell 125 retries on timeout instead of immediate failure
✅ Cell 121 continues execution even if Redis unavailable
✅ Cell 147 initializes image generation via APIM gateway
✅ Cosmos DB firewall instructions clear if error occurs (Cell 135)

---

**Total Estimated Time**: 15-20 minutes (manual) or 5 minutes (automated)
**Recommended Approach**: Use automated script, then test modified cells
**Created**: 2025-11-17 03:15 UTC
