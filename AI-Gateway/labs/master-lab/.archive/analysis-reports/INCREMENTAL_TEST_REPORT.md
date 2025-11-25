# Incremental Testing Report

**Generated:** 2025-11-11T02:29:08.035585
**Notebook:** master-ai-gateway copy.ipynb
**Testing Method:** Incremental (1, then 1-2, then 1-2-3, etc.)

## Summary

- **Total Iterations:** 29
- **Cells Tested:** 29
- **Total Issues:** 154

## Iteration Results


### Iteration 1: Cells [1]

**Issues Found:** 0


### Iteration 2: Cells [1, 2]

**Issues Found:** 1


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


### Iteration 3: Cells [1, 2, 3]

**Issues Found:** 1


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


### Iteration 4: Cells [1, 2, 3, 4]

**Issues Found:** 1


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


### Iteration 5: Cells [1, 2, 3, 4, 5]

**Issues Found:** 1


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


### Iteration 6: Cells [1, 2, 3, 4, 5, 6]

**Issues Found:** 1


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


### Iteration 7: Cells [1, 2, 3, 4, 5, 6, 7]

**Issues Found:** 1


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


### Iteration 8: Cells [1, 2, 3, 4, 5, 6, 7, 8]

**Issues Found:** 1


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


### Iteration 9: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9]

**Issues Found:** 2


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


### Iteration 10: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

**Issues Found:** 2


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


### Iteration 11: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

**Issues Found:** 3


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


#### Cell 11

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


### Iteration 12: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13]

**Issues Found:** 5


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


#### Cell 11

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


#### Cell 13

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 13
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 13 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 13
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 13:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


### Iteration 13: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14]

**Issues Found:** 5


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


#### Cell 11

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


#### Cell 13

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 13
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 13 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 13
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 13:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


### Iteration 14: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15]

**Issues Found:** 5


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


#### Cell 11

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


#### Cell 13

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 13
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 13 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 13
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 13:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


### Iteration 15: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 17]

**Issues Found:** 7


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


#### Cell 11

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


#### Cell 13

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 13
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 13 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 13
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 13:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 17

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 17
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 17 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


### Iteration 16: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 17, 18]

**Issues Found:** 7


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


#### Cell 11

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


#### Cell 13

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 13
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 13 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 13
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 13:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 17

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 17
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 17 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


### Iteration 17: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 17, 18, 22]

**Issues Found:** 7


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


#### Cell 11

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


#### Cell 13

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 13
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 13 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 13
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 13:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 17

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 17
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 17 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


### Iteration 18: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 17, 18, 22, 23]

**Issues Found:** 7


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


#### Cell 11

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


#### Cell 13

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 13
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 13 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 13
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 13:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 17

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 17
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 17 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


### Iteration 19: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 17, 18, 22, 23, 24]

**Issues Found:** 7


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


#### Cell 11

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


#### Cell 13

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 13
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 13 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 13
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 13:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 17

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 17
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 17 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


### Iteration 20: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 17, 18, 22, 23, 24, 27]

**Issues Found:** 8


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


#### Cell 11

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


#### Cell 13

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 13
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 13 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 13
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 13:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 17

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 17
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 17 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


#### Cell 27

- **[HIGH]** Error detected in output

### Iteration 21: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 17, 18, 22, 23, 24, 27, 28]

**Issues Found:** 8


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


#### Cell 11

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


#### Cell 13

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 13
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 13 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 13
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 13:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 17

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 17
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 17 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


#### Cell 27

- **[HIGH]** Error detected in output

### Iteration 22: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 17, 18, 22, 23, 24, 27, 28, 30]

**Issues Found:** 8


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


#### Cell 11

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


#### Cell 13

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 13
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 13 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 13
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 13:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 17

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 17
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 17 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


#### Cell 27

- **[HIGH]** Error detected in output

### Iteration 23: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 17, 18, 22, 23, 24, 27, 28, 30, 31]

**Issues Found:** 8


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


#### Cell 11

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


#### Cell 13

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 13
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 13 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 13
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 13:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 17

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 17
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 17 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


#### Cell 27

- **[HIGH]** Error detected in output

### Iteration 24: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 17, 18, 22, 23, 24, 27, 28, 30, 31, 32]

**Issues Found:** 9


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


#### Cell 11

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


#### Cell 13

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 13
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 13 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 13
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 13:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 17

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 17
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 17 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


#### Cell 27

- **[HIGH]** Error detected in output

#### Cell 32

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 32
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 32 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


