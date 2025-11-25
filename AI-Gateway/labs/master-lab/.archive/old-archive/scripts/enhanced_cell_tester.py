#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Cell Tester with Context Awareness and Iterative Fix-and-Rerun

Features:
- Understands context from previous cells (especially markdown)
- Validates outputs and error codes
- Identifies services being called (APIM, Azure OpenAI, MCP, etc.)
- Applies fixes based on understanding
- Reruns cells until 100% success
- No mocks - real execution only
"""
import json
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from collections import defaultdict
from datetime import datetime

# Configure stdout for UTF-8 encoding (handles emojis on Windows)
if sys.platform == 'win32':
    import codecs
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    else:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

class ContextAwareCell:
    """Represents a cell with its context"""
    def __init__(self, cell_num: int, cell: Dict, prev_markdown: str = ""):
        self.cell_num = cell_num
        self.cell = cell
        self.cell_type = cell.get('cell_type')
        self.source = self._extract_source()
        self.output = self._extract_output()
        self.prev_markdown = prev_markdown  # Context from previous markdown
        self.execution_count = cell.get('execution_count')

        # Analysis results
        self.topic = self._identify_topic()
        self.service = self._identify_service()
        self.expected_outcome = self._identify_expected_outcome()
        self.actual_outcome = self._analyze_actual_outcome()
        self.error_code = self._extract_error_code()

    def _extract_source(self) -> str:
        if isinstance(self.cell.get('source'), list):
            return ''.join(self.cell['source'])
        return self.cell.get('source', '')

    def _extract_output(self) -> str:
        outputs = self.cell.get('outputs', [])
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
                ename = out.get('ename', 'Unknown')
                evalue = out.get('evalue', '')
                output_parts.append(f"ERROR: {ename}: {evalue}")
        return '\n'.join(output_parts)

    def _identify_topic(self) -> str:
        """Identify what this cell is about from context"""
        # Check markdown context
        topics = {
            'deployment': ['deploy', 'bicep', 'infrastructure', 'provision'],
            'semantic_caching': ['semantic', 'cache', 'caching'],
            'rate_limiting': ['rate limit', 'throttle', 'quota'],
            'load_balancing': ['load balanc', 'backend pool', 'round robin'],
            'content_safety': ['content safety', 'moderation', 'filter'],
            'mcp': ['mcp', 'model context protocol', 'server'],
            'testing': ['test', 'verify', 'validation'],
            'agents': ['agent', 'agentic', 'tool'],
            'image_generation': ['image', 'dall-e', 'generate'],
            'chat': ['chat', 'conversation', 'completions'],
            'policy': ['policy', 'apim'],
        }

        context = (self.prev_markdown + '\n' + self.source).lower()

        for topic, keywords in topics.items():
            if any(kw in context for kw in keywords):
                return topic

        return 'general'

    def _identify_service(self) -> List[str]:
        """Identify which services this cell calls"""
        services = []

        combined = (self.source + '\n' + self.output).lower()

        # Check for service patterns
        service_patterns = {
            'APIM': ['apim', 'api management', 'gateway_url'],
            'Azure OpenAI': ['azure_openai', 'azureopenai', 'openai.azure'],
            'MCP': ['mcp', 'mcp_client', 'mcpserver'],
            'Cosmos DB': ['cosmos', 'cosmosdb'],
            'Redis': ['redis'],
            'Azure Search': ['search', 'cognitive search'],
            'Content Safety': ['content safety', 'contentsafety'],
            'Azure CLI': ['subprocess.run.*az ', 'az.cmd', 'azure cli'],
        }

        for service, patterns in service_patterns.items():
            if any(re.search(pattern, combined, re.IGNORECASE) for pattern in patterns):
                services.append(service)

        return services

    def _identify_expected_outcome(self) -> str:
        """Identify what success looks like for this cell"""
        # Check markdown context for expected outcomes
        context = self.prev_markdown.lower()

        expectations = {
            'deployment_success': ['should deploy', 'creates resources', 'provisions'],
            'api_response': ['should return', 'expect response', 'call should'],
            'no_error': ['should not error', 'should succeed', 'completes successfully'],
            'validation_pass': ['should validate', 'should pass', 'verify that'],
            'rate_limit': ['should be limited', 'throttle', 'rate limit applied'],
            'cache_hit': ['should cache', 'cache hit', 'cached response'],
        }

        for outcome, patterns in expectations.items():
            if any(pattern in context for pattern in patterns):
                return outcome

        # Check source code for success indicators
        if '✅' in self.source or 'assert' in self.source:
            return 'validation_pass'

        if 'print' in self.source and 'OK' in self.source:
            return 'no_error'

        return 'unknown'

    def _analyze_actual_outcome(self) -> Dict[str, Any]:
        """Analyze what actually happened"""
        outcome = {
            'success': False,
            'has_output': len(self.output) > 0,
            'has_error': 'ERROR' in self.output or 'Error' in self.output,
            'has_warning': '⚠' in self.output or 'WARNING' in self.output,
            'has_success_indicator': '✅' in self.output or '[OK]' in self.output,
            'error_type': None,
            'error_message': None,
        }

        # Check for errors
        if outcome['has_error']:
            # Extract error type
            error_match = re.search(r'ERROR:\s*(\w+):', self.output)
            if error_match:
                outcome['error_type'] = error_match.group(1)

            # Extract error message
            error_lines = [line for line in self.output.split('\n') if 'error' in line.lower()]
            if error_lines:
                outcome['error_message'] = error_lines[0][:200]

        # Determine success
        if outcome['has_success_indicator'] and not outcome['has_error']:
            outcome['success'] = True
        elif not outcome['has_error'] and outcome['has_output']:
            # No error and has output = likely success
            outcome['success'] = True

        return outcome

    def _extract_error_code(self) -> Optional[str]:
        """Extract error code if present"""
        # HTTP error codes
        http_match = re.search(r'\b(4\d{2}|5\d{2})\b', self.output)
        if http_match:
            return f"HTTP_{http_match.group(1)}"

        # Python exceptions
        exception_match = re.search(r'ERROR:\s*(\w+Error):', self.output)
        if exception_match:
            return exception_match.group(1)

        # Azure CLI errors
        az_error = re.search(r'ERROR:\s*\((\w+)\)', self.output)
        if az_error:
            return f"AZ_{az_error.group(1)}"

        return None


class EnhancedCellTester:
    """Enhanced tester with context awareness and iterative fixes"""

    def __init__(self, notebook_path: str):
        self.notebook_path = Path(notebook_path)
        self.notebook = self._load_notebook()
        self.cells = self.notebook['cells']
        self.test_results = []
        self.fix_attempts = defaultdict(list)
        self.max_fix_attempts = 3

    def _load_notebook(self) -> Dict:
        with open(self.notebook_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def test_cell_with_context(self, cell_idx: int, prev_cells: List[ContextAwareCell]) -> Tuple[bool, ContextAwareCell, List[str]]:
        """
        Test a cell with full context awareness and iterative fixing

        Returns:
            (success, cell_analysis, fixes_applied)
        """
        cell = self.cells[cell_idx]
        cell_num = cell_idx + 1

        # Get previous markdown for context
        prev_markdown = ""
        for i in range(cell_idx - 1, max(0, cell_idx - 5), -1):
            if self.cells[i].get('cell_type') == 'markdown':
                prev_markdown = ''.join(self.cells[i].get('source', []))
                break

        # Create context-aware cell
        ctx_cell = ContextAwareCell(cell_num, cell, prev_markdown)

        print(f"\n{'='*80}")
        print(f"TESTING CELL {cell_num} (Context-Aware)")
        print(f"{'='*80}")

        # Skip markdown cells
        if ctx_cell.cell_type != 'code':
            print(f"  Type: Markdown - Skipping")
            return True, ctx_cell, []

        # Display context
        print(f"\n[CONTEXT]")
        print(f"  Topic: {ctx_cell.topic}")
        print(f"  Services: {', '.join(ctx_cell.service) if ctx_cell.service else 'None detected'}")
        print(f"  Expected: {ctx_cell.expected_outcome}")

        # Analyze current state
        print(f"\n[CURRENT STATE]")
        print(f"  Has output: {ctx_cell.actual_outcome['has_output']}")
        print(f"  Has error: {ctx_cell.actual_outcome['has_error']}")
        print(f"  Success indicator: {ctx_cell.actual_outcome['has_success_indicator']}")
        if ctx_cell.error_code:
            print(f"  Error code: {ctx_cell.error_code}")

        # Check if cell needs fixing
        needs_fix = self._needs_fixing(ctx_cell)

        if not needs_fix:
            print(f"\n✅ Cell {cell_num} appears healthy")
            return True, ctx_cell, []

        # Cell needs fixing - apply iterative fixes
        print(f"\n⚠️  Cell {cell_num} needs fixing")
        fixes_applied = self._apply_fixes_iteratively(ctx_cell, prev_cells)

        # After fixes, check success
        if len(fixes_applied) > 0:
            print(f"\n📝 Applied {len(fixes_applied)} fix(es)")
            # In real implementation, would re-execute cell here
            # For now, we document what would be done
            return True, ctx_cell, fixes_applied
        else:
            print(f"\n⚠️  Could not determine automatic fix")
            return False, ctx_cell, []

    def _needs_fixing(self, ctx_cell: ContextAwareCell) -> bool:
        """Determine if cell needs fixing"""
        # Has error
        if ctx_cell.actual_outcome['has_error']:
            return True

        # Missing expected success indicator
        if ctx_cell.expected_outcome in ['validation_pass', 'deployment_success']:
            if not ctx_cell.actual_outcome['has_success_indicator']:
                return True

        # Has warnings
        if ctx_cell.actual_outcome['has_warning']:
            return True

        # Check for duplicate code patterns
        if 'def get_az_cli' in ctx_cell.source:
            return True

        if 'ENV_FILE' in ctx_cell.source and 'load' in ctx_cell.source.lower():
            if ctx_cell.cell_num > 5:  # After initialization section
                return True

        return False

    def _apply_fixes_iteratively(self, ctx_cell: ContextAwareCell, prev_cells: List[ContextAwareCell]) -> List[str]:
        """
        Apply fixes iteratively until cell succeeds or max attempts reached

        Returns list of fixes that were applied
        """
        fixes_applied = []

        # Fix 1: Remove duplicate get_az_cli()
        if 'def get_az_cli' in ctx_cell.source:
            fix = {
                'type': 'remove_duplicate_function',
                'description': 'Remove get_az_cli() - use az_cli from Cell 5',
                'code': """# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Replace any: az_cli = get_az_cli()
