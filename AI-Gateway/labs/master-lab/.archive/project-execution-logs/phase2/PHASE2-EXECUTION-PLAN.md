# PHASE 2: EXECUTION PLAN - Revised Errors
## AI Gateway Master Lab - Additional Remediation

**Created**: 2025-11-17
**Status**: 🔄 PLANNING

---

## Error Categorization

### 🔴 CRITICAL Severity (Blocking Core Functionality)

1. **Cell 29**: dall-e-3 SKU Error - Invalid 'GlobalStandard' SKU
   - **Error**: `(InvalidResourceProperties) The specified SKU 'GlobalStandard' of account deploy`
   - **Impact**: Image generation model deployment fails
   - **Priority**: HIGH - Blocks all image generation features
   - **Note**: This was supposedly fixed in Phase 1 - need to investigate why still failing

2. **Cell 81**: Sales Analysis Column Error
   - **Error**: `agg function failed [how->mean,dtype->object]` + Cannot find 'TotalSales' column
   - **Root Cause**: Code looks for 'TotalSales' but CSV has 'TotalAmount'
   - **Impact**: Data analysis cells fail
   - **Priority**: HIGH - Blocks data analysis demos

3. **Cell 103**: Semantic Cache Not Working
   - **Error**: All requests show `cached: False`
   - **Impact**: Semantic caching feature completely non-functional
   - **Priority**: HIGH - Core feature not working

4. **Cell 150**: Vector Search No Embeddings
   - **Error**: `RuntimeError: No embedding deployment resolved (404)`
   - **Impact**: Vector search/RAG pattern fails
   - **Priority**: HIGH - Advanced AI feature blocked

### 🟠 HIGH Severity (Major Features Degraded)

5. **Cell 17**: UTF-8 BOM Error in Policy Verification
   - **Error**: `JSONDecodeError: Unexpected UTF-8 BOM (decode using utf-8-sig)`
   - **Impact**: Policy verification fails after successful application
   - **Priority**: MEDIUM-HIGH - Policy applies but verification broken

6. **Cell 108/110**: Image Generation Missing Deployment + Auth
   - **Error**: Cell 108: No image deployment found (404)
   - **Error**: Cell 110: 401 missing subscription key
   - **Impact**: Image generation completely broken
   - **Priority**: HIGH - Should merge into single cell with proper setup

7. **Cell 127**: Cosmos DB RBAC Permissions
   - **Error**: `(Forbidden) Request blocked - principal does not have required RBAC permissions`
   - **Impact**: Conversation persistence fails
   - **Priority**: MEDIUM-HIGH - Feature exists but unusable

8. **Cell 119**: Simulated Agent-to-Agent Communication
   - **Error**: Using synthetic/simulated A2A instead of real agents
   - **Impact**: Demo shows fake output, not real functionality
   - **Priority**: MEDIUM - Feature demo not authentic

### 🟡 MEDIUM Severity (Code Quality / Optimization)

9. **Cell 83**: Should Use MCP Instead of Pandas
   - **Issue**: Using pandas fallback instead of MCP calls
   - **Impact**: Not demonstrating MCP capabilities
   - **Priority**: MEDIUM - Should merge with Cell 81

10. **Cell 98**: MCP Connection Returns 404
   - **Issue**: MCP docs server returns 404, needs content/request
   - **Impact**: Connection test incomplete
   - **Priority**: MEDIUM - Works but incomplete demo

11. **Cell 133**: Log Analytics Query Error
   - **Error**: `name 'utils' is not defined`
   - **Impact**: Logging/monitoring demo fails
   - **Priority**: MEDIUM - Monitoring feature broken

12. **Cell 134/135**: Image Generation Consolidation
   - **Issue**: Multiple fragmented image cells, 404 errors
   - **Impact**: Poor code organization, failures
   - **Priority**: MEDIUM - Should consolidate into single cell

13. **Cell 137**: Excel MCP Duplicate
   - **Issue**: Should merge with other Excel MCP calls
   - **Impact**: Code duplication
   - **Priority**: LOW - Consolidation for clarity

---

## Execution Stages

### STAGE 1: CRITICAL Infrastructure Fixes

