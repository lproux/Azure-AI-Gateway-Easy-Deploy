"""
Reusable modules for AI Gateway Workshop
Future optimization: Import these instead of duplicating code
"""

import os
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Optional, List, Any
from datetime import datetime


@dataclass
class WorkshopConfig:
    """Environment configuration container"""
    subscription_id: str = ""
    resource_group: str = ""
    location: str = "eastus2"
    apim_gateway_url: str = ""
    apim_service_name: str = ""
    apim_api_key: str = ""
    openai_endpoint: Optional[str] = None
    cosmos_endpoint: Optional[str] = None
    redis_endpoint: Optional[str] = None

    @classmethod
    def from_env(cls, env_file: str = 'master-lab.env'):
        """Load configuration from environment file"""
        from dotenv import load_dotenv

        config = cls()
        env_path = Path(env_file)

        if env_path.exists():
            load_dotenv(env_path)
            config.subscription_id = os.environ.get('SUBSCRIPTION_ID', '')
            config.resource_group = os.environ.get('RESOURCE_GROUP', '')
            config.location = os.environ.get('LOCATION', 'eastus2')
            config.apim_gateway_url = os.environ.get('APIM_GATEWAY_URL', '')
            config.apim_service_name = os.environ.get('APIM_SERVICE_NAME', '')
            config.apim_api_key = os.environ.get('APIM_API_KEY', '')
            config.openai_endpoint = os.environ.get('OPENAI_ENDPOINT')
            config.cosmos_endpoint = os.environ.get('COSMOS_ENDPOINT')
            config.redis_endpoint = os.environ.get('REDIS_ENDPOINT')

        return config

    def validate(self) -> List[str]:
        """Validate required fields, return list of missing fields"""
        missing = []
        if not self.subscription_id:
            missing.append('subscription_id')
        if not self.resource_group:
            missing.append('resource_group')
        if not self.apim_gateway_url:
            missing.append('apim_gateway_url')
        return missing


class AzureOps:
    """Azure operations wrapper for deployments and resource management"""

    def __init__(self, credential, subscription_id: str):
        from azure.mgmt.resource import ResourceManagementClient

        self.credential = credential
        self.subscription_id = subscription_id
        self.resource_client = ResourceManagementClient(credential, subscription_id)

    def ensure_resource_group(self, name: str, location: str):
        """Create or update resource group"""
        rg = self.resource_client.resource_groups.create_or_update(
            name,
            {"location": location}
        )
        return rg

    def deploy_bicep(self, resource_group: str, template_path: str, parameters: Dict) -> Dict:
        """Deploy Bicep template and return outputs"""
        from azure.mgmt.resource.resources.models import DeploymentMode

        deployment_name = f"deploy-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        poller = self.resource_client.deployments.begin_create_or_update(
            resource_group,
            deployment_name,
            {
                "properties": {
                    "template_link": {"uri": template_path},
                    "parameters": parameters,
                    "mode": DeploymentMode.incremental
                }
            }
        )

        result = poller.result()
        return result.properties.outputs or {}

    def get_deployment_outputs(self, resource_group: str, deployment_name: str) -> Dict:
        """Get outputs from an existing deployment"""
        deployment = self.resource_client.deployments.get(resource_group, deployment_name)
        return deployment.properties.outputs or {}


class MCPClient:
    """MCP client wrapper for Model Context Protocol operations"""

    def __init__(self, base_url: str = None):
        self.base_url = base_url
        self._connected = False

    def connect(self, server_url: str) -> bool:
        """Connect to MCP server"""
        import httpx

        try:
            response = httpx.get(f"{server_url}/health", timeout=5)
            self._connected = response.status_code == 200
            return self._connected
        except Exception:
            self._connected = False
            return False

    def list_tools(self) -> List[Dict]:
        """List available MCP tools"""
        if not self._connected:
            return []

        import httpx
        try:
            response = httpx.get(f"{self.base_url}/tools")
            return response.json().get('tools', [])
        except Exception:
            return []

    def call_tool(self, tool_name: str, arguments: Dict) -> Any:
        """Call an MCP tool with arguments"""
        if not self._connected:
            raise RuntimeError("Not connected to MCP server")

        import httpx
        response = httpx.post(
            f"{self.base_url}/tools/{tool_name}",
            json=arguments
        )
        return response.json()


def generate_env_from_outputs(deployment_outputs: Dict, filepath: str = 'master-lab.env') -> str:
    """Generate master-lab.env content from deployment outputs"""
    lines = [
        "# Auto-generated from deployment outputs",
        f"# Generated: {datetime.now().isoformat()}",
        ""
    ]

    for key, value in deployment_outputs.items():
        # Handle nested output format from ARM
        if isinstance(value, dict) and 'value' in value:
            value = value['value']
        lines.append(f"{key.upper()}={value}")

    content = "\n".join(lines)

    with open(filepath, 'w') as f:
        f.write(content)

    return filepath


def get_apim_token(credential) -> str:
    """Get management token for APIM operations"""
    token = credential.get_token("https://management.azure.com/.default")
    return token.token


def apply_apim_policy(
    subscription_id: str,
    resource_group: str,
    service_name: str,
    api_id: str,
    policy_xml: str,
    credential
) -> bool:
    """Apply APIM policy via REST API"""
    import requests

    token = get_apim_token(credential)

    url = (
        f"https://management.azure.com/subscriptions/{subscription_id}"
        f"/resourceGroups/{resource_group}"
        f"/providers/Microsoft.ApiManagement/service/{service_name}"
        f"/apis/{api_id}/policies/policy?api-version=2022-08-01"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    body = {
        "properties": {
            "value": policy_xml,
            "format": "xml"
        }
    }

    response = requests.put(url, headers=headers, json=body)
    return response.status_code in [200, 201]


def test_openai_via_apim(
    gateway_url: str,
    api_key: str,
    api_path: str = "/openai/deployments/gpt-4o-mini/chat/completions",
    message: str = "Hello"
) -> Dict:
    """Test OpenAI completion via APIM gateway"""
    import requests
    import time

    url = f"{gateway_url}{api_path}?api-version=2024-02-01"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json"
    }

    body = {
        "messages": [{"role": "user", "content": message}],
        "max_tokens": 100
    }

    start = time.time()
    response = requests.post(url, headers=headers, json=body)
    elapsed = time.time() - start

    return {
        "status_code": response.status_code,
        "elapsed": elapsed,
        "response": response.json() if response.ok else response.text
    }


# Utility functions
def detect_environment() -> Dict[str, bool]:
    """Detect current execution environment"""
    import os

    return {
        "codespace": bool(os.environ.get('CODESPACE_NAME')),
        "wsl": 'microsoft' in os.uname().release.lower() if hasattr(os, 'uname') else False,
        "windows": os.name == 'nt',
        "linux": os.name == 'posix'
    }


def find_az_cli() -> Optional[str]:
    """Find Azure CLI executable path"""
    import shutil

    # Common locations
    paths = [
        shutil.which('az'),
        '/usr/bin/az',
        '/usr/local/bin/az',
        'C:\\Program Files (x86)\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd',
        'C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd'
    ]

    for path in paths:
        if path and Path(path).exists():
            return str(path)

    return None
