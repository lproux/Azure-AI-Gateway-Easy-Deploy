# Cell Number Mapping and Error Cross-Reference

**Generated:** 2025-11-17T04:19:00
**Purpose:** Map user-reported cell numbers to actual cell indices in the notebook

## Summary

- **Total Cells:** 173 (84 code, 89 markdown)
- **User-Reported Errors:** 19 cells
- **Issue:** Some user-reported numbers point to markdown cells, actual errors are in nearby code cells

## Cell-by-Cell Mapping

### CRITICAL Severity

| User Reported | Actual Cell | Cell Type | Issue | Actual Location |
|--------------|-------------|-----------|-------|-----------------|
| 45 | 45 | CODE | Load balancing not working | Cell 45: Backend verification |
| 47 | 47 | CODE | Load balancing test showing all UK South | Cell 47: Load balancing test |
| 63 | 63 | CODE | Model routing - appears to be content safety, not model routing | Cell 63: Content safety test |
| 78 | 78 | MARKDOWN | Excel error - actual code is in cell 80 | Cell 80: Sales analysis |
| 80 | 80 | CODE | Excel BadZipFile error ✓ | Cell 80: Excel sales analysis |
| 83 | 83 | MARKDOWN | Excel error description | Cell 85: Cost analysis |

### HIGH Severity

| User Reported | Actual Cell | Cell Type | Issue | Actual Location |
|--------------|-------------|-----------|-------|-----------------|
| 85 | 85 | CODE | TaskGroup SubException - but code shows cost analysis | Need to find MCP TaskGroup error |
| 93 | 93 | MARKDOWN | Semantic Kernel section header | Cells 95-99, 106, 108: SK errors |
| 95 | 95 | CODE | MCP connection 404 - code shows SK without MCP | Cell 97: Manual MCP connection |
| 97 | 97 | CODE | Kernel attribute error ✓ | Cell 97: MCP connection test |
| 99 | 99 | CODE | AutoGen + APIM - code shows SK hybrid | Cell 101: AutoGen production |
| 104 | 104 | MARKDOWN | Dict formatting - GitHub MCP description | Cells 106, 108: SK diagnostics |
| 108 | 108 | CODE | Semantic cache + client not defined ✓ | Cell 108: SK diagnostic |

### MEDIUM Severity

| User Reported | Actual Cell | Cell Type | Issue | Actual Location |
|--------------|-------------|-----------|-------|-----------------|
| 29 | 29 | CODE | Model deployment - dall-e-3 SKU ✓ | Cell 29: BICEP step 2 |
| 95 | 95 | CODE | MCP connection 404 ✓ | Cell 97: Manual MCP test |
| 106 | 106 | CODE | Diagnostic issues ✓ | Cell 106: Timeout wrapper |

### WARNING Severity

| User Reported | Actual Cell | Cell Type | Issue | Actual Location |
|--------------|-------------|-----------|-------|-----------------|
| 17 | 17 | MARKDOWN | Semantic caching - actual code in cell 16 | Cell 16: Lab 01 semantic caching |
| 22 | 22 | MARKDOWN | API_ID autodiscovery | Cell 21: Policy apply helper |
| 43 | 43 | CODE | Load balancing policy applied ✓ | Cell 43: Lab 03 load balancing |

### Outdated Code

| User Reported | Actual Cell | Cell Type | Issue | Actual Location |
|--------------|-------------|-----------|-------|-----------------|
| 155+ | 155 | CODE | Missing APIM_GATEWAY_URL ✓ | Cell 155: Dynamic column analysis |
| 155+ | 117 | CODE | Missing environment variables | Cell 117: Variable validation |

## Confirmed Code Cells to Fix

Based on actual cell analysis:

### CRITICAL
1. **Cell 45** - Load balancing: Backend verification helper
2. **Cell 47** - Load balancing: All requests going to UK South only
3. **Cell 80** - Excel: BadZipFile error in sales analysis
4. **Cell 85** - Excel: Cost analysis (CSV fallback needed)

### HIGH
1. **Cell 87** - MCP TaskGroup: Function calling with MCP tools
2. **Cell 95** - Semantic Kernel: Missing positional argument
3. **Cell 97** - MCP connection: Manual connection test showing 404
4. **Cell 99** - Semantic Kernel: Hybrid approach with kernel.arguments error
5. **Cell 101** - AutoGen: Production AutoGen + APIM + MCP
6. **Cell 106** - Semantic Kernel: Timeout wrapper testing
7. **Cell 108** - Semantic Kernel: Diagnostic report with client not defined

### MEDIUM
1. **Cell 29** - Model deployment: gpt-4.1-mini and dall-e-3 SKU issues
2. **Cell 106** - Diagnostic configuration issues

### WARNING
1. **Cell 16** - Semantic caching: Lab 01 not working
2. **Cell 21** - API_ID: Autodiscovery warnings
3. **Cell 43** - Load balancing: Policy applied but not working

### OUTDATED CODE (Cell 155+)
1. **Cell 117** - Missing APIM_GATEWAY_URL validation
2. **Cell 155** - Dynamic analysis missing environment variables
3. **Multiple cells** - Various cells with outdated patterns

## Additional Findings

### Cells with Load Balancing References
Cells 13, 16, 31, 37, 43, 44, 45, 47, 49, 57, 58, 59, 60 all contain load balancing references.

**Root Cause:** Load balancing policy is being applied, but backend pool configuration may not be correct.

### Cells with Excel Processing
Cells 80, 85 contain Excel processing code with BadZipFile errors.

**Root Cause:** Excel files may be encrypted or corrupted. Need to use CSV fallback.

### Cells with Semantic Kernel
Cells 92, 95, 96, 99, 106, 108, 162, 164, 168, 170, 172 contain Semantic Kernel code.

**Root Cause:** API incompatibility with SK version, incorrect settings format.

### Cells with AutoGen
Cells 13, 101, 166, 170, 172 contain AutoGen code.

**Root Cause:** SSE transport configuration with APIM.

## Recommended Action Plan

1. **Start with Cell Mapping Confirmation**
   - Review this mapping with user
   - Confirm which cells to prioritize

2. **Fix CRITICAL Errors First**
   - Cell 47: Load balancing backend pool
   - Cell 80, 85: Excel file handling

3. **Fix HIGH Errors**
   - Cell 87: MCP TaskGroup
   - Cells 95, 99, 106, 108: Semantic Kernel
   - Cell 101: AutoGen

4. **Fix MEDIUM/WARNING**
   - Cell 29: Model deployments
   - Cell 16: Semantic caching
   - Cell 21, 43: Policy application

5. **Update Outdated Code**
   - Cell 117, 155+: Environment variables

## Notes

- ACCESS CONTROL SECTION (cells 57-60) is IMMUTABLE - DO NOT MODIFY
- All testing must be sequential from cell 1 to target cell
- No shortcuts or mock testing allowed
- Full notebook execution required after each fix
