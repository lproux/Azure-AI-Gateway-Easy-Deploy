# Analysis Report: Cells 42-238 (Lab Exercises)

**Analyzed:** 105 code cells, 114 markdown cells
**Lab Start Cell:** 12

## Summary

**Total Issues Found:** 18
- HIGH Severity: 0
- MEDIUM Severity: 18

## Duplicate Code Patterns

### Environment Loaders
- **Count:** 1
- **Recommendation:** Remove, use Cell 3 from initialization section

### Azure CLI Resolution
- **get_az_cli() functions:** 8
- **Other az CLI resolvers:** 9
- **Recommendation:** Use az_cli variable from Cell 5

### Hardcoded Paths
- **Cells with hardcoded bicep paths:** 0
- **Recommendation:** Use BICEP_DIR from Cell 3

### Duplicate Imports

Top duplicated imports:
- `os`: imported 26 times
- `time`: imported 11 times
- `notebook_mcp_helpers`: imported 11 times
- `shutil`: imported 10 times
- `os,`: imported 9 times
- `subprocess`: imported 9 times
- `tempfile`: imported 8 times
- `pathlib`: imported 6 times
- `typing`: imported 6 times
- `json`: imported 6 times
- `openai`: imported 5 times
- `asyncio`: imported 5 times
- `requests`: imported 4 times
- `azure.identity`: imported 4 times
- `dotenv`: imported 4 times

## Issues by Cell

### Cell 13

- **[MEDIUM]** Duplicate environment loader

### Cell 22

- **[MEDIUM]** Duplicate Azure CLI resolution

### Cell 38

- **[MEDIUM]** Duplicate get_az_cli() function
- **[MEDIUM]** Duplicate Azure CLI resolution

### Cell 45

- **[MEDIUM]** Duplicate get_az_cli() function
- **[MEDIUM]** Duplicate Azure CLI resolution

### Cell 55

- **[MEDIUM]** Duplicate get_az_cli() function
- **[MEDIUM]** Duplicate Azure CLI resolution

### Cell 64

- **[MEDIUM]** Duplicate get_az_cli() function
- **[MEDIUM]** Duplicate Azure CLI resolution

### Cell 99

- **[MEDIUM]** Duplicate get_az_cli() function
- **[MEDIUM]** Duplicate Azure CLI resolution

### Cell 104

- **[MEDIUM]** Duplicate get_az_cli() function
- **[MEDIUM]** Duplicate Azure CLI resolution

### Cell 211

- **[MEDIUM]** Duplicate get_az_cli() function
- **[MEDIUM]** Duplicate Azure CLI resolution

### Cell 224

- **[MEDIUM]** Duplicate get_az_cli() function
- **[MEDIUM]** Duplicate Azure CLI resolution


## Recommendations

Based on analysis of lab exercise cells 42-238:

1. **Remove Duplicate Environment Loaders**
   - Found 1 duplicate loaders
   - Replace with: `if 'ENV' not in globals(): raise RuntimeError("Run Cell 3 first")`

2. **Remove Duplicate Azure CLI Resolvers**
   - Found 8 get_az_cli() functions
   - Replace with: `if 'az_cli' not in globals(): raise RuntimeError("Run Cell 5 first")`

3. **Fix Hardcoded Bicep Paths**
   - Found 0 cells with hardcoded paths
   - Use BICEP_DIR environment variable set in Cell 3

4. **Consolidate Imports**
   - Many cells re-import the same modules
   - Consider using Cell 28 (Master Imports) more effectively

## Next Steps

1. Review issues found in each cell
2. Apply fixes similar to cells 1-41:
   - Remove duplicate code
   - Fix hardcoded paths
   - Add prerequisite checks
3. Create final consolidated notebook
4. Test end-to-end

## Expected Impact

After consolidation of cells 42-238:
- Additional cells removed: Est. 5-10
- Code reduction: Est. 500-1,000 lines
- Issue count reduction: 18 → <10

