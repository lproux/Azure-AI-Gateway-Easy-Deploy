"""Azure AI Gateway Quick Start Module

Provides simplified initialization and helper functions for Azure AI Gateway labs.
"""

__version__ = "1.0.0"

from .shared_init import (
    quick_init,
    load_environment,
    get_azure_openai_client,
    get_cosmos_client,
    get_search_client,
)

__all__ = [
    "quick_init",
    "load_environment",
    "get_azure_openai_client",
    "get_cosmos_client",
    "get_search_client",
]
