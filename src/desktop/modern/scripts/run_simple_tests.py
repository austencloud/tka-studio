#!/usr/bin/env python3
"""
Simple test runner for Start Position Services.
"""

from __future__ import annotations

import os
from pathlib import Path
import sys


# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Set environment to avoid conftest import issues
os.environ["PYTHONPATH"] = str(src_path)


def run_start_position_service_tests():
    """Run just the start position service tests manually."""
    print("🧪 Running Start Position Service Tests")
    print("=" * 50)

    try:
        # Import the service classes
        from desktop.modern.application.services.start_position import (
            StartPositionDataService,
            StartPositionOrchestrator,
            StartPositionSelectionService,
            StartPositionUIService,
        )
        from desktop.modern.core.interfaces.start_position_services import (
            IStartPositionDataService,
            IStartPositionOrchestrator,
            IStartPositionSelectionService,
            IStartPositionUIService,
        )

        passed = 0
        failed = 0

        # Test 1: Data Service Interface Implementation
        print("🔍 Testing StartPositionDataService...")
        try:
            service = StartPositionDataService()
            assert isinstance(service, IStartPositionDataService)
            print("  ✅ test_service_implements_interface - PASSED")
            passed += 1
        except Exception as e:
            print(f"  ❌ test_service_implements_interface - FAILED: {e}")
            failed += 1

        # Test 2: Selection Service Interface Implementation
        print("🔍 Testing StartPositionSelectionService...")
        try:
            service = StartPositionSelectionService()
            assert isinstance(service, IStartPositionSelectionService)
            print("  ✅ test_service_implements_interface - PASSED")
            passed += 1
        except Exception as e:
            print(f"  ❌ test_service_implements_interface - FAILED: {e}")
            failed += 1

        # Test 3: UI Service Interface Implementation
        print("🔍 Testing StartPositionUIService...")
        try:
            service = StartPositionUIService()
            assert isinstance(service, IStartPositionUIService)
            print("  ✅ test_service_implements_interface - PASSED")
            passed += 1
        except Exception as e:
            print(f"  ❌ test_service_implements_interface - FAILED: {e}")
            failed += 1

        # Test 4: Orchestrator Interface Implementation
        print("🔍 Testing StartPositionOrchestrator...")
        try:
            # Create mock dependencies
            data_service = StartPositionDataService()
            selection_service = StartPositionSelectionService()
            ui_service = StartPositionUIService()

            service = StartPositionOrchestrator(
                data_service, selection_service, ui_service
            )
            assert isinstance(service, IStartPositionOrchestrator)
            print("  ✅ test_service_implements_interface - PASSED")
            passed += 1
        except Exception as e:
            print(f"  ❌ test_service_implements_interface - FAILED: {e}")
            failed += 1

        # Test 5: Basic functionality
        print("🔍 Testing basic functionality...")
        try:
            selection_service = StartPositionSelectionService()
            result = selection_service.validate_selection("alpha1_alpha1")
            assert result == True
            print("  ✅ test_basic_functionality - PASSED")
            passed += 1
        except Exception as e:
            print(f"  ❌ test_basic_functionality - FAILED: {e}")
            failed += 1

        print("=" * 50)
        print(f"📊 Test Results: {passed}/{passed + failed} tests passed")

        if failed == 0:
            print("✅ ALL TESTS PASSED!")
            return True
        print(f"❌ {failed} tests failed")
        return False

    except Exception as e:
        print(f"❌ Test setup failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_start_position_service_tests()
    sys.exit(0 if success else 1)
