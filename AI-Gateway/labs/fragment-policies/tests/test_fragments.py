"""
Test suite for APIM policy fragments.

This module tests individual fragments for:
- Valid XML syntax
- Correct policy structure
- Named value references
- Fragment deployment
- Policy application
"""

import pytest
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List
import subprocess


class TestFragmentStructure:
    """Test fragment XML structure and validity."""

    @pytest.fixture(scope="class")
    def fragments_dir(self) -> Path:
        """Get fragments directory path."""
        return Path(__file__).parent.parent / "fragments"

    @pytest.fixture(scope="class")
    def fragment_config(self) -> Dict:
        """Load fragment configuration."""
        config_path = Path(__file__).parent.parent / "config" / "fragment-config.json"
        return json.loads(config_path.read_text())

    def test_fragments_directory_exists(self, fragments_dir):
        """Test that fragments directory exists."""
        assert fragments_dir.exists(), f"Fragments directory not found: {fragments_dir}"
        assert fragments_dir.is_dir(), f"Fragments path is not a directory: {fragments_dir}"

    def test_all_fragment_files_exist(self, fragments_dir, fragment_config):
        """Test that all configured fragment files exist."""
        for fragment_id, config in fragment_config["fragments"].items():
            fragment_file = fragments_dir / Path(config["file"]).name
            assert fragment_file.exists(), f"Fragment file not found: {fragment_file}"

    def test_fragment_xml_valid(self, fragments_dir):
        """Test that all fragment XML files are valid."""
        for xml_file in fragments_dir.glob("*.xml"):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                assert root.tag == "fragment", f"Root element must be <fragment> in {xml_file.name}"
            except ET.ParseError as e:
                pytest.fail(f"Invalid XML in {xml_file.name}: {e}")

    def test_fragment_has_content(self, fragments_dir):
        """Test that fragments are not empty."""
        for xml_file in fragments_dir.glob("*.xml"):
            content = xml_file.read_text().strip()
            assert len(content) > 50, f"Fragment {xml_file.name} appears to be empty or too small"
            assert "<fragment>" in content, f"Fragment {xml_file.name} missing <fragment> tag"
            assert "</fragment>" in content, f"Fragment {xml_file.name} missing </fragment> closing tag"

    def test_fragment_named_value_references(self, fragments_dir, fragment_config):
        """Test that fragments reference configured named values correctly."""
        for fragment_id, config in fragment_config["fragments"].items():
            fragment_file = fragments_dir / Path(config["file"]).name
            content = fragment_file.read_text()

            # Check for named value syntax: {{{{named-value-...}}}}
            if "configuration" in config:
                for config_key in config["configuration"].keys():
                    # Named values in fragments use double curly braces (escaped in JSON)
                    expected_ref = f"{{{{named-value-{config_key}}}}}"
                    assert expected_ref in content, \
                        f"Fragment {fragment_id} should reference named value: {expected_ref}"


class TestFragmentContent:
    """Test specific fragment content and policies."""

    @pytest.fixture(scope="class")
    def fragments_dir(self) -> Path:
        return Path(__file__).parent.parent / "fragments"

    def test_token_metrics_fragment(self, fragments_dir):
        """Test token metrics fragment contains required policies."""
        fragment = fragments_dir / "token-metrics.xml"
        content = fragment.read_text()

        assert "azure-openai-emit-token-metric" in content
        assert "dimension" in content
        assert "Subscription ID" in content or "subscription" in content.lower()

    def test_load_balancing_fragment(self, fragments_dir):
        """Test load balancing fragment contains required policies."""
        fragment = fragments_dir / "load-balancing.xml"
        content = fragment.read_text()

        assert "set-backend-service" in content
        assert "backend-id" in content
        assert "retry" in content or "forward-request" in content

    def test_token_ratelimit_fragment(self, fragments_dir):
        """Test token rate limiting fragment contains required policies."""
        fragment = fragments_dir / "token-ratelimit.xml"
        content = fragment.read_text()

        assert "azure-openai-token-limit" in content
        assert "tokens-per-minute" in content
        assert "counter-key" in content

    def test_private_connectivity_fragment(self, fragments_dir):
        """Test private connectivity fragment contains required policies."""
        fragment = fragments_dir / "private-connectivity.xml"
        content = fragment.read_text()

        assert "authentication-managed-identity" in content
        assert "cognitiveservices.azure.com" in content
        assert "set-header" in content
        assert "Authorization" in content

    def test_caching_fragment(self, fragments_dir):
        """Test caching fragment contains required policies."""
        fragment = fragments_dir / "caching.xml"
        content = fragment.read_text()

        assert "azure-openai-semantic-cache-lookup" in content or "cache-lookup" in content
        assert "azure-openai-semantic-cache-store" in content or "cache-store" in content

    def test_circuit_breaker_fragment(self, fragments_dir):
        """Test circuit breaker fragment contains required logic."""
        fragment = fragments_dir / "circuit-breaker.xml"
        content = fragment.read_text()

        assert "circuit" in content.lower()
        assert "choose" in content
        assert "when" in content
        assert "503" in content or "return-response" in content


