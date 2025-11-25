// ============================================================================
// Master AI Gateway Lab - Main Infrastructure Deployment
// ============================================================================
// This Bicep file orchestrates the deployment of all infrastructure for the
// Master AI Gateway Lab, consolidating 7 individual labs into one environment.
//
// Deployed Resources:
// - API Management (StandardV2)
// - 3x AI Foundry Hubs + Projects (UK South, Sweden Central, West Europe)
// - 7+ AI Models across 3 regions
// - Redis Enterprise (semantic caching)
// - Azure Cognitive Search (vector search)
// - Cosmos DB (message storage)
// - Content Safety (content moderation)
// - Container Apps Environment + MCP servers
// - Log Analytics + Application Insights
// ============================================================================

targetScope = 'resourceGroup'

// ============================================================================
// Parameters
// ============================================================================

@description('Primary location for resources')
param location string = 'uksouth'

@description('API Management SKU')
@allowed(['Basicv2', 'Standardv2', 'Premium'])
param apimSku string = 'Standardv2'

@description('APIM subscriptions configuration')
param apimSubscriptionsConfig array = [
  { name: 'subscription1', displayName: 'Lab Subscription 1' }
  { name: 'subscription2', displayName: 'Lab Subscription 2' }
  { name: 'subscription3', displayName: 'Lab Subscription 3' }
]

@description('Foundry project name')
param foundryProjectName string = 'master-lab'

@description('Inference API path in APIM')
param inferenceAPIPath string = 'inference'

@description('Inference API type')
@allowed(['AzureOpenAI', 'AzureAI'])
param inferenceAPIType string = 'AzureOpenAI'

@description('Redis Cache SKU')
param redisCacheSku string = 'Balanced_B0'

@description('Azure Search SKU')
@allowed(['free', 'basic', 'standard'])
param searchSku string = 'basic'

@description('Deploy MCP servers')
param deployMCPServers bool = true

// ============================================================================
// Variables
// ============================================================================

var resourceSuffix = uniqueString(subscription().id, resourceGroup().id)

// AI Services config for 3 regions
var aiServicesConfig = [
  { name: 'foundry1', location: 'uksouth', priority: 1, weight: 100 }
  { name: 'foundry2', location: 'swedencentral', priority: 2, weight: 50 }
  { name: 'foundry3', location: 'westeurope', priority: 2, weight: 50 }
]

// Models for foundry1 (UK South primary - comprehensive model set)
var foundry1Models = [
  // Chat models
  { name: 'gpt-4o-mini', publisher: 'OpenAI', version: '2024-07-18', sku: 'GlobalStandard', capacity: 100 }
  { name: 'gpt-4o', publisher: 'OpenAI', version: '2024-08-06', sku: 'GlobalStandard', capacity: 100 }
  { name: 'gpt-4', publisher: 'OpenAI', version: 'turbo-2024-04-09', sku: 'GlobalStandard', capacity: 100 }
  // Image generation
  { name: 'dall-e-3', publisher: 'OpenAI', version: '3.0', sku: 'Standard', capacity: 1 }
  // Embeddings
  { name: 'text-embedding-3-small', publisher: 'OpenAI', version: '1', sku: 'GlobalStandard', capacity: 20 }
  { name: 'text-embedding-3-large', publisher: 'OpenAI', version: '1', sku: 'GlobalStandard', capacity: 20 }
  { name: 'text-embedding-ada-002', publisher: 'OpenAI', version: '2', sku: 'Standard', capacity: 20 }
]

// Models for foundry2 (Sweden Central secondary - core models for failover)
var foundry2Models = [
  { name: 'gpt-4o-mini', publisher: 'OpenAI', version: '2024-07-18', sku: 'GlobalStandard', capacity: 100 }
]

// Models for foundry3 (West Europe secondary - core models for failover)
var foundry3Models = [
  { name: 'gpt-4o-mini', publisher: 'OpenAI', version: '2024-07-18', sku: 'GlobalStandard', capacity: 100 }
]

// ============================================================================
// Module 1: Core Infrastructure (APIM, Log Analytics, App Insights)
// ============================================================================

module coreInfra '../deploy/deploy-01-core.bicep' = {
  name: 'coreInfraDeployment'
  params: {
    apimSku: apimSku
    apimSubscriptionsConfig: apimSubscriptionsConfig
  }
}

// ============================================================================
// Module 2: AI Foundry Infrastructure (3 Hubs + Projects + Models)
// ============================================================================

module aiFoundry '../deploy/deploy-02-ai-foundry.bicep' = {
  name: 'aiFoundryDeployment'
  params: {
    apimPrincipalId: coreInfra.outputs.apimPrincipalId
    appInsightsId: coreInfra.outputs.appInsightsId
    appInsightsInstrumentationKey: coreInfra.outputs.appInsightsInstrumentationKey
    foundryProjectName: foundryProjectName
    inferenceAPIPath: inferenceAPIPath
    inferenceAPIType: inferenceAPIType
    apimLoggerId: coreInfra.outputs.apimLoggerId
  }
  dependsOn: [
    coreInfra
  ]
}

// ============================================================================
// Module 3: Supporting Services (Redis, Search, Cosmos, Content Safety)
// ============================================================================