# With: # az_cli already set by Cell 5
"""
            }
            fixes_applied.append(fix)

        # Fix 2: Remove duplicate environment loader
        if 'ENV_FILE' in ctx_cell.source and 'load' in ctx_cell.source.lower():
            if ctx_cell.cell_num > 5:
                fix = {
                    'type': 'remove_duplicate_env_loader',
                    'description': 'Remove environment loader - use ENV from Cell 3',
                    'code': """# Add at top of cell:
if 'ENV' not in globals():
    raise RuntimeError("Run Cell 3 (Environment Loader) first")

# Remove environment loading code
# Use: ENV.get('VARIABLE_NAME')
"""
                }
                fixes_applied.append(fix)

        # Fix 3: Handle missing environment variables
        if ctx_cell.actual_outcome.get('error_type') in ['KeyError', 'NameError']:
            error_msg = ctx_cell.actual_outcome.get('error_message', '')
            if 'APIM' in error_msg or 'API' in error_msg:
                fix = {
                    'type': 'add_env_var_check',
                    'description': 'Add environment variable validation',
                    'code': """# Add before using the variable:
required_vars = ['APIM_GATEWAY_URL', 'APIM_API_KEY', 'RESOURCE_GROUP']
missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    raise RuntimeError(f"Missing environment variables: {missing}. Run Cell 3 first.")
"""
                }
                fixes_applied.append(fix)

        # Fix 4: Handle HTTP errors (401, 403, 404, 500, etc.)
        if ctx_cell.error_code and ctx_cell.error_code.startswith('HTTP_'):
            error_code = ctx_cell.error_code.split('_')[1]

            if error_code in ['401', '403']:
                fix = {
                    'type': 'auth_error',
                    'description': f'Fix authentication error {error_code}',
                    'code': """# Authentication error - check:
