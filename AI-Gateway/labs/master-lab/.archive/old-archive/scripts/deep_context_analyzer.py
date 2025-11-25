#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deep Context-Aware Analyzer with Expected vs Actual Output Comparison

This analyzer:
1. Reads markdown context to understand section purpose
2. Predicts expected outcome based on context
3. Compares with actual output
4. Provides detailed reasoning and fix recommendations
5. Consolidates all fixes for review before application
"""
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from datetime import datetime

# Configure UTF-8 for Windows
if sys.platform == 'win32':
    import codecs
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    else:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


class DeepContextAnalyzer:
    """Deep analysis with expected vs actual comparison"""

    def __init__(self, notebook_path: str):
        self.notebook_path = Path(notebook_path)
        with open(self.notebook_path, 'r', encoding='utf-8') as f:
            self.notebook = json.load(f)
        self.cells = self.notebook['cells']
        self.analysis_results = []

    def analyze_all_cells(self, start_cell: int = 34, end_cell: int = None):
        """Analyze all cells with deep context awareness"""

        if end_cell is None:
            end_cell = len(self.cells)

        print(f"Analyzing cells {start_cell + 1} to {end_cell}...")
        print()

        # Track markdown context
        current_section = None
        current_markdown = ""
        section_cells = []

        for idx in range(start_cell, min(end_cell, len(self.cells))):
            cell = self.cells[idx]
            cell_num = idx + 1
            cell_type = cell.get('cell_type')

            # Track markdown cells for context
            if cell_type == 'markdown':
                source = self._get_source(cell)

                # Check if this starts a new section
                if self._is_section_header(source):
                    # Analyze previous section if exists
                    if current_section and section_cells:
                        self._analyze_section(current_section, current_markdown, section_cells)

                    # Start new section
                    current_section = self._extract_section_title(source)
                    current_markdown = source
                    section_cells = []
                else:
                    # Append to current section context
                    current_markdown += "\n\n" + source

            elif cell_type == 'code':
                # Add code cell to current section
                section_cells.append({
                    'cell_num': cell_num,
                    'cell': cell,
                    'index': idx
                })

        # Analyze final section
        if current_section and section_cells:
            self._analyze_section(current_section, current_markdown, section_cells)

        return self.analysis_results

    def _is_section_header(self, markdown: str) -> bool:
        """Check if markdown is a section header"""
        # Look for markdown headers (# Section, ## Section, etc.)
        lines = markdown.strip().split('\n')
        if not lines:
            return False
        first_line = lines[0].strip()
        return first_line.startswith('#') or 'section' in first_line.lower() or 'lab' in first_line.lower()

    def _extract_section_title(self, markdown: str) -> str:
        """Extract section title from markdown"""
        lines = markdown.strip().split('\n')
        if lines:
            first_line = lines[0].strip()
            # Remove markdown formatting
            return re.sub(r'^#+\s*', '', first_line)
        return "Unknown Section"

    def _analyze_section(self, section_title: str, markdown_context: str, code_cells: List[Dict]):
        """Analyze a complete section with all its code cells"""

        print("="*80)
        print(f"ANALYZING SECTION: {section_title}")
        print("="*80)
        print(f"Code cells in section: {len(code_cells)}")
        print()

        # Understand section purpose from markdown
        section_analysis = self._understand_section_purpose(section_title, markdown_context)

        print(f"📋 Section Purpose: {section_analysis['purpose']}")
        print(f"🎯 Expected Outcomes: {', '.join(section_analysis['expected_outcomes'])}")
        print(f"🔧 Services Involved: {', '.join(section_analysis['services'])}")
        print()

        # Analyze each code cell in this section
        for cell_info in code_cells:
            analysis = self._analyze_code_cell(
                cell_info['cell_num'],
                cell_info['cell'],
                section_title,
                section_analysis,
                markdown_context
            )
            self.analysis_results.append(analysis)

    def _understand_section_purpose(self, section_title: str, markdown: str) -> Dict:
        """Deep understanding of section purpose from markdown context"""

        markdown_lower = markdown.lower()
        title_lower = section_title.lower()

        # Initialize analysis
        analysis = {
            'section_title': section_title,
            'purpose': '',
            'expected_outcomes': [],
            'services': [],
            'prerequisites': [],
            'success_indicators': []
        }

        # Identify section type and purpose
        if 'section 0' in title_lower or 'deployment' in title_lower or 'infrastructure' in title_lower:
            analysis['purpose'] = 'Deploy Azure infrastructure using Bicep templates'
            analysis['expected_outcomes'] = [
                'Resource group created/verified',
                'APIM service deployed',
                'Azure OpenAI deployed',
                'Supporting services deployed',
                'All resources accessible'
            ]
            analysis['services'] = ['Azure CLI', 'Bicep', 'APIM', 'Azure OpenAI']
            analysis['prerequisites'] = ['Azure CLI authenticated', 'Environment variables set']
            analysis['success_indicators'] = ['✅', 'Successfully deployed', 'Deployment complete']

        elif 'section 1' in title_lower or 'load balanc' in markdown_lower or 'backend pool' in markdown_lower:
            analysis['purpose'] = 'Configure and test load balancing with backend pools'
            analysis['expected_outcomes'] = [
                'Backend pool configured in APIM',
                'Multiple backends added',
                'Round-robin distribution working',
                'Requests distributed evenly'
            ]
            analysis['services'] = ['APIM', 'Azure CLI']
            analysis['prerequisites'] = ['APIM deployed', 'API configured']
            analysis['success_indicators'] = ['Backend pool created', 'Load distribution confirmed']

        elif 'section 2' in title_lower or 'rate limit' in markdown_lower or 'throttl' in markdown_lower:
            analysis['purpose'] = 'Configure and test rate limiting policies'
            analysis['expected_outcomes'] = [
                'Rate limit policy applied',
                'Requests succeed under limit',
                'Requests rejected over limit',
                'HTTP 429 returned when throttled'
            ]
            analysis['services'] = ['APIM']
            analysis['prerequisites'] = ['APIM deployed', 'API configured']
            analysis['success_indicators'] = ['Rate limit applied', '429 Too Many Requests']

        elif 'section 3' in title_lower or 'content safety' in markdown_lower or 'moderation' in markdown_lower:
            analysis['purpose'] = 'Test content safety and moderation features'
            analysis['expected_outcomes'] = [
                'Safe content passes',
                'Unsafe content blocked',
                'Moderation filters active',
                'Appropriate error codes returned'
            ]
            analysis['services'] = ['Azure OpenAI', 'Content Safety']
            analysis['prerequisites'] = ['Azure OpenAI deployed', 'Content safety enabled']
            analysis['success_indicators'] = ['Content filtered', 'Safety check passed']

        elif 'section 4' in title_lower or 'semantic cach' in markdown_lower:
            analysis['purpose'] = 'Configure and test semantic caching'
            analysis['expected_outcomes'] = [
                'Cache configured',
                'First request cache miss',
                'Similar requests cache hit',
                'Response time improved'
            ]
            analysis['services'] = ['Redis', 'Azure OpenAI', 'APIM']
            analysis['prerequisites'] = ['Redis deployed', 'Cache policy configured']
            analysis['success_indicators'] = ['Cache hit', 'Cache miss', 'Semantic match']

        elif 'mcp' in title_lower or 'model context protocol' in markdown_lower:
            analysis['purpose'] = 'Initialize and test MCP servers and tools'
            analysis['expected_outcomes'] = [
                'MCP servers initialized',
                'Tools available',
                'Tool calls successful',
                'Expected data returned'
            ]
            analysis['services'] = ['MCP', 'Azure Search', 'Cosmos DB']
            analysis['prerequisites'] = ['MCP servers deployed', 'Client initialized']
            analysis['success_indicators'] = ['MCP server ready', 'Tool executed', 'Result returned']

        elif 'agent' in title_lower or 'agentic' in markdown_lower:
            analysis['purpose'] = 'Test agentic capabilities and tool usage'
            analysis['expected_outcomes'] = [
                'Agent receives task',
                'Agent selects appropriate tool',
                'Tool executes successfully',
                'Result returned to user'
            ]
            analysis['services'] = ['Azure OpenAI', 'MCP']
            analysis['prerequisites'] = ['MCP initialized', 'Tools configured']
            analysis['success_indicators'] = ['Agent response', 'Tool used', 'Task completed']

        elif 'test' in title_lower or 'verify' in title_lower or 'validation' in title_lower:
            analysis['purpose'] = 'Verify and test configured features'
            analysis['expected_outcomes'] = [
                'All tests pass',
                'Features work as expected',
                'No errors returned'
            ]
            analysis['services'] = ['APIM', 'Azure OpenAI']
            analysis['prerequisites'] = ['Services deployed', 'Configuration complete']
            analysis['success_indicators'] = ['✅', 'Test passed', 'Success']

        else:
            # Generic analysis
            analysis['purpose'] = f'Execute tasks for: {section_title}'
            analysis['expected_outcomes'] = ['Task completes successfully']
            analysis['services'] = self._detect_services(markdown)
            analysis['success_indicators'] = ['✅', 'Success', 'Complete']

        return analysis

    def _detect_services(self, text: str) -> List[str]:
        """Detect services mentioned in text"""
        text_lower = text.lower()
        services = []

        service_keywords = {
            'APIM': ['apim', 'api management', 'gateway'],
            'Azure OpenAI': ['azure openai', 'azureopenai', 'openai'],
            'Azure CLI': ['az cli', 'azure cli'],
            'MCP': ['mcp', 'model context protocol'],
            'Redis': ['redis', 'cache'],
            'Azure Search': ['azure search', 'cognitive search'],
            'Cosmos DB': ['cosmos', 'cosmosdb'],
            'Bicep': ['bicep', 'deployment']
        }

        for service, keywords in service_keywords.items():
            if any(kw in text_lower for kw in keywords):
                services.append(service)

        return services or ['General']

    def _analyze_code_cell(self, cell_num: int, cell: Dict, section_title: str,
                          section_analysis: Dict, markdown_context: str) -> Dict:
        """Deep analysis of a single code cell"""

        print(f"\n{'─'*80}")
        print(f"Cell {cell_num}: Analyzing...")

        source = self._get_source(cell)
        output = self._get_output(cell)

        # Predict expected outcome based on code and context
        expected = self._predict_expected_outcome(source, section_analysis)

        # Analyze actual outcome
        actual = self._analyze_actual_outcome(output, section_analysis)

        # Compare expected vs actual
        comparison = self._compare_outcomes(expected, actual, source, output)

        # Determine if fix is needed
        needs_fix = comparison['matches'] == False
        fix_recommendation = None

        if needs_fix:
            fix_recommendation = self._recommend_fix(
                cell_num, source, output, expected, actual, section_analysis, comparison
            )

        # Build analysis result
        analysis = {
            'cell_num': cell_num,
            'section': section_title,
            'source_preview': source[:200] + '...' if len(source) > 200 else source,
            'expected': expected,
            'actual': actual,
            'comparison': comparison,
            'needs_fix': needs_fix,
            'fix_recommendation': fix_recommendation,
            'reasoning': comparison['reasoning']
        }

        # Print summary
        status = "❌ NEEDS FIX" if needs_fix else "✅ MATCHES EXPECTED"
        print(f"   {status}")
        print(f"   Expected: {expected['summary']}")
        print(f"   Actual: {actual['summary']}")

        if needs_fix and fix_recommendation:
            print(f"   💡 Fix: {fix_recommendation['type']}")

        return analysis

    def _get_source(self, cell: Dict) -> str:
        """Get cell source as string"""
        source = cell.get('source', [])
        if isinstance(source, list):
            return ''.join(source)
        return source

    def _get_output(self, cell: Dict) -> str:
        """Get cell output as string"""
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
                ename = out.get('ename', 'Error')
                evalue = out.get('evalue', '')
                output_parts.append(f"ERROR: {ename}: {evalue}")

        return '\n'.join(output_parts)

    def _predict_expected_outcome(self, source: str, section_analysis: Dict) -> Dict:
        """Predict what the cell should do based on code and context"""

        expected = {
            'type': 'unknown',
            'summary': '',
            'indicators': [],
            'no_errors': True
        }

        source_lower = source.lower()

        # Analyze code to predict outcome
        if 'def get_az_cli' in source:
            expected['type'] = 'function_definition'
            expected['summary'] = 'Should NOT define get_az_cli() - use Cell 5 instead'
            expected['indicators'] = []
            expected['no_errors'] = True

        elif 'az deployment' in source_lower or 'bicep' in source_lower:
            expected['type'] = 'deployment'
            expected['summary'] = 'Azure resource deployment should succeed'
            expected['indicators'] = ['Successfully deployed', 'Deployment complete', '✅']
            expected['no_errors'] = True

        elif 'mcp_client' in source_lower and 'call_tool' in source_lower:
            expected['type'] = 'mcp_tool_call'
            expected['summary'] = 'MCP tool should execute and return results'
            expected['indicators'] = ['result', 'success', 'data']
            expected['no_errors'] = True

        elif 'requests.post' in source or 'requests.get' in source:
            expected['type'] = 'api_call'
            expected['summary'] = 'API call should succeed with valid response'
            expected['indicators'] = ['200', 'success', 'response']
            expected['no_errors'] = True

        elif 'policy' in source_lower and 'apply' in source_lower:
            expected['type'] = 'policy_application'
            expected['summary'] = 'Policy should be applied successfully'
            expected['indicators'] = ['Policy applied', 'Success', '✅']
            expected['no_errors'] = True

        elif 'print(' in source or 'display(' in source:
            expected['type'] = 'output_display'
            expected['summary'] = 'Should display information without errors'
            expected['indicators'] = section_analysis['success_indicators']
            expected['no_errors'] = True

        else:
            # Use section context
            expected['type'] = 'general'
            expected['summary'] = f"Should: {section_analysis['expected_outcomes'][0] if section_analysis['expected_outcomes'] else 'complete successfully'}"
            expected['indicators'] = section_analysis['success_indicators']
            expected['no_errors'] = True

        return expected

    def _analyze_actual_outcome(self, output: str, section_analysis: Dict) -> Dict:
        """Analyze what actually happened"""

        actual = {
            'type': 'unknown',
            'summary': '',
            'has_output': len(output) > 0,
            'has_error': False,
            'error_details': None,
            'success_indicators_found': []
        }

        if not output:
            actual['type'] = 'no_output'
            actual['summary'] = 'Cell has no output (may not have been executed)'
            return actual

        output_lower = output.lower()

        # Check for errors
        if 'ERROR:' in output or 'error:' in output_lower or 'exception' in output_lower:
            actual['has_error'] = True
            actual['type'] = 'error'

            # Extract error type
            error_match = re.search(r'ERROR:\s*(\w+(?:Error)?)', output)
            if error_match:
                actual['error_details'] = error_match.group(1)
                actual['summary'] = f'Error occurred: {actual["error_details"]}'
            else:
                actual['summary'] = 'Error occurred (type unknown)'

        # Check for HTTP errors
        elif any(code in output for code in ['401', '403', '404', '429', '500', '502', '503']):
            actual['has_error'] = True
            actual['type'] = 'http_error'

            http_match = re.search(r'\b(4\d{2}|5\d{2})\b', output)
            if http_match:
                actual['error_details'] = f'HTTP_{http_match.group(1)}'
                actual['summary'] = f'HTTP error: {http_match.group(1)}'

        # Check for success indicators
        else:
            found_indicators = []
            for indicator in section_analysis['success_indicators']:
                if indicator.lower() in output_lower:
                    found_indicators.append(indicator)

            actual['success_indicators_found'] = found_indicators

            if found_indicators:
                actual['type'] = 'success'
                actual['summary'] = f'Success - found indicators: {", ".join(found_indicators)}'
            else:
                actual['type'] = 'output_without_clear_status'
                actual['summary'] = 'Has output but unclear if successful'

        return actual

    def _compare_outcomes(self, expected: Dict, actual: Dict, source: str, output: str) -> Dict:
        """Compare expected vs actual and provide reasoning"""

        comparison = {
            'matches': False,
            'confidence': 'low',
            'reasoning': '',
            'discrepancies': []
        }

        # Case 1: Expected no errors, but got error
        if expected['no_errors'] and actual['has_error']:
            comparison['matches'] = False
            comparison['confidence'] = 'high'
            comparison['reasoning'] = f"Expected success but got {actual['type']}: {actual.get('error_details', 'unknown')}"
            comparison['discrepancies'].append('Error occurred when success expected')

        # Case 2: Expected function definition but found duplicate
        elif expected['type'] == 'function_definition' and 'def get_az_cli' in source:
            comparison['matches'] = False
            comparison['confidence'] = 'high'
            comparison['reasoning'] = 'Duplicate function definition found - should use Cell 5 instead'
            comparison['discrepancies'].append('Duplicate get_az_cli() function')

        # Case 3: No output when output expected
        elif expected['indicators'] and not actual['has_output']:
            comparison['matches'] = False
            comparison['confidence'] = 'medium'
            comparison['reasoning'] = 'No output - cell may not have been executed yet'
            comparison['discrepancies'].append('Missing output')

        # Case 4: Success indicators expected but not found
        elif expected['indicators'] and actual['has_output'] and not actual['has_error']:
            found = any(ind in output for ind in expected['indicators'])
            if found:
                comparison['matches'] = True
                comparison['confidence'] = 'high'
                comparison['reasoning'] = 'Output matches expected success indicators'
            else:
                comparison['matches'] = False
                comparison['confidence'] = 'medium'
                comparison['reasoning'] = f"Expected indicators ({', '.join(expected['indicators'])}) not found in output"
                comparison['discrepancies'].append('Success indicators missing')

        # Case 5: Success without errors
        elif actual['type'] == 'success' and expected['no_errors']:
            comparison['matches'] = True
            comparison['confidence'] = 'high'
            comparison['reasoning'] = 'Cell executed successfully with expected outcome'

        # Case 6: Output but unclear status
        elif actual['type'] == 'output_without_clear_status':
            comparison['matches'] = True
            comparison['confidence'] = 'medium'
            comparison['reasoning'] = 'Cell has output, assuming success (no errors detected)'

        # Case 7: No output yet
        elif actual['type'] == 'no_output':
            comparison['matches'] = True
            comparison['confidence'] = 'low'
            comparison['reasoning'] = 'Cell not executed yet - no comparison possible'

        else:
            comparison['matches'] = False
            comparison['confidence'] = 'low'
            comparison['reasoning'] = 'Unable to determine if outcome matches expected'

        return comparison

    def _recommend_fix(self, cell_num: int, source: str, output: str,
                      expected: Dict, actual: Dict, section_analysis: Dict,
                      comparison: Dict) -> Dict:
        """Recommend specific fix based on analysis"""

        fix = {
            'type': 'unknown',
            'description': '',
            'code': '',
            'priority': 'medium',
            'confidence': 'medium'
        }

        # Fix 1: Duplicate get_az_cli()
        if 'def get_az_cli' in source:
            fix['type'] = 'remove_duplicate_function'
            fix['description'] = 'Remove get_az_cli() function - use Cell 5 instead'
            fix['code'] = """# Add at top of cell:
