"""Test to verify advanced picker positions and pictograph loading."""

import sys
from pathlib import Path

# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def test_advanced_picker_positions():
    """Test that advanced picker has correct positions."""
    print("🔍 Testing advanced picker positions...")

    try:
        from application.services.start_position.start_position_ui_service import (
            StartPositionUIService,
        )

        service = StartPositionUIService()

        # Test diamond positions
        diamond_positions = service.get_positions_for_mode("diamond", is_advanced=True)
        print(f"✅ Diamond advanced positions: {len(diamond_positions)} positions")
        print(f"   First few: {diamond_positions[:5]}")

        # Test box positions
        box_positions = service.get_positions_for_mode("box", is_advanced=True)
        print(f"✅ Box advanced positions: {len(box_positions)} positions")
        print(f"   First few: {box_positions[:5]}")

        # Verify we have exactly 16 positions for each mode
        assert (
            len(diamond_positions) == 16
        ), f"Expected 16 diamond positions, got {len(diamond_positions)}"
        assert (
            len(box_positions) == 16
        ), f"Expected 16 box positions, got {len(box_positions)}"

        # Test basic positions
        basic_diamond = service.get_positions_for_mode("diamond", is_advanced=False)
        basic_box = service.get_positions_for_mode("box", is_advanced=False)

        print(f"✅ Basic diamond positions: {basic_diamond}")
        print(f"✅ Basic box positions: {basic_box}")

        # Verify basic positions
        assert (
            len(basic_diamond) == 3
        ), f"Expected 3 basic diamond positions, got {len(basic_diamond)}"
        assert (
            len(basic_box) == 3
        ), f"Expected 3 basic box positions, got {len(basic_box)}"

        # Test option size calculation
        size_advanced = service.calculate_option_size(1200, is_advanced=True)
        size_basic = service.calculate_option_size(1200, is_advanced=False)

        print(f"✅ Option size for advanced (1200px container): {size_advanced}px")
        print(f"✅ Option size for basic (1200px container): {size_basic}px")

        # Verify sizes are reasonable
        assert (
            120 <= size_advanced <= 300
        ), f"Advanced size {size_advanced} outside expected range [120, 300]"
        assert (
            80 <= size_basic <= 200
        ), f"Basic size {size_basic} outside expected range [80, 200]"

        print("\n🎉 All advanced picker position tests passed!")
        return True

    except Exception as e:
        print(f"❌ Advanced picker position test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_advanced_picker_positions()
    sys.exit(0 if success else 1)
