#!/usr/bin/env python3
"""
Fix MCP Server Port Mismatch
Issue: Container Apps configured for port 8080, but containers listen on port 80
"""

import subprocess
import sys
import time

RESOURCE_GROUP = "lab-master-lab"
SERVERS = ["weather", "oncall", "github", "spotify", "product-catalog", "place-order", "ms-learn"]

def run_command(cmd, description):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def fix_server_port(app_name):
    """Fix port configuration for a single MCP server"""
    print(f"🔧 Fixing: {app_name}")

    cmd = f"""az containerapp ingress update \
        --name {app_name} \
        --resource-group {RESOURCE_GROUP} \
        --target-port 80 \
        --output none"""

    success, stdout, stderr = run_command(cmd, f"Update {app_name} port")

    if success:
        print(f"  ✅ Port updated to 80")
        return True
    else:
        print(f"  ❌ Failed: {stderr[:100]}")
        return False

def main():
    print("=" * 60)
    print("MCP SERVER PORT FIX")
    print("=" * 60)
    print()
    print(f"📋 Fixing port configuration for {len(SERVERS)} MCP servers...")
    print()

    results = {"success": [], "failed": []}

    for server in SERVERS:
        app_name = f"mcp-{server}-pavavy6pu5"

        if fix_server_port(app_name):
            results["success"].append(server)
        else:
            results["failed"].append(server)

        print("---")

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✅ Fixed: {len(results['success'])}/{len(SERVERS)}")
    print(f"❌ Failed: {len(results['failed'])}/{len(SERVERS)}")

    if results["failed"]:
        print(f"\nFailed servers: {', '.join(results['failed'])}")

    print()
    print("⏳ Wait 30-60 seconds for replicas to start...")
    print()
    print("Then test connectivity:")
    print("  python3 test_mcp_servers.py")
    print()

    return 0 if len(results["failed"]) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
