# Phase 1 Execution Plan - Notebook Remediation

**Generated:** 2025-11-17T04:25:00
**Status:** In Progress
**Phase:** Phase 1 - Review and Fix All Cells (100% Success Rate)

## User-Confirmed Approaches

### 1. Excel Processing
- **Approach:** Convert to CSV files
- **Action:** Modify cells 80 and 85 to use CSV files from `sample-data/csv/` instead of Excel
- **Reason:** Excel files are encrypted/corrupted (BadZipFile error)

### 2. Load Balancing
- **Approach:** Round-robin across 3 regions
- **Action:** Configure backend pool for even distribution across UK South, East US, Norway East
- **Reason:** Currently all requests go to UK South only

### 3. Model Deployments
- **Models to deploy:**
  - gpt-4.1-nano (user specified, not gpt-4.1-mini)
  - dall-e-3 with SKU: 'GlobalStandard' (fix from 'Standard')
- **Action:** Update cell 29 deployment configuration

### 4. Semantic Kernel / AutoGen
- **Approach:** Research and update to latest API versions
- **Action:** Update import statements, method signatures, and settings format
- **Frameworks:** semantic_kernel, autogen

## Execution Order (By Severity)

### Stage 1: CRITICAL Errors (Must Pass Before Proceeding)

#### 1.1 Load Balancing (Cells 43-47)
**Testing Loop:** A→B→C→D→E→F→G→H→I→J(retry if fail)→K(full notebook)→L(success)

- **Cell 43:** Lab 03 load balancing configuration
  - Current: Policy applied
  - Issue: All requests to UK South only
  - Fix: Verify backend pool creation with correct regions

- **Cell 44:** Backend pool creation helper
  - Current: Creates pool but may not be configured correctly
  - Fix: Ensure 3 backends (UK South, East US, Norway East) with round-robin

- **Cell 45:** Backend verification
  - Current: Lists backends
  - Fix: Verify all 3 backends present and configured

- **Cell 47:** Load balancing test
  - Current: All requests showing UK South
  - Expected: ~33% distribution across 3 regions
  - Test: Run 15-20 requests, verify distribution

**Acceptance Criteria:**
- ✓ Backend pool exists with 3 backends
- ✓ Each backend configured for correct region
- ✓ Load balancing policy applied successfully
- ✓ Test shows distribution across all 3 regions (tolerance: ±20%)

#### 1.2 Excel Processing (Cells 80, 85)
**Testing Loop:** A→B→C→D→E→F→G→H→I→J→K→L

- **Cell 80:** Sales analysis
  - Current: `pd.read_excel` → BadZipFile error
  - Fix: Change to `pd.read_csv`, update file path to `sample-data/csv/sales_performance.csv`
  - Expected: Successfully read sales data, perform analysis, generate AI summary

- **Cell 85:** Cost analysis
  - Current: Excel processing
  - Fix: Verify CSV approach already implemented, ensure file exists
  - Expected: Successfully read cost data, generate AI insights

**Acceptance Criteria:**
- ✓ CSV files exist in sample-data/csv/
- ✓ pandas reads CSV without errors
- ✓ Data analysis completes
- ✓ AI summary generation works

### Stage 2: HIGH Severity Errors

#### 2.1 MCP TaskGroup (Cell 87)
**Testing Loop:** A→B→C→D→E→F→G→H→I→J→K→L

- **Current:** TaskGroup SubException with KeyError: 0
- **Root Cause:** MCP client/server communication issue
- **Fix:** Update MCP client code, add error handling, verify server connectivity
- **Expected:** Successful MCP tool calling with docs server

#### 2.2 Semantic Kernel Integration (Cells 95, 99, 106, 108)
**Testing Loop:** A→B→C→D→E→F→G→H→I→J→K→L (for each cell)

- **Cell 95:** SK Without MCP
  - Issue: `get_chat_message_contents() missing 1 required positional argument: 'settings'`
  - Fix: Research latest semantic_kernel API, update method call

- **Cell 99:** SK Hybrid Approach
  - Issue: `Kernel object has no attribute 'arguments'`
  - Fix: Update to current Kernel API, remove deprecated attributes

- **Cell 106:** SK Timeout Wrapper
  - Issue: `invoke_prompt() missing 1 required positional argument: 'prompt'`
  - Fix: Update invoke_prompt call signature

- **Cell 108:** SK Diagnostic
  - Issue: Client not defined, semantic cache not working
  - Fix: Initialize client, fix cache configuration

**Research Required:**
- Latest semantic_kernel version and breaking changes
- Correct AzureChatCompletion initialization
- Proper settings object format
- Current Kernel API methods

#### 2.3 AutoGen + APIM (Cell 101)
**Testing Loop:** A→B→C→D→E→F→G→H→I→J→K→L

- **Current:** AutoGen + APIM + MCP SSE transport not working
- **Issue:** TaskGroup errors, connection failures
- **Fix:** Update AutoGen configuration for SSE, verify APIM routing
- **Expected:** Successful multi-agent conversation via APIM gateway

### Stage 3: MEDIUM Severity Errors

#### 3.1 Model Deployment (Cell 29)
**Testing Loop:** A→B→C→D→E→F→G→H→I→J→K→L

