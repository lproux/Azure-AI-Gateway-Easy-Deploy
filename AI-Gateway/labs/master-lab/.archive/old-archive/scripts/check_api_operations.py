#!/usr/bin/env python3
"""Check API operations and backends"""
import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.mgmt.apimanagement import ApiManagementClient

# Load credentials
load_dotenv('.azure-credentials.env')

tenant_id = os.getenv('AZURE_TENANT_ID')
client_id = os.getenv('AZURE_CLIENT_ID')
client_secret = os.getenv('AZURE_CLIENT_SECRET')
subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')

credential = ClientSecretCredential(tenant_id, client_id, client_secret)

# APIM details
resource_group = 'lab-master-lab'
service_name = 'apim-pavavy6pu5hpa'
api_name = 'inference-api'

print("=" * 80)
print("CHECKING API OPERATIONS AND BACKENDS")
print("=" * 80)

client = ApiManagementClient(credential, subscription_id)

# Get API details
api = client.api.get(resource_group, service_name, api_name)
print(f"API: {api.display_name}")
print(f"Path: {api.path}")
print(f"Subscription Required: {api.subscription_required}")
print()

# List operations
print("Operations:")
print("-" * 80)
try:
    operations = client.api_operation.list_by_api(resource_group, service_name, api_name)
    for op in operations:
        print(f"  {op.method} {op.url_template}")
        print(f"    Display Name: {op.display_name}")
        print()
except Exception as e:
    print(f"Error listing operations: {e}")
    print()

# List backends
print("Backends:")
print("-" * 80)
try:
    backends = client.backend.list_by_service(resource_group, service_name)
    for backend in backends:
        print(f"Name: {backend.name}")
        print(f"  URL: {backend.url}")
        print(f"  Protocol: {backend.protocol}")
        if hasattr(backend, 'type') and backend.type:
            print(f"  Type: {backend.type}")
        print()
except Exception as e:
    print(f"Error listing backends: {e}")
    print()

# Check API policy
print("API Policy:")
print("-" * 80)
try:
    policy = client.api_policy.get(resource_group, service_name, api_name, 'policy')
    print(policy.value[:500])
    print("...")
except Exception as e:
    print(f"Error getting policy: {e}")

print("=" * 80)
