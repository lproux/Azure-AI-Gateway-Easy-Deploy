#!/usr/bin/env python3
"""
Renumber Notebook Sections
- Promotes Access Control to Section 1
- Renumbers all subsequent sections
- FLAGS duplicates instead of deleting them
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

    # Track changes
    changes_log = []

    print("\nApplying renumbering...")
    print("=" * 80)

    # Define renumbering mappings
    section_mapping = {
        # Keep Section 0 as is
        'section0': 'section0',

        # Lab 1.4 becomes Section 1
        'lab1-4': 'section1',

        # Section 1 becomes Section 2
        'section1': 'section2',
        'lab1-1': 'lab2-1',
        'lab1-2': 'lab2-2',
        'lab1-3': 'lab2-3',
        'lab1-5': 'lab2-4',  # Note: 1.5 becomes 2.4 (Content Safety)
        'lab1-6': 'lab2-5',

        # Section 2 becomes Section 3
        'section2': 'section3',
        'lab2-1': 'lab3-1',
        'lab2-2': 'lab3-2',
        'lab2-3': 'lab3-3',
        'lab2-4': 'lab3-4',

        # Section 3 becomes Section 4
        'section3': 'section4',
        'section3-1': 'section4-1',
        'section3-2': 'section4-2',
        'section3-3': 'section4-3',
        'section3-4': 'section4-4',
        'section3-5': 'section4-5',

        # Section 4 becomes Section 5
        'section4': 'section5',
        'lab4-1': 'lab5-1',
        'lab4-2': 'lab5-2',
        'lab4-3': 'lab5-3',

        # Section 5 becomes Section 6
        'section5': 'section6',
        'section5-1': 'section6-1',
        'section5-2': 'section6-2',
        'section5-3': 'section6-3',
        'section5-4': 'section6-4',
        'section5-5': 'section6-5',
    }

    # Process each cell
    for i, cell in enumerate(cells):
        if cell['cell_type'] == 'markdown':
            source = ''.join(cell.get('source', []))
            original_source = source

            # Update anchor IDs
            for old_id, new_id in section_mapping.items():
                source = source.replace(f'<a id="{old_id}">', f'<a id="{new_id}">')
                source = source.replace(f'<a id=\'{old_id}\'>', f'<a id=\'{new_id}\'>')
                source = source.replace(f'#{old_id}', f'#{new_id}')

            # Update section headers
            # Promote Lab 1.4 (Access Controlling) to Section 1
            if '<a id="lab1-4">' in source or '<a id=\'lab1-4\'>' in source:
                # Change header from ## to #
                source = re.sub(r'## Access Controlling', '# Section 1: Access Controlling', source)
                changes_log.append(f"Cell {i}: Promoted Lab 1.4 (Access Controlling) → Section 1")

            # Update Section 1 to Section 2
            elif '<a id="section2">' in source and re.search(r'# Section 1:', source):
                source = re.sub(r'# Section 1:', '# Section 2:', source)
                changes_log.append(f"Cell {i}: Renumbered Section 1 → Section 2")

            # Update Section 2 to Section 3
            elif '<a id="section3">' in source and re.search(r'# Section 2:', source):
                source = re.sub(r'# Section 2:', '# Section 3:', source)
                changes_log.append(f"Cell {i}: Renumbered Section 2 → Section 3")

            # Update Section 3 to Section 4
            elif '<a id="section4">' in source and re.search(r'# Section 3:', source):
                source = re.sub(r'# Section 3:', '# Section 4:', source)
                changes_log.append(f"Cell {i}: Renumbered Section 3 → Section 4")

            # Update Section 4 to Section 5
            elif '<a id="section5">' in source and re.search(r'# Section 4:', source):
                source = re.sub(r'# Section 4:', '# Section 5:', source)
                changes_log.append(f"Cell {i}: Renumbered Section 4 → Section 5")

            # Update Section 5 to Section 6
            elif '<a id="section6">' in source and re.search(r'# Section 5:', source):
                source = re.sub(r'# Section 5:', '# Section 6:', source)
                changes_log.append(f"Cell {i}: Renumbered Section 5 → Section 6")

            # Update Lab numbers under Section 2 (formerly Section 1)
            source = re.sub(r'## Lab 1\.1:', '## Lab 2.1:', source)
            source = re.sub(r'## Lab 1\.2:', '## Lab 2.2:', source)
            source = re.sub(r'## Lab 1\.3:', '## Lab 2.3:', source)
            source = re.sub(r'## Lab 1\.5:', '## Lab 2.4:', source)  # Content Safety
            source = re.sub(r'## Lab 1\.6:', '## Lab 2.5:', source)

            # Update Lab numbers under Section 3 (formerly Section 2)
            if '<a id="lab3-' in source:
                source = re.sub(r'## Lab 2\.1:', '## Lab 3.1:', source)
                source = re.sub(r'## Lab 2\.2:', '## Lab 3.2:', source)
                source = re.sub(r'## Lab 2\.3:', '## Lab 3.3:', source)
                source = re.sub(r'## Lab 2\.4:', '## Lab 3.4:', source)

            # Update Lab numbers under Section 5 (formerly Section 4)
            source = re.sub(r'## Lab 4\.1:', '## Lab 5.1:', source)
            source = re.sub(r'## Lab 4\.2:', '## Lab 5.2:', source)
            source = re.sub(r'## Lab 4\.3:', '## Lab 5.3:', source)

            # FLAG DUPLICATES instead of deleting
            # Flag Lab 01 (cell 53) - duplicate of Lab 2.1
            if i == 53 and re.search(r'## Lab 01:', source):
                source = '⚠️ **DUPLICATE - FLAGGED FOR REVIEW** ⚠️\n\n' + source
                changes_log.append(f"Cell {i}: FLAGGED duplicate Lab 01")

            # Flag duplicate Lab 1.1 at cell 56
            if i == 56 and '<a id="lab2-1">' in source:
                source = '⚠️ **DUPLICATE - FLAGGED FOR REVIEW** ⚠️\n\n' + source
                changes_log.append(f"Cell {i}: FLAGGED duplicate Lab 1.1 (now Lab 2.1)")

            # Flag duplicate Lab 2.4 at cell 118
            if i == 118 and '<a id="lab3-4">' in source:
                source = '⚠️ **DUPLICATE - FLAGGED FOR REVIEW** ⚠️\n\n' + source
                changes_log.append(f"Cell {i}: FLAGGED duplicate Lab 2.4 (now Lab 3.4)")

            # Update the cell if changes were made
            if source != original_source:
                cell['source'] = source.split('\n')

    # Save the renumbered notebook
    notebook['cells'] = cells

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)

    print(f"\n✅ Renumbered notebook saved as: {output_file}")
    print(f"\nChanges made: {len(changes_log)}")
    for change in changes_log:
        print(f"  • {change}")

    return changes_log

def create_new_toc():
    """Generate new table of contents"""

    toc = """# Master AI Gateway Workshop

