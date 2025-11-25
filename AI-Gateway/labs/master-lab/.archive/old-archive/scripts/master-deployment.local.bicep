// ============================================================================
// MASTER AI GATEWAY LAB - CONSOLIDATED BICEP DEPLOYMENT
// ============================================================================
// This file consolidates all 31 AI Gateway labs into a single one-click deployment
//
// Deployed Resources:
// - 3x AI Foundry Hubs + Projects (UK South, Sweden Central, West Europe)
// - 1x API Management (StandardV2)
// - 1x Redis Cache (for semantic caching)
// - 1x Azure AI Content Safety
// - 1x Container Apps Environment + 7 MCP servers
// - 1x Azure Cognitive Search (for vector search)
// - 1x Cosmos DB (for message storage)
// - 1x Log Analytics + Application Insights
// - 1x Container Registry
//
// ============================================================================

targetScope = 'resourceGroup'

// ============================================================================
// PARAMETERS
// ============================================================================

@description('Primary location for resources (UK South)')
param location string = 'uksouth'

@description('API Management SKU')
@allowed(['Basicv2', 'Standardv2', 'Premium'])
param apimSku string = 'Standardv2'

@description('Redis Cache SKU for semantic caching')
param redisCacheSku string = 'Balanced_B0'

@description('Azure Search SKU')
@allowed(['free', 'basic', 'standard'])
param searchSku string = 'basic'

@description('Subscription configurations for APIM')
param apimSubscriptionsConfig array = [
  { name: 'subscription1', displayName: 'Subscription 1' }
  { name: 'subscription2', displayName: 'Subscription 2' }
  { name: 'subscription3', displayName: 'Subscription 3' }
]

@description('Foundry project name')
param foundryProjectName string = 'master-lab'

@description('Inference API path in APIM')
param inferenceAPIPath string = 'inference'

@description('Inference API type')
@allowed(['AzureOpenAI', 'AzureAI'])
param inferenceAPIType string = 'AzureOpenAI'

// ============================================================================
// VARIABLES
// ============================================================================

var resourceSuffix = uniqueString(subscription().id, resourceGroup().id)

// AI Services config for 3 regions
var aiServicesConfig = [
  { name: 'foundry1', location: 'uksouth', priority: 1, weight: 100 }
  { name: 'foundry2', location: 'swedencentral', priority: 2, weight: 50 }
  { name: 'foundry3', location: 'westeurope', priority: 2, weight: 50 }
]

// All 14 models - primary region gets ALL, secondary regions get core only
var modelsConfigPrimary = [
  { name: 'gpt-4o-mini', publisher: 'OpenAI', version: '2024-07-18', sku: 'GlobalStandard', capacity: 100, aiservice: 'foundry1' }
  { name: 'gpt-4.1-mini', publisher: 'OpenAI', version: '2025-04-14', sku: 'GlobalStandard', capacity: 20, aiservice: 'foundry1' }
  { name: 'gpt-4.1', publisher: 'OpenAI', version: '2025-04-14', sku: 'GlobalStandard', capacity: 100, aiservice: 'foundry1' }
  { name: 'gpt-4o', publisher: 'OpenAI', version: '2024-08-06', sku: 'GlobalStandard', capacity: 100, aiservice: 'foundry1' }
  { name: 'gpt-4o-realtime-preview', publisher: 'OpenAI', version: '2024-10-01-preview', sku: 'GlobalStandard', capacity: 100, aiservice: 'foundry1' }
  { name: 'dall-e-3', publisher: 'OpenAI', version: '3.0', sku: 'Standard', capacity: 1, aiservice: 'foundry1' }
  { name: 'FLUX-1.1-pro', publisher: 'Black Forest Labs', version: '1', sku: 'GlobalStandard', capacity: 100, aiservice: 'foundry1' }
  { name: 'text-embedding-3-small', publisher: 'OpenAI', version: '1', sku: 'GlobalStandard', capacity: 20, aiservice: 'foundry1' }
  { name: 'text-embedding-3-large', publisher: 'OpenAI', version: '1', sku: 'GlobalStandard', capacity: 20, aiservice: 'foundry1' }
  { name: 'text-embedding-ada-002', publisher: 'OpenAI', version: '2', sku: 'Standard', capacity: 20, aiservice: 'foundry1' }
  { name: 'DeepSeek-R1', publisher: 'DeepSeek', version: '1', sku: 'GlobalStandard', capacity: 1, aiservice: 'foundry1' }
  { name: 'Phi-4', publisher: 'Microsoft', version: '3', sku: 'GlobalStandard', capacity: 1, aiservice: 'foundry1' }
]

var modelsConfigSecondary = [
  { name: 'gpt-4o-mini', publisher: 'OpenAI', version: '2024-07-18', sku: 'GlobalStandard', capacity: 100, aiservice: 'foundry2' }
  { name: 'gpt-4o-mini', publisher: 'OpenAI', version: '2024-07-18', sku: 'GlobalStandard', capacity: 100, aiservice: 'foundry3' }
]

var modelsConfig = concat(modelsConfigPrimary, modelsConfigSecondary)

// ============================================================================
// CORE MODULES (using existing tested modules)
// ============================================================================

// 1. Log Analytics
module lawModule '../../modules/operational-insights/v1/workspaces.bicep' = {
  name: 'lawModule'
}

// 2. Application Insights
module appInsightsModule '../../modules/monitor/v1/appinsights.bicep' = {
  name: 'appInsightsModule'
  params: {
    lawId: lawModule.outputs.id
    customMetricsOptedInType: 'WithDimensions'
  }
}

