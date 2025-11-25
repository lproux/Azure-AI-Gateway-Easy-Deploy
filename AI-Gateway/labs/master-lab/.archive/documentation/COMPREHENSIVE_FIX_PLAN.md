# 🎯 Comprehensive Fix Plan - All Issues Tracked

**Date**: 2025-11-22
**Status**: In Progress

---

## 📊 Issues Tracker

### 🔴 CRITICAL - Cell 53-54: Semantic Caching 500 Errors

**Problem**:
- First request succeeds (2.60s)
- All subsequent requests fail with 500 errors
- Only 1/20 requests successful

**Root Cause**:
The policy I applied uses API key authentication for embeddings backend, but the **WORKING** semantic-caching.ipynb uses:
```xml
embeddings-backend-auth="system-assigned"  <!-- Managed Identity! -->
```

**My Policy** (WRONG):
```xml
<azure-openai-semantic-cache-lookup score-threshold="0.8" embeddings-backend-id="embeddings-backend" ignore-system-messages="true" max-message-count="10">
```

**Working Policy** (CORRECT):
```xml
<azure-openai-semantic-cache-lookup score-threshold="0.8" embeddings-backend-id="embeddings-backend" embeddings-backend-auth="system-assigned" />
```

**Differences**:
1. ❌ Missing `embeddings-backend-auth="system-assigned"`
2. ❌ Extra attributes: `ignore-system-messages`, `max-message-count`
3. ❌ Has `<vary-by>@(context.Subscription.Id)</vary-by>` child element

**Fix Plan**:
- [ ] Update policy to match working notebook exactly
- [ ] Remove extra attributes
- [ ] Add `embeddings-backend-auth="system-assigned"`
- [ ] Test semantic caching again

**Status**: 🔴 In Progress

---

### 🟡 MEDIUM - Cell 54: Division by Zero Error

**Problem**:
```python
ZeroDivisionError: division by zero
print(f"avg ~{sum(valid_results[1:])/len(valid_results[1:]):.2f}s)")
```

**Root Cause**:
- Only 1 successful request
- `valid_results[1:]` is empty list
- Division by zero when calculating average

**Fix**:
```python
# Add check for list length
if len(valid_results) > 1:
    avg_cached = sum(valid_results[1:]) / len(valid_results[1:])
    print(f"   Subsequent requests faster (cache hits, avg ~{avg_cached:.2f}s)")
else:
    print("   No cached requests to show (only 1 successful request)")
```

**Status**: 🟡 Ready to fix

---

### 🟡 MEDIUM - Cell 56: Redis Cache TTL Too Short

**Problem**:
- Expired Keys: 38 (constantly increasing)
- User wants 20-minute TTL instead of 2 minutes

**Current Config**:
```xml
<azure-openai-semantic-cache-store duration="120" />  <!-- 2 minutes -->
```

**Desired Config**:
```xml
<azure-openai-semantic-cache-store duration="1200" />  <!-- 20 minutes -->
```

**Fix Plan**:
- [ ] Update policy with `duration="1200"`
- [ ] Re-apply policy
- [ ] Test cache expiry

**Status**: 🟡 Ready to fix

---

### 🔴 CRITICAL - Cell 58: Cosmos DB RBAC Permissions

**Problem**:
```
Request blocked by Auth cosmos-pavavy6pu5hpa : principal [c1a04baa-9221-4490-821b-5968bbf3772b]
does not have required RBAC permissions to perform action
[Microsoft.DocumentDB/databaseAccounts/sqlDatabases/write]
```

**What I Did**:
```bash
az cosmosdb sql role assignment create \
    --account-name cosmos-pavavy6pu5hpa \
    --principal-id c1a04baa-9221-4490-821b-5968bbf3772b \
    --role-definition-id .../00000000-0000-0000-0000-000000000002 \
    --scope "/"
```

**Status**: ✅ Granted (but may need 60-90 seconds propagation)

**Fix Plan**:
- [x] RBAC granted
- [ ] Wait 90 seconds
- [ ] Re-test cell 58
- [ ] If still failing: Check if principal ID is correct
- [ ] Alternative: Grant via Azure Portal

**Status**: 🟡 Waiting for propagation

---

### 🔴 CRITICAL - Cell 60: Cosmos DB "Owner Resource Does Not Exist"

**Problem**:
```
(NotFound) Message: {"Errors":["Owner resource does not exist"]}
```

**Root Cause**:
- Database or container was never created
- Cell 58 failed, so database wasn't set up
- Cell 60 tries to query non-existent resource

**Dependencies**:
1. Cell 58 must succeed first (create database/container)
2. RBAC permissions must be granted
3. Then Cell 60 can query

**Fix Plan**:
- [ ] Fix Cell 58 (RBAC + database creation)
- [ ] Verify database exists in Azure Portal
- [ ] Then re-test Cell 60

**Status**: 🔴 Blocked by Cell 58

---

### 🔴 CRITICAL - Cell 62: Vector Search 500 Errors (Embeddings)

**Problem**:
```
Error code: 500 - {'statusCode': 500, 'message': 'Internal server error'}
```
When generating embeddings for movies.

**Root Cause**:
Same as Cell 53-54! The semantic caching policy is breaking ALL embedding calls:
- Cell 62 tries to call embeddings model
- Semantic caching policy intercepts
- Embeddings backend auth fails
- 500 error returned

**Fix Plan**:
- [ ] Fix semantic caching policy (add system-assigned auth)
- [ ] Re-test cell 62
- [ ] Should work once policy is fixed