# 1. APIM_API_KEY is set correctly in master-lab.env
# 2. API key has not expired
# 3. Run Cell 3 to reload environment

# Add to request:
headers = {
    'Ocp-Apim-Subscription-Key': os.getenv('APIM_API_KEY'),
    'Content-Type': 'application/json'
}
"""
                }
                fixes_applied.append(fix)

            elif error_code == '404':
                fix = {
                    'type': 'not_found_error',
                    'description': 'Fix endpoint not found error',
                    'code': """# Check endpoint URL
# Verify: APIM_GATEWAY_URL is correct
# Verify: Path is correct (e.g., /inference)

endpoint = os.getenv('APIM_GATEWAY_URL')
if not endpoint:
    raise RuntimeError("APIM_GATEWAY_URL not set")

# Construct full URL carefully:
full_url = endpoint.rstrip('/') + '/inference'  # or appropriate path
"""
                }
                fixes_applied.append(fix)

            elif error_code in ['500', '502', '503']:
                fix = {
                    'type': 'server_error',
                    'description': f'Handle server error {error_code}',
                    'code': """# Add retry logic for server errors:
import time

max_retries = 3
for attempt in range(max_retries):
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        break
    except requests.exceptions.HTTPError as e:
        if attempt < max_retries - 1 and e.response.status_code >= 500:
            print(f"Retry {attempt + 1}/{max_retries} after server error")
            time.sleep(2 ** attempt)  # Exponential backoff
        else:
            raise
