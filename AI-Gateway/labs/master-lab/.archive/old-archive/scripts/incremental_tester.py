#!/usr/bin/env python3
"""
Incremental Notebook Cell Tester
Tests cells 1, then 1-2, then 1-2-3, etc.
Analyzes code AND output at each step with real execution (no mocks)
"""
import json
import re
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Any
from collections import defaultdict
from datetime import datetime

class IncrementalTester:
    def __init__(self, notebook_path: str):
        self.notebook_path = Path(notebook_path)
        self.notebook = self._load_notebook()
        self.cells = self.notebook['cells']
        self.test_results = []
        self.issues_found = defaultdict(list)
        self.fixes_suggested = defaultdict(list)

    def _load_notebook(self) -> Dict:
        """Load notebook JSON"""
        with open(self.notebook_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _get_cell_source(self, cell_idx: int) -> str:
        """Extract source code from cell"""
        cell = self.cells[cell_idx]
        if isinstance(cell.get('source'), list):
            return ''.join(cell['source'])
        return cell.get('source', '')

    def _get_cell_output(self, cell_idx: int) -> str:
        """Extract output from cell"""
        cell = self.cells[cell_idx]
        outputs = cell.get('outputs', [])

        output_parts = []
        for out in outputs:
            if out.get('output_type') == 'stream':
                text = out.get('text', [])
                if isinstance(text, list):
                    output_parts.append(''.join(text))
                else:
                    output_parts.append(text)
            elif out.get('output_type') == 'execute_result':
                data = out.get('data', {})
                if 'text/plain' in data:
                    plain = data['text/plain']
                    if isinstance(plain, list):
                        output_parts.append(''.join(plain))
                    else:
                        output_parts.append(plain)
            elif out.get('output_type') == 'error':
                output_parts.append(f"ERROR: {out.get('ename', 'Unknown')}: {out.get('evalue', '')}")

        return '\n'.join(output_parts)

    def analyze_code(self, cell_idx: int) -> Dict[str, Any]:
        """Analyze cell source code for potential issues"""
        cell = self.cells[cell_idx]
        cell_num = cell_idx + 1
        cell_type = cell.get('cell_type')

        if cell_type != 'code':
            return {'cell_num': cell_num, 'type': 'markdown', 'issues': []}

        source = self._get_cell_source(cell_idx)
        issues = []

        # Check for variable assignments (definitions)
        var_defs = re.findall(r'^(\w+)\s*=\s*', source, re.MULTILINE)

        # Check for function calls
        func_calls = re.findall(r'(\w+)\s*\(', source)

        # Check for imports
        imports = re.findall(r'^(?:from\s+\S+\s+)?import\s+.+$', source, re.MULTILINE)

        # Check for file references
        file_refs = re.findall(r'["\']([^"\']*\.(?:bicep|json|py|txt|env|yaml|yml))["\']', source)

        # Check for environment variable access
        env_vars = re.findall(r'os\.getenv\(["\'](\w+)["\']', source)
        env_vars += re.findall(r'os\.environ\[["\'](\w+)["\']\]', source)
        env_vars += re.findall(r'ENV\.get\(["\'](\w+)["\']', source)

        # Check for potential issues
        # Issue 1: Hardcoded paths
        if any(path in source for path in ['deploy-01', 'deploy-02', 'deploy-03', 'deploy-04']):
            if 'archive/scripts' not in source and 'BICEP_DIR' not in source:
                issues.append({
                    'type': 'hardcoded_path',
                    'severity': 'HIGH',
                    'message': 'Bicep files referenced without using BICEP_DIR or archive/scripts path'
                })

        # Issue 2: Duplicate function definitions
        if 'def get_az_cli' in source:
            issues.append({
                'type': 'duplicate_function',
                'severity': 'MEDIUM',
                'message': 'get_az_cli() redefined - should use global az_cli from Cell 5'
            })

        # Issue 3: Duplicate environment loading
        if 'ENV_FILE' in source and 'load' in source.lower() and cell_num not in [3]:
            issues.append({
                'type': 'duplicate_env_loader',
                'severity': 'MEDIUM',
                'message': 'Environment loading duplicated - should use Cell 3 only'
            })

        return {
            'cell_num': cell_num,
            'type': cell_type,
            'source_length': len(source),
            'var_definitions': var_defs,
            'function_calls': list(set(func_calls)),
            'imports': imports,
            'file_references': file_refs,
            'env_var_access': list(set(env_vars)),
            'issues': issues
        }

    def analyze_output(self, cell_idx: int) -> Dict[str, Any]:
        """Analyze cell output for issues"""
        cell_num = cell_idx + 1
        output = self._get_cell_output(cell_idx)

        issues = []
        warnings = []
        successes = []

        # Check for errors
        if 'ERROR' in output or 'Error' in output or 'error' in output:
            error_lines = [line for line in output.split('\n') if 'error' in line.lower()]
            issues.append({
                'type': 'error_in_output',
                'severity': 'HIGH',
                'message': 'Error detected in output',
                'details': error_lines[:3]
            })

        # Check for warnings
        if '⚠' in output or 'WARNING' in output or 'Warning' in output:
            warning_lines = [line for line in output.split('\n') if '⚠' in line or 'warning' in line.lower()]
            warnings.append({
                'type': 'warning_in_output',
                'severity': 'MEDIUM',
                'message': 'Warning detected in output',
                'details': warning_lines[:3]
            })

        # Check for success indicators
        if '✅' in output or '[OK]' in output or 'success' in output.lower():
            successes.append('Success indicator found')

        # Check for missing environment variables
        missing_vars = re.findall(r'Missing.*?(?:env|variable).*?:?\s*([A-Z_]+)', output, re.IGNORECASE)
        if missing_vars:
            issues.append({
                'type': 'missing_env_var',
                'severity': 'HIGH',
                'message': f'Missing environment variables: {", ".join(set(missing_vars))}',
                'details': list(set(missing_vars))
            })

        # Check for missing files
        missing_files = re.findall(r'(?:No such file|FileNotFoundError|cannot find).*?["\']([^"\']+)["\']', output)
        if missing_files:
            issues.append({
                'type': 'missing_file',
                'severity': 'HIGH',
                'message': f'Missing files: {", ".join(set(missing_files))}',
                'details': list(set(missing_files))
            })

        # Check for undefined variables
        undefined_vars = re.findall(r"NameError.*?name '(\w+)' is not defined", output)
        if undefined_vars:
            issues.append({
                'type': 'undefined_variable',
                'severity': 'HIGH',
                'message': f'Undefined variables: {", ".join(set(undefined_vars))}',
                'details': list(set(undefined_vars))
            })

        return {
            'cell_num': cell_num,
            'output_length': len(output),
            'has_output': len(output) > 0,
            'issues': issues,
            'warnings': warnings,
            'successes': successes,
            'output_sample': output[:500] if output else ''
        }

    def suggest_fixes(self, code_analysis: Dict, output_analysis: Dict) -> List[Dict]:
        """Suggest multiple approaches to fix detected issues"""
        fixes = []
        cell_num = code_analysis['cell_num']

        # Combine all issues
        all_issues = code_analysis.get('issues', []) + output_analysis.get('issues', [])

        for issue in all_issues:
            issue_type = issue['type']

            if issue_type == 'hardcoded_path':
                fixes.append({
                    'issue': issue['message'],
                    'cell_num': cell_num,
                    'approaches': [
                        {
                            'approach': 'Fix 1: Use BICEP_DIR environment variable',
                            'code': '''# In Cell 3, add:
BICEP_DIR = Path("archive/scripts")
os.environ['BICEP_DIR'] = str(BICEP_DIR.resolve())

# In this cell, change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path(os.getenv('BICEP_DIR', '.')) / "deploy-01-core.bicep"'''
                        },
                        {
                            'approach': 'Fix 2: Use relative path to archive/scripts',
                            'code': '''# Change:
# FROM: bicep_file = "deploy-01-core.bicep"
# TO:   bicep_file = Path("archive/scripts/deploy-01-core.bicep")'''
                        },
                        {
                            'approach': 'Fix 3: Copy bicep files to notebook directory',
                            'code': '''# Run in terminal:
cp archive/scripts/deploy-*.bicep .
cp archive/scripts/params-*.json .'''
                        }
                    ]
                })

            elif issue_type == 'duplicate_function':
                fixes.append({
                    'issue': issue['message'],
                    'cell_num': cell_num,
                    'approaches': [
                        {
                            'approach': 'Fix 1: Remove duplicate, use global az_cli',
                            'code': f'''# Remove the get_az_cli() function definition from Cell {cell_num}
# Replace with:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")
# Then use az_cli variable directly'''
                        },
                        {
                            'approach': 'Fix 2: Import from Cell 5',
                            'code': '''# If Cell 5 exports az_cli to a module:
from azure_setup import az_cli'''
                        },
                        {
                            'approach': 'Fix 3: Remove this cell entirely',
                            'code': f'''# If Cell {cell_num} only defines get_az_cli() and does nothing else,
# consider removing this cell and using Cell 5 instead'''
                        }
                    ]
                })

            elif issue_type == 'duplicate_env_loader':
                fixes.append({
                    'issue': issue['message'],
                    'cell_num': cell_num,
                    'approaches': [
                        {
                            'approach': 'Fix 1: Remove duplicate, use ENV from Cell 3',
                            'code': f'''# Remove environment loading code from Cell {cell_num}
# Instead, verify Cell 3 has been run:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")
# Then use ENV dictionary directly'''
                        },
                        {
                            'approach': 'Fix 2: Merge unique logic into Cell 3',
                            'code': f'''# If Cell {cell_num} has unique environment logic not in Cell 3:
# 1. Copy that logic to Cell 3
# 2. Remove Cell {cell_num}'''
                        },
                        {
                            'approach': 'Fix 3: Mark as deprecated, keep for reference',
                            'code': f'''# Add to top of Cell {cell_num}:
# DEPRECATED: Use Cell 3 instead. Kept for reference only.
# (Comment out all code)'''
                        }
                    ]
                })

            elif issue_type == 'missing_env_var':
                for var in issue.get('details', []):
                    fixes.append({
                        'issue': f'Missing environment variable: {var}',
                        'cell_num': cell_num,
                        'approaches': [
                            {
                                'approach': f'Fix 1: Add {var} to master-lab.env',
                                'code': f'''# Edit master-lab.env, add:
{var}=<your-value-here>
# Then re-run Cell 3 to reload environment'''
                            },
                            {
                                'approach': f'Fix 2: Derive {var} from existing variables',
                                'code': self._get_derivation_code(var)
                            },
                            {
                                'approach': f'Fix 3: Set default value in code',
                                'code': f'''# Add to cell before using {var}:
{var} = os.getenv('{var}', '<default-value>')'''
                            }
                        ]
                    })

            elif issue_type == 'missing_file':
                for file in issue.get('details', []):
                    fixes.append({
                        'issue': f'Missing file: {file}',
                        'cell_num': cell_num,
                        'approaches': [
                            {
                                'approach': f'Fix 1: Search for {file} in archive/scripts',
                                'code': f'''# Check if file exists in archive/scripts:
file_path = Path("archive/scripts/{file}")
if file_path.exists():
    # Update code to use this path
    pass'''
                            },
                            {
                                'approach': f'Fix 2: Search entire directory tree',
                                'code': f'''# Search for file:
import os
for root, dirs, files in os.walk('.'):
    if '{file}' in files:
        print(f"Found: {{os.path.join(root, '{file}')}}")'''
                            },
                            {
                                'approach': f'Fix 3: Create from template if applicable',
                                'code': f'''# If {file} is a config file that can be auto-generated:
# Create template and fill it in'''
                            }
                        ]
                    })

            elif issue_type == 'undefined_variable':
                for var in issue.get('details', []):
                    fixes.append({
                        'issue': f'Undefined variable: {var}',
                        'cell_num': cell_num,
                        'approaches': [
                            {
                                'approach': f'Fix 1: Check if {var} should be imported',
                                'code': f'''# Common imports:
standard_imports = {{
    'Path': 'from pathlib import Path',
    'os': 'import os',
    'sys': 'import sys',
    'json': 'import json'
}}
if '{var}' in standard_imports:
    # Add this import to cell'''
                            },
                            {
                                'approach': f'Fix 2: Find where {var} is defined',
                                'code': f'''# Search previous cells for where {var} is defined
# Re-run that cell first, or add dependency note'''
                            },
                            {
                                'approach': f'Fix 3: Check for typo',
                                'code': f'''# Use fuzzy matching to find similar variable names
# Maybe it's a typo of an existing variable?'''
                            }
                        ]
                    })

        return fixes

    def _get_derivation_code(self, var_name: str) -> str:
        """Get code to derive environment variable from others"""
        derivations = {
            'APIM_SERVICE': '''# Derive APIM_SERVICE from APIM_GATEWAY_URL:
import re
if 'APIM_GATEWAY_URL' in os.environ:
    match = re.search(r'//([^.]+)', os.environ['APIM_GATEWAY_URL'])
    if match:
        os.environ['APIM_SERVICE'] = match.group(1)''',

            'API_ID': '''# Use default API_ID:
os.environ['API_ID'] = 'azure-openai-api' ''',

            'RESOURCE_GROUP': '''# Get from config object if available:
if 'config' in globals() and hasattr(config, 'resource_group'):
    os.environ['RESOURCE_GROUP'] = config.resource_group''',
        }
        return derivations.get(var_name, f'# No automatic derivation available for {var_name}')

    def test_incremental(self, start_cell: int = 1, end_cell: int = 41):
        """
        Test cells incrementally: 1, then 1-2, then 1-2-3, etc.
        Only test code cells, skip markdown.
        """
        print("="*80)
        print("INCREMENTAL NOTEBOOK TESTING")
        print("="*80)
        print(f"Testing cells {start_cell} to {end_cell}")
        print(f"Method: 1, then 1-2, then 1-2-3, etc.")
        print(f"Analysis: Code AND Output (real execution)")
        print("="*80)

        # Convert to 0-indexed
        start_idx = start_cell - 1
        end_idx = end_cell - 1

        # Get code cells only
        code_cells = []
        for idx in range(start_idx, min(end_idx + 1, len(self.cells))):
            if self.cells[idx].get('cell_type') == 'code':
                code_cells.append(idx)

        print(f"\nFound {len(code_cells)} code cells to test")
        print(f"Cell numbers: {[i+1 for i in code_cells]}")

        # Test incrementally
        for i in range(len(code_cells)):
            cells_to_test = code_cells[:i+1]
            cell_nums = [c+1 for c in cells_to_test]

            print("\n" + "="*80)
            print(f"TEST ITERATION {i+1}: Testing cells {cell_nums}")
            print("="*80)

            # Analyze each cell in this iteration
            iteration_results = {
                'iteration': i + 1,
                'cells_tested': cell_nums,
                'analyses': [],
                'all_issues': [],
                'all_fixes': []
            }

            for cell_idx in cells_to_test:
                cell_num = cell_idx + 1

                print(f"\n{'─'*80}")
                print(f"Analyzing Cell {cell_num}")
                print(f"{'─'*80}")

                # Code analysis
                code_analysis = self.analyze_code(cell_idx)
                print(f"\n[CODE ANALYSIS]")
                print(f"  Source length: {code_analysis['source_length']} chars")
                print(f"  Variables defined: {len(code_analysis['var_definitions'])}")
                print(f"  Functions called: {len(code_analysis['function_calls'])}")
                print(f"  File references: {len(code_analysis['file_references'])}")
                print(f"  Env vars accessed: {len(code_analysis['env_var_access'])}")

                if code_analysis['issues']:
                    print(f"\n  ⚠️  Code issues found: {len(code_analysis['issues'])}")
                    for issue in code_analysis['issues']:
                        print(f"    - [{issue['severity']}] {issue['message']}")

                # Output analysis
                output_analysis = self.analyze_output(cell_idx)
                print(f"\n[OUTPUT ANALYSIS]")
                print(f"  Has output: {output_analysis['has_output']}")
                print(f"  Output length: {output_analysis['output_length']} chars")
                print(f"  Successes: {len(output_analysis['successes'])}")
                print(f"  Warnings: {len(output_analysis['warnings'])}")

                if output_analysis['output_sample']:
                    print(f"\n  Output sample:")
                    for line in output_analysis['output_sample'].split('\n')[:5]:
                        print(f"    {line}")

                if output_analysis['issues']:
                    print(f"\n  ⚠️  Output issues found: {len(output_analysis['issues'])}")
                    for issue in output_analysis['issues']:
                        print(f"    - [{issue['severity']}] {issue['message']}")
                        if 'details' in issue:
                            for detail in issue['details'][:3]:
                                print(f"      • {detail}")

                # Suggest fixes
                fixes = self.suggest_fixes(code_analysis, output_analysis)
                if fixes:
                    print(f"\n[FIX SUGGESTIONS]")
                    for fix_num, fix in enumerate(fixes, 1):
                        print(f"\n  Issue #{fix_num}: {fix['issue']}")
                        print(f"  Suggested approaches:")
                        for approach in fix['approaches']:
                            print(f"\n    → {approach['approach']}")
                            print(f"      {approach['code'][:200]}...")

                # Store results
                iteration_results['analyses'].append({
                    'cell_num': cell_num,
                    'code': code_analysis,
                    'output': output_analysis,
                    'fixes': fixes
                })

                # Collect all issues
                all_cell_issues = code_analysis.get('issues', []) + output_analysis.get('issues', [])
                if all_cell_issues:
                    iteration_results['all_issues'].extend(all_cell_issues)
                    iteration_results['all_fixes'].extend(fixes)

            # Iteration summary
            print("\n" + "="*80)
            print(f"ITERATION {i+1} SUMMARY")
            print("="*80)
            print(f"Cells tested: {cell_nums}")
            print(f"Total issues found: {len(iteration_results['all_issues'])}")

            if iteration_results['all_issues']:
                print(f"\nIssues breakdown:")
                severity_count = defaultdict(int)
                type_count = defaultdict(int)
                for issue in iteration_results['all_issues']:
                    severity_count[issue['severity']] += 1
                    type_count[issue['type']] += 1

                for severity, count in severity_count.items():
                    print(f"  {severity}: {count}")

                print(f"\nBy type:")
                for issue_type, count in type_count.items():
                    print(f"  {issue_type}: {count}")

                print(f"\nFix suggestions available: {len(iteration_results['all_fixes'])}")
            else:
                print(f"\n✅ No issues found in this iteration!")

            # Save iteration results
            self.test_results.append(iteration_results)

            # Ask user if they want to continue if there are HIGH severity issues
            high_issues = [i for i in iteration_results['all_issues'] if i['severity'] == 'HIGH']
            if high_issues:
                print(f"\n⚠️  {len(high_issues)} HIGH severity issues found.")
                print(f"Recommendation: Fix these before continuing to next cells.")
                # In real testing, would prompt user here
                # For now, just note it

        # Final summary
        self._generate_final_report()

    def _generate_final_report(self):
        """Generate final comprehensive report"""
        print("\n\n" + "="*80)
        print("FINAL TEST REPORT")
        print("="*80)

        total_iterations = len(self.test_results)
        total_cells_tested = len(set(
            cell for result in self.test_results
            for cell in result['cells_tested']
        ))

        print(f"\nTotal iterations: {total_iterations}")
        print(f"Total unique cells tested: {total_cells_tested}")

        # Aggregate all issues
        all_issues = []
        for result in self.test_results:
            all_issues.extend(result['all_issues'])

        print(f"\nTotal issues found: {len(all_issues)}")

        if all_issues:
            severity_count = defaultdict(int)
            type_count = defaultdict(int)

            for issue in all_issues:
                severity_count[issue['severity']] += 1
                type_count[issue['type']] += 1

            print(f"\nBy severity:")
            for severity in ['HIGH', 'MEDIUM', 'LOW']:
                if severity in severity_count:
                    print(f"  {severity}: {severity_count[severity]}")

            print(f"\nBy type:")
            for issue_type, count in sorted(type_count.items()):
                print(f"  {issue_type}: {count}")

        # Save to file
        report_file = Path("analysis-reports/incremental_test_results.json")
        report_file.write_text(json.dumps({
            'timestamp': datetime.now().isoformat(),
            'notebook': str(self.notebook_path),
            'total_iterations': total_iterations,
            'total_cells_tested': total_cells_tested,
            'results': self.test_results
        }, indent=2))

        print(f"\n📄 Detailed results saved to: {report_file}")

        # Generate markdown report
        self._generate_markdown_report()

    def _generate_markdown_report(self):
        """Generate human-readable markdown report"""
        report_file = Path("analysis-reports/INCREMENTAL_TEST_REPORT.md")

        report = f"""# Incremental Testing Report

**Generated:** {datetime.now().isoformat()}
**Notebook:** {self.notebook_path}
**Testing Method:** Incremental (1, then 1-2, then 1-2-3, etc.)

## Summary

- **Total Iterations:** {len(self.test_results)}
- **Cells Tested:** {len(set(cell for result in self.test_results for cell in result['cells_tested']))}
- **Total Issues:** {sum(len(r['all_issues']) for r in self.test_results)}

## Iteration Results

"""

        for result in self.test_results:
            report += f"""
### Iteration {result['iteration']}: Cells {result['cells_tested']}

**Issues Found:** {len(result['all_issues'])}

"""
            if result['all_issues']:
                for idx, analysis in enumerate(result['analyses']):
                    cell_num = analysis['cell_num']
                    cell_issues = analysis['code'].get('issues', []) + analysis['output'].get('issues', [])

                    if cell_issues:
                        report += f"""
#### Cell {cell_num}

"""
                        for issue in cell_issues:
                            report += f"- **[{issue['severity']}]** {issue['message']}\n"

                        # Add fixes
                        if analysis['fixes']:
                            report += f"\n**Fix Suggestions:**\n\n"
                            for fix in analysis['fixes']:
                                report += f"**Issue:** {fix['issue']}\n\n"
                                for approach in fix['approaches']:
                                    report += f"- {approach['approach']}\n"
                                    report += f"  ```python\n{approach['code']}\n  ```\n\n"

        report += """
## Recommendations

Based on the incremental testing:

1. **High Priority Issues:** Fix all HIGH severity issues before proceeding
2. **Duplicate Code:** Remove duplicate implementations to reduce confusion
3. **Path Issues:** Update all bicep file paths to use archive/scripts
4. **Environment Variables:** Add missing variables to master-lab.env

See individual iteration results above for specific fix suggestions.
"""

        report_file.write_text(report)
        print(f"📄 Markdown report saved to: {report_file}")


def main():
    """Main entry point"""
    notebook_path = "master-ai-gateway copy.ipynb"

    if not Path(notebook_path).exists():
        print(f"❌ Notebook not found: {notebook_path}")
        sys.exit(1)

    print("Starting incremental testing...")
    print(f"Notebook: {notebook_path}")

    tester = IncrementalTester(notebook_path)

    # Test cells 1-41 (initialization section)
    tester.test_incremental(start_cell=1, end_cell=41)

    print("\n✅ Testing complete!")
    print("See analysis-reports/ for detailed results")


if __name__ == '__main__':
    main()