**Status**: 🔴 Blocked by semantic caching policy

---

### 🔴 CRITICAL - Cell 63: RAG Pattern 500 Errors

**Problem**:
Same as Cell 62 - can't generate embeddings.

**Root Cause**:
Same - semantic caching policy breaking embeddings.

**Fix Plan**:
- [ ] Fix semantic caching policy
- [ ] Re-test cell 63

**Status**: 🔴 Blocked by semantic caching policy

---

## 🎯 Fix Priority Order

### Priority 1: Fix Semantic Caching Policy (Fixes Cells 53-54, 62, 63)

**Impact**: Highest - fixes 4 cells at once

**Steps**:
1. ✅ Identify correct policy format from working notebook
2. ⏳ Update policy to use `embeddings-backend-auth="system-assigned"`
3. ⏳ Remove extra attributes
4. ⏳ Test semantic caching
5. ⏳ Test vector search (Cell 62-63)

**Expected Result**:
- Semantic caching works (15-100x speedup)
- Vector search embeddings work
- No more 500 errors

---

### Priority 2: Fix Cosmos DB RBAC (Fixes Cells 58, 60)

**Impact**: Medium - fixes 2 cells

**Steps**:
1. ✅ Grant RBAC role assignment
2. ⏳ Wait 90 seconds for propagation
3. ⏳ Re-test Cell 58
4. ⏳ Verify database created
5. ⏳ Re-test Cell 60

**Expected Result**:
- Cosmos DB allows database creation
- Messages stored successfully
- Query returns results

---

### Priority 3: Fix Division by Zero (Cell 54)

**Impact**: Low - cosmetic fix

**Steps**:
1. ⏳ Add length check before division
2. ⏳ Handle edge case of 0 or 1 results

**Expected Result**:
- No more division by zero error
- Graceful handling of edge cases

---

### Priority 4: Increase Cache TTL (Cell 56)

**Impact**: Low - improvement, not a bug

**Steps**:
1. ⏳ Update policy with `duration="1200"`
2. ⏳ Re-apply policy
3. ⏳ Monitor Redis expired keys

**Expected Result**:
- Fewer expired keys
- Better cache hit rate
- Longer-lived cache entries

---

## 📋 Correct Semantic Caching Policy

Based on the **WORKING** semantic-caching.ipynb:

```xml
<policies>
    <inbound>
        <base />
        <!-- CHECK: Use system-assigned managed identity for embeddings backend -->
        <azure-openai-semantic-cache-lookup
            score-threshold="0.8"
            embeddings-backend-id="embeddings-backend"
            embeddings-backend-auth="system-assigned" />

        <!-- Use the main backend pool, NOT a specific backend -->
        <set-backend-service backend-id="inference-backend-pool" />
    </inbound>
    <backend>
        <retry count="2" interval="0" first-fast-retry="true"
               condition="@(context.Response.StatusCode == 429 || context.Response.StatusCode == 503)">
            <forward-request buffer-request-body="true" />
        </retry>
    </backend>
    <outbound>
        <base />
        <!-- Cache for 20 minutes (1200 seconds) as requested -->
        <azure-openai-semantic-cache-store duration="1200" />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>
```

**Key Changes from My Policy**:
1. ✅ Added `embeddings-backend-auth="system-assigned"`
2. ✅ Removed `ignore-system-messages="true"`
3. ✅ Removed `max-message-count="10"`
4. ✅ Removed `<vary-by>` child element
5. ✅ Changed duration from 120 to 1200 (20 minutes)

---

## 🎯 Alternative Approach: New Semantic Caching Notebook

**User Request**: Create a new standalone semantic-caching notebook using master-lab resources.

**Plan**:
1. Copy structure from working `semantic-caching.ipynb`
2. Use master-lab.env for all resources
3. Use same policy format that works
4. Test in isolation
5. Compare with master notebook

**Benefits**:
- Isolates semantic caching from other labs
- Uses proven working structure
- Easier to debug
- Can compare side-by-side

**Location**:
- Source: `C:\Users\lproux\Documents\GitHub\...\semantic-caching\semantic-caching.ipynb`
- Target: `master-lab/semantic-caching-standalone.ipynb`

---

## 📊 Current Status Summary

| Cell | Lab | Issue | Status | Blocker |
|------|-----|-------|--------|---------|
| 53 | Semantic Caching | 500 errors after 1st request | 🔴 In Progress | Wrong policy auth |
| 54 | Visualization | Division by zero | 🟡 Ready to fix | Cell 53 |
| 56 | Redis Stats | TTL too short | 🟡 Ready to fix | Policy update |
| 58 | Cosmos DB Setup | RBAC permissions | 🟡 Propagating | Wait 90s |
| 60 | Cosmos DB Query | Resource not found | 🔴 Blocked | Cell 58 |
| 62 | Vector Search Setup | 500 errors | 🔴 Blocked | Cell 53 policy |
| 63 | RAG Pattern | 500 errors | 🔴 Blocked | Cell 53 policy |

---

## 🚀 Next Actions

**Immediate** (fixes 4 cells):
1. Update semantic caching policy with correct auth
2. Test cells 53-54
3. Test cells 62-63

**After 90 seconds** (fixes 2 cells):
1. Re-test Cosmos DB cells 58-60

**Final polish**:
1. Fix division by zero in cell 54
2. Create standalone semantic-caching notebook

---

**Updated**: 2025-11-22
**Next Update**: After applying corrected policy
