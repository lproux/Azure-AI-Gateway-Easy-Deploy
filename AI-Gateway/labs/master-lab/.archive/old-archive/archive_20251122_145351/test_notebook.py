"""
Comprehensive Notebook Test Suite using A-L Methodology
Tests each cell with real execution (no mocking)
"""

import papermill as pm
import nbformat
import json
import sys
import re
import traceback
from pathlib import Path
from datetime import datetime

class NotebookTester:
    def __init__(self, notebook_path):
        self.notebook_path = Path(notebook_path)
        self.nb = nbformat.read(notebook_path, as_version=4)
        self.test_results = []
        self.log_file = Path(f'test_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')

    def log(self, message):
        """Log to both console and file"""
        print(message)
        with open(self.log_file, 'a') as f:
            f.write(f"{datetime.now().isoformat()} - {message}\n")

    def test_cell(self, cell_index, max_retries=3):
        """
        Testing operation for each cell following the A-L methodology:
        A - Analyze current code
        B - Analyze current output
        C - Create resolution for cell
        D - Create predicted output
        E - Run the cell
        F - Analyze actual output
        G - Compare expected with actual output
        H - Analyze discrepancies
        I - Verify actual output matches
        J - If not matching, restart at A (up to max_retries)
        K - When J passes, run notebook up to this cell
        L - When K passes, mark success

        IMPORTANT: No mock testing - real execution only
        """

        cell = self.nb.cells[cell_index]
        if cell.cell_type != 'code':
            self.log(f"[SKIP] Cell {cell_index} is markdown")
            return True

        self.log(f"\n{'='*60}")
        self.log(f"Testing Code Cell {cell_index}")
        self.log(f"{'='*60}")

        for retry in range(max_retries):
            try:
                # A - Analyze current code
                self.log(f"[A] Analyzing code...")
                code_analysis = self.analyze_code(cell)
                self.log(f"    Dependencies: {code_analysis.get('dependencies', [])[:5]}")
                self.log(f"    Creates: {code_analysis.get('creates', [])[:5]}")

                # B - Analyze current output
                self.log(f"[B] Analyzing existing output...")
                current_output = self.get_cell_outputs(cell)
                self.log(f"    Current output type: {current_output.get('type', 'none')}")

                # C - Create resolution
                self.log(f"[C] Creating resolution...")
                resolution = self.create_resolution(code_analysis)
                self.log(f"    Strategy: {resolution}")

                # D - Create predicted output
                self.log(f"[D] Predicting output...")
                predicted = self.predict_output(code_analysis)
                self.log(f"    Expected: {predicted.get('type', 'unknown')}")

                # E - Run the cell (REAL EXECUTION)
                self.log(f"[E] Executing cell...")
                actual_output = self.execute_cell_real(cell_index)

                # F - Analyze actual output
                self.log(f"[F] Actual output received:")
                self.log(f"    Type: {actual_output.get('type', 'none')}")
                if actual_output.get('error'):
                    self.log(f"    Error: {actual_output['error'][:100]}")

                # G - Compare outputs
                self.log(f"[G] Comparing outputs...")
                comparison = self.compare_outputs(predicted, actual_output)
                self.log(f"    Match: {comparison['matches']}")

                # H - Analyze discrepancies
                if not comparison['matches']:
                    self.log(f"[H] Analyzing discrepancies...")
                    for disc in comparison.get('discrepancies', []):
                        self.log(f"    - {disc[:80]}")

                # I - Verify match
                self.log(f"[I] Verification: {'PASS' if comparison['matches'] else 'FAIL'}")

                # J - Check if restart needed
                if not comparison['matches']:
                    if retry < max_retries - 1:
                        self.log(f"[J] Output mismatch, retry {retry + 1}/{max_retries}")
                        continue
                    else:
                        self.log(f"[J] Max retries reached, FAILING")
                        return False

                # K - Run notebook up to this cell
                self.log(f"[K] Running cumulative test (cells 0-{cell_index})...")
                cumulative_success = self.run_notebook_to_cell(cell_index)

                if not cumulative_success:
                    self.log(f"[K] Cumulative run failed")
                    if retry < max_retries - 1:
                        continue
                    return False

                # L - Success!
                self.log(f"[L] Cell {cell_index} TEST SUCCESS")
                return True

            except Exception as e:
                self.log(f"[ERROR] Exception: {str(e)[:100]}")
                if retry < max_retries - 1:
                    self.log(f"Retrying... ({retry + 1}/{max_retries})")
                    continue
                return False

        return False

    def analyze_code(self, cell):
        """Analyze code cell for dependencies and outputs"""
        code = ''.join(cell.source) if isinstance(cell.source, list) else cell.source
        analysis = {
            'dependencies': [],
            'creates': [],
            'imports': [],
            'has_print': 'print(' in code,
            'has_azure': 'azure' in code.lower(),
            'has_api_call': 'requests.' in code or 'httpx.' in code
        }

        # Find imports
        import_lines = [l for l in code.split('\n') if l.strip().startswith(('import ', 'from '))]
        analysis['imports'] = import_lines

        # Find variable assignments
        for line in code.split('\n'):
            if '=' in line and not line.strip().startswith('#'):
                parts = line.split('=')
                if len(parts) >= 2:
                    var_name = parts[0].strip()
                    if var_name and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', var_name):
                        analysis['creates'].append(var_name)

        # Find dependencies (simple heuristic)
        possible_vars = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code)
        builtins = {'print', 'len', 'str', 'int', 'float', 'list', 'dict', 'set', 'True', 'False', 'None'}
        for var in set(possible_vars):
            if var not in analysis['creates'] and var not in builtins:
                if not any(var in imp for imp in import_lines):
                    analysis['dependencies'].append(var)

        return analysis

    def create_resolution(self, code_analysis):
        """Determine execution strategy"""
        if code_analysis['imports']:
            return "import_execution"
        elif code_analysis['has_api_call']:
            return "api_execution"
        elif code_analysis['dependencies']:
            return "dependent_execution"
        else:
            return "standalone_execution"

    def predict_output(self, code_analysis):
        """Predict expected output type"""
        prediction = {'type': 'none', 'should_error': False}

        if code_analysis['imports']:
            prediction['type'] = 'import_success'
        elif code_analysis['has_print']:
            prediction['type'] = 'stream'
        elif code_analysis['creates']:
            prediction['type'] = 'variable_creation'

        if code_analysis['has_api_call']:
            prediction['warning'] = 'API call - may fail without network'

        return prediction

    def execute_cell_real(self, cell_index):
        """Execute cell using papermill - REAL EXECUTION"""
        temp_nb = Path(f'temp_test_{cell_index}_{datetime.now().strftime("%H%M%S")}.ipynb')

        # Create notebook with all cells up to target
        test_nb = nbformat.v4.new_notebook()
        test_nb.cells = self.nb.cells[:cell_index + 1]
        nbformat.write(test_nb, temp_nb)

        result = {'type': 'none', 'error': None, 'outputs': []}

        try:
            output_nb_path = temp_nb.with_suffix('.executed.ipynb')
            pm.execute_notebook(
                str(temp_nb),
                str(output_nb_path),
                kernel_name='python3',
                progress_bar=False,
                log_output=False
            )

            # Read executed notebook
            output_nb = nbformat.read(output_nb_path, as_version=4)
            executed_cell = output_nb.cells[cell_index]

            # Extract outputs
            if hasattr(executed_cell, 'outputs'):
                for output in executed_cell.outputs:
                    if output.output_type == 'error':
                        result['error'] = output.ename + ': ' + output.evalue
                        result['type'] = 'error'
                    elif output.output_type == 'stream':
                        result['outputs'].append(output.text)
                        result['type'] = 'stream'
                    elif output.output_type == 'execute_result':
                        result['outputs'].append(str(output.data))
                        result['type'] = 'execute_result'

            if result['type'] == 'none' and not result['error']:
                result['type'] = 'success_silent'

        except pm.exceptions.PapermillExecutionError as e:
            result['error'] = str(e)
            result['type'] = 'execution_error'
        except Exception as e:
            result['error'] = f"Unexpected: {e}"
            result['type'] = 'system_error'
        finally:
            temp_nb.unlink(missing_ok=True)
            temp_nb.with_suffix('.executed.ipynb').unlink(missing_ok=True)

        return result

    def get_cell_outputs(self, cell):
        """Extract existing outputs from cell"""
        result = {'type': 'none', 'outputs': []}

        if hasattr(cell, 'outputs'):
            for output in cell.outputs:
                if hasattr(output, 'output_type'):
                    result['type'] = output.output_type

        return result

    def compare_outputs(self, predicted, actual):
        """Compare predicted vs actual outputs"""
        comparison = {'matches': True, 'discrepancies': []}

        if actual.get('error') and not predicted.get('should_error'):
            comparison['matches'] = False
            comparison['discrepancies'].append(f"Unexpected error: {actual['error']}")

        if actual['type'] == 'error' and not predicted.get('should_error'):
            comparison['matches'] = False
            comparison['discrepancies'].append(f"Got error but expected {predicted['type']}")

        return comparison

    def run_notebook_to_cell(self, cell_index):
        """Run entire notebook from start to specified cell"""
        temp_nb = Path(f'temp_cumulative_{cell_index}.ipynb')

        test_nb = nbformat.v4.new_notebook()
        test_nb.cells = self.nb.cells[:cell_index + 1]
        nbformat.write(test_nb, temp_nb)

        try:
            output_path = temp_nb.with_suffix('.cumulative.ipynb')
            pm.execute_notebook(
                str(temp_nb),
                str(output_path),
                kernel_name='python3',
                progress_bar=False
            )
            self.log(f"    Cumulative execution successful")
            return True
        except Exception as e:
            self.log(f"    Cumulative execution failed: {str(e)[:100]}")
            return False
        finally:
            temp_nb.unlink(missing_ok=True)
            temp_nb.with_suffix('.cumulative.ipynb').unlink(missing_ok=True)

    def run_full_test(self):
        """Run tests on all code cells"""
        self.log(f"Starting full notebook test: {self.notebook_path}")
        self.log(f"Total cells: {len(self.nb.cells)}")

        code_cells = [(i, c) for i, c in enumerate(self.nb.cells) if c.cell_type == 'code']
        self.log(f"Code cells to test: {len(code_cells)}")

        failed_cells = []

        for cell_num, (index, cell) in enumerate(code_cells, 1):
            self.log(f"\n[{cell_num}/{len(code_cells)}] Testing cell index {index}")

            success = self.test_cell(index)

            if not success:
                self.log(f"FAILED at cell {index}")
                failed_cells.append(index)

        self.log(f"\n{'='*60}")
        self.log("TEST SUMMARY")
        self.log(f"{'='*60}")

        if failed_cells:
            self.log(f"FAILED - {len(failed_cells)} cells failed: {failed_cells}")
            return False
        else:
            self.log("SUCCESS - All cells tested!")
            return True

if __name__ == "__main__":
    notebook_path = "master-ai-gateway-fix-MCP-clean.ipynb"

    if len(sys.argv) > 1:
        notebook_path = sys.argv[1]

    if not Path(notebook_path).exists():
        print(f"Error: {notebook_path} not found")
        sys.exit(1)

    tester = NotebookTester(notebook_path)
    success = tester.run_full_test()

    print(f"\nTest log saved to: {tester.log_file}")
    sys.exit(0 if success else 1)
