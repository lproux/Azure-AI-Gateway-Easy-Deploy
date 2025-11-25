# Current APIM Policy Analysis

**Date**: 2025-11-23
**Status**: Policy has `system-assigned` auth but still has issues

---

## Current Policy (from Azure Portal)

```xml
<policies>
    <inbound>
        <base />
        <!-- Semantic Cache Lookup: Check Redis for similar prompts (score >= 0.8) -->
        <azure-openai-semantic-cache-lookup
            score-threshold="0.8"
            embeddings-backend-id="embeddings-backend"
            embeddings-backend-auth="system-assigned" />
    </inbound>
    <backend>
        <base />
    </backend>
    <outbound>
        <!-- Cache the response in Redis for 2 minutes -->
        <azure-openai-semantic-cache-store duration="120" />
        <base />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>
```

---

## Policy Analysis

### ✅ What's Correct:
1. **System-Assigned Auth Present**: `embeddings-backend-auth="system-assigned"` ✅
   - This is the critical fix that was missing before
   - Should allow embeddings to work

2. **Semantic Cache Lookup**: Correctly configured with 0.8 threshold ✅

3. **Semantic Cache Store**: Present in outbound section ✅

### ❌ Issues Found:

1. **Cache Duration Still Short**:
   ```xml
   <azure-openai-semantic-cache-store duration="120" />
   ```
   - Current: 120 seconds (2 minutes)
   - **Requested**: 1200 seconds (20 minutes)
   - **Action needed**: Re-apply policy with correct duration

2. **Missing Backend Service Directive**:
   - The policy doesn't have `<set-backend-service backend-id="inference-backend-pool" />`
   - This might be why it's failing with 500 errors
   - The policy needs to route to the backend pool

3. **Missing Retry Logic**:
   - Our corrected policy had retry logic for 429/503 errors
   - Current policy doesn't have this

---

## Comparison: Current vs Expected

| Element | Current | Expected (from working notebook) |
|---------|---------|----------------------------------|
| `embeddings-backend-auth` | ✅ `system-assigned` | ✅ `system-assigned` |
| Cache duration | ❌ 120s | ✅ 1200s |
| `<set-backend-service>` | ❌ Missing | ✅ Present |
| Retry logic in `<backend>` | ❌ Missing | ✅ Present |

---

## Why 500 Errors Persist

Even though `system-assigned` auth is present, you're still getting 500 errors because:

1. **Missing Backend Service Directive**: The policy doesn't specify which backend pool to use
   - Without `<set-backend-service backend-id="inference-backend-pool" />`, APIM doesn't know where to route embedding requests
   - This causes internal server errors

2. **Policy Incomplete**: The current policy is simpler than the working policy
   - Missing retry logic
   - Missing backend service routing

---

## Root Cause Discovery

Looking at the current policy, it appears someone manually edited it in the Azure Portal and:
- ✅ Added `embeddings-backend-auth="system-assigned"` (good!)
- ❌ But removed other critical elements like backend routing
- ❌ Kept cache duration at 120s instead of 1200s

This explains why:
- Standalone semantic-caching notebook works (it was using a complete policy)
- Master notebook fails (it's using this incomplete policy)

---

## Solution

We need to re-apply the COMPLETE corrected policy from `semantic-caching-policy-CORRECT.xml`:

```xml
<policies>
    <inbound>
        <base />
        <check-header name="api-key" failed-check-httpcode="401" failed-check-error-message="Missing or invalid API key" />
        <azure-openai-semantic-cache-lookup
            score-threshold="0.8"
            embeddings-backend-id="embeddings-backend"
            embeddings-backend-auth="system-assigned" />
        <set-backend-service backend-id="inference-backend-pool" />  <!-- CRITICAL -->
    </inbound>
    <backend>
        <retry count="2" interval="0" first-fast-retry="true"
               condition="@(context.Response.StatusCode == 429 || context.Response.StatusCode == 503)">
            <forward-request buffer-request-body="true" />
        </retry>
    </backend>
    <outbound>
        <base />
        <azure-openai-semantic-cache-store duration="1200" />  <!-- 20 minutes -->
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>
```

**Key Additions Needed**:
1. ✅ Keep `embeddings-backend-auth="system-assigned"` (already there)
2. ➕ Add `<set-backend-service backend-id="inference-backend-pool" />` (CRITICAL FIX)
3. ➕ Add retry logic in `<backend>` section
4. ➕ Change cache duration to 1200 seconds

---

## Next Steps

1. **Re-apply complete policy**:
   ```bash
   python3 apply_correct_semantic_policy.py
   ```

2. **Wait 60 seconds** for policy propagation

3. **Test master notebook cells 62-63**:
   - Should now work because backend routing is fixed
   - Embeddings will route to correct backend pool
   - Semantic caching will work with system-assigned auth

---

## Why Standalone Notebook Works

The standalone semantic-caching notebook works because:
- It uses the COMPLETE policy (applied earlier)
- Has all required elements: auth, backend routing, retry logic
- This is why you saw "SEMANTIC CACHING WORKS!!!!!"

The master notebook fails because:
- The current policy is incomplete (missing backend routing)
- Even with correct auth, APIM doesn't know where to send requests
- Results in 500 internal server errors

---

**Conclusion**: The fix applied earlier was partially reverted or modified. We need to re-apply the COMPLETE policy with all elements.
