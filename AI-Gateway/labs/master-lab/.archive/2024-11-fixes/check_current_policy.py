#!/usr/bin/env python3
"""
Check current APIM semantic caching policy
"""
import subprocess
import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('master-lab.env')

apim_service_id = os.environ.get('APIM_SERVICE_ID')

if not apim_service_id:
    print("❌ APIM_SERVICE_ID not found in master-lab.env")
    exit(1)

print("=" * 80)
print("🔍 CHECKING CURRENT APIM POLICY")
print("=" * 80)
print(f"\nAPIM Service ID: {apim_service_id}")

uri = f"https://management.azure.com{apim_service_id}/apis/inference-api/policies/policy?api-version=2023-09-01-preview"

cmd = ['az', 'rest', '--method', 'get', '--uri', uri]

print(f"\nFetching policy...")
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    # Debug: show what we got
    print(f"DEBUG: stdout length = {len(result.stdout)}")
    print(f"DEBUG: first 100 chars = {result.stdout[:100]}")

    if not result.stdout.strip():
        print("\n❌ Error: Empty response from Azure")
        print("   Stderr:", result.stderr)
        exit(1)

    # Handle UTF-8 BOM if present
    stdout_text = result.stdout.encode('utf-8').decode('utf-8-sig').strip()

    try:
        policy_data = json.loads(stdout_text)
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON decode error: {e}")
        print(f"Response text: {stdout_text[:500]}")
        exit(1)
    policy_xml = policy_data.get('properties', {}).get('value', '')

    print("\n" + "=" * 80)
    print("CURRENT POLICY")
    print("=" * 80)
    print(policy_xml)
    print("=" * 80)

    # Check for key elements
    print("\n🔍 Policy Analysis:")

    if 'azure-openai-semantic-cache-lookup' in policy_xml:
        print("✅ Semantic cache lookup present")

        if 'embeddings-backend-auth="system-assigned"' in policy_xml:
            print("✅ System-assigned auth configured")
        else:
            print("❌ MISSING: embeddings-backend-auth=\"system-assigned\"")
            print("   This is why embeddings are failing with 500 errors!")
    else:
        print("❌ Semantic cache lookup NOT FOUND")

    if 'azure-openai-semantic-cache-store' in policy_xml:
        print("✅ Semantic cache store present")

        if 'duration="1200"' in policy_xml:
            print("✅ Cache duration: 20 minutes (1200s)")
        elif 'duration="120"' in policy_xml:
            print("⚠️  Cache duration: 2 minutes (120s) - should be 1200s")
    else:
        print("⚠️  Semantic cache store NOT FOUND")

else:
    print(f"\n❌ Error fetching policy:")
    print(result.stderr)
