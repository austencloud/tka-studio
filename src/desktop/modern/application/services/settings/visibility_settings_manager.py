"""
Visibility Settings Manager Implementation

Implements visibility settings management for glyphs, motion arrows,
and other UI elements with QSettings persistence.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import QObject, QSettings, pyqtSignal


logger = logging.getLogger(__name__)


class VisibilitySettingsManager(QObject):
    """
    Implementation of visibility settings management using QSettings.

    Features:
    - Manages glyph visibility (letters, elementals, vtg, tka, position)
    - Controls motion arrow visibility (red/blue)
    - Handles grid and non-radial point visibility
    - Emits events when visibility changes
    - Provides batch operations for performance
    """

    visibility_changed = pyqtSignal(str, bool)  # element_name, visible

    # Default visibility settings
    DEFAULT_VISIBILITY = {
        # Glyph types
        "letter": True,
        "elemental": True,
        "vtg": False,
        "tka": False,
        "position": True,
        # Motion arrows
        "red_motion": True,
        "blue_motion": True,
        # Grid and special elements
        "grid": True,
        "non_radial": True,
    }

    def __init__(self, settings: QSettings):
        super().__init__()
        self.settings = settings
        logger.debug("Initialized VisibilitySettingsManager")

    def get_glyph_visibility(self, glyph_name: str) -> bool:
        """
        Get visibility state for a specific glyph type.

        Args:
            glyph_name: Name of the glyph type

        Returns:
            True if visible, False if hidden
        """
        try:
            default = self.DEFAULT_VISIBILITY.get(glyph_name, True)
            return self.settings.value(
                f"visibility/glyph_{glyph_name}", default, type=bool
            )
        except Exception as e:
            logger.error(f"Failed to get glyph visibility for {glyph_name}: {e}")
            return self.DEFAULT_VISIBILITY.get(glyph_name, True)

    def set_glyph_visibility(self, glyph_name: str, visible: bool) -> None:
        """
        Set visibility state for a specific glyph type.

        Args:
            glyph_name: Name of the glyph type
            visible: Visibility state to set
        """
        try:
            old_visibility = self.get_glyph_visibility(glyph_name)

            self.settings.setValue(f"visibility/glyph_{glyph_name}", visible)
            self.settings.sync()

            # Emit change event if visibility actually changed
            if old_visibility != visible:
                self.visibility_changed.emit(f"glyph_{glyph_name}", visible)
                logger.debug(f"Glyph {glyph_name} visibility changed to {visible}")

        except Exception as e:
            logger.error(f"Failed to set glyph visibility for {glyph_name}: {e}")

    def get_motion_visibility(self, motion_color: str) -> bool:
        """
        Get visibility for motion arrows (red/blue).

        Args:
            motion_color: Color of the motion ("red" or "blue")

        Returns:
            True if visible, False if hidden
        """
        try:
            if motion_color not in ["red", "blue"]:
                logger.warning(f"Invalid motion color: {motion_color}")
                return True

            default = self.DEFAULT_VISIBILITY.get(f"{motion_color}_motion", True)
            return self.settings.value(
                f"visibility/{motion_color}_motion", default, type=bool
            )
        except Exception as e:
            logger.error(f"Failed to get motion visibility for {motion_color}: {e}")
            return True

    def set_motion_visibility(self, motion_color: str, visible: bool) -> None:
        """
        Set visibility for motion arrows (red/blue).

        Args:
            motion_color: Color of the motion ("red" or "blue")
            visible: Visibility state to set
        """
        try:
            if motion_color not in ["red", "blue"]:
                logger.warning(f"Invalid motion color: {motion_color}")
                return

            old_visibility = self.get_motion_visibility(motion_color)

            self.settings.setValue(f"visibility/{motion_color}_motion", visible)
            self.settings.sync()

            # Emit change event if visibility actually changed
            if old_visibility != visible:
                self.visibility_changed.emit(f"{motion_color}_motion", visible)
                logger.debug(f"{motion_color} motion visibility changed to {visible}")

        except Exception as e:
            logger.error(f"Failed to set motion visibility for {motion_color}: {e}")

    def get_non_radial_visibility(self) -> bool:
        """
        Get visibility state for non-radial points.

        Returns:
            True if visible, False if hidden
        """
        try:
            default = self.DEFAULT_VISIBILITY.get("non_radial", True)
            return self.settings.value("visibility/non_radial", default, type=bool)
        except Exception as e:
            logger.error(f"Failed to get non-radial visibility: {e}")
            return True

    def set_non_radial_visibility(self, visible: bool) -> None:
        """
        Set visibility state for non-radial points.

        Args:
            visible: Visibility state to set
        """
        try:
            old_visibility = self.get_non_radial_visibility()

            self.settings.setValue("visibility/non_radial", visible)
            self.settings.sync()

            # Emit change event if visibility actually changed
            if old_visibility != visible:
                self.visibility_changed.emit("non_radial", visible)
                logger.debug(f"Non-radial visibility changed to {visible}")

        except Exception as e:
            logger.error(f"Failed to set non-radial visibility: {e}")

    def get_grid_visibility(self) -> bool:
        """
        Get grid visibility setting.

        Returns:
            True if grid is visible, False if hidden
        """
        try:
            default = self.DEFAULT_VISIBILITY.get("grid", True)
            return self.settings.value("visibility/grid", default, type=bool)
        except Exception as e:
            logger.error(f"Failed to get grid visibility: {e}")
            return True

    def set_grid_visibility(self, visible: bool) -> None:
        """
        Set grid visibility setting.

        Args:
            visible: Grid visibility state to set
        """
        try:
            old_visibility = self.get_grid_visibility()

            self.settings.setValue("visibility/grid", visible)
            self.settings.sync()

            # Emit change event if visibility actually changed
            if old_visibility != visible:
                self.visibility_changed.emit("grid", visible)
                logger.debug(f"Grid visibility changed to {visible}")

        except Exception as e:
            logger.error(f"Failed to set grid visibility: {e}")

    def get_all_visibility_settings(self) -> dict[str, bool]:
        """
        Get all visibility settings as a dictionary.

        Returns:
            Dictionary mapping element names to visibility states
        """
        try:
            result = {}

            # Get glyph visibilities
            for glyph_type in ["letter", "elemental", "vtg", "tka", "position"]:
                result[f"glyph_{glyph_type}"] = self.get_glyph_visibility(glyph_type)

            # Get motion visibilities
            for color in ["red", "blue"]:
                result[f"{color}_motion"] = self.get_motion_visibility(color)

            # Get other visibilities
            result["grid"] = self.get_grid_visibility()
            result["non_radial"] = self.get_non_radial_visibility()

            return result

        except Exception as e:
            logger.error(f"Failed to get all visibility settings: {e}")
            return self.DEFAULT_VISIBILITY.copy()

    def set_all_visibility_settings(self, visibility_dict: dict[str, bool]) -> bool:
        """
        Set multiple visibility settings at once.

        Args:
            visibility_dict: Dictionary of element names to visibility states

        Returns:
            True if all settings were applied successfully
        """
        try:
            success_count = 0
            total_count = len(visibility_dict)

            for element_name, visible in visibility_dict.items():
                try:
                    # Parse element name and call appropriate setter
                    if element_name.startswith("glyph_"):
                        glyph_name = element_name[6:]  # Remove "glyph_" prefix
                        self.set_glyph_visibility(glyph_name, visible)
                    elif element_name.endswith("_motion"):
                        color = element_name.split("_")[0]  # Get color part
                        self.set_motion_visibility(color, visible)
                    elif element_name == "grid":
                        self.set_grid_visibility(visible)
                    elif element_name == "non_radial":
                        self.set_non_radial_visibility(visible)
                    else:
                        logger.warning(f"Unknown visibility setting: {element_name}")
                        continue

                    success_count += 1

                except Exception as e:
                    logger.error(f"Failed to set visibility for {element_name}: {e}")

            logger.info(f"Set {success_count}/{total_count} visibility settings")
            return success_count == total_count

        except Exception as e:
            logger.error(f"Failed to set all visibility settings: {e}")
            return False

    def reset_to_defaults(self) -> None:
        """
        Reset all visibility settings to defaults.
        """
        try:
            self.set_all_visibility_settings(self.DEFAULT_VISIBILITY)
            logger.info("Reset all visibility settings to defaults")
        except Exception as e:
            logger.error(f"Failed to reset visibility settings: {e}")

    def toggle_glyph_visibility(self, glyph_name: str) -> bool:
        """
        Toggle the visibility of a glyph type.

        Args:
            glyph_name: Name of the glyph type

        Returns:
            New visibility state
        """
        current = self.get_glyph_visibility(glyph_name)
        new_state = not current
        self.set_glyph_visibility(glyph_name, new_state)
        return new_state

    def toggle_motion_visibility(self, motion_color: str) -> bool:
        """
        Toggle the visibility of motion arrows.

        Args:
            motion_color: Color of the motion ("red" or "blue")

        Returns:
            New visibility state
        """
        current = self.get_motion_visibility(motion_color)
        new_state = not current
        self.set_motion_visibility(motion_color, new_state)
        return new_state
