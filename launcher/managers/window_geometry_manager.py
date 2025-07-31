#!/usr/bin/env python3
"""
Window Geometry Manager - Window Positioning and State Management
================================================================

Handles window geometry, positioning, and state persistence:
- Window geometry calculations and setup
- State saving and restoration
- Multi-monitor support
- Window positioning optimization

Architecture:
- Extracted from launcher_window.py for better separation of concerns
- Manages window geometry and positioning logic
- Handles state persistence across sessions
"""

import logging
from typing import Any, Optional

from config.config.launcher_config import LauncherConfig
from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QApplication, QWidget

logger = logging.getLogger(__name__)


class WindowGeometryManager:
    """Manages window geometry, positioning, and state persistence."""

    def __init__(self, config: LauncherConfig):
        """Initialize the geometry manager."""
        self.config = config
        self.saved_geometry = None
        self.saved_dock_geometry = None

    def setup_window_geometry(self, window: QWidget):
        """Setup initial window geometry."""
        try:
            # Try to restore from config first
            saved_rect = self.config.get_window_geometry()

            if saved_rect.x() != 0 or saved_rect.y() != 0:
                # Use saved geometry
                window.setGeometry(saved_rect)
                # Restored window geometry - log removed to reduce startup noise
            else:
                # Calculate centered position
                centered_rect = self._calculate_centered_geometry(
                    saved_rect.width(), saved_rect.height()
                )
                window.setGeometry(centered_rect)
                logger.info(f"📐 Set centered window geometry: {centered_rect}")

        except Exception as e:
            logger.error(f"❌ Failed to setup window geometry: {e}")
            # Fallback to default size and center
            self._set_default_geometry(window)

    def _calculate_centered_geometry(self, width: int, height: int) -> QRect:
        """Calculate centered window geometry."""
        screen = QApplication.primaryScreen()
        if not screen:
            return QRect(100, 100, width, height)

        screen_geometry = screen.availableGeometry()

        # Center the window
        x = screen_geometry.x() + (screen_geometry.width() - width) // 2
        y = screen_geometry.y() + (screen_geometry.height() - height) // 2

        return QRect(x, y, width, height)

    def _set_default_geometry(self, window: QWidget):
        """Set default window geometry as fallback."""
        default_width = 1000
        default_height = 700

        centered_rect = self._calculate_centered_geometry(default_width, default_height)
        window.setGeometry(centered_rect)

        logger.info(f"📐 Set default window geometry: {centered_rect}")

    def save_window_geometry(self, window: QWidget):
        """Save current window geometry."""
        try:
            current_geometry = window.geometry()
            self.saved_geometry = current_geometry

            # Save to config using correct LauncherConfig API
            self.config.set_window_geometry(current_geometry)
            self.config.save_configuration()

            logger.debug(f"💾 Saved window geometry: {current_geometry}")

        except Exception as e:
            logger.error(f"❌ Failed to save window geometry: {e}")

    def restore_window_geometry(self, window: QWidget):
        """Restore previously saved window geometry."""
        try:
            if self.saved_geometry:
                window.setGeometry(self.saved_geometry)
                logger.debug(f"📐 Restored window geometry: {self.saved_geometry}")
            else:
                # Try to restore from config
                saved_rect = self.config.get_window_geometry()
                if saved_rect.x() != 0 or saved_rect.y() != 0:
                    window.setGeometry(saved_rect)
                    logger.debug(f"📐 Restored geometry from config: {saved_rect}")

        except Exception as e:
            logger.error(f"❌ Failed to restore window geometry: {e}")

    def save_dock_geometry(self, dock_geometry: QRect):
        """Save dock window geometry."""
        try:
            self.saved_dock_geometry = dock_geometry
            logger.debug(f"💾 Saved dock geometry: {dock_geometry}")

        except Exception as e:
            logger.error(f"❌ Failed to save dock geometry: {e}")

    def get_saved_dock_geometry(self) -> Optional[QRect]:
        """Get saved dock geometry."""
        return self.saved_dock_geometry

    def optimize_window_position(self, window: QWidget) -> bool:
        """Optimize window position for current screen configuration."""
        try:
            current_geometry = window.geometry()
            screen = QApplication.screenAt(current_geometry.center())

            if not screen:
                screen = QApplication.primaryScreen()

            if not screen:
                return False

            screen_geometry = screen.availableGeometry()

            # Check if window is completely within screen bounds
            if screen_geometry.contains(current_geometry):
                return True  # Already optimized

            # Adjust position to fit within screen
            x = max(
                screen_geometry.x(),
                min(
                    current_geometry.x(),
                    screen_geometry.right() - current_geometry.width(),
                ),
            )
            y = max(
                screen_geometry.y(),
                min(
                    current_geometry.y(),
                    screen_geometry.bottom() - current_geometry.height(),
                ),
            )

            optimized_geometry = QRect(
                x, y, current_geometry.width(), current_geometry.height()
            )
            window.setGeometry(optimized_geometry)

            logger.info(f"🎯 Optimized window position: {optimized_geometry}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to optimize window position: {e}")
            return False

    def get_screen_info(self) -> dict[str, Any]:
        """Get information about available screens."""
        screens_info = []

        for i, screen in enumerate(QApplication.screens()):
            screen_info = {
                "index": i,
                "name": screen.name(),
                "geometry": {
                    "x": screen.geometry().x(),
                    "y": screen.geometry().y(),
                    "width": screen.geometry().width(),
                    "height": screen.geometry().height(),
                },
                "available_geometry": {
                    "x": screen.availableGeometry().x(),
                    "y": screen.availableGeometry().y(),
                    "width": screen.availableGeometry().width(),
                    "height": screen.availableGeometry().height(),
                },
                "is_primary": screen == QApplication.primaryScreen(),
                "device_pixel_ratio": screen.devicePixelRatio(),
            }
            screens_info.append(screen_info)

        return {
            "screen_count": len(QApplication.screens()),
            "primary_screen": (
                QApplication.primaryScreen().name()
                if QApplication.primaryScreen()
                else None
            ),
            "screens": screens_info,
        }

    def validate_geometry(self, geometry: QRect) -> bool:
        """Validate that geometry is reasonable and within screen bounds."""
        if geometry.width() < 400 or geometry.height() < 300:
            logger.warning(f"⚠️ Geometry too small: {geometry}")
            return False

        # Check if geometry intersects with any screen
        for screen in QApplication.screens():
            if screen.availableGeometry().intersects(geometry):
                return True

        logger.warning(f"⚠️ Geometry outside all screens: {geometry}")
        return False

    def get_geometry_info(self, window: QWidget) -> dict[str, Any]:
        """Get detailed geometry information for debugging."""
        current_geometry = window.geometry()

        return {
            "current_geometry": {
                "x": current_geometry.x(),
                "y": current_geometry.y(),
                "width": current_geometry.width(),
                "height": current_geometry.height(),
            },
            "saved_geometry": (
                {
                    "x": self.saved_geometry.x() if self.saved_geometry else None,
                    "y": self.saved_geometry.y() if self.saved_geometry else None,
                    "width": (
                        self.saved_geometry.width() if self.saved_geometry else None
                    ),
                    "height": (
                        self.saved_geometry.height() if self.saved_geometry else None
                    ),
                }
                if self.saved_geometry
                else None
            ),
            "config_geometry": {
                "x": self.config.get_window_geometry().x(),
                "y": self.config.get_window_geometry().y(),
                "width": self.config.get_window_geometry().width(),
                "height": self.config.get_window_geometry().height(),
            },
            "is_valid": self.validate_geometry(current_geometry),
            "screen_info": self.get_screen_info(),
        }
