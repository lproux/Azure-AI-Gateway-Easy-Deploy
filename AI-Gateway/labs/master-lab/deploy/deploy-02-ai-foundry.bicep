// Deploy Step 2: AI Foundry Infrastructure
// - 3 AI Foundry Hubs (UK South, Sweden Central, West Europe)
// - 3 AI Foundry Projects
// - 14 AI Models (12 in UK South primary, 1 in each secondary region)

targetScope = 'resourceGroup'

// Parameters
@description('APIM Principal ID from Step 1')
param apimPrincipalId string

@description('App Insights ID from Step 1')
param appInsightsId string

@description('App Insights Instrumentation Key from Step 1')
param appInsightsInstrumentationKey string

@description('Foundry project name')
param foundryProjectName string = 'master-lab'

@description('Inference API path in APIM')
param inferenceAPIPath string = 'inference'

@description('Inference API type')
@allowed(['AzureOpenAI', 'AzureAI'])
param inferenceAPIType string = 'AzureOpenAI'

@description('APIM Logger ID from Step 1')
param apimLoggerId string

// Variables

// AI Services config for 3 regions
var aiServicesConfig = [
  { name: 'foundry1', location: 'uksouth', priority: 1, weight: 100 }
  { name: 'foundry2', location: 'swedencentral', priority: 2, weight: 50 }
  { name: 'foundry3', location: 'westeurope', priority: 2, weight: 50 }
]

// Models for foundry1 (UK South primary - stable production models)
// Note: gpt-4o-realtime-preview, DeepSeek-R1, and Phi-4 removed due to regional availability
var foundry1Models = [
  { name: 'gpt-4o-mini', publisher: 'OpenAI', version: '2024-07-18', sku: 'GlobalStandard', capacity: 100 }
  { name: 'gpt-4o', publisher: 'OpenAI', version: '2024-08-06', sku: 'GlobalStandard', capacity: 100 }
  { name: 'gpt-4', publisher: 'OpenAI', version: 'turbo-2024-04-09', sku: 'GlobalStandard', capacity: 100 }
  { name: 'dall-e-3', publisher: 'OpenAI', version: '3.0', sku: 'Standard', capacity: 1 }
  { name: 'text-embedding-3-small', publisher: 'OpenAI', version: '1', sku: 'GlobalStandard', capacity: 20 }
  { name: 'text-embedding-3-large', publisher: 'OpenAI', version: '1', sku: 'GlobalStandard', capacity: 20 }
  { name: 'text-embedding-ada-002', publisher: 'OpenAI', version: '2', sku: 'Standard', capacity: 20 }
]

// Models for foundry2 (Sweden Central secondary - gpt-4o-mini only)
var foundry2Models = [
  { name: 'gpt-4o-mini', publisher: 'OpenAI', version: '2024-07-18', sku: 'GlobalStandard', capacity: 100 }
]

// Models for foundry3 (West Europe secondary - gpt-4o-mini only)
var foundry3Models = [
  { name: 'gpt-4o-mini', publisher: 'OpenAI', version: '2024-07-18', sku: 'GlobalStandard', capacity: 100 }
]

// Resources

// AI Foundry (3 regions with models)
module foundryModule '../../modules/cognitive-services/v3/foundry.bicep' = {
  name: 'foundryModule'
  params: {
    aiServicesConfig: aiServicesConfig
    foundry1Models: foundry1Models
    foundry2Models: foundry2Models
    foundry3Models: foundry3Models
    apimPrincipalId: apimPrincipalId
    foundryProjectName: foundryProjectName
    appInsightsId: appInsightsId
    appInsightsInstrumentationKey: appInsightsInstrumentationKey
  }
}

// APIM Inference API
module inferenceAPIModule '../../modules/apim/v2/inference-api.bicep' = {
  name: 'inferenceAPIModule'
  params: {
    policyXml: loadTextContent('policies/backend-pool-load-balancing-policy.xml')
    apimLoggerId: apimLoggerId
    appInsightsId: appInsightsId
    appInsightsInstrumentationKey: appInsightsInstrumentationKey
    aiServicesConfig: foundryModule.outputs.extendedAIServicesConfig
    inferenceAPIType: inferenceAPIType
    inferenceAPIPath: inferenceAPIPath
  }
}

// Outputs
output foundryProjectEndpoint string = foundryModule.outputs.extendedAIServicesConfig[0].foundryProjectEndpoint
output aiServicesConfig array = foundryModule.outputs.extendedAIServicesConfig
output inferenceAPIPath string = inferenceAPIPath
