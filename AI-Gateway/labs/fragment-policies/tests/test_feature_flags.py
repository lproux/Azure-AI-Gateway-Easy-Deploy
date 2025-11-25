"""
Test suite for feature flag management.

This module tests:
- Feature flag creation
- Feature toggle functionality
- Feature flag naming conventions
- Default states
"""

import pytest
import json
from pathlib import Path
from typing import Dict
import subprocess
import os


class TestFeatureFlagConfiguration:
    """Test feature flag configuration."""

    @pytest.fixture(scope="class")
    def config(self) -> Dict:
        """Load fragment configuration."""
        config_path = Path(__file__).parent.parent / "config" / "fragment-config.json"
        return json.loads(config_path.read_text())

    def test_all_fragments_have_feature_flags(self, config):
        """Test that every fragment has an associated feature flag."""
        fragments = config["fragments"]
        feature_flags = config["feature_flags"]

        for fragment_id, fragment_config in fragments.items():
            feature_flag = fragment_config["feature_flag"]
            assert feature_flag in feature_flags, \
                f"Fragment {fragment_id} references undefined feature flag: {feature_flag}"

    def test_feature_flag_naming_convention(self, config):
        """Test that feature flags follow naming convention."""
        for flag_name in config["feature_flags"].keys():
            assert flag_name.startswith("feature-"), \
                f"Feature flag {flag_name} should start with 'feature-'"
            assert flag_name.endswith("-enabled"), \
                f"Feature flag {flag_name} should end with '-enabled'"

    def test_feature_flags_have_defaults(self, config):
        """Test that all feature flags have default values."""
        for flag_name, flag_config in config["feature_flags"].items():
            assert "default" in flag_config, \
                f"Feature flag {flag_name} missing default value"
            assert isinstance(flag_config["default"], bool), \
                f"Feature flag {flag_name} default must be boolean"

    def test_feature_flags_have_descriptions(self, config):
        """Test that all feature flags have descriptions."""
        for flag_name, flag_config in config["feature_flags"].items():
            assert "description" in flag_config, \
                f"Feature flag {flag_name} missing description"
            assert len(flag_config["description"]) > 10, \
                f"Feature flag {flag_name} description too short"

    def test_feature_flag_values_are_boolean(self, config):
        """Test that feature flag default values are boolean."""
        for flag_name, flag_config in config["feature_flags"].items():
            default = flag_config["default"]
            assert default in [True, False], \
                f"Feature flag {flag_name} default must be True or False, got {default}"


class TestFeatureFlagDefaults:
    """Test feature flag default states."""

    @pytest.fixture(scope="class")
    def config(self) -> Dict:
        config_path = Path(__file__).parent.parent / "config" / "fragment-config.json"
        return json.loads(config_path.read_text())

    def test_token_metrics_enabled_by_default(self, config):
        """Test that token metrics is enabled by default."""
        assert config["feature_flags"]["feature-token-metrics-enabled"]["default"] is True

    def test_load_balancing_enabled_by_default(self, config):
        """Test that load balancing is enabled by default."""
        assert config["feature_flags"]["feature-load-balancing-enabled"]["default"] is True

    def test_token_ratelimit_disabled_by_default(self, config):
        """Test that token rate limiting is disabled by default (for testing)."""
        assert config["feature_flags"]["feature-token-ratelimit-enabled"]["default"] is False

    def test_private_connectivity_disabled_by_default(self, config):
        """Test that private connectivity is disabled by default (requires setup)."""
        assert config["feature_flags"]["feature-private-connectivity-enabled"]["default"] is False

    def test_caching_disabled_by_default(self, config):
        """Test that caching is disabled by default (requires Redis)."""
        assert config["feature_flags"]["feature-caching-enabled"]["default"] is False

    def test_circuit_breaker_enabled_by_default(self, config):
        """Test that circuit breaker is enabled by default."""
        assert config["feature_flags"]["feature-circuit-breaker-enabled"]["default"] is True


class TestFeatureFlagNaming:
    """Test feature flag to fragment naming alignment."""

    @pytest.fixture(scope="class")
    def config(self) -> Dict:
        config_path = Path(__file__).parent.parent / "config" / "fragment-config.json"
        return json.loads(config_path.read_text())

    def test_fragment_to_feature_flag_mapping(self, config):
        """Test that fragment IDs map correctly to feature flags."""
        for fragment_id, fragment_config in config["fragments"].items():
            # Fragment ID: fragment-{name}
            # Feature flag: feature-{name}-enabled

            fragment_name = fragment_id.replace("fragment-", "")
            expected_flag = f"feature-{fragment_name}-enabled"
            actual_flag = fragment_config["feature_flag"]

            assert actual_flag == expected_flag, \
                f"Fragment {fragment_id} feature flag mismatch. Expected: {expected_flag}, Got: {actual_flag}"


class TestFeatureFlagIntegration:
    """Integration tests for feature flags (requires APIM service)."""

    @pytest.fixture(scope="class")
    def apim_config(self) -> Dict:
        """Load APIM configuration."""
        config_path = Path(__file__).parent.parent / "config" / "apim-config.json"
        if not config_path.exists():
            pytest.skip("APIM configuration not found")
        return json.loads(config_path.read_text())

    @pytest.mark.integration
    @pytest.mark.skipif(
        not os.getenv("APIM_SERVICE_NAME"),
        reason="APIM_SERVICE_NAME environment variable not set"
    )
    def test_can_create_named_value(self, apim_config):
        """Test that we can create a named value in APIM."""
        service_name = os.getenv("APIM_SERVICE_NAME")
        resource_group = apim_config.get("apim", {}).get("resource_group", "")

        if "${" in resource_group:
            pytest.skip("Resource group uses environment variables")

        # Try to create a test named value
        test_name = "test-feature-flag"
        test_value = "true"

        result = subprocess.run(
            f"az apim nv create-or-update --service-name {service_name} "
            f"--resource-group {resource_group} --named-value-id {test_name} "
            f"--value {test_value}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            # Clean up test named value
            subprocess.run(
                f"az apim nv delete --service-name {service_name} "
                f"--resource-group {resource_group} --named-value-id {test_name} -y",
                shell=True,
                capture_output=True,
                timeout=60
            )

        assert result.returncode == 0, f"Failed to create named value: {result.stderr}"


class TestFeatureFlagValues:
    """Test feature flag value constraints."""

    def test_feature_flag_true_string_representation(self):
        """Test that enabled feature flags use 'true' string."""
        assert str(True).lower() == "true"

    def test_feature_flag_false_string_representation(self):
        """Test that disabled feature flags use 'false' string."""
        assert str(False).lower() == "false"

    def test_feature_flag_boolean_conversion(self):
        """Test boolean to string conversion for APIM Named Values."""
        test_cases = [
            (True, "true"),
            (False, "false")
        ]

        for bool_val, expected_str in test_cases:
            actual_str = str(bool_val).lower()
            assert actual_str == expected_str, \
                f"Boolean {bool_val} should convert to '{expected_str}', got '{actual_str}'"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
