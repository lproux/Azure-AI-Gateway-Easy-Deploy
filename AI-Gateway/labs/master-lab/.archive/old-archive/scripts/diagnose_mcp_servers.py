#!/usr/bin/env python3
"""
Deep diagnostic for MCP Container Apps
Checks status, logs, revisions, and identifies the root cause
"""

import subprocess
import json
import sys

RESOURCE_GROUP = "lab-master-lab"
SERVERS = ["weather", "oncall", "github", "spotify", "product-catalog", "place-order", "ms-learn"]

def run_az_command(cmd, description):
    """Run Azure CLI command and return parsed JSON output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            print(f"  ❌ {description} failed: {result.stderr[:100]}")
            return None

        # Try to parse as JSON if possible
        try:
            return json.loads(result.stdout) if result.stdout.strip() else None
        except json.JSONDecodeError:
            return result.stdout
    except subprocess.TimeoutExpired:
        print(f"  ⏱ {description} timed out")
        return None
    except Exception as e:
        print(f"  ❌ {description} error: {e}")
        return None

def diagnose_container_app(app_name):
    """Comprehensive diagnostic for a single container app"""
    print(f"\n{'='*80}")
    print(f"🔍 DIAGNOSING: {app_name}")
    print(f"{'='*80}")

    issues = []

    # 1. Check if app exists
    print("\n1️⃣ Checking if app exists...")
    show_cmd = f"az containerapp show --name {app_name} --resource-group {RESOURCE_GROUP} -o json"
    app_info = run_az_command(show_cmd, "App show")

    if not app_info:
        issues.append("App does not exist or cannot be accessed")
        return issues

    print(f"  ✅ App exists")

    # 2. Check provisioning state
    print("\n2️⃣ Checking provisioning state...")
    prov_state = app_info.get('properties', {}).get('provisioningState', 'Unknown')
    running_status = app_info.get('properties', {}).get('runningStatus', 'Unknown')
    print(f"  Provisioning: {prov_state}")
    print(f"  Running Status: {running_status}")

    if prov_state != 'Succeeded':
        issues.append(f"Provisioning state is {prov_state} (expected: Succeeded)")
    if running_status != 'Running':
        issues.append(f"Running status is {running_status} (expected: Running)")

    # 3. Check ingress configuration
    print("\n3️⃣ Checking ingress configuration...")
    ingress = app_info.get('properties', {}).get('configuration', {}).get('ingress', {})

    if not ingress:
        issues.append("Ingress is not configured")
    else:
        external = ingress.get('external', False)
        target_port = ingress.get('targetPort', 'Unknown')
        fqdn = ingress.get('fqdn', 'Unknown')

        print(f"  External: {external}")
        print(f"  Target Port: {target_port}")
        print(f"  FQDN: {fqdn}")

        if not external:
            issues.append("Ingress is not external (should be True)")
        if target_port not in [80, 8080]:
            issues.append(f"Target port is {target_port} (expected 80 or 8080)")

    # 4. Check active revisions
    print("\n4️⃣ Checking active revisions...")
    revisions_cmd = f"az containerapp revision list --name {app_name} --resource-group {RESOURCE_GROUP} -o json"
    revisions = run_az_command(revisions_cmd, "Revisions list")

    if revisions:
        active_revisions = [r for r in revisions if r.get('properties', {}).get('active', False)]
        print(f"  Total revisions: {len(revisions)}")
        print(f"  Active revisions: {len(active_revisions)}")

        if len(active_revisions) == 0:
            issues.append("No active revisions found")
        else:
            # Check latest active revision
            latest = active_revisions[0]
            replica_count = latest.get('properties', {}).get('replicas', 0)
            health_state = latest.get('properties', {}).get('healthState', 'Unknown')
            prov_state = latest.get('properties', {}).get('provisioningState', 'Unknown')

            print(f"  Latest active revision: {latest.get('name', 'Unknown')}")
            print(f"    Replicas: {replica_count}")
            print(f"    Health State: {health_state}")
            print(f"    Provisioning State: {prov_state}")

            if replica_count == 0:
                issues.append("Active revision has 0 replicas")
            if health_state != 'Healthy':
                issues.append(f"Health state is {health_state} (expected: Healthy)")
            if prov_state not in ['Succeeded', 'Provisioned']:
                issues.append(f"Revision provisioning state is {prov_state}")

    # 5. Check container configuration
    print("\n5️⃣ Checking container configuration...")
    containers = app_info.get('properties', {}).get('template', {}).get('containers', [])

    if not containers:
        issues.append("No containers defined")
    else:
        for i, container in enumerate(containers):
            print(f"  Container {i+1}: {container.get('name', 'Unknown')}")
            print(f"    Image: {container.get('image', 'Unknown')}")

            # Check if image exists/is accessible
            image = container.get('image', '')
            if not image:
                issues.append(f"Container {i+1} has no image specified")

    # 6. Check recent logs (last 50 lines)
    print("\n6️⃣ Checking recent logs...")
    logs_cmd = f"az containerapp logs show --name {app_name} --resource-group {RESOURCE_GROUP} --tail 50 --output table"
    logs = run_az_command(logs_cmd, "Logs fetch")

    if logs:
        print("  Recent logs (last 50 lines):")
        print("  " + "-" * 70)
        log_lines = str(logs).split('\n')[:10]  # Show first 10 for brevity
        for line in log_lines:
            print(f"  {line}")
        if len(str(logs).split('\n')) > 10:
            print(f"  ... ({len(str(logs).split('\n')) - 10} more lines)")
    else:
        issues.append("Could not fetch logs")

    return issues

def main():
    print("=" * 80)
    print("🔍 MCP CONTAINER APPS DEEP DIAGNOSTIC")
    print("=" * 80)
    print()

    all_issues = {}

    for server in SERVERS:
        app_name = f"mcp-{server}-pavavy6pu5"
        issues = diagnose_container_app(app_name)
        all_issues[server] = issues

    # Summary
    print("\n" + "=" * 80)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 80)

    for server, issues in all_issues.items():
        print(f"\n{server.upper()}:")
        if not issues:
            print("  ✅ No issues detected")
        else:
            for issue in issues:
                print(f"  ❌ {issue}")

    # Recommendations
    print("\n" + "=" * 80)
    print("💡 RECOMMENDATIONS")
    print("=" * 80)

    common_issues = {}
    for server, issues in all_issues.items():
        for issue in issues:
            common_issues[issue] = common_issues.get(issue, 0) + 1

    if common_issues:
        print("\nCommon issues affecting multiple servers:")
        for issue, count in sorted(common_issues.items(), key=lambda x: x[1], reverse=True):
            if count > 1:
                print(f"  [{count}/{len(SERVERS)} servers] {issue}")

    # Determine best fix strategy
    print("\n" + "=" * 80)
    print("🔧 RECOMMENDED FIX STRATEGY")
    print("=" * 80)

    if any("No containers defined" in issues for issues in all_issues.values()):
        print("\n❌ CRITICAL: Containers not defined properly")
        print("   → RECOMMENDATION: Redeploy MCP servers from scratch")
        print("   → Use deployment cell in notebook")
        return 2

    elif any("Active revision has 0 replicas" in issues for issues in all_issues.values()):
        print("\n⚠ Replicas not starting")
        print("   → RECOMMENDATION: Check logs and restart revisions")
        print("   → Or redeploy if logs show image/startup failures")
        return 1

    elif any("Ingress is not external" in issues for issues in all_issues.values()):
        print("\n⚠ Ingress misconfigured")
        print("   → RECOMMENDATION: Fix ingress configuration")
        return 1

    else:
        print("\n⚠ Multiple issues detected")
        print("   → RECOMMENDATION: Fastest solution is to redeploy")
        return 2

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
