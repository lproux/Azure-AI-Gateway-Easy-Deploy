#!/usr/bin/env python3
"""
Scan all lab notebooks to find MCP server references
"""
import json
import re
from pathlib import Path
from collections import defaultdict

LABS_DIR = Path("/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external/AI-Gateway/labs")

def scan_notebook(notebook_path):
    """Scan a notebook for MCP server references"""
    mcp_refs = set()
    
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        # Scan all cells for MCP references
        for cell in nb.get('cells', []):
            if cell.get('cell_type') == 'code':
                source = ''.join(cell.get('source', []))
                
                # Look for common MCP patterns
                patterns = [
                    r'mcp\.(\w+)',  # mcp.weather, mcp.excel, etc.
                    r'MCP_SERVER_(\w+)_URL',  # MCP_SERVER_WEATHER_URL
                    r'(\w+)MCP\(',  # WeatherMCP(), ExcelMCP()
                    r'(\w+)-mcp',  # weather-mcp, excel-mcp
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, source, re.IGNORECASE)
                    mcp_refs.update(matches)
        
        return mcp_refs
    except Exception as e:
        return set()

def main():
    print("=" * 80)
    print("🔍 Scanning Lab Notebooks for MCP Server References")
    print("=" * 80)
    print()
    
    # Find all notebooks
    notebooks = list(LABS_DIR.rglob("*.ipynb"))
    print(f"Found {len(notebooks)} notebooks to scan...")
    print()
    
    # Scan each notebook
    all_mcp_servers = defaultdict(list)
    
    for nb_path in notebooks:
        # Skip backup and executed files
        if any(x in nb_path.name for x in ['backup', 'executed', 'modified', 'nkp']):
            continue
            
        mcp_refs = scan_notebook(nb_path)
        
        if mcp_refs:
            lab_name = nb_path.parent.name
            for ref in mcp_refs:
                all_mcp_servers[ref.lower()].append(lab_name)
    
    # Sort by frequency
    sorted_servers = sorted(all_mcp_servers.items(), key=lambda x: len(x[1]), reverse=True)
    
    print("=" * 80)
    print("📊 MCP Servers Found (sorted by usage)")
    print("=" * 80)
    print()
    
    # Group by type
    currently_deployed = {'excel', 'docs'}
    needs_deployment = []
    
    for server, labs in sorted_servers:
        # Clean up the server name
        server_clean = server.lower().replace('_', '-').replace('server', '').strip('-')
        
        count = len(set(labs))
        status = "✅ DEPLOYED" if server_clean in currently_deployed else "⚠️  MISSING"
        
        print(f"{status:15} | {server_clean:20} | Used in {count} labs")
        
        if server_clean not in currently_deployed:
            needs_deployment.append((server_clean, count, labs))
    
    print()
    print("=" * 80)
    print("🎯 Deployment Plan")
    print("=" * 80)
    print()
    
    print("✅ Currently Deployed (2 servers):")
    print("   1. excel - Excel Analytics MCP")
    print("   2. docs - Research Documents MCP")
    print()
    
    if needs_deployment:
        print(f"⚠️  Need to Deploy ({len(needs_deployment)} servers):")
        for i, (server, count, labs) in enumerate(needs_deployment[:10], 1):
            example_labs = list(set(labs))[:3]
            print(f"   {i}. {server} (used in {count} labs)")
            print(f"      Examples: {', '.join(example_labs)}")
    else:
        print("✅ All required servers are deployed!")
    
    print()
    print("=" * 80)
    print("💡 Next Steps")
    print("=" * 80)
    print()
    print("1. For each missing server, we need to:")
    print("   - Find or create the server implementation (Dockerfile + server.py)")
    print("   - Build Docker image in ACR")
    print("   - Deploy to Azure Container Instances")
    print("   - Update .mcp-servers-config and helper library")
    print()
    print("2. Check if these servers exist in:")
    print("   - Workshop folder")
    print("   - Other lab folders (mcp-a2a-agents, etc.)")
    print("   - Public MCP registries")
    print()

if __name__ == "__main__":
    main()