### Iteration 25: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 17, 18, 22, 23, 24, 27, 28, 30, 31, 32, 34]

**Issues Found:** 9


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


#### Cell 11

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


#### Cell 13

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 13
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 13 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 13
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 13:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 17

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 17
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 17 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


#### Cell 27

- **[HIGH]** Error detected in output

#### Cell 32

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 32
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 32 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


### Iteration 26: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 17, 18, 22, 23, 24, 27, 28, 30, 31, 32, 34, 36]

**Issues Found:** 9


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


#### Cell 11

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


#### Cell 13

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 13
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 13 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 13
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 13:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 17

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 17
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 17 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


#### Cell 27

- **[HIGH]** Error detected in output

#### Cell 32

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 32
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 32 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


### Iteration 27: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 17, 18, 22, 23, 24, 27, 28, 30, 31, 32, 34, 36, 38]

**Issues Found:** 10


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


#### Cell 11

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


#### Cell 13

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 13
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 13 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 13
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 13:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 17

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 17
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 17 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


#### Cell 27

- **[HIGH]** Error detected in output

#### Cell 32

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 32
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 32 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


#### Cell 38

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


### Iteration 28: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 17, 18, 22, 23, 24, 27, 28, 30, 31, 32, 34, 36, 38, 40]

**Issues Found:** 10


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


#### Cell 11

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


#### Cell 13

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 13
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 13 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 13
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 13:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 17

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 17
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 17 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


#### Cell 27

- **[HIGH]** Error detected in output

#### Cell 32

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 32
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 32 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


#### Cell 38

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


### Iteration 29: Cells [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 17, 18, 22, 23, 24, 27, 28, 30, 31, 32, 34, 36, 38, 40, 41]

**Issues Found:** 11


#### Cell 2

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 2
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 2 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 2
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 2:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 9

- **[HIGH]** Missing environment variables: vars

**Fix Suggestions:**

**Issue:** Missing environment variable: vars

- Fix 1: Add vars to master-lab.env
  ```python
# Edit master-lab.env, add:
vars=<your-value-here>
# Then re-run Cell 3 to reload environment
  ```

- Fix 2: Derive vars from existing variables
  ```python
# No automatic derivation available for vars
  ```

- Fix 3: Set default value in code
  ```python
# Add to cell before using vars:
vars = os.getenv('vars', '<default-value>')
  ```


#### Cell 11

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


#### Cell 13

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 13
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 13 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 13
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 13:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


#### Cell 17

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5
- **[HIGH]** Error detected in output

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 17
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 17 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


#### Cell 27

- **[HIGH]** Error detected in output

#### Cell 32

- **[MEDIUM]** get_az_cli() redefined - should use global az_cli from Cell 5

**Fix Suggestions:**

**Issue:** get_az_cli() redefined - should use global az_cli from Cell 5

- Fix 1: Remove duplicate, use global az_cli
  ```python
# Remove the get_az_cli() function definition from Cell 32
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly
  ```

- Fix 2: Import from Cell 5
  ```python
# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli
  ```

- Fix 3: Remove this cell entirely
  ```python
# If Cell 32 only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead
  ```


#### Cell 38

- **[HIGH]** Bicep files referenced without using BICEP_DIR or archive/scripts path

**Fix Suggestions:**

**Issue:** Bicep files referenced without using BICEP_DIR or archive/scripts path

- Fix 1: Use BICEP_DIR environment variable
  ```python
# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"
  ```

- Fix 2: Use relative path to archive/scripts
  ```python
# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")
  ```

- Fix 3: Copy bicep files to notebook directory
  ```python
# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .
  ```


#### Cell 41

- **[MEDIUM]** Environment loading duplicated - should use Cell 3 only

**Fix Suggestions:**

**Issue:** Environment loading duplicated - should use Cell 3 only

- Fix 1: Remove duplicate, use ENV from Cell 3
  ```python
# Remove environment loading code from Cell 41
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly
  ```

- Fix 2: Merge unique logic into Cell 3
  ```python
# If Cell 41 has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell 41
  ```

- Fix 3: Mark as deprecated, keep for reference
  ```python
# Add to top of Cell 41:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)
  ```


## Recommendations

Based on the incremental testing:

1. **High Priority Issues:** Fix all HIGH severity issues before proceeding
2. **Duplicate Code:** Remove duplicate implementations to reduce confusion
3. **Path Issues:** Update all bicep file paths to use archive/scripts
4. **Environment Variables:** Add missing variables to master-lab.env

See individual iteration results above for specific fix suggestions.
