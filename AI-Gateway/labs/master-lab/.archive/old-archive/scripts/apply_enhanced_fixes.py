#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apply all fixes identified by enhanced cell tester to create final consolidated notebook
"""
import json
import re
import sys

# Configure stdout for UTF-8 encoding (handles emojis on Windows)
if sys.platform == 'win32':
    import codecs
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    else:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

from pathlib import Path
from datetime import datetime
from typing import Dict, List

class FixApplicator:
    """Applies fixes to notebook cells"""

    def __init__(self, notebook_path: str):
        self.notebook_path = Path(notebook_path)
        with open(self.notebook_path, 'r', encoding='utf-8') as f:
            self.notebook = json.load(f)
        self.cells = self.notebook['cells']
        self.fixes_applied = []

    def apply_all_fixes(self):
        """Apply all identified fixes"""

        # Fixes identified by enhanced tester
        # Format: cell_num -> (fix_type, description)
        fixes_to_apply = {
            38: [('remove_duplicate_function', 'get_az_cli')],
            45: [('remove_duplicate_function', 'get_az_cli')],
            55: [('remove_duplicate_function', 'get_az_cli')],
            57: [('auth_error', 'HTTP_401')],
            64: [('remove_duplicate_function', 'get_az_cli')],
            75: [('mcp_service_check', None)],
            77: [('mcp_service_check', None)],
            79: [('mcp_service_check', None)],
            81: [('mcp_service_check', None)],
            88: [('mcp_service_check', None)],
            89: [('mcp_service_check', None)],
            92: [('mcp_service_check', None)],
            99: [('remove_duplicate_function', 'get_az_cli'), ('auth_error', 'HTTP_403')],
            102: [('add_env_var_check', 'NameError')],
            104: [('remove_duplicate_function', 'get_az_cli')],
            211: [('remove_duplicate_function', 'get_az_cli')],
            224: [('remove_duplicate_function', 'get_az_cli')],
        }

        print(f"Applying fixes to {len(fixes_to_apply)} cells...")
        print()

        for cell_num, fixes in sorted(fixes_to_apply.items()):
            cell_idx = cell_num - 1  # Convert to 0-indexed

            if cell_idx < 0 or cell_idx >= len(self.cells):
                print(f"⚠️  Cell {cell_num} out of range, skipping")
                continue

            cell = self.cells[cell_idx]

            if cell.get('cell_type') != 'code':
                print(f"⚠️  Cell {cell_num} is not a code cell, skipping")
                continue

            print(f"📝 Fixing Cell {cell_num}:")

            for fix_type, param in fixes:
                success = self._apply_fix(cell_idx, fix_type, param)
                if success:
                    print(f"   ✅ Applied {fix_type}")
                    self.fixes_applied.append({
                        'cell_num': cell_num,
                        'fix_type': fix_type,
                        'param': param
                    })
                else:
                    print(f"   ❌ Failed to apply {fix_type}")

            print()

        return len(self.fixes_applied)

    def _apply_fix(self, cell_idx: int, fix_type: str, param: any) -> bool:
        """Apply a specific fix to a cell"""

        cell = self.cells[cell_idx]
        source = self._get_source(cell)

        if fix_type == 'remove_duplicate_function':
            if param == 'get_az_cli':
                new_source = self._remove_get_az_cli(source)
                if new_source != source:
                    self._set_source(cell, new_source)
                    return True

        elif fix_type == 'mcp_service_check':
            new_source = self._add_mcp_service_check(source)
            if new_source != source:
                self._set_source(cell, new_source)
                return True

        elif fix_type == 'auth_error':
            new_source = self._fix_auth_error(source, param)
            if new_source != source:
                self._set_source(cell, new_source)
                return True

        elif fix_type == 'add_env_var_check':
            new_source = self._add_env_var_check(source)
            if new_source != source:
                self._set_source(cell, new_source)
                return True

        return False

    def _get_source(self, cell: Dict) -> str:
        """Get cell source as string"""
        source = cell.get('source', [])
        if isinstance(source, list):
            return ''.join(source)
        return source

    def _set_source(self, cell: Dict, new_source: str):
        """Set cell source"""
        cell['source'] = [new_source]

    def _remove_get_az_cli(self, source: str) -> str:
        """Remove get_az_cli() function definition and calls"""

        # Check if get_az_cli exists
        if 'def get_az_cli' not in source:
            return source

        # Add prerequisite check at top if not present
        prereq_check = """# Require Cell 5 (Azure CLI Setup) to have been run
if 'az_cli' not in globals():
    raise RuntimeError("❌ Run Cell 5 (Azure CLI Setup) first to set az_cli variable")

