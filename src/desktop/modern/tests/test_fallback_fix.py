"""
Quick test to verify the StartPositionOption fallback fix.
"""

import sys
from pathlib import Path

# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def test_start_position_option_fallback():
    """Test that StartPositionOption works without injected services."""
    print("🔍 Testing StartPositionOption fallback fix...")

    try:
        # Create mock pool manager
        class MockPoolManager:
            def checkout_pictograph(self, parent=None):
                return None

            def checkin_pictograph(self, component):
                pass

        mock_pool = MockPoolManager()

        # Test 1: StartPositionOption with correct constructor parameters
        print("  Testing StartPositionOption with correct constructor...")
        from presentation.components.start_position_picker.start_position_option import (
            StartPositionOption,
        )

        option = StartPositionOption(
            "alpha1_alpha1", mock_pool, "diamond", True  # enhanced_styling
        )

        # Verify it was created successfully
        assert option.position_key == "alpha1_alpha1"
        assert option.grid_mode == "diamond"
        assert option.enhanced_styling == True

        # Verify the service has the get_position_data method
        assert hasattr(option.data_service, "get_position_data")

        print("    ✅ StartPositionOption fallback works correctly")

        # Test 2: Verify the method call would work
        print("  Testing that get_position_data method exists...")
        try:
            # This should not raise an AttributeError
            method = getattr(option.data_service, "get_position_data")
            assert callable(method)
            print("    ✅ get_position_data method is callable")
        except AttributeError as e:
            print(f"    ❌ get_position_data method missing: {e}")
            return False

        print("🎉 StartPositionOption fallback fix verified!")
        return True

    except Exception as e:
        print(f"❌ StartPositionOption fallback test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_start_position_option_fallback()
    if success:
        print("✅ FALLBACK FIX VERIFIED - Ready to test in application")
    else:
        print("❌ FALLBACK FIX FAILED - Check the errors above")