## Table of Contents

### [Section 0: Initialize and Deploy](#section0)
- [0.1 Environment Detection](#env-detection)
- [0.2 Bootstrap Configuration](#bootstrap)
- [0.3 Dependencies Installation](#dependencies)
- [0.4 Azure Authentication & Service Principal](#azure-auth)
- [0.5 Core Helper Functions](#helpers)
- [0.6 Deployment Configuration](#deploy-config)
- [0.7 Deploy Infrastructure](#deploy-infra)
- [0.8 Reload Complete Configuration](#reload-config)

### [Section 1: Access Controlling](#section1)
- OAuth 2.0 Authorization
- Token Acquisition & Validation
- Azure AD Integration

### [Section 2: Core AI Gateway Features](#section2)
- [Lab 2.1: Zero to Production](#lab2-1)
- [Lab 2.2: Backend Pool Load Balancing](#lab2-2)
- [Lab 2.3: Token Metrics Emitting](#lab2-3)
- [Lab 2.4: Content Safety](#lab2-4)
- [Lab 2.5: Model Routing](#lab2-5)

### [Section 3: Advanced Features](#section3)
- [Lab 3.1: Semantic Caching](#lab3-1)
- [Lab 3.2: Message Storing with Cosmos DB](#lab3-2)
- [Lab 3.3: Vector Searching with RAG](#lab3-3)
- [Lab 3.4: Built-in LLM Logging](#lab3-4)

### [Section 4: MCP Fundamentals](#section4)
- [4.1 MCP Server Integration](#section4-1)
- [4.2 Exercise: Sales Analysis via MCP + AI](#section4-2)
- [4.3 Exercise: Azure Cost Analysis via MCP](#section4-3)
- [4.4 Exercise: Function Calling with MCP Tools](#section4-4)
- [4.5 Exercise: Dynamic Column Analysis](#section4-5)

### [Section 5: AI Foundry & Integrations](#section5)
- [Lab 5.1: AI Foundry SDK](#lab5-1)
- [Lab 5.2: GitHub Repository Access](#lab5-2)
- [Lab 5.3: GitHub + AI Code Analysis](#lab5-3)

### [Section 6: Semantic Kernel & AutoGen](#section6)
- [6.1 SK Plugin for Gateway-Routed Function Calling](#section6-1)
- [6.2 SK Streaming Chat with Function Calling](#section6-2)
- [6.3 AutoGen Multi-Agent Conversation](#section6-3)
- [6.4 SK Agent with Custom Azure OpenAI Client](#section6-4)
- [6.5 Hybrid SK + AutoGen Orchestration](#section6-5)
"""

    return toc

if __name__ == "__main__":
    # Files
    input_notebook = "master-ai-gateway-fix-MCP-clean.ipynb"
    output_notebook = f"master-ai-gateway-renumbered-{datetime.now().strftime('%Y%m%d_%H%M%S')}.ipynb"

    print("=" * 80)
    print("SECTION RENUMBERING UTILITY")
    print("=" * 80)

    # Check if input exists
    if not Path(input_notebook).exists():
        print(f"❌ Input file not found: {input_notebook}")
        exit(1)

    # Renumber sections
    changes = renumber_sections(input_notebook, output_notebook)

    print("\n" + "=" * 80)
    print("NEXT STEP: Update Table of Contents (Cell 0)")
    print("=" * 80)
    print("\nNew TOC structure:")
    print(create_new_toc())

    # Save new TOC to file
    with open('NEW_TABLE_OF_CONTENTS.md', 'w') as f:
        f.write(create_new_toc())

    print("\n✅ New TOC saved to: NEW_TABLE_OF_CONTENTS.md")
    print(f"✅ Renumbered notebook saved to: {output_notebook}")
    print("\n🎉 Renumbering complete!")
    print("   - Access Control is now Section 1")
    print("   - All sections renumbered sequentially")
    print("   - Duplicates FLAGGED (not deleted)")
    print("\n" + "=" * 80)
