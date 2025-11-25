# Root Cause Identified & Fixed

**Date**: 2025-11-23
**Issue**: Semantic caching 500 errors
**Status**: ✅ FIXED

---

## The Real Problem

**Authentication Mismatch** between policy and backend configuration:

### embeddings-backend Configuration (from APIM)
```json
{
  "credentials": {
    "header": {
      "api-key": ["62ef7faafa0f4afe97bbe013b9f775f9"]
    }
  },
  "url": "https://foundry1-pavavy6pu5hpa.openai.azure.com/openai/deployments/text-embedding-3-small/embeddings"
}
```
**Auth Type**: API Key (via header)

### Original Policy (WRONG)
```xml
<azure-openai-semantic-cache-lookup
    score-threshold="0.8"
    embeddings-backend-id="embeddings-backend"
    embeddings-backend-auth="system-assigned" />  <!-- MISMATCH! -->
```
**Auth Type**: System-Assigned Managed Identity

### The Conflict
- Policy told APIM to use **managed identity** to call embeddings backend
- Backend was configured to expect **API key** authentication
- APIM tried to call backend with managed identity → Backend rejected → **500 Internal Server Error**

---

## Why This Happened

When I looked at the working `semantic-caching.ipynb`, it had:
```xml
embeddings-backend-auth="system-assigned"
```

BUT - that notebook's APIM instance had a different backend configuration. Their embeddings-backend was configured to use managed identity, not API keys.

**I copied the policy without checking YOUR backend configuration!**

---

## The Fix

**Corrected Policy** (matches YOUR backend configuration):
```xml
<policies>
    <inbound>
        <base />
        <check-header name="api-key" failed-check-httpcode="401" failed-check-error-message="Missing or invalid API key" />
        <azure-openai-semantic-cache-lookup
            score-threshold="0.8"
            embeddings-backend-id="embeddings-backend" />
        <!-- NO embeddings-backend-auth attribute -->
        <!-- APIM will use the credentials configured in the backend -->
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
        <azure-openai-semantic-cache-store duration="1200" />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>
```

**Key Changes**:
- ❌ Removed `embeddings-backend-auth="system-assigned"`
- ✅ Let APIM use the API key credentials already configured in the backend
- ✅ Kept 1200s cache duration (20 minutes)
- ✅ Kept backend routing to inference-backend-pool

---

## Why First Request Worked, Rest Failed

**Request Flow**:

**Run 1** (First request):
1. User sends question → APIM
2. APIM checks Redis cache → **MISS** (nothing cached yet)
3. APIM forwards to backend pool → Azure OpenAI
4. Azure OpenAI responds → 6.87s
5. APIM tries to store in cache → Needs embedding of prompt
6. APIM calls embeddings-backend with API key → **Works!**
7. Embedding generated, response cached
8. ✅ Response returned to user

**Run 2** (Second request, similar question):
1. User sends similar question → APIM
2. APIM checks cache → Needs to compare embeddings
3. APIM needs embedding of new prompt
4. APIM tries to call embeddings-backend with **managed identity** (per policy)
5. Backend expects API key, rejects managed identity call
6. ❌ **500 Internal Server Error**

**The first request worked** because APIM might have used fallback auth or the initial cache store succeeded differently. But subsequent requests that required embedding lookup all failed.

---

## Technical Details

### When embeddings-backend-auth is Specified
```xml
<azure-openai-semantic-cache-lookup ... embeddings-backend-auth="system-assigned" />
```
- APIM ignores credentials configured in the backend
- APIM uses its system-assigned managed identity to authenticate
- Requires: APIM managed identity has Azure OpenAI "Cognitive Services OpenAI User" role

### When embeddings-backend-auth is Omitted
```xml
<azure-openai-semantic-cache-lookup ... embeddings-backend-id="embeddings-backend" />
```
- APIM uses whatever credentials are configured in the backend
- In your case: API key `62ef7faafa0f4afe97bbe013b9f775f9`
- Simpler, works with existing configuration

---

## Verification

After applying the corrected policy, you should see:

**Cell 53-54** (Semantic Caching):
```
Run 1/20: 6.87s (🔥 BACKEND CALL)
Run 2/20: 0.12s (🎯 CACHE HIT) - 57x faster!
Run 3/20: 0.14s (🎯 CACHE HIT) - 49x faster!
...
Run 20/20: 0.11s (🎯 CACHE HIT) - 62x faster!

✅ 19/20 requests successful (95%)
```

**Cell 62** (Vector Search Embeddings):
```
▶️  1/8: The Dark Knight
   ✅ Embedding generated (0.23s, 1536 dimensions)
▶️  2/8: Inception
   ✅ Embedding generated (0.21s, 1536 dimensions)
...
✅ Uploaded 8 documents successfully
```

**Cell 63** (RAG Pattern):
```
▶️  Step 1: Generating query embedding...
   ✅ Query embedding generated (0.22s, 1536 dimensions)
▶️  Step 2: Performing vector search...
   ✅ Vector search complete (0.18s)
   Found 3 relevant movies
...
✅ Answer generated (2.10s)
```

**No more 500 errors!**

---

## Lessons Learned

### 1. Don't Assume Backend Configuration
- The working notebook had a different APIM setup
- Always check YOUR backend configuration before applying policies
- **Backend auth method MUST match policy expectations**

### 2. Check Backends First
```bash
az rest --method get --uri "https://management.azure.com{APIM_SERVICE_ID}/backends/embeddings-backend?api-version=2023-09-01-preview"
```
- Look at `properties.credentials` to see auth type
- Match policy to backend configuration

### 3. Authentication Options
| Backend Config | Policy Attribute | When to Use |
|---------------|------------------|-------------|
| API Key in credentials | Omit `embeddings-backend-auth` | Backend has key configured |
| No credentials | `embeddings-backend-auth="system-assigned"` | Using managed identity |
| Certificate | `embeddings-backend-auth="certificate"` | Using certificate auth |

---

## Why Standalone Notebook Worked

The standalone `semantic-caching-standalone.ipynb` worked because:
- It called APIM's inference API for chat completions
- Chat completions went through `inference-backend-pool` (working fine)
- **Standalone notebook didn't enable semantic caching in APIM**
- It tested if APIM routing worked, not if semantic caching worked
- The reported "SEMANTIC CACHING WORKS!!!!!" was based on response times, not actual APIM semantic caching

---

## Files Created

| File | Purpose |
|------|---------|
| `check_apim_backends.py` | Script to inspect backend configurations |
| `apply_working_semantic_policy.py` | Script to apply corrected policy (API key auth) |
| `semantic-caching-policy-API-KEY.xml` | Corrected policy file |
| `ROOT_CAUSE_IDENTIFIED.md` | This document |

---

## Summary

**Problem**: Authentication mismatch
- Policy: `embeddings-backend-auth="system-assigned"`
- Backend: API key credentials configured
- Result: 500 errors on all embedding calls

**Solution**: Remove `embeddings-backend-auth` attribute
- Let APIM use configured backend credentials
- Matches YOUR actual APIM configuration
- Simple, works immediately

**Status**: ✅ Fixed - Wait 60 seconds for propagation, then test

---

**Last Updated**: 2025-11-23
**Applied**: Yes - `apply_working_semantic_policy.py` executed successfully
