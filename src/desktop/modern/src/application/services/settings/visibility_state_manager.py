"""
Modern Visibility State Manager for TKA.

Provides sophisticated state management with observer pattern, dependency logic,
validation, and integration with existing IVisibilityService.
"""

from typing import Dict, List, Callable, Any
import logging
from threading import Lock

from core.interfaces.tab_settings_interfaces import IVisibilityService

logger = logging.getLogger(__name__)


class ModernVisibilityStateManager:
    """
    Central manager for all visibility states with observer pattern and dependency logic.

    Provides sophisticated state management that matches legacy functionality while
    using modern architecture patterns.
    """

    def __init__(self, visibility_service: IVisibilityService):
        self.visibility_service = visibility_service
        self._lock = Lock()  # Thread-safe operations

        # Get or create global visibility service for cross-application updates
        self._global_service = self._get_global_service()

        # Observer pattern for UI updates
        self._observers: Dict[str, List[Callable]] = {
            "glyph": [],
            "motion": [],
            "non_radial": [],
            "all": [],
            "buttons": [],  # For button state updates
        }

        # Define dependent glyphs that require both motions to be visible
        self.dependent_glyphs = ["TKA", "VTG", "Elemental", "Positions"]

        # Define all glyph types for validation
        self.all_glyph_types = ["TKA", "Reversals", "VTG", "Elemental", "Positions"]

        # Motion colors
        self.motion_colors = ["red", "blue"]

    def _get_global_service(self):
        """Get or create global visibility service."""
        try:
            # Try to get from DI container first
            from application.services.pictograph.global_visibility_service import (
                GlobalVisibilityService,
            )
            from application.services.pictograph.global_visibility_service_singleton import (
                get_global_visibility_service,
            )

            try:
                from core.application.application_factory import get_container

                container = get_container()
                if container:
                    return container.resolve(GlobalVisibilityService)
            except Exception:
                pass

            # Fallback to singleton pattern
            return get_global_visibility_service()

        except Exception as e:
            logger.warning(f"Could not get GlobalVisibilityService: {e}")
            return None

    def register_observer(
        self, callback: Callable, categories: List[str] = None
    ) -> None:
        """Register a component to be notified when specific visibility states change."""
        if categories is None:
            categories = ["all"]

        with self._lock:
            for category in categories:
                if category in self._observers:
                    self._observers[category].append(callback)
                    logger.debug(f"Registered observer for category: {category}")

    def unregister_observer(
        self, callback: Callable, categories: List[str] = None
    ) -> None:
        """Unregister an observer from specific categories."""
        if categories is None:
            categories = ["all"]

        with self._lock:
            for category in categories:
                if (
                    category in self._observers
                    and callback in self._observers[category]
                ):
                    self._observers[category].remove(callback)
                    logger.debug(f"Unregistered observer from category: {category}")

    def _notify_observers(self, categories: List[str]) -> None:
        """Notify all observers in the specified categories."""
        with self._lock:
            notified_callbacks = set()

            for category in categories:
                if category in self._observers:
                    for callback in self._observers[category]:
                        if callback not in notified_callbacks:
                            try:
                                callback()
                                notified_callbacks.add(callback)
                            except Exception as e:
                                logger.error(f"Error notifying observer: {e}")

    def get_glyph_visibility(
        self, glyph_type: str, check_dependencies: bool = True
    ) -> bool:
        """
        Get the visibility of a glyph, considering dependencies.

        Args:
            glyph_type: The type of glyph (TKA, VTG, etc.)
            check_dependencies: Whether to check motion dependencies

        Returns:
            True if glyph should be visible, False otherwise
        """
        # Get base visibility from service
        base_visibility = self.visibility_service.get_glyph_visibility(glyph_type)

        # For dependent glyphs, check if both motions are visible
        if check_dependencies and glyph_type in self.dependent_glyphs:
            return base_visibility and self.are_all_motions_visible()

        # For non-dependent glyphs, return direct visibility
        return base_visibility

    def set_glyph_visibility(self, glyph_type: str, visible: bool) -> None:
        """Set the visibility of a glyph and notify observers."""
        if glyph_type not in self.all_glyph_types:
            logger.warning(f"Unknown glyph type: {glyph_type}")
            return

        self.visibility_service.set_glyph_visibility(glyph_type, visible)

        # Propagate to all registered pictographs via global service
        if self._global_service:
            self._global_service.apply_visibility_change("glyph", glyph_type, visible)

        self._notify_observers(["glyph", "all"])
        logger.debug(f"Set {glyph_type} visibility to {visible}")

    def get_motion_visibility(self, color: str) -> bool:
        """Get visibility for a specific motion color."""
        if color not in self.motion_colors:
            logger.warning(f"Unknown motion color: {color}")
            return False

        return self.visibility_service.get_motion_visibility(color)

    def set_motion_visibility(self, color: str, visible: bool) -> None:
        """
        Set visibility for a specific motion color with validation.
        Ensures at least one motion remains visible at all times.
        """
        if color not in self.motion_colors:
            logger.warning(f"Unknown motion color: {color}")
            return

        other_color = "blue" if color == "red" else "red"

        # Prevent turning off both colors
        if not visible and not self.get_motion_visibility(other_color):
            logger.info(
                f"Cannot disable {color} motion - would leave no motions visible"
            )
            # Force enable the other motion to maintain at least one visible
            self.visibility_service.set_motion_visibility(other_color, True)
            self.visibility_service.set_motion_visibility(color, False)

            # Propagate both changes to all registered pictographs via global service
            if self._global_service:
                self._global_service.apply_visibility_change(
                    "motion", f"{other_color}_motion", True
                )
                self._global_service.apply_visibility_change(
                    "motion", f"{color}_motion", False
                )

            self._notify_observers(["motion", "glyph", "buttons", "all"])
            return

        # Normal case - set the requested visibility
        self.visibility_service.set_motion_visibility(color, visible)

        # Propagate to all registered pictographs via global service
        if self._global_service:
            self._global_service.apply_visibility_change(
                "motion", f"{color}_motion", visible
            )

        self._notify_observers(["motion", "glyph", "buttons", "all"])
        logger.debug(f"Set {color} motion visibility to {visible}")

    def are_all_motions_visible(self) -> bool:
        """Check if both motion types are currently visible."""
        return all(self.get_motion_visibility(color) for color in self.motion_colors)

    def get_non_radial_visibility(self) -> bool:
        """Get visibility state for non-radial points."""
        return self.visibility_service.get_non_radial_visibility()

    def set_non_radial_visibility(self, visible: bool) -> None:
        """Set visibility state for non-radial points."""
        self.visibility_service.set_non_radial_visibility(visible)

        # Propagate to all registered pictographs via global service
        if self._global_service:
            self._global_service.apply_visibility_change(
                "glyph", "Non-radial_points", visible
            )

        self._notify_observers(["non_radial", "all"])
        logger.debug(f"Set non-radial visibility to {visible}")

    def get_all_visibility_states(self) -> Dict[str, Any]:
        """Get comprehensive visibility state information."""
        return {
            "glyphs": {
                glyph_type: {
                    "base_visible": self.visibility_service.get_glyph_visibility(
                        glyph_type
                    ),
                    "effective_visible": self.get_glyph_visibility(glyph_type),
                    "is_dependent": glyph_type in self.dependent_glyphs,
                }
                for glyph_type in self.all_glyph_types
            },
            "motions": {
                color: self.get_motion_visibility(color) for color in self.motion_colors
            },
            "non_radial": self.get_non_radial_visibility(),
            "all_motions_visible": self.are_all_motions_visible(),
        }

    def validate_state(self) -> Dict[str, Any]:
        """Validate current visibility state and return validation results."""
        issues = []
        warnings = []

        # Check if at least one motion is visible
        if not any(self.get_motion_visibility(color) for color in self.motion_colors):
            issues.append("No motions are visible - this should not be possible")

        # Check dependent glyph consistency
        all_motions_visible = self.are_all_motions_visible()
        for glyph_type in self.dependent_glyphs:
            base_visible = self.visibility_service.get_glyph_visibility(glyph_type)
            effective_visible = self.get_glyph_visibility(glyph_type)

            if base_visible and not effective_visible and not all_motions_visible:
                warnings.append(
                    f"{glyph_type} is enabled but hidden due to motion dependencies"
                )

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "state_summary": self.get_all_visibility_states(),
        }

    def apply_to_all_pictographs(self) -> None:
        """
        Trigger global application of visibility changes to all pictographs.
        This will be implemented by the GlobalVisibilityService.
        """
        # This method serves as a hook for the global visibility service
        # The actual implementation will be in GlobalVisibilityService
        self._notify_observers(["all"])
        logger.debug("Triggered global pictograph visibility update")
