// Deploy Step 4: MCP Servers
// - Container Registry
// - Container Apps Environment
// - 5 MCP Server Container Apps (removed oncall & spotify - no reliable public images)

targetScope = 'resourceGroup'

// Parameters
@description('Primary location')
param location string = 'uksouth'

@description('Log Analytics Customer ID from Step 1')
param logAnalyticsCustomerId string

@description('Log Analytics Primary Shared Key from Step 1')
@secure()
param logAnalyticsPrimarySharedKey string

// Variables
var resourceSuffix = uniqueString(subscription().id, resourceGroup().id)
var shortSuffix = take(resourceSuffix, 10)  // Use shorter suffix for container app names (max 32 chars total)

// MCP Servers - 5 total (2 with real images, 3 placeholders)
var mcpServers = [
  'weather'
  'github'
  'product-catalog'
  'place-order'
  'ms-learn'
]

// MCP Server Docker Images
// - Real images for weather, github (public Docker Hub / ghcr.io)
// - Placeholder for product-catalog, place-order, ms-learn (demo only)
var mcpServerImages = {
  weather: 'mcp/openweather:latest'
  github: 'ghcr.io/github/github-mcp-server:latest'
  'product-catalog': 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
  'place-order': 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
  'ms-learn': 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
}

// Resources

// 1. Container Registry
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

// 2. Managed Identity for Container Apps
resource containerAppUAI 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'cae-mi-${resourceSuffix}'
  location: location
}

// 3. Role Assignment - ACR Pull for Container Apps
var acrPullRole = resourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
resource containerAppUAIRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, containerAppUAI.id, acrPullRole)
  properties: {
    roleDefinitionId: acrPullRole
    principalId: containerAppUAI.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// 4. Container Apps Environment
resource containerAppEnv 'Microsoft.App/managedEnvironments@2023-11-02-preview' = {
  name: 'cae-${resourceSuffix}'
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsCustomerId
        sharedKey: logAnalyticsPrimarySharedKey
      }
    }
  }
}

// 5. MCP Container Apps (5 servers)
resource mcpContainerApps 'Microsoft.App/containerApps@2023-11-02-preview' = [for server in mcpServers: {
  name: 'mcp-${server}-${shortSuffix}'
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
          image: mcpServerImages[server]  // Use real images for weather/github, placeholder for others
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

// Outputs
output containerRegistryName string = containerRegistry.name
output containerRegistryLoginServer string = containerRegistry.properties.loginServer
output containerAppEnvId string = containerAppEnv.id
output mcpServerUrls array = [for (server, i) in mcpServers: {
  name: server
  url: 'https://${mcpContainerApps[i].properties.configuration.ingress.fqdn}'
}]