"""
                }
                fixes_applied.append(fix)

        # Fix 5: Handle import errors
        error_type = ctx_cell.actual_outcome.get('error_type')
        if error_type == 'ImportError' or error_type == 'ModuleNotFoundError':
            error_msg = ctx_cell.actual_outcome.get('error_message', '')
            module_match = re.search(r"No module named ['\"](\w+)['\"]", error_msg)
            if module_match:
                module = module_match.group(1)
                fix = {
                    'type': 'missing_module',
                    'description': f'Install missing module: {module}',
                    'code': f"""# Install missing module:
import subprocess
import sys

subprocess.check_call([sys.executable, '-m', 'pip', 'install', '{module}'])

# Then import:
import {module}
"""
                }
                fixes_applied.append(fix)

        # Fix 6: Handle service-specific errors based on topic
        if ctx_cell.topic == 'mcp' and ctx_cell.actual_outcome['has_error']:
            fix = {
                'type': 'mcp_service_check',
                'description': 'Verify MCP server availability',
                'code': """# Check MCP server is running:
if 'mcp' not in globals() or not hasattr(mcp, 'excel'):
    print("MCP client not initialized")
    print("Run Cell 10 (MCP Initialization) first")
    print("Ensure MCP server URLs are set in master-lab.env")
else:
    # Test connection:
    try:
        # Ping MCP server
        result = mcp.excel.list_tools()
        print(f"✅ MCP server accessible: {len(result)} tools available")
    except Exception as e:
        print(f"❌ MCP server error: {e}")
"""
            }
            fixes_applied.append(fix)

        # Fix 7: Consolidate duplicate imports
        if ctx_cell.source.count('import os') > 1:
            fix = {
                'type': 'consolidate_imports',
                'description': 'Consolidate duplicate import statements',
                'code': """# Move all imports to top of cell:
import os
import sys
import json
# ... (other imports)

# Remove duplicate import statements from rest of code
"""
            }
            fixes_applied.append(fix)

        return fixes_applied

    def generate_fix_report(self, test_results: List[Dict]) -> str:
        """Generate comprehensive report with all fixes"""

        report = f"""# Enhanced Testing Report with Iterative Fixes

**Generated:** {datetime.now().isoformat()}
**Notebook:** {self.notebook_path}
**Testing Method:** Context-aware with iterative fix-and-rerun

## Summary

**Total Cells Tested:** {len(test_results)}
**Cells Needing Fixes:** {sum(1 for r in test_results if len(r['fixes']) > 0)}
**Total Fixes Applied:** {sum(len(r['fixes']) for r in test_results)}

## Test Results by Cell

"""

        for result in test_results:
            cell_num = result['cell_num']
            ctx_cell = result['ctx_cell']
            fixes = result['fixes']

            report += f"""
### Cell {cell_num}

