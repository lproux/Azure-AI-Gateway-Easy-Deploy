#!/usr/bin/env python3
"""
Automated MCP Server Redeployment (Non-Interactive Version)
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
            print(f" ❌")
            print(f"     Error: {result.stderr[:200]}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        print(" ⏱ Timeout")
        return False, "Timeout"
    except Exception as e:
        print(f" ❌ {type(e).__name__}: {str(e)[:100]}")
        return False, str(e)

def delete_container_app(app_name):
    """Delete a single container app"""
    cmd = f"az containerapp delete --name {app_name} --resource-group {RESOURCE_GROUP} --yes --output none 2>&1"
    return run_command(cmd, f"Deleting {app_name}", timeout=60)

def check_deployment_exists(deployment_name):
    """Check if deployment already exists"""
    cmd = f"az deployment group show --name {deployment_name} --resource-group {RESOURCE_GROUP} -o json 2>&1"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        return result.returncode == 0
    except:
        return False

def deploy_mcp_servers():
    """Deploy MCP servers using Bicep"""
    print("\n3️⃣ Deploying MCP servers...")

    # Check if Bicep file exists
    bicep_file = "deploy-04-mcp.bicep"
    json_file = "deploy-04-mcp.json"

    import os
    if not os.path.exists(json_file):
        print(f"  ℹ️  {json_file} not found, trying to compile Bicep...")

        if os.path.exists(bicep_file):
            compile_cmd = f"az bicep build --file {bicep_file} 2>&1"
            success, output = run_command(compile_cmd, f"Compiling {bicep_file}")
            if not success:
                return False, "Bicep compilation failed"
        else:
            print(f"  ❌ Neither {bicep_file} nor {json_file} found")
            return False, "Template files not found"

    # Deploy
    deploy_cmd = f"""az deployment group create \
        --name {DEPLOYMENT_NAME} \
        --resource-group {RESOURCE_GROUP} \
        --template-file {json_file} \
        --output json 2>&1"""

    print(f"  🚀 Deploying MCP servers (this may take 3-5 minutes)...")
    print(f"     Please wait...")

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
            print(f"  ❌ Deployment failed")
            print(f"     {result.stderr[:300]}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        print("  ⏱ Deployment timed out (may still be running in background)")
        return False, "Timeout"
    except Exception as e:
        print(f"  ❌ Deployment error: {type(e).__name__}")
        print(f"     {str(e)[:200]}")
        return False, str(e)

def get_deployment_outputs(deployment_name):
    """Get outputs from deployment"""
    cmd = f"az deployment group show --name {deployment_name} --resource-group {RESOURCE_GROUP} --query properties.outputs -o json 2>&1"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
        return {}
    except:
        return {}

def update_env_file(mcp_urls):
    """Update master-lab.env with new MCP server URLs"""
    print("\n4️⃣ Updating master-lab.env...")

    try:
        # Read current env file
        with open('master-lab.env', 'r') as f:
            lines = f.readlines()

        # Remove old MCP_SERVER lines and rebuild
        updated_lines = []
        in_mcp_section = False

        for line in lines:
            # Skip old MCP_SERVER lines
            if line.strip().startswith('MCP_SERVER_') and '_URL=' in line:
                if not in_mcp_section:
                    in_mcp_section = True
                    # Insert new MCP URLs here
                    for mcp in mcp_urls:
                        name = mcp.get('name', '').upper().replace('-', '_')
                        url = mcp.get('url', '')
                        if name and url:
                            updated_lines.append(f"MCP_SERVER_{name}_URL={url}\n")
                continue  # Skip old line
            else:
                updated_lines.append(line)

        # Write updated env file
        with open('master-lab.env', 'w') as f:
            f.writelines(updated_lines)

        print("  ✅ master-lab.env updated with new URLs")

        # Also update .mcp-servers-config
        print("  ⏳ Updating .mcp-servers-config...", end="", flush=True)
        config_lines = ["# MCP Server Configuration (Auto-updated)\n\n"]
        for mcp in mcp_urls:
            name = mcp.get('name', '').upper().replace('-', '_')
            url = mcp.get('url', '')
            if name and url:
                config_lines.append(f"MCP_SERVER_{name}_URL={url}\n")

        with open('.mcp-servers-config', 'w') as f:
            f.writelines(config_lines)
        print(" ✅")

        return True

    except Exception as e:
        print(f"  ❌ Failed to update files: {e}")
        return False

def main():
    print("=" * 80)
    print("🔄 MCP SERVER AUTOMATED REDEPLOYMENT")
    print("=" * 80)
    print()
    print("⚠️  This will delete all existing MCP Container Apps and redeploy fresh")
    print()

    start_time = time.time()

    # Step 1: Delete existing apps
    print("1️⃣ Deleting existing MCP Container Apps...")
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
        print(f"      (May not exist - continuing anyway)")

    # Step 2: Wait for deletions to complete
    print("\n2️⃣ Waiting for deletions to complete...")
    for i in range(15, 0, -5):
        print(f"  ⏳ {i} seconds...", end="", flush=True)
        time.sleep(5)
        print(" ✓")
    print("  ✅ Done")

    # Step 3: Deploy new MCP servers
    success, deployment_result = deploy_mcp_servers()

    if not success:
        print("\n" + "=" * 80)
        print("❌ DEPLOYMENT FAILED")
        print("=" * 80)
        print("\n💡 Possible solutions:")
        print("   1. Check Azure CLI is logged in: az login")
        print("   2. Check Bicep files exist: deploy-04-mcp.bicep or .json")
        print("   3. Check Azure permissions")
        print("   4. Run deployment manually from notebook cell")
        return 2

    # Step 4: Get new URLs from deployment outputs
    print("\n4️⃣ Retrieving new server URLs...")
    outputs = get_deployment_outputs(DEPLOYMENT_NAME)

    mcp_urls = []
    if outputs and 'mcpServerUrls' in outputs:
        mcp_urls = outputs['mcpServerUrls'].get('value', [])
        print(f"  ✅ Retrieved {len(mcp_urls)} server URLs")
        for mcp in mcp_urls:
            name = mcp.get('name', 'unknown')
            url = mcp.get('url', 'unknown')
            print(f"     • {name}: {url[:60]}...")
    else:
        print("  ⚠️  Could not retrieve URLs from deployment outputs")
        print("      Trying to query Container Apps directly...")

        # Fallback: Query apps directly
        for server in SERVERS:
            app_name = f"mcp-{server}-pavavy6pu5"
            cmd = f"az containerapp show --name {app_name} --resource-group {RESOURCE_GROUP} --query properties.configuration.ingress.fqdn -o tsv 2>&1"
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
                if result.returncode == 0 and result.stdout.strip():
                    fqdn = result.stdout.strip()
                    mcp_urls.append({"name": server, "url": f"https://{fqdn}"})
            except:
                pass

        if mcp_urls:
            print(f"  ✅ Retrieved {len(mcp_urls)} URLs from direct query")

    # Step 5: Update env files
    if mcp_urls:
        update_env_file(mcp_urls)
    else:
        print("\n  ⚠️  No URLs retrieved - you'll need to manually update master-lab.env")

    # Step 6: Test connectivity
    print("\n5️⃣ Testing new server connectivity...")
    print("  ⏳ Waiting 45 seconds for servers to fully start...")
    for i in range(45, 0, -15):
        print(f"     {i}s...", end="", flush=True)
        time.sleep(15)
        print(" ✓")

    print("\n  🔍 Running connectivity test...")
    test_cmd = "python3 test_mcp_servers.py 2>&1"
    success, test_output = run_command(test_cmd, "Testing all servers", timeout=90)

    if success and test_output:
        print("\n" + "-" * 80)
        print(test_output)
        print("-" * 80)

    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)

    print("\n" + "=" * 80)
    print("✅ REDEPLOYMENT COMPLETE")
    print("=" * 80)
    print(f"\n⏱  Total time: {minutes}m {seconds}s")
    print()
    print("📋 Next steps:")
    print("   1. Review test results above")
    print("   2. If any servers still fail, check Azure Portal")
    print("   3. Re-run Cell 2 in notebook (MCP Client Initialization)")
    print("   4. All servers should now return HTTP 200")
    print()

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {type(e).__name__}: {e}")
        sys.exit(1)
