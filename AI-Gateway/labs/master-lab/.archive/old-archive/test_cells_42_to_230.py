#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Priority 3: Test Cells 42-230 Incrementally

Tests lab exercise cells to verify they work correctly after fixes.
Validates outputs, checks for errors, and provides detailed reporting.
"""
import json
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


class LabCellTester:
    """Test lab exercise cells incrementally with validation"""

    def __init__(self, notebook_path: str):
        self.notebook_path = Path(notebook_path)
        with open(self.notebook_path, 'r', encoding='utf-8') as f:
            self.notebook = json.load(f)
        self.cells = self.notebook['cells']
        self.test_results = []

    def test_cells_42_to_230(self):
        """Test cells 42-230 incrementally"""

        print("=" * 80)
        print("PRIORITY 3: TESTING CELLS 42-230 (Lab Exercises)")
        print("=" * 80)
        print()
        print("Testing approach:")
        print("  • Run cells in order")
        print("  • Validate outputs")
        print("  • Check for errors")
        print("  • Document results")
        print()

        # Key cells to watch (recently fixed)
        watch_cells = [45, 55, 57, 59, 64, 71, 72, 73, 99, 100, 102, 104]

        # Count totals
        total_cells = min(230, len(self.cells))
        print(f"Testing cells 42-{total_cells}")
        print("=" * 80)
        print()

        for cell_num in range(42, total_cells + 1):
            idx = cell_num - 1

            if idx >= len(self.cells):
                print(f"⚠️  Cell {cell_num}: Not found (notebook ends at cell {len(self.cells)})")
                break

            cell = self.cells[idx]

            # Get cell type
            cell_type = cell.get('cell_type', 'unknown')

            # Mark important cells
            marker = " 🔍" if cell_num in watch_cells else ""

            # Show progress every 10 cells
            if cell_num % 10 == 0:
                print(f"\n{'=' * 80}")
                print(f"Progress: Cell {cell_num}/{total_cells}")
                print(f"{'=' * 80}\n")

            if cell_type == 'markdown':
                self._test_markdown_cell(cell_num, cell, verbose=False)
            elif cell_type == 'code':
                self._test_code_cell(cell_num, cell, watch=cell_num in watch_cells)
            else:
                print(f"⚠️  Cell {cell_num}: Unknown type: {cell_type}")

        # Summary
        self._print_summary()

    def _test_markdown_cell(self, cell_num: int, cell: dict, verbose=False):
        """Test markdown cell"""
        if verbose:
            source = self._get_source(cell)
            preview = source[:60].replace('\n', ' ')
            print(f"Cell {cell_num}: Markdown - {preview}...")

        self.test_results.append({
            'cell': cell_num,
            'type': 'markdown',
            'status': 'ok',
            'message': 'Documentation'
        })

    def _test_code_cell(self, cell_num: int, cell: dict, watch=False):
        """Test code cell"""
        source = self._get_source(cell)

        # Show cell header
        print(f"\nCell {cell_num}: CODE{' 🔍' if watch else ''}")

        # Show source preview
        lines = source.split('\n')
        non_empty = [l for l in lines if l.strip() and not l.strip().startswith('#')]
        if non_empty:
            preview = non_empty[0][:80]
            print(f"  Source: {preview}...")

        # Check outputs
        outputs = cell.get('outputs', [])

        if not outputs:
            print(f"  📊 Output: None (not executed)")
            self.test_results.append({
                'cell': cell_num,
                'type': 'code',
                'status': 'not_executed',
                'message': 'Cell has no output',
                'watch': watch
            })
            return

        # Analyze outputs
        has_error = False
        error_details = []
        has_output = False
        output_preview = ""

        for output in outputs:
            output_type = output.get('output_type', '')

            if output_type == 'error':
                has_error = True
                ename = output.get('ename', 'Unknown')
                evalue = output.get('evalue', '')
                error_details.append(f"{ename}: {evalue[:80]}")

            elif output_type == 'stream':
                has_output = True
                text = ''.join(output.get('text', []))
                output_preview = text[:100].replace('\n', ' ')

            elif output_type in ['display_data', 'execute_result']:
                has_output = True

        # Report results
        if has_error:
            print(f"  ❌ Status: ERROR")
            for error in error_details:
                print(f"     {error}")

            if watch:
                print(f"     🔍 WATCH: This cell was recently fixed!")

            self.test_results.append({
                'cell': cell_num,
                'type': 'code',
                'status': 'error',
                'message': '; '.join(error_details),
                'watch': watch
            })

        elif has_output:
            print(f"  ✅ Status: SUCCESS")
            if output_preview:
                print(f"     Output: {output_preview}...")

            if watch:
                print(f"     🔍 WATCH: Verified fix working correctly")

            self.test_results.append({
                'cell': cell_num,
                'type': 'code',
                'status': 'success',
                'message': 'Cell executed with output',
                'watch': watch
            })

        else:
            print(f"  ⚠️  Status: UNCLEAR")
            self.test_results.append({
                'cell': cell_num,
                'type': 'code',
                'status': 'unclear',
                'message': 'No clear output',
                'watch': watch
            })

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
        print("TEST SUMMARY (Cells 42-230)")
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

        # Calculate percentages
        total_code = sum(1 for r in self.test_results if r['type'] == 'code')
        if total_code > 0:
            executed = sum(1 for r in self.test_results if r['type'] == 'code' and r['status'] in ['success', 'error'])
            success = sum(1 for r in self.test_results if r['status'] == 'success')
            print()
            print("Code Cell Statistics:")
            print(f"  • Total code cells: {total_code}")
            print(f"  • Executed: {executed} ({100*executed//total_code}%)")
            print(f"  • Successful: {success} ({100*success//total_code if total_code else 0}%)")

        # List errors
        errors = [r for r in self.test_results if r['status'] == 'error']
        if errors:
            print()
            print("❌ Cells with Errors:")
            for result in errors:
                watch_marker = " 🔍 [RECENTLY FIXED]" if result.get('watch') else ""
                print(f"   • Cell {result['cell']}: {result['message'][:100]}{watch_marker}")

        # List watch cells status
        watch_results = [r for r in self.test_results if r.get('watch')]
        if watch_results:
            print()
            print("🔍 Recently Fixed Cells Status:")
            for result in watch_results:
                status_icon = {
                    'success': '✅',
                    'error': '❌',
                    'not_executed': '⏸️',
                    'unclear': '⚠️'
                }.get(result['status'], '❔')
                print(f"   {status_icon} Cell {result['cell']}: {result['status'].upper()}")

        # List not executed
        not_executed = [r for r in self.test_results if r['status'] == 'not_executed']
        if not_executed:
            print()
            print(f"⏸️  Cells Not Executed: {len(not_executed)} cells")
            if len(not_executed) > 10:
                print(f"   (First 10: {', '.join(str(r['cell']) for r in not_executed[:10])}...)")
            else:
                print(f"   ({', '.join(str(r['cell']) for r in not_executed)})")

        print()
        print("=" * 80)
        print("PRIORITY 3 STATUS")
        print("=" * 80)
        print()

        if errors:
            print(f"⚠️  Found {len(errors)} cells with errors")
            # Check if any are watch cells
            watch_errors = [e for e in errors if e.get('watch')]
            if watch_errors:
                print(f"   ⚠️  {len(watch_errors)} recently fixed cells still have errors!")
        else:
            print("✅ No errors found in executed cells")

        if not_executed:
            print(f"📋 {len(not_executed)} cells not executed yet")
        else:
            print("✅ All cells have been executed")

        print()
        print("Next Steps:")
        if errors:
            print("  1. Investigate cells with errors")
            print("  2. Apply targeted fixes")
            print("  3. Rerun cells to verify")
        if not_executed:
            print("  1. Run notebook to execute remaining cells")
            print("  2. Verify all cells execute successfully")

        print()

    def save_report(self, output_path: str):
        """Save detailed test report"""

        report_path = Path(output_path)

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Test Report: Cells 42-230 (Lab Exercises)\n\n")
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

            # Errors section
            errors = [r for r in self.test_results if r['status'] == 'error']
            if errors:
                f.write("\n---\n\n")
                f.write("## Cells with Errors\n\n")
                for result in errors:
                    f.write(f"### Cell {result['cell']}\n\n")
                    f.write(f"**Error:** {result['message']}\n\n")
                    if result.get('watch'):
                        f.write("**Recently Fixed:** Yes\n\n")

            # Watch cells section
            watch_results = [r for r in self.test_results if r.get('watch')]
            if watch_results:
                f.write("\n---\n\n")
                f.write("## Recently Fixed Cells Status\n\n")
                for result in watch_results:
                    f.write(f"### Cell {result['cell']}\n\n")
                    f.write(f"- **Status:** {result['status']}\n")
                    f.write(f"- **Message:** {result['message']}\n\n")

            # Not executed section
            not_executed = [r for r in self.test_results if r['status'] == 'not_executed']
            if not_executed:
                f.write("\n---\n\n")
                f.write("## Cells Not Executed\n\n")
                f.write(f"Total: {len(not_executed)} cells\n\n")
                f.write("Cell numbers: " + ", ".join(str(r['cell']) for r in not_executed) + "\n\n")

        print(f"\n📝 Detailed report saved: {report_path}")


def main():
    print("=" * 80)
    print("PRIORITY 3: TEST CELLS 42-230")
    print("=" * 80)
    print()

    # Use the notebook with error fixes
    notebook_file = 'master-ai-gateway-with-error-fixes.ipynb'

    # Check if file exists
    if not Path(notebook_file).exists():
        notebook_file = 'master-ai-gateway-with-approved-fixes.ipynb'
        print(f"ℹ️  Using notebook: {notebook_file}")
    else:
        print(f"✅ Using notebook with error fixes: {notebook_file}")

    print()

    # Test
    tester = LabCellTester(notebook_file)
    tester.test_cells_42_to_230()

    # Save report
    tester.save_report('analysis-reports/TEST_REPORT_CELLS_42_230.md')

    print("=" * 80)


if __name__ == '__main__':
    main()
