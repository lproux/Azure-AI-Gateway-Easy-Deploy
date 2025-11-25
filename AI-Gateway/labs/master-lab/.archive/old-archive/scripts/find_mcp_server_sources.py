#!/usr/bin/env python3
"""
Find source code for MCP servers in the repository
"""
from pathlib import Path

BASE_DIR = Path("/mnt/c/Users/lproux/OneDrive - Microsoft/bkp/Documents/GitHub/MCP-servers-internalMSFT-and-external")

# Priority servers (most used)
PRIORITY_SERVERS = ['weather', 'oncall', 'github', 'spotify', 'product-catalog', 'place-order', 'ms-learn']

def find_server_implementations():
    """Find server.py files and Dockerfiles"""
    
    print("=" * 80)
    print("🔍 Searching for MCP Server Implementations")
    print("=" * 80)
    print()
    
    # Find all server.py files
    server_files = list(BASE_DIR.rglob("server.py"))
    dockerfiles = list(BASE_DIR.rglob("Dockerfile"))
    
    print(f"Found {len(server_files)} server.py files")
    print(f"Found {len(dockerfiles)} Dockerfiles")
    print()
    
    # Organize by server type
    implementations = {}
    
    for server_path in server_files:
        parent = server_path.parent
        server_name = parent.name.lower()
        
        # Check if Dockerfile exists
        has_dockerfile = (parent / "Dockerfile").exists()
        
        # Check for requirements.txt
        has_requirements = (parent / "requirements.txt").exists()
        
        # Get relative path
        rel_path = parent.relative_to(BASE_DIR)
        
        implementations[server_name] = {
            'path': str(rel_path),
            'has_dockerfile': has_dockerfile,
            'has_requirements': has_requirements,
            'ready': has_dockerfile and has_requirements
        }
    
    print("=" * 80)
    print("📦 MCP Server Implementations Found")
    print("=" * 80)
    print()
    
    # Show priority servers first
    print("🎯 PRIORITY Servers (most used in labs):")
    print("-" * 80)
    for server in PRIORITY_SERVERS:
        if server in implementations:
            impl = implementations[server]
            status = "✅ READY" if impl['ready'] else "⚠️  INCOMPLETE"
            print(f"{status:15} | {server:20} | {impl['path']}")
        else:
            print(f"❌ NOT FOUND  | {server:20} | Need to create")
    print()
    
    # Show other implementations
    print("📋 OTHER Implementations Found:")
    print("-" * 80)
    for server, impl in sorted(implementations.items()):
        if server not in PRIORITY_SERVERS:
            status = "✅ READY" if impl['ready'] else "⚠️  INCOMPLETE"
            print(f"{status:15} | {server:20} | {impl['path']}")
    
    print()
    print("=" * 80)
    print("📊 Summary")
    print("=" * 80)
    print()
    
    ready_count = sum(1 for impl in implementations.values() if impl['ready'])
    total_count = len(implementations)
    
    print(f"Total implementations found: {total_count}")
    print(f"Ready to deploy: {ready_count}")
    print(f"Need work: {total_count - ready_count}")
    print()
    
    # Check priority servers
    priority_ready = [s for s in PRIORITY_SERVERS if s in implementations and implementations[s]['ready']]
    priority_missing = [s for s in PRIORITY_SERVERS if s not in implementations]
    priority_incomplete = [s for s in PRIORITY_SERVERS if s in implementations and not implementations[s]['ready']]
    
    print(f"Priority servers ({len(PRIORITY_SERVERS)}):")
    print(f"  ✅ Ready: {len(priority_ready)}")
    print(f"  ⚠️  Incomplete: {len(priority_incomplete)}")
    print(f"  ❌ Missing: {len(priority_missing)}")
    
    if priority_missing:
        print(f"\n❌ Missing servers: {', '.join(priority_missing)}")
    
    return implementations, priority_ready, priority_missing

if __name__ == "__main__":
    implementations, ready, missing = find_server_implementations()
    
    print()
    print("=" * 80)
    print("💡 Next Steps")
    print("=" * 80)
    print()
    
    if ready:
        print(f"1. Deploy {len(ready)} ready servers:")
        for server in ready:
            print(f"   - {server}")
        print()
    
    if missing:
        print(f"2. Create {len(missing)} missing servers:")
        for server in missing:
            print(f"   - {server} (need Dockerfile + server.py + requirements.txt)")
        print()
    
    print("3. Once all ready, create one-click deployment script")
