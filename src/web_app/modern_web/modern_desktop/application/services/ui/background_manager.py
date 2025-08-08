"""
Background Manager

Pure service for managing background widgets and animations.
Extracted from KineticConstructorModern to follow single responsibility principle.

PROVIDES:
- Background widget creation and management
- Background type switching
- Background cleanup and resource management
- Background positioning and resizing
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

from PyQt6.QtWidgets import QMainWindow


if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer
    from desktop.modern.presentation.components.backgrounds.background_widget import (
        MainBackgroundWidget,
    )


class IBackgroundManager(ABC):
    """Interface for background management operations."""

    @abstractmethod
    def setup_background(
        self,
        main_window: QMainWindow,
        container: DIContainer,
        progress_callback: Optional[callable] = None,
    ) -> MainBackgroundWidget:
        """Setup background widget for the main window."""

    @abstractmethod
    def apply_background_change(
        self, main_window: QMainWindow, background_type: str
    ) -> None:
        """Apply a background change immediately."""

    @abstractmethod
    def cleanup_background(self, background_widget: MainBackgroundWidget) -> None:
        """Clean up background widget resources."""


class BackgroundManager(IBackgroundManager):
    """
    Pure service for background management operations.

    Handles background widget lifecycle without business logic dependencies.
    Uses clean separation of concerns following TKA architecture.
    """

    def __init__(self):
        """Initialize background manager."""
        self.current_background: Optional[MainBackgroundWidget] = None

    def setup_background(
        self,
        main_window: QMainWindow,
        container: DIContainer,
        progress_callback: Optional[callable] = None,
    ) -> MainBackgroundWidget:
        """Setup background widget for the main window."""
        # Don't override progress - let orchestrator handle it

        # Get background type from UI state service
        from desktop.modern.core.interfaces.core_services import IUIStateManager

        ui_state_service = container.resolve(IUIStateManager)
        background_type = ui_state_service.get_setting("background_type", "Aurora")

        # Create background widget
        background_widget = self._create_background_widget(main_window, background_type)

        # Position and show background
        self._position_background(main_window, background_widget)
        background_widget.show()

        # Store reference for cleanup
        self.current_background = background_widget

        return background_widget

    def apply_background_change(
        self, main_window: QMainWindow, background_type: str
    ) -> None:
        """Apply a background change immediately."""
        try:
            # Clean up old background
            if self.current_background:
                self.cleanup_background(self.current_background)

            # Create new background widget
            new_background = self._create_background_widget(
                main_window, background_type
            )

            # Position and show new background
            self._position_background(main_window, new_background)
            new_background.show()

            # Update reference
            self.current_background = new_background

            print(f"✅ Background changed to: {background_type}")

        except Exception as e:
            print(f"⚠️ Failed to change background: {e}")

    def cleanup_background(self, background_widget: MainBackgroundWidget) -> None:
        """Clean up background widget resources."""
        if background_widget:
            # Call cleanup method if available
            if hasattr(background_widget, "cleanup"):
                background_widget.cleanup()

            # Hide and delete widget
            background_widget.hide()
            background_widget.deleteLater()

    def handle_window_resize(
        self, main_window: QMainWindow, background_widget: MainBackgroundWidget
    ) -> None:
        """Handle main window resize events for background positioning."""
        if background_widget:
            self._position_background(main_window, background_widget)

    def get_background_types(self) -> list[str]:
        """Get list of available background types."""
        return [
            "Aurora",
            "AuroraBorealis",
            "Starfield",
            "Snowfall",
            "Bubbles",
            "Solid",
        ]

    def is_background_animated(self, background_type: str) -> bool:
        """Check if background type is animated."""
        animated_backgrounds = {
            "Aurora",
            "AuroraBorealis",
            "Starfield",
            "Snowfall",
            "Bubbles",
        }
        return background_type in animated_backgrounds

    def get_background_performance_impact(self, background_type: str) -> str:
        """Get performance impact level for background type."""
        performance_map = {
            "Solid": "None",
            "Starfield": "Low",
            "Bubbles": "Low",
            "Snowfall": "Medium",
            "Aurora": "Medium",
            "AuroraBorealis": "High",
        }
        return performance_map.get(background_type, "Unknown")

    def _create_background_widget(
        self, main_window: QMainWindow, background_type: str
    ) -> MainBackgroundWidget:
        """Create background widget of specified type."""
        from desktop.modern.presentation.components.backgrounds.background_widget import (
            MainBackgroundWidget,
        )

        return MainBackgroundWidget(main_window, background_type)

    def _position_background(
        self, main_window: QMainWindow, background_widget: MainBackgroundWidget
    ) -> None:
        """Position background widget to cover the main window."""
        background_widget.setGeometry(main_window.rect())
        background_widget.lower()

    def get_background_settings(self) -> dict:
        """Get background-related settings and capabilities."""
        return {
            "available_types": self.get_background_types(),
            "animated_types": [
                bg_type
                for bg_type in self.get_background_types()
                if self.is_background_animated(bg_type)
            ],
            "performance_impact": {
                bg_type: self.get_background_performance_impact(bg_type)
                for bg_type in self.get_background_types()
            },
        }

    def validate_background_type(self, background_type: str) -> bool:
        """Validate that background type is supported."""
        return background_type in self.get_background_types()

    def get_recommended_background_for_performance(self) -> str:
        """Get recommended background type for best performance."""
        return "Starfield"  # Good balance of visual appeal and performance

    def get_current_background_info(self) -> dict:
        """Get information about current background."""
        if not self.current_background:
            return {"type": None, "active": False}

        # Try to determine background type from widget
        background_type = getattr(self.current_background, "background_type", "Unknown")

        return {
            "type": background_type,
            "active": True,
            "animated": self.is_background_animated(background_type),
            "performance_impact": self.get_background_performance_impact(
                background_type
            ),
        }
