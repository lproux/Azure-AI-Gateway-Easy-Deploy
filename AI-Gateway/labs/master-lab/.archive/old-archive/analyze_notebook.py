import json
import re
import sys

def extract_cell_info(cell, index):
    """Extract information from a single cell"""
    info = {
        'index': index,
        'type': cell.get('cell_type', 'unknown'),
        'source': ''.join(cell.get('source', [])),
        'outputs': cell.get('outputs', [])
    }
    return info

def analyze_cell(cell_info):
    """Analyze a cell for dependencies and outputs"""
    source = cell_info['source']
    index = cell_info['index']

    analysis = {
        'cell': index,
        'type': cell_info['type'],
        'purpose': '',
        'cell_classification': '',
        'inputs': {
            'env_vars': [],
            'imports': [],
            'variables_used': [],
            'files_read': [],
            'azure_queries': []
        },
        'outputs': {
            'variables_created': [],
            'files_written': [],
            'env_vars_set': [],
            'side_effects': []
        },
        'dependencies': [],
        'issues': []
    }

    if cell_info['type'] == 'markdown':
        # Extract purpose from markdown
        lines = source.split('\n')
        if lines:
            first_line = lines[0].strip('#').strip()
            analysis['purpose'] = first_line[:100]
        analysis['cell_classification'] = 'DOCUMENTATION'
        return analysis

    # Environment variables read
    env_reads = re.findall(r'os\.environ(?:\[|\.get\()\s*["\']([^"\']+)["\']', source)
    analysis['inputs']['env_vars'].extend(env_reads)

    # Environment variables set
    env_sets = re.findall(r'os\.environ\s*\[\s*["\']([^"\']+)["\']\s*\]\s*=', source)
    analysis['inputs']['env_vars_set'] = env_sets

    # Imports
    import_matches = re.findall(r'^(?:from\s+(\S+)\s+)?import\s+(.+?)(?:\s+as\s+\w+)?$', source, re.MULTILINE)
    for match in import_matches:
        if match[0]:
            analysis['inputs']['imports'].append(f"from {match[0]} import {match[1]}")
        else:
            analysis['inputs']['imports'].append(f"import {match[1]}")

    # File reads
    file_reads = re.findall(r'open\s*\(\s*["\']([^"\']+)["\'].*?["\']r', source)
    file_reads.extend(re.findall(r'load_dotenv\s*\(\s*["\']?([^"\')\s]+)?["\']?\s*\)', source))
    file_reads.extend(re.findall(r'pd\.read_\w+\s*\(\s*["\']([^"\']+)["\']', source))
    analysis['inputs']['files_read'].extend(file_reads)

    # File writes
    file_writes = re.findall(r'open\s*\(\s*["\']([^"\']+)["\'].*?["\']w', source)
    file_writes.extend(re.findall(r'\.to_csv\s*\(\s*["\']([^"\']+)["\']', source))
    analysis['outputs']['files_written'].extend(file_writes)

    # Variable assignments (simple heuristic)
    var_assigns = re.findall(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*[^=]', source, re.MULTILINE)
    analysis['outputs']['variables_created'].extend(var_assigns)

    # Azure CLI commands
    if 'az ' in source or 'azd ' in source:
        analysis['outputs']['side_effects'].append('Azure CLI/AZD command')

    # Bicep deployment
    if '.bicep' in source or 'az deployment' in source:
        analysis['cell_classification'] = 'DEPLOYMENT'
        analysis['outputs']['side_effects'].append('Azure deployment')

    # Check for specific patterns
    if 'load_dotenv' in source:
        analysis['cell_classification'] = 'INITIALIZATION'
        analysis['purpose'] = 'Load environment variables from .env file'

    if 'subprocess.run' in source or '!' in source[:50]:
        analysis['outputs']['side_effects'].append('Shell command execution')

    # Check for Azure resource queries
    if 'az account' in source or 'az resource' in source or 'az group' in source:
        analysis['inputs']['azure_queries'].append('Azure resource query')

    # Classify cell
    if not analysis['cell_classification']:
        if any(x in source.lower() for x in ['bicep', 'az deployment', 'azd up', 'azd deploy']):
            analysis['cell_classification'] = 'DEPLOYMENT'
        elif 'load_dotenv' in source or 'MCP' in source or 'Client(' in source:
            analysis['cell_classification'] = 'INITIALIZATION'
        elif any(x in source for x in ['AZURE_', 'ENDPOINT', 'API_KEY']) and '=' in source:
            analysis['cell_classification'] = 'PRE-DEPLOYMENT'
        elif 'master-lab.env' in source and 'w' in source:
            analysis['cell_classification'] = 'POST-DEPLOYMENT'
        else:
            analysis['cell_classification'] = 'LAB/TEST'

    return analysis

# Read notebook
with open('/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab/master-ai-gateway-REORGANIZED.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Analyze cells (excluding 57-69)
cells = nb['cells']
analyses = []

for i, cell in enumerate(cells):
    if 57 <= i <= 69:
        continue  # Skip protected cells

    cell_info = extract_cell_info(cell, i)
    analysis = analyze_cell(cell_info)
    analyses.append(analysis)

# Print analysis for specific cells
print("=" * 80)
print("DETAILED CELL-BY-CELL ANALYSIS")
print("=" * 80)

# Focus on cells 0-56 and 70-end
for analysis in analyses:
    if analysis['cell'] <= 56 or analysis['cell'] >= 70:
        print(f"\n{'='*80}")
        print(f"Cell {analysis['cell']}: {analysis['cell_classification']}")
        print(f"{'='*80}")
        if analysis['purpose']:
            print(f"Purpose: {analysis['purpose']}")

        if analysis['type'] == 'code':
            if analysis['inputs']['env_vars']:
                print(f"  ENV READS: {', '.join(analysis['inputs']['env_vars'])}")
            if analysis['inputs']['imports']:
                print(f"  IMPORTS: {analysis['inputs']['imports'][:3]}")
            if analysis['inputs']['files_read']:
                print(f"  FILES READ: {', '.join(analysis['inputs']['files_read'])}")
            if analysis['outputs']['variables_created']:
                vars_created = [v for v in analysis['outputs']['variables_created'] if not v.startswith('_')]
                if vars_created:
                    print(f"  VARS CREATED: {', '.join(vars_created[:5])}")
            if analysis['outputs']['files_written']:
                print(f"  FILES WRITTEN: {', '.join(analysis['outputs']['files_written'])}")
            if analysis['outputs']['side_effects']:
                print(f"  SIDE EFFECTS: {', '.join(analysis['outputs']['side_effects'])}")

# Save full analysis
with open('/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs/master-lab/cell_analysis.json', 'w') as f:
    json.dump(analyses, f, indent=2)

print("\n\nFull analysis saved to cell_analysis.json")
