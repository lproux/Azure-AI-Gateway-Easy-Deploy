#!/usr/bin/env python3
"""
Analyze cells 42-238 using the same methodology as cells 1-41
"""
import json
import re
from pathlib import Path
from collections import defaultdict

def analyze_cells_42_238():
    """Analyze remaining cells 42-238"""

    # Load consolidated notebook
    nb_path = Path('master-ai-gateway-consolidated.ipynb')
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells = nb['cells']
    print(f"Loaded notebook: {len(cells)} cells")

    # We removed 9 cells from original 238, so we have 229 cells
    # Original cells 42-238 are now approximately cells 34-230 in consolidated

    # Find where cell 42 starts (look for cell after cell 41)
    # Original structure: Cells 1-41 were initialization
    # In consolidated: We removed cells 2,14,18,22,23,24,31,32,41 from first 41
    # So original cell 42 is now at a different index

    # Strategy: Find cells that are likely lab exercises (after initialization)
    # Look for markdown headers with "Section", "Lab", "Exercise", or specific patterns

    print("\n" + "="*80)
    print("ANALYZING CELLS 42-238 (LAB EXERCISES)")
    print("="*80)

    # Find transition point from initialization to lab exercises
    lab_start_idx = None
    for idx, cell in enumerate(cells):
        if cell['cell_type'] == 'markdown':
            source = ''.join(cell.get('source', []))
            # Look for section markers
            if any(marker in source.upper() for marker in ['# SECTION 0', '# SECTION 1', '## SECTION', 'EXERCISE', 'LAB']):
                if 'SECTION 0' not in source.upper():  # Section 0 is deployment
                    lab_start_idx = idx
                    print(f"\n✅ Found lab exercise section start at cell {idx + 1}")
                    print(f"   Marker: {source[:100]}")
                    break

    if not lab_start_idx:
        # Fallback: assume cells after 41 (accounting for removals)
        # We removed 8 cells before cell 41, so original cell 42 is roughly cell 34
        lab_start_idx = 34
        print(f"\n⚠️  Using estimated start: cell {lab_start_idx}")

    # Analyze cells from lab start to end
    lab_cells = cells[lab_start_idx:]
    print(f"\nLab exercise cells: {len(lab_cells)}")

    # Analysis structures
    issues_found = defaultdict(list)
    code_cells = []
    markdown_cells = []

    # Categorize cells
    for idx, cell in enumerate(lab_cells):
        global_idx = lab_start_idx + idx
        cell_num = global_idx + 1

        if cell['cell_type'] == 'code':
            code_cells.append((cell_num, cell))
        else:
            markdown_cells.append((cell_num, cell))

    print(f"Code cells: {len(code_cells)}")
    print(f"Markdown cells: {len(markdown_cells)}")

    # Analyze code cells for common issues
    print("\n" + "="*80)
    print("CODE ANALYSIS (Lab Exercise Cells)")
    print("="*80)

    duplicate_patterns = {
        'env_loader': 0,
        'az_cli_resolver': 0,
        'get_az_cli': 0,
        'import_duplicates': defaultdict(int),
        'file_references': defaultdict(list),
        'hardcoded_paths': [],
    }

    for cell_num, cell in code_cells:
        source = ''.join(cell.get('source', []))

        # Check for duplicate environment loading
        if 'ENV_FILE' in source and 'load' in source.lower():
            duplicate_patterns['env_loader'] += 1
            issues_found[cell_num].append(('MEDIUM', 'Duplicate environment loader'))

        # Check for duplicate Azure CLI resolution
        if 'def get_az_cli' in source:
            duplicate_patterns['get_az_cli'] += 1
            issues_found[cell_num].append(('MEDIUM', 'Duplicate get_az_cli() function'))

        # Check for Azure CLI resolution patterns
        if 'shutil.which' in source and 'az' in source:
            duplicate_patterns['az_cli_resolver'] += 1
            issues_found[cell_num].append(('MEDIUM', 'Duplicate Azure CLI resolution'))

        # Check for imports
        imports = re.findall(r'^import\s+(\S+)', source, re.MULTILINE)
        imports += re.findall(r'^from\s+(\S+)\s+import', source, re.MULTILINE)
        for imp in imports:
            duplicate_patterns['import_duplicates'][imp] += 1

        # Check for file references
        files = re.findall(r'["\']([^"\']*\.(?:bicep|json|py|txt|env|yaml|yml))["\']', source)
        for f in files:
            duplicate_patterns['file_references'][f].append(cell_num)

        # Check for hardcoded paths
        if any(keyword in source for keyword in ['deploy-01', 'deploy-02', 'deploy-03', 'deploy-04']):
            if 'BICEP_DIR' not in source and 'archive/scripts' not in source:
                duplicate_patterns['hardcoded_paths'].append(cell_num)
                issues_found[cell_num].append(('HIGH', 'Hardcoded bicep file paths'))

    # Report findings
    print(f"\n📊 Summary:")
    print(f"  Duplicate environment loaders: {duplicate_patterns['env_loader']}")
    print(f"  Duplicate get_az_cli() definitions: {duplicate_patterns['get_az_cli']}")
    print(f"  Duplicate Azure CLI resolvers: {duplicate_patterns['az_cli_resolver']}")
    print(f"  Hardcoded bicep paths: {len(duplicate_patterns['hardcoded_paths'])}")

    # Most duplicated imports
    if duplicate_patterns['import_duplicates']:
        print(f"\n  Most duplicated imports:")
        top_imports = sorted(duplicate_patterns['import_duplicates'].items(),
                           key=lambda x: x[1], reverse=True)[:10]
        for imp, count in top_imports:
            if count > 3:  # Only show if imported more than 3 times
                print(f"    {imp}: {count} times")

    # File references
    if duplicate_patterns['file_references']:
        print(f"\n  File references:")
        for file, cells in sorted(duplicate_patterns['file_references'].items()):
            if len(cells) > 1:
                print(f"    {file}: referenced in {len(cells)} cells")

    # Issues by severity
    print("\n" + "="*80)
    print("ISSUES FOUND (Cells 42-238 equivalent)")
    print("="*80)

    high_severity = sum(1 for cell_issues in issues_found.values()
                       for sev, _ in cell_issues if sev == 'HIGH')
    medium_severity = sum(1 for cell_issues in issues_found.values()
                         for sev, _ in cell_issues if sev == 'MEDIUM')

    print(f"\nTotal issues: {high_severity + medium_severity}")
    print(f"  HIGH: {high_severity}")
    print(f"  MEDIUM: {medium_severity}")

    if issues_found:
        print(f"\nIssues by cell:")
        for cell_num in sorted(issues_found.keys())[:20]:  # Show first 20
            print(f"\n  Cell {cell_num}:")
            for severity, issue in issues_found[cell_num]:
                print(f"    [{severity}] {issue}")

    # Save analysis
    report_path = Path('analysis-reports/CELLS_42_238_ANALYSIS.md')
    report = generate_report(lab_start_idx, code_cells, markdown_cells,
                           duplicate_patterns, issues_found)
    report_path.write_text(report)
    print(f"\n📄 Report saved: {report_path}")

    return issues_found, duplicate_patterns


