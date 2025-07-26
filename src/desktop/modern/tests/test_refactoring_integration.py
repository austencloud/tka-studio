"""
Integration test for the PictographData/GlyphData refactoring.

This test verifies that our refactoring works correctly by testing
the complete flow from PictographData creation to glyph rendering.
"""

import pytest
from shared.application.services.pictograph.pictograph_visibility_manager import (
    get_pictograph_visibility_manager,
    reset_pictograph_visibility_manager,
)
from desktop.modern.domain.models.enums import (
    Direction,
    ElementalType,
    GridPosition,
    LetterType,
    Location,
    MotionType,
    Orientation,
    RotationDirection,
    Timing,
    VTGMode,
)
from desktop.modern.domain.models.grid_data import GridData
from desktop.modern.domain.models.motion_data import MotionData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.pictograph_utils import (
    compute_elemental_type_from_pictograph,
    compute_vtg_mode,
    get_turns_from_motions,
    has_dash_from_pictograph,
)


class TestRefactoringIntegration:
    """Test the complete refactored system integration."""

    def setup_method(self):
        """Set up test environment."""
        reset_pictograph_visibility_manager()

    def test_complete_pictograph_workflow(self):
        """Test complete workflow from PictographData creation to glyph computation."""
        # Create motion data
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.5,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
        )
        red_motion = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.EAST,
            end_loc=Location.WEST,
            turns=2.0,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
        )

        # Glyph data is no longer needed

        # Create PictographData with enum types
        pictograph_data = PictographData(
            motions={"blue": blue_motion, "red": red_motion},
            letter="A",
            start_position=GridPosition.ALPHA1,
            end_position=GridPosition.ALPHA3,
            timing=Timing.SPLIT,
            direction=Direction.SAME,
            letter_type=LetterType.TYPE1,
        )

        # Test that all enum fields are properly set
        assert pictograph_data.timing == Timing.SPLIT
        assert pictograph_data.direction == Direction.SAME
        assert pictograph_data.letter_type == LetterType.TYPE1
        assert pictograph_data.start_position == GridPosition.ALPHA1
        assert pictograph_data.end_position == GridPosition.ALPHA3

        # Test computed VTG mode
        vtg_mode = compute_vtg_mode(pictograph_data)
        assert vtg_mode == VTGMode.SPLIT_SAME

        # Test computed elemental type
        elemental_type = compute_elemental_type_from_pictograph(pictograph_data)
        assert elemental_type == ElementalType.WATER

        # Test dash detection
        has_dash = has_dash_from_pictograph(pictograph_data)
        assert has_dash is False  # Type1 doesn't have dash

        # Test turns extraction
        turns_data = get_turns_from_motions(pictograph_data)
        assert turns_data == "(1.5, 2.0)"

        # Test visibility manager
        visibility_manager = get_pictograph_visibility_manager()
        visibility_manager.initialize_pictograph_visibility(
            pictograph_data.id, pictograph_data.letter_type
        )

        # Type1 should show elemental and VTG
        assert (
            visibility_manager.get_pictograph_visibility(
                pictograph_data.id, "elemental"
            )
            is True
        )
        assert (
            visibility_manager.get_pictograph_visibility(pictograph_data.id, "vtg")
            is True
        )
        assert (
            visibility_manager.get_pictograph_visibility(pictograph_data.id, "tka")
            is True
        )
        assert (
            visibility_manager.get_pictograph_visibility(
                pictograph_data.id, "positions"
            )
            is True
        )

    def test_serialization_with_enums(self):
        """Test that serialization works correctly with enum types."""
        # Create PictographData with enum types
        pictograph_data = PictographData(
            letter="W-",
            timing=Timing.TOG,
            direction=Direction.OPP,
            letter_type=LetterType.TYPE3,
            start_position=GridPosition.BETA1,
            end_position=GridPosition.BETA3,
        )

        # Test serialization to dict
        data_dict = pictograph_data.to_dict()
        assert data_dict["timing"] == "tog"
        assert data_dict["direction"] == "opp"
        assert data_dict["letter_type"] == "Type3"
        assert data_dict["start_position"] == "beta1"
        assert data_dict["end_position"] == "beta3"

        # Test deserialization from dict
        restored_pictograph = PictographData.from_dict(data_dict)
        assert restored_pictograph.timing == Timing.TOG
        assert restored_pictograph.direction == Direction.OPP
        assert restored_pictograph.letter_type == LetterType.TYPE3
        assert restored_pictograph.start_position == GridPosition.BETA1
        assert restored_pictograph.end_position == GridPosition.BETA3

        # Test that computed values work correctly
        vtg_mode = compute_vtg_mode(restored_pictograph)
        assert vtg_mode == VTGMode.TOG_OPP

        elemental_type = compute_elemental_type_from_pictograph(restored_pictograph)
        assert elemental_type == ElementalType.AIR

        has_dash = has_dash_from_pictograph(restored_pictograph)
        assert has_dash is True  # Type3 has dash

    def test_backward_compatibility(self):
        """Test that old string-based data can still be loaded."""
        # Create data dict with old string format
        old_data = {
            "id": "test-id",
            "letter": "B",
            "timing": "split",  # Old string format
            "direction": "opp",  # Old string format
            "letter_type": "Type2",  # Old string format
            "start_position": "gamma1",  # Old string format
            "end_position": "gamma3",  # Old string format
            "glyph_data": {},
            "grid_data": {},
            "arrows": {},
            "props": {},
            "motions": {},
            "beat": 1,
            "is_blank": False,
            "is_mirrored": False,
            "metadata": {},
        }

        # Should be able to load old format
        pictograph_data = PictographData.from_dict(old_data)
        assert pictograph_data.timing == Timing.SPLIT
        assert pictograph_data.direction == Direction.OPP
        assert pictograph_data.letter_type == LetterType.TYPE2
        assert pictograph_data.start_position == GridPosition.GAMMA1
        assert pictograph_data.end_position == GridPosition.GAMMA3

    def test_type6_visibility_rules(self):
        """Test visibility rules for Type6 (static) letters."""
        pictograph_data = PictographData(
            letter="α",
            letter_type=LetterType.TYPE6,
        )

        visibility_manager = get_pictograph_visibility_manager()
        visibility_manager.initialize_pictograph_visibility(
            pictograph_data.id, pictograph_data.letter_type
        )

        # Type6 should not show elemental, VTG, or positions
        assert (
            visibility_manager.get_pictograph_visibility(
                pictograph_data.id, "elemental"
            )
            is False
        )
        assert (
            visibility_manager.get_pictograph_visibility(pictograph_data.id, "vtg")
            is False
        )
        assert (
            visibility_manager.get_pictograph_visibility(pictograph_data.id, "tka")
            is True
        )  # Always show TKA
        assert (
            visibility_manager.get_pictograph_visibility(
                pictograph_data.id, "positions"
            )
            is False
        )

    def test_glyph_data_removal(self):
        """Test that GlyphData has been completely removed."""
        # GlyphData should no longer exist
        try:
            from desktop.modern.domain.models.glyph_data import GlyphData

            assert False, "GlyphData should have been removed"
        except ImportError:
            pass  # Expected - GlyphData should not exist

    def test_global_visibility_overrides(self):
        """Test global visibility overrides work correctly."""
        pictograph_data = PictographData(
            letter="A",
            letter_type=LetterType.TYPE1,
        )

        visibility_manager = get_pictograph_visibility_manager()
        visibility_manager.initialize_pictograph_visibility(
            pictograph_data.id, pictograph_data.letter_type
        )

        # Initially should show elemental
        assert (
            visibility_manager.get_pictograph_visibility(
                pictograph_data.id, "elemental"
            )
            is True
        )

        # Set global override to hide elemental
        visibility_manager.set_global_visibility("elemental", False)

        # Should now be hidden due to global override
        assert (
            visibility_manager.get_pictograph_visibility(
                pictograph_data.id, "elemental"
            )
            is False
        )

        # Reset global visibility
        visibility_manager.set_global_visibility("elemental", True)

        # Should be visible again
        assert (
            visibility_manager.get_pictograph_visibility(
                pictograph_data.id, "elemental"
            )
            is True
        )
