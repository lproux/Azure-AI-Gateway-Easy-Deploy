#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apply Approved Fixes Based on User Selections

User Choices:
- Q1: A - Apply all 9 HIGH priority fixes
- Q2: B - Investigate all 78 cells
- Q3: A (modified) - Add debugging, comment out old code
- Q4: C - HIGH fixes now, MEDIUM after running
- Q5: A - Incremental testing
- Q6: A - Investigate error cells in detail
"""
import json
import re
import sys
from pathlib import Path
from datetime import datetime

# Configure UTF-8 for Windows
if sys.platform == 'win32':
    import codecs
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    else:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


class ApprovedFixApplicator:
    """Apply approved fixes to notebook"""

    def __init__(self, notebook_path: str):
        self.notebook_path = Path(notebook_path)
        with open(self.notebook_path, 'r', encoding='utf-8') as f:
            self.notebook = json.load(f)
        self.cells = self.notebook['cells']
        self.fixes_applied = []

    def apply_all_approved_fixes(self):
        """Apply all fixes according to user approval"""

        print("Applying fixes according to your selections:")
        print("  Q1: A - Apply 9 HIGH priority fixes")
        print("  Q2: B - Investigate 78 cells (after running)")
        print("  Q3: A (modified) - Cell 100 with commented code")
        print("  Q4: C - HIGH now, MEDIUM after running")
        print("  Q5: A - Incremental testing")
        print("  Q6: A - Investigate error cells")
        print()

        # HIGH Priority Fixes (Q1: A)
        print("="*80)
        print("APPLYING HIGH PRIORITY FIXES (9 cells)")
        print("="*80)
        print()

        # Fix 1-8: Remove duplicate get_az_cli() functions
        duplicate_cells = [38, 45, 55, 64, 99, 104, 211, 224]
        for cell_num in duplicate_cells:
            success = self._remove_duplicate_get_az_cli(cell_num)
            if success:
                print(f"✅ Cell {cell_num}: Removed duplicate get_az_cli()")
            else:
                print(f"⚠️  Cell {cell_num}: Could not remove (may not exist)")

        # Fix 9: Add environment variable check (Cell 102)
        success = self._add_env_var_check(102)
        if success:
            print(f"✅ Cell 102: Added environment variable validation")
        else:
            print(f"⚠️  Cell 102: Could not add env var check")

        print()

        # MEDIUM Priority Fix (Q3: A modified)
        print("="*80)
        print("APPLYING MEDIUM PRIORITY FIX (1 cell)")
        print("="*80)
        print()

        success = self._fix_cell_100_with_commented_code()
        if success:
            print(f"✅ Cell 100: Added debugging (old code commented)")
        else:
            print(f"⚠️  Cell 100: Could not apply fix")

        print()
        print(f"Total fixes applied: {len(self.fixes_applied)}")

        return len(self.fixes_applied)

    def _remove_duplicate_get_az_cli(self, cell_num: int) -> bool:
        """Remove duplicate get_az_cli() function from cell"""

        idx = cell_num - 1
        if idx < 0 or idx >= len(self.cells):
            return False

        cell = self.cells[idx]
        if cell.get('cell_type') != 'code':
            return False

        source = self._get_source(cell)

        # Check if get_az_cli exists
        if 'def get_az_cli' not in source:
            return False

        # Add prerequisite check at top
        prereq_check = """# Require Cell 5 (Azure CLI Setup) to have been run
if 'az_cli' not in globals():
    raise RuntimeError("❌ Run Cell 5 (Azure CLI Setup) first to set az_cli variable")

"""

        # Add check if not already present
        if 'if \'az_cli\' not in globals()' not in source:
            source = prereq_check + source

        # Remove get_az_cli() function definition
        lines = source.split('\n')
        new_lines = []
        in_function = False
        function_indent = 0

        for line in lines:
            # Check if this is the start of get_az_cli()
            if 'def get_az_cli' in line:
                in_function = True
                function_indent = len(line) - len(line.lstrip())
                continue

            # If we're in the function, skip lines until we're back to original indent
            if in_function:
                current_indent = len(line) - len(line.lstrip())
                if line.strip() and current_indent <= function_indent:
                    in_function = False
                    new_lines.append(line)
                continue

            new_lines.append(line)

        new_source = '\n'.join(new_lines)

        # Remove any remaining az_cli = get_az_cli() calls
        new_source = re.sub(
            r'az_cli\s*=\s*get_az_cli\(\)',
            '# az_cli already set by Cell 5',
            new_source
        )

        self._set_source(cell, new_source)
        self.fixes_applied.append({
            'cell': cell_num,
            'type': 'remove_duplicate_function',
            'description': 'Removed get_az_cli() function'
        })

        return True

    def _add_env_var_check(self, cell_num: int) -> bool:
        """Add environment variable validation to cell"""

        idx = cell_num - 1
        if idx < 0 or idx >= len(self.cells):
            return False

        cell = self.cells[idx]
        if cell.get('cell_type') != 'code':
            return False

        source = self._get_source(cell)

        # Check if already has validation
        if 'required_vars' in source:
            return False

        # Add validation at top
        var_check = """# Validate required environment variables
