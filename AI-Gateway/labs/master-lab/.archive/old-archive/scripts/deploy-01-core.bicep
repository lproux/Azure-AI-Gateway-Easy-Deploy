// Deploy Step 1: Core Infrastructure
// - Log Analytics Workspace
// - Application Insights
// - API Management (StandardV2)

targetScope = 'resourceGroup'

// Parameters
@description('API Management SKU')
@allowed(['Basicv2', 'Standardv2', 'Premium'])
param apimSku string = 'Standardv2'

@description('APIM subscriptions configuration')
param apimSubscriptionsConfig array = [
  { name: 'subscription1', displayName: 'Subscription 1' }
  { name: 'subscription2', displayName: 'Subscription 2' }
  { name: 'subscription3', displayName: 'Subscription 3' }
]

// Resources

// 1. Log Analytics Workspace
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

// Outputs
output logAnalyticsWorkspaceId string = lawModule.outputs.id
output logAnalyticsCustomerId string = lawModule.outputs.customerId
output logAnalyticsPrimarySharedKey string = lawModule.outputs.primarySharedKey

output appInsightsId string = appInsightsModule.outputs.id
output appInsightsName string = appInsightsModule.outputs.name
output appInsightsInstrumentationKey string = appInsightsModule.outputs.instrumentationKey

output apimServiceId string = apimModule.outputs.id
output apimServiceName string = apimModule.outputs.name
output apimGatewayUrl string = apimModule.outputs.gatewayUrl
output apimPrincipalId string = apimModule.outputs.principalId
output apimLoggerId string = apimModule.outputs.loggerId
output apimSubscriptions array = apimModule.outputs.apimSubscriptions
