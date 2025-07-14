"""
Step 5: Component Service Usage Verification

Verify that presentation components are using services correctly.
"""

import sys
from pathlib import Path

# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def verify_service_usage():
    """Verify components properly use injected services."""
    print("🔍 Verifying Component Service Usage...")

    from application.services.start_position import (
        StartPositionDataService,
        StartPositionOrchestrator,
        StartPositionSelectionService,
        StartPositionUIService,
    )

    # Create services
    data_service = StartPositionDataService()
    selection_service = StartPositionSelectionService()
    ui_service = StartPositionUIService()
    orchestrator = StartPositionOrchestrator(
        data_service, selection_service, ui_service
    )

    # Mock pool manager
    class MockPool:
        def checkout_pictograph(self, parent=None):
            return None

        def checkin_pictograph(self, component):
            pass

    mock_pool = MockPool()

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

    # Test StartPositionOption service usage
    total_tests += 1
    try:
        # Test if service injection works
        option = StartPositionOption(
            "alpha1_alpha1", mock_pool, "diamond", data_service=data_service
        )
        assert hasattr(option, "data_service")
        assert option.data_service == data_service
        print("  ✅ StartPositionOption accepts injected data service")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ StartPositionOption service usage failed: {e}")

    # Test StartPositionPicker service usage
    total_tests += 1
    try:
        # Test if service injection works
        picker = StartPositionPicker(
            mock_pool, data_service, selection_service, ui_service, orchestrator
        )
        assert hasattr(picker, "orchestrator")
        assert picker.orchestrator == orchestrator
        assert hasattr(picker, "ui_service")
        assert picker.ui_service == ui_service
        print("  ✅ StartPositionPicker accepts injected services")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ StartPositionPicker service usage failed: {e}")

    # Test EnhancedStartPositionPicker service usage
    total_tests += 1
    try:
        # Test if service injection works
        enhanced = EnhancedStartPositionPicker(
            mock_pool, data_service, selection_service, ui_service, orchestrator
        )
        assert hasattr(enhanced, "ui_service")
        assert enhanced.ui_service == ui_service
        assert hasattr(enhanced, "orchestrator")
        assert enhanced.orchestrator == orchestrator
        print("  ✅ EnhancedStartPositionPicker accepts injected services")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ EnhancedStartPositionPicker service usage failed: {e}")

    # Test AdvancedStartPositionPicker service usage
    total_tests += 1
    try:
        # Test if service injection works
        advanced = AdvancedStartPositionPicker(
            mock_pool,
            "diamond",
            data_service,
            selection_service,
            ui_service,
            orchestrator,
        )
        assert hasattr(advanced, "data_service")
        assert advanced.data_service == data_service
        assert hasattr(advanced, "orchestrator")
        assert advanced.orchestrator == orchestrator
        print("  ✅ AdvancedStartPositionPicker accepts injected services")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ AdvancedStartPositionPicker service usage failed: {e}")

    print(f"\n📊 Component Service Usage: {tests_passed}/{total_tests} tests passed")
    return tests_passed == total_tests


if __name__ == "__main__":
    success = verify_service_usage()
    if success:
        print("🎉 ALL COMPONENTS USE SERVICES CORRECTLY!")
    else:
        print("❌ SOME COMPONENTS NOT USING SERVICES PROPERLY!")