// 3. API Management
module apimModule '../../modules/apim/v2/apim.bicep' = {
  name: 'apimModule'
  params: {
    apimSku: apimSku
    apimSubscriptionsConfig: apimSubscriptionsConfig
    lawId: lawModule.outputs.id
    appInsightsId: appInsightsModule.outputs.id
    appInsightsInstrumentationKey: appInsightsModule.outputs.instrumentationKey
  }
}

// 4. AI Foundry (3 regions with models)
module foundryModule '../../modules/cognitive-services/v3/foundry.bicep' = {
  name: 'foundryModule'
  params: {
    aiServicesConfig: aiServicesConfig
    modelsConfig: modelsConfig
    apimPrincipalId: apimModule.outputs.principalId
    foundryProjectName: foundryProjectName
    appInsightsId: appInsightsModule.outputs.id
    appInsightsInstrumentationKey: appInsightsModule.outputs.instrumentationKey
  }
}

// 5. APIM Inference API
module inferenceAPIModule '../../modules/apim/v2/inference-api.bicep' = {
  name: 'inferenceAPIModule'
  params: {
    policyXml: loadTextContent('policies/backend-pool-load-balancing-policy.xml')
    apimLoggerId: apimModule.outputs.loggerId
    appInsightsId: appInsightsModule.outputs.id
    appInsightsInstrumentationKey: appInsightsModule.outputs.instrumentationKey
    aiServicesConfig: foundryModule.outputs.extendedAIServicesConfig
    inferenceAPIType: inferenceAPIType
    inferenceAPIPath: inferenceAPIPath
  }
}

// ============================================================================
// INLINED RESOURCES (no existing modules)
// ============================================================================

// 6. Redis Cache for semantic caching
resource redisEnterprise 'Microsoft.Cache/redisEnterprise@2025-05-01-preview' = {
  name: 'redis-${resourceSuffix}'
  location: location
  sku: {
    name: redisCacheSku
  }
}

resource redisDatabase 'Microsoft.Cache/redisEnterprise/databases@2025-05-01-preview' = {
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

// 7. Content Safety
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

// 8. Azure Cognitive Search
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

// 9. Cosmos DB
resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2024-12-01-preview' = {
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

// 10. Container Registry
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-11-01-preview' = {
  name: 'acr${resourceSuffix}'
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
    publicNetworkAccess: 'Enabled'
  }
}

// 11. Container Apps Environment
resource containerAppEnv 'Microsoft.App/managedEnvironments@2023-11-02-preview' = {
  name: 'cae-${resourceSuffix}'
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: lawModule.outputs.customerId
        sharedKey: lawModule.outputs.primarySharedKey
      }
    }
  }
}

// Managed Identity for Container Apps
resource containerAppUAI 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'cae-mi-${resourceSuffix}'
  location: location
}

var acrPullRole = resourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
resource containerAppUAIRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, containerAppUAI.id, acrPullRole)
  properties: {
    roleDefinitionId: acrPullRole
    principalId: containerAppUAI.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// 12-18. MCP Container Apps (placeholder images - will be built separately)
var mcpServers = [
  'weather'
  'oncall'
  'github'
  'spotify'
  'product-catalog'
  'place-order'
  'ms-learn'
]

resource mcpContainerApps 'Microsoft.App/containerApps@2023-11-02-preview' = [for server in mcpServers: {
  name: 'mcp-${server}-${resourceSuffix}'
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${containerAppUAI.id}': {}
    }
  }
  properties: {
    managedEnvironmentId: containerAppEnv.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8080
        allowInsecure: false
      }
      registries: [
        {
          identity: containerAppUAI.id
          server: containerRegistry.properties.loginServer
        }
      ]
    }
    template: {
      containers: [
        {
          name: server
          image: 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest' // Placeholder
          resources: {
            cpu: json('0.25')
            memory: '0.5Gi'
          }
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 3
      }
    }
  }
  dependsOn: [
    containerAppUAIRoleAssignment
  ]
}]

// ============================================================================
// OUTPUTS
// ============================================================================

output logAnalyticsWorkspaceId string = lawModule.outputs.customerId
output appInsightsName string = appInsightsModule.outputs.name
output apimServiceId string = apimModule.outputs.id
output apimServiceName string = apimModule.outputs.name
output apimResourceGatewayURL string = apimModule.outputs.gatewayUrl
output apimSubscriptions array = apimModule.outputs.apimSubscriptions

// AI Foundry
output foundryProjectEndpoint string = foundryModule.outputs.extendedAIServicesConfig[0].foundryProjectEndpoint

// Redis
output redisCacheHost string = redisEnterprise.properties.hostName
output redisCachePort int = 10000
#disable-next-line outputs-should-not-contain-secrets
output redisCacheKey string = redisDatabase.listKeys().primaryKey

// Content Safety
output contentSafetyEndpoint string = contentSafety.properties.endpoint
#disable-next-line outputs-should-not-contain-secrets
output contentSafetyKey string = contentSafety.listKeys().key1

// Search
output searchServiceName string = searchService.name
output searchServiceEndpoint string = 'https://${searchService.name}.search.windows.net'
#disable-next-line outputs-should-not-contain-secrets
output searchServiceAdminKey string = searchService.listAdminKeys().primaryKey

// Cosmos DB
output cosmosDbAccountName string = cosmosAccount.name
output cosmosDbEndpoint string = cosmosAccount.properties.documentEndpoint

// Container Registry
output containerRegistryName string = containerRegistry.name
output containerRegistryLoginServer string = containerRegistry.properties.loginServer

// MCP Server URLs
output mcpServerUrls array = [for (server, i) in mcpServers: {
  name: server
  url: 'https://${mcpContainerApps[i].properties.configuration.ingress.fqdn}'
}]
