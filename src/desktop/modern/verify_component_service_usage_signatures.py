"""
Step 5: Component Service Usage Verification (Constructor Check Only)

Verify that presentation components have proper constructor signatures for service injection.
"""

import inspect
import sys
from pathlib import Path

# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def verify_service_usage():
    """Verify components have proper constructor signatures for service injection."""
    print("🔍 Verifying Component Service Usage...")

    tests_passed = 0
    total_tests = 0

    # Test imports first
    total_tests += 1
    try:
        from presentation.components.start_position_picker.advanced_start_position_picker import (
            AdvancedStartPositionPicker,
        )
        from presentation.components.start_position_picker.enhanced_start_position_picker import (
            EnhancedStartPositionPicker,
        )
        from presentation.components.start_position_picker.start_position_option import (
            StartPositionOption,
        )
        from presentation.components.start_position_picker.start_position_picker import (
            StartPositionPicker,
        )

        print("  ✅ All component imports successful")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Component imports failed: {e}")
        return tests_passed, total_tests

    # Test StartPositionOption constructor signature
    total_tests += 1
    try:
        sig = inspect.signature(StartPositionOption.__init__)
        params = list(sig.parameters.keys())

        # Check if it accepts data_service parameter
        assert "data_service" in params or any(
            "data_service" in str(p) for p in sig.parameters.values()
        )
        print("  ✅ StartPositionOption has data_service parameter")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ StartPositionOption constructor check failed: {e}")

    # Test StartPositionPicker constructor signature
    total_tests += 1
    try:
        sig = inspect.signature(StartPositionPicker.__init__)
        params = list(sig.parameters.keys())

        # Check if it accepts service parameters
        service_params = [
            "data_service",
            "selection_service",
            "ui_service",
            "orchestrator",
        ]
        found_services = [p for p in service_params if p in params]
        assert len(found_services) >= 2  # Should have at least some service parameters
        print(f"  ✅ StartPositionPicker has service parameters: {found_services}")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ StartPositionPicker constructor check failed: {e}")

    # Test EnhancedStartPositionPicker constructor signature
    total_tests += 1
    try:
        sig = inspect.signature(EnhancedStartPositionPicker.__init__)
        params = list(sig.parameters.keys())

        # Check if it accepts service parameters
        service_params = [
            "data_service",
            "selection_service",
            "ui_service",
            "orchestrator",
        ]
        found_services = [p for p in service_params if p in params]
        assert len(found_services) >= 2  # Should have at least some service parameters
        print(
            f"  ✅ EnhancedStartPositionPicker has service parameters: {found_services}"
        )
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ EnhancedStartPositionPicker constructor check failed: {e}")

    # Test AdvancedStartPositionPicker constructor signature
    total_tests += 1
    try:
        sig = inspect.signature(AdvancedStartPositionPicker.__init__)
        params = list(sig.parameters.keys())

        # Check if it accepts service parameters
        service_params = [
            "data_service",
            "selection_service",
            "ui_service",
            "orchestrator",
        ]
        found_services = [p for p in service_params if p in params]
        assert len(found_services) >= 2  # Should have at least some service parameters
        print(
            f"  ✅ AdvancedStartPositionPicker has service parameters: {found_services}"
        )
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ AdvancedStartPositionPicker constructor check failed: {e}")

    print(f"\n📊 Component Service Usage: {tests_passed}/{total_tests} tests passed")
    return tests_passed == total_tests


if __name__ == "__main__":
    success = verify_service_usage()
    if success:
        print("🎉 ALL COMPONENTS HAVE PROPER SERVICE INJECTION!")
    else:
        print("❌ SOME COMPONENTS MISSING SERVICE INJECTION!")
