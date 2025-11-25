# Create Service Principal for Master Lab Deployment
# Run this from PowerShell where Azure CLI is authenticated

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Creating Service Principal for Master Lab" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Get subscription ID
$subscriptionId = az account show --query id -o tsv
Write-Host "[*] Using Subscription: $subscriptionId"
Write-Host ""

# Service Principal name
$spName = "master-lab-deployment-sp"
Write-Host "[*] Service Principal Name: $spName"
Write-Host ""

# Create Service Principal with Contributor role
Write-Host "[*] Creating Service Principal..."
Write-Host "[*] This will have Contributor role on subscription: $subscriptionId"
Write-Host ""

$spOutput = az ad sp create-for-rbac `
  --name $spName `
  --role Contributor `
  --scopes "/subscriptions/$subscriptionId" `
  --output json | ConvertFrom-Json

# Extract values
$tenantId = $spOutput.tenant
$clientId = $spOutput.appId
$clientSecret = $spOutput.password

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "Service Principal Created Successfully!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT: Save these credentials securely!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Tenant ID:     $tenantId"
Write-Host "Client ID:     $clientId"
Write-Host "Client Secret: $clientSecret"
Write-Host ""

# Create .azure-credentials.env file
$envContent = @"
AZURE_TENANT_ID=$tenantId
AZURE_CLIENT_ID=$clientId
AZURE_CLIENT_SECRET=$clientSecret
AZURE_SUBSCRIPTION_ID=$subscriptionId
"@

$envContent | Out-File -FilePath ".azure-credentials.env" -Encoding UTF8

Write-Host "==========================================" -ForegroundColor Green
Write-Host "Created .azure-credentials.env file" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "File contents:" -ForegroundColor Yellow
Get-Content ".azure-credentials.env"
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. The .azure-credentials.env file has been created"
Write-Host "2. Make sure it's in .gitignore (already added)"
Write-Host "3. Run Cell 13 in the notebook to test authentication"
Write-Host ""
Write-Host "To delete this Service Principal later:" -ForegroundColor Yellow
Write-Host "  az ad sp delete --id $clientId"
Write-Host ""
