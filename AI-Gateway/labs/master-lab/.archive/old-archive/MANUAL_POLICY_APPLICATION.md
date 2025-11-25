# Manual Policy Application Guide - Semantic Caching

**Issue**: Azure CLI is having errors, so we'll apply the policy manually through the Azure Portal.

**Time required**: 2-3 minutes

---

## 📋 Step-by-Step Instructions

### Step 1: Open Azure Portal

1. Go to: https://portal.azure.com
2. Sign in with your account

### Step 2: Navigate to API Management

1. In the search bar at the top, type: **API Management**
2. Click on **API Management services**
3. Click on your APIM service: **apim-pavavy6pu5hpa**

### Step 3: Open the Inference API

1. In the left menu, click **APIs**
2. Find and click **inference-api** in the list of APIs

### Step 4: Open Policy Editor

1. Click on **All operations** (at the top of the operations list)
2. In the **Inbound processing** section, click **</>** (the code view icon)
   - This will open the policy code editor

### Step 5: Add Semantic Caching Policy

You'll see existing policy XML. You need to **add the semantic caching lines** to the existing policy.

**Current policy probably looks like:**
```xml
<policies>
    <inbound>
        <base />
        <authentication-managed-identity resource="https://cognitiveservices.azure.com" />
        <!-- Other existing policies may be here -->
    </inbound>
    <backend>
        <base />
    </backend>
    <outbound>
        <base />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>
```

**Modify it to add semantic caching (in bold):**

1. In the `<inbound>` section, **after** `<base />`, add:
```xml
<!-- Semantic Cache Lookup: Check Redis for similar prompts (score >= 0.8) -->
<azure-openai-semantic-cache-lookup
    score-threshold="0.8"
    embeddings-backend-id="embeddings-backend"
    embeddings-backend-auth="system-assigned" />
```

2. In the `<outbound>` section, **after** `<base />`, add:
```xml
<!-- Cache the response in Redis for 2 minutes -->
<azure-openai-semantic-cache-store duration="120" />
```

**Final policy should look like:**
```xml
<policies>
    <inbound>
        <base />
        <!-- Semantic Cache Lookup: Check Redis for similar prompts (score >= 0.8) -->
        <azure-openai-semantic-cache-lookup
            score-threshold="0.8"
            embeddings-backend-id="embeddings-backend"
            embeddings-backend-auth="system-assigned" />
        <authentication-managed-identity resource="https://cognitiveservices.azure.com" />
        <!-- Other existing policies may be here -->
    </inbound>
    <backend>
        <base />
    </backend>
    <outbound>
        <base />
        <!-- Cache the response in Redis for 2 minutes -->
        <azure-openai-semantic-cache-store duration="120" />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>
```

### Step 6: Save the Policy

1. Click **Save** at the bottom of the policy editor
2. You should see a success message

### Step 7: Wait for Propagation

⏳ Wait **60 seconds** for the policy to propagate globally.

---

## ✅ Verification

### Option 1: Check in Portal

1. In the policy editor, verify you see:
   - `azure-openai-semantic-cache-lookup` in the `<inbound>` section
   - `azure-openai-semantic-cache-store` in the `<outbound>` section

2. If both are present → ✅ Policy applied successfully!

### Option 2: Test with Notebook

1. Wait 60 seconds after saving
2. Run **Cell 53** (Test Semantic Caching)
3. Look for cache hits (responses < 0.5 seconds)

---

## 📊 Expected Results After Manual Application

**When you run Cell 53, you should see:**

```
▶️  Run 1/20: How to Brew the Perfect Cup of Coffee?
   ⏱️  1.234s - 🔥 BACKEND CALL

▶️  Run 2/20: What are the steps to Craft the Ideal Espresso?
   ⏱️  0.156s - 🎯 CACHE HIT

▶️  Run 3/20: Tell me how to create the best steaming Java?
   ⏱️  0.143s - 🎯 CACHE HIT

...

📊 PERFORMANCE SUMMARY
Likely Cache Hits:  17/20 (85%)
```

---

## 🐛 Troubleshooting

### Issue: Can't find "inference-api"

**Solution**: The API might have a different name
1. In APIs list, look for an API related to OpenAI or inference
2. Click on it to verify it's the right one
3. The API ID should be in the URL: `/apis/inference-api`

### Issue: "embeddings-backend not found" error when saving

**Solution**: Run **Cell 51** in the notebook first
- This creates the embeddings-backend that the policy references
- Then come back and apply the policy

### Issue: Policy saves but no cache hits

**Possible causes**:
1. **Wait longer** - Policy can take up to 2 minutes to propagate
2. **Redis not configured** - Check Azure Portal → API Management → External cache → Caches
   - Should see "default" cache
   - If not, the setup script didn't work - we can fix this manually too

---

## 💡 Policy Explanation

### What Each Part Does

**Inbound (before calling Azure OpenAI)**:
```xml
<azure-openai-semantic-cache-lookup
    score-threshold="0.8"
    embeddings-backend-id="embeddings-backend"
    embeddings-backend-auth="system-assigned" />
```
- Converts the prompt to a vector using embeddings-backend
- Searches Redis cache for similar prompts (>80% similarity)
- If found → returns cached response (skip backend call)
- If not found → continues to backend

**Outbound (after receiving response from Azure OpenAI)**:
```xml
<azure-openai-semantic-cache-store duration="120" />
```
- Stores the response in Redis cache
- Associates it with the prompt's vector
- Cache expires after 120 seconds (2 minutes)

---

## 🎯 Alternative: Copy Full Policy

If you prefer to replace the entire policy, here's the complete policy XML:

```xml
<policies>
    <inbound>
        <base />
        <!-- Semantic Cache Lookup: Check Redis for similar prompts (score >= 0.8) -->
        <azure-openai-semantic-cache-lookup
            score-threshold="0.8"
            embeddings-backend-id="embeddings-backend"
            embeddings-backend-auth="system-assigned" />
        <authentication-managed-identity resource="https://cognitiveservices.azure.com" />
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

**⚠️ Note**: This assumes you want to keep managed identity authentication. If you're using API key only, you can remove the `<authentication-managed-identity>` line.

---

## ✅ Summary

**What you just did**:
1. ✅ Opened Azure Portal
2. ✅ Navigated to API Management → APIs → inference-api
3. ✅ Edited the policy to add semantic caching
4. ✅ Saved the policy

**What happens now**:
- Requests are converted to vectors and checked against Redis cache
- Similar requests (>80% similarity) get cached responses
- 10-20x faster responses for similar queries
- 70-90% cost reduction for repetitive questions

**Next step**: Run Cell 53 in your notebook to test! 🎉

---

**Need help?** Take a screenshot of the policy editor and I can verify it's correct.
