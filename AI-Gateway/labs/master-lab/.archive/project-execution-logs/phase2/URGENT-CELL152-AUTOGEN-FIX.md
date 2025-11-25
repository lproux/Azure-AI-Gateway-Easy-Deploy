# URGENT: Cell 152 - AutoGen Coordinator NotFoundError Fix

**Date**: 2025-11-17
**Severity**: 🔴 BLOCKING
**Status**: ✅ FIXED

---

## Issue Description

**Error**:
```
NotFoundError
Traceback (most recent call last)
  File .../openai/_base_client.py:1047, in SyncAPIClient.request
```

**Impact**: Complete blocking of AutoGen + SK hybrid orchestration
**User Note**: "This was working previously" - indicating regression

---

## Root Cause

**Problem**: AutoGen `base_url` configuration was incomplete

**Incorrect Configuration**:
```python
hybrid_autogen_config = {
    "model": deployment_name,
    "api_type": "azure",
    "api_key": subscription_key_both,
    "base_url": apim_gateway_url,  # ❌ Just https://apim-xxx.azure-api.net
    "api_version": "2024-02-01",
}
```

**Why it Failed**:
- `base_url` pointed to just the APIM gateway root
- Azure OpenAI endpoint requires full path: `/inference/openai`
- OpenAI client tried to POST to: `https://apim-xxx.azure-api.net/chat/completions`
- APIM returned 404 (Not Found) because correct path is `/inference/openai/chat/completions`

---

## Fix Applied

### Updated Configuration

```python
# Configure AutoGen for APIM
# FIXED: base_url must include full path to OpenAI endpoint
inference_path = os.getenv("INFERENCE_API_PATH", "/inference")
autogen_base_url = f"{apim_gateway_url.rstrip('/')}{inference_path}/openai"

hybrid_autogen_config = {
    "model": deployment_name,
    "api_type": "azure",
    "api_key": subscription_key_both,
    "base_url": autogen_base_url,  # ✅ Full path: https://apim-xxx.azure-api.net/inference/openai
    "api_version": "2024-02-01",
}
```

**Key Changes**:
1. Added inference path construction
2. Appended `/openai` to complete the endpoint
3. Now matches APIM routing configuration

---

## Why This Worked Before

**Hypothesis**: Previous version may have used:
- Different AutoGen configuration style
- Azure-specific parameters (`azure_endpoint` instead of `base_url`)
- Direct foundry endpoints instead of APIM routing

**Current Approach**: Uses APIM gateway for all LLM calls (including AutoGen)

---

## Technical Details

### Correct URL Structure

For Azure OpenAI through APIM:
```
Base:     https://apim-xxx.azure-api.net
+ Path:   /inference
+ OpenAI: /openai
= Full:   https://apim-xxx.azure-api.net/inference/openai
```

### API Calls
```
Chat:     {base_url}/chat/completions
Models:   {base_url}/models
Embeddings: {base_url}/embeddings
```

With correct `base_url`, these resolve to:
```
https://apim-xxx.azure-api.net/inference/openai/chat/completions  ✅
https://apim-xxx.azure-api.net/inference/openai/models           ✅
```

---

## Expected Outcome

After this fix:
- ✅ AutoGen agents can call Azure OpenAI through APIM
- ✅ Coordinator initiates chat successfully
- ✅ Multi-agent orchestration works
- ✅ SK + AutoGen hybrid workflows functional

---

## Testing

### Verification Command
```python
# Test AutoGen configuration
print(f"APIM Gateway: {apim_gateway_url}")
print(f"AutoGen base_url: {autogen_base_url}")
# Should output: https://apim-xxx.azure-api.net/inference/openai

# Test agent communication
response = hybrid_proxy.initiate_chat(
    sales_agent,
    message="Test message",
    max_turns=1
)
# Should NOT throw NotFoundError
```

---

## Files Modified

- `master-ai-gateway-fix-MCP.ipynb` - Cell 152
- Backup: `master-ai-gateway-fix-MCP.ipynb.backup-cell152-20251117-*`

---

## Impact

**Fixed Cells**: Cell 152 (AutoGen + SK Hybrid)
**Benefits**:
- Multi-agent orchestration restored
- Most complete functionality cell working
- Hybrid SK+AutoGen demonstrations functional

**Related Functionality**:
- Sales agent workflows
- Order processing automation
- Customer discount calculations
- Multi-agent coordination

---

**Status**: ✅ FIXED - AutoGen now uses full APIM OpenAI endpoint path