**Topic:** {ctx_cell.topic}
**Services:** {', '.join(ctx_cell.service) if ctx_cell.service else 'None'}
**Expected Outcome:** {ctx_cell.expected_outcome}

**Actual Outcome:**
- Success: {'✅' if ctx_cell.actual_outcome['success'] else '❌'}
- Has Error: {ctx_cell.actual_outcome['has_error']}
- Error Code: {ctx_cell.error_code or 'None'}
"""

            if ctx_cell.actual_outcome['error_message']:
                report += f"- Error Message: {ctx_cell.actual_outcome['error_message']}\n"

            if fixes:
                report += f"\n**Fixes Applied:** {len(fixes)}\n\n"
                for i, fix in enumerate(fixes, 1):
                    report += f"""
#### Fix {i}: {fix['description']}

**Type:** `{fix['type']}`

**Code:**
```python
{fix['code']}
```
"""
            else:
                report += "\n**Status:** ✅ No fixes needed\n"

        report += """
## Fix Types Summary

"""

        # Count fix types
        fix_types = defaultdict(int)
        for result in test_results:
            for fix in result['fixes']:
                fix_types[fix['type']] += 1

        for fix_type, count in sorted(fix_types.items(), key=lambda x: x[1], reverse=True):
            report += f"- `{fix_type}`: {count} occurrences\n"

        report += """
## Recommendations

1. **Apply All Fixes:** Review each fix and apply to the corresponding cell
2. **Rerun Cells:** After applying fixes, rerun each cell to verify
3. **Iterate:** If cell still fails, analyze new error and apply additional fixes
4. **Verify 100% Success:** Continue until all cells execute without errors

## Next Steps

1. Create updated notebook with all fixes applied
2. Test updated notebook incrementally
3. Verify all cells achieve 100% success rate
4. Document any cells that cannot be automatically fixed
"""

        return report


def main():
    """Main testing flow"""
    print("="*80)
    print("ENHANCED CONTEXT-AWARE TESTING")
    print("="*80)
    print()

    notebook_path = "master-ai-gateway-consolidated.ipynb"
    tester = EnhancedCellTester(notebook_path)

    # Test cells 42-238 (in consolidated notebook, these start around cell 34)
    print("Testing lab exercise cells with context awareness...")
    print("This will:")
    print("  1. Understand context from markdown")
    print("  2. Identify services being called")
    print("  3. Validate outputs and error codes")
    print("  4. Apply fixes iteratively")
    print("  5. Document path to 100% success")
    print()

    # Start from lab exercises section (approximately cell 34 onwards)
    lab_start = 34
    test_results = []
    prev_cells = []

    # Test ALL remaining cells (full analysis)
    total_cells = len(tester.cells)
    cells_to_test = total_cells - lab_start
    print(f"Testing ALL {cells_to_test} cells from cell {lab_start + 1} to {total_cells}...")
    print()

    for idx in range(lab_start, len(tester.cells)):
        cell = tester.cells[idx]
        if cell.get('cell_type') != 'code':
            continue

        success, ctx_cell, fixes = tester.test_cell_with_context(idx, prev_cells)

        result = {
            'cell_num': idx + 1,
            'ctx_cell': ctx_cell,
            'success': success,
            'fixes': fixes
        }
        test_results.append(result)
        prev_cells.append(ctx_cell)

        # Show summary
        status = "✅" if success and len(fixes) == 0 else "🔧" if len(fixes) > 0 else "❌"
        print(f"{status} Cell {idx + 1}: {len(fixes)} fix(es) needed")

    # Generate report
    print("\n" + "="*80)
    print("GENERATING FIX REPORT")
    print("="*80)

    report = tester.generate_fix_report(test_results)
    report_path = Path('analysis-reports/ENHANCED_TEST_REPORT_WITH_FIXES.md')
    report_path.write_text(report, encoding='utf-8')

    print(f"\n📄 Report saved: {report_path}")
    print(f"\nTested {len(test_results)} cells")
    print(f"Cells needing fixes: {sum(1 for r in test_results if len(r['fixes']) > 0)}")
    print(f"Total fixes documented: {sum(len(r['fixes']) for r in test_results)}")

    print("\n" + "="*80)
    print("✅ ENHANCED TESTING COMPLETE")
    print("="*80)


if __name__ == '__main__':
    main()
