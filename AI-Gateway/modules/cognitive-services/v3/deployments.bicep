

@description('Configuration array for the model deployments')
param modelsConfig array = []

@description('Filter models by this service name')
param filterByService string = ''

param cognitiveServiceName string

resource cognitiveService 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: cognitiveServiceName
}

@batchSize(1)
resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = [for model in modelsConfig: if (model.?aiservice == filterByService) {
  name: model.name
  parent: cognitiveService
  sku: {
    name: model.sku
    capacity: model.capacity
  }
  properties: {
    model: {
      format: model.publisher
      name: model.name
      version: model.version
    }
    raiPolicyName: 'Microsoft.DefaultV2'
  }
}]
