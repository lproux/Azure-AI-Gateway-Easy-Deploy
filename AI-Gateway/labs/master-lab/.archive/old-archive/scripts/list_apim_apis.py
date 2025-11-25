#!/usr/bin/env python3
"""List all APIs in the APIM service"""
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

print("=" * 80)
print("LISTING APIM APIS")
print("=" * 80)
print(f"Service: {service_name}")
print(f"Resource Group: {resource_group}")
print()

client = ApiManagementClient(credential, subscription_id)

# List all APIs
apis = client.api.list_by_service(resource_group, service_name)

print("APIs found:")
print("-" * 80)
for api in apis:
    print(f"Name: {api.name}")
    print(f"  Display Name: {api.display_name}")
    print(f"  Path: {api.path}")
    print(f"  Service URL: {api.service_url}")
    print(f"  Protocols: {api.protocols}")
    print()

print("=" * 80)
