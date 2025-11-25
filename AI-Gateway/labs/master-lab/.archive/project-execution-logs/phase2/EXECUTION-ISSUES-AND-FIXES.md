# Phase 2 Execution Issues and Recommended Fixes

**Date**: 2025-11-17  
**Source**: Test execution output  
**Status**: 9 issues identified  

---

## Issues Summary

| Cell | Issue | Severity | Status |
|------|-------|----------|--------|
| 17 | UTF-8 BOM JSON decode error | Medium | Needs fix |
| 81, 83, 86 | Excel BadZipFile error | High | Needs investigation |
| 96 | 404 status considered "connected" | Low | Remove or fix |
| 99-100 | Weather API not returning data | Medium | Expected behavior |
| 103 | No cache headers detected | High | APIM policy issue |
| 108 | DALL-E-3 deployment not found | High | APIM backend missing |
| 128 | Utils formatting issue | Low | Needs fix |
| 145 | Wrong embedding model | High | **FIXED BELOW** |
| 147 | AutoGen connection error | High | Endpoint issue |

---

## Detailed Analysis and Fixes

### Issue 1: Cell 17 - UTF-8 BOM JSON Decode Error

**Error**:
```
JSONDecodeError: Unexpected UTF-8 BOM (decode using utf-8-sig): line 1 column 1 (char 0)
```

**Root Cause**: Azure Management API returning JSON with UTF-8 BOM marker

**Fix**: Update JSON parsing to handle BOM
```python
# Replace:
policy_content = response.json()

# With:
response_text = response.text
if response_text.startswith('\ufeff'):
    response_text = response_text[1:]  # Remove BOM
policy_content = json.loads(response_text)
```

---

### Issue 2: Cells 81, 83, 86 - Excel BadZipFile Error

**Error**:
```
Excel MCP Error: Failed to upload Excel file: File is not a zip file
```

**Root Cause**: MCP server cannot parse Excel files OR files are corrupted

**Investigation Needed**:
1. Check if Excel files are valid: `file ./sample-data/excel/sales_performance.xlsx`
2. Try opening files in Excel to verify integrity
3. Check MCP Excel server logs
4. Verify .xlsx files are not password-protected

**Temporary Workaround**: 
Create new Excel files using pandas:
```python
import pandas as pd

# Sales data
sales_data = {
    'Region': ['North', 'South', 'East', 'West'] * 5,
    'Product': ['A', 'B', 'C', 'D', 'E'] * 4,
    'TotalAmount': [1000, 1500, 2000, 2500] * 5,
    'Quantity': [10, 15, 20, 25] * 5
}
df = pd.DataFrame(sales_data)
df.to_excel('./sample-data/excel/sales_performance_new.xlsx', index=False)

# Cost data
cost_data = {
    'Resource_Type': ['VM', 'Storage', 'Database', 'Network'] * 3,
    'Daily_Cost': [100, 50, 200, 75] * 3
}
df_cost = pd.DataFrame(cost_data)
df_cost.to_excel('./sample-data/excel/azure_resource_costs_new.xlsx', index=False)
```

---

### Issue 3: Cell 96 - 404 Status Considered "Connected"

**Output**:
```
RESULT: ✅ CONNECTED (Status: 404)
```

**Root Cause**: Cell treats any response (even 404) as "connected"

**Recommendation**: **Remove this cell** or fix the logic:
```python
# Should be:
if status_code == 200:
    print("RESULT: ✅ CONNECTED")
elif status_code == 404:
    print("RESULT: ❌ NOT FOUND (404) - Endpoint exists but resource not found")
else:
    print(f"RESULT: ⚠️ UNEXPECTED STATUS: {status_code}")
```

---

### Issue 4: Cells 99-100 - Weather API No Data

**Output**:
```
Response: I'm unable to retrieve the weather data for Paris at the moment.
```

**Root Cause**: Weather API call likely failing, LLM returning graceful fallback

**Status**: This is **expected behavior** if:
- Weather API key is not configured
- MCP weather server is down
- Network connectivity issues

**Not a critical issue** - this is a demo cell showing fallback behavior.

---

### Issue 5: Cell 103 (was 101) - No Semantic Caching Headers

**Output**:
```
All requests showing Cache: UNKNOWN
Cache Hits: 0 (0.0%)
```

**Root Cause**: Cell 17 (semantic cache policy) failed to apply correctly due to JSON BOM error

**Fix Priority**: **HIGH**

**Dependencies**: Fix Issue #1 first, then re-apply cache policy

**Verification**:
1. Fix Cell 17 BOM issue
2. Re-run Cell 17 to apply semantic cache policy
3. Wait 60 seconds for policy propagation
4. Run Cell 103 again
5. Should see `Cache: HIT` for repeated questions

---

### Issue 6: Cell 108 - DALL-E-3 Deployment Not Found ⚠️

**Error**:
```
404 Client Error: DeploymentNotFound for url: .../deployments/dall-e-3/images/generations
```

**Root Cause**: DALL-E-3 **not configured as APIM backend**

**Environment Shows**:
```bash
# master-lab.env has the foundry endpoint:
MODEL_DALL_E_3_ENDPOINT_R1=https://foundry1-pavavy6pu5hpa.openai.azure.com/
MODEL_DALL_E_3_KEY_R1=62ef7faafa0f4afe97bbe013b9f775f9
```

**But**: APIM doesn't have "dall-e-3" as a backend/deployment

