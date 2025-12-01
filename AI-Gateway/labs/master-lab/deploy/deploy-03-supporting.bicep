// Deploy Step 3: Supporting Services
// - Redis Enterprise (semantic caching)
// - Azure Cognitive Search
// - Cosmos DB (with data plane RBAC)
// - Content Safety

targetScope = 'resourceGroup'

// Parameters
@description('Primary location')
param location string = 'uksouth'

@description('Redis Cache SKU')
param redisCacheSku string = 'Balanced_B0'

@description('Azure Search SKU')
@allowed(['free', 'basic', 'standard'])
param searchSku string = 'basic'

@description('Principal ID for Cosmos DB data plane RBAC (e.g., user or service principal object ID)')
param cosmosDbPrincipalId string = ''

// Variables
var resourceSuffix = uniqueString(subscription().id, resourceGroup().id)

// Resources

// 1. Redis Enterprise for semantic caching
resource redisEnterprise 'Microsoft.Cache/redisEnterprise@2024-10-01' = {
  name: 'redis-${resourceSuffix}'
  location: location
  sku: {
    name: redisCacheSku
  }
  properties: {}
}

resource redisDatabase 'Microsoft.Cache/redisEnterprise/databases@2024-10-01' = {
  name: 'default'
  parent: redisEnterprise
  properties: {
    evictionPolicy: 'NoEviction'
    clusteringPolicy: 'EnterpriseCluster'
    modules: [
      { name: 'RediSearch' }
    ]
    port: 10000
  }
}

// 2. Content Safety
resource contentSafety 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: 'contentsafety-${resourceSuffix}'
  location: location
  sku: {
    name: 'S0'
  }
  kind: 'ContentSafety'
  properties: {
    customSubDomainName: 'contentsafety-${resourceSuffix}'
    publicNetworkAccess: 'Enabled'
  }
}

// 3. Azure Cognitive Search
resource searchService 'Microsoft.Search/searchServices@2024-06-01-preview' = {
  name: 'search-${resourceSuffix}'
  location: location
  sku: {
    name: searchSku
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
  }
}

// 4. Cosmos DB
resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {
  name: 'cosmos-${resourceSuffix}'
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
    }
    enableFreeTier: false
  }
}

// 4a. Cosmos DB SQL Database for messages
resource cosmosDatabase 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-05-15' = {
  name: 'messages-db'
  parent: cosmosAccount
  properties: {
    resource: {
      id: 'messages-db'
    }
  }
}

// 4b. Cosmos DB SQL Container for conversations
resource cosmosContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = {
  name: 'conversations'
  parent: cosmosDatabase
  properties: {
    resource: {
      id: 'conversations'
      partitionKey: {
        paths: ['/conversationId']
        kind: 'Hash'
      }
    }
    options: {
      throughput: 400
    }
  }
}

// 4c. Cosmos DB Data Plane RBAC - Assign Cosmos DB Built-in Data Contributor role
// Role definition ID 00000000-0000-0000-0000-000000000002 = Cosmos DB Built-in Data Contributor
// This allows read/write operations on Cosmos DB data plane (required for SDK access with Azure AD)
resource cosmosDataContributorRole 'Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments@2024-05-15' = if (!empty(cosmosDbPrincipalId)) {
  name: guid(cosmosAccount.id, cosmosDbPrincipalId, '00000000-0000-0000-0000-000000000002')
  parent: cosmosAccount
  properties: {
    roleDefinitionId: '${cosmosAccount.id}/sqlRoleDefinitions/00000000-0000-0000-0000-000000000002'
    principalId: cosmosDbPrincipalId
    scope: cosmosAccount.id
  }
}

// Outputs
output redisCacheHost string = redisEnterprise.properties.hostName
output redisCachePort int = 10000
#disable-next-line outputs-should-not-contain-secrets
output redisCacheKey string = redisDatabase.listKeys().primaryKey

output contentSafetyEndpoint string = contentSafety.properties.endpoint
#disable-next-line outputs-should-not-contain-secrets
output contentSafetyKey string = contentSafety.listKeys().key1

output searchServiceName string = searchService.name
output searchServiceEndpoint string = 'https://${searchService.name}.search.windows.net'
#disable-next-line outputs-should-not-contain-secrets
output searchServiceAdminKey string = searchService.listAdminKeys().primaryKey

output cosmosDbAccountName string = cosmosAccount.name
output cosmosDbEndpoint string = cosmosAccount.properties.documentEndpoint
#disable-next-line outputs-should-not-contain-secrets
output cosmosDbKey string = cosmosAccount.listKeys().primaryMasterKey
