# Azure CLI PATH Detection Fix - Summary

**Date:** 2025-11-10
**Notebook:** master-ai-gateway.ipynb
**Issue:** Azure CLI not found in Jupyter notebook despite being available in terminal

## Problem

The notebook was unable to find Azure CLI (`az`) when running subprocess commands, even though:
- Azure CLI is installed at `/usr/bin/az` in WSL
- `which az` returns `/usr/bin/az` in terminal
- Azure CLI works perfectly in terminal

This was causing cells that use `subprocess` with `az` commands to fail.

## Root Cause

1. **PATH Environment**: Jupyter kernel may not inherit the full shell PATH, especially `/usr/bin`
2. **MSAL Token Cache**: Stale MSAL tokens can cause authentication failures
3. **Subprocess Usage**: Some cells were using `shell=True` with string commands instead of proper list-based subprocess calls

## Solution Applied

### Three Cells Fixed

1. **Cell 13** - Service Principal Creation
   - Uses: `az account show`, `az ad sp create-for-rbac`
   
2. **Cell 42** - Token Rate Limiting with APIM
   - Uses: `az apim api policy create`
   
3. **Cell 89** - Azure OpenAI Image Model Deployment
   - Uses: `az cognitiveservices account deployment create`

### Key Changes for Each Cell

#### 1. Azure CLI Detection Function

Added `get_az_cli()` helper function that:
- Uses `shutil.which('az')` first (works for WSL)
- Falls back to common paths: `/usr/bin/az`, Windows CLI path
- Returns absolute path to Azure CLI executable

```python
def get_az_cli():
    """Find Azure CLI executable - handles WSL vs Windows paths"""
    az_path = shutil.which('az')
    if az_path:
        return az_path
    
    common_paths = [
        '/usr/bin/az',  # WSL/Linux
        r'C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd',  # Windows
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return 'az'  # Fallback to system PATH
```

#### 2. PATH Environment Setup

Each cell now explicitly adds `/usr/bin` to PATH:

```python
az_cli = get_az_cli()
env = os.environ.copy()
if '/usr/bin' not in env.get('PATH', ''):
    env['PATH'] = f"/usr/bin:{env['PATH']}"
```

#### 3. Proper Subprocess Calls

Changed from shell=True with strings to list-based commands with explicit env:

**Before:**
```python
subprocess.run(
    'az account show --output json',
    shell=True,
    capture_output=True,
    text=True
)
```

**After:**
```python
subprocess.run(
    [az_cli, 'account', 'show', '--output', 'json'],
    capture_output=True,
    text=True,
    env=env
)
```

#### 4. MSAL Cache Clearing (Cell 13 only)

Added `clear_msal_cache()` function to fix authentication issues:

```python
def clear_msal_cache():
    """Clear MSAL token cache to fix authentication issues"""
    cache_files = [
        os.path.expanduser('~/.azure/msal_token_cache.json'),
        os.path.expanduser('~/.msal_token_cache.json'),
        os.path.expanduser('~/.azure/msal_http_cache')
    ]
    
    cleared = []
    for cache_file in cache_files:
        if os.path.exists(cache_file):
            try:
                os.remove(cache_file)
                cleared.append(cache_file)
            except Exception as e:
                print(f'[WARN] Could not remove {cache_file}: {e}')
    
    if cleared:
        print(f'[INFO] Cleared MSAL cache: {", ".join(cleared)}')
    
    return len(cleared) > 0
```

#### 5. Diagnostic Output

Each cell now prints diagnostic information:
- Azure CLI path being used
- Whether PATH includes /usr/bin
- Version check results (Cell 89)

## Files Modified

1. **master-ai-gateway.ipynb** - Updated cells 13, 42, 89
2. **Backup created**: `archive/backups/master-ai-gateway.ipynb.backup-azure-cli-fix-20251110-022008`

## How to Use

### For Users

1. **Open the notebook** in Jupyter
2. **Restart the kernel** to ensure fresh environment
3. **Run the updated cells** (13, 42, 89)
4. **Check diagnostic output**:
   - Should see: `[INFO] Azure CLI: /usr/bin/az`
   - Should see: `[INFO] PATH includes /usr/bin: True`
   - Cell 13 may show: `[INFO] Cleared MSAL cache: ...`

### For Developers

The fix script can be run again if needed:

```bash
cd "/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab"
python3 fix_azure_cli_path.py
```

## Testing

To verify Azure CLI is working:

```python
import subprocess
import shutil
import os

# Find Azure CLI
az_cli = shutil.which('az') or '/usr/bin/az'
print(f"Azure CLI: {az_cli}")

# Test version
result = subprocess.run(
    [az_cli, '--version'],
    capture_output=True,
    text=True
)
print(result.stdout[:200])
```

## Troubleshooting

### If Azure CLI still not found:

1. **Check installation**:
   ```bash
   which az
   /usr/bin/az --version
   ```

2. **Check WSL PATH**:
   ```bash
   echo $PATH | grep /usr/bin
   ```

3. **Manually set in notebook**:
   ```python
   import os
   os.environ['PATH'] = f"/usr/bin:{os.environ['PATH']}"
   ```

### If MSAL errors persist:

1. **Manually clear cache**:
   ```bash
   rm -rf ~/.azure/msal_*
   rm -rf ~/.msal_*
   ```

2. **Re-login**:
   ```bash
   az logout
   az login
   ```

3. **Check account**:
   ```bash
   az account show
   az account list
   ```

## Summary of Changes

| Cell | Purpose | Changes Made |
|------|---------|--------------|
| 13 | Service Principal Creation | Added `get_az_cli()`, `clear_msal_cache()`, fixed subprocess calls, added diagnostic output |
| 42 | APIM Token Rate Limiting | Added `get_az_cli()`, fixed subprocess calls, added Azure CLI version check, improved error messages |
| 89 | Image Model Deployment | Added `get_az_cli()`, converted from `shlex.split()` to list-based commands, improved error handling |

## Future Considerations

1. **Global Helper Module**: Consider moving `get_az_cli()` to a shared helper module
2. **Environment Validation Cell**: Add a dedicated cell early in notebook to validate Azure CLI setup
3. **Automated Testing**: Create tests to verify Azure CLI is accessible before running dependent cells
4. **Documentation**: Add troubleshooting guide in notebook markdown cells

## References

- Previous fix found in backups: `archive/backups/master-ai-gateway.ipynb.backup-cell55-fix`
- Fix script: `fix_azure_cli_path.py`
- Backup: `archive/backups/master-ai-gateway.ipynb.backup-azure-cli-fix-20251110-022008`