if 'az_cli' not in globals():
    raise RuntimeError("❌ Run Cell 5 (Azure CLI Setup) first")

# Remove entire get_az_cli() function definition
# Remove any: az_cli = get_az_cli()"""
            fix['priority'] = 'high'
            fix['confidence'] = 'high'

        # Fix 2: HTTP authentication error
        elif actual.get('error_details') in ['HTTP_401', 'HTTP_403']:
            fix['type'] = 'fix_authentication'
            fix['description'] = f"Fix {actual['error_details']} authentication error"
            fix['code'] = """# Add before API call:
import os
headers = headers if 'headers' in locals() else {}
if 'Ocp-Apim-Subscription-Key' not in headers:
    api_key = os.getenv('APIM_API_KEY')
    if api_key:
        headers['Ocp-Apim-Subscription-Key'] = api_key
    else:
        raise RuntimeError("APIM_API_KEY not set in environment")"""
            fix['priority'] = 'high'
            fix['confidence'] = 'high'

        # Fix 3: MCP client not available
        elif 'mcp_client' in source and actual['has_error']:
            fix['type'] = 'add_mcp_check'
            fix['description'] = 'Add MCP service availability check'
            fix['code'] = """# Add at top of cell:
if 'mcp_client' not in globals():
    print("⚠️  MCP client not initialized. Run MCP initialization cells first.")
    raise RuntimeError("MCP client not available")"""
            fix['priority'] = 'high'
            fix['confidence'] = 'high'

        # Fix 4: Missing environment variables
        elif actual.get('error_details') in ['NameError', 'KeyError']:
            fix['type'] = 'add_env_var_check'
            fix['description'] = 'Add environment variable validation'
            fix['code'] = """# Add at top of cell:
import os
required_vars = ['RESOURCE_GROUP', 'APIM_GATEWAY_URL']  # Adjust as needed
missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    print(f"⚠️  Missing: {missing}. Run Cell 3 (Environment Loader) first")
    raise RuntimeError(f"Missing environment variables: {missing}")"""
            fix['priority'] = 'high'
            fix['confidence'] = 'high'

        # Fix 5: HTTP 404 - endpoint not found
        elif actual.get('error_details') == 'HTTP_404':
            fix['type'] = 'fix_endpoint'
            fix['description'] = 'Fix endpoint URL (404 Not Found)'
            fix['code'] = """# Check endpoint URL:
# - Verify API is deployed
# - Check path is correct
# - Ensure APIM gateway URL is correct
print(f"Endpoint: {url}")  # Add debugging"""
            fix['priority'] = 'medium'
            fix['confidence'] = 'medium'

        # Fix 6: HTTP 500/502/503 - server error
        elif actual.get('error_details') in ['HTTP_500', 'HTTP_502', 'HTTP_503']:
            fix['type'] = 'add_retry_logic'
            fix['description'] = f'Add retry logic for {actual["error_details"]} server error'
            fix['code'] = """# Add retry with exponential backoff:
import time
for attempt in range(3):
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        break
    except requests.exceptions.HTTPError as e:
        if attempt < 2 and e.response.status_code >= 500:
            wait_time = 2 ** attempt
            print(f"Retry {attempt + 1}/3 after {wait_time}s...")
            time.sleep(wait_time)
        else:
            raise"""
            fix['priority'] = 'medium'
            fix['confidence'] = 'medium'

        else:
            # Generic fix suggestion
            fix['type'] = 'manual_investigation'
            fix['description'] = 'Requires manual investigation'
            fix['code'] = f"""# Analysis:
# Expected: {expected['summary']}
# Actual: {actual['summary']}
# Discrepancies: {', '.join(comparison['discrepancies'])}
# Recommendation: Review cell code and output, apply targeted fix"""
            fix['priority'] = 'medium'
            fix['confidence'] = 'low'

        return fix

    def generate_comprehensive_report(self) -> str:
        """Generate comprehensive expected vs actual comparison report"""

        report = f"""# Deep Context-Aware Analysis Report

**Generated:** {datetime.now().isoformat()}
**Notebook:** {self.notebook_path.name}
**Analysis Type:** Expected vs Actual Output Comparison with Deep Context Understanding

---

## Executive Summary

**Total Cells Analyzed:** {len(self.analysis_results)}
**Cells Needing Fixes:** {sum(1 for r in self.analysis_results if r['needs_fix'])}
**Cells Matching Expected:** {sum(1 for r in self.analysis_results if not r['needs_fix'])}

### Fix Priority Breakdown
"""

        # Count by priority
        high_priority = sum(1 for r in self.analysis_results
                          if r['needs_fix'] and r['fix_recommendation']
                          and r['fix_recommendation']['priority'] == 'high')
        medium_priority = sum(1 for r in self.analysis_results
                            if r['needs_fix'] and r['fix_recommendation']
                            and r['fix_recommendation']['priority'] == 'medium')

        report += f"""
- **HIGH Priority:** {high_priority} cells (critical issues blocking functionality)
- **MEDIUM Priority:** {medium_priority} cells (improvements recommended)
- **Total Fixes Needed:** {sum(1 for r in self.analysis_results if r['needs_fix'])}

---

## Cell-by-Cell Analysis

"""

        current_section = None
        for analysis in self.analysis_results:
            # Section header
            if analysis['section'] != current_section:
                current_section = analysis['section']
                report += f"\n## 📂 {current_section}\n\n"

            # Cell analysis
            status = "❌ NEEDS FIX" if analysis['needs_fix'] else "✅ MATCHES EXPECTED"
            report += f"### Cell {analysis['cell_num']} {status}\n\n"

            report += f"**Source Preview:**\n```python\n{analysis['source_preview']}\n```\n\n"

            report += f"#### Expected Outcome\n"
            report += f"- **Type:** {analysis['expected']['type']}\n"
            report += f"- **Summary:** {analysis['expected']['summary']}\n"
            if analysis['expected']['indicators']:
                report += f"- **Success Indicators:** {', '.join(analysis['expected']['indicators'])}\n"
            report += f"- **Should Have Errors:** {'No' if analysis['expected']['no_errors'] else 'Yes'}\n\n"

            report += f"#### Actual Outcome\n"
            report += f"- **Type:** {analysis['actual']['type']}\n"
            report += f"- **Summary:** {analysis['actual']['summary']}\n"
            report += f"- **Has Output:** {'Yes' if analysis['actual']['has_output'] else 'No'}\n"
            report += f"- **Has Error:** {'Yes' if analysis['actual']['has_error'] else 'No'}\n"
            if analysis['actual'].get('error_details'):
                report += f"- **Error Details:** {analysis['actual']['error_details']}\n"
            if analysis['actual'].get('success_indicators_found'):
                report += f"- **Indicators Found:** {', '.join(analysis['actual']['success_indicators_found'])}\n"
            report += "\n"

            report += f"#### Comparison\n"
            report += f"- **Matches Expected:** {'✅ Yes' if analysis['comparison']['matches'] else '❌ No'}\n"
            report += f"- **Confidence:** {analysis['comparison']['confidence'].upper()}\n"
            report += f"- **Reasoning:** {analysis['reasoning']}\n"
            if analysis['comparison']['discrepancies']:
                report += f"- **Discrepancies:** {', '.join(analysis['comparison']['discrepancies'])}\n"
            report += "\n"

            if analysis['needs_fix'] and analysis['fix_recommendation']:
                fix = analysis['fix_recommendation']
                report += f"#### 💡 Recommended Fix\n"
                report += f"- **Type:** `{fix['type']}`\n"
                report += f"- **Priority:** {fix['priority'].upper()}\n"
                report += f"- **Confidence:** {fix['confidence'].upper()}\n"
                report += f"- **Description:** {fix['description']}\n\n"
                report += f"**Fix Code:**\n```python\n{fix['code']}\n```\n\n"

            report += "---\n\n"

        # Consolidated fixes section
        report += self._generate_consolidated_fixes_section()

        return report

    def _generate_consolidated_fixes_section(self) -> str:
        """Generate consolidated fixes section"""

        section = """
## 🔧 Consolidated Fixes

This section consolidates all recommended fixes for easy application.

### High Priority Fixes (Apply First)

"""

        high_priority_fixes = [
            (r['cell_num'], r['fix_recommendation'])
            for r in self.analysis_results
            if r['needs_fix'] and r['fix_recommendation']
            and r['fix_recommendation']['priority'] == 'high'
        ]

        if high_priority_fixes:
            for cell_num, fix in sorted(high_priority_fixes):
                section += f"#### Cell {cell_num}: {fix['description']}\n"
                section += f"```python\n{fix['code']}\n```\n\n"
        else:
            section += "*No high priority fixes needed.*\n\n"

        section += "### Medium Priority Fixes\n\n"

        medium_priority_fixes = [
            (r['cell_num'], r['fix_recommendation'])
            for r in self.analysis_results
            if r['needs_fix'] and r['fix_recommendation']
            and r['fix_recommendation']['priority'] == 'medium'
        ]

        if medium_priority_fixes:
            for cell_num, fix in sorted(medium_priority_fixes):
                section += f"#### Cell {cell_num}: {fix['description']}\n"
                section += f"```python\n{fix['code']}\n```\n\n"
        else:
            section += "*No medium priority fixes needed.*\n\n"

        # Summary of all fixes by type
        section += "### Fixes by Type\n\n"

        fixes_by_type = defaultdict(list)
        for r in self.analysis_results:
            if r['needs_fix'] and r['fix_recommendation']:
                fixes_by_type[r['fix_recommendation']['type']].append(r['cell_num'])

        for fix_type, cells in sorted(fixes_by_type.items()):
            section += f"- **{fix_type}:** {len(cells)} cells ({', '.join(map(str, cells))})\n"

        section += "\n---\n\n"

        return section


