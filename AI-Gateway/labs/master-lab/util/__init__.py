"""
Azure AI Gateway Deployment Utilities

One-command deployment for all labs and resources.
"""

from .deploy_all import (
    deploy_complete_infrastructure,
    DeploymentConfig,
    DeploymentProgress,
    ResourceOutputs
)

__all__ = [
    'deploy_complete_infrastructure',
    'DeploymentConfig',
    'DeploymentProgress',
    'ResourceOutputs'
]

__version__ = '1.0.0'
