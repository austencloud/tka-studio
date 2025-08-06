"""
Modern Menu Bar Navigation Widget

Navigation component for the TKA modern desktop app with tab management.
Provides clean button-based navigation between different application sections.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from ...ui.buttons.styled_button import ButtonContext, StyledButton


if TYPE_CHECKING:
    pass


class MenuBarNavigationWidget(QWidget):
    """Modern navigation widget with tab buttons."""

    tab_changed = pyqtSignal(str)  # Emit tab name instead of index

    def __init__(self, parent=None, size_provider: Callable[[], QSize] | None = None):
        super().__init__(parent)

        self._size_provider = size_provider or self._default_size_provider
        self._current_tab = "construct"  # Default to construct tab

        # Tab configuration
        self.tab_config = [
            {"name": "construct", "label": "Construct ⚒️"},
            {"name": "browse", "label": "Browse 🔍"},
            {"name": "write", "label": "Write ✍️"},
            {"name": "learn", "label": "Learn 🧠"},
            {"name": "sequence_card", "label": "Sequence Card 📋"},
        ]

        self.tab_buttons: dict[str, StyledButton] = {}

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

        # Button layout - centered horizontally
        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()  # Add stretch before buttons

        # Create tab buttons
        for tab_info in self.tab_config:
            button = StyledButton(
                label=tab_info["label"], context=ButtonContext.NAVIGATION, parent=self
            )
            button.clicked.connect(
                lambda checked, name=tab_info["name"]: self._on_tab_clicked(name)
            )

            self.tab_buttons[tab_info["name"]] = button
            self.button_layout.addWidget(button)

        self.button_layout.addStretch()  # Add stretch after buttons

        main_layout.addLayout(self.button_layout)

        # Set initial active tab
        self._update_button_states()

    def _setup_styling(self):
        """Apply modern styling to the navigation widget."""
        self.setStyleSheet(
            """
            MenuBarNavigationWidget {
                background: transparent;
                border: none;
            }
        """
        )

    def _connect_signals(self):
        """Connect internal signals."""

    def _on_tab_clicked(self, tab_name: str):
        """Handle tab button click."""
        if tab_name != self._current_tab:
            self.set_active_tab(tab_name)

    def set_active_tab(self, tab_name: str):
        """Set the active tab and update button states."""
        if tab_name not in self.tab_buttons:
            print(f"Warning: Unknown tab name: {tab_name}")
            return

        self._current_tab = tab_name
        self._update_button_states()
        self.tab_changed.emit(tab_name)

    def _update_button_states(self):
        """Update button visual states and sizing."""
        # Update button selection states
        for name, button in self.tab_buttons.items():
            is_active = name == self._current_tab
            button.set_selected(is_active)

        # Update button sizing based on available space
        self._update_button_sizing()

    def _update_button_sizing(self):
        """Update button sizes based on available space."""
        if not self._size_provider:
            return

        available_size = self._size_provider()

        # Calculate button dimensions
        total_buttons = len(self.tab_buttons)
        if total_buttons == 0:
            return

        # Use responsive sizing - make buttons wider
        base_width = max(
            140,
            available_size.width()
            // (total_buttons + 1.5),  # Less spacing allowance for wider buttons
        )
        button_width = min(base_width, 220)  # Increased max width cap from 180 to 220

        # Apply font sizing
        font_size = max(10, min(14, available_size.width() // 100))
        font = QFont("Segoe UI", font_size, QFont.Weight.Medium)

        # Update button height based on font size to prevent text clipping
        button_height = max(
            44, int(font_size * 2.8)
        )  # Dynamic height based on font size, minimum 44px

        # Update all buttons
        try:
            for button in self.tab_buttons.values():
                button.setFixedSize(button_width, button_height)
                button.setFont(font)
                button.update_appearance()
        except Exception as e:
            print(f"Error updating button appearance: {e}")

        # Update spacing
        spacing = max(5, available_size.width() // 200)
        self.button_layout.setSpacing(spacing)

    def get_current_tab(self) -> str:
        """Get the currently active tab name."""
        return self._current_tab

    def get_available_tabs(self) -> list[str]:
        """Get list of available tab names."""
        return [tab["name"] for tab in self.tab_config]

    def resizeEvent(self, event):
        """Handle resize events to update button sizing."""
        super().resizeEvent(event)
        self._update_button_sizing()

    def update_size_provider(self, size_provider: Callable[[], QSize]):
        """Update the size provider and refresh sizing."""
        self._size_provider = size_provider
        self._update_button_sizing()