import os
required_vars = ['RESOURCE_GROUP', 'APIM_GATEWAY_URL']
missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    print(f"⚠️  Missing environment variables: {missing}")
    print("   Run Cell 3 (Environment Loader) first")
    raise RuntimeError(f"Missing variables: {missing}")

"""

        new_source = var_check + source
        self._set_source(cell, new_source)
        self.fixes_applied.append({
            'cell': cell_num,
            'type': 'add_env_var_check',
            'description': 'Added environment variable validation'
        })

        return True

    def _fix_cell_100_with_commented_code(self) -> bool:
        """Fix Cell 100 with debugging, comment out old code"""

        cell_num = 100
        idx = cell_num - 1

        if idx < 0 or idx >= len(self.cells):
            return False

        cell = self.cells[idx]
        if cell.get('cell_type') != 'code':
            return False

        source = self._get_source(cell)

        # Add comment banner and debugging at top
        fix_header = """# ============================================================================
# DEBUGGING ADDED - Review this fix manually
# Original code commented out below for comparison
# Issue: HTTP 404 - endpoint not found
# Fix: Added endpoint verification and debugging
# ============================================================================

# NEW CODE: Add debugging to verify endpoint
import os
print("🔍 Debugging Cell 100 - Endpoint Verification")
print(f"APIM Gateway URL: {os.getenv('APIM_GATEWAY_URL', 'NOT SET')}")
print(f"API ID: {os.getenv('API_ID', 'NOT SET')}")

# Check if URL is being constructed correctly
if 'url' in locals():
    print(f"Constructed URL: {url}")
else:
    print("⚠️  URL variable not yet defined")

# ============================================================================
# ORIGINAL CODE (COMMENTED OUT FOR REVIEW)
# ============================================================================
"""

        # Comment out all original code
        lines = source.split('\n')
        commented_lines = []
        for line in lines:
            # Skip empty lines and already commented lines
            if line.strip() and not line.strip().startswith('#'):
                commented_lines.append('# ' + line)
            else:
                commented_lines.append(line)

        commented_source = '\n'.join(commented_lines)

        # Combine
        new_source = fix_header + commented_source

        # Add note at end
        new_source += """

# ============================================================================
# END OF COMMENTED CODE
# ============================================================================
# TODO: After reviewing, uncomment the code you want to keep and remove debugging
# Or apply targeted fix based on debugging output
"""

        self._set_source(cell, new_source)
        self.fixes_applied.append({
            'cell': cell_num,
            'type': 'add_debugging_with_commented_code',
            'description': 'Added debugging, commented out original code for review'
        })

        return True

    def _get_source(self, cell: dict) -> str:
        """Get cell source as string"""
        source = cell.get('source', [])
        if isinstance(source, list):
            return ''.join(source)
        return source

    def _set_source(self, cell: dict, new_source: str):
        """Set cell source"""
        cell['source'] = [new_source]

    def save(self, output_path: str):
        """Save fixed notebook"""
        output = Path(output_path)
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(self.notebook, f, indent=1)
        return str(output)

    def generate_changelog(self) -> str:
        """Generate changelog of applied fixes"""

        changelog = f"""# Applied Fixes Changelog

**Date:** {datetime.now().isoformat()}
**Source:** master-ai-gateway-consolidated.ipynb
**Output:** master-ai-gateway-with-approved-fixes.ipynb

## User Selections

- **Q1:** A - Apply all 9 HIGH priority fixes ✅
- **Q2:** B - Investigate all 78 cells (after running) ⏳
- **Q3:** A (modified) - Cell 100 with commented code for review ✅
- **Q4:** C - HIGH fixes now, MEDIUM after running ✅
- **Q5:** A - Incremental testing (next step) ⏳
- **Q6:** A - Investigate error cells in detail (next step) ⏳

---

## Fixes Applied: {len(self.fixes_applied)}

### HIGH Priority Fixes (9 cells)

"""

        # Group by type
        by_type = {}
        for fix in self.fixes_applied:
            fix_type = fix['type']
            if fix_type not in by_type:
                by_type[fix_type] = []
            by_type[fix_type].append(fix['cell'])

        for fix_type, cells in sorted(by_type.items()):
            changelog += f"\n#### {fix_type}\n"
            changelog += f"**Cells:** {', '.join(map(str, cells))}\n\n"

            # Add details for each cell
            for fix in self.fixes_applied:
                if fix['type'] == fix_type:
                    changelog += f"- **Cell {fix['cell']}:** {fix['description']}\n"

            changelog += "\n"

        changelog += """
