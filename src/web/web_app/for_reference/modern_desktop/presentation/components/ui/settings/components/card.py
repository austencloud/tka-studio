"""
Enhanced Setting Card component with glassmorphism styling.
Ported from legacy settings dialog with improvements and optimized spacing.
"""

from __future__ import annotations

from typing import Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget


class SettingCard(QFrame):
    """Setting card with glassmorphism styling and flexible content."""

    value_changed = pyqtSignal(str, object)  # setting_key, new_value

    def __init__(
        self,
        title: str,
        description: str | None = None,
        setting_key: str | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self.title = title
        self.description = description
        self.setting_key = setting_key

        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self):
        """Set up the card UI structure with improved accessibility spacing."""
        self.setObjectName("setting_card")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)  # Increased for better accessibility
        layout.setSpacing(8)  # Increased for better readability

        # Header with title and optional description
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)  # Improved spacing for readability

        # Title
        self.title_label = QLabel(self.title)
        self.title_label.setObjectName("setting_title")
        self.title_label.setFont(QFont("Inter", 11, QFont.Weight.Bold))
        header_layout.addWidget(self.title_label)

        # Description (if provided)
        if self.description:
            self.description_label = QLabel(self.description)
            self.description_label.setObjectName("setting_description")
            self.description_label.setFont(QFont("Inter", 9))
            self.description_label.setWordWrap(True)
            header_layout.addWidget(self.description_label)

        layout.addLayout(header_layout)

        # Content area for controls (to be added by subclasses)
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 8, 0, 0)  # Improved spacing
        layout.addLayout(self.content_layout)

        # Add stretch to push controls to the right if needed
        self.content_layout.addStretch()

    def add_control(self, control: QWidget, align_right: bool = True):
        """Add a control widget to the content area."""
        if align_right:
            # Remove the stretch and add control, then add stretch back
            if self.content_layout.count() > 0:
                item = self.content_layout.takeAt(0)  # Remove stretch
                if item and item.widget():
                    item.widget().deleteLater()
            self.content_layout.addStretch()
            self.content_layout.addWidget(control)
        else:
            # Add control at the beginning
            self.content_layout.insertWidget(0, control)

    def _apply_styling(self):
        """Apply enhanced glassmorphism styling to the card with better spacing."""
        self.setStyleSheet(
            """
            QFrame#setting_card {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.10));
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 12px;
                margin: 2px 0;
            }

            QFrame#setting_card:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.22),
                    stop:1 rgba(255, 255, 255, 0.16));
                border-color: rgba(255, 255, 255, 0.35);
            }

            QLabel#setting_title {
                color: rgba(255, 255, 255, 0.95);
                background: transparent;
                border: none;
                font-family: "Inter", "Segoe UI", sans-serif;
                font-weight: 600;
                letter-spacing: 0.2px;
            }

            QLabel#setting_description {
                color: rgba(255, 255, 255, 0.75);
                background: transparent;
                border: none;
                font-family: "Inter", "Segoe UI", sans-serif;
                font-weight: 400;
                letter-spacing: 0.1px;
                line-height: 1.4;
            }
        """
        )

    def emit_change(self, value: Any):
        """Emit value change signal with the setting key."""
        if self.setting_key:
            self.value_changed.emit(self.setting_key, value)


class ToggleCard(SettingCard):
    """Setting card with a modern toggle switch."""

    def __init__(
        self,
        title: str,
        description: str | None = None,
        setting_key: str | None = None,
        initial_value: bool = False,
        parent=None,
    ):
        self.current_value = initial_value
        super().__init__(title, description, setting_key, parent)
        self._create_toggle()

    def _create_toggle(self):
        """Create and add the toggle control."""
        from .toggle import Toggle

        self.toggle = Toggle()
        self.toggle.setChecked(self.current_value)
        self.toggle.toggled.connect(self._on_toggle_changed)
        self.add_control(self.toggle)

    def _on_toggle_changed(self, checked: bool):
        """Handle toggle state change."""
        self.current_value = checked
        self.emit_change(checked)

    def set_value(self, value: bool):
        """Set the toggle value programmatically."""
        self.current_value = value
        self.toggle.setChecked(value)


class ComboCard(SettingCard):
    """Setting card with a styled combo box."""

    def __init__(
        self,
        title: str,
        description: str | None = None,
        setting_key: str | None = None,
        options: list[str] | None = None,
        initial_value: str = "",
        parent=None,
    ):
        self.options = options or []
        self.current_value = initial_value
        super().__init__(title, description, setting_key, parent)
        self._create_combo()

    def _create_combo(self):
        """Create and add the combo box control."""
        from .combo_box import ComboBox

        self.combo = ComboBox(self.options)
        if self.current_value in self.options:
            self.combo.setCurrentText(self.current_value)

        self.combo.currentTextChanged.connect(self._on_combo_changed)
        self.add_control(self.combo)

    def _on_combo_changed(self, text: str):
        """Handle combo box selection change."""
        self.current_value = text
        self.emit_change(text)

    def set_value(self, value: str):
        """Set the combo box value programmatically."""
        self.current_value = value
        if value in self.options:
            self.combo.setCurrentText(value)

    def get_value(self) -> str:
        """Get the current combo box value."""
        return self.current_value
