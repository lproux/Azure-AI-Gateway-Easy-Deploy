# Fix MCP Server Port Mismatch (Notebook Cell Version)
# Issue: Container Apps configured for port 8080, but containers listen on port 80
# Run this cell once to fix all 7 MCP servers

import subprocess
import time
from IPython.display import display, HTML

print("=" * 80)
print("🔧 MCP SERVER PORT FIX")
print("=" * 80)
print()

RESOURCE_GROUP = "lab-master-lab"
SERVERS = ["weather", "oncall", "github", "spotify", "product-catalog", "place-order", "ms-learn"]

print(f"📋 Fixing port configuration for {len(SERVERS)} MCP servers...")
print(f"   Issue: TargetPort 8080 → Changing to 80 (actual listening port)")
print()

results = {"success": [], "failed": []}

for server in SERVERS:
    app_name = f"mcp-{server}-pavavy6pu5"

    print(f"🔧 {app_name}... ", end="", flush=True)

    try:
        cmd = [
            "az", "containerapp", "ingress", "update",
            "--name", app_name,
            "--resource-group", RESOURCE_GROUP,
            "--target-port", "80",
            "--output", "none"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            print("✅ Fixed")
            results["success"].append(server)
        else:
            print(f"❌ Failed: {result.stderr[:50]}")
            results["failed"].append(server)
    except subprocess.TimeoutExpired:
        print("⏱ Timeout")
        results["failed"].append(server)
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}")
        results["failed"].append(server)

print()
print("=" * 80)
print("📊 SUMMARY")
print("=" * 80)
print(f"✅ Fixed: {len(results['success'])}/{len(SERVERS)} servers")
print(f"❌ Failed: {len(results['failed'])}/{len(SERVERS)} servers")

if results["failed"]:
    print(f"\n⚠ Failed servers: {', '.join(results['failed'])}")
    print("   Try running this cell again or fix manually in Azure Portal")

if len(results['success']) > 0:
    print()
    print("⏳ IMPORTANT: Wait 30-60 seconds for new replicas to start!")
    print()
    print("✅ Next steps:")
    print("   1. Wait 60 seconds")
    print("   2. Run: !python3 test_mcp_servers.py")
    print("   3. Or re-run Cell 2 (MCP Client Initialization)")

    # Display countdown
    print()
    print("⏱ Waiting 60 seconds for replicas to start...", end="", flush=True)
    for i in range(60, 0, -10):
        print(f" {i}s", end="", flush=True)
        time.sleep(10)
    print(" Done!")

    # Auto-test connectivity
    print()
    print("🔍 Testing connectivity...")
    try:
        test_result = subprocess.run(
            ["python3", "test_mcp_servers.py"],
            capture_output=True,
            text=True,
            timeout=60
        )
        print(test_result.stdout)
    except Exception as e:
        print(f"❌ Could not run test: {e}")
        print("   Manually run: python3 test_mcp_servers.py")

print()
print("=" * 80)