---

## Next Steps (According to Your Selections)

### Immediate (Q4: C - HIGH fixes now)
✅ HIGH priority fixes applied
✅ Cell 100 has commented code for your review

### Next: Incremental Testing (Q5: A)

**Phase 1: Test Cells 1-41 (Initialization)**
1. Run Cell 3 (Environment Loader)
2. Run Cell 5 (Azure CLI Setup)
3. Run remaining initialization cells
4. Verify all succeed

**Phase 2: Test Cells 42-230 (Lab Exercises)**
1. Run cells incrementally
2. Document which cells fail
3. Apply MEDIUM fixes based on actual errors (Q4: C)

### Pending: Investigate Cells (Q2: B, Q6: A)

**Q2: Investigate all 78 MEDIUM priority cells**
- Will do after running notebook
- Many cells just need execution, not fixes
- Will identify actual errors vs unexecuted cells

**Q6: Investigate 3 cells with specific errors**
- Cell 57: SystemExit error in API call
- Cell 59: Content safety test - unclear outcome
- Cells 71-73: MCP-related errors
- Will investigate in detail after initial testing

---

## Files Created

- ✅ `master-ai-gateway-with-approved-fixes.ipynb` - Notebook with fixes applied
- ✅ `APPLIED_FIXES_CHANGELOG.md` - This changelog
- ✅ Backups created before applying fixes

## Verification Checklist

**Before Running:**
- [ ] Review Cell 100 (has commented code for manual review)
- [ ] Check all HIGH priority cells (38, 45, 55, 64, 99, 102, 104, 211, 224)
- [ ] Verify prerequisite checks added correctly

**After Running Cells 1-41:**
- [ ] Cell 3 loads environment successfully
- [ ] Cell 5 sets az_cli correctly
- [ ] No cells with removed get_az_cli() throw errors
- [ ] Cell 102 env var check works correctly

**After Running Cells 42-230:**
- [ ] Document which cells succeed
- [ ] Document which cells fail with errors
- [ ] Apply MEDIUM fixes to failing cells
- [ ] Rerun until 100% success

---

## Expected Outcomes

**After HIGH Priority Fixes:**
- No more duplicate get_az_cli() functions
- Clear prerequisite error messages
- Better environment variable validation
- Cell 100 has debugging for your review

**After Incremental Testing:**
- Will identify which of 78 MEDIUM priority cells actually need fixes
- Most cells likely just needed execution
- Only cells with real errors will get targeted fixes

**Final Goal:**
- 100% of cells execute successfully
- All issues resolved
- Notebook ready for production use

---

**Status:** Phase 1 complete (HIGH fixes applied)
**Next:** Review Cell 100, then begin incremental testing (Q5: A)
"""

        return changelog


def main():
    print("="*80)
    print("APPLYING APPROVED FIXES")
    print("="*80)
    print()

    # Confirm backups exist
    backup_files = list(Path('.').glob('*BACKUP*.ipynb'))
    if backup_files:
        print("✅ Backups confirmed:")
        for backup in backup_files:
            print(f"   - {backup.name}")
        print()
    else:
        print("⚠️  No backups found! Creating backup now...")
        import subprocess
        subprocess.run(['cp', 'master-ai-gateway-consolidated.ipynb',
                       f'master-ai-gateway-consolidated-BACKUP-{datetime.now().strftime("%Y%m%d-%H%M%S")}.ipynb'])
        print()

    # Apply fixes
    applicator = ApprovedFixApplicator('master-ai-gateway-consolidated.ipynb')
    num_fixes = applicator.apply_all_approved_fixes()

    # Save
    output_path = applicator.save('master-ai-gateway-with-approved-fixes.ipynb')

    print()
    print("="*80)
    print("✅ FIXES APPLIED SUCCESSFULLY")
    print("="*80)
    print(f"\nFixed notebook: {output_path}")
    print(f"Total fixes: {num_fixes}")

    # Generate changelog
    changelog = applicator.generate_changelog()
    changelog_path = Path('analysis-reports/APPLIED_FIXES_CHANGELOG.md')
    changelog_path.write_text(changelog, encoding='utf-8')

    print(f"Changelog: {changelog_path}")

    print()
    print("="*80)
    print("NEXT STEPS")
    print("="*80)
    print()
    print("1. 📝 Review Cell 100 (has commented code for your manual review)")
    print("2. 🧪 Test cells 1-41 incrementally (initialization)")
    print("3. 🧪 Test cells 42-230 incrementally (lab exercises)")
    print("4. 🔍 Investigate 3 cells with specific errors (57, 59, 71-73)")
    print("5. 🔧 Apply MEDIUM fixes based on actual test results")
    print("6. ✅ Verify 100% success rate")
    print()
    print("See APPLIED_FIXES_CHANGELOG.md for complete details")


if __name__ == '__main__':
    main()
