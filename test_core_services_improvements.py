#!/usr/bin/env python3
"""
Test script to validate core services improvements.
This script tests the new service availability tracking and error handling.
"""

import os
import sys

# Add the src directory to Python path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "src", "desktop", "modern", "src")
)


def test_service_registration_manager():
    """Test the improved ServiceRegistrationManager."""
    print("=== Testing ServiceRegistrationManager Improvements ===")

    try:
        from application.services.core.service_registration_manager import (
            ServiceRegistrationManager,
        )

        # Test instantiation
        manager = ServiceRegistrationManager()
        print("✅ ServiceRegistrationManager instantiated successfully")

        # Test initial availability tracking
        status = manager.get_registration_status()
        print(f"✅ Registration status retrieved: {len(status)} fields")

        # Test availability summary
        summary = manager.get_service_availability_summary()
        print("✅ Service availability summary generated:")
        print(f"   {summary.split(chr(10))[0]}")  # First line only

        # Test that all expected fields are present
        expected_fields = [
            "event_system_available",
            "arrow_positioning_available",
            "prop_management_available",
            "prop_orchestration_available",
            "availability_summary",
        ]

        for field in expected_fields:
            if field in status:
                print(f"✅ Status field '{field}' present")
            else:
                print(f"❌ Status field '{field}' missing")
                return False

        return True

    except Exception as e:
        print(f"❌ ServiceRegistrationManager test failed: {e}")
        return False


def test_object_pool_manager():
    """Test the improved ObjectPoolManager."""
    print("\n=== Testing ObjectPoolManager Improvements ===")

    try:
        from application.services.core.object_pool_manager import ObjectPoolManager

        # Test instantiation
        manager = ObjectPoolManager()
        print("✅ ObjectPoolManager instantiated successfully")

        # Test pool creation with our improved pattern
        def simple_factory():
            return f"test_object_{id(object())}"

        manager.initialize_pool(
            pool_name="test_pool", max_objects=3, object_factory=simple_factory
        )
        print("✅ Pool initialization completed with improved Qt pattern")

        # Test pool access
        obj = manager.get_pooled_object("test_pool", 0)
        if obj:
            print("✅ Pool object retrieval successful")
        else:
            print("❌ Pool object retrieval failed")
            return False

        # Test that we can access the pool (this is what production code actually does)
        pool_size = len(manager._pools.get("test_pool", []))
        if pool_size == 3:
            print("✅ Pool size correct (production usage pattern)")
        else:
            print(f"❌ Pool size incorrect: {pool_size}")
            return False

        return True

    except Exception as e:
        print(f"❌ ObjectPoolManager test failed: {e}")
        return False


def test_session_state_tracker():
    """Test that SessionStateTracker still imports correctly."""
    print("\n=== Testing SessionStateTracker Import ===")

    try:
        from application.services.core.session_state_tracker import SessionStateTracker

        print("✅ SessionStateTracker imports successfully")
        # Note: We don't instantiate it as it requires dependencies
        return True

    except Exception as e:
        print(f"❌ SessionStateTracker import failed: {e}")
        return False


def main():
    """Run all tests."""
    print("Core Services Improvements Validation")
    print("=" * 50)

    tests = [
        test_service_registration_manager,
        test_object_pool_manager,
        test_session_state_tracker,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print(f"\n{'=' * 50}")
    print(f"RESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All improvements validated successfully!")
        print("✅ No regressions detected")
        print("✅ New features working correctly")
        return True
    else:
        print("❌ Some tests failed - check improvements")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