#### Stage 1.1: Cell 29 - dall-e-3 SKU Investigation
- **Actions**:
  1. Review Phase 1 fix (was supposedly fixed)
  2. Check actual model deployment configuration
  3. Research correct SKU for dall-e-3
  4. Update deployment if Phase 1 fix was incomplete
- **Expected Outcome**: dall-e-3 deploys successfully
- **Backup**: Create before any changes

#### Stage 1.2: Cell 81 - Sales Analysis Column Fix
- **Actions**:
  1. Change 'TotalSales' references to 'TotalAmount'
  2. Fix groupby aggregation to use correct column
  3. Update error handling for missing columns
- **Expected Outcome**: Sales analysis runs without errors
- **Backup**: Create before changes

#### Stage 1.3: Cell 103 - Semantic Cache Debugging
- **Actions**:
  1. Review semantic cache policy from Cell 17
  2. Check APIM response headers for cache indicators
  3. Verify embeddings backend is configured
  4. Test cache hit/miss logic
- **Expected Outcome**: Cache hits show `cached: True`
- **Related**: May be connected to Cell 17 UTF-8 BOM error
- **Backup**: Create before changes

#### Stage 1.4: Cell 150 - Vector Search Embeddings
- **Actions**:
  1. Verify embedding deployment exists (text-embedding-3-small/large)
  2. Fix 404 error when discovering embeddings
  3. Configure Azure Search integration
  4. Remove simulated fallback
- **Expected Outcome**: Real embeddings generated, vector search works
- **Backup**: Create before changes

---

### STAGE 2: HIGH Severity Feature Fixes

#### Stage 2.1: Cell 17 - UTF-8 BOM Fix
- **Actions**:
  1. Add `encoding='utf-8-sig'` to JSON parsing
  2. Or strip BOM manually before JSON decode
  3. Improve error handling for policy verification
- **Expected Outcome**: Policy verification completes successfully
- **Backup**: Create before changes

#### Stage 2.2: Cells 108/110/134/135 - Image Generation Consolidation
- **Actions**:
  1. Merge all image generation cells into single comprehensive cell
  2. Fix deployment discovery (dall-e-3 should exist after Stage 1.1)
  3. Add proper subscription key handling
  4. Implement FLUX model fallback
  5. Add vision analysis
- **Expected Outcome**: Single working image generation cell
- **Backup**: Create before changes
- **Dependencies**: Requires Stage 1.1 completion

#### Stage 2.3: Cell 127 - Cosmos DB RBAC
- **Actions**:
  1. Document required RBAC role for service principal
  2. Provide Azure CLI command to assign role
  3. Add error handling for RBAC failures
  4. Test with proper permissions
- **Expected Outcome**: Clear documentation + working code with proper permissions
- **Note**: May require user to run Azure CLI commands

#### Stage 2.4: Cell 119 - Real Agent-to-Agent Communication
- **Actions**:
  1. Review AutoGen agent configuration
  2. Ensure agents are initialized (planner, critic, summarizer)
  3. Replace simulated coordination with real agent calls
  4. Test agent communication flow
- **Expected Outcome**: Real A2A communication, not simulated
- **Backup**: Create before changes

---

### STAGE 3: MEDIUM Severity Optimizations

#### Stage 3.1: Cells 81/83/137 - MCP Data Analysis Consolidation
- **Actions**:
  1. Merge Cell 81 (pandas) and Cell 83 (MCP) into single cell
  2. Prioritize MCP calls, fallback to pandas only if needed
  3. Merge Cell 137 into consolidated data analysis cell
  4. Demonstrate MCP Excel capabilities
- **Expected Outcome**: Single comprehensive data analysis cell using MCP
- **Backup**: Create before changes

#### Stage 3.2: Cell 98 - MCP Docs Connection Enhancement
- **Actions**:
  1. Add proper request payload to MCP docs server
  2. Demonstrate search/query functionality
  3. Show successful 200 response with content
- **Expected Outcome**: Working MCP docs demonstration
- **Backup**: Create before changes

