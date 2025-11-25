#!/usr/bin/env python3
"""
Create Service Principal using Python and Azure SDK
No PowerShell or Bash required - pure Python!
"""

import os
import json
import subprocess
from datetime import datetime

def run_az_command(cmd):
    """Run az CLI command and return JSON output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout) if result.stdout.strip() else None
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {e.stderr}")
        return None
    except json.JSONDecodeError:
        return result.stdout.strip()

print("=" * 70)
print("Creating Service Principal for Master Lab")
print("=" * 70)
print()

# Get subscription info
print("[*] Getting subscription information...")
subscription_info = run_az_command("az account show --output json")

if not subscription_info:
    print("[ERROR] Failed to get subscription. Make sure you're logged in:")
    print("        az login")
    exit(1)

subscription_id = subscription_info['id']
subscription_name = subscription_info['name']

print(f"[OK] Subscription: {subscription_name}")
print(f"[OK] Subscription ID: {subscription_id}")
print()

# Service Principal name with timestamp to avoid conflicts
sp_name = f"master-lab-sp-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
print(f"[*] Service Principal Name: {sp_name}")
print()

# Create Service Principal
print("[*] Creating Service Principal...")
print("[*] This will have Contributor role on the subscription")
print()

sp_output = run_az_command(
    f'az ad sp create-for-rbac '
    f'--name "{sp_name}" '
    f'--role Contributor '
    f'--scopes "/subscriptions/{subscription_id}" '
    f'--output json'
)

if not sp_output:
    print("[ERROR] Failed to create Service Principal")
    print("[INFO] Make sure you have permissions to create App Registrations")
    exit(1)

# Extract credentials
tenant_id = sp_output['tenant']
client_id = sp_output['appId']
client_secret = sp_output['password']

print()
print("=" * 70)
print("Service Principal Created Successfully!")
print("=" * 70)
print()
print("Credentials (save these securely!):")
print(f"  Tenant ID:     {tenant_id}")
print(f"  Client ID:     {client_id}")
print(f"  Client Secret: {client_secret}")
print()

# Create .azure-credentials.env file
env_content = f"""# Azure Service Principal Credentials
# Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Service Principal: {sp_name}

AZURE_TENANT_ID={tenant_id}
AZURE_CLIENT_ID={client_id}
AZURE_CLIENT_SECRET={client_secret}
AZURE_SUBSCRIPTION_ID={subscription_id}
"""

credentials_file = '.azure-credentials.env'
with open(credentials_file, 'w') as f:
    f.write(env_content)

print("=" * 70)
print("Created .azure-credentials.env")
print("=" * 70)
print()
print(f"[OK] File: {os.path.abspath(credentials_file)}")
print("[OK] This file is in .gitignore (not committed to git)")
print()
print("=" * 70)
print("Next Steps")
print("=" * 70)
print()
print("1. The .azure-credentials.env file is ready")
print("2. Run Cell 13 in the notebook to test authentication")
print("3. Run Cell 15 to start deployment")
print()
print("=" * 70)
print("To Delete Service Principal Later")
print("=" * 70)
print()
print(f"  az ad sp delete --id {client_id}")
print()
print("=" * 70)
