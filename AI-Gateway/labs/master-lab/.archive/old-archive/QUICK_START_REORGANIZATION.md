# Quick Start: Notebook Reorganization

## 🎯 Goal
Transform the notebook from mixed structure to clear logical flow:
**Deploy → Configure → Initialize → Verify → Labs**

---

## 📊 Current vs. Target Structure

### Current State (MIXED)
```
❌ Cells 1-240: Mixed deployment, config, init, verification, and labs
   - Hard to navigate
   - Difficult to debug
   - Can't run setup separately from labs
   - Dependencies unclear
```

### Target State (ORGANIZED)
```
✅ SECTION 1: Deploy Everything (Cells 1-20)
   → All infrastructure deployment

✅ SECTION 2: Configuration (Cells 21-50)
   → .env generation, config loading

✅ SECTION 3: Initialize (Cells 51-80)
   → Dependencies, SDK setup, clients

✅ SECTION 4: Verify (Cells 81-120)
   → All connectivity and functionality tests

✅ SECTION 5: Labs (Cells 121-280)
   → All 30 labs in logical order
```

---

## 🚀 Quick Implementation (3 Options)

### Option A: Manual Cell-by-Cell (Precise)
**Time: 2-3 days**
**Effort: High**
**Risk: Low**

1. Create new notebook
2. Copy cells one by one following mapping
3. Test after each section
4. Verify all dependencies

### Option B: Automated Script (Fast)
**Time: 4-6 hours**
**Effort: Medium**
**Risk: Medium**

1. Run reorganization script (see below)
2. Review output notebook
3. Fix any broken dependencies
4. Test sections

### Option C: Hybrid Approach (Recommended)
**Time: 1 day**
**Effort: Medium**
**Risk: Low**

1. Use script for initial reorganization
2. Manually adjust problem areas
3. Test each section thoroughly
4. Iterate until clean

---

## 🔧 Automated Reorganization Script

Save as: `reorganize_notebook.py`

