#!/usr/bin/env python3
"""
Dock Position Manager - Window Positioning and Geometry Logic
============================================================

Handles positioning and geometry calculations for the TKA dock window:
- Screen positioning based on dock configuration
- Height calculations based on application count
- Screen boundary validation
- Multi-monitor support

Architecture:
- Extracted from dock_window.py for better separation of concerns
- Pure calculation logic without UI dependencies
- Supports different dock positions and configurations
"""

import logging
from typing import List
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QScreen

from domain.models import (
    DockConfiguration,
    DockPosition,
    ApplicationData,
    WindowGeometry,
)

logger = logging.getLogger(__name__)


class DockPositionManager:
    """Manages positioning and geometry calculations for dock windows."""

    def __init__(self, dock_config: DockConfiguration):
        """Initialize the position manager with dock configuration."""
        self.dock_config = dock_config
        self.base_height = 16  # Base height for padding and borders
        self.icon_size = 48  # Size of each application icon
        self.icon_spacing = 2  # Spacing between icons

    def calculate_dock_height(self, application_count: int = None) -> int:
        """Calculate appropriate dock height based on number of applications."""
        screen = QApplication.primaryScreen()
        if screen:
            full_h = screen.geometry().height()
            avail_h = screen.availableGeometry().height()
            task_h = full_h - avail_h
            # subtract a small padding to ensure icons don't exceed taskbar
            dock_h = max(task_h - 2, 0)
            logger.debug(f"🔧 Taskbar height: {task_h}, setting dock height: {dock_h}")
            return dock_h
        # Fallback to default icon size plus padding
        return self.base_height + self.icon_size + self.icon_spacing

    def calculate_actual_dock_height(self, applications: List[ApplicationData]) -> int:
        """Calculate dock height based on actual number of applications."""
        # Use same logic as calculate_dock_height
        screen = QApplication.primaryScreen()
        if screen:
            full_h = screen.geometry().height()
            avail_h = screen.availableGeometry().height()
            task_h = full_h - avail_h
            dock_h = max(task_h - 2, 0)
            logger.debug(f"🔧 Taskbar height: {task_h}, actual dock height: {dock_h}")
            return dock_h
        # Fallback to default icon size plus padding
        return self.base_height + self.icon_size + self.icon_spacing

    def position_dock(self, dock_widget) -> bool:
        """Position the dock on screen according to configuration."""
        screen = QApplication.primaryScreen()
        if not screen:
            logger.warning("⚠️ No screen available for dock positioning")
            return False

        # Use full screen geometry so dock overlays the taskbar
        screen_geometry = screen.geometry()
        dock_rect = self.calculate_dock_position(screen_geometry, dock_widget.height())

        dock_widget.setGeometry(dock_rect)
        logger.info(f"📍 Positioned dock at {dock_rect}")
        return True

    def calculate_dock_position(
        self, screen_geometry: QRect, dock_height: int
    ) -> QRect:
        """Calculate horizontal bottom-docked position overlaying the taskbar."""
        # Full width dock overlaying taskbar at bottom
        dock_width = screen_geometry.width() - 2 * self.dock_config.margin_x
        x = screen_geometry.left() + self.dock_config.margin_x
        y = screen_geometry.bottom() - dock_height - self.dock_config.margin_y
        return QRect(x, y, dock_width, dock_height)

    def get_dock_geometry(self, dock_widget) -> WindowGeometry:
        """Get current dock geometry for state persistence."""
        geometry = dock_widget.geometry()
        return WindowGeometry(
            x=geometry.x(),
            y=geometry.y(),
            width=geometry.width(),
            height=geometry.height(),
        )

    def validate_position(self, dock_rect: QRect) -> bool:
        """Validate that the dock position is within screen bounds."""
        screen = QApplication.primaryScreen()
        if not screen:
            return False

        screen_geometry = screen.geometry()

        # Check if dock is completely within screen bounds
        if not screen_geometry.contains(dock_rect):
            logger.warning(
                f"⚠️ Dock position {dock_rect} is outside screen bounds {screen_geometry}"
            )
            return False

        return True

    def get_available_positions(self) -> List[DockPosition]:
        """Get list of available dock positions."""
        return [
            DockPosition.BOTTOM_LEFT,
            DockPosition.BOTTOM_RIGHT,
            DockPosition.TOP_LEFT,
            DockPosition.TOP_RIGHT,
        ]

    def suggest_optimal_position(self) -> DockPosition:
        """Suggest optimal dock position based on screen configuration."""
        screen = QApplication.primaryScreen()
        if not screen:
            return DockPosition.BOTTOM_LEFT

        screen_geometry = screen.geometry()

        # For wide screens, prefer left/right positions
        # For tall screens, prefer top/bottom positions
        aspect_ratio = screen_geometry.width() / screen_geometry.height()

        if aspect_ratio > 1.5:  # Wide screen
            return DockPosition.BOTTOM_LEFT
        else:  # More square or tall screen
            return DockPosition.BOTTOM_LEFT  # Default to bottom-left

    def update_configuration(self, new_config: DockConfiguration):
        """Update dock configuration."""
        self.dock_config = new_config
        logger.info(f"📝 Updated dock configuration: {new_config}")

    def get_position_info(self) -> dict:
        """Get detailed information about current position configuration."""
        screen = QApplication.primaryScreen()
        screen_info = {}

        if screen:
            geometry = screen.geometry()
            screen_info = {
                "screen_width": geometry.width(),
                "screen_height": geometry.height(),
                "screen_x": geometry.x(),
                "screen_y": geometry.y(),
            }

        return {
            "dock_config": {
                "position": self.dock_config.position.value,
                "width": self.dock_config.width,
                "margin_x": self.dock_config.margin_x,
                "margin_y": self.dock_config.margin_y,
            },
            "screen_info": screen_info,
            "calculated_dimensions": {
                "base_height": self.base_height,
                "icon_size": self.icon_size,
                "icon_spacing": self.icon_spacing,
            },
        }
