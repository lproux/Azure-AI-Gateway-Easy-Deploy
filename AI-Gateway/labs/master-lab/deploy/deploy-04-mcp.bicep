// Deploy Step 4: MCP Servers
// - Container Registry
// - Container Apps Environment
// - 7 MCP Server Container Apps (weather, github, product-catalog, place-order, ms-learn, excel, docs)
// - 4 MCP Server Container Instances (excel, docs, weather, github - for redundancy)

targetScope = 'resourceGroup'

// Parameters
@description('Primary location')
param location string = 'uksouth'

@description('Secondary location for ACI deployments')
param aciLocation string = 'eastus'

@description('Log Analytics Customer ID from Step 1')
param logAnalyticsCustomerId string

@description('Log Analytics Primary Shared Key from Step 1')
@secure()
param logAnalyticsPrimarySharedKey string

@description('External ACR for Excel/Docs MCP images')
param externalAcrServer string = 'acrmcpwksp321028.azurecr.io'

// Variables
var resourceSuffix = uniqueString(subscription().id, resourceGroup().id)
var shortSuffix = take(resourceSuffix, 10)  // Use shorter suffix for container app names (max 32 chars total)

// MCP Servers for Container Apps - 7 total
var mcpServers = [
  'weather'
  'github'
  'product-catalog'
  'place-order'
  'ms-learn'
  'excel'
  'docs'
]

// MCP Server Docker Images
// - Real images for weather, github (public Docker Hub / ghcr.io)
// - Excel/Docs from external ACR (acrmcpwksp321028)
// - Placeholder for product-catalog, place-order, ms-learn (demo only)
var mcpServerImages = {
  weather: 'mcp/openweather:latest'
  github: 'ghcr.io/github/github-mcp-server:latest'
  'product-catalog': 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
  'place-order': 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
  'ms-learn': 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
  excel: '${externalAcrServer}/excel-analytics-mcp:v4'
  docs: '${externalAcrServer}/research-docs-mcp:v2'
}

// MCP Server ports (most use 8080, excel/docs use 8000)
var mcpServerPorts = {
  weather: 8080
  github: 8080
  'product-catalog': 8080
  'place-order': 8080
  'ms-learn': 8080
  excel: 8000
  docs: 8000
}

// ACI deployments for redundancy (excel, docs, weather, github)
var aciServers = [
  {
    name: 'excel'
    image: '${externalAcrServer}/excel-analytics-mcp:v4'
    port: 8000
  }
  {
    name: 'docs'
    image: '${externalAcrServer}/research-docs-mcp:v2'
    port: 8000
  }
]

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

// 5. MCP Container Apps (7 servers)
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
        targetPort: mcpServerPorts[server]
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
          image: mcpServerImages[server]
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

// 6. MCP Container Instances (ACI) for redundancy - Excel and Docs
resource mcpContainerInstances 'Microsoft.ContainerInstance/containerGroups@2023-05-01' = [for server in aciServers: {
  name: '${server.name}-mcp-master'
  location: aciLocation
  properties: {
    containers: [
      {
        name: '${server.name}-mcp'
        properties: {
          image: server.image
          ports: [
            {
              port: server.port
              protocol: 'TCP'
            }
          ]
          resources: {
            requests: {
              cpu: 1
              memoryInGB: json('1.5')
            }
          }
        }
      }
    ]
    osType: 'Linux'
    restartPolicy: 'Always'
    ipAddress: {
      type: 'Public'
      ports: [
        {
          port: server.port
          protocol: 'TCP'
        }
      ]
      dnsNameLabel: '${server.name}-mcp-master'
    }
    imageRegistryCredentials: [
      {
        server: externalAcrServer
        username: 'acrmcpwksp321028'
        password: '' // Note: This needs to be provided at deployment time
      }
    ]
  }
}]

// Outputs
output containerRegistryName string = containerRegistry.name
output containerRegistryLoginServer string = containerRegistry.properties.loginServer
output containerAppEnvId string = containerAppEnv.id

// Container Apps URLs
output mcpServerUrls array = [for (server, i) in mcpServers: {
  name: server
  url: 'https://${mcpContainerApps[i].properties.configuration.ingress.fqdn}'
  type: 'containerApp'
}]

// Container Instances URLs
output mcpAciUrls array = [for (server, i) in aciServers: {
  name: server.name
  url: 'http://${mcpContainerInstances[i].properties.ipAddress.fqdn}:${server.port}'
  type: 'containerInstance'
}]

// Combined MCP URLs for easy consumption
output allMcpUrls array = concat(
  [for (server, i) in mcpServers: {
    name: server
    url: 'https://${mcpContainerApps[i].properties.configuration.ingress.fqdn}'
    type: 'containerApp'
  }],
  [for (server, i) in aciServers: {
    name: '${server.name}-aci'
    url: 'http://${mcpContainerInstances[i].properties.ipAddress.fqdn}:${server.port}'
    type: 'containerInstance'
  }]
)
