# Quick Reference: MSAL Cache Corruption Fix

## Problem
Cells 74 and 105 failed with: `ERROR: Can't get attribute 'NormalizedResponse' on <module 'msal.throttled_http_client'`

## Solution
3-tier error handling with automatic MSAL cache flush and retry

## Changes Summary

### Cell Mapping (Original → New)
| Original | New | Description |
|----------|-----|-------------|
| Cell 74 (idx 73) | Cell 76 (idx 75) | Private Connectivity Policy |
| Cell 105 (idx 104) | Cell 107 (idx 106) | Model Routing Policy |
| N/A | Cell 6 (idx 5) | NEW: MSAL Helper Functions |

### Files Modified
- `master-ai-gateway-fix-MCP.ipynb` - 3 cells changed/added

### New Functions (Cell 6)
```python
flush_msal_cache()           # Removes corrupted MSAL cache
az_with_msal_retry(...)      # Executes az with automatic retry
```

## Error Handling Flow

```
1. Execute az command
   ↓ (if MSAL error detected)
2. Flush MSAL cache
   ↓
3. Re-authenticate (az login)
   ↓
4. Retry original command
   ↓ (if still fails)
5. Fall back to Azure SDK
```

## Usage

### Execute in Order
1. Cell 5: Azure CLI Setup
2. Cell 6: MSAL Helper (loads functions)
3. Cell 76: Private Connectivity Policy
4. Cell 107: Model Routing Policy

### Manual Cache Flush
```python
# In notebook
flush_msal_cache()

# In terminal
rm -rf ~/.azure/msal_*
```

## Verification
Run this in a notebook cell to verify setup:
```python
# Check required components
assert 'az_cli' in globals(), "Run Cell 5 first"
assert 'flush_msal_cache' in globals(), "Run Cell 6 first"
assert 'az_with_msal_retry' in globals(), "Run Cell 6 first"
print("✓ All MSAL helpers loaded successfully")
```

## Key Features
- Automatic MSAL error detection
- Self-healing cache management
- Multiple fallback tiers
- No manual intervention required
- Clear error messages and logging

## MSAL Cache Locations Cleaned
- `~/.azure/msal_token_cache.bin`
- `~/.azure/msal_token_cache.json`
- `~/.azure/msal_http_cache/`
- `~/.azure/service_principal_entries.bin`

## Dependencies
**Required:**
- `azure-cli`
- `azure-identity`

**Optional (for SDK fallback):**
- `azure-mgmt-apimanagement`

## Status
✓ Implementation complete
✓ Verification passed
✓ Documentation complete
⧗ Testing recommended

## Documentation
Full details: `phase1.4-cells74-105-msal.md`
