"""
Modern Visibility State Manager for TKA.

Provides sophisticated state management with observer pattern, dependency logic,
validation, and integration with existing IVisibilityService.
"""

import logging
from threading import Lock
from typing import Any, Callable, Dict, List, Optional

from core.interfaces.tab_settings_interfaces import IVisibilitySettingsManager

logger = logging.getLogger(__name__)


class VisibilityStateManager:
    """
    Central manager for all visibility states with observer pattern and dependency logic.

    Provides sophisticated state management that matches legacy functionality while
    using modern architecture patterns.
    """

    def __init__(
        self,
        visibility_service: IVisibilitySettingsManager,
        global_visibility_service=None,
    ):
        self.visibility_service = visibility_service
        self._lock = Lock()  # Thread-safe operations

        # Use injected global service or create one
        self._global_service = global_visibility_service or self._get_global_service()

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

    def validate_dependencies(self) -> bool:
        """Validate that all required dependencies are available."""
        return self._validate_required_dependency(
            self.visibility_service, "visibility_service"
        )

    def _get_global_service(self):
        """Get or create global visibility service."""
        try:
            # Try to get from DI container first
            from application.services.pictograph.global_visibility_service import (
                PictographVisibilityManager,
            )

            try:
                from core.dependency_injection.di_container import get_container

                container = get_container()
                if container:
                    return container.resolve(PictographVisibilityManager)
            except Exception:
                pass

            # Fallback to creating new instance
            return PictographVisibilityManager()

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