class TestFragmentConfiguration:
    """Test fragment configuration file."""

    @pytest.fixture(scope="class")
    def config(self) -> Dict:
        config_path = Path(__file__).parent.parent / "config" / "fragment-config.json"
        return json.loads(config_path.read_text())

    def test_config_has_version(self, config):
        """Test configuration has version field."""
        assert "version" in config
        assert isinstance(config["version"], str)

    def test_config_has_fragments(self, config):
        """Test configuration defines fragments."""
        assert "fragments" in config
        assert len(config["fragments"]) > 0

    def test_config_has_feature_flags(self, config):
        """Test configuration defines feature flags."""
        assert "feature_flags" in config
        assert len(config["feature_flags"]) > 0

    def test_fragment_definitions_complete(self, config):
        """Test that all fragment definitions are complete."""
        required_fields = ["id", "description", "file", "applies_to", "feature_flag"]

        for fragment_id, fragment_config in config["fragments"].items():
            for field in required_fields:
                assert field in fragment_config, \
                    f"Fragment {fragment_id} missing required field: {field}"

    def test_applies_to_valid(self, config):
        """Test that applies_to contains valid policy sections."""
        valid_sections = ["inbound", "backend", "outbound", "on-error"]

        for fragment_id, fragment_config in config["fragments"].items():
            applies_to = fragment_config["applies_to"]
            assert isinstance(applies_to, list), \
                f"Fragment {fragment_id}: applies_to must be a list"

            for section in applies_to:
                assert section in valid_sections, \
                    f"Fragment {fragment_id}: invalid section '{section}'"

    def test_deployment_order_exists(self, config):
        """Test that deployment order is defined."""
        assert "deployment_order" in config
        assert isinstance(config["deployment_order"], list)

    def test_all_fragments_in_deployment_order(self, config):
        """Test that all fragments appear in deployment order."""
        fragment_ids = set(config["fragments"].keys())
        deployment_order = set(config["deployment_order"])

        assert fragment_ids == deployment_order, \
            f"Deployment order mismatch. Missing: {fragment_ids - deployment_order}, Extra: {deployment_order - fragment_ids}"


class TestFragmentDeployment:
    """Integration tests for fragment deployment (requires APIM service)."""

    @pytest.fixture(scope="class")
    def apim_config(self) -> Dict:
        """Load APIM configuration."""
        config_path = Path(__file__).parent.parent / "config" / "apim-config.json"
        if not config_path.exists():
            pytest.skip("APIM configuration not found")
        return json.loads(config_path.read_text())

    @pytest.mark.integration
    @pytest.mark.skipif(
        "APIM_SERVICE_NAME" not in str(subprocess.run("env", shell=True, capture_output=True).stdout),
        reason="APIM_SERVICE_NAME not set"
    )
    def test_can_list_fragments(self, apim_config):
        """Test that we can list fragments from APIM."""
        service_name = apim_config.get("apim", {}).get("service_name", "")
        resource_group = apim_config.get("apim", {}).get("resource_group", "")

        if "${" in service_name or "${" in resource_group:
            pytest.skip("APIM configuration uses environment variables")

        result = subprocess.run(
            f"az apim api policy-fragment list --service-name {service_name} --resource-group {resource_group}",
            shell=True,
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Failed to list fragments: {result.stderr}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
