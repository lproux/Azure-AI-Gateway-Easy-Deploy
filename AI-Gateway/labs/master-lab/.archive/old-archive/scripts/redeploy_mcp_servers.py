#!/usr/bin/env python3
"""
Automated MCP Server Redeployment
Deletes broken Container Apps and redeploys fresh, then updates master-lab.env
"""

import subprocess
import json
import sys
import time
from datetime import datetime

RESOURCE_GROUP = "lab-master-lab"
SERVERS = ["weather", "oncall", "github", "spotify", "product-catalog", "place-order", "ms-learn"]
DEPLOYMENT_NAME = "master-lab-04-mcp-redeploy"

def run_command(cmd, description, timeout=120):
    """Run command with error handling"""
    try:
        print(f"  ⏳ {description}...", end="", flush=True)
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            print(" ✅")
            return True, result.stdout
        else:
            print(f" ❌\n     Error: {result.stderr[:150]}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        print(" ⏱ Timeout")
        return False, "Timeout"
    except Exception as e:
        print(f" ❌ {type(e).__name__}")
        return False, str(e)

def delete_container_app(app_name):
    """Delete a single container app"""
    cmd = f"az containerapp delete --name {app_name} --resource-group {RESOURCE_GROUP} --yes --output none"
    return run_command(cmd, f"Deleting {app_name}", timeout=60)

def check_deployment_exists(deployment_name):
    """Check if deployment already exists"""
    cmd = f"az deployment group show --name {deployment_name} --resource-group {RESOURCE_GROUP} -o json"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        return result.returncode == 0
    except:
        return False

def deploy_mcp_servers():
    """Deploy MCP servers using Bicep"""
    print("\n4️⃣ Deploying MCP servers...")

    # Check if deployment already exists
    if check_deployment_exists(DEPLOYMENT_NAME):
        print("  ℹ️  Deployment already exists, using existing...")
        return True, None

    # Compile Bicep
    bicep_file = "deploy-04-mcp.bicep"
    json_file = "deploy-04-mcp.json"

    print(f"  📝 Compiling {bicep_file}...")
    compile_cmd = f"az bicep build --file {bicep_file}"
    success, output = run_command(compile_cmd, "Compiling Bicep")

    if not success:
        return False, "Bicep compilation failed"

    # Deploy
    deploy_cmd = f"""az deployment group create \
        --name {DEPLOYMENT_NAME} \
        --resource-group {RESOURCE_GROUP} \
        --template-file {json_file} \
        --output json"""

    print(f"  🚀 Deploying MCP servers (this may take 3-5 minutes)...")
    try:
        result = subprocess.run(
            deploy_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=600  # 10 minutes max
        )
        if result.returncode == 0:
            print("  ✅ Deployment complete")
            try:
                return True, json.loads(result.stdout)
            except:
                return True, result.stdout
        else:
            print(f"  ❌ Deployment failed: {result.stderr[:150]}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        print("  ⏱ Deployment timed out (may still be running)")
        return False, "Timeout"
    except Exception as e:
        print(f"  ❌ Deployment error: {type(e).__name__}")
        return False, str(e)

def get_deployment_outputs(deployment_name):
    """Get outputs from deployment"""
    cmd = f"az deployment group show --name {deployment_name} --resource-group {RESOURCE_GROUP} --query properties.outputs -o json"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return json.loads(result.stdout)
        return {}
    except:
        return {}

def update_env_file(mcp_urls):
    """Update master-lab.env with new MCP server URLs"""
    print("\n5️⃣ Updating master-lab.env...")

    try:
        # Read current env file
        with open('master-lab.env', 'r') as f:
            lines = f.readlines()

        # Update MCP server URLs
        updated_lines = []
        mcp_section_found = False

        for line in lines:
            # Keep non-MCP lines
            if not line.strip().startswith('MCP_SERVER_'):
                updated_lines.append(line)
            # Mark that we're in MCP section
            elif line.strip().startswith('MCP_SERVER_'):
                if not mcp_section_found:
                    mcp_section_found = True
                    # Add updated MCP URLs
                    for mcp in mcp_urls:
                        name = mcp.get('name', '').upper().replace('-', '_')
                        url = mcp.get('url', '')
                        updated_lines.append(f"MCP_SERVER_{name}_URL={url}\n")

        # Write updated env file
        with open('master-lab.env', 'w') as f:
            f.writelines(updated_lines)

        print("  ✅ master-lab.env updated")
        return True

    except Exception as e:
        print(f"  ❌ Failed to update env file: {e}")
        return False

def main():
    print("=" * 80)
    print("🔄 MCP SERVER AUTOMATED REDEPLOYMENT")
    print("=" * 80)
    print()
    print("⚠️  WARNING: This will delete all existing MCP Container Apps")
    print("   and redeploy them fresh.")
    print()

    # Confirmation
    response = input("Continue? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("\n❌ Cancelled")
        return 1

    start_time = time.time()

    # Step 1: Delete existing apps
    print("\n1️⃣ Deleting existing MCP Container Apps...")
    delete_results = {"success": [], "failed": []}

    for server in SERVERS:
        app_name = f"mcp-{server}-pavavy6pu5"
        success, _ = delete_container_app(app_name)

        if success:
            delete_results["success"].append(server)
        else:
            delete_results["failed"].append(server)

    print(f"\n  📊 Deleted: {len(delete_results['success'])}/{len(SERVERS)}")
    if delete_results["failed"]:
        print(f"  ⚠️  Failed to delete: {', '.join(delete_results['failed'])}")

    # Step 2: Wait for deletions to complete
    print("\n2️⃣ Waiting for deletions to complete...")
    time.sleep(10)
    print("  ✅ Done")

    # Step 3: Deploy new MCP servers
    print("\n3️⃣ Deploying new MCP servers...")
    success, deployment_result = deploy_mcp_servers()

    if not success:
        print("\n❌ DEPLOYMENT FAILED")
        print("   Manual intervention required")
        return 2

    # Step 4: Get new URLs from deployment outputs
    print("\n4️⃣ Retrieving new server URLs...")
    outputs = get_deployment_outputs(DEPLOYMENT_NAME)

    mcp_urls = []
    if outputs and 'mcpServerUrls' in outputs:
        mcp_urls = outputs['mcpServerUrls'].get('value', [])
        print(f"  ✅ Retrieved {len(mcp_urls)} server URLs")

    if not mcp_urls:
        print("  ⚠️  Could not retrieve URLs from deployment")
        print("   You may need to manually update master-lab.env")

    # Step 5: Update env file
    if mcp_urls:
        update_env_file(mcp_urls)

    # Step 6: Test connectivity
    print("\n6️⃣ Testing new server connectivity...")
    print("  ⏳ Waiting 30 seconds for servers to start...")
    time.sleep(30)

    test_cmd = "python3 test_mcp_servers.py"
    run_command(test_cmd, "Running connectivity test", timeout=60)

    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)

    print("\n" + "=" * 80)
    print("✅ REDEPLOYMENT COMPLETE")
    print("=" * 80)
    print(f"\n⏱  Total time: {minutes}m {seconds}s")
    print()
    print("📋 Next steps:")
    print("   1. Check test results above")
    print("   2. Re-run Cell 2 in notebook (MCP Client Initialization)")
    print("   3. Verify all 7 servers return HTTP 200")
    print()

    return 0

if __name__ == "__main__":
    sys.exit(main())
