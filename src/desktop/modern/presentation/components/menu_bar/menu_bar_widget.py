"""
Modern Menu Bar Widget

Main menu bar component for the TKA modern desktop app.
Provides navigation, settings access, and social media integration.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from .navigation.menu_bar_navigation_widget import MenuBarNavigationWidget
from ..ui.buttons.styled_button import ButtonContext, StyledButton


if TYPE_CHECKING:
    pass


class MenuBarWidget(QWidget):
    """Modern menu bar with navigation and utility buttons."""

    tab_changed = pyqtSignal(str)  # Forward navigation signals
    settings_requested = pyqtSignal()

    def __init__(self, parent=None, size_provider: Callable[[], QSize] | None = None):
        super().__init__(parent)

        self._size_provider = size_provider or self._default_size_provider

        self._setup_ui()
        self._setup_styling()
        self._connect_signals()

    def _default_size_provider(self) -> QSize:
        """Default size provider if none given."""
        return QSize(1200, 800)

    def _setup_ui(self):
        """Setup the UI layout and components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create single container that holds both navigation and settings
        self.main_container = QWidget()
        main_layout.addWidget(self.main_container)

        # Container layout - horizontal with proper spacing management
        container_layout = QHBoxLayout(self.main_container)
        container_layout.setContentsMargins(10, 5, 10, 5)
        container_layout.setSpacing(0)

        # Left spacer to push navigation towards center
        container_layout.addStretch()

        # Navigation section - centered
        self.navigation_widget = MenuBarNavigationWidget(
            parent=self.main_container, size_provider=self._size_provider
        )
        container_layout.addWidget(self.navigation_widget)

        # Right spacer to balance the layout
        container_layout.addStretch()

        # Settings button - positioned absolutely on the right
        self.settings_button = StyledButton(
            label="⚙️ Settings",
            context=ButtonContext.SETTINGS,
            parent=self.main_container,
        )
        self.settings_button.clicked.connect(lambda: self.settings_requested.emit())
        self.settings_button.show()  # Make sure it's visible

        # Position settings button absolutely on the right
        # This will be handled in the resize event

        # Style the main container with more transparency to show background
        self.main_container.setStyleSheet(
            """
            QWidget {
                background: rgba(30, 30, 30, 0.3);
                border-bottom: 2px solid rgba(100, 149, 237, 0.2);
                border-radius: 0px;
            }
        """
        )
        self.main_container.setFixedHeight(60)

        # Initial positioning of settings button
        self._position_settings_button()

    def _setup_styling(self):
        """Apply styling to the menu bar."""
        self.setStyleSheet(
            """
            MenuBarWidget {
                background: transparent;
                border: none;
            }
        """
        )

    def _connect_signals(self):
        """Connect internal signals."""
        # Forward navigation signals
        self.navigation_widget.tab_changed.connect(self.tab_changed.emit)

    def set_active_tab(self, tab_name: str):
        """Set the active tab in the navigation widget."""
        self.navigation_widget.set_active_tab(tab_name)

    def get_current_tab(self) -> str:
        """Get the currently active tab."""
        return self.navigation_widget.get_current_tab()

    def get_available_tabs(self) -> list[str]:
        """Get list of available tabs."""
        return self.navigation_widget.get_available_tabs()

    def update_size_provider(self, size_provider: Callable[[], QSize]):
        """Update size provider for responsive design."""
        self._size_provider = size_provider
        self.navigation_widget.update_size_provider(size_provider)
        self._position_settings_button()

    def _position_settings_button(self):
        """Position the settings button absolutely on the right side."""
        if not hasattr(self, "settings_button") or not self.main_container.width():
            return

        # Update button sizing first
        available_size = self._size_provider()
        font_size = max(9, min(12, available_size.width() // 120))

        from PyQt6.QtGui import QFont

        font = QFont("Segoe UI", font_size, QFont.Weight.Medium)
        self.settings_button.setFont(font)
        self.settings_button.update_appearance()

        # Set a reasonable fixed width for the settings button
        settings_width = max(100, min(140, available_size.width() // 10))
        self.settings_button.setFixedSize(settings_width, 40)

        # Position settings button absolutely on the right side
        container_width = self.main_container.width()
        container_height = self.main_container.height()
        button_width = self.settings_button.width()
        button_height = self.settings_button.height()

        # Position with some margin from the right edge
        margin = 10
        x_pos = container_width - button_width - margin
        y_pos = (container_height - button_height) // 2  # Center vertically

        self.settings_button.move(x_pos, y_pos)
        self.settings_button.raise_()  # Ensure it's on top

    def resizeEvent(self, event):
        """Handle resize events."""
        super().resizeEvent(event)
        self._position_settings_button()
