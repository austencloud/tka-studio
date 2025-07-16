"""
Test the cleaned-up service architecture - Quick validation
"""

import sys
from pathlib import Path

# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def test_clean_architecture():
    """Test that cleaned-up architecture works correctly."""
    print("🧪 Testing Clean Architecture...")

    # Test service imports
    try:
        from application.services.start_position import (
            StartPositionDataService,
            StartPositionOrchestrator,
            StartPositionSelectionService,
            StartPositionUIService,
        )

        print("✅ Service imports successful")
    except Exception as e:
        print(f"❌ Service imports failed: {e}")
        return False

    # Test service instantiation
    try:
        data_service = StartPositionDataService()
        selection_service = StartPositionSelectionService()
        ui_service = StartPositionUIService()
        orchestrator = StartPositionOrchestrator(
            data_service, selection_service, ui_service
        )
        print("✅ Service instantiation successful")
    except Exception as e:
        print(f"❌ Service instantiation failed: {e}")
        return False

    # Test component imports
    try:
        from presentation.components.start_position_picker.start_position_option import (
            StartPositionOption,
        )

        print("✅ Component imports successful")
    except Exception as e:
        print(f"❌ Component imports failed: {e}")
        return False

    # Test component construction with new signature
    try:
        from application.services.pictograph_pool_manager import PictographPoolManager

        # Mock pool manager
        class MockPool:
            def checkout_pictograph(self, parent=None):
                return None

            def checkin_pictograph(self, component):
                pass

        mock_pool = MockPool()

        # Test with new signature (no Optional parameters)
        option = StartPositionOption(
            "alpha1_alpha1", mock_pool, "diamond", True  # enhanced_styling
        )
        print("✅ Component construction with clean signature successful")
    except Exception as e:
        print(f"❌ Component construction failed: {e}")
        return False

    print("🎉 Clean architecture validation passed!")
    return True


if __name__ == "__main__":
    success = test_clean_architecture()
    if success:
        print("\n✅ CLEAN ARCHITECTURE VALIDATION PASSED!")
    else:
        print("\n❌ CLEAN ARCHITECTURE VALIDATION FAILED!")
