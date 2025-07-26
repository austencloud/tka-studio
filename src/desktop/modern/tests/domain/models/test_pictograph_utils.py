"""
Tests for pictograph utility functions.

Tests the utility functions that compute derived data from PictographData,
replacing the redundant fields that were previously stored in GlyphData.
"""

import pytest
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
    compute_elemental_type,
    compute_elemental_type_from_pictograph,
    compute_vtg_mode,
    get_turns_from_motions,
    has_dash,
    has_dash_from_letter_string,
    has_dash_from_pictograph,
    should_show_elemental,
    should_show_positions,
    should_show_tka,
    should_show_vtg,
)


class TestVTGModeComputation:
    """Test VTG mode computation from timing and direction."""

    def test_split_same(self):
        """Test SPLIT_SAME VTG mode computation."""
        pictograph = PictographData(
            timing=Timing.SPLIT,
            direction=Direction.SAME,
        )
        result = compute_vtg_mode(pictograph)
        assert result == VTGMode.SPLIT_SAME

    def test_split_opp(self):
        """Test SPLIT_OPP VTG mode computation."""
        pictograph = PictographData(
            timing=Timing.SPLIT,
            direction=Direction.OPP,
        )
        result = compute_vtg_mode(pictograph)
        assert result == VTGMode.SPLIT_OPP

    def test_tog_same(self):
        """Test TOG_SAME VTG mode computation."""
        pictograph = PictographData(
            timing=Timing.TOG,
            direction=Direction.SAME,
        )
        result = compute_vtg_mode(pictograph)
        assert result == VTGMode.TOG_SAME

    def test_tog_opp(self):
        """Test TOG_OPP VTG mode computation."""
        pictograph = PictographData(
            timing=Timing.TOG,
            direction=Direction.OPP,
        )
        result = compute_vtg_mode(pictograph)
        assert result == VTGMode.TOG_OPP

    def test_missing_timing(self):
        """Test VTG mode computation with missing timing."""
        pictograph = PictographData(
            direction=Direction.SAME,
        )
        result = compute_vtg_mode(pictograph)
        assert result is None

    def test_missing_direction(self):
        """Test VTG mode computation with missing direction."""
        pictograph = PictographData(
            timing=Timing.SPLIT,
        )
        result = compute_vtg_mode(pictograph)
        assert result is None


class TestElementalTypeComputation:
    """Test elemental type computation from VTG mode."""

    def test_vtg_to_elemental_mapping(self):
        """Test all VTG mode to elemental type mappings."""
        mappings = {
            VTGMode.SPLIT_SAME: ElementalType.WATER,
            VTGMode.SPLIT_OPP: ElementalType.FIRE,
            VTGMode.TOG_SAME: ElementalType.EARTH,
            VTGMode.TOG_OPP: ElementalType.AIR,
            VTGMode.QUARTER_SAME: ElementalType.SUN,
            VTGMode.QUARTER_OPP: ElementalType.MOON,
        }

        for vtg_mode, expected_elemental in mappings.items():
            result = compute_elemental_type(vtg_mode)
            assert result == expected_elemental

    def test_none_vtg_mode(self):
        """Test elemental type computation with None VTG mode."""
        result = compute_elemental_type(None)
        assert result is None

    def test_from_pictograph(self):
        """Test elemental type computation directly from pictograph."""
        pictograph = PictographData(
            timing=Timing.SPLIT,
            direction=Direction.SAME,
        )
        result = compute_elemental_type_from_pictograph(pictograph)
        assert result == ElementalType.WATER


class TestDashDetection:
    """Test dash detection functions."""

    def test_has_dash_type3(self):
        """Test dash detection for Type3 letters."""
        assert has_dash(LetterType.TYPE3) is True

    def test_has_dash_type5(self):
        """Test dash detection for Type5 letters."""
        assert has_dash(LetterType.TYPE5) is True

    def test_no_dash_type1(self):
        """Test no dash for Type1 letters."""
        assert has_dash(LetterType.TYPE1) is False

    def test_no_dash_none(self):
        """Test no dash for None letter type."""
        assert has_dash(None) is False

    def test_dash_from_string(self):
        """Test dash detection from letter string."""
        assert has_dash_from_letter_string("W-") is True
        assert has_dash_from_letter_string("A") is False
        assert has_dash_from_letter_string(None) is False

    def test_dash_from_pictograph_with_type(self):
        """Test dash detection from pictograph with letter type."""
        pictograph = PictographData(
            letter="W-",
            letter_type=LetterType.TYPE3,
        )
        assert has_dash_from_pictograph(pictograph) is True

    def test_dash_from_pictograph_fallback(self):
        """Test dash detection from pictograph fallback to string."""
        pictograph = PictographData(
            letter="W-",
        )
        assert has_dash_from_pictograph(pictograph) is True


