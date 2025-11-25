// Deploy Step 2c: APIM Inference API Configuration
// Configures APIM API for AI Foundry backend pool

targetScope = 'resourceGroup'

// Parameters
@description('APIM Logger ID from Step 1')
param apimLoggerId string

@description('App Insights ID from Step 1')
param appInsightsId string

@description('App Insights Instrumentation Key from Step 1')
param appInsightsInstrumentationKey string

@description('Inference API path in APIM')
param inferenceAPIPath string = 'inference'

@description('Inference API type')
@allowed(['AzureOpenAI', 'AzureAI'])
param inferenceAPIType string = 'AzureOpenAI'

// Variables
var resourceSuffix = uniqueString(subscription().id, resourceGroup().id)

// Get existing foundry hubs
resource foundry1 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: 'foundry1-${resourceSuffix}'
}

resource foundry2 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: 'foundry2-${resourceSuffix}'
}

resource foundry3 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: 'foundry3-${resourceSuffix}'
}

// Get existing projects
resource project1 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' existing = {
  parent: foundry1
  name: 'master-lab-foundry1'
}

resource project2 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' existing = {
  parent: foundry2
  name: 'master-lab-foundry2'
}

resource project3 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' existing = {
  parent: foundry3
  name: 'master-lab-foundry3'
}

// Build AI Services Config for APIM
var aiServicesConfig = [
  {
    name: 'foundry1'
    location: 'uksouth'
    priority: 1
    weight: 100
    cognitiveServiceName: foundry1.name
    endpoint: foundry1.properties.endpoint
    foundryProjectEndpoint: 'https://${foundry1.name}.services.ai.azure.com/api/projects/${project1.name}'
  }
  {
    name: 'foundry2'
    location: 'swedencentral'
    priority: 2
    weight: 50
    cognitiveServiceName: foundry2.name
    endpoint: foundry2.properties.endpoint
    foundryProjectEndpoint: 'https://${foundry2.name}.services.ai.azure.com/api/projects/${project2.name}'
  }
  {
    name: 'foundry3'
    location: 'westeurope'
    priority: 2
    weight: 50
    cognitiveServiceName: foundry3.name
    endpoint: foundry3.properties.endpoint
    foundryProjectEndpoint: 'https://${foundry3.name}.services.ai.azure.com/api/projects/${project3.name}'
  }
]

// APIM Inference API Module
module inferenceAPIModule '../../modules/apim/v2/inference-api.bicep' = {
  name: 'inferenceAPIModule'
  params: {
    policyXml: loadTextContent('policies/backend-pool-load-balancing-policy.xml')
    apimLoggerId: apimLoggerId
    appInsightsId: appInsightsId
    appInsightsInstrumentationKey: appInsightsInstrumentationKey
    aiServicesConfig: aiServicesConfig
    inferenceAPIType: inferenceAPIType
    inferenceAPIPath: inferenceAPIPath
  }
}

// Outputs
output inferenceAPIPath string = inferenceAPIPath
output aiServicesConfig array = aiServicesConfig
