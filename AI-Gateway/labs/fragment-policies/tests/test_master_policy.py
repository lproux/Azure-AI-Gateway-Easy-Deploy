"""
Test suite for master policy generation and application.

This module tests:
- Master policy XML generation
- Conditional fragment inclusion
- Policy structure validation
- Fragment ordering
"""

import pytest
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List
import re


class TestMasterPolicyGeneration:
    """Test master policy generation logic."""

    @pytest.fixture(scope="class")
    def fragment_config(self) -> Dict:
        """Load fragment configuration."""
        config_path = Path(__file__).parent.parent / "config" / "fragment-config.json"
        return json.loads(config_path.read_text())

    def generate_master_policy(self, enabled_fragments: List[str], fragments_config: Dict) -> str:
        """
        Generate master API policy with conditional fragment includes.

        This is a test implementation matching the notebook's logic.
        """
        inbound_fragments = []
        backend_fragments = []
        outbound_fragments = []
        onerror_fragments = []

        for fragment_id in enabled_fragments:
            if fragment_id not in fragments_config["fragments"]:
                continue

            fragment_info = fragments_config["fragments"][fragment_id]
            applies_to = fragment_info["applies_to"]
            feature_flag = fragment_info["feature_flag"]

            # Create conditional include block
            include_block = f'''
        <choose>
            <when condition="@({{{{named-value-{feature_flag}}}}} == &quot;true&quot;)">
                <include-fragment fragment-id="{fragment_id}" />
            </when>
        </choose>'''

            # Add to appropriate sections
            if "inbound" in applies_to:
                inbound_fragments.append(include_block)
            if "backend" in applies_to:
                backend_fragments.append(include_block)
            if "outbound" in applies_to:
                outbound_fragments.append(include_block)
            if "on-error" in applies_to:
                onerror_fragments.append(include_block)

        # Generate complete policy
        policy_xml = f"""<policies>
    <inbound>
        <base />
{''.join(inbound_fragments)}
    </inbound>
    <backend>
        <base />
{''.join(backend_fragments)}
    </backend>
    <outbound>
        <base />
{''.join(outbound_fragments)}
    </outbound>
    <on-error>
        <base />
{''.join(onerror_fragments)}
    </on-error>
</policies>"""

        return policy_xml

    def test_master_policy_basic_structure(self, fragment_config):
        """Test that generated master policy has correct XML structure."""
        all_fragments = list(fragment_config["fragments"].keys())
        policy_xml = self.generate_master_policy(all_fragments, fragment_config)

        # Parse XML
        try:
            root = ET.fromstring(policy_xml)
        except ET.ParseError as e:
            pytest.fail(f"Generated policy XML is invalid: {e}")

        assert root.tag == "policies", "Root element must be <policies>"

        # Check for required sections
        sections = [child.tag for child in root]
        assert "inbound" in sections, "Missing <inbound> section"
        assert "backend" in sections, "Missing <backend> section"
        assert "outbound" in sections, "Missing <outbound> section"
        assert "on-error" in sections, "Missing <on-error> section"

    def test_master_policy_has_base_policies(self, fragment_config):
        """Test that each section includes <base /> policy."""
        all_fragments = list(fragment_config["fragments"].keys())
        policy_xml = self.generate_master_policy(all_fragments, fragment_config)

        root = ET.fromstring(policy_xml)

        for section in ["inbound", "backend", "outbound", "on-error"]:
            section_elem = root.find(section)
            assert section_elem is not None, f"Missing {section} section"

            # Check for <base /> as first child
            children = list(section_elem)
            if children:  # Some sections might be empty except for base
                assert children[0].tag == "base", f"{section} section should start with <base />"

    def test_master_policy_conditional_includes(self, fragment_config):
        """Test that fragment includes are wrapped in conditional logic."""
        all_fragments = list(fragment_config["fragments"].keys())
        policy_xml = self.generate_master_policy(all_fragments, fragment_config)

        # Check for conditional includes
        assert "<choose>" in policy_xml, "Policy should contain <choose> elements"
        assert "<when" in policy_xml, "Policy should contain <when> elements"
        assert "include-fragment" in policy_xml, "Policy should contain <include-fragment> elements"

    def test_master_policy_fragment_ordering(self, fragment_config):
        """Test that fragments are included in correct order."""
        deployment_order = fragment_config["deployment_order"]
        policy_xml = self.generate_master_policy(deployment_order, fragment_config)

        # Extract all fragment-id references in order
        fragment_refs = re.findall(r'fragment-id="([^"]+)"', policy_xml)

        # Verify they appear in deployment order
        expected_order = [
            fid for fid in deployment_order
            if fid in fragment_config["fragments"]
        ]

        assert fragment_refs == expected_order, \
            f"Fragments not in deployment order. Expected: {expected_order}, Got: {fragment_refs}"

    def test_master_policy_section_mapping(self, fragment_config):
        """Test that fragments appear in correct policy sections."""
        all_fragments = list(fragment_config["fragments"].keys())
        policy_xml = self.generate_master_policy(all_fragments, fragment_config)

        root = ET.fromstring(policy_xml)

        for fragment_id, fragment_info in fragment_config["fragments"].items():
            applies_to = fragment_info["applies_to"]

            for section in applies_to:
                section_elem = root.find(section)
                section_xml = ET.tostring(section_elem, encoding='unicode')

                assert fragment_id in section_xml, \
                    f"Fragment {fragment_id} should be in {section} section"

    def test_master_policy_feature_flag_references(self, fragment_config):
        """Test that master policy references correct feature flags."""
        all_fragments = list(fragment_config["fragments"].keys())
        policy_xml = self.generate_master_policy(all_fragments, fragment_config)

        for fragment_id, fragment_info in fragment_config["fragments"].items():
            feature_flag = fragment_info["feature_flag"]

            # Check that feature flag is referenced in policy
            assert f"named-value-{feature_flag}" in policy_xml, \
                f"Master policy should reference feature flag: {feature_flag}"

    def test_master_policy_empty_fragments(self, fragment_config):
        """Test master policy generation with no fragments."""
        policy_xml = self.generate_master_policy([], fragment_config)

        root = ET.fromstring(policy_xml)

        # Should still have all sections with base policies
        for section in ["inbound", "backend", "outbound", "on-error"]:
            section_elem = root.find(section)
            assert section_elem is not None
            base = section_elem.find("base")
            assert base is not None

    def test_master_policy_single_fragment(self, fragment_config):
        """Test master policy generation with single fragment."""
        fragment_id = "fragment-token-metrics"
        policy_xml = self.generate_master_policy([fragment_id], fragment_config)

        # Should contain only one fragment reference
        fragment_refs = re.findall(r'fragment-id="([^"]+)"', policy_xml)
        assert len(fragment_refs) == 1
        assert fragment_refs[0] == fragment_id