class TestTurnsExtraction:
    """Test turns data extraction from motions."""

    def test_turns_from_motions(self):
        """Test turns extraction from motion data."""
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

        pictograph = PictographData(motions={"blue": blue_motion, "red": red_motion})

        result = get_turns_from_motions(pictograph)
        assert result == "(1.5, 2.0)"

    def test_no_motions(self):
        """Test turns extraction with no motions."""
        pictograph = PictographData()
        result = get_turns_from_motions(pictograph)
        assert result is None


class TestVisibilityRules:
    """Test visibility rule functions."""

    def test_show_elemental_type1(self):
        """Test elemental visibility for Type1."""
        assert should_show_elemental(LetterType.TYPE1) is True

    def test_show_elemental_other_types(self):
        """Test elemental visibility for other types."""
        assert should_show_elemental(LetterType.TYPE2) is False
        assert should_show_elemental(None) is False

    def test_show_vtg_type1(self):
        """Test VTG visibility for Type1."""
        assert should_show_vtg(LetterType.TYPE1) is True

    def test_show_vtg_other_types(self):
        """Test VTG visibility for other types."""
        assert should_show_vtg(LetterType.TYPE2) is False
        assert should_show_vtg(None) is False

    def test_show_positions_not_type6(self):
        """Test position visibility for non-Type6."""
        assert should_show_positions(LetterType.TYPE1) is True
        assert should_show_positions(LetterType.TYPE2) is True

    def test_show_positions_type6(self):
        """Test position visibility for Type6 (static)."""
        assert should_show_positions(LetterType.TYPE6) is False

    def test_show_positions_none(self):
        """Test position visibility for None."""
        assert should_show_positions(None) is True

    def test_show_tka_always(self):
        """Test TKA visibility (always True)."""
        assert should_show_tka(LetterType.TYPE1) is True
        assert should_show_tka(LetterType.TYPE6) is True
        assert should_show_tka(None) is True


class TestPictographDataEnumUpgrade:
    """Test that PictographData properly uses enum types."""

    def test_enum_field_types(self):
        """Test that PictographData fields accept enum types."""
        pictograph = PictographData(
            timing=Timing.SPLIT,
            direction=Direction.SAME,
            letter_type=LetterType.TYPE1,
            start_position=GridPosition.ALPHA1,
            end_position=GridPosition.ALPHA3,
        )

        assert pictograph.timing == Timing.SPLIT
        assert pictograph.direction == Direction.SAME
        assert pictograph.letter_type == LetterType.TYPE1
        assert pictograph.start_position == GridPosition.ALPHA1
        assert pictograph.end_position == GridPosition.ALPHA3

    def test_serialization_with_enums(self):
        """Test serialization/deserialization with enum types."""
        pictograph = PictographData(
            timing=Timing.TOG,
            direction=Direction.OPP,
            letter_type=LetterType.TYPE2,
            start_position=GridPosition.BETA1,
            end_position=GridPosition.BETA3,
        )

        # Test to_dict
        data = pictograph.to_dict()
        assert data["timing"] == "tog"
        assert data["direction"] == "opp"
        assert data["letter_type"] == "Type2"
        assert data["start_position"] == "beta1"
        assert data["end_position"] == "beta3"

        # Test from_dict
        restored = PictographData.from_dict(data)
        assert restored.timing == Timing.TOG
        assert restored.direction == Direction.OPP
        assert restored.letter_type == LetterType.TYPE2
        assert restored.start_position == GridPosition.BETA1
        assert restored.end_position == GridPosition.BETA3
