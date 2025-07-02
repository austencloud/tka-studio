"""
Screen Service Implementation.

Handles multi-monitor detection, screen geometry calculation,
and intelligent screen selection for launcher positioning.
"""

import logging
from typing import List, Optional

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QScreen

from domain.models import ScreenData, WindowGeometry
from core.interfaces import IScreenService

logger = logging.getLogger(__name__)


class ScreenService(IScreenService):
    """
    Service for managing screens and monitor detection.

    Provides intelligent multi-monitor support with proper geometry
    calculation for both windowed and docked modes.
    """

    def __init__(self):
        """Initialize the screen service."""
        self._app = QApplication.instance()
        if not self._app:
            logger.warning(
                "No QApplication instance found, screen detection may be limited"
            )

    def get_available_screens(self) -> List[ScreenData]:
        """Get all available screens/monitors."""
        if not self._app:
            # Fallback for testing without QApplication
            return [self._create_default_screen()]

        screens = []
        qt_screens = self._app.screens()

        for i, screen in enumerate(qt_screens):
            geometry = self._qt_rect_to_geometry(screen.geometry())
            screen_data = ScreenData(
                index=i,
                name=screen.name(),
                geometry=geometry,
                is_primary=(screen == self._app.primaryScreen()),
                scale_factor=screen.devicePixelRatio(),
            )
            screens.append(screen_data)

        logger.debug(f"Found {len(screens)} screens")
        return screens

    def get_primary_screen(self) -> ScreenData:
        """Get the primary screen."""
        if not self._app:
            return self._create_default_screen()

        primary_screen = self._app.primaryScreen()
        if not primary_screen:
            return self._create_default_screen()

        geometry = self._qt_rect_to_geometry(primary_screen.geometry())
        return ScreenData(
            index=0,
            name=primary_screen.name(),
            geometry=geometry,
            is_primary=True,
            scale_factor=primary_screen.devicePixelRatio(),
        )

    def get_screen_by_index(self, index: int) -> Optional[ScreenData]:
        """Get screen by index."""
        screens = self.get_available_screens()
        if 0 <= index < len(screens):
            return screens[index]
        return None

    def get_current_screen(
        self, window_geometry: WindowGeometry
    ) -> Optional[ScreenData]:
        """Get the screen containing the specified window geometry."""
        screens = self.get_available_screens()

        # Find screen that contains the center of the window
        window_center_x = window_geometry.x + window_geometry.width // 2
        window_center_y = window_geometry.y + window_geometry.height // 2

        for screen in screens:
            if self._point_in_screen(window_center_x, window_center_y, screen):
                return screen

        # Fallback to primary screen
        return self.get_primary_screen()

    def calculate_docked_geometry(
        self, screen: ScreenData, dock_width: int = 110
    ) -> WindowGeometry:
        """Calculate geometry for docked mode on the specified screen."""
        # Position dock at bottom left as horizontal panel overlaying taskbar
        return WindowGeometry(
            x=screen.geometry.x,
            y=screen.geometry.y + screen.geometry.height - dock_width,
            width=screen.geometry.width,
            height=dock_width,
        )

    def calculate_centered_geometry(
        self, screen: ScreenData, width: int, height: int
    ) -> WindowGeometry:
        """Calculate centered window geometry on the specified screen."""
        center_x = screen.geometry.x + (screen.geometry.width - width) // 2
        center_y = screen.geometry.y + (screen.geometry.height - height) // 2

        return WindowGeometry(x=center_x, y=center_y, width=width, height=height)

    def is_geometry_on_screen(
        self, geometry: WindowGeometry, screen: ScreenData
    ) -> bool:
        """Check if geometry is within screen bounds."""
        # Check if any part of the window is on the screen
        window_right = geometry.x + geometry.width
        window_bottom = geometry.y + geometry.height
        screen_right = screen.geometry.x + screen.geometry.width
        screen_bottom = screen.geometry.y + screen.geometry.height

        return (
            geometry.x < screen_right
            and window_right > screen.geometry.x
            and geometry.y < screen_bottom
            and window_bottom > screen.geometry.y
        )

    def get_best_screen_for_docked_mode(self) -> ScreenData:
        """Get the best screen for docked mode (usually primary or leftmost)."""
        screens = self.get_available_screens()

        if not screens:
            return self._create_default_screen()

        # Prefer primary screen
        for screen in screens:
            if screen.is_primary:
                return screen

        # Fallback to leftmost screen
        leftmost_screen = min(screens, key=lambda s: s.geometry.x)
        return leftmost_screen

    def _qt_rect_to_geometry(self, rect: QRect) -> WindowGeometry:
        """Convert Qt QRect to WindowGeometry."""
        return WindowGeometry(
            x=rect.x(), y=rect.y(), width=rect.width(), height=rect.height()
        )

    def _point_in_screen(self, x: int, y: int, screen: ScreenData) -> bool:
        """Check if a point is within screen bounds."""
        return (
            screen.geometry.x <= x < screen.geometry.x + screen.geometry.width
            and screen.geometry.y <= y < screen.geometry.y + screen.geometry.height
        )

    def _create_default_screen(self) -> ScreenData:
        """Create a default screen for fallback scenarios."""
        return ScreenData(
            index=0,
            name="Default Screen",
            geometry=WindowGeometry(x=0, y=0, width=1920, height=1080),
            is_primary=True,
            scale_factor=1.0,
        )
