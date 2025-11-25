#!/usr/bin/env python3
"""
Test script to validate the deployment module imports correctly.
"""

import sys
from pathlib import Path

# Add parent directory to path if needed
util_parent = Path(__file__).parent.parent
if str(util_parent) not in sys.path:
    sys.path.insert(0, str(util_parent))


def test_imports():
    """Test that all imports work correctly"""
    print("Testing imports...")

    try:
        from util import (
            deploy_complete_infrastructure,
            DeploymentConfig,
            DeploymentProgress,
            ResourceOutputs
        )
        print("✅ Main exports imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import main exports: {e}")
        return False

    try:
        from util.deploy_all import (
            generate_random_suffix,
            compile_bicep_template,
            create_credential,
            verify_prerequisites,
            DEFAULT_PRIMARY_MODELS,
            DEFAULT_SECONDARY_MODELS,
            MCP_SERVERS,
            AI_FOUNDRY_REGIONS
        )
        print("✅ Internal functions imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import internal functions: {e}")
        return False

    return True


def test_data_classes():
    """Test that data classes can be instantiated"""
    print("\nTesting data classes...")

    try:
        from util import DeploymentConfig, DeploymentProgress, ResourceOutputs

        # Test DeploymentConfig
        config = DeploymentConfig(
            subscription_id='test-sub-id',
            resource_group='test-rg'
        )
        print(f"✅ DeploymentConfig created with suffix: {config.resource_suffix}")

        # Test DeploymentProgress
        progress = DeploymentProgress(
            step="Test Step",
            status="in_progress",
            message="Testing..."
        )
        print(f"✅ DeploymentProgress created: {progress.step}")

        # Test ResourceOutputs
        outputs = ResourceOutputs()
        print("✅ ResourceOutputs created")

        return True

    except Exception as e:
        print(f"❌ Failed to create data classes: {e}")
        return False


def test_default_configs():
    """Test that default configurations are valid"""
    print("\nTesting default configurations...")

    try:
        from util.deploy_all import (
            DEFAULT_PRIMARY_MODELS,
            DEFAULT_SECONDARY_MODELS,
            MCP_SERVERS,
            AI_FOUNDRY_REGIONS
        )

        print(f"✅ PRIMARY_MODELS: {len(DEFAULT_PRIMARY_MODELS)} models")
        for model in DEFAULT_PRIMARY_MODELS:
            print(f"   - {model['name']} v{model['version']}")

        print(f"✅ SECONDARY_MODELS: {len(DEFAULT_SECONDARY_MODELS)} models")
        for model in DEFAULT_SECONDARY_MODELS:
            print(f"   - {model['name']} v{model['version']}")

        print(f"✅ MCP_SERVERS: {len(MCP_SERVERS)} servers")
        for server in MCP_SERVERS:
            print(f"   - {server['name']}")

        print(f"✅ AI_FOUNDRY_REGIONS: {len(AI_FOUNDRY_REGIONS)} regions")
        for region in AI_FOUNDRY_REGIONS:
            print(f"   - {region['short_name']} ({region['location']})")

        return True

    except Exception as e:
        print(f"❌ Failed to validate default configs: {e}")
        return False


def test_utility_functions():
    """Test utility functions"""
    print("\nTesting utility functions...")

    try:
        from util.deploy_all import generate_random_suffix

        suffix1 = generate_random_suffix()
        suffix2 = generate_random_suffix()

        print(f"✅ Random suffix 1: {suffix1}")
        print(f"✅ Random suffix 2: {suffix2}")

        assert len(suffix1) == 13, "Suffix should be 13 characters"
        assert suffix1 != suffix2, "Suffixes should be unique"
        assert suffix1.islower(), "Suffix should be lowercase"

        print("✅ Suffix generation works correctly")

        return True

    except Exception as e:
        print(f"❌ Failed to test utility functions: {e}")
        return False


def test_resource_outputs_methods():
    """Test ResourceOutputs methods"""
    print("\nTesting ResourceOutputs methods...")

    try:
        from util import ResourceOutputs
        import tempfile
        import os

        outputs = ResourceOutputs(
            apim_gateway_url='https://test-apim.azure-api.net',
            apim_service_name='test-apim',
            apim_subscription_key='test-key',
            foundry1_endpoint='https://foundry1.openai.azure.com',
            redis_host='test-redis.redis.cache.windows.net',
            resource_suffix='test123'
        )

        # Test to_env_file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env') as f:
            env_file = f.name

        try:
            outputs.to_env_file(env_file)
            assert os.path.exists(env_file), "ENV file should be created"

            with open(env_file) as f:
                content = f.read()
                assert 'APIM_GATEWAY_URL=https://test-apim.azure-api.net' in content
                assert 'REDIS_HOST=test-redis.redis.cache.windows.net' in content

            print(f"✅ to_env_file works correctly")

        finally:
            if os.path.exists(env_file):
                os.remove(env_file)

        # Test to_json
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json_file = f.name

        try:
            outputs.to_json(json_file)
            assert os.path.exists(json_file), "JSON file should be created"

            import json
            with open(json_file) as f:
                data = json.load(f)
                assert data['apim_gateway_url'] == 'https://test-apim.azure-api.net'
                assert data['resource_suffix'] == 'test123'

            print(f"✅ to_json works correctly")

        finally:
            if os.path.exists(json_file):
                os.remove(json_file)

        return True

    except Exception as e:
        print(f"❌ Failed to test ResourceOutputs methods: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 70)
    print("DEPLOYMENT MODULE VALIDATION")
    print("=" * 70)

    tests = [
        ("Imports", test_imports),
        ("Data Classes", test_data_classes),
        ("Default Configurations", test_default_configs),
        ("Utility Functions", test_utility_functions),
        ("ResourceOutputs Methods", test_resource_outputs_methods)
    ]

    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))

    print("\n" + "=" * 70)
    print("TEST RESULTS")
    print("=" * 70)

    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
        if not result:
            all_passed = False

    print("=" * 70)

    if all_passed:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
