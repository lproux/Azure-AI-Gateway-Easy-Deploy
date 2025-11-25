// Deploy Step 2: AI Foundry (AIServices) Accounts
// Creates multiple Azure Cognitive Services accounts of kind 'AIServices'
// with system-assigned identity and project management enabled.
// Outputs array with ids, endpoints, and locations for later backend pool configuration.

targetScope = 'resourceGroup'

@description('Stable suffix used in naming (matches Python resource_suffix)')
param resourceSuffix string

@description('Foundry configuration array (name without suffix, location, optional tags)')
param foundryConfig array = [
  {
    name: 'foundry1'
    location: 'uksouth'
  }
  {
    name: 'foundry2'
    location: 'eastus'
  }
  {
    name: 'foundry3'
    location: 'norwayeast'
  }
]

@description('SKU for AIServices accounts')
@allowed(['S0'])
param foundrySku string = 'S0'

// Resources
resource foundryAccounts 'Microsoft.CognitiveServices/accounts@2024-10-01' = [for f in foundryConfig: {
  name: '${f.name}-${resourceSuffix}'
  location: f.location
  sku: {
    name: foundrySku
  }
  kind: 'AIServices'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    // NOTE: Some preview properties (e.g. allowProjectManagement) are not yet exposed in the published type definitions.
    // Omitting them here to satisfy Bicep type validation; they can be enabled post-deployment via CLI/SDK if required.
    customSubDomainName: toLower('${f.name}-${resourceSuffix}')
    // publicNetworkAccess may be ignored for certain kinds; retain for clarity.
    publicNetworkAccess: 'Enabled'
  }
}]

// Outputs
output foundryAccounts array = [for (f,i) in foundryConfig: {
  name: foundryAccounts[i].name
  location: foundryAccounts[i].location
  id: foundryAccounts[i].id
  endpoint: foundryAccounts[i].properties.endpoint
}]
