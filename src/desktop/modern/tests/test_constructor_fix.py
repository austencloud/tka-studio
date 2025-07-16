"""Quick test to verify the constructor parameter fixes."""

import sys
from pathlib import Path

# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def test_constructor_parameters():
    """Test that all constructors work with correct parameters."""
    print("🔍 Testing constructor parameters...")

    try:
        # Test StartPositionOption
        from presentation.components.start_position_picker.start_position_option import (
            StartPositionOption,
        )

        # Mock pool manager
        class MockPool:
            def checkout_pictograph(self, parent=None):
                return None

            def checkin_pictograph(self, component):
                pass

        mock_pool = MockPool()

        # Test with correct parameters
        option = StartPositionOption(
            "alpha1_alpha1", mock_pool, "diamond", True  # enhanced_styling
        )

        print("✅ StartPositionOption constructor works correctly")

        # Test service imports
        from application.services.start_position.start_position_data_service import (
            StartPositionDataService,
        )
        from application.services.start_position.start_position_orchestrator import (
            StartPositionOrchestrator,
        )
        from application.services.start_position.start_position_selection_service import (
            StartPositionSelectionService,
        )
        from application.services.start_position.start_position_ui_service import (
            StartPositionUIService,
        )

        # Create services
        data_service = StartPositionDataService()
        selection_service = StartPositionSelectionService()
        ui_service = StartPositionUIService()
        orchestrator = StartPositionOrchestrator(
            data_service, selection_service, ui_service
        )

        print("✅ All services created successfully")

        # Test UI service calculate_option_size
        size = ui_service.calculate_option_size(1200, is_advanced=True)
        print(f"✅ UI service calculate_option_size returned: {size}px")

        # Test AdvancedStartPositionPicker constructor
        from presentation.components.start_position_picker.advanced_start_position_picker import (
            AdvancedStartPositionPicker,
        )

        # This should work now
        advanced_picker = AdvancedStartPositionPicker(
            mock_pool,
            data_service,
            selection_service,
            ui_service,
            orchestrator,
            "diamond",
        )

        print("✅ AdvancedStartPositionPicker constructor works correctly")

        print("\n🎉 All constructor parameter tests passed!")
        return True

    except Exception as e:
        print(f"❌ Constructor parameter test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_constructor_parameters()
    sys.exit(0 if success else 1)
