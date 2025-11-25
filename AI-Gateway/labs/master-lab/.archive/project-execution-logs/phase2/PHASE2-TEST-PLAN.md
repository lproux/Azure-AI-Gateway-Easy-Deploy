# PHASE 2: Full Notebook Testing Plan

**Date**: 2025-11-17
**Status**: 🧪 TESTING IN PROGRESS

---

## Test Scope

### Fixes to Validate (3 Critical Fixes)

1. **Cell 29 - dall-e-3 SKU Fix**
   - **Expected**: Deployment succeeds with SKU 'Standard'
   - **Look for**: `[OK] dall-e-3 deployed` or similar success message
   - **Failure indicator**: `InvalidResourceProperties` error mentioning SKU

2. **Cell 81 - Sales Analysis Column Fix**
   - **Expected**: Sales analysis completes without errors
   - **Look for**: `✅ Using columns: group_by='Region', metric='TotalAmount'`
   - **Failure indicator**: `agg function failed` or `TypeError: Could not convert string`

3. **Cell 152 - AutoGen Coordinator Fix**
   - **Expected**: AutoGen agents communicate successfully
   - **Look for**: Agent responses without `NotFoundError`
   - **Failure indicator**: `NotFoundError` or `404` when initiating chat

---

## Test Execution

### Method
- **Command**: `jupyter nbconvert --execute --allow-errors`
- **Timeout**: 600 seconds per cell, 1200 seconds total
- **Output**: `executed-phase2-test.ipynb`
- **Log**: `/tmp/phase2-test-output.log`

### Test Configuration
- **Allow Errors**: Yes (continue on failure to see all results)
- **Sequential Execution**: Cells 1-152
- **Kernel**: python3

---

## Success Criteria

### Overall Success
- ✅ All 3 fixed cells execute without their original errors
- ✅ No new regressions in previously working cells
- ✅ Notebook completes execution (with acceptable external failures)

### Acceptable Failures
- ⚠️ MCP server unavailability (external dependency)
- ⚠️ Network timeouts to Azure services
- ⚠️ Missing optional features (image generation if not configured)

### Unacceptable Failures
- ❌ Python syntax errors in modified cells
- ❌ Original errors still present (SKU error, column error, NotFoundError)
- ❌ New errors introduced by fixes

---

## Validation Checklist

### Cell 29 Validation
- [ ] Cell executes without SKU error
- [ ] dall-e-3 shows successful deployment or skip (not error)
- [ ] No `GlobalStandard` error message

### Cell 81 Validation
- [ ] Cell executes without aggregation error
- [ ] Finds TotalAmount column successfully
- [ ] Sales analysis produces output or graceful failure

### Cell 152 Validation
- [ ] Cell executes without NotFoundError
- [ ] AutoGen configuration loads
- [ ] Agent initialization succeeds (communication may timeout but shouldn't 404)

---

## Test Timeline

**Start**: 2025-11-17 (timestamp in log)
**Expected Duration**: 10-20 minutes
**Monitoring**: Check `/tmp/phase2-test-output.log` for progress

---

## Post-Test Actions

### If Tests Pass (Expected)
1. ✅ Review test output for all 3 fixes
2. ✅ Document results in `PHASE2-TEST-RESULTS.md`
3. ✅ Create git commit with all fixes
4. ✅ Push to repository
5. ✅ Continue with remaining 11 errors

### If Tests Fail (Unexpected)
1. 🔍 Identify which fix(es) failed
2. 🔍 Review error messages
3. 🔧 Apply additional fixes as needed
4. 🔄 Re-test
5. ✅ Commit once passing

---

## Known Issues Being Tested

### Primary Fixes
1. **Cell 29**: dall-e-3 'GlobalStandard' → 'Standard' SKU
2. **Cell 81**: 'TotalSales' → 'TotalAmount' column search
3. **Cell 152**: AutoGen base_url missing `/inference/openai` path

### Not Yet Fixed (Expected Failures)
- Cell 17: UTF-8 BOM error in policy verification
- Cell 103: Semantic cache not working (heuristic timing issue)
- Cell 150: Vector search missing embeddings
- Cells 108/110/134/135: Image generation issues
- Cell 127: Cosmos DB RBAC permissions
- Cell 119: Simulated A2A communication
- Cells 83/137: MCP consolidation pending
- Cell 98: MCP connection enhancement pending
- Cell 133: Log Analytics utils error

---

## Test Output Location

- **Executed Notebook**: `executed-phase2-test.ipynb`
- **Test Log**: `/tmp/phase2-test-output.log`
- **Results Document**: `PHASE2-TEST-RESULTS.md` (to be created)

---

**Status**: 🧪 TEST RUNNING - Check back in 10-15 minutes for results