def main():
    print("="*80)
    print("DEEP CONTEXT-AWARE ANALYSIS")
    print("Expected vs Actual Output Comparison")
    print("="*80)
    print()

    # Analyze consolidated notebook
    analyzer = DeepContextAnalyzer('master-ai-gateway-consolidated.ipynb')

    print("Starting deep analysis with context awareness...")
    print("This will:")
    print("  1. Read markdown context for each section")
    print("  2. Understand section purpose and goals")
    print("  3. Predict expected outcome for each cell")
    print("  4. Compare with actual output")
    print("  5. Provide detailed reasoning")
    print("  6. Recommend fixes with code")
    print()

    # Analyze cells (starting from lab exercises)
    results = analyzer.analyze_all_cells(start_cell=34, end_cell=None)

    # Generate comprehensive report
    print("\n" + "="*80)
    print("GENERATING COMPREHENSIVE REPORT")
    print("="*80)

    report = analyzer.generate_comprehensive_report()
    report_path = Path('analysis-reports/DEEP_CONTEXT_ANALYSIS_REPORT.md')
    report_path.write_text(report, encoding='utf-8')

    print(f"\n✅ Report generated: {report_path}")
    print(f"\nAnalyzed: {len(results)} cells")
    print(f"Needs fixes: {sum(1 for r in results if r['needs_fix'])}")
    print(f"Matches expected: {sum(1 for r in results if not r['needs_fix'])}")

    print("\n" + "="*80)
    print("✅ DEEP ANALYSIS COMPLETE")
    print("="*80)
    print("\nNext: Review report and approve fixes before application")


if __name__ == '__main__':
    main()
