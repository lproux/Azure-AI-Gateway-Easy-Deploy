# Authentication Tests - Complete Guide

## ✅ What Was Fixed

1. **Removed duplicate JWT policy cell** (old Cell 30)
2. **Removed old single JWT test** (old Cells 31-32)
3. **Added 4 comprehensive authentication tests** (Cells 36-39)

## 📋 Final Structure

```
Cell 27: Azure CLI Login Check
Cell 28: Access Control Workshop (header)
Cell 29: Apply JWT Only Policy
Cell 30: (removed - was duplicate)
Cell 31: (removed - old test header)
Cell 32: (removed - old single test)
Cell 33: Apply Dual Auth Policy
Cell 34: Reset to API Key Policy
Cell 35: Troubleshooting

Cell 36: Authentication Tests Header
Cell 37: TEST 1 - No Auth (should fail)
Cell 38: TEST 2 - API Key Only
Cell 39: TEST 3 - JWT Only
Cell 40: TEST 4 - Dual Auth
```

## 🧪 How to Run Each Test

### Prerequisites (Run Once)
```bash
# In terminal or Jupyter cell
az login

# Then run Cell 27 to verify
```

---

### TEST 1: No Auth (Should Fail)

**Purpose**: Prove APIM blocks unauthenticated requests

**Steps**:
1. Run **Cell 37** (TEST 1 - No Auth)

**Expected Result**:
```
✅ EXPECTED: Request failed with 401 Unauthorized
Error: AuthenticationError: Error code: 401 - {'statusCode': 401, 'message': 'Invalid JWT.'}
```

---

### TEST 2: API Key Only

**Purpose**: Prove API Key authentication works

**Steps**:
1. Run **Cell 34** (Reset to API Key Policy)
2. Wait 60 seconds for policy to propagate
3. Run **Cell 38** (TEST 2 - API Key Only)

**Expected Result**:
```
✅ SUCCESS: API Key Authentication Working!
Response: API Key auth successful!
Tokens: 42
```

**If it fails**: You may have JWT policy still active. Re-run Cell 34 and wait longer.

---

### TEST 3: JWT Only

**Purpose**: Prove JWT token authentication works

**Steps**:
1. Run **Cell 29** (Apply JWT Only Policy)
2. Wait 60 seconds for policy to propagate
3. Run **Cell 39** (TEST 3 - JWT Only)

**Expected Result**:
```
✅ SUCCESS: JWT Authentication Working!
Response: JWT auth successful!
Tokens: 38
🎉 JWT token successfully validated by APIM!
```

**If it fails**:
- Check `az login` is active
- Wait longer for policy propagation (up to 2 minutes)
- Verify tenant ID is correct

---

### TEST 4: Dual Auth (JWT + API Key)

**Purpose**: Prove dual authentication (both JWT and API Key) works

**Steps**:
1. Run **Cell 33** (Apply Dual Auth Policy)
2. Wait 60 seconds for policy to propagate
3. Run **Cell 40** (TEST 4 - Dual Auth)

**Expected Result**:
```
✅ SUCCESS: Dual Authentication Working!
Response: Dual auth successful!
Tokens: 39
🎉 Both JWT and API Key validated successfully!
```

**If it fails**:
- Make sure you have valid JWT token (`az login`)
- Make sure APIM_API_KEY is loaded
- Wait for policy propagation

---

## 🔄 Testing Workflow

### Full Test Sequence

```python
# 1. Setup (once)
az login
Run Cell 27  # Azure CLI check

# 2. Test API Key mode
Run Cell 34  # Reset to API Key
Wait 60 seconds
Run Cell 38  # TEST 2 - API Key ✅

# 3. Test JWT mode
Run Cell 29  # Apply JWT policy
Wait 60 seconds
Run Cell 39  # TEST 3 - JWT ✅

# 4. Test Dual Auth mode
Run Cell 33  # Apply Dual Auth
Wait 60 seconds
Run Cell 40  # TEST 4 - Dual Auth ✅

# 5. Test No Auth (always fails)
Run Cell 37  # TEST 1 - No Auth ❌ (expected)

# 6. Reset for other labs
Run Cell 34  # Reset to API Key for MCP exercises
```

---

## 🎯 What Each Test Proves

| Test | Auth Method | Headers Sent | Expected Result |
|------|-------------|--------------|-----------------|
| TEST 1 | None | (empty) | ❌ 401 Unauthorized |
| TEST 2 | API Key | `api-key: xxx` | ✅ Success |
| TEST 3 | JWT | `Authorization: Bearer xxx` | ✅ Success |
| TEST 4 | Both | `api-key: xxx`<br>`Authorization: Bearer xxx` | ✅ Success |

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Cannot get JWT token" | Run `az login` |
| "401 Unauthorized" after applying policy | Wait 60-120 seconds for propagation |
| "APIM_API_KEY not set" | Run Cell 022 to load environment |
| TEST 2 fails with JWT error | Policy not propagated, run Cell 34 again |
| TEST 3 fails with API key error | Policy not propagated, run Cell 29 again |

---

## 📝 Notes

- **Policy Propagation**: APIM policies take 30-120 seconds to propagate globally
- **JWT Token Expiry**: JWT tokens expire after ~1 hour, re-run `az login` if expired
- **Sequential Testing**: Always reset to API Key (Cell 34) between different tests
- **MCP Exercises**: Require API Key mode (Cell 34) to be active

---

**Status**: ✅ All 4 authentication tests ready to use!
**Date**: 2025-11-21
**Notebook**: master-ai-gateway-fix-MCP-clean.ipynb
