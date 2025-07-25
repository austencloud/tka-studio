"""
Final verification test for the refactoring.
"""


def test_final_verification():
    """Test that all core functionality works correctly after refactoring."""
    # Test basic imports and functionality
    from application.services.pictograph.pictograph_visibility_manager import (
        get_pictograph_visibility_manager,
    )
    from domain.models.enums import Direction, GridPosition, LetterType, Timing, VTGMode
    from domain.models.pictograph_data import PictographData
    from domain.models.pictograph_utils import (
        compute_vtg_mode,
        has_dash_from_pictograph,
    )

    # Test creating a pictograph with enum types
    pictograph = PictographData(
        letter="A",
        timing=Timing.SPLIT,
        direction=Direction.SAME,
        letter_type=LetterType.TYPE1,
        start_position=GridPosition.ALPHA1,
        end_position=GridPosition.ALPHA3,
    )

    # Test serialization
    data = pictograph.to_dict()
    restored = PictographData.from_dict(data)

    # Test utility functions
    vtg_mode = compute_vtg_mode(pictograph)
    has_dash = has_dash_from_pictograph(pictograph)

    # Test visibility manager
    vm = get_pictograph_visibility_manager()
    vm.initialize_pictograph_visibility(pictograph.id, pictograph.letter_type)

    # Assertions
    assert vtg_mode == VTGMode.SPLIT_SAME
    assert has_dash is False
    assert pictograph.timing == Timing.SPLIT
    assert pictograph.direction == Direction.SAME
    assert pictograph.letter_type == LetterType.TYPE1
    assert restored.timing == Timing.SPLIT
    assert restored.direction == Direction.SAME
    assert restored.letter_type == LetterType.TYPE1

    print("✅ All core functionality working correctly!")
    print(f"VTG Mode: {vtg_mode}")
    print(f"Has Dash: {has_dash}")
    print(f"Timing: {pictograph.timing}")
    print(f"Direction: {pictograph.direction}")
    print(f"Letter Type: {pictograph.letter_type}")
