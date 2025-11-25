#!/usr/bin/env python3
"""
Auto-fix environment variables for AI Gateway notebook
Extracts missing values from Azure and updates master-lab.env
"""

import os
import subprocess
import json
from pathlib import Path

print("="*80)
print("Auto-Fix Environment Variables")
print("="*80)

ENV_FILE = Path("master-lab.env")
RESOURCE_GROUP = "lab-master-lab"

# Step 1: Get Subscription ID
print("\n[1/4] Getting subscription ID...")
try:
    result = subprocess.run(
        ["az", "account", "show", "--query", "id", "-o", "tsv"],
        capture_output=True,
        text=True,
        check=True
    )
    subscription_id = result.stdout.strip()
    print(f"✅ Subscription ID: {subscription_id}")
except Exception as e:
    print(f"❌ Failed to get subscription ID: {e}")
    print("💡 Run: az login")
    subscription_id = None

# Step 2: Get Azure OpenAI Foundry endpoints
print("\n[2/4] Getting Azure OpenAI Foundry endpoints...")
foundries = {}

try:
    result = subprocess.run(
        ["az", "cognitiveservices", "account", "list",
         "--resource-group", RESOURCE_GROUP,
         "--query", "[?contains(name, 'foundry')].[name,properties.endpoint]",
         "-o", "json"],
        capture_output=True,
        text=True,
        check=True
    )

    accounts = json.loads(result.stdout)
    for name, endpoint in accounts:
        # Get keys
        key_result = subprocess.run(
            ["az", "cognitiveservices", "account", "keys", "list",
             "--resource-group", RESOURCE_GROUP,
             "--name", name,
             "--query", "key1",
             "-o", "tsv"],
            capture_output=True,
            text=True,
            check=True
        )
        key = key_result.stdout.strip()

        if 'foundry1' in name:
            foundries['FOUNDRY1'] = (endpoint, key)
            print(f"✅ Foundry 1 (UK South): {endpoint}")
        elif 'foundry2' in name:
            foundries['FOUNDRY2'] = (endpoint, key)
            print(f"✅ Foundry 2 (East US): {endpoint}")
        elif 'foundry3' in name:
            foundries['FOUNDRY3'] = (endpoint, key)
            print(f"✅ Foundry 3 (Norway East): {endpoint}")

except Exception as e:
    print(f"❌ Failed to get foundry endpoints: {e}")

# Step 3: Read current .env file
print("\n[3/4] Reading current master-lab.env...")
env_lines = []
if ENV_FILE.exists():
    with open(ENV_FILE, 'r') as f:
        env_lines = f.readlines()
    print(f"✅ Found {len(env_lines)} existing lines")
else:
    print("❌ master-lab.env not found!")

# Step 4: Update .env file
print("\n[4/4] Updating master-lab.env...")

# Check if variables already exist
has_subscription = any('SUBSCRIPTION_ID=' in line for line in env_lines)
has_foundry1 = any('AZURE_OPENAI_ENDPOINT_FOUNDRY1=' in line for line in env_lines)

if has_subscription and has_foundry1:
    print("✅ All variables already present")
else:
    # Append missing variables
    additions = []

    if not has_subscription and subscription_id:
        additions.append(f"\n# Azure Subscription (Auto-added {Path(__file__).name})\n")
        additions.append(f"SUBSCRIPTION_ID={subscription_id}\n")

    if not has_foundry1 and foundries:
        additions.append(f"\n# Azure OpenAI Foundries - For Backend Pool (Auto-added)\n")
        for name, (endpoint, key) in sorted(foundries.items()):
            additions.append(f"AZURE_OPENAI_ENDPOINT_{name}={endpoint}\n")
            additions.append(f"AZURE_OPENAI_KEY_{name}={key}\n")

    if additions:
        with open(ENV_FILE, 'a') as f:
            f.writelines(additions)
        print(f"✅ Added {len(additions)} lines to {ENV_FILE}")
    else:
        print("⚠️ No additions needed (or values not found)")

print("\n" + "="*80)
print("Environment Update Complete!")
print("="*80)
print("\nNext steps:")
print("1. Review master-lab.env to verify values")
print("2. Ensure .azure-credentials.env exists (for service principal)")
print("3. Run notebook cells")
