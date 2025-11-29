#!/usr/bin/env python3
"""
Notebook Test Runner for master-ai-gateway-deploy-from-notebook.ipynb

This script runs the notebook sequentially using papermill and reports
cell-by-cell execution status. It does NOT modify the notebook.

Usage:
    python test_notebook_runner.py                    # Run all cells
    python test_notebook_runner.py --cells 0-10      # Run cells 0-10
    python test_notebook_runner.py --cell 5          # Run up to cell 5
"""

import sys
import os
import json
import argparse
import time
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    import papermill as pm
    import nbformat
except ImportError:
    print("Installing required packages...")
    os.system(f"{sys.executable} -m pip install papermill nbformat --quiet")
    import papermill as pm
    import nbformat


def load_notebook(notebook_path: str) -> dict:
    """Load notebook and return cell information."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    return nb


def get_cell_info(nb: dict, cell_index: int) -> dict:
    """Get information about a specific cell."""
    if cell_index >= len(nb['cells']):
        return None

    cell = nb['cells'][cell_index]
    cell_type = cell['cell_type']
    source = ''.join(cell.get('source', []))

    # Get first line for identification
    first_line = source.split('\n')[0][:80] if source else "(empty)"

    # Get cell ID if present
    cell_id = cell.get('id', cell.get('metadata', {}).get('id', f'cell_{cell_index}'))

    return {
        'index': cell_index,
        'id': cell_id,
        'type': cell_type,
        'first_line': first_line,
        'source': source,
        'outputs': cell.get('outputs', [])
    }


def run_notebook_to_cell(notebook_path: str, max_cell: int, output_path: str = None) -> dict:
    """
    Run notebook from start to specified cell using papermill.

    Returns execution results including any errors.
    """
    if output_path is None:
        output_path = notebook_path.replace('.ipynb', '_output.ipynb')

    # Load original notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Create a copy with only cells up to max_cell
    nb_subset = nb.copy()
    nb_subset.cells = nb.cells[:max_cell + 1]

    # Save subset notebook
    subset_path = notebook_path.replace('.ipynb', f'_subset_{max_cell}.ipynb')
    with open(subset_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb_subset, f)

    # Run with papermill
    start_time = time.time()
    result = {
        'success': False,
        'error': None,
        'cell_index': max_cell,
        'duration': 0,
        'output_path': output_path
    }

    try:
        pm.execute_notebook(
            subset_path,
            output_path,
            cwd=str(Path(notebook_path).parent),
            kernel_name='python3',
            progress_bar=False,
            log_output=True
        )
        result['success'] = True
    except pm.PapermillExecutionError as e:
        result['error'] = {
            'cell_index': e.cell_index if hasattr(e, 'cell_index') else None,
            'message': str(e),
            'traceback': e.traceback if hasattr(e, 'traceback') else None
        }
    except Exception as e:
        result['error'] = {
            'cell_index': None,
            'message': str(e),
            'traceback': None
        }
    finally:
        result['duration'] = time.time() - start_time
        # Clean up subset file
        if os.path.exists(subset_path):
            os.remove(subset_path)

    return result


def analyze_output(output_path: str, cell_index: int) -> dict:
    """Analyze the output of a specific cell after execution."""
    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)

        if cell_index >= len(nb['cells']):
            return {'error': 'Cell index out of range'}

        cell = nb['cells'][cell_index]
        outputs = cell.get('outputs', [])

        # Extract text outputs
        text_outputs = []
        errors = []

        for output in outputs:
            if output.get('output_type') == 'stream':
                text_outputs.append(''.join(output.get('text', [])))
            elif output.get('output_type') == 'execute_result':
                data = output.get('data', {})
                if 'text/plain' in data:
                    text_outputs.append(''.join(data['text/plain']))
            elif output.get('output_type') == 'error':
                errors.append({
                    'ename': output.get('ename'),
                    'evalue': output.get('evalue'),
                    'traceback': output.get('traceback', [])
                })

        return {
            'cell_index': cell_index,
            'text_outputs': text_outputs,
            'errors': errors,
            'has_output': len(outputs) > 0
        }
    except Exception as e:
        return {'error': str(e)}


def main():
    parser = argparse.ArgumentParser(description='Test notebook runner')
    parser.add_argument('--cells', type=str, help='Cell range (e.g., 0-10)')
    parser.add_argument('--cell', type=int, help='Run up to this cell')
    parser.add_argument('--list', action='store_true', help='List cells only')
    args = parser.parse_args()

    notebook_path = Path(__file__).parent / 'master-ai-gateway-deploy-from-notebook.ipynb'

    if not notebook_path.exists():
        print(f"Error: Notebook not found at {notebook_path}")
        sys.exit(1)

    nb = load_notebook(str(notebook_path))
    total_cells = len(nb['cells'])
    code_cells = [i for i, c in enumerate(nb['cells']) if c['cell_type'] == 'code']

    print("=" * 70)
    print("NOTEBOOK TEST RUNNER")
    print("=" * 70)
    print(f"Notebook: {notebook_path.name}")
    print(f"Total cells: {total_cells}")
    print(f"Code cells: {len(code_cells)} at indices: {code_cells[:10]}...")
    print("=" * 70)

    if args.list:
        print("\nCell listing:")
        for i in range(min(30, total_cells)):
            info = get_cell_info(nb, i)
            marker = "[CODE]" if info['type'] == 'code' else "[MD]  "
            print(f"  {i:3d} {marker} {info['first_line'][:60]}")
        if total_cells > 30:
            print(f"  ... and {total_cells - 30} more cells")
        return

    # Determine which cells to run
    if args.cell is not None:
        max_cell = args.cell
    elif args.cells:
        start, end = map(int, args.cells.split('-'))
        max_cell = end
    else:
        max_cell = total_cells - 1

    print(f"\nRunning cells 0 to {max_cell}...")
    print("-" * 70)

    output_path = str(notebook_path).replace('.ipynb', '_test_output.ipynb')
    result = run_notebook_to_cell(str(notebook_path), max_cell, output_path)

    print(f"\nExecution completed in {result['duration']:.2f}s")
    print(f"Success: {result['success']}")

    if result['error']:
        print(f"\nError at cell {result['error'].get('cell_index', 'unknown')}:")
        print(f"  {result['error']['message'][:200]}")

    # Analyze last few code cells
    if os.path.exists(output_path):
        print("\nLast code cell outputs:")
        for i in code_cells:
            if i <= max_cell:
                analysis = analyze_output(output_path, i)
                if analysis.get('has_output') or analysis.get('errors'):
                    print(f"\n  Cell {i}:")
                    for text in analysis.get('text_outputs', [])[:3]:
                        for line in text.split('\n')[:5]:
                            print(f"    {line[:80]}")
                    for err in analysis.get('errors', []):
                        print(f"    ERROR: {err['ename']}: {err['evalue']}")


if __name__ == '__main__':
    main()
