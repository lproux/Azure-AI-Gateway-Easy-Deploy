import json
import re

with open("master-ai-gateway-fix-MCP-clean.ipynb", "r", encoding="utf-8") as f:
    notebook = json.load(f)

cells = notebook["cells"]
print(f"Total cells: {len(cells)}")
print(f"Code cells: {sum(1 for c in cells if c['cell_type'] == 'code')}")
print(f"Markdown cells: {sum(1 for c in cells if c['cell_type'] == 'markdown')}")
print("\n" + "="*80)
print("NOTEBOOK STRUCTURE ANALYSIS")
print("="*80)

current_section = None
code_without_docs = []
section_issues = []

for i, cell in enumerate(cells):
    if cell["cell_type"] == "markdown":
        source = "".join(cell["source"])
        
        # Check for section headers
        if re.match(r'^#{1,3} ', source):
            lines = source.split('\n')
            header = lines[0].strip()
            print(f"\nCell {i:3d}: {header}")
            
            # Check for section numbering issues
            if "Section" in header:
                current_section = header
                # Look for numbering inconsistencies
                if re.search(r'Section [0-9]', header) and i > 50:
                    section_match = re.search(r'Section ([0-9]+)', header)
                    if section_match:
                        sec_num = int(section_match.group(1))
                        if sec_num < 2 and "Access" not in header:
                            section_issues.append(f"Cell {i}: {header} - appears after cell 50 but numbered as Section {sec_num}")
            
            if "Lab" in header:
                print(f"         └─> LAB IDENTIFIED: {header}")
                
    elif cell["cell_type"] == "code":
        # Check if previous cell was documentation
        if i > 0 and cells[i-1]["cell_type"] != "markdown":
            code_without_docs.append(i)
        elif i > 0 and cells[i-1]["cell_type"] == "markdown":
            prev_source = "".join(cells[i-1]["source"])
            if not any(keyword in prev_source.lower() for keyword in ["purpose", "input", "output", "what", "step"]):
                code_without_docs.append(i)

print("\n" + "="*80)
print("ISSUES IDENTIFIED")
print("="*80)

print(f"\n1. Section numbering issues found: {len(section_issues)}")
for issue in section_issues[:10]:
    print(f"   - {issue}")

print(f"\n2. Code cells without documentation: {len(code_without_docs)} cells")
print(f"   First 10 undocumented cells: {code_without_docs[:10]}")

# Check for misaligned content
print("\n3. Checking for misaligned content...")
for i, cell in enumerate(cells):
    if cell["cell_type"] == "markdown":
        source = "".join(cell["source"])
        if "Lab 2.4" in source and i > 100:
            print(f"   - Cell {i}: Contains 'Lab 2.4' but positioned late in notebook")
        if "Phase 3" in source:
            print(f"   - Cell {i}: Contains 'Phase 3' content")

# Look for deployment references
print("\n4. Deployment file references:")
deployment_refs = 0
for i, cell in enumerate(cells):
    source = "".join(cell.get("source", []))
    if any(term in source for term in ["deploy-0", "deploy/", "deployment", ".bicep", ".json"]):
        deployment_refs += 1
        if deployment_refs <= 5:
            preview = source[:100].replace('\n', ' ')
            print(f"   - Cell {i}: {preview}...")

print(f"   Total cells with deployment references: {deployment_refs}")

