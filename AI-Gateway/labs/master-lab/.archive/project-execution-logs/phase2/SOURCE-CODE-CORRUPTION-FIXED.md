# Source Code Corruption - Root Cause & Fix

**Date**: 2025-11-17
**Status**: ✅ FIXED - Corruption resolved, fixes need to be re-applied

---

## Critical Discovery

Found **source code corruption** in the notebook causing 4 cells to fail silently during execution:

### Corrupted Cells (Before Fix)

| Cell | Description | Source Elements | With Newlines | Status |
|------|-------------|-----------------|---------------|--------|
| 101 | Semantic Cache Policy | 160 | 0 | ❌ Corrupted |
| 107 | DALL-E Image Generation | 274 | 0 | ❌ Corrupted |
| 136 | AutoGen A2A Agents | 230 | 0 | ❌ Corrupted |
| 140 | Vector Search | 427 | 0 | ❌ Corrupted |

**Impact**: All 4 cells executed (have execution_count) but produced ZERO outputs due to syntax errors from single-line code.

---

## Root Cause

**Notebook Edit Tool Issue**: When I edited these cells earlier, the NotebookEdit tool concatenated all source lines into single strings, removing newline characters (`\n`) between statements. This created syntax errors preventing any output.

**Example**:
```python
# Before (proper format - array of strings with newlines):
source: [
  "# Lab 22: DALL-E\n",
  "print('Starting...')\n",
  "import os\n"
]

# After corruption (array without newlines):
source: [
  "# Lab 22: DALL-E",
  "print('Starting...')",
  "import os"
]

# When joined: "# Lab 22: DALL-Eprint('Starting...')import os"
# Result: SyntaxError (no newlines between statements)
```

---

## Cells Affected & Symptoms

### Cell 101 - Semantic Cache Policy

**Symptom**: Executed (exec_count=53) but NO output
**Effect**: Policy never applied → Cell 102 cache test showed 0% hit rate
**Explanation**: Policy application cell failed silently, so test cell had no policy to work with

### Cell 107 - DALL-E Image Generation

**Symptom**: Executed (exec_count=55) but NO output
**Effect**: Image generation never ran
**Fix Applied (but lost)**: Direct foundry endpoint

### Cell 136 - AutoGen A2A Agents

**Symptom**: Executed (exec_count=68) but NO output
**Effect**: Multi-agent conversation never started
**Fix Applied (but lost)**: Endpoint validation

### Cell 140 - Vector Search with Embeddings

**Symptom**: Executed (exec_count=70) but NO output
**Effect**: Vector search never executed
**Fix Applied (but lost)**: Embedding model fix

---

## Fix Applied

### Step 1: Restore from Backup

Restored all 4 cells from `master-ai-gateway-fix-MCP copy 6.ipynb` (Nov 17 12:54):

| Cell | Restored From | Elements | With Newlines | Status |
|------|---------------|----------|---------------|--------|
| 101 | Backup Cell 16 | 149 | 149 | ✅ Fixed |
| 107 | Backup Cell 107 | 174 | 174 | ✅ Fixed |
| 136 | Backup Cell 140 | 214 | 214 | ✅ Fixed |
| 140 | Backup Cell 144 | 340 | 340 | ✅ Fixed |

### Step 2: Fixes Lost - Need Re-application

**Problem**: Backup predates my fixes, so fixes were lost:
- ❌ Cell 107: DALL-E direct endpoint fix LOST
- ❌ Cell 136: AutoGen validation fix LOST
- ❌ Cell 140: Vector Search embedding model fix LOST

**Solution**: Must re-apply these 3 fixes using proper editing method that preserves newlines

---

## Re-Application Strategy

### Method: Use Edit Tool with Line-by-Line Replacements

Instead of NotebookEdit (which corrupts newlines), use the Edit tool to:
1. Read the cell source as joined string
2. Find exact multi-line code block to replace
3. Replace with new multi-line code block
4. Edit tool preserves original line structure

### Fixes to Re-Apply

#### Fix 1: Cell 107 - DALL-E Direct Endpoint

**Find**:
```python
url = f"{apim_gateway_url.rstrip('/')}/{inference_api_path.strip('/')}/openai/deployments/{model}/images/generations?api-version={IMAGE_API_VERSION}"

headers = {
    "Content-Type": "application/json",
    "api-key": apim_api_key
}
```

**Replace With**:
```python
# Try direct foundry endpoint first, fallback to APIM
dalle_endpoint = os.getenv("MODEL_DALL_E_3_ENDPOINT_R1")
dalle_key_env = os.getenv("MODEL_DALL_E_3_KEY_R1")

if dalle_endpoint and dalle_key_env:
    endpoint = dalle_endpoint.rstrip('/')
    endpoint_key = dalle_key_env
    print(f"   Using direct foundry endpoint (bypassing APIM)")
else:
    endpoint = f"{apim_gateway_url.rstrip('/')}/{inference_api_path.strip('/')}"
    endpoint_key = apim_api_key
    print(f"   Using APIM gateway endpoint")

url = f"{endpoint}/openai/deployments/{model}/images/generations?api-version={IMAGE_API_VERSION}"

headers = {
    "Content-Type": "application/json",
    "api-key": endpoint_key
}
```

#### Fix 2: Cell 136 - AutoGen Endpoint Validation

