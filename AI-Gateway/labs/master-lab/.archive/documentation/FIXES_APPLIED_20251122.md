# 🔧 Fixes Applied - November 22, 2025

## 📋 Summary

Multiple issues identified and fixed in the master notebook after running semantic caching cells.

---

## ✅ FIXED ISSUES

### 1. API 500 Internal Server Errors (CRITICAL - FIXED)

**Problem**:
- Semantic caching policy was causing 500 errors on ALL API requests
- First 2 requests succeeded, then all subsequent requests failed
- Backend URL had typo: `azure.comopenai` instead of `azure.com/openai`

**Root Cause**:
```xml
<!-- Broken policy caused by Cell 52 -->
<azure-openai-semantic-cache-lookup ... />
```
- Embeddings backend was not properly configured
- Policy referenced non-existent backend
- This broke the entire API

**Fix Applied**:
✅ **Restored basic policy** (removed semantic caching)
```bash
python3.12 restore_basic_policy.py
```

**Result**:
- ✅ API now works! (0.76s response time)
- ✅ All cells should work now (except those requiring semantic caching)

**Files Created**:
- `restore-basic-policy.xml` - Basic working policy
- `restore_basic_policy.py` - Script to apply it
- `test_api_working.py` - Test script

---

### 2. Cosmos DB RBAC Permissions (FIXED)

**Problem**:
```
(Forbidden) Request blocked by Auth cosmos-pavavy6pu5hpa :
Request for Read DatabaseAccount is blocked because principal
[c1a04baa-9221-4490-821b-5968bbf3772b] does not have required
RBAC permissions to perform action
[Microsoft.DocumentDB/databaseAccounts/sqlDatabases/write]
```

**Root Cause**:
- Service principal `c1a04baa-9221-4490-821b-5968bbf3772b` had no Cosmos DB permissions
- Cosmos DB requires Azure AD authentication (local auth disabled)

**Fix Applied**:
✅ **Granted Cosmos DB Built-in Data Contributor role**
```bash
python3.12 grant_cosmos_rbac.py
```

**Result**:
- ✅ Service principal now has read/write access to Cosmos DB
- ⏳ Wait 60 seconds for permissions to propagate
- 🎯 Lab 10 (cells 58-60) should work now

**Files Created**:
- `grant_cosmos_rbac.py` - Script to grant permissions

---

### 3. Semantic Caching Cells Updated (PARTIAL)

**Problem**:
- Original semantic caching cells (53-55) were not using the working code
- Wrong API version
- Complex extra_headers approach

**Fix Applied**:
✅ **Updated cells 53-55** with working code from `semantic-caching.ipynb`
```bash
python3.12 update_semantic_caching.py
```

**What Changed**:
- Cell 53: Uses API version `2025-03-01-preview`
- Cell 54: Better visualization
- Cell 55: Added Redis statistics

**Current Status**:
- ⚠️ Cells updated, but semantic caching policy was removed to fix 500 errors
- ℹ️ Cells 53-55 will work WITHOUT caching (just normal API calls)
- ℹ️ To enable caching again, need to properly configure embeddings backend first

---

## ⚠️ KNOWN ISSUES (NOT YET FIXED)

### 1. Azure CLI APIM Commands Missing

**Problem**:
```
ERROR: 'backend' is misspelled or not recognized by the system
ERROR: 'policy' is misspelled or not recognized by the system
ERROR: 'cache' is misspelled or not recognized by the system
```

**Root Cause**:
- Azure CLI APIM extension not installed or outdated

**Fix Needed**:
```bash
# Install APIM extension
az extension add --name apim

# Or update if already installed
az extension update --name apim
```

---

### 2. Semantic Caching Not Configured

**Problem**:
- Removed semantic caching policy to fix 500 errors
- Embeddings backend not created (URL had typo)
- Cell 52 fails with "backend not recognized"

**Root Cause**:
1. Backend URL typo: `https://foundry1-pavavy6pu5hpa.openai.azure.comopenai/...`
   - Should be: `https://foundry1-pavavy6pu5hpa.openai.azure.com/openai/...`

2. Azure CLI can't run `az apim backend create` (extension missing)