```python
#!/usr/bin/env python3
"""
Master Lab Notebook Reorganizer
Transforms mixed-structure notebook into organized sections
"""

import json
import sys
from pathlib import Path

# Cell mapping: current_cell_id → (new_section, new_position)
CELL_MAP = {
    # SECTION 1: DEPLOY (1-20)
    8: (1, 4), 28: (1, 5), 30: (1, 7), 110: (1, 8), 113: (1, 9), 203: (1, 10),

    # SECTION 2: CONFIGURE (21-50)
    24: (2, 21), 31: (2, 22), 3: (2, 24), 25: (2, 25), 13: (2, 26), 27: (2, 27),
    6: (2, 28), 29: (2, 29), 5: (2, 30), 7: (2, 31), 22: (2, 32), 9: (2, 33),
    11: (2, 34), 10: (2, 35),

    # SECTION 3: INITIALIZE (51-80)
    4: (3, 51), 14: (3, 52), 23: (3, 54), 43: (3, 55), 73: (3, 56), 49: (3, 57),
    104: (3, 58), 58: (3, 59),

    # SECTION 4: VERIFY (81-120)
    37: (4, 89), 38: (4, 90), 39: (4, 91), 40: (4, 92), 41: (4, 93), 42: (4, 94),
    59: (4, 86), 61: (4, 87), 63: (4, 88), 46: (4, 104), 47: (4, 105), 48: (4, 106),
    69: (4, 95), 71: (4, 96), 75: (4, 97), 108: (4, 98), 103: (4, 107), 115: (4, 112),

    # SECTION 5: LABS (121+)
    36: (5, 121), 44: (5, 129), 52: (5, 141), 54: (5, 146), 56: (5, 151),
    68: (5, 161), 70: (5, 166), 72: (5, 171), 76: (5, 176), 80: (5, 181),
    # ... (add remaining lab cells)
}

# Section headers
SECTION_HEADERS = {
    1: {
        'type': 'markdown',
        'source': [
            '# SECTION 1: DEPLOY EVERYTHING (4.1)\n',
            '\n',
            '## Overview\n',
            'This section handles all Azure infrastructure deployment:\n',
            '- Resource groups\n',
            '- API Management (APIM)\n',
            '- Azure OpenAI / AI services\n',
            '- Storage and networking\n',
            '- Optional resources\n',
            '\n',
            '**Expected Duration:** 10-15 minutes\n',
            '\n',
            '**Prerequisites:**\n',
            '- Azure subscription\n',
            '- Azure CLI installed and authenticated\n',
            '- Contributor role on subscription\n'
        ]
    },
    2: {
        'type': 'markdown',
        'source': [
            '# SECTION 2: CONFIGURATION & ENVIRONMENT (4.2)\n',
            '\n',
            '## Overview\n',
            'This section generates and loads configuration:\n',
            '- Generate .env file from deployment outputs\n',
            '- Load environment variables\n',
            '- Configure service endpoints\n',
            '- Setup authentication credentials\n',
            '\n',
            '**Expected Duration:** 1-2 minutes\n'
        ]
    },
    3: {
        'type': 'markdown',
        'source': [
            '# SECTION 3: INITIALIZE EVERYTHING (4.3)\n',
            '\n',
            '## Overview\n',
            'This section initializes all dependencies:\n',
            '- Install Python packages\n',
            '- Import SDK libraries\n',
            '- Initialize Azure clients\n',
            '- Setup helper functions\n',
            '- Initialize MCP connections\n',
            '\n',
            '**Expected Duration:** 2-3 minutes\n'
        ]
    },
    4: {
        'type': 'markdown',
        'source': [
            '# SECTION 4: VERIFICATION - MAKE SURE EVERYTHING WORKS (4.4)\n',
            '\n',
            '## Overview\n',
            'This section verifies all systems are operational:\n',
            '- Infrastructure accessibility\n',
            '- Authentication methods\n',
            '- Basic API functionality\n',
            '- Service-specific features\n',
            '- MCP server connectivity\n',
            '- Load balancing\n',
            '\n',
            '**Expected Duration:** 3-5 minutes\n',
            '\n',
            '✅ All tests must pass before proceeding to labs!\n'
        ]
    },
    5: {
        'type': 'markdown',
        'source': [
            '# SECTION 5: ALL LABS (4.5)\n',
            '\n',
            '## Overview\n',
            'This section contains all workshop labs:\n',
            '- 30+ hands-on exercises\n',
            '- Each lab is independent\n',
            '- Prerequisites listed in lab headers\n',
            '- Can be run selectively\n',
            '\n',
            '**Labs included:**\n',
            '- Lab 01-10: Core functionality\n',
            '- Lab 11-20: MCP integration\n',
            '- Lab 21-30: Advanced features\n',
            '\n',
            '**Note:** You can jump to any lab after Section 4 completes successfully.\n'
        ]
    }
}


def reorganize_notebook(input_path, output_path):
    """Reorganize notebook cells according to CELL_MAP"""

    print(f"Loading notebook: {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    original_cells = nb['cells']
    print(f"Original cell count: {len(original_cells)}")

    # Create new cell array with placeholders
    max_new_idx = max(pos for _, pos in CELL_MAP.values()) if CELL_MAP else 300
    new_cells = [None] * (max_new_idx + 50)  # Extra buffer

    # Insert section headers
    for section_num, header_cell in SECTION_HEADERS.items():
        # Calculate insertion position
        if section_num == 1:
            pos = 0
        elif section_num == 2:
            pos = 20
        elif section_num == 3:
            pos = 50
        elif section_num == 4:
            pos = 80
        else:  # section 5
            pos = 120

        new_cells[pos] = header_cell

    # Map cells to new positions
    moved_count = 0
    for old_idx, (section, new_idx) in CELL_MAP.items():
        if 0 <= old_idx - 1 < len(original_cells):
            cell = original_cells[old_idx - 1]
            new_cells[new_idx - 1] = cell
            moved_count += 1
            print(f"  Cell {old_idx} → Section {section}, Position {new_idx}")

    # Handle unmapped cells (place in appropriate section based on content)
    unmapped = []
    for idx, cell in enumerate(original_cells, 1):
        if idx not in CELL_MAP:
            unmapped.append((idx, cell))

    print(f"\nMapped: {moved_count} cells")
    print(f"Unmapped: {len(unmapped)} cells (will be added to labs section)")

    # Add unmapped cells to labs section
    labs_start = 121
    next_pos = labs_start + sum(1 for c in new_cells[labs_start:] if c is not None)
    for old_idx, cell in unmapped:
        if cell.get('cell_type') != 'markdown' or len(''.join(cell.get('source', []))) > 10:
            new_cells[next_pos] = cell
            next_pos += 1

    # Remove None placeholders
    final_cells = [c for c in new_cells if c is not None]

    print(f"\nFinal cell count: {len(final_cells)}")

    # Update notebook
    nb['cells'] = final_cells

    # Save reorganized notebook
    print(f"\nSaving reorganized notebook: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)

    print("✅ Reorganization complete!")

    return len(final_cells)


def main():
    if len(sys.argv) < 2:
        print("Usage: python reorganize_notebook.py <input_notebook.ipynb> [output_notebook.ipynb]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else input_path.parent / f"{input_path.stem}-REORGANIZED{input_path.suffix}"

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    # Backup original
    backup_path = input_path.parent / f"{input_path.stem}-BACKUP{input_path.suffix}"
    print(f"Creating backup: {backup_path}")
    import shutil
    shutil.copy(input_path, backup_path)

    # Reorganize
    reorganize_notebook(input_path, output_path)

    print(f"\n📁 Files:")
    print(f"  Original (backup): {backup_path}")
    print(f"  Reorganized: {output_path}")


if __name__ == '__main__':
    main()
```