**Find**:
```python
# AutoGen configuration pointing to APIM
autogen_config = {
    "model": deployment_name,
    "api_type": "azure",
    "api_key": apim_api_key,
    "base_url": f"{apim_gateway_url.rstrip('/')}/{inference_api_path.strip('/')}",
    "api_version": "2024-02-01",
}
```

**Replace With**:
```python
# Build correct endpoint (APIM base + inference path)
if "openai_endpoint" in globals() and openai_endpoint:
    endpoint = openai_endpoint.rstrip("/")
else:
    apim_base = apim_gateway_url if "apim_gateway_url" in globals() and apim_gateway_url else os.getenv("APIM_GATEWAY_URL", "")
    inference_path = inference_api_path if "inference_api_path" in globals() else os.getenv("INFERENCE_API_PATH", "inference")
    endpoint = f"{apim_base.rstrip('/')}/{inference_path.strip('/')}"

# Get API key
api_key = subscription_key_both if "subscription_key_both" in globals() and subscription_key_both else (
    apim_api_key if "apim_api_key" in globals() and apim_api_key else os.getenv("APIM_API_KEY", "")
)

# Validate configuration
if not endpoint or not api_key:
    print("❌ Missing AutoGen configuration:")
    if not endpoint:
        print("   - APIM endpoint not found (need APIM_GATEWAY_URL)")
    if not api_key:
        print("   - API key not found (need APIM_API_KEY or subscription_key)")
    raise RuntimeError("Missing AutoGen configuration. Please ensure master-lab.env is loaded.")

# AutoGen configuration pointing to APIM
autogen_config = {
    "model": deployment_name,
    "api_type": "azure",
    "api_key": api_key,
    "base_url": endpoint,
    "api_version": "2024-02-01",
}

config_list = [autogen_config]

print("✓ AutoGen configuration created")
print(f"  Model: {deployment_name}")
print(f"  Base URL: {endpoint}")
print(f"  API Key: {'*' * 8}{api_key[-4:] if len(api_key) > 4 else '****'}")
```

#### Fix 3: Cell 140 - Vector Search Embedding Model

**Find**:
```python
# Model Configuration
embedding_model = os.getenv("EMBEDDING_MODEL", "gpt-4o-mini")
```

**Replace With**:
```python
# Model Configuration - Use actual embedding deployment
embedding_model = (
    os.getenv("MODEL_TEXT_EMBEDDING_3_SMALL_DEPLOYMENT") or
    os.getenv("EMBEDDING_MODEL") or
    "text-embedding-3-small"  # Default to actual embedding model
)
```

**AND Find**:
```python
# Azure OpenAI client for embeddings
openai_client = AsyncAzureOpenAI(
    azure_endpoint=f"{apim_gateway_url.rstrip('/')}/{inference_api_path.strip('/')}",
    api_key=apim_api_key,
    api_version=api_version
)
```

**Replace With**:
```python
# Azure OpenAI client for embeddings - Try direct foundry endpoint first
embedding_endpoint_foundry = os.getenv("MODEL_TEXT_EMBEDDING_3_SMALL_ENDPOINT_R1")
embedding_key_foundry = os.getenv("MODEL_TEXT_EMBEDDING_3_SMALL_KEY_R1")

if embedding_endpoint_foundry and embedding_key_foundry:
    # Use direct foundry endpoint (bypassing APIM)
    embedding_endpoint = embedding_endpoint_foundry.rstrip('/')
    embedding_key = embedding_key_foundry
    print("   ℹ️  Using direct foundry endpoint for embeddings (bypassing APIM)")
else:
    # Fallback to APIM gateway
    embedding_endpoint = f"{apim_gateway_url.rstrip('/')}/{inference_api_path.strip('/')}"
    embedding_key = apim_api_key
    print("   ℹ️  Using APIM gateway endpoint for embeddings")

openai_client = AsyncAzureOpenAI(
    azure_endpoint=embedding_endpoint,
    api_key=embedding_key,
    api_version=api_version
)
```

---

## Status

**Corruption**: ✅ FIXED (all 4 cells have proper newline formatting)
**Fixes Re-applied**: ⏳ IN PROGRESS (cells 107, 136, 140)
**Ready for Test**: ⏸️ After fixes re-applied

---

## Verification Steps

After re-applying fixes:

1. **Check source formatting**:
   ```python
   # All cells should have elements with '\n'
   cell['source'] = ["line 1\n", "line 2\n", ...]
   ```

2. **Test individual cells** in Jupyter UI

3. **Run full notebook** with `jupyter nbconvert --execute`

4. **Verify outputs**:
   - Cell 101: Policy application message
   - Cell 102: Cache hit rate >0%
   - Cell 107: Image generation output
   - Cell 136: Agent conversation output
   - Cell 140: Vector search results

---

## Lessons Learned

1. **NotebookEdit Tool Risk**: Can corrupt multi-line cells by removing newlines
2. **Always Verify**: Check source array has newlines after edits
3. **Use Read/Edit Instead**: For multi-line code blocks, use Read + Edit tools
4. **Backup Before Edit**: Keep backups of working notebooks
5. **Test After Edit**: Execute cells immediately after editing to catch corruption

---

**Next**: Re-apply 3 fixes using Edit tool to preserve newlines, then retest
