"""
Utility functions for deriving data from PictographData.

This module provides functions to compute derived values that were previously
stored redundantly in GlyphData, such as VTG mode, elemental type, and dash status.
"""

from __future__ import annotations

from typing import Optional

from .enums import Direction, ElementalType, LetterType, Timing, VTGMode
from .pictograph_data import PictographData


def compute_vtg_mode(pictograph_data: PictographData) -> Optional[VTGMode]:
    """
    Compute VTG mode from timing and direction in PictographData.

    Args:
        pictograph_data: The pictograph data containing timing and direction

    Returns:
        VTGMode enum value or None if timing/direction not available
    """
    if not pictograph_data.timing or not pictograph_data.direction:
        return None

    timing = pictograph_data.timing
    direction = pictograph_data.direction

    # Map timing and direction combinations to VTG modes
    if timing == Timing.SPLIT:
        if direction == Direction.SAME:
            return VTGMode.SPLIT_SAME
        if direction == Direction.OPP:
            return VTGMode.SPLIT_OPP
    elif timing == Timing.TOG:
        if direction == Direction.SAME:
            return VTGMode.TOG_SAME
        if direction == Direction.OPP:
            return VTGMode.TOG_OPP

    # Default fallback
    return VTGMode.SPLIT_SAME


def compute_elemental_type(vtg_mode: Optional[VTGMode]) -> Optional[ElementalType]:
    """
    Compute elemental type from VTG mode.

    Args:
        vtg_mode: The VTG mode to translate

    Returns:
        ElementalType enum value or None if vtg_mode is None
    """
    if not vtg_mode:
        return None

    # Map VTG modes to elemental types
    vtg_to_elemental = {
        VTGMode.SPLIT_SAME: ElementalType.WATER,
        VTGMode.SPLIT_OPP: ElementalType.FIRE,
        VTGMode.TOG_SAME: ElementalType.EARTH,
        VTGMode.TOG_OPP: ElementalType.AIR,
        VTGMode.QUARTER_SAME: ElementalType.SUN,
        VTGMode.QUARTER_OPP: ElementalType.MOON,
    }

    return vtg_to_elemental.get(vtg_mode)


def compute_elemental_type_from_pictograph(
    pictograph_data: PictographData,
) -> Optional[ElementalType]:
    """
    Compute elemental type directly from PictographData.

    Args:
        pictograph_data: The pictograph data

    Returns:
        ElementalType enum value or None
    """
    vtg_mode = compute_vtg_mode(pictograph_data)
    return compute_elemental_type(vtg_mode)


def has_dash(letter_type: Optional[LetterType]) -> bool:
    """
    Determine if a letter has a dash based on its type.

    Letters of type 3 (Cross-Shift) and type 5 (Dual-Dash) have dashes.

    Args:
        letter_type: The letter type to check

    Returns:
        True if the letter type has a dash, False otherwise
    """
    if not letter_type:
        return False

    return letter_type in (LetterType.TYPE3, LetterType.TYPE5)


def has_dash_from_letter_string(letter: Optional[str]) -> bool:
    """
    Determine if a letter has a dash based on the letter string.

    Args:
        letter: The letter string to check

    Returns:
        True if the letter string contains a dash, False otherwise
    """
    if not letter:
        return False

    return "-" in letter


def has_dash_from_pictograph(pictograph_data: PictographData) -> bool:
    """
    Determine if a pictograph's letter has a dash.

    Checks both the letter_type (preferred) and letter string (fallback).

    Args:
        pictograph_data: The pictograph data

    Returns:
        True if the letter has a dash, False otherwise
    """
    # Prefer letter_type if available
    if pictograph_data.letter_type:
        return has_dash(pictograph_data.letter_type)

    # Fallback to letter string
    return has_dash_from_letter_string(pictograph_data.letter)


def get_turns_from_motions(pictograph_data: PictographData) -> Optional[str]:
    """
    Get turns data from motion data in PictographData.

    Args:
        pictograph_data: The pictograph data containing motions

    Returns:
        Turns data as string tuple or None if no motions
    """
    if not pictograph_data.motions:
        return None

    turns_list = []

    # Get turns from blue motion
    if "blue" in pictograph_data.motions:
        blue_turns = pictograph_data.motions["blue"].turns
        turns_list.append(str(blue_turns))

    # Get turns from red motion
    if "red" in pictograph_data.motions:
        red_turns = pictograph_data.motions["red"].turns
        turns_list.append(str(red_turns))

    if turns_list:
        return f"({', '.join(turns_list)})"

    return None


def should_show_elemental(letter_type: Optional[LetterType]) -> bool:
    """
    Determine if elemental glyph should be shown based on letter type.

    Args:
        letter_type: The letter type

    Returns:
        True if elemental glyph should be shown
    """
    return letter_type == LetterType.TYPE1 if letter_type else False


def should_show_vtg(letter_type: Optional[LetterType]) -> bool:
    """
    Determine if VTG glyph should be shown based on letter type.

    Args:
        letter_type: The letter type

    Returns:
        True if VTG glyph should be shown
    """
    return letter_type == LetterType.TYPE1 if letter_type else False


def should_show_positions(letter_type: Optional[LetterType]) -> bool:
    """
    Determine if position glyphs should be shown based on letter type.

    Args:
        letter_type: The letter type

    Returns:
        True if position glyphs should be shown
    """
    # Don't show positions for Type6 (Static: α, β, Γ)
    return letter_type != LetterType.TYPE6 if letter_type else True


def should_show_tka(letter_type: Optional[LetterType]) -> bool:
    """
    Determine if TKA glyph should be shown based on letter type.

    Args:
        letter_type: The letter type

    Returns:
        True if TKA glyph should be shown (always True for now)
    """
    return True
