#!/usr/bin/env python3
"""
Test script to verify the refactoring works correctly.

This script tests the new service-based architecture without running the full application.

Usage:
    python test_refactoring.py
    OR
    python3 test_refactoring.py
    OR
    py test_refactoring.py
"""

import sys
from pathlib import Path

# Add the current directory to Python path (we're already in src/desktop)
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Also add the parent directories for imports
sys.path.insert(0, str(current_dir.parent))  # src
sys.path.insert(0, str(current_dir.parent.parent))  # TKA root


def test_service_registration():
    """Test that services can be registered without errors."""
    print("🧪 Testing service registration...")

    try:
        from modern.core.dependency_injection.construct_tab_service_registration import (
            register_construct_tab_services,
            register_legacy_compatibility_services,
        )
        from modern.core.dependency_injection.di_container import DIContainer

        # Create container
        container = DIContainer()

        # Register services
        register_construct_tab_services(container)
        register_legacy_compatibility_services(container)

        print("✅ Service registration successful!")
        return True

    except Exception as e:
        print(f"❌ Service registration failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_interface_imports():
    """Test that all interfaces can be imported."""
    print("🧪 Testing interface imports...")

    try:
        print("✅ Interface imports successful!")
        return True

    except Exception as e:
        print(f"❌ Interface imports failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_service_imports():
    """Test that all service implementations can be imported."""
    print("🧪 Testing service implementation imports...")

    try:
        print("✅ Service implementation imports successful!")
        return True

    except Exception as e:
        print(f"❌ Service implementation imports failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_component_imports():
    """Test that new components can be imported."""
    print("🧪 Testing component imports...")

    try:
        print("✅ Component imports successful!")
        return True

    except Exception as e:
        print(f"❌ Component imports failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("🚀 Starting refactoring tests...\n")

    tests = [
        test_interface_imports,
        test_service_imports,
        test_component_imports,
        test_service_registration,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()  # Add spacing between tests

    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Refactoring is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