---

## 🏃 How to Run Reorganization

### Step 1: Backup
```bash
cd AI-Gateway/labs/master-lab
cp master-ai-gateway-fix-MCP.ipynb master-ai-gateway-fix-MCP-BACKUP-$(date +%Y%m%d).ipynb
```

### Step 2: Run Script
```bash
python3 reorganize_notebook.py master-ai-gateway-fix-MCP.ipynb master-ai-gateway-REORGANIZED.ipynb
```

### Step 3: Test New Structure
```bash
# Open in Jupyter
jupyter notebook master-ai-gateway-REORGANIZED.ipynb

# Or VS Code
code master-ai-gateway-REORGANIZED.ipynb
```

### Step 4: Validate Sections
Run each section in order:
1. ✅ Section 1 (Deploy) → Should complete without errors
2. ✅ Section 2 (Configure) → Should generate .env
3. ✅ Section 3 (Initialize) → Should load all clients
4. ✅ Section 4 (Verify) → All tests should pass
5. ✅ Section 5 (Labs) → Test 2-3 random labs

---

## 📝 Manual Adjustments Needed After Script

### 1. Add Missing Section Dividers
Between sections, add visual separators:
```markdown
---
✅ SECTION X COMPLETE
---
```

### 2. Update Cell Dependencies
Some cells may reference old cell numbers in comments:
```python
# OLD: See cell 42 for details
# NEW: See Section 4, Verification cell for details
```

### 3. Add Progress Indicators
Insert at start of each section:
```python
print("=" * 80)
print("🚀 Starting Section X: [Name]")
print("=" * 80)
```

### 4. Fix Broken References
Search for:
- `# From cell XX` → Update to section reference
- Variable dependencies → Ensure previous section defines them
- Hardcoded cell numbers → Update or remove

---

## ✅ Verification Checklist

After reorganization, verify:

### Section 1: Deploy
- [ ] All deployment cells present
- [ ] Deployment completes successfully
- [ ] Resources created in Azure
- [ ] No errors in output

### Section 2: Configure
- [ ] .env file generated
- [ ] All required variables present
- [ ] Environment loads without errors
- [ ] Endpoints are valid

### Section 3: Initialize
- [ ] All packages installed
- [ ] No import errors
- [ ] All clients initialized
- [ ] Helper functions available

### Section 4: Verify
- [ ] Infrastructure tests pass
- [ ] Authentication tests pass
- [ ] API functionality tests pass
- [ ] MCP connectivity tests pass (or skip gracefully)
- [ ] Readiness report shows 100% or explains failures

### Section 5: Labs
- [ ] All lab headers present
- [ ] Labs are in logical order
- [ ] Can jump to any lab
- [ ] Each lab runs independently

---

## 🐛 Common Issues & Fixes

### Issue 1: Undefined Variables
**Symptom:** `NameError: name 'xxx' is not defined`
**Fix:** Move variable definition to earlier section

### Issue 2: Import Errors
**Symptom:** `ModuleNotFoundError`
**Fix:** Ensure Section 3 includes all imports

### Issue 3: Missing Dependencies
**Symptom:** Cell depends on previous cell output
**Fix:** Check CELL_MAP, ensure dependency moved together

### Issue 4: Broken MCP Connections
**Symptom:** Timeout errors in Section 4
**Fix:** Add try/except wrapper, allow graceful skip

---

## 📈 Success Metrics

Track these metrics after reorganization:

| Metric | Target | Current |
|--------|--------|---------|
| Section 1 Success Rate | 100% | TBD |
| Section 2 Success Rate | 100% | TBD |
| Section 3 Success Rate | 100% | TBD |
| Section 4 Success Rate | 95%+ | TBD |
| Section 5 Lab Count | 30+ | TBD |
| One-Click Execution Time | <15 min | TBD |
| Total Errors (1-4) | 0 | TBD |

---

## 🎯 Next Steps

1. **Review:** Read full REORGANIZATION_PLAN.md
2. **Decide:** Choose implementation option (A, B, or C)
3. **Backup:** Create backup of current notebook
4. **Execute:** Run reorganization
5. **Test:** Validate all sections
6. **Iterate:** Fix issues, re-test
7. **Document:** Update README with new structure

---

## 📚 Related Documents

- **REORGANIZATION_PLAN.md** - Full detailed plan
- **MASTER_LAB_FIX_PLAN.md** - Error fixing strategy
- **master-ai-gateway-fix-MCP.ipynb** - Current notebook
- **master-ai-gateway-REORGANIZED.ipynb** - Target output

---

**Last Updated:** 2025-11-13
**Status:** READY TO EXECUTE
**Estimated Time:** 1 day (hybrid approach)
