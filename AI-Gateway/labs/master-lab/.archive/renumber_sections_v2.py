#!/usr/bin/env python3
"""
Renumber Notebook Sections V2
- Promotes Access Control (Lab 1.4) to Section 1
- Renumbers all subsequent sections sequentially
- FLAGS duplicates instead of deleting
"""

import json
import re
from datetime import datetime
from pathlib import Path

def renumber_sections(input_file, output_file):
    """Renumber sections with Access Control as Section 1"""

    print(f"Loading notebook: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    cells = notebook['cells']
    changes_log = []

    print("\nApplying renumbering...")
    print("=" * 80)

    # Process each cell
    for i, cell in enumerate(cells):
        if cell['cell_type'] == 'markdown':
            source_lines = cell.get('source', [])
            source = ''.join(source_lines)
            original_source = source

            # === STEP 1: Promote Lab 1.4 (Access Controlling) to Section 1 ===
            if '<a id="lab1-4">' in source or "<a id='lab1-4'>" in source:
                # Update anchor
                source = source.replace('<a id="lab1-4">', '<a id="section1">')
                source = source.replace("<a id='lab1-4'>", "<a id='section1'>")
                # Promote header from ## to #
                source = re.sub(r'^## Access Controlling', '# Section 1: Access Controlling', source, flags=re.MULTILINE)
                changes_log.append(f"Cell {i:3d}: Promoted Lab 1.4 → Section 1: Access Controlling")

            # === STEP 2: Renumber Section 1 → Section 2 ===
            elif '<a id="section1">' in source and '# Section 1:' in source:
                source = source.replace('<a id="section1">', '<a id="section2">')
                source = re.sub(r'# Section 1:', '# Section 2:', source)
                changes_log.append(f"Cell {i:3d}: Renumbered Section 1 → Section 2")

            # === STEP 3: Renumber Section 2 → Section 3 ===
            elif '<a id="section2">' in source and '# Section 2:' in source:
                source = source.replace('<a id="section2">', '<a id="section3">')
                source = re.sub(r'# Section 2:', '# Section 3:', source)
                changes_log.append(f"Cell {i:3d}: Renumbered Section 2 → Section 3")

            # === STEP 4: Renumber Section 3 → Section 4 ===
            elif '<a id="section3">' in source and '# Section 3:' in source:
                source = source.replace('<a id="section3">', '<a id="section4">')
                source = re.sub(r'# Section 3:', '# Section 4:', source)
                changes_log.append(f"Cell {i:3d}: Renumbered Section 3 → Section 4")

            # === STEP 5: Renumber Section 4 → Section 5 ===
            elif '<a id="section4">' in source and '# Section 4:' in source:
                source = source.replace('<a id="section4">', '<a id="section5">')
                source = re.sub(r'# Section 4:', '# Section 5:', source)
                changes_log.append(f"Cell {i:3d}: Renumbered Section 4 → Section 5")

            # === STEP 6: Renumber Section 5 → Section 6 ===
            elif '<a id="section5">' in source and '# Section 5:' in source:
                source = source.replace('<a id="section5">', '<a id="section6">')
                source = re.sub(r'# Section 5:', '# Section 6:', source)
                changes_log.append(f"Cell {i:3d}: Renumbered Section 5 → Section 6")

            # === STEP 7: Renumber Labs in Section 2 (formerly Section 1) ===
            # Lab 1.1 → 2.1
            if '<a id="lab1-1">' in source or "<a id='lab1-1'>" in source:
                source = source.replace('<a id="lab1-1">', '<a id="lab2-1">')
                source = source.replace("<a id='lab1-1'>", "<a id='lab2-1'>")
                source = re.sub(r'## Lab 1\.1:', '## Lab 2.1:', source)
                changes_log.append(f"Cell {i:3d}: Renumbered Lab 1.1 → Lab 2.1")

            # Lab 1.2 → 2.2
            if '<a id="lab1-2">' in source:
                source = source.replace('<a id="lab1-2">', '<a id="lab2-2">')
                source = re.sub(r'## Lab 1\.2:', '## Lab 2.2:', source)
                changes_log.append(f"Cell {i:3d}: Renumbered Lab 1.2 → Lab 2.2")

            # Lab 1.3 → 2.3
            if '<a id="lab1-3">' in source:
                source = source.replace('<a id="lab1-3">', '<a id="lab2-3">')
                source = re.sub(r'## Lab 1\.3:', '## Lab 2.3:', source)
                changes_log.append(f"Cell {i:3d}: Renumbered Lab 1.3 → Lab 2.3")

            # Lab 1.5 → 2.4 (Content Safety)
            if '<a id="lab1-5">' in source:
                source = source.replace('<a id="lab1-5">', '<a id="lab2-4">')
                source = re.sub(r'## Lab 1\.5:', '## Lab 2.4:', source)
                changes_log.append(f"Cell {i:3d}: Renumbered Lab 1.5 → Lab 2.4 (Content Safety)")

            # Lab 1.6 → 2.5
            if '<a id="lab1-6">' in source:
                source = source.replace('<a id="lab1-6">', '<a id="lab2-5">')
                source = re.sub(r'## Lab 1\.6:', '## Lab 2.5:', source)
                changes_log.append(f"Cell {i:3d}: Renumbered Lab 1.6 → Lab 2.5")

            # === STEP 8: Renumber Labs in Section 3 (formerly Section 2) ===
            # Lab 2.1 → 3.1
            if '<a id="lab2-1">' in source and i != 56:  # Skip the one we just created
                source = source.replace('<a id="lab2-1">', '<a id="lab3-1">')
                source = re.sub(r'## Lab 2\.1:', '## Lab 3.1:', source)
                changes_log.append(f"Cell {i:3d}: Renumbered Lab 2.1 → Lab 3.1")

            # Lab 2.2 → 3.2
            if '<a id="lab2-2">' in source and i != 60:
                source = source.replace('<a id="lab2-2">', '<a id="lab3-2">')
                source = re.sub(r'## Lab 2\.2:', '## Lab 3.2:', source)
                changes_log.append(f"Cell {i:3d}: Renumbered Lab 2.2 → Lab 3.2")

            # Lab 2.3 → 3.3
            if '<a id="lab2-3">' in source and i != 70:
                source = source.replace('<a id="lab2-3">', '<a id="lab3-3">')
                source = re.sub(r'## Lab 2\.3:', '## Lab 3.3:', source)
                changes_log.append(f"Cell {i:3d}: Renumbered Lab 2.3 → Lab 3.3")

            # Lab 2.4 → 3.4
            if '<a id="lab2-4">' in source:
                source = source.replace('<a id="lab2-4">', '<a id="lab3-4">')
                source = re.sub(r'## Lab 2\.4:', '## Lab 3.4:', source)
                changes_log.append(f"Cell {i:3d}: Renumbered Lab 2.4 → Lab 3.4")

            # === STEP 9: Renumber Labs in Section 5 (formerly Section 4) ===
            # Lab 4.1 → 5.1
            if '<a id="lab4-1">' in source:
                source = source.replace('<a id="lab4-1">', '<a id="lab5-1">')
                source = re.sub(r'## Lab 4\.1:', '## Lab 5.1:', source)
                changes_log.append(f"Cell {i:3d}: Renumbered Lab 4.1 → Lab 5.1")

            # Lab 4.2 → 5.2
            if '<a id="lab4-2">' in source:
                source = source.replace('<a id="lab4-2">', '<a id="lab5-2">')
                source = re.sub(r'## Lab 4\.2:', '## Lab 5.2:', source)
                changes_log.append(f"Cell {i:3d}: Renumbered Lab 4.2 → Lab 5.2")

            # Lab 4.3 → 5.3
            if '<a id="lab4-3">' in source:
                source = source.replace('<a id="lab4-3">', '<a id="lab5-3">')
                source = re.sub(r'## Lab 4\.3:', '## Lab 5.3:', source)
                changes_log.append(f"Cell {i:3d}: Renumbered Lab 4.3 → Lab 5.3")

            # === STEP 10: FLAG DUPLICATES ===
            # Flag Lab 01 at cell 53 (duplicate of Lab 2.1)
            if i == 53 and ('<a id="lab01">' in source or "<a id='lab01'>" in source):
                source = '\n⚠️ **DUPLICATE - FLAGGED FOR REVIEW** ⚠️\n\n' + source
                changes_log.append(f"Cell {i:3d}: FLAGGED duplicate Lab 01")

            # Flag duplicate Lab 1.1 at cell 56 (if it still has old ID after renumbering)
            if i == 56 and 'Zero to Production' in source and '⚠️' not in source:
                # Check if this is the second occurrence
                has_zero_to_prod_before = False
                for j in range(53, 56):
                    prev_source = ''.join(cells[j].get('source', []))
                    if 'Zero to Production' in prev_source:
                        has_zero_to_prod_before = True
                        break
                if has_zero_to_prod_before:
                    source = '\n⚠️ **DUPLICATE - FLAGGED FOR REVIEW** ⚠️\n\n' + source
                    changes_log.append(f"Cell {i:3d}: FLAGGED duplicate Lab (Zero to Production)")

            # Flag duplicate Lab 3.4 at cell 118 (Built-in LLM Logging)
            if i == 118 and '<a id="lab3-4">' in source:
                source = '\n⚠️ **DUPLICATE - FLAGGED FOR REVIEW** ⚠️\n\n' + source
                changes_log.append(f"Cell {i:3d}: FLAGGED duplicate Lab 3.4 (Built-in LLM Logging)")

            # Update the cell if changes were made
            if source != original_source:
                cell['source'] = source.split('\n')

    # Save the renumbered notebook
    notebook['cells'] = cells

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)

    print(f"\n✅ Renumbered notebook saved as: {output_file}")
    print(f"\nTotal changes: {len(changes_log)}")
    for change in changes_log:
        print(f"  • {change}")

    return changes_log

if __name__ == "__main__":
    input_notebook = "master-ai-gateway-fix-MCP-clean.ipynb"
    output_notebook = f"master-ai-gateway-renumbered-{datetime.now().strftime('%Y%m%d_%H%M%S')}.ipynb"

    print("=" * 80)
    print("SECTION RENUMBERING UTILITY V2")
    print("=" * 80)

    if not Path(input_notebook).exists():
        print(f"❌ Input file not found: {input_notebook}")
        exit(1)

    changes = renumber_sections(input_notebook, output_notebook)

    print("\n" + "=" * 80)
    print(f"✅ Renumbering complete! {len(changes)} changes applied")
    print(f"✅ Output: {output_notebook}")
    print("=" * 80)
