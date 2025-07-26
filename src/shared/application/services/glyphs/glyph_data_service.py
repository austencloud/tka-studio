"""
Glyph Data Service for Kinetic Constructor

This service determines glyph information (VTG mode, elemental type, letter type, etc.)
from pictograph data and motion information, following validated glyph classification logic.
"""

from typing import Optional

from desktop.modern.core.interfaces.data_builder_services import IGlyphDataService
from desktop.modern.domain.models import (
    BeatData,
    ElementalType,
    LetterType,
    Location,
    MotionData,
    PictographData,
    VTGMode,
)


class GlyphDataService(IGlyphDataService):
    """Service for determining glyph data from beat information."""

    # Complete mapping from letters to letter types
    LETTER_TYPE_MAP = {
        # TYPE1 letters (Dual-Shift: A-V)
        "A": LetterType.TYPE1,
        "B": LetterType.TYPE1,
        "C": LetterType.TYPE1,
        "D": LetterType.TYPE1,
        "E": LetterType.TYPE1,
        "F": LetterType.TYPE1,
        "G": LetterType.TYPE1,
        "H": LetterType.TYPE1,
        "I": LetterType.TYPE1,
        "J": LetterType.TYPE1,
        "K": LetterType.TYPE1,
        "L": LetterType.TYPE1,
        "M": LetterType.TYPE1,
        "N": LetterType.TYPE1,
        "O": LetterType.TYPE1,
        "P": LetterType.TYPE1,
        "Q": LetterType.TYPE1,
        "R": LetterType.TYPE1,
        "S": LetterType.TYPE1,
        "T": LetterType.TYPE1,
        "U": LetterType.TYPE1,
        "V": LetterType.TYPE1,
        # TYPE2 letters (Shift: W,X,Y,Z,Σ,Δ,θ,Ω)
        "W": LetterType.TYPE2,
        "X": LetterType.TYPE2,
        "Y": LetterType.TYPE2,
        "Z": LetterType.TYPE2,
        "Σ": LetterType.TYPE2,
        "Δ": LetterType.TYPE2,
        "θ": LetterType.TYPE2,
        "Ω": LetterType.TYPE2,
        # TYPE3 letters (Cross-Shift: W-,X-,Y-,Z-,Σ-,Δ-,θ-,Ω-)
        "W-": LetterType.TYPE3,
        "X-": LetterType.TYPE3,
        "Y-": LetterType.TYPE3,
        "Z-": LetterType.TYPE3,
        "Σ-": LetterType.TYPE3,
        "Δ-": LetterType.TYPE3,
        "θ-": LetterType.TYPE3,
        "Ω-": LetterType.TYPE3,
        # TYPE4 letters (Dash: Φ,Ψ,Λ)
        "Φ": LetterType.TYPE4,
        "Ψ": LetterType.TYPE4,
        "Λ": LetterType.TYPE4,
        # TYPE5 letters (Dual-Dash: Φ-,Ψ-,Λ-)
        "Φ-": LetterType.TYPE5,
        "Ψ-": LetterType.TYPE5,
        "Λ-": LetterType.TYPE5,
        # TYPE6 letters (Static: α,β,Γ)
        "α": LetterType.TYPE6,
        "β": LetterType.TYPE6,
        "Γ": LetterType.TYPE6,
    }

    def determine_glyph_data(self, pictograph_data: PictographData) -> None:
        """
        Determine glyph data from pictograph information.

        Note: This method no longer returns GlyphData as all glyph information
        is now computed directly from PictographData using utility functions.

        Args:
            pictograph_data: The pictograph data to analyze
        """
        # All glyph data is now computed from PictographData when needed:
        # - VTG mode: compute_vtg_mode(pictograph_data)
        # - Elemental type: compute_elemental_type_from_pictograph(pictograph_data)
        # - Has dash: has_dash_from_pictograph(pictograph_data)
        # - Turns: get_turns_from_motions(pictograph_data)
        # - Visibility: PictographVisibilityManager

    def determine_glyph_data_from_beat(self, beat_data: BeatData) -> None:
        """
        Backward compatibility method to determine glyph data from beat data.

        Note: This method no longer returns GlyphData as all glyph information
        is now computed directly from PictographData using utility functions.

        Args:
            beat_data: The beat data to analyze
        """
        # Convert BeatData to PictographData for processing
        pictograph_data = self._beat_data_to_pictograph_data(beat_data)
        self.determine_glyph_data(pictograph_data)

    def _beat_data_to_pictograph_data(self, beat_data: BeatData) -> PictographData:
        """Convert BeatData to PictographData for glyph processing."""
        from desktop.modern.domain.models.arrow_data import ArrowData, GridData

        # Create arrows from motion data
        arrows = {}
        if beat_data.blue_motion:
            arrows["blue"] = ArrowData(motion_data=beat_data.blue_motion, color="blue")
        if beat_data.red_motion:
            arrows["red"] = ArrowData(motion_data=beat_data.red_motion, color="red")

        return PictographData(
            grid_data=GridData(),  # Default grid data
            arrows=arrows,
            letter=beat_data.letter,
            start_position=beat_data.start_position,
            end_position=beat_data.end_position,
            is_blank=beat_data.is_blank,
        )

    def _determine_letter_type(self, letter: str) -> Optional[LetterType]:
        """Determine the letter type from the letter string."""
        # Use the full letter string (not just first character) for compound letters like "W-"
        return self.LETTER_TYPE_MAP.get(letter)

    def _determine_vtg_mode(self, pictograph_data: PictographData) -> Optional[VTGMode]:
        """
        Determine VTG mode from motion data.

        This is a simplified implementation. The full logic is quite complex
        and involves grid mode checking, position analysis, etc.
        """
        # Handle cases where arrows or motions are missing
        if not hasattr(pictograph_data, "arrows") or not pictograph_data.arrows:
            return None

        if not pictograph_data.arrows.get("blue") or not pictograph_data.arrows.get(
            "red"
        ):
            return None

        # Handle cases where motions are missing
        if not hasattr(pictograph_data, "motions") or not pictograph_data.motions:
            return None

        blue_motion = pictograph_data.motions.get("blue")
        red_motion = pictograph_data.motions.get("red")

        # If either motion is missing, return None
        if not blue_motion or not red_motion:
            return None

        # Simplified VTG determination based on motion patterns
        # This would need to be expanded with the full classification logic

        # Check if motions are in same or opposite directions
        is_same_direction = self._motions_same_direction(blue_motion, red_motion)

        # Check if motions are split, together, or quarter
        timing = self._determine_timing(blue_motion, red_motion)

        if timing == "split":
            return VTGMode.SPLIT_SAME if is_same_direction else VTGMode.SPLIT_OPP
        elif timing == "together":
            return VTGMode.TOG_SAME if is_same_direction else VTGMode.TOG_OPP
        elif timing == "quarter":
            return VTGMode.QUARTER_SAME if is_same_direction else VTGMode.QUARTER_OPP

        return VTGMode.SPLIT_SAME  # Default fallback

    def _motions_same_direction(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> bool:
        """Check if two motions are in the same direction."""
        # Simplified check - would need full directional logic
        return blue_motion.prop_rot_dir == red_motion.prop_rot_dir

    def _determine_timing(self, blue_motion: MotionData, red_motion: MotionData) -> str:
        """Determine if motions are split, together, or quarter pattern."""
        # Simplified pattern detection - would need full pattern analysis logic
        blue_start = blue_motion.start_loc
        red_start = red_motion.start_loc

        # Basic pattern detection based on starting locations
        opposite_locations = {
            Location.NORTH: Location.SOUTH,
            Location.SOUTH: Location.NORTH,
            Location.EAST: Location.WEST,
            Location.WEST: Location.EAST,
        }

        if red_start == opposite_locations.get(blue_start):
            return "split"
        elif blue_start == red_start:
            return "together"
        else:
            return "quarter"

    def _vtg_to_elemental(self, vtg_mode: Optional[VTGMode]) -> Optional[ElementalType]:
        """Convert VTG mode to elemental type."""
        if not vtg_mode:
            return None

        mapping = {
            VTGMode.SPLIT_SAME: ElementalType.WATER,
            VTGMode.SPLIT_OPP: ElementalType.FIRE,
            VTGMode.TOG_SAME: ElementalType.EARTH,
            VTGMode.TOG_OPP: ElementalType.AIR,
            VTGMode.QUARTER_SAME: ElementalType.SUN,
            VTGMode.QUARTER_OPP: ElementalType.MOON,
        }
        return mapping.get(vtg_mode)

    def _determine_positions(
        self, pictograph_data: PictographData
    ) -> tuple[Optional[str], Optional[str]]:
        """Determine start and end positions from pictograph data."""
        # First try to use the explicit start/end positions from pictograph data
        if pictograph_data.start_position and pictograph_data.end_position:
            return pictograph_data.start_position, pictograph_data.end_position

        # Fallback to deriving from motion data if available
        if (
            not hasattr(pictograph_data, "arrows")
            or not pictograph_data.arrows
            or not pictograph_data.arrows.get("blue")
        ):
            return None, None

        # For now, use blue motion's start and end locations
        # This would need more sophisticated logic in the full implementation
        if not hasattr(pictograph_data, "motions") or not pictograph_data.motions:
            return None, None

        blue_motion = pictograph_data.motions.get("blue")
        if not blue_motion:
            return None, None

        # Map locations to position names
        location_to_position = {
            Location.NORTH: "alpha",
            Location.EAST: "beta",
            Location.SOUTH: "gamma",
            Location.WEST: "alpha",  # Simplified mapping
        }

        start_pos = (
            location_to_position.get(blue_motion.start_loc)
            if hasattr(blue_motion, "start_loc")
            else None
        )
        end_pos = (
            location_to_position.get(blue_motion.end_loc)
            if hasattr(blue_motion, "end_loc")
            else None
        )

        return start_pos, end_pos