**Changes:**
```python
models_config = {
    'foundry1': [
        {'name': 'gpt-4o-mini', 'format': 'OpenAI', 'version': '2024-07-18', 'sku': 'GlobalStandard', 'capacity': 100},
        {'name': 'gpt-4o', 'format': 'OpenAI', 'version': '2024-08-06', 'sku': 'GlobalStandard', 'capacity': 100},
        {'name': 'gpt-4.1-nano', 'format': 'OpenAI', 'version': 'latest', 'sku': 'GlobalStandard', 'capacity': 100},  # ADD
        {'name': 'text-embedding-3-small', 'format': 'OpenAI', 'version': '1', 'sku': 'GlobalStandard', 'capacity': 20},
        {'name': 'text-embedding-3-large', 'format': 'OpenAI', 'version': '1', 'sku': 'GlobalStandard', 'capacity': 20},
        {'name': 'dall-e-3', 'format': 'OpenAI', 'version': '3.0', 'sku': 'GlobalStandard', 'capacity': 1},  # FIX SKU
        {'name': 'gpt-4o-realtime-preview', 'format': 'OpenAI', 'version': '2024-10-01', 'sku': 'GlobalStandard', 'capacity': 100},  # Keep, expect to skip
    ],
    # ... other foundries
}
```

**Acceptance Criteria:**
- ✓ dall-e-3 deploys successfully with GlobalStandard SKU
- ✓ gpt-4.1-nano deploys successfully (or document if not available)
- ✓ gpt-4o-realtime-preview fails gracefully with clear skip message

### Stage 4: WARNING Severity

#### 4.1 Semantic Caching (Cell 16)
**Testing Loop:** A→B→C→D→E→F→G→H→I→J→K→L

- **Current:** Policy applied but caching not happening
- **Issue:** Cache hit rate not showing, timing not improving
- **Fix:** Verify Redis connection, check cache policy, test with identical requests
- **Expected:** Second identical request should be <100ms (cache hit)

#### 4.2 API_ID Autodiscovery (Cell 21)
**Testing Loop:** A→B→C→D→E→F→G→H→I→J→K→L

- **Current:** Warning about API_ID not properly configured
- **Fix:** Implement autodiscovery from deployment outputs
- **Expected:** No warnings, API_ID automatically resolved

### Stage 5: Outdated Code (Cells 117, 155+)

#### 5.1 Environment Variable Updates
**Testing Loop:** A→B→C→D→E→F→G→H→I→J→K→L (for each cell)

- **Cell 117:** Add APIM_GATEWAY_URL validation
- **Cell 155+:** Update all environment variable references
- **Fix:** Ensure consistent variable names, add fallbacks
- **Expected:** No missing variable errors

## Testing Protocol (A-L Loop)

For each cell fix:

**A. Analyze Current Code**
- Read cell source
- Identify exact error
- Understand dependencies

**B. Analyze Current Output**
- Review error messages
- Check stack traces
- Note failure points

**C. Create Resolution**
- Write fix based on research
- Document changes
- Prepare expected behavior

**D. Create Predicted Output**
- Write what success looks like
- Define acceptance criteria
- Set measurable goals

**E. Run the Cell**
- Execute modified cell
- Capture all output
- Log execution time

**F. Analyze Actual Output**
- Compare to predicted
- Check for errors
- Verify data correctness

**G. Compare Expected vs Actual**
- Line-by-line comparison
- Identify discrepancies
- Document deviations

**H. Analyze Discrepancies**
- Understand root causes
- Determine if acceptable
- Plan additional fixes

**I. Verify Match**
- Confirm expected = actual
- Check acceptance criteria
- Validate success metrics

**J. If No Match → Restart at A**
- Document failure reason
- Revise approach
- Iterate until success

**K. Run Full Notebook to Cell**
- Sequential execution from cell 1
- Verify no regressions
- Confirm cumulative success

**L. Success Confirmation**
- Document final state
- Log resolution time
- Move to next cell

## Execution Logs

All testing will be logged to:
- `project-execution-logs/phase1/cell-{number}-fix-log.md`
- `project-execution-logs/phase1/execution-timeline.jsonl`

Each log will contain:
- Timestamp
- Cell number
- Testing loop iteration
- Attempt number
- Success/Failure status
- Error messages
- Resolution approach
- Actual vs Expected output
- Notebook execution time (cells 1-N)

## Git Push Strategy

After completion of each stage:
- Stage 1 (Critical) → Git push with approval
- Stage 2 (High) → Git push with approval
- Stage 3 (Medium) → Git push with approval
- Stage 4 (Warning) → Git push with approval
- Stage 5 (Outdated) → Git push with approval

Each commit will include:
- Summary of fixes
- Cells modified
- Testing results
- Known issues (if any)

## Immutable Sections

**DO NOT MODIFY:**
- ACCESS CONTROL SECTION (Cells 57-60 range)
  - Cell 57: JWT Only Policy
  - Cell 58: API Key test
  - Cell 59: Dual Auth Policy
  - Cell 60: Reset to API-KEY

These cells demonstrate authentication policies and must remain unchanged.

## Success Criteria for Phase 1 Completion

- [ ] All CRITICAL errors fixed and verified
- [ ] All HIGH severity errors fixed and verified
- [ ] All MEDIUM severity errors fixed and verified
- [ ] All WARNING issues fixed and verified
- [ ] All outdated code updated
- [ ] Full notebook executes sequentially without errors (cells 1-173)
- [ ] All images migrated to images/ folder and referenced correctly
- [ ] Documentation updated
- [ ] Git commits created for each stage
- [ ] No regressions introduced

## Next Steps After Phase 1

Only after Phase 1 is 100% complete:
- Phase 2: Integrate other labs
- Phase 3: Add Semantic Kernel + AutoGen examples (enhanced)
- Phase 4: Pruning and optimization
- Phase 5: Helper functions and utilities
- Phase 6: Deployment infrastructure
- Phase 7: Final documentation

**Status:** Phase 1 in progress - Starting with Critical errors
**Last Updated:** 2025-11-17T04:25:00
