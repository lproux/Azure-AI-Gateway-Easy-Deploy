"""
Pytest configuration and shared fixtures.
"""

import pytest
import os
from pathlib import Path


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test (requires APIM service)"
    )
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow running"
    )


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def fragments_dir(project_root) -> Path:
    """Get fragments directory."""
    return project_root / "fragments"


@pytest.fixture(scope="session")
def config_dir(project_root) -> Path:
    """Get config directory."""
    return project_root / "config"


@pytest.fixture(scope="session")
def is_ci_environment() -> bool:
    """Check if running in CI environment."""
    return os.getenv("CI", "false").lower() == "true"


@pytest.fixture(scope="session")
def has_apim_credentials() -> bool:
    """Check if APIM credentials are available."""
    return all([
        os.getenv("APIM_SERVICE_NAME"),
        os.getenv("AZURE_SUBSCRIPTION_ID"),
        os.getenv("AZURE_RESOURCE_GROUP")
    ])