def generate_report(lab_start_idx, code_cells, markdown_cells, duplicate_patterns, issues_found):
    """Generate markdown report"""

    high_count = sum(1 for cell_issues in issues_found.values()
                    for sev, _ in cell_issues if sev == 'HIGH')
    medium_count = sum(1 for cell_issues in issues_found.values()
                      for sev, _ in cell_issues if sev == 'MEDIUM')

    report = f"""# Analysis Report: Cells 42-238 (Lab Exercises)

**Analyzed:** {len(code_cells)} code cells, {len(markdown_cells)} markdown cells
**Lab Start Cell:** {lab_start_idx + 1}

## Summary

**Total Issues Found:** {high_count + medium_count}
- HIGH Severity: {high_count}
- MEDIUM Severity: {medium_count}

## Duplicate Code Patterns

### Environment Loaders
- **Count:** {duplicate_patterns['env_loader']}
- **Recommendation:** Remove, use Cell 3 from initialization section

### Azure CLI Resolution
- **get_az_cli() functions:** {duplicate_patterns['get_az_cli']}
- **Other az CLI resolvers:** {duplicate_patterns['az_cli_resolver']}
- **Recommendation:** Use az_cli variable from Cell 5

### Hardcoded Paths
- **Cells with hardcoded bicep paths:** {len(duplicate_patterns['hardcoded_paths'])}
- **Recommendation:** Use BICEP_DIR from Cell 3

### Duplicate Imports

Top duplicated imports:
"""

    top_imports = sorted(duplicate_patterns['import_duplicates'].items(),
                        key=lambda x: x[1], reverse=True)[:15]
    for imp, count in top_imports:
        if count > 3:
            report += f"- `{imp}`: imported {count} times\n"

    report += """
## Issues by Cell

"""

    for cell_num in sorted(issues_found.keys()):
        report += f"### Cell {cell_num}\n\n"
        for severity, issue in issues_found[cell_num]:
            report += f"- **[{severity}]** {issue}\n"
        report += "\n"

    report += """
## Recommendations

Based on analysis of lab exercise cells 42-238:

1. **Remove Duplicate Environment Loaders**
   - Found {env_loader} duplicate loaders
   - Replace with: `if 'ENV' not in globals(): raise RuntimeError("Run Cell 3 first")`

2. **Remove Duplicate Azure CLI Resolvers**
   - Found {get_az_cli} get_az_cli() functions
   - Replace with: `if 'az_cli' not in globals(): raise RuntimeError("Run Cell 5 first")`

3. **Fix Hardcoded Bicep Paths**
   - Found {hardcoded} cells with hardcoded paths
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
- Issue count reduction: {total_issues} → <10

""".format(
        env_loader=duplicate_patterns['env_loader'],
        get_az_cli=duplicate_patterns['get_az_cli'],
        hardcoded=len(duplicate_patterns['hardcoded_paths']),
        total_issues=high_count + medium_count
    )

    return report


if __name__ == '__main__':
    print("="*80)
    print("ANALYZING CELLS 42-238 (LAB EXERCISES)")
    print("="*80)
    print()

    issues, patterns = analyze_cells_42_238()

    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE")
    print("="*80)
    print("\nSee analysis-reports/CELLS_42_238_ANALYSIS.md for full report")
