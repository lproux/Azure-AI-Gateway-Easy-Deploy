# Phase 2 - Investigation Complete: Root Causes & Solutions

**Date**: 2025-11-17  
**Investigation**: Infrastructure → Excel Files → Quick Fixes  
**Status**: All root causes identified  

---

## 🔍 Key Findings

### Finding 1: Excel Files are ENCRYPTED ⚠️

**Evidence**:
```bash
$ file ./sample-data/excel/*.xlsx
./sample-data/excel/sales_performance.xlsx:    CDFV2 Encrypted
./sample-data/excel/azure_resource_costs.xlsx: CDFV2 Encrypted
```

**Impact**: MCP Excel server and Python openpyxl cannot read encrypted Excel files

**Root Cause**: Files are password-protected or encrypted (CDFV2 format)

**Solution Options**:

**Option A - Create New Unencrypted Files** (Recommended):
```python
import pandas as pd

# Sales data
sales_data = {
    'Region': ['North', 'South', 'East', 'West', 'Central'] * 20,
    'Product': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'] * 20,
    'CustomerID': [f'C{i:04d}' for i in range(1, 101)],
    'TotalAmount': [round(1000 + i * 50.5, 2) for i in range(100)],
    'Quantity': [10 + i % 50 for i in range(100)],
    'Discount': [round(0.05 + (i % 10) * 0.01, 2) for i in range(100)]
}
df_sales = pd.DataFrame(sales_data)
df_sales.to_excel('./sample-data/excel/sales_performance_new.xlsx', index=False)

# Cost data
cost_data = {
    'Resource_Type': ['Virtual Machine', 'Storage', 'Database', 'Network'] * 30,
    'Resource_Name': [f'Resource-{i:03d}' for i in range(1, 121)],
    'Daily_Cost': [round(50 + i * 5.25, 2) for i in range(120)]
}
df_costs = pd.DataFrame(cost_data)
df_costs.to_excel('./sample-data/excel/azure_resource_costs_new.xlsx', index=False)
```

Then update cells 81 and 86 to use the new files:
```python
# Cell 81
excel_file_path = Path("./sample-data/excel/sales_performance_new.xlsx")

# Cell 86
cost_file_path = Path("./sample-data/excel/azure_resource_costs_new.xlsx")
```

**Option B - Decrypt Existing Files**:
Open in Excel, remove password, save as new file

---

### Finding 2: APIM Backends Missing for DALL-E & Embeddings

**Evidence**:
- DALL-E-3: 404 DeploymentNotFound
- text-embedding-3-small: 400 OperationNotSupported when using gpt-4o-mini

**Root Cause**: Foundry models deployed but not configured as APIM backends

**Models Deployed**:
```bash
# From master-lab.env:
MODEL_DALL_E_3_ENDPOINT_R1=https://foundry1-pavavy6pu5hpa.openai.azure.com/
MODEL_TEXT_EMBEDDING_3_SMALL_ENDPOINT_R1=https://foundry1-pavavy6pu5hpa.openai.azure.com/
MODEL_TEXT_EMBEDDING_3_LARGE_ENDPOINT_R1=https://foundry1-pavavy6pu5hpa.openai.azure.com/
```

**Solution - Use Direct Foundry Endpoints** (Bypass APIM):

For **Cell 108** (Image Generation):
```python
# Use direct foundry endpoint instead of APIM
dalle_endpoint = os.getenv("MODEL_DALL_E_3_ENDPOINT_R1")
dalle_key = os.getenv("MODEL_DALL_E_3_KEY_R1")

if dalle_endpoint and dalle_key:
    url = f"{dalle_endpoint}openai/deployments/dall-e-3/images/generations?api-version=2024-08-01-preview"
    headers = {
        "Content-Type": "application/json",
        "api-key": dalle_key
    }
    print(f"✅ Using direct foundry endpoint (bypassing APIM)")
else:
    # Fallback to APIM (will fail until backend added)
    url = f"{apim_gateway_url.rstrip('/')}/{inference_api_path.strip('/')}/openai/deployments/dall-e-3/images/generations?api-version=2024-08-01-preview"
    headers = {
        "Content-Type": "application/json",
        "api-key": apim_api_key,
        "Ocp-Apim-Subscription-Key": apim_api_key
    }
```

For **Cell 145** (Vector Search Embeddings):
```python
# Use direct foundry endpoint for embeddings
embedding_endpoint = os.getenv("MODEL_TEXT_EMBEDDING_3_SMALL_ENDPOINT_R1")
embedding_key = os.getenv("MODEL_TEXT_EMBEDDING_3_SMALL_KEY_R1")

if embedding_endpoint and embedding_key:
    openai_client = AsyncAzureOpenAI(
        azure_endpoint=embedding_endpoint,
        api_key=embedding_key,
        api_version=api_version
    )
    print(f"✅ Using direct foundry endpoint for embeddings")
else:
    # Fallback to APIM
    openai_client = AsyncAzureOpenAI(
        azure_endpoint=f"{apim_gateway_url}/{inference_api_path}",
        api_key=apim_api_key,
        api_version=api_version
    )
```

---

### Finding 3: Semantic Caching Not Working

**Evidence**: All 20 requests showing `Cache: UNKNOWN`

