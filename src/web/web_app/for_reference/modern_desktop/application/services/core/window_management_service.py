"""
Window Management Service

Pure service for window positioning and screen management.
Extracted from ApplicationLifecycleManager to follow single responsibility principle.

PROVIDES:
- Window positioning and sizing
- Screen detection and multi-monitor support
- Parallel testing mode geometry handling
- Screen validation
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QMainWindow


class IWindowManagementService(ABC):
    """Interface for window management operations."""

    @abstractmethod
    def set_window_dimensions(
        self,
        main_window: QMainWindow,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
    ) -> None:
        """Set window dimensions using modern responsive design."""

    @abstractmethod
    def determine_target_screen(self, parallel_mode=False, monitor=""):
        """Determine target screen for application placement."""

    @abstractmethod
    def validate_screen_configuration(self) -> dict:
        """Validate screen configuration and return status."""


class WindowManagementService(IWindowManagementService):
    """
    Pure service for window positioning and screen management.

    Handles window dimensions, screen detection, and multi-monitor support
    without any session or domain logic dependencies.
    """

    def set_window_dimensions(
        self,
        main_window: QMainWindow,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
    ) -> None:
        """Set window dimensions using modern responsive design: 90% of screen size."""
        # Check for parallel testing mode first
        if parallel_mode and parallel_geometry:
            try:
                x, y, width, height = map(int, parallel_geometry.split(","))
                main_window.setGeometry(x, y, width, height)
                main_window.setMinimumSize(1400, 900)
                print(f"🔄 Modern positioned at: {x},{y} ({width}x{height})")
                return
            except Exception as e:
                print(f"⚠️ Failed to apply parallel testing geometry: {e}")
                # Fall through to normal positioning

        # Use target screen for consistent positioning
        screen = target_screen or QGuiApplication.primaryScreen()

        if not screen:
            main_window.setGeometry(100, 100, 1400, 900)
            main_window.setMinimumSize(1400, 900)
            return

        # Calculate responsive dimensions (90% of screen)
        available_geometry = screen.availableGeometry()
        window_width = int(available_geometry.width() * 0.9)
        window_height = int(available_geometry.height() * 0.9)
        x = available_geometry.x() + int(
            (available_geometry.width() - window_width) / 2
        )
        y = available_geometry.y() + int(
            (available_geometry.height() - window_height) / 2
        )

        main_window.setGeometry(x, y, window_width, window_height)
        main_window.setMinimumSize(1400, 900)

    def determine_target_screen(self, parallel_mode=False, monitor=""):
        """Determine target screen for application placement."""
        screens = QGuiApplication.screens()

        # Override screen selection for parallel testing
        if parallel_mode and len(screens) > 1:
            if monitor in ["secondary", "right"]:
                # Determine which screen is physically on the right
                primary_screen = screens[0]
                secondary_screen = screens[1]

                # If secondary has higher X coordinate, it's on the right
                if secondary_screen.geometry().x() > primary_screen.geometry().x():
                    target_screen = secondary_screen
                    print(
                        "🔄 Modern forced to RIGHT monitor (secondary) for parallel testing"
                    )
                else:
                    # Primary is on the right
                    target_screen = primary_screen
                    print(
                        "🔄 Modern forced to RIGHT monitor (primary) for parallel testing"
                    )
                return target_screen
            if monitor in ["primary", "left"]:
                # Force to left monitor
                primary_screen = screens[0]
                secondary_screen = screens[1]

                if primary_screen.geometry().x() < secondary_screen.geometry().x():
                    target_screen = primary_screen
                    print(
                        "🔄 Modern forced to LEFT monitor (primary) for parallel testing"
                    )
                else:
                    target_screen = secondary_screen
                    print(
                        "🔄 Modern forced to LEFT monitor (secondary) for parallel testing"
                    )
                return target_screen

        # Default behavior: use primary screen
        return QGuiApplication.primaryScreen()

    def validate_screen_configuration(self) -> dict:
        """Validate screen configuration and return status."""
        try:
            screens = QGuiApplication.screens()
            primary_screen = QGuiApplication.primaryScreen()

            if not screens:
                return {
                    "valid": False,
                    "error": "No screens detected",
                    "screen_count": 0,
                    "primary_screen": None,
                }

            if not primary_screen:
                return {
                    "valid": False,
                    "error": "No primary screen detected",
                    "screen_count": len(screens),
                    "primary_screen": None,
                }

            # Collect screen information
            screen_info = []
            for i, screen in enumerate(screens):
                geometry = screen.geometry()
                available_geometry = screen.availableGeometry()
                screen_info.append(
                    {
                        "index": i,
                        "name": screen.name(),
                        "geometry": {
                            "x": geometry.x(),
                            "y": geometry.y(),
                            "width": geometry.width(),
                            "height": geometry.height(),
                        },
                        "available_geometry": {
                            "x": available_geometry.x(),
                            "y": available_geometry.y(),
                            "width": available_geometry.width(),
                            "height": available_geometry.height(),
                        },
                        "is_primary": screen == primary_screen,
                    }
                )

            return {
                "valid": True,
                "screen_count": len(screens),
                "primary_screen": primary_screen.name(),
                "screens": screen_info,
                "multi_monitor": len(screens) > 1,
            }

        except Exception as e:
            return {
                "valid": False,
                "error": f"Screen validation failed: {e}",
                "screen_count": 0,
                "primary_screen": None,
            }
