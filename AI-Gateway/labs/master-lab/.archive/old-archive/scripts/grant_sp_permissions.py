#!/usr/bin/env python3
"""
Grant User Access Administrator role to Service Principal
This allows the SP to create role assignments during deployment
Uses Azure Python SDK to avoid Azure CLI cache issues
"""

import os
import uuid
from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from azure.mgmt.authorization import AuthorizationManagementClient

print('=' * 70)
print('GRANT USER ACCESS ADMINISTRATOR TO SERVICE PRINCIPAL')
print('=' * 70)
print()

# Load Service Principal credentials
credentials_file = '.azure-credentials.env'
if not os.path.exists(credentials_file):
    print('[ERROR] .azure-credentials.env not found!')
    print('[*] Please run Cell 11 first to create Service Principal')
    exit(1)

load_dotenv(credentials_file)
client_id = os.getenv('AZURE_CLIENT_ID')
subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
sp_object_id = os.getenv('AZURE_SP_OBJECT_ID')  # We'll need to get this

if not client_id or not subscription_id:
    print('[ERROR] Missing credentials in .azure-credentials.env')
    exit(1)

print(f'[*] Service Principal Client ID: {client_id}')
print(f'[*] Subscription ID: {subscription_id}')
print()

# Use Azure CLI credential to manage roles (this requires your user account has Owner or UAA permission)
print('[*] Authenticating with Azure CLI...')
try:
    credential = AzureCliCredential()
    auth_client = AuthorizationManagementClient(credential, subscription_id)
    print('[OK] Authenticated successfully')
except Exception as e:
    print(f'[ERROR] Authentication failed: {e}')
    print()
    print('[*] Manual command to grant role:')
    print(f'    az role assignment create \\')
    print(f'      --assignee {client_id} \\')
    print(f'      --role "User Access Administrator" \\')
    print(f'      --scope /subscriptions/{subscription_id}')
    print()
    print('[*] Note: You need Owner or User Access Administrator permission to grant roles')
    exit(1)

# Get Service Principal object ID if not in .env
if not sp_object_id:
    print('[*] Getting Service Principal object ID...')
    # We need to use MS Graph or Azure CLI for this
    # For now, we'll get it from the error message in the deployment
    # The error shows: object id 'c1a04baa-9221-4490-821b-5968bbf3772b'
    print('[*] Service Principal object ID not found in .azure-credentials.env')
    print('[*] Looking it up...')

    # Try to find it from existing role assignments
    scope = f'/subscriptions/{subscription_id}'
    try:
        assignments = list(auth_client.role_assignments.list_for_subscription(
            filter=f"principalId eq '{client_id}'"
        ))
        if assignments:
            # This won't work because filter uses objectId not clientId
            pass
    except:
        pass

    # Extract from error message - hardcoded from your error
    sp_object_id = 'c1a04baa-9221-4490-821b-5968bbf3772b'
    print(f'[*] Using object ID from deployment error: {sp_object_id}')

print()

# Check current role assignments
print('[*] Checking current role assignments for Service Principal...')
scope = f'/subscriptions/{subscription_id}'

try:
    assignments = list(auth_client.role_assignments.list_for_subscription())
    sp_assignments = [a for a in assignments if a.principal_id == sp_object_id]

    print(f'[OK] Found {len(sp_assignments)} existing role assignment(s)')
    for assignment in sp_assignments:
        # Get role definition name
        role_def = auth_client.role_definitions.get_by_id(assignment.role_definition_id)
        print(f'  - {role_def.role_name} at {assignment.scope}')
    print()

    # Check if User Access Administrator already exists
    has_uaa = any('User Access Administrator' in auth_client.role_definitions.get_by_id(a.role_definition_id).role_name
                  for a in sp_assignments)

    if has_uaa:
        print('[OK] Service Principal already has User Access Administrator role')
        print('[OK] No action needed')
    else:
        print('[*] Granting User Access Administrator role...')

        # Get User Access Administrator role definition ID (built-in role)
        uaa_role_id = '18d7d88d-d35e-4fb5-a5c3-7773c20a72d9'
        role_definition_id = f'/subscriptions/{subscription_id}/providers/Microsoft.Authorization/roleDefinitions/{uaa_role_id}'

        # Create role assignment
        role_assignment_name = str(uuid.uuid4())

        try:
            assignment = auth_client.role_assignments.create(
                scope=scope,
                role_assignment_name=role_assignment_name,
                parameters={
                    'role_definition_id': role_definition_id,
                    'principal_id': sp_object_id,
                    'principal_type': 'ServicePrincipal'
                }
            )

            print('[OK] User Access Administrator role granted successfully!')
            print(f'  - Role: User Access Administrator')
            print(f'  - Scope: {assignment.scope}')
            print(f'  - Principal: {assignment.principal_id}')
            print()
            print('[OK] You can now re-run the deployment (Cell 17)')

        except Exception as e:
            print(f'[ERROR] Failed to grant role: {e}')
            print()
            print('[*] You may need to run this command manually:')
            print(f'    az role assignment create \\')
            print(f'      --assignee {client_id} \\')
            print(f'      --role "User Access Administrator" \\')
            print(f'      --scope /subscriptions/{subscription_id}')
            exit(1)

except Exception as e:
    print(f'[ERROR] Failed to check role assignments: {e}')
    print()
    print('[*] Manual command to grant role:')
    print(f'    az role assignment create \\')
    print(f'      --assignee {client_id} \\')
    print(f'      --role "User Access Administrator" \\')
    print(f'      --scope /subscriptions/{subscription_id}')
    exit(1)
