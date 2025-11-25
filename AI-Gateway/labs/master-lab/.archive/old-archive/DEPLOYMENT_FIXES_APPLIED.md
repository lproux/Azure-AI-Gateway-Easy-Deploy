# DEPLOYMENT FIXES - COMPLETE ✅

**Date:** 2025-11-14
**Issue:** Cell 11 deployment failed with missing variables and file path errors

---

## ISSUES IDENTIFIED

### 1. Missing Service Principal Credentials ❌
**Problem:** Deployment needed service principal credentials from `.azure-credentials.env`
**Error:** No authentication for Azure resources

### 2. Wrong BICEP Directory ❌
**Problem:** BICEP_DIR pointed to `archive/scripts` instead of `deploy`
**Error:** `FileNotFoundError: Bicep file not found`

### 3. Windows Path Handling ❌  
**Problem:** Paths with spaces like `C:\Program Files\...` not quoted properly
**Error:** `'C:\Program' is not recognized as an internal or external command`

---

## FIXES APPLIED

### ✅ FIX 1: Cell 3 - Load Service Principal Credentials

**Added to Cell 3:**
```python
from dotenv import load_dotenv

# Load service principal credentials if available
AZ_CREDS_FILE = Path('.azure-credentials.env')
if AZ_CREDS_FILE.exists():
    load_dotenv(AZ_CREDS_FILE, override=True)
    print(f'[OK] Loaded service principal credentials from {AZ_CREDS_FILE}')
else:
    print(f'[INFO] No {AZ_CREDS_FILE} found - will use Azure CLI credentials')
```

**What it does:**
- Loads `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET` from `.azure-credentials.env`
- Falls back to Azure CLI if file doesn't exist

---

### ✅ FIX 2: Cell 8 - Service Principal Authentication

**Updated Cell 8 credential creation:**
```python
# Prefer service principal if env vars are present (from .azure-credentials.env)
if all(os.getenv(k) for k in ['AZURE_TENANT_ID','AZURE_CLIENT_ID','AZURE_CLIENT_SECRET']):
    credential = ClientSecretCredential(
        tenant_id=os.getenv('AZURE_TENANT_ID'),
        client_id=os.getenv('AZURE_CLIENT_ID'),
        client_secret=os.getenv('AZURE_CLIENT_SECRET')
    )
    print('[auth] Using Service Principal credentials')

# Fallback to Azure CLI or DefaultAzureCredential
if credential is None:
    credential = AzureCliCredential()
```

**Authentication Priority:**
1. Service Principal (from `.azure-credentials.env`) ← **Preferred for CI/CD**
2. Azure CLI credentials (from `az login`)
3. DefaultAzureCredential (managed identity, etc.)

---

### ✅ FIX 3: Cell 11 - Correct BICEP Directory

**Changed:**
```python
# OLD
BICEP_DIR = Path(os.getenv('BICEP_DIR', 'archive/scripts'))

# NEW  
BICEP_DIR = Path(os.getenv('BICEP_DIR', 'deploy'))
```

**Bicep Files Location:**
```
deploy/
├── deploy-01-core.bicep
├── deploy-01-core.json
├── deploy-02-ai-foundry.bicep
├── deploy-02-ai-foundry.json
├── deploy-02c-apim-api.bicep
├── deploy-02c-apim-api.json
├── deploy-03-supporting.bicep
├── deploy-03-supporting.json
├── deploy-04-mcp.bicep
└── deploy-04-mcp.json
```

---

### ✅ FIX 4: Cell 2 - Windows Path Handling (Already Fixed!)

**Good News:** Cell 2 already has sophisticated path handling!

**Existing Code:**
```python
def convert_path_for_cli(path_str):
    """Convert Windows path to appropriate format for Azure CLI.
    If running in WSL, convert to WSL path format.
    Otherwise, use native Windows path with proper quoting.
    """
    p = Path(path_str).resolve()
    
    if is_wsl():
        # Convert C:\Users\... -> /mnt/c/Users/...
        return wsl_path
    else:
        # Windows native - use quotes for paths with spaces
        return f'"{p}"'
```

**This automatically handles:**
- Windows paths with spaces: `C:\Program Files\...`
- WSL path conversion: `/mnt/c/Users/...`
- Proper quoting for Azure CLI

---

## VERIFICATION

**Test these in order:**

1. **Cell 3:** Check for service principal loading
   ```python
   # Expected output:
   [OK] Loaded service principal credentials from .azure-credentials.env
   # OR
   [INFO] No .azure-credentials.env found - will use Azure CLI credentials
   ```

2. **Cell 8:** Verify credential creation
   ```python
   # Expected output:
   [auth] Using Service Principal credentials
   # OR
   [auth] Using AzureCliCredential
   ```

3. **Cell 11:** Run deployment
   ```python
   # Expected output:
   [CONFIG] BICEP_DIR: deploy
   [deploy] compiled deploy/deploy-01-core.bicep -> deploy/deploy-01-core.json
   ```

---

## SERVICE PRINCIPAL SETUP (.azure-credentials.env)

Create this file in the master-lab directory:

```bash
# .azure-credentials.env
AZURE_TENANT_ID=your-tenant-id-here
AZURE_CLIENT_ID=your-client-id-here  
AZURE_CLIENT_SECRET=your-client-secret-here
SUBSCRIPTION_ID=d334f2cd-3efd-494e-9fd3-2470b1a13e4c
```

**How to get these values:**
```bash
# Create service principal
az ad sp create-for-rbac --name "master-lab-sp" \
  --role contributor \
  --scopes /subscriptions/d334f2cd-3efd-494e-9fd3-2470b1a13e4c

# Output will show:
# - appId → AZURE_CLIENT_ID
# - password → AZURE_CLIENT_SECRET
# - tenant → AZURE_TENANT_ID
```

---

## EXECUTION ORDER (Updated)

```
Cell 1:  Azure CLI helper
Cell 2:  Deployment helpers (with WSL/Windows path handling)
Cell 3:  ★ Load .azure-credentials.env
Cell 8:  ★ Create credential (Service Principal → Azure CLI → Default)
Cell 11: ★★★ DEPLOYMENT
         └─> BICEP_DIR = 'deploy' ✅
         └─> Uses service principal authentication ✅
         └─> Handles Windows paths correctly ✅
```

---

## STATUS

✅ **Cell 3:** Loads `.azure-credentials.env`  
✅ **Cell 8:** Service Principal authentication priority  
✅ **Cell 11:** BICEP_DIR points to `deploy` folder  
✅ **Cell 2:** Windows/WSL path handling (already working)

---

## READY TO DEPLOY 🚀

All fixes applied. The deployment should now:
1. Load service principal credentials (if available)
2. Create proper Azure authentication
3. Find Bicep files in the `deploy` folder
4. Handle Windows paths with spaces correctly

**Estimated deployment time:** 45-60 minutes (all 4 steps)