class TestMasterPolicyValidation:
    """Test master policy validation rules."""

    @pytest.fixture
    def sample_policy_xml(self) -> str:
        """Sample master policy XML."""
        return """<policies>
    <inbound>
        <base />
        <choose>
            <when condition="@({{{{named-value-feature-token-metrics-enabled}}}} == &quot;true&quot;)">
                <include-fragment fragment-id="fragment-token-metrics" />
            </when>
        </choose>
    </inbound>
    <backend>
        <base />
    </backend>
    <outbound>
        <base />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>"""

    def test_policy_xml_well_formed(self, sample_policy_xml):
        """Test that policy XML is well-formed."""
        try:
            ET.fromstring(sample_policy_xml)
        except ET.ParseError as e:
            pytest.fail(f"Policy XML is not well-formed: {e}")

    def test_policy_has_all_sections(self, sample_policy_xml):
        """Test that policy contains all required sections."""
        root = ET.fromstring(sample_policy_xml)

        required_sections = ["inbound", "backend", "outbound", "on-error"]
        actual_sections = [child.tag for child in root]

        for section in required_sections:
            assert section in actual_sections, f"Missing required section: {section}"

    def test_policy_named_value_syntax(self, sample_policy_xml):
        """Test that named values use correct syntax."""
        # Named values should be {{{{named-value-xxx}}}} (double braces, escaped in XML)
        assert "{{{{named-value-" in sample_policy_xml
        assert "}}}}" in sample_policy_xml

    def test_policy_condition_syntax(self, sample_policy_xml):
        """Test that conditions use correct syntax."""
        assert "@(" in sample_policy_xml
        assert "&quot;true&quot;" in sample_policy_xml  # Escaped quotes


class TestMasterPolicyIntegration:
    """Integration tests for master policy application."""

    @pytest.fixture(scope="class")
    def fragment_config(self) -> Dict:
        config_path = Path(__file__).parent.parent / "config" / "fragment-config.json"
        return json.loads(config_path.read_text())

    def test_all_fragments_can_be_included(self, fragment_config):
        """Test that all configured fragments can be included in master policy."""
        from test_master_policy import TestMasterPolicyGeneration

        generator = TestMasterPolicyGeneration()
        all_fragments = list(fragment_config["fragments"].keys())

        # Should not raise exception
        try:
            policy_xml = generator.generate_master_policy(all_fragments, fragment_config)
            ET.fromstring(policy_xml)  # Validate XML
        except Exception as e:
            pytest.fail(f"Failed to generate master policy with all fragments: {e}")

    def test_policy_size_reasonable(self, fragment_config):
        """Test that generated policy size is reasonable."""
        from test_master_policy import TestMasterPolicyGeneration

        generator = TestMasterPolicyGeneration()
        all_fragments = list(fragment_config["fragments"].keys())
        policy_xml = generator.generate_master_policy(all_fragments, fragment_config)

        # Policy should be reasonable size (not empty, not too large)
        assert len(policy_xml) > 500, "Policy too small"
        assert len(policy_xml) < 100000, "Policy too large"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
