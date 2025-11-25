#!/usr/bin/env python3
"""
Test Cell 63 JWT authentication fix
"""
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import sys

def run_cell(notebook_path, cell_index):
    """Run a specific cell in a notebook"""
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Create executor
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

    # Execute cells up to and including the target cell
    print(f"Executing cells 0-{cell_index} from notebook...")
    for idx in range(cell_index + 1):
        cell = nb.cells[idx]
        if cell.cell_type == 'code':
            print(f"\n{'='*80}")
            print(f"Executing Cell {idx + 1} (Index {idx})")
            print(f"{'='*80}")

            # Show the source
            source = ''.join(cell.source) if isinstance(cell.source, list) else cell.source
            print(f"Source:\n{source[:200]}...")

            try:
                # Execute the cell
                ep.preprocess_cell(cell, {'metadata': {'path': './'}}, idx)

                # Show outputs
                if hasattr(cell, 'outputs') and cell.outputs:
                    print(f"\nOutputs:")
                    for output in cell.outputs:
                        if output.output_type == 'stream':
                            print(output.text, end='')
                        elif output.output_type == 'execute_result':
                            if 'text/plain' in output.data:
                                print(output.data['text/plain'])
                        elif output.output_type == 'error':
                            print(f"ERROR: {output.ename}: {output.evalue}")

            except Exception as e:
                print(f"ERROR executing cell: {e}")
                if idx == cell_index:
                    return False

    return True

if __name__ == '__main__':
    notebook_path = '/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab/master-ai-gateway-fix-MCP.ipynb'

    # Run cell 63 (index 62)
    success = run_cell(notebook_path, 62)

    if success:
        print("\n" + "="*80)
        print("✓ Cell 63 executed successfully!")
        print("="*80)
        sys.exit(0)
    else:
        print("\n" + "="*80)
        print("✗ Cell 63 failed")
        print("="*80)
        sys.exit(1)