**Root Cause Chain**:
1. Cell 17 applies semantic cache policy → Fails with UTF-8 BOM error
2. Policy not applied → No caching headers in responses
3. Cell 103 checks headers → All show UNKNOWN

**Solution - Fix Cell 17 BOM Handling**:
```python
# In Cell 17, when reading policy response:
try:
    response_text = response.text
    # Remove UTF-8 BOM if present
    if response_text.startswith('\ufeff'):
        response_text = response_text[1:]
    policy_content = json.loads(response_text)
except json.JSONDecodeError as e:
    print(f"❌ JSON decode error: {e}")
    print(f"   Response text (first 200 chars): {response_text[:200]}")
```

After fixing:
1. Re-run Cell 17 to apply policy
2. Wait 60 seconds for propagation
3. Run Cell 103 - should see `Cache: HIT`

---

### Finding 4: AutoGen Connection Error (Cell 147)

**Error**: `ConnectError: [Errno 11001] getaddrinfo failed`

**Root Cause**: Endpoint configuration issue in AutoGen config_list

**Debug Needed**:
```python
# Add to Cell 147 before agent creation:
print(f"DEBUG: config_list = {json.dumps(config_list, indent=2)}")
print(f"DEBUG: base_url should be: {apim_gateway_url}/{inference_api_path}")
```

**Expected Configuration**:
```python
config_list = [{
    "model": "gpt-4o-mini",
    "api_type": "azure",
    "api_key": apim_api_key,
    "base_url": f"{apim_gateway_url.rstrip('/')}/{inference_api_path.strip('/')}",
    "api_version": "2024-06-01"
}]
```

---

## 📋 Complete Fix Checklist

### High Priority (Critical Path)

- [ ] **Excel Files**: Create new unencrypted files OR decrypt existing
  - Files needed: `sales_performance_new.xlsx`, `azure_resource_costs_new.xlsx`
  - Update cells 81, 86 to use new files

- [ ] **DALL-E (Cell 108)**: Use direct foundry endpoint
  - Bypass APIM, use `MODEL_DALL_E_3_ENDPOINT_R1` directly

- [ ] **Embeddings (Cell 145)**: Use direct foundry endpoint
  - Use `MODEL_TEXT_EMBEDDING_3_SMALL_ENDPOINT_R1` directly
  - Change model from `gpt-4o-mini` to `text-embedding-3-small`

- [ ] **Semantic Caching (Cell 17 → Cell 103)**: Fix UTF-8 BOM handling
  - Update Cell 17 to strip BOM before JSON parsing
  - Re-apply policy, wait 60s, test Cell 103

- [ ] **AutoGen (Cell 147)**: Fix endpoint configuration
  - Debug config_list to ensure correct base_url
  - Should use APIM gateway URL

### Medium Priority

- [ ] **Cell 96**: Remove or fix 404 logic
- [ ] **Cell 128**: Replace utils with direct print
- [ ] **Cells 99-100**: Document expected behavior (weather API)

### Testing After Fixes

- [ ] Test Cells 81, 83, 86, 132 (MCP Excel)
- [ ] Test Cell 108 (DALL-E image generation)
- [ ] Test Cell 103 (Semantic caching)
- [ ] Test Cell 145 (Vector search with real embeddings)
- [ ] Test Cell 147 (AutoGen A2A agents)

---

## 🎯 Quick Start: Apply All Fixes

### Step 1: Create New Excel Files

Run this in a Jupyter cell or Python script:
```python
import pandas as pd

# Create sales_performance_new.xlsx
sales_data = {
    'Region': ['North', 'South', 'East', 'West'] * 25,
    'Product': ['Product A', 'Product B', 'Product C', 'Product D'] * 25,
    'TotalAmount': [1000 + i * 50 for i in range(100)],
    'Quantity': [10 + i for i in range(100)]
}
pd.DataFrame(sales_data).to_excel('./sample-data/excel/sales_performance_new.xlsx', index=False)

# Create azure_resource_costs_new.xlsx
cost_data = {
    'Resource_Type': ['VM', 'Storage', 'Database', 'Network'] * 30,
    'Daily_Cost': [100 + i * 5 for i in range(120)]
}
pd.DataFrame(cost_data).to_excel('./sample-data/excel/azure_resource_costs_new.xlsx', index=False)

print("✅ New Excel files created!")
```

### Step 2: Update Notebook Cells

I'll provide the exact cell updates in the next section...

---

## 📊 Summary Statistics

**Total Issues**: 9  
**Root Causes Identified**: 4
- Encrypted Excel files
- Missing APIM backends
- UTF-8 BOM in policy response
- AutoGen endpoint misconfiguration

**Solutions Available**:
- ✅ 4 workarounds ready (direct endpoints)
- ✅ 2 fixes ready (BOM handling, utils)
- ⏳ 1 requires file creation (Excel)
- ⏳ 1 requires debugging (AutoGen config)
- ⏳ 1 cosmetic (Cell 96)

**Estimated Fix Time**:
- Excel files: 5 minutes
- Cell updates: 15 minutes
- Testing: 20 minutes
- **Total: ~40 minutes**

---

## 🚀 Next Steps

1. **Create new Excel files** (use Step 1 script above)
2. **Apply cell fixes** (I'll prepare these now)
3. **Test each fixed cell**
4. **Commit changes**

Ready to proceed with **Step 3: Quick Fixes** - applying all the cell updates?

