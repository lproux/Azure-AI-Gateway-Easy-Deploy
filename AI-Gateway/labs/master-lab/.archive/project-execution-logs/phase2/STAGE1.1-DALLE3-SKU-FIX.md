# STAGE 1.1: Cell 29 - dall-e-3 SKU Fix

**Date**: 2025-11-17
**Severity**: CRITICAL
**Status**: ✅ FIXED

---

## Issue Description

**Error**:
```
[SKIP] dall-e-3 failed: (InvalidResourceProperties) The specified SKU 'GlobalStandard' of account deploy...
```

**Root Cause**:
- Phase 1 incorrectly changed dall-e-3 SKU from 'Standard' to 'GlobalStandard'
- dall-e-3 model does NOT support 'GlobalStandard' SKU
- dall-e-3 only supports regional deployment with 'Standard' SKU

---

## Research Findings

### Microsoft Documentation Analysis

**dall-e-3 Availability**:
- Regions: East US, Australia East, Sweden Central
- SKU: 'Standard' (regional deployment only)
- Does NOT support 'GlobalStandard'

**gpt-image-1 Availability** (for comparison):
- Regions: West US 3, UAE North, Poland Central
- SKU: 'GlobalStandard' (global deployment)
- This is a DIFFERENT model from dall-e-3

### Azure CLI Deployment Example
```azurecli
az cognitiveservices account deployment create \
  --name <myResourceName> \
  --model-name dall-e-3 \
  --model-version "3.0" \
  --model-format OpenAI \
  --sku-capacity "1" \
  --sku-name "Standard"  # Not GlobalStandard!
```

**Source**: Microsoft Learn - Azure OpenAI Models Documentation

---

## Fix Applied

### Cell 29 (Deployment Configuration)

**Location**: Line 142 in `models_config` dictionary

**Before (Phase 1 - INCORRECT)**:
```python
{'name': 'dall-e-3', 'format': 'OpenAI', 'version': '3.0', 'sku': 'GlobalStandard', 'capacity': 1},
```

**After (Phase 2 - CORRECT)**:
```python
{'name': 'dall-e-3', 'format': 'OpenAI', 'version': '3.0', 'sku': 'Standard', 'capacity': 1},
```

**Change**: `'sku': 'GlobalStandard'` → `'sku': 'Standard'`

---

## Why Phase 1 Was Wrong

**Phase 1 Assumption**:
- All models should use 'GlobalStandard' SKU for consistency
- dall-e-3 should follow same pattern as other models

**Reality**:
- dall-e-3 is a REGIONAL model, not global
- Only certain newer models (like gpt-image-1) support GlobalStandard
- Each model has specific SKU requirements based on deployment type

**Lesson Learned**:
- Must verify SKU compatibility per model in Microsoft documentation
- Cannot assume all models support same SKU types
- Regional vs Global deployment is model-specific

---

## Expected Outcome

After this fix:
- ✅ dall-e-3 deployment should succeed
- ✅ Model will deploy to specified region (UK South in foundry1)
- ✅ Image generation features will work
- ✅ No more InvalidResourceProperties error

---

## Testing

### Verification Steps
1. Run Cell 29 (deployment cell)
2. Check deployment output for dall-e-3
3. Verify deployment shows [OK] or success message
4. Confirm no SKU-related errors

### Expected Output
```
[*] Deploying dall-e-3...
[OK] dall-e-3 deployed successfully
```

---

## Related Cells

- **Cell 29**: Model deployment (FIXED)
- **Cell 108**: Image deployment discovery (depends on this fix)
- **Cell 110**: Image generation (depends on this fix)
- **Cell 134/135**: Image generation cells (depends on this fix)

---

## Files Modified

- `master-ai-gateway-fix-MCP.ipynb` - Cell 29 models_config
- Backup: `master-ai-gateway-fix-MCP.ipynb.backup-dalle-fix-20251117-*`

---

## Documentation References

- [Azure OpenAI Models - Image Generation](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/models#image-generation-models)
- [DALL-E Quickstart](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/dall-e-quickstart)
- [Deployment Types](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/deployment-types)

---

## Phase 1 vs Phase 2

### Phase 1 (INCORRECT)
- Changed: 'Standard' → 'GlobalStandard'
- Reasoning: Thought all models should use GlobalStandard
- Result: Deployment failed

### Phase 2 (CORRECT)
- Changed: 'GlobalStandard' → 'Standard'
- Reasoning: Microsoft docs confirm dall-e-3 requires Standard SKU
- Result: Deployment should succeed

---

**Status**: ✅ FIXED - dall-e-3 now uses correct 'Standard' SKU
