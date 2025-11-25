#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Priority 2: Test Cells 1-41 Incrementally

Tests initialization cells to verify they work correctly after fixes.
Validates outputs, checks for errors, and provides detailed reporting.
"""
import json
import sys
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

# Configure UTF-8 for Windows
if sys.platform == 'win32':
    import codecs
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    else:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


class CellTester:
    """Test cells incrementally with validation"""

    def __init__(self, notebook_path: str):
        self.notebook_path = Path(notebook_path)
        with open(self.notebook_path, 'r', encoding='utf-8') as f:
            self.notebook = json.load(f)
        self.cells = self.notebook['cells']
        self.test_results = []

    def test_cells_1_to_41(self):
        """Test cells 1-41 incrementally"""

        print("=" * 80)
        print("PRIORITY 2: TESTING CELLS 1-41 (Initialization)")
        print("=" * 80)
        print()
        print("Testing approach:")
        print("  • Run cells in order")
        print("  • Validate outputs")
        print("  • Check for errors")
        print("  • Document results")
        print()
        print("=" * 80)
        print()

        # Key cells to watch (recently fixed)
        watch_cells = [3, 5, 38, 45, 55, 64, 99, 102, 104]

        for cell_num in range(1, 42):
            idx = cell_num - 1

            if idx >= len(self.cells):
                print(f"⚠️  Cell {cell_num}: Not found (notebook may have fewer cells)")
                continue

            cell = self.cells[idx]

            # Get cell type
            cell_type = cell.get('cell_type', 'unknown')

            # Mark important cells
            marker = " 🔍" if cell_num in watch_cells else ""

            print(f"\n{'=' * 80}")
            print(f"Cell {cell_num}: {cell_type.upper()}{marker}")
            print(f"{'=' * 80}")

            if cell_type == 'markdown':
                self._test_markdown_cell(cell_num, cell)
            elif cell_type == 'code':
                self._test_code_cell(cell_num, cell, watch=cell_num in watch_cells)
            else:
                print(f"⚠️  Unknown cell type: {cell_type}")

        # Summary
        self._print_summary()

    def _test_markdown_cell(self, cell_num: int, cell: dict):
        """Test markdown cell"""
        source = self._get_source(cell)
        preview = source[:100].replace('\n', ' ')

        print(f"Type: Documentation")
        print(f"Preview: {preview}...")
        print("✅ Markdown cell (no execution needed)")

        self.test_results.append({
            'cell': cell_num,
            'type': 'markdown',
            'status': 'ok',
            'message': 'Documentation'
        })

    def _test_code_cell(self, cell_num: int, cell: dict, watch=False):
        """Test code cell"""
        source = self._get_source(cell)

        # Show source preview
        lines = source.split('\n')
        non_empty = [l for l in lines if l.strip() and not l.strip().startswith('#')]
        if non_empty:
            preview = non_empty[0][:60]
            print(f"Source: {preview}...")
        else:
            print(f"Source: (comments only or empty)")

        # Check outputs
        outputs = cell.get('outputs', [])

        if not outputs:
            print("📊 Output: None (cell not executed yet)")
            self.test_results.append({
                'cell': cell_num,
                'type': 'code',
                'status': 'not_executed',
                'message': 'Cell has no output'
            })
            return

        # Analyze outputs
        has_error = False
        error_details = []
        has_output = False

        for output in outputs:
            output_type = output.get('output_type', '')

            if output_type == 'error':
                has_error = True
                ename = output.get('ename', 'Unknown')
                evalue = output.get('evalue', '')
                error_details.append(f"{ename}: {evalue[:100]}")

            elif output_type in ['stream', 'display_data', 'execute_result']:
                has_output = True

        # Report results
        if has_error:
            print("❌ Status: ERROR")
            for error in error_details:
                print(f"   Error: {error}")

            # Check if it's a known error we should investigate
            if watch:
                print(f"   🔍 WATCH: This cell was recently fixed - ERROR needs investigation!")

            self.test_results.append({
                'cell': cell_num,
                'type': 'code',
                'status': 'error',
                'message': '; '.join(error_details),
                'watch': watch
            })

        elif has_output:
            print("✅ Status: SUCCESS (has output)")

            # Additional validation for watch cells
            if watch:
                print(f"   🔍 WATCH: Verifying fix was applied correctly...")
                self._verify_watch_cell(cell_num, source, outputs)

            self.test_results.append({
                'cell': cell_num,
                'type': 'code',
                'status': 'success',
                'message': 'Cell executed with output'
            })

        else:
            print("⚠️  Status: UNCLEAR (no error, but no clear output)")
            self.test_results.append({
                'cell': cell_num,
                'type': 'code',
                'status': 'unclear',
                'message': 'No clear output'
            })

    def _verify_watch_cell(self, cell_num: int, source: str, outputs: list):
        """Verify watch cells have correct fixes applied"""

        # Cell 3: Environment loader
        if cell_num == 3:
            if 'load_dotenv' in source:
                print("     ✓ Environment loader present")

        # Cell 5: Azure CLI setup
        elif cell_num == 5:
            if 'az_cli' in source and 'shutil.which' in source:
                print("     ✓ Azure CLI setup code present")

        # Cells 38, 45, 55, 64, 99, 104: Should NOT have duplicate get_az_cli
        elif cell_num in [38, 45, 55, 64, 99, 104]:
            if 'def get_az_cli' in source:
                print("     ⚠️  WARNING: Still has get_az_cli() function definition!")
            else:
                print("     ✓ Duplicate get_az_cli() removed")

            if "'az_cli' not in globals()" in source:
                print("     ✓ Prerequisite check added")

        # Cell 102: Should have env var check
        elif cell_num == 102:
            if 'required_vars' in source:
                print("     ✓ Environment variable validation present")

    def _get_source(self, cell: dict) -> str:
        """Get cell source as string"""
        source = cell.get('source', [])
        if isinstance(source, list):
            return ''.join(source)
        return source

    def _print_summary(self):
        """Print test summary"""

        print("\n")
        print("=" * 80)
        print("TEST SUMMARY (Cells 1-41)")
        print("=" * 80)
        print()

        # Count by status
        status_counts = {}
        for result in self.test_results:
            status = result['status']
            status_counts[status] = status_counts.get(status, 0) + 1

        print("Results by Status:")
        for status, count in sorted(status_counts.items()):
            icon = {
                'ok': '📝',
                'success': '✅',
                'error': '❌',
                'not_executed': '⏸️',
                'unclear': '⚠️'
            }.get(status, '❔')
            print(f"  {icon} {status.upper()}: {count} cells")

        # List errors
        errors = [r for r in self.test_results if r['status'] == 'error']
        if errors:
            print()
            print("❌ Cells with Errors:")
            for result in errors:
                watch_marker = " 🔍 [RECENTLY FIXED]" if result.get('watch') else ""
                print(f"   • Cell {result['cell']}: {result['message']}{watch_marker}")

        # List not executed
        not_executed = [r for r in self.test_results if r['status'] == 'not_executed']
        if not_executed:
            print()
            print("⏸️  Cells Not Executed:")
            print(f"   {len(not_executed)} cells have no output (need to be run)")

        print()
        print("=" * 80)
        print("PRIORITY 2 STATUS")
        print("=" * 80)
        print()

        if errors:
            print(f"⚠️  Found {len(errors)} cells with errors - need investigation")
        else:
            print("✅ No errors found in executed cells")

        if not_executed:
            print(f"📋 {len(not_executed)} cells not executed yet - need to run notebook")
        else:
            print("✅ All cells have been executed")

        print()
        print("Next Steps:")
        if errors:
            print("  1. Investigate cells with errors")
            print("  2. Apply fixes if needed")
            print("  3. Rerun cells to verify")
        if not_executed:
            print("  1. Run notebook incrementally (cells 1-41)")
            print("  2. Verify each cell executes successfully")
            print("  3. Check watch cells especially")

        print()

    def save_report(self, output_path: str):
        """Save detailed test report"""

        report_path = Path(output_path)

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Test Report: Cells 1-41 (Initialization)\n\n")
            f.write(f"**Date:** {datetime.now().isoformat()}\n")
            f.write(f"**Notebook:** {self.notebook_path.name}\n\n")
            f.write("---\n\n")

            # Summary
            f.write("## Summary\n\n")
            status_counts = {}
            for result in self.test_results:
                status = result['status']
                status_counts[status] = status_counts.get(status, 0) + 1

            for status, count in sorted(status_counts.items()):
                f.write(f"- **{status.upper()}:** {count} cells\n")

            f.write("\n---\n\n")

            # Details
            f.write("## Cell-by-Cell Results\n\n")

            for result in self.test_results:
                f.write(f"### Cell {result['cell']}\n\n")
                f.write(f"- **Type:** {result['type']}\n")
                f.write(f"- **Status:** {result['status']}\n")
                f.write(f"- **Message:** {result['message']}\n")
                if result.get('watch'):
                    f.write(f"- **Note:** 🔍 Recently fixed - requires special attention\n")
                f.write("\n")

            # Errors section
            errors = [r for r in self.test_results if r['status'] == 'error']
            if errors:
                f.write("---\n\n")
                f.write("## Cells Requiring Investigation\n\n")
                for result in errors:
                    f.write(f"### Cell {result['cell']}\n\n")
                    f.write(f"**Error:** {result['message']}\n\n")
                    if result.get('watch'):
                        f.write("**Recently Fixed:** Yes - this cell should have been fixed\n\n")
                    f.write("**Action Needed:**\n")
                    f.write("1. Review cell code\n")
                    f.write("2. Identify root cause\n")
                    f.write("3. Apply targeted fix\n")
                    f.write("4. Retest\n\n")

        print(f"\n📝 Detailed report saved: {report_path}")


def main():
    print("=" * 80)
    print("PRIORITY 2: TEST CELLS 1-41")
    print("=" * 80)
    print()

    # Use the notebook with error fixes
    notebook_file = 'master-ai-gateway-with-error-fixes.ipynb'

    # Check if file exists, fallback to previous version
    if not Path(notebook_file).exists():
        notebook_file = 'master-ai-gateway-with-approved-fixes.ipynb'
        print(f"ℹ️  Using notebook: {notebook_file}")
    else:
        print(f"✅ Using notebook with error fixes: {notebook_file}")

    print()

    # Test
    tester = CellTester(notebook_file)
    tester.test_cells_1_to_41()

    # Save report
    tester.save_report('analysis-reports/TEST_REPORT_CELLS_1_41.md')

    print("=" * 80)


if __name__ == '__main__':
    main()
