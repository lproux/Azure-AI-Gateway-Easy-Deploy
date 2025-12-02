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

// External ACR parameter removed - all images now use public registries (MCR/GHCR)
// param externalAcrServer string = 'acrmcpwksp321028.azurecr.io'

@description('OpenWeather API Key for weather MCP server (free tier from https://openweathermap.org/api)')
@secure()
param owmApiKey string = ''

@description('Pre-created ACR name (if provided, uses existing ACR; otherwise creates new one)')
param existingAcrName string = ''

// Variables
var resourceSuffix = uniqueString(subscription().id, resourceGroup().id)
var shortSuffix = take(resourceSuffix, 10)  // Use shorter suffix for container app names (max 32 chars total)
var useExistingAcr = !empty(existingAcrName)

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
// Weather and Excel use local ACR images (built by deploy_all.py before this deployment)
// Other servers use public images
var mcpServerImages = {
  weather: '${containerRegistryName}.azurecr.io/weather-mcp:latest'  // Built from mcp-http-wrappers/weather-mcp
  github: 'ghcr.io/github/github-mcp-server:latest'
  'product-catalog': 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
  'place-order': 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
  'ms-learn': 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
  excel: '${containerRegistryName}.azurecr.io/excel-mcp:latest'  // Built from mcp-http-wrappers/excel-mcp
  docs: 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'  // Placeholder for docs MCP
}

// Container Registry name - use existing if provided, otherwise generate
var containerRegistryName = useExistingAcr ? existingAcrName : 'acr${resourceSuffix}'

// MCP Server ports
var mcpServerPorts = {
  weather: 8080
  github: 8080
  'product-catalog': 8080
  'place-order': 8080
  'ms-learn': 8080
  excel: 8000  // Excel MCP uses port 8000
  docs: 8080   // Using placeholder image (port 8080)
}

// MCP Server environment variables
var mcpServerEnvVars = {
  weather: !empty(owmApiKey) ? [
    { name: 'OWM_API_KEY', secretRef: 'owm-api-key' }
  ] : []
  github: []
  'product-catalog': []
  'place-order': []
  'ms-learn': []
  excel: []
  docs: []
}

// MCP Server secrets
var mcpServerSecrets = {
  weather: !empty(owmApiKey) ? [
    { name: 'owm-api-key', value: owmApiKey }
  ] : []
  github: []
  'product-catalog': []
  'place-order': []
  'ms-learn': []
  excel: []
  docs: []
}

// ACI deployments for redundancy (excel, docs)
// Using local ACR images for excel, placeholder for docs
var aciServers = [
  {
    name: 'excel'
    image: '${containerRegistryName}.azurecr.io/excel-mcp:latest'  // Built from mcp-http-wrappers/excel-mcp
    port: 8000  // Excel MCP uses port 8000
  }
  {
    name: 'docs'
    image: 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'  // Placeholder for docs MCP
    port: 8080
  }
]

// Resources

// 1. Container Registry - create only if not using existing
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-11-01-preview' = if (!useExistingAcr) {
  name: containerRegistryName
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
    publicNetworkAccess: 'Enabled'
  }
}

// Reference existing ACR if provided
resource existingContainerRegistry 'Microsoft.ContainerRegistry/registries@2023-11-01-preview' existing = if (useExistingAcr) {
  name: existingAcrName
}

// Helper variable to get the right ACR reference
// Note: These use conditional expressions that are safe because only one path is evaluated
var acrLoginServer = useExistingAcr ? existingContainerRegistry.properties.loginServer : containerRegistry!.properties.loginServer
var acrCredentials = useExistingAcr ? existingContainerRegistry.listCredentials() : containerRegistry!.listCredentials()

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
          server: acrLoginServer
        }
      ]
      secrets: mcpServerSecrets[server]
    }
    template: {
      containers: [
        {
          name: server
          image: mcpServerImages[server]
          env: mcpServerEnvVars[server]
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
  name: '${server.name}-mcp-${shortSuffix}'
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
      dnsNameLabel: '${server.name}-mcp-${shortSuffix}'
    }
    // Credentials for ACR - only needed for excel which uses local ACR image
    imageRegistryCredentials: server.name == 'excel' ? [
      {
        server: acrLoginServer
        username: acrCredentials.username
        password: acrCredentials.passwords[0].value
      }
    ] : []
  }
}]

// Outputs
output containerRegistryName string = containerRegistryName
output containerRegistryLoginServer string = acrLoginServer
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

// Note: Combined URLs can be computed in the deployment script by merging mcpServerUrls and mcpAciUrls