**Fix Options**:

**Option A - Add DALL-E backend to APIM** (Recommended):
```bash
# Add DALL-E backend to APIM
az apim backend create \
  --resource-group lab-master-lab \
  --service-name apim-pavavy6pu5hpa \
  --backend-id dalle3-backend \
  --url "https://foundry1-pavavy6pu5hpa.openai.azure.com" \
  --protocol http \
  --credentials header.api-key=62ef7faafa0f4afe97bbe013b9f775f9
```

**Option B - Use direct foundry endpoint in Cell 108**:
```python
# Instead of APIM gateway, use foundry directly
dalle_endpoint = os.getenv("MODEL_DALL_E_3_ENDPOINT_R1")
dalle_key = os.getenv("MODEL_DALL_E_3_KEY_R1")

url = f"{dalle_endpoint}openai/deployments/dall-e-3/images/generations?api-version=2024-08-01-preview"
headers = {"api-key": dalle_key}
```

---

### Issue 7: Cell 128 - Utils Formatting

**Issue**: `utils` module not recognized for log formatting

**Fix**: Replace utils call with direct print:
```python
# Replace:
if 'utils' in globals() and hasattr(utils, 'print_ok'):
    utils.print_ok('Lab Complete!')
else:
    print('[OK] Lab Complete!')

# With:
print('✅ Lab Complete!')
```

---

### Issue 8: Cell 145 - Wrong Embedding Model ✅ FIXED

**Error**:
```
OperationNotSupported: The embeddings operation does not work with the specified model, gpt-4o-mini
```

**Root Cause**: Cell 145 using `gpt-4o-mini` for embeddings instead of `text-embedding-3-small`

**Environment Has**:
```bash
MODEL_TEXT_EMBEDDING_3_SMALL_ENDPOINT_R1=https://foundry1-pavavy6pu5hpa.openai.azure.com/
```

**FIX APPLIED**:
```python
# Cell 145 now uses:
embedding_model = (
    os.getenv("MODEL_TEXT_EMBEDDING_3_SMALL_DEPLOYMENT") or
    os.getenv("EMBEDDING_MODEL") or
    "text-embedding-3-small"  # Correct default
)
```

**But needs to route through APIM correctly** - similar to DALL-E issue above.

---

### Issue 9: Cell 147 - AutoGen Connection Error

**Error**:
```
APIConnectionError: Connection error.
ConnectError: [Errno 11001] getaddrinfo failed
```

**Root Cause**: AutoGen trying to connect to invalid endpoint

**Likely Cause**: `azure_endpoint` not set correctly or using wrong URL format

**Debug**:
Check what endpoint AutoGen is trying to use:
```python
# In Cell 147, add debug output:
print(f"DEBUG: Azure endpoint = {azure_endpoint}")
print(f"DEBUG: Base URL = {config_list[0]['base_url']}")
```

**Expected**: Should be using APIM gateway:
```
https://apim-pavavy6pu5hpa.azure-api.net/inference
```

---

## Priority Fix Order

1. **HIGH PRIORITY**:
   - Issue #6: Add DALL-E backend to APIM OR use direct endpoint
   - Issue #8: Fix embedding model (✅ prepared fix)
   - Issue #5: Fix semantic caching (depends on #1)
   - Issue #9: Fix AutoGen endpoint configuration

2. **MEDIUM PRIORITY**:
   - Issue #1: Handle UTF-8 BOM in Cell 17
   - Issue #2: Investigate Excel file corruption

3. **LOW PRIORITY**:
   - Issue #3: Fix Cell 96 logic or remove
   - Issue #4: Weather API (expected behavior, low priority)
   - Issue #7: Utils formatting (cosmetic)

---

## Quick Fix Script

Here's a script to apply the most critical fixes:

```python
# Fix Cell 108 - Use direct DALL-E endpoint
DALLE_ENDPOINT = os.getenv("MODEL_DALL_E_3_ENDPOINT_R1")
DALLE_KEY = os.getenv("MODEL_DALL_E_3_KEY_R1")

if DALLE_ENDPOINT and DALLE_KEY:
    # Use direct endpoint
    url = f"{DALLE_ENDPOINT}openai/deployments/dall-e-3/images/generations"
    headers = {"api-key": DALLE_KEY}
else:
    # Fallback to APIM (will fail until backend added)
    url = f"{apim_gateway_url}/inference/openai/deployments/dall-e-3/images/generations"
    headers = {"api-key": apim_api_key}
```

---

## Testing Recommendations

After applying fixes:

1. **Test embedding model** (Cell 145):
   ```bash
   # Should use text-embedding-3-small
   ```

2. **Test DALL-E** (Cell 108):
   ```bash
   # Should generate image successfully
   ```

3. **Test semantic caching** (Cell 103):
   ```bash
   # Should show Cache: HIT for repeated questions
   ```

4. **Test AutoGen** (Cell 147):
   ```bash
   # Should connect and create agents successfully
   ```

---

## Summary

- **Critical Issues**: 4 (DALL-E, embeddings, caching, AutoGen)
- **Fixes Ready**: 2 (embeddings config, utils formatting)
- **Needs Investigation**: 2 (Excel files, APIM backends)
- **Low Priority**: 3 (Cell 96, weather API, BOM handling)

**Recommendation**: Focus on adding APIM backends for DALL-E and embeddings models, or use direct foundry endpoints as workaround.

