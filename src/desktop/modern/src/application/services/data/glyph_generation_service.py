"""
Glyph Generation Service

Pure service for generating glyph data from beat data.
Extracted from PictographManagementService to follow single responsibility principle.

PROVIDES:
- Glyph data generation from beat data
- Letter type classification
- VTG mode determination
- Elemental type mapping
- Position determination
"""

from typing import Optional, Tuple, Dict
from abc import ABC, abstractmethod

from domain.models.core_models import (
    BeatData,
    MotionData,
    GlyphData,
    VTGMode,
    ElementalType,
    LetterType,
    Location,
)


class IGlyphGenerationService(ABC):
    """Interface for glyph generation operations."""

    @abstractmethod
    def generate_glyph_data(self, beat_data: BeatData) -> Optional[GlyphData]:
        """Generate glyph data for beat data."""

    @abstractmethod
    def determine_letter_type(self, letter: str) -> Optional[LetterType]:
        """Determine letter type from letter string."""

    @abstractmethod
    def generate_glyph_key(self, beat_data: BeatData) -> str:
        """Generate glyph key for beat data."""


class GlyphGenerationService(IGlyphGenerationService):
    """
    Pure service for glyph generation operations.

    Handles all glyph-related calculations without external dependencies.
    Uses immutable data patterns following TKA architecture.
    """

    def __init__(self):
        """Initialize glyph generation service."""
        self._letter_type_map = self._build_letter_type_map()
        self._glyph_mappings = self._build_glyph_mappings()

    def generate_glyph_data(self, beat_data: BeatData) -> Optional[GlyphData]:
        """Generate glyph data for beat data."""
        if beat_data.is_blank or not beat_data.letter:
            return None

        # Determine letter type
        letter_type = self.determine_letter_type(beat_data.letter)

        # Determine VTG mode
        vtg_mode = self._determine_vtg_mode(beat_data)

        # Determine if letter has dash
        has_dash = "-" in beat_data.letter if beat_data.letter else False

        # Determine start and end positions
        start_position, end_position = self._determine_positions(beat_data)

        return GlyphData(
            vtg_mode=vtg_mode,
            elemental_type=self._vtg_to_elemental(vtg_mode),
            letter_type=letter_type,
            has_dash=has_dash,
            turns_data=None,  # TODO: Implement turns data parsing
            start_position=start_position,
            end_position=end_position,
            show_elemental=letter_type == LetterType.TYPE1 if letter_type else False,
            show_vtg=letter_type == LetterType.TYPE1 if letter_type else False,
            show_tka=True,
            show_positions=letter_type != LetterType.TYPE6 if letter_type else True,
        )

    def determine_letter_type(self, letter: str) -> Optional[LetterType]:
        """Determine the letter type from the letter string."""
        return self._letter_type_map.get(letter)

    def generate_glyph_key(self, beat_data: BeatData) -> str:
        """Generate glyph key for beat data."""
        key_parts = []

        if beat_data.blue_motion:
            key_parts.append(f"blue_{beat_data.blue_motion.motion_type.value}")

        if beat_data.red_motion:
            key_parts.append(f"red_{beat_data.red_motion.motion_type.value}")

        return "_".join(key_parts) if key_parts else "blank"

    def get_glyph_symbol(self, glyph_key: str) -> Optional[str]:
        """Get glyph symbol for glyph key."""
        return self._glyph_mappings.get(glyph_key)

    def _determine_vtg_mode(self, beat_data: BeatData) -> Optional[VTGMode]:
        """Determine VTG mode from beat data."""
        blue_motion = beat_data.blue_motion
        red_motion = beat_data.red_motion

        if not blue_motion or not red_motion:
            return None

        # Simplified VTG determination
        same_direction = self._motions_same_direction(blue_motion, red_motion)
        motion_pattern = self._determine_motion_pattern(blue_motion, red_motion)

        if motion_pattern == "split":
            return VTGMode.SPLIT_SAME if same_direction else VTGMode.SPLIT_OPP
        elif motion_pattern == "together":
            return VTGMode.TOG_SAME if same_direction else VTGMode.TOG_OPP
        elif motion_pattern == "quarter":
            return VTGMode.QUARTER_SAME if same_direction else VTGMode.QUARTER_OPP

        return VTGMode.SPLIT_SAME  # Default

    def _motions_same_direction(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> bool:
        """Check if motions are in same direction."""
        return blue_motion.prop_rot_dir == red_motion.prop_rot_dir

    def _determine_motion_pattern(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> str:
        """Determine motion pattern (split, together, quarter)."""
        blue_start = blue_motion.start_loc
        red_start = red_motion.start_loc

        # Check if starting positions are opposite
        opposite_pairs = [
            (Location.NORTH, Location.SOUTH),
            (Location.EAST, Location.WEST),
            (Location.NORTHEAST, Location.SOUTHWEST),
            (Location.NORTHWEST, Location.SOUTHEAST),
        ]

        for pair in opposite_pairs:
            if (blue_start, red_start) in [pair, pair[::-1]]:
                return "split"

        # Check if starting positions are adjacent
        if blue_start == red_start:
            return "together"

        return "quarter"  # Default

    def _determine_positions(
        self, beat_data: BeatData
    ) -> Tuple[Optional[str], Optional[str]]:
        """Determine start and end positions from beat data."""
        # Extract from metadata if available
        start_pos = beat_data.metadata.get("start_pos")
        end_pos = beat_data.metadata.get("end_pos")

        if start_pos and end_pos:
            return start_pos, end_pos

        # Generate from motion data if available
        if beat_data.blue_motion and beat_data.red_motion:
            start_pos = f"{beat_data.blue_motion.start_loc.value}_{beat_data.red_motion.start_loc.value}"
            end_pos = f"{beat_data.blue_motion.end_loc.value}_{beat_data.red_motion.end_loc.value}"
            return start_pos, end_pos

        return None, None

    def _vtg_to_elemental(self, vtg_mode: Optional[VTGMode]) -> Optional[ElementalType]:
        """Convert VTG mode to elemental type."""
        if not vtg_mode:
            return None

        vtg_to_elemental_map = {
            VTGMode.SPLIT_SAME: ElementalType.FIRE,
            VTGMode.SPLIT_OPP: ElementalType.WATER,
            VTGMode.TOG_SAME: ElementalType.AIR,
            VTGMode.TOG_OPP: ElementalType.EARTH,
            VTGMode.QUARTER_SAME: ElementalType.FIRE,
            VTGMode.QUARTER_OPP: ElementalType.WATER,
        }

        return vtg_to_elemental_map.get(vtg_mode)

    def _build_letter_type_map(self) -> Dict[str, LetterType]:
        """Build letter type mapping."""
        return {
            # Type 1 letters (show elemental and VTG glyphs)
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
            # Type 2 letters (no elemental/VTG glyphs)
            "W": LetterType.TYPE2,
            "X": LetterType.TYPE2,
            "Y": LetterType.TYPE2,
            "Z": LetterType.TYPE2,
            "Σ": LetterType.TYPE2,
            "Δ": LetterType.TYPE2,
            "θ": LetterType.TYPE2,
            "Ω": LetterType.TYPE2,
            # Type 3 letters (no elemental/VTG glyphs)
            "W-": LetterType.TYPE3,
            "X-": LetterType.TYPE3,
            "Y-": LetterType.TYPE3,
            "Z-": LetterType.TYPE3,
            "Σ-": LetterType.TYPE3,
            "Δ-": LetterType.TYPE3,
            "θ-": LetterType.TYPE3,
            "Ω-": LetterType.TYPE3,
            # Type 4 letters (no elemental/VTG glyphs)
            "Φ": LetterType.TYPE4,
            "Ψ": LetterType.TYPE4,
            "Λ": LetterType.TYPE4,
            # Type 5 letters (no elemental/VTG glyphs)
            "Φ-": LetterType.TYPE5,
            "Ψ-": LetterType.TYPE5,
            "Λ-": LetterType.TYPE5,
            # Type 6 letters (don't show positions)
            "α": LetterType.TYPE6,
            "β": LetterType.TYPE6,
            "Γ": LetterType.TYPE6,
        }

    def _build_glyph_mappings(self) -> Dict[str, str]:
        """Build glyph symbol mappings."""
        return {
            "blue_pro_red_anti": "⚡",
            "blue_static_red_static": "⬜",
            "blue_dash_red_dash": "⚊",
            "blank": "○",
        }
