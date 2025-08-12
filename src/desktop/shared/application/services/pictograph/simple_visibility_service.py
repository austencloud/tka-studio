"""
Simple Visibility Service for TKA Pictographs.

Replaces the complex VisibilityStateManager and PictographVisibilityManager
with a straightforward service that just tracks visibility state.

No observers, no threading, no weak references, no global registration.
Just simple state management.
"""

import logging

logger = logging.getLogger(__name__)


class PictographVisibilityService:
    """
    Simple visibility state management for pictograph elements.

    Tracks visibility for:
    - Glyphs: TKA, VTG, Elemental, Positions, Reversals
    - Motions: red, blue
    - Other: non_radial, grid, props, arrows
    """

    def __init__(self, base_visibility_service=None):
        """
        Initialize with default visibility states.

        Args:
            base_visibility_service: Optional underlying service that stores persistent settings
        """
        self._base_service = base_visibility_service

        # Default visibility states
        self._glyph_visibility = {
            "TKA": True,
            "VTG": True,
            "Elemental": True,
            "Positions": True,
            "Reversals": True,
        }

        self._motion_visibility = {
            "red": True,
            "blue": True,
        }

        self._other_visibility = {
            "non_radial": True,
            "grid": True,
            "props": True,
            "arrows": True,
        }

        # Glyphs that depend on both motions being visible
        self._dependent_glyphs = {"TKA", "VTG", "Elemental", "Positions"}

        # Initialize from base service if available
        if self._base_service:
            self._sync_from_base_service()

    def _sync_from_base_service(self) -> None:
        """Sync current state from the base visibility service."""
        if not self._base_service:
            return

        try:
            # Sync glyph visibility
            for glyph in self._glyph_visibility:
                if hasattr(self._base_service, "get_glyph_visibility"):
                    self._glyph_visibility[glyph] = (
                        self._base_service.get_glyph_visibility(glyph)
                    )

            # Sync motion visibility
            for color in self._motion_visibility:
                if hasattr(self._base_service, "get_motion_visibility"):
                    self._motion_visibility[color] = (
                        self._base_service.get_motion_visibility(color)
                    )

        except Exception as e:
            logger.warning(f"Failed to sync from base service: {e}")

    def get_glyph_visibility(
        self, glyph_type: str, check_dependencies: bool = True
    ) -> bool:
        """
        Get visibility for a glyph type.

        Args:
            glyph_type: The glyph type (TKA, VTG, etc.)
            check_dependencies: Whether to check motion dependencies

        Returns:
            True if glyph should be visible
        """
        if glyph_type not in self._glyph_visibility:
            logger.warning(f"Unknown glyph type: {glyph_type}")
            return False

        base_visible = self._glyph_visibility[glyph_type]

        # For dependent glyphs, check if both motions are visible
        if check_dependencies and glyph_type in self._dependent_glyphs:
            return base_visible and self.are_all_motions_visible()

        return base_visible

    def set_glyph_visibility(self, glyph_type: str, visible: bool) -> None:
        """
        Set visibility for a glyph type.

        Args:
            glyph_type: The glyph type
            visible: Whether it should be visible
        """
        if glyph_type not in self._glyph_visibility:
            logger.warning(f"Unknown glyph type: {glyph_type}")
            return

        self._glyph_visibility[glyph_type] = visible

        # Update base service if available
        if self._base_service and hasattr(self._base_service, "set_glyph_visibility"):
            try:
                self._base_service.set_glyph_visibility(glyph_type, visible)
            except Exception as e:
                logger.warning(f"Failed to update base service: {e}")

    def get_motion_visibility(self, color: str) -> bool:
        """
        Get visibility for a motion color.

        Args:
            color: red or blue

        Returns:
            True if motion should be visible
        """
        if color not in self._motion_visibility:
            logger.warning(f"Unknown motion color: {color}")
            return False

        return self._motion_visibility[color]

    def set_motion_visibility(self, color: str, visible: bool) -> None:
        """
        Set visibility for a motion color.
        Ensures at least one motion remains visible.

        Args:
            color: red or blue
            visible: Whether it should be visible
        """
        if color not in self._motion_visibility:
            logger.warning(f"Unknown motion color: {color}")
            return

        other_color = "blue" if color == "red" else "red"

        # Prevent turning off both colors
        if not visible and not self._motion_visibility[other_color]:
            logger.info(
                f"Cannot disable {color} motion - would leave no motions visible"
            )
            # Force enable the other motion
            self._motion_visibility[other_color] = True
            if self._base_service and hasattr(
                self._base_service, "set_motion_visibility"
            ):
                try:
                    self._base_service.set_motion_visibility(other_color, True)
                except Exception as e:
                    logger.warning(f"Failed to update base service: {e}")

        self._motion_visibility[color] = visible

        # Update base service if available
        if self._base_service and hasattr(self._base_service, "set_motion_visibility"):
            try:
                self._base_service.set_motion_visibility(color, visible)
            except Exception as e:
                logger.warning(f"Failed to update base service: {e}")

    def are_all_motions_visible(self) -> bool:
        """Check if both motion types are visible."""
        return all(self._motion_visibility.values())

    def get_element_visibility(self, element_type: str, element_name: str) -> bool:
        """
        Get visibility for any element using the update_visibility interface.

        Args:
            element_type: Type of element (glyph, motion, other)
            element_name: Name of element

        Returns:
            True if element should be visible
        """
        if element_type == "glyph":
            return self.get_glyph_visibility(element_name)
        elif element_type == "motion":
            # Convert motion names like "red_motion" to "red"
            color = element_name.replace("_motion", "")
            return self.get_motion_visibility(color)
        else:
            # Handle other elements like grid, props, arrows
            return self._other_visibility.get(element_name, True)

    def set_element_visibility(
        self, element_type: str, element_name: str, visible: bool
    ) -> None:
        """
        Set visibility for any element using the update_visibility interface.

        Args:
            element_type: Type of element (glyph, motion, other)
            element_name: Name of element
            visible: Whether it should be visible
        """
        if element_type == "glyph":
            self.set_glyph_visibility(element_name, visible)
        elif element_type == "motion":
            # Convert motion names like "red_motion" to "red"
            color = element_name.replace("_motion", "")
            self.set_motion_visibility(color, visible)
        else:
            # Handle other elements
            if element_name in self._other_visibility:
                self._other_visibility[element_name] = visible

    def get_all_visibility_states(self) -> dict[str, dict[str, bool]]:
        """Get all current visibility states."""
        return {
            "glyphs": dict(self._glyph_visibility),
            "motions": dict(self._motion_visibility),
            "other": dict(self._other_visibility),
        }

    def reset_to_defaults(self) -> None:
        """Reset all visibility to default states."""
        for key in self._glyph_visibility:
            self._glyph_visibility[key] = True
        for key in self._motion_visibility:
            self._motion_visibility[key] = True
        for key in self._other_visibility:
            self._other_visibility[key] = True


# Global instance for backward compatibility
_global_visibility_service: PictographVisibilityService | None = None


def get_visibility_service() -> PictographVisibilityService:
    """Get the global visibility service instance."""
    global _global_visibility_service
    if _global_visibility_service is None:
        # Try to get base service from DI container
        base_service = None
        try:
            from desktop.modern.core.dependency_injection.di_container import (
                get_container,
            )
            from desktop.modern.core.interfaces.tab_settings_interfaces import (
                IVisibilitySettingsManager,
            )

            container = get_container()
            if container:
                base_service = container.resolve(IVisibilitySettingsManager)
        except Exception:
            pass  # Use without base service

        _global_visibility_service = PictographVisibilityService(base_service)

    return _global_visibility_service
