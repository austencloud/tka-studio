"""
Step 4: Service Functionality Tests

This script validates that all service methods work correctly.
"""

import sys
from pathlib import Path

# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def test_service_functionality():
    """Test all service methods work correctly."""
    print("🧪 Testing Service Functionality...")

    from desktop.modern.application.services.start_position import (
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

    tests_passed = 0
    total_tests = 0

    # Test data service
    total_tests += 1
    try:
        positions = data_service.get_available_positions("diamond")
        assert isinstance(positions, list)
        print(f"  ✅ Data service: Retrieved {len(positions)} positions")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Data service failed: {e}")

    # Test selection service
    total_tests += 1
    try:
        assert selection_service.validate_selection("alpha1_alpha1") == True
        assert selection_service.validate_selection("invalid") == False
        assert (
            selection_service.extract_end_position_from_key("alpha1_alpha1") == "alpha1"
        )
        assert selection_service.normalize_position_key("alpha1") == "alpha1_alpha1"
        print("  ✅ Selection service: All methods work correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Selection service failed: {e}")

    # Test UI service
    total_tests += 1
    try:
        size = ui_service.calculate_option_size(1000, False)
        assert 80 <= size <= 200

        positions = ui_service.get_positions_for_mode("diamond", False)
        assert len(positions) == 3

        advanced_positions = ui_service.get_positions_for_mode("diamond", True)
        assert len(advanced_positions) == 16

        layout_config = ui_service.get_grid_layout_config("diamond", False)
        assert layout_config["position_count"] == 3

        print("  ✅ UI service: All methods work correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ UI service failed: {e}")

    # Test orchestrator
    total_tests += 1
    try:
        from PyQt6.QtCore import QSize

        layout_params = orchestrator.calculate_responsive_layout(QSize(800, 600), 3)
        assert "rows" in layout_params
        assert "cols" in layout_params
        assert "option_size" in layout_params

        # Test with proper normalization flow
        normalized = selection_service.normalize_position_key("alpha1")
        assert normalized == "alpha1_alpha1"

        # Then validate the normalized key
        assert selection_service.validate_selection(normalized) == True

        print("  ✅ Orchestrator: All methods work correctly")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Orchestrator failed: {e}")

    print(f"\n📊 Service Functionality: {tests_passed}/{total_tests} tests passed")
    return tests_passed == total_tests


if __name__ == "__main__":
    success = test_service_functionality()
    if success:
        print("🎉 ALL SERVICE FUNCTIONALITY TESTS PASSED!")
    else:
        print("❌ SOME SERVICE FUNCTIONALITY TESTS FAILED!")
