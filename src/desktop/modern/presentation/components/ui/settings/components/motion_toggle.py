"""
Motion Toggle Component for Visibility Settings.

Reusable motion toggle button with color coding and glassmorphism styling.
Extracted from the monolithic visibility tab for better component organization.
"""


from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QPushButton


class MotionToggle(QPushButton):
    """Large, prominent motion toggle button with color coding and glassmorphism styling."""

    toggled = pyqtSignal(bool)

    def __init__(self, color: str, parent=None):
        """
        Initialize motion toggle button.
        
        Args:
            color: Motion color ("blue" or "red")
            parent: Parent widget
        """
        super().__init__(parent)
        self.color = color
        self.is_active = True
        
        self.setCheckable(True)
        self.setChecked(True)
        self.setText(f"{color.title()} Motion")
        self.setMinimumSize(100, 35)
        self.setMaximumSize(120, 40)
        
        self.clicked.connect(self._on_clicked)
        self._apply_styling()

    def _on_clicked(self):
        """Handle button click and emit toggled signal."""
        self.toggled.emit(self.isChecked())

    def set_active(self, active: bool):
        """
        Set active state and update styling.
        
        Args:
            active: Whether the motion is active/visible
        """
        self.is_active = active
        self.setChecked(active)
        self._apply_styling()

    def _apply_styling(self):
        """Apply color-coded glassmorphism styling based on motion color and state."""
        base_color = (
            "59, 130, 246" if self.color == "blue" else "239, 68, 68"
        )  # Blue or Red

        if self.is_active:
            background = f"rgba({base_color}, 0.8)"
            border_color = f"rgba({base_color}, 1.0)"
            text_color = "white"
        else:
            background = "rgba(255, 255, 255, 0.1)"
            border_color = "rgba(255, 255, 255, 0.3)"
            text_color = "rgba(255, 255, 255, 0.6)"

        self.setStyleSheet(
            f"""
            QPushButton {{
                background: {background};
                border: 2px solid {border_color};
                border-radius: 12px;
                color: {text_color};
                font-size: 14px;
                font-weight: bold;
                padding: 8px 16px;
            }}

            QPushButton:hover {{
                background: rgba({base_color}, 0.9);
                border-color: rgba({base_color}, 1.0);
            }}

            QPushButton:pressed {{
                background: rgba({base_color}, 0.7);
            }}
        """
        )

    def get_color(self) -> str:
        """Get the motion color."""
        return self.color

    def get_is_active(self) -> bool:
        """Get the active state."""
        return self.is_active