"""

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

        return new_source

    def _add_mcp_service_check(self, source: str) -> str:
        """Add MCP service availability check"""

        # Check if we're calling MCP client
        if 'mcp_client' not in source.lower():
            return source

        # Add check at top if not present
        check_code = """# Check MCP service availability
if 'mcp_client' not in globals():
    print("⚠️  MCP client not initialized. Run MCP initialization cells first.")
    raise RuntimeError("MCP client not available")

"""

        if 'mcp_client\' not in globals()' not in source:
            source = check_code + source

        return source

    def _fix_auth_error(self, source: str, error_code: str) -> str:
        """Add authentication error handling"""

        if error_code in ['HTTP_401', 'HTTP_403']:
            # Add header validation
            auth_check = """# Validate authentication headers
import os
headers = headers if 'headers' in locals() else {}
if 'Ocp-Apim-Subscription-Key' not in headers:
    api_key = os.getenv('APIM_API_KEY')
    if api_key:
        headers['Ocp-Apim-Subscription-Key'] = api_key
    else:
        print("⚠️  APIM_API_KEY not set in environment")

"""
            # Add before first request/post call
            if 'requests.' in source and 'Ocp-Apim-Subscription-Key' not in source:
                lines = source.split('\n')
                for i, line in enumerate(lines):
                    if 'requests.' in line and ('post' in line or 'get' in line):
                        lines.insert(i, auth_check)
                        break
                return '\n'.join(lines)

        return source

    def _add_env_var_check(self, source: str) -> str:
        """Add environment variable validation"""

        var_check = """# Validate required environment variables
required_vars = ['RESOURCE_GROUP', 'APIM_GATEWAY_URL']
missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    print(f"⚠️  Missing environment variables: {missing}")
    print("   Run Cell 3 (Environment Loader) first")
    raise RuntimeError(f"Missing variables: {missing}")

"""

        if 'required_vars' not in source:
            source = var_check + source

        return source

    def save(self, output_path: str):
        """Save fixed notebook"""

        output = Path(output_path)
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(self.notebook, f, indent=1)

        return str(output)

    def generate_changelog(self) -> str:
        """Generate changelog of applied fixes"""

        changelog = f"""# Fix Application Changelog

**Date:** {datetime.now().isoformat()}
**Source:** master-ai-gateway-consolidated.ipynb
**Output:** master-ai-gateway-final.ipynb

## Fixes Applied

**Total Fixes:** {len(self.fixes_applied)}

### By Cell

"""

        # Group by cell
        by_cell = {}
        for fix in self.fixes_applied:
            cell_num = fix['cell_num']
            if cell_num not in by_cell:
                by_cell[cell_num] = []
            by_cell[cell_num].append((fix['fix_type'], fix['param']))

        for cell_num in sorted(by_cell.keys()):
            changelog += f"**Cell {cell_num}:**\n"
            for fix_type, param in by_cell[cell_num]:
                if param:
                    changelog += f"- {fix_type} ({param})\n"
                else:
                    changelog += f"- {fix_type}\n"
            changelog += "\n"

        changelog += f"""
### By Fix Type

"""

        # Group by type
        by_type = {}
        for fix in self.fixes_applied:
            fix_type = fix['fix_type']
            if fix_type not in by_type:
                by_type[fix_type] = []
            by_type[fix_type].append(fix['cell_num'])

        for fix_type, cells in sorted(by_type.items()):
            changelog += f"**{fix_type}:** {len(cells)} occurrences\n"
            changelog += f"- Cells: {', '.join(map(str, cells))}\n\n"

        changelog += """
## Expected Impact

After applying these fixes:
- ✅ No more duplicate get_az_cli() functions
- ✅ MCP service availability validated before use
- ✅ Authentication headers properly configured
- ✅ Environment variables validated before use
- ✅ Cells can now run successfully

## Next Steps

1. Test the final notebook incrementally
2. Verify all cells execute without errors
3. Document any remaining issues
4. Achieve 100% success rate

"""

        return changelog


def main():
    print("="*80)
    print("APPLYING ENHANCED FIXES")
    print("="*80)
    print()

    # Load consolidated notebook
    applicator = FixApplicator('master-ai-gateway-consolidated.ipynb')

    # Apply all fixes
    num_fixes = applicator.apply_all_fixes()

    # Save final notebook
    output_path = applicator.save('master-ai-gateway-final.ipynb')

    print("="*80)
    print(f"✅ FIXES APPLIED: {num_fixes}")
    print("="*80)
    print(f"\nFinal notebook: {output_path}")

    # Generate changelog
    changelog = applicator.generate_changelog()
    changelog_path = Path('analysis-reports/FIX_APPLICATION_CHANGELOG.md')
    changelog_path.write_text(changelog, encoding='utf-8')
    print(f"Changelog: {changelog_path}")

    print("\nNext: Test the final notebook to verify 100% success")


if __name__ == '__main__':
    main()