module supportingServices '../deploy/deploy-03-supporting.bicep' = {
  name: 'supportingServicesDeployment'
  params: {
    location: location
    redisCacheSku: redisCacheSku
    searchSku: searchSku
  }
}

// ============================================================================
// Module 4: MCP Servers (Container Apps)
// ============================================================================

module mcpServers '../deploy/deploy-04-mcp.bicep' = if (deployMCPServers) {
  name: 'mcpServersDeployment'
  params: {
    location: location
  }
  dependsOn: [
    coreInfra
    supportingServices
  ]
}

// ============================================================================
// Outputs
// ============================================================================

// Core Infrastructure Outputs
output resourceGroupName string = resourceGroup().name
output location string = location
output resourceSuffix string = resourceSuffix

// Log Analytics & Application Insights
output logAnalyticsWorkspaceId string = coreInfra.outputs.logAnalyticsWorkspaceId
output logAnalyticsCustomerId string = coreInfra.outputs.logAnalyticsCustomerId
output appInsightsName string = coreInfra.outputs.appInsightsName
output appInsightsInstrumentationKey string = coreInfra.outputs.appInsightsInstrumentationKey

// API Management
output apimServiceName string = coreInfra.outputs.apimServiceName
output apimGatewayUrl string = coreInfra.outputs.apimGatewayUrl
output apimResourceGatewayURL string = coreInfra.outputs.apimGatewayUrl
output apimSubscriptions array = coreInfra.outputs.apimSubscriptions

// AI Foundry
output foundryProjectEndpoint string = aiFoundry.outputs.foundryProjectEndpoint
output aiServicesConfig array = aiFoundry.outputs.aiServicesConfig
output inferenceAPIPath string = aiFoundry.outputs.inferenceAPIPath

// Supporting Services
output redisCacheHost string = supportingServices.outputs.redisCacheHost
output redisCachePort int = supportingServices.outputs.redisCachePort
output redisCacheKey string = supportingServices.outputs.redisCacheKey

output contentSafetyEndpoint string = supportingServices.outputs.contentSafetyEndpoint
output contentSafetyKey string = supportingServices.outputs.contentSafetyKey

output searchServiceName string = supportingServices.outputs.searchServiceName
output searchServiceEndpoint string = supportingServices.outputs.searchServiceEndpoint
output searchServiceAdminKey string = supportingServices.outputs.searchServiceAdminKey

output cosmosDbAccountName string = supportingServices.outputs.cosmosDbAccountName
output cosmosDbEndpoint string = supportingServices.outputs.cosmosDbEndpoint
output cosmosDbKey string = supportingServices.outputs.cosmosDbKey

// MCP Servers (if deployed)
output mcpServersDeployed bool = deployMCPServers

// Quick Start Commands
output quickStartCommands object = {
  openNotebook: 'code master-ai-gateway-fix-MCP-clean-documented-final.ipynb'
  loginToAzure: 'az login'
  setSubscription: 'az account set --subscription <subscription-id>'
  viewResources: 'az resource list --resource-group ${resourceGroup().name} --output table'
  getAPIMKeys: 'az apim show --name ${coreInfra.outputs.apimServiceName} --resource-group ${resourceGroup().name}'
}

// Environment Configuration
output environmentVariables object = {
  AZURE_SUBSCRIPTION_ID: subscription().subscriptionId
  AZURE_RESOURCE_GROUP: resourceGroup().name
  AZURE_LOCATION: location

  APIM_SERVICE_NAME: coreInfra.outputs.apimServiceName
  APIM_GATEWAY_URL: coreInfra.outputs.apimGatewayUrl

  FOUNDRY_PROJECT_ENDPOINT: aiFoundry.outputs.foundryProjectEndpoint

  REDIS_HOST: supportingServices.outputs.redisCacheHost
  REDIS_PORT: string(supportingServices.outputs.redisCachePort)

  SEARCH_SERVICE_ENDPOINT: supportingServices.outputs.searchServiceEndpoint

  COSMOS_DB_ENDPOINT: supportingServices.outputs.cosmosDbEndpoint

  CONTENT_SAFETY_ENDPOINT: supportingServices.outputs.contentSafetyEndpoint

  LOG_ANALYTICS_WORKSPACE_ID: coreInfra.outputs.logAnalyticsWorkspaceId
  APP_INSIGHTS_NAME: coreInfra.outputs.appInsightsName
}

// Deployment Summary
output deploymentSummary object = {
  totalResources: 15
  estimatedDeploymentTime: '35-40 minutes'
  labs: [
    'Lab 08: Access Control (OAuth 2.0, JWT, API Key)'
    'Lab 09: Semantic Caching (Redis)'
    'Lab 10: Message Storing (Cosmos DB)'
    'Lab 11: Vector Search (AI Search)'
    'Lab 02: Load Balancing (Multi-region)'
    'Lab 06: MCP Integration (7 MCP servers)'
    'Lab 12: Built-in Logging (Log Analytics)'
  ]
  nextSteps: [
    '1. Open master-ai-gateway-fix-MCP-clean-documented-final.ipynb'
    '2. Configure environment variables in .env file'
    '3. Run Section 0 cells to initialize'
    '4. Explore each lab section'
  ]
}