**Fix Needed**:
1. Install Azure CLI APIM extension
2. Create embeddings backend with correct URL
3. Apply semantic caching policy
4. Test cells 53-55 again

**Manual Fix (Azure Portal)**:
1. Go to APIM service > APIs > inference-api
2. Click "Backends" > "Add"
3. Create backend:
   - ID: `embeddings-backend`
   - URL: `https://foundry1-pavavy6pu5hpa.openai.azure.com/openai/deployments/text-embedding-3-small/embeddings`
4. Apply semantic caching policy from `semantic-caching-policy.xml`

---

### 3. Azure AI Search 500 Errors (Cells 62-63)

**Problem**:
```
Error code: 500 - {'statusCode': 500, 'message': 'Internal server error'}
```

**Status**:
- ⚠️ May be related to the broken semantic caching policy
- 🎯 Re-test after confirming API is fully working

**Possible Causes**:
1. Semantic caching policy breaking embeddings calls
2. Search service configuration issue
3. Missing RBAC permissions

**Fix Needed**:
- Re-test cells 62-63 now that basic policy is restored
- If still failing, check Search service permissions

---

## 📊 Lab Status After Fixes

| Lab | Cells | Status | Notes |
|-----|-------|--------|-------|
| Lab 09: Semantic Caching | 52-55 | ⚠️ Partial | API works, caching disabled |
| Lab 10: Message Storing | 58-60 | ✅ Should work | Cosmos RBAC granted |
| Lab 11: Vector Search | 62-63 | ⚠️ Unknown | Need to re-test |

---

## 🚀 What to Do Next

### Immediate (Test Now):

1. **Re-open notebook with Python 3.12 kernel**

2. **Test basic API functionality**:
   - Run any cell that makes API requests
   - Should work without 500 errors now

3. **Test Cosmos DB (Lab 10)**:
   - Wait 60 seconds for RBAC propagation
   - Run cells 58-60
   - Should work now

4. **Test Vector Search (Lab 11)**:
   - Run cells 62-63
   - Check if 500 errors are gone

### Later (To Enable Semantic Caching):

1. **Install Azure CLI APIM extension**:
   ```bash
   az extension add --name apim
   ```

2. **Create embeddings backend** (via Portal or CLI):
   - Fix URL typo: `azure.comopenai` → `azure.com/openai`
   - Backend ID: `embeddings-backend`

3. **Re-run Cell 52** to apply semantic caching policy

4. **Test cells 53-55** to verify caching works

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `restore-basic-policy.xml` | Basic APIM policy without caching |
| `restore_basic_policy.py` | Script to apply basic policy |
| `test_api_working.py` | Test if API is functional |
| `grant_cosmos_rbac.py` | Grant Cosmos DB permissions |
| `FIXES_APPLIED_20251122.md` | This summary document |

---

## 🎯 Quick Commands

```bash
# Test if API is working
python3.12 test_api_working.py

# Restore basic policy (if needed again)
python3.12 restore_basic_policy.py

# Grant Cosmos DB permissions (if needed again)
python3.12 grant_cosmos_rbac.py

# Check Azure CLI APIM extension
az extension list | grep apim
```

---

## ✅ Success Criteria

After these fixes, you should be able to:

1. ✅ Make API requests without 500 errors
2. ✅ Store messages in Cosmos DB (Lab 10)
3. ✅ Test vector search (Lab 11) - if it was just policy-related
4. ⚠️ Semantic caching (Lab 09) - requires additional setup

---

## 💡 Key Learnings

1. **Broken APIM policies can break the entire API**
   - Always test policy changes carefully
   - Keep a working policy backup

2. **Cosmos DB requires proper RBAC**
   - Service principals need explicit role assignments
   - Permissions take 30-60 seconds to propagate

3. **Azure CLI extensions matter**
   - APIM commands require `az extension add --name apim`
   - Check extension status before debugging commands

4. **URL typos can be critical**
   - `azure.comopenai` vs `azure.com/openai`
   - Always verify URLs carefully

---

**Last Updated**: 2025-11-22
**Status**: API Restored ✅ | Cosmos Fixed ✅ | Caching Disabled ⚠️
