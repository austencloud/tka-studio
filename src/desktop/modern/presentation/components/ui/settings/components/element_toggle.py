"""
Element Toggle Component for Visibility Settings.

Reusable element visibility checkbox with dependency awareness and glassmorphism styling.
Extracted from the monolithic visibility tab for better component organization.
"""

from __future__ import annotations

from PyQt6.QtWidgets import QCheckBox


class ElementToggle(QCheckBox):
    """Modern styled checkbox for element visibility with dependency awareness."""

    def __init__(self, label: str, tooltip: str | None = None, parent=None):
        """
        Initialize element toggle checkbox.

        Args:
            label: Display label for the checkbox
            tooltip: Optional tooltip text
            parent: Parent widget
        """
        super().__init__(label, parent)

        if tooltip:
            self.setToolTip(tooltip)

        self.is_dependent = False
        self._apply_styling()

    def set_dependent(self, dependent: bool):
        """
        Mark this toggle as dependent on motion visibility.

        Args:
            dependent: Whether this element depends on motion visibility
        """
        self.is_dependent = dependent
        self._update_enabled_state()

    def set_motions_visible(self, visible: bool):
        """
        Update enabled state based on motion visibility.

        Args:
            visible: Whether motions are visible (affects dependent elements)
        """
        if self.is_dependent:
            self.setEnabled(visible)
            self._update_enabled_state()

    def _update_enabled_state(self):
        """Update styling based on enabled state."""
        self._apply_styling()

    def _apply_styling(self):
        """Apply modern glassmorphism styling with dependency awareness."""
        if self.isEnabled():
            opacity = "1.0"
            text_color = "white"
        else:
            opacity = "0.5"
            text_color = "rgba(255, 255, 255, 0.5)"

        self.setStyleSheet(
            f"""
            QCheckBox {{
                color: {text_color};
                font-size: 14px;
                font-weight: 500;
                spacing: 10px;
                padding: 8px;
                opacity: {opacity};
            }}

            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border: 2px solid rgba(255, 255, 255, 0.4);
                border-radius: 6px;
                background: rgba(255, 255, 255, 0.1);
            }}

            QCheckBox::indicator:hover {{
                border-color: rgba(255, 255, 255, 0.6);
                background: rgba(255, 255, 255, 0.15);
            }}

            QCheckBox::indicator:checked {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(34, 197, 94, 0.9),
                    stop:1 rgba(34, 197, 94, 0.7));
                border-color: rgba(34, 197, 94, 1.0);
            }}

            QCheckBox::indicator:checked:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(34, 197, 94, 1.0),
                    stop:1 rgba(34, 197, 94, 0.8));
            }}
        """
        )

    def get_is_dependent(self) -> bool:
        """Get whether this element is dependent on motion visibility."""
        return self.is_dependent