#### Stage 3.3: Cell 133 - Log Analytics Fix
- **Actions**:
  1. Define or import 'utils' module
  2. Fix Log Analytics query
  3. Test logging output display
- **Expected Outcome**: Proper logging display with query results
- **Backup**: Create before changes

---

## Testing Strategy

### Per-Cell Testing (A-L Protocol)
For each cell fix:
- **A**: Analyze error and root cause
- **B**: Build fix with proper imports and error handling
- **C**: Create backup before modification
- **D**: Document changes with before/after code
- **E**: Execute cell in isolation
- **F**: Verify expected output
- **G**: Test edge cases
- **H**: Handle errors gracefully
- **I**: Integrate with dependent cells
- **J**: Journal all changes in phase2/ folder
- **K**: Keep reference files
- **L**: Log success confirmation

### Batch Testing
After each stage:
1. Run all cells in stage sequentially
2. Verify no regression in previously working cells
3. Document results

### Full Notebook Test
After all stages:
1. Sequential execution cells 1-173
2. Validate all fixes working together
3. Document final results

---

## Documentation Requirements

### Per Fix
- Create `cell-{number}-original.py` (reference)
- Create `cell-{number}-fixed.py` (new code)
- Create `STAGE{X}.{Y}-{NAME}-FIX.md` (detailed documentation)

### Stage Summaries
- `STAGE1-CRITICAL-COMPLETE.md`
- `STAGE2-HIGH-COMPLETE.md`
- `STAGE3-MEDIUM-COMPLETE.md`

### Phase Summary
- `PHASE2-COMPLETION-SUMMARY.md`

### Testing
- `PHASE2-BATCH-TEST-STATUS.md`
- `PHASE2-BATCH-TEST-RESULTS.md`

---

## Risk Assessment

### HIGH Risk Items
1. **Cell 29 dall-e-3**: Already fixed in Phase 1, may indicate deployment issue
2. **Cell 103 Semantic Cache**: Complex APIM policy interaction
3. **Cell 150 Vector Search**: Requires Azure Search configuration

### MEDIUM Risk Items
1. **Cell 127 Cosmos DB**: Requires Azure RBAC changes
2. **Cell 119 A2A**: Complex agent coordination

### LOW Risk Items
1. **Cell 81**: Simple column name fix
2. **Cell 17**: Simple encoding fix
3. **Cell 133**: Simple import/definition fix

---

## Dependencies

### Infrastructure Requirements
- dall-e-3 model deployed (Stage 1.1)
- Embedding models deployed (text-embedding-3-small/large)
- Azure Search instance (for Cell 150)
- Cosmos DB with proper RBAC (for Cell 127)
- MCP servers running (docs, excel)

### Code Dependencies
- Image generation cells → dall-e-3 deployment (Stage 1.1)
- Semantic cache → Policy verification (Cell 17)
- Vector search → Embedding deployment
- A2A communication → AutoGen agents initialized

---

## Success Metrics

| Objective | Target | Measurement |
|-----------|--------|-------------|
| Fix CRITICAL issues | 100% | 4/4 cells working |
| Fix HIGH issues | 100% | 4/4 cells working |
| Fix MEDIUM issues | 100% | 5/5 cells working |
| Create backups | All stages | 1 per stage minimum |
| Document fixes | All fixes | 1 doc per fix |
| Batch test | Pass | All cells execute |
| Full test | Pass | Sequential 1-173 |

---

## Timeline Estimate

- **Stage 1 (CRITICAL)**: 2-3 hours
- **Stage 2 (HIGH)**: 2-3 hours
- **Stage 3 (MEDIUM)**: 1-2 hours
- **Testing**: 1 hour
- **Documentation**: Continuous
- **Total**: 6-9 hours

---

## Next Steps

1. ✅ Create Phase 2 execution plan (this document)
2. ⏳ Begin Stage 1.1: Investigate Cell 29 dall-e-3 issue
3. ⏳ Continue through stages systematically
4. ⏳ Test after each stage
5. ⏳ Git commit after major stages
6. ⏳ Final testing and documentation
7. ⏳ Git push when complete

---

**Phase 2 Status**: 📋 PLAN CREATED - READY TO BEGIN
