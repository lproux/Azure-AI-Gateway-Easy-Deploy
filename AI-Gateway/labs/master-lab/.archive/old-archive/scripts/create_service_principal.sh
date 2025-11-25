#!/bin/bash
# Create Service Principal for Master Lab Deployment
# Run this from a terminal where Azure CLI is authenticated

echo "=========================================="
echo "Creating Service Principal for Master Lab"
echo "=========================================="
echo ""

# Get subscription ID
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
echo "[*] Using Subscription: $SUBSCRIPTION_ID"
echo ""

# Service Principal name
SP_NAME="master-lab-deployment-sp"
echo "[*] Service Principal Name: $SP_NAME"
echo ""

# Create Service Principal with Contributor role
echo "[*] Creating Service Principal..."
echo "[*] This will have Contributor role on subscription: $SUBSCRIPTION_ID"
echo ""

SP_OUTPUT=$(az ad sp create-for-rbac \
  --name "$SP_NAME" \
  --role Contributor \
  --scopes "/subscriptions/$SUBSCRIPTION_ID" \
  --output json)

# Extract values
TENANT_ID=$(echo $SP_OUTPUT | jq -r '.tenant')
CLIENT_ID=$(echo $SP_OUTPUT | jq -r '.appId')
CLIENT_SECRET=$(echo $SP_OUTPUT | jq -r '.password')

echo ""
echo "=========================================="
echo "Service Principal Created Successfully!"
echo "=========================================="
echo ""
echo "IMPORTANT: Save these credentials securely!"
echo ""
echo "Tenant ID:     $TENANT_ID"
echo "Client ID:     $CLIENT_ID"
echo "Client Secret: $CLIENT_SECRET"
echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Create .azure-credentials.env file:"
echo ""
echo "cat > .azure-credentials.env << EOF"
echo "AZURE_TENANT_ID=$TENANT_ID"
echo "AZURE_CLIENT_ID=$CLIENT_ID"
echo "AZURE_CLIENT_SECRET=$CLIENT_SECRET"
echo "AZURE_SUBSCRIPTION_ID=$SUBSCRIPTION_ID"
echo "EOF"
echo ""
echo "2. Run in notebook to verify:"
echo "   from dotenv import load_dotenv"
echo "   load_dotenv('.azure-credentials.env')"
echo ""
echo "=========================================="
