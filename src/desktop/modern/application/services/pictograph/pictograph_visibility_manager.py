"""
PictographVisibilityManager for managing glyph visibility flags.

This manager handles visibility state for different glyph types that were
previously stored in GlyphData. It provides a centralized way to manage
visibility settings for elemental, VTG, TKA, and position glyphs.
"""

from dataclasses import dataclass

from desktop.modern.domain.models.enums import LetterType
from desktop.modern.domain.models.pictograph_utils import (
    should_show_elemental,
    should_show_positions,
    should_show_tka,
    should_show_vtg,
)


@dataclass
class PictographVisibilityState:
    """
    Visibility state for a single pictograph's glyphs.
    """

    show_elemental: bool = True
    show_vtg: bool = True
    show_tka: bool = True
    show_positions: bool = True

    def to_dict(self) -> dict[str, bool]:
        """Convert to dictionary for serialization."""
        return {
            "show_elemental": self.show_elemental,
            "show_vtg": self.show_vtg,
            "show_tka": self.show_tka,
            "show_positions": self.show_positions,
        }

    @classmethod
    def from_dict(cls, data: dict[str, bool]) -> "PictographVisibilityState":
        """Create from dictionary."""
        return cls(
            show_elemental=data.get("show_elemental", True),
            show_vtg=data.get("show_vtg", True),
            show_tka=data.get("show_tka", True),
            show_positions=data.get("show_positions", True),
        )

    @classmethod
    def from_letter_type(
        cls, letter_type: LetterType | None
    ) -> "PictographVisibilityState":
        """
        Create visibility state based on letter type defaults.

        Args:
            letter_type: The letter type to determine default visibility

        Returns:
            PictographVisibilityState with appropriate defaults
        """
        return cls(
            show_elemental=should_show_elemental(letter_type),
            show_vtg=should_show_vtg(letter_type),
            show_tka=should_show_tka(letter_type),
            show_positions=should_show_positions(letter_type),
        )


class PictographVisibilityManager:
    """
    Manager for pictograph glyph visibility settings.

    This class replaces the visibility flags that were previously stored
    in GlyphData, providing a centralized way to manage visibility state
    for different glyph types across pictographs.
    """

    def __init__(self):
        """Initialize the visibility manager."""
        # Per-pictograph visibility state
        self._pictograph_visibility: dict[str, PictographVisibilityState] = {}

        # Global visibility overrides (from settings)
        self._global_visibility: dict[str, bool] = {
            "elemental": True,
            "vtg": True,
            "tka": True,
            "positions": True,
        }

    def get_visibility_state(self, pictograph_id: str) -> PictographVisibilityState:
        """
        Get visibility state for a pictograph.

        Args:
            pictograph_id: The pictograph ID

        Returns:
            PictographVisibilityState for the pictograph
        """
        return self._pictograph_visibility.get(
            pictograph_id, PictographVisibilityState()
        )

    def set_visibility_state(
        self, pictograph_id: str, visibility_state: PictographVisibilityState
    ) -> None:
        """
        Set visibility state for a pictograph.

        Args:
            pictograph_id: The pictograph ID
            visibility_state: The visibility state to set
        """
        self._pictograph_visibility[pictograph_id] = visibility_state

    def set_pictograph_visibility(
        self, pictograph_id: str, glyph_type: str, visible: bool
    ) -> None:
        """
        Set visibility for a specific glyph type on a pictograph.

        Args:
            pictograph_id: The pictograph ID
            glyph_type: The glyph type ("elemental", "vtg", "tka", "positions")
            visible: Whether the glyph should be visible
        """
        state = self.get_visibility_state(pictograph_id)

        if glyph_type == "elemental":
            state.show_elemental = visible
        elif glyph_type == "vtg":
            state.show_vtg = visible
        elif glyph_type == "tka":
            state.show_tka = visible
        elif glyph_type == "positions":
            state.show_positions = visible
        else:
            raise ValueError(f"Unknown glyph type: {glyph_type}")

        self._pictograph_visibility[pictograph_id] = state

    def get_pictograph_visibility(self, pictograph_id: str, glyph_type: str) -> bool:
        """
        Get visibility for a specific glyph type on a pictograph.

        Args:
            pictograph_id: The pictograph ID
            glyph_type: The glyph type ("elemental", "vtg", "tka", "positions")

        Returns:
            True if the glyph should be visible
        """
        state = self.get_visibility_state(pictograph_id)
        global_visible = self._global_visibility.get(glyph_type, True)

        if glyph_type == "elemental":
            return state.show_elemental and global_visible
        elif glyph_type == "vtg":
            return state.show_vtg and global_visible
        elif glyph_type == "tka":
            return state.show_tka and global_visible
        elif glyph_type == "positions":
            return state.show_positions and global_visible
        else:
            raise ValueError(f"Unknown glyph type: {glyph_type}")

    def set_global_visibility(self, glyph_type: str, visible: bool) -> None:
        """
        Set global visibility override for a glyph type.

        Args:
            glyph_type: The glyph type ("elemental", "vtg", "tka", "positions")
            visible: Whether the glyph type should be globally visible
        """
        if glyph_type not in self._global_visibility:
            raise ValueError(f"Unknown glyph type: {glyph_type}")

        self._global_visibility[glyph_type] = visible

    def get_global_visibility(self, glyph_type: str) -> bool:
        """
        Get global visibility override for a glyph type.

        Args:
            glyph_type: The glyph type ("elemental", "vtg", "tka", "positions")

        Returns:
            True if the glyph type is globally visible
        """
        return self._global_visibility.get(glyph_type, True)

    def initialize_pictograph_visibility(
        self, pictograph_id: str, letter_type: LetterType | None
    ) -> None:
        """
        Initialize visibility state for a pictograph based on its letter type.

        Args:
            pictograph_id: The pictograph ID
            letter_type: The letter type to determine default visibility
        """
        visibility_state = PictographVisibilityState.from_letter_type(letter_type)
        self.set_visibility_state(pictograph_id, visibility_state)

    def remove_pictograph_visibility(self, pictograph_id: str) -> None:
        """
        Remove visibility state for a pictograph.

        Args:
            pictograph_id: The pictograph ID to remove
        """
        self._pictograph_visibility.pop(pictograph_id, None)

    def clear_all_visibility(self) -> None:
        """Clear all pictograph visibility states."""
        self._pictograph_visibility.clear()

    def get_all_visibility_states(self) -> dict[str, PictographVisibilityState]:
        """
        Get all pictograph visibility states.

        Returns:
            Dictionary mapping pictograph IDs to visibility states
        """
        return self._pictograph_visibility.copy()


# Global instance for application-wide use
_visibility_manager: PictographVisibilityManager | None = None


def get_pictograph_visibility_manager() -> PictographVisibilityManager:
    """
    Get the global pictograph visibility manager instance.

    Returns:
        The global PictographVisibilityManager instance
    """
    global _visibility_manager
    if _visibility_manager is None:
        _visibility_manager = PictographVisibilityManager()
    return _visibility_manager
