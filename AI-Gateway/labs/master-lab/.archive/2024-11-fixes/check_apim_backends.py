#!/usr/bin/env python3
"""
Check APIM backends configuration
"""
import subprocess
import json
import os
from dotenv import load_dotenv

load_dotenv('master-lab.env')

apim_service_id = os.environ.get('APIM_SERVICE_ID')

if not apim_service_id:
    print("❌ APIM_SERVICE_ID not found in master-lab.env")
    exit(1)

print("=" * 80)
print("🔍 CHECKING APIM BACKENDS")
print("=" * 80)
print(f"\nAPIM Service ID: {apim_service_id}\n")

# List all backends
uri = f"https://management.azure.com{apim_service_id}/backends?api-version=2023-09-01-preview"
cmd = ['az', 'rest', '--method', 'get', '--uri', uri]

print("[*] Fetching all backends...")
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    try:
        data = json.loads(result.stdout.encode('utf-8').decode('utf-8-sig').strip())
        backends = data.get('value', [])

        print(f"\n✅ Found {len(backends)} backend(s)\n")

        for backend in backends:
            backend_id = backend.get('name', 'Unknown')
            props = backend.get('properties', {})
            url = props.get('url', 'N/A')
            protocol = props.get('protocol', 'N/A')

            print(f"{'='*80}")
            print(f"Backend ID: {backend_id}")
            print(f"{'='*80}")
            print(f"URL: {url}")
            print(f"Protocol: {protocol}")

            # Check for credentials/auth
            credentials = props.get('credentials', {})
            if credentials:
                print(f"Credentials configured: Yes")
                auth_header = credentials.get('header', {})
                if auth_header:
                    print(f"  Header auth: {list(auth_header.keys())}")
                auth_query = credentials.get('query', {})
                if auth_query:
                    print(f"  Query auth: {list(auth_query.keys())}")
            else:
                print(f"Credentials configured: No (might use managed identity)")

            # Check for managed identity
            if 'identity' in backend:
                print(f"Managed Identity: {backend.get('identity', {}).get('type', 'None')}")

            print()

        # Check specifically for embeddings-backend
        print(f"\n{'='*80}")
        print("CHECKING FOR 'embeddings-backend'")
        print(f"{'='*80}")

        embeddings_backend = next((b for b in backends if b.get('name') == 'embeddings-backend'), None)

        if embeddings_backend:
            print("✅ 'embeddings-backend' exists")
            props = embeddings_backend.get('properties', {})
            print(f"\nConfiguration:")
            print(f"  URL: {props.get('url', 'N/A')}")
            print(f"  Protocol: {props.get('protocol', 'N/A')}")

            # Full details
            print(f"\nFull backend configuration:")
            print(json.dumps(embeddings_backend, indent=2))
        else:
            print("❌ 'embeddings-backend' NOT FOUND!")
            print("\nThis is why semantic caching fails!")
            print("The policy references 'embeddings-backend' but it doesn't exist.")
            print("\nAvailable backends:")
            for b in backends:
                print(f"  - {b.get('name')}")

    except Exception as e:
        print(f"❌ Error parsing response: {e}")
        print(f"Response: {result.stdout[:500]}")
else:
    print(f"❌ Error fetching backends:")
    print(result.stderr)

print("\n" + "=" * 80)
