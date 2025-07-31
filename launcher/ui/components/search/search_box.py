"""
Reliable Search Box Component
============================

Professional search input with glassmorphism styling.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit

from ...pyqt6_compatible_design_system import get_reliable_style_builder
from ...reliable_effects import get_shadow_manager


class ReliableSearchBox(QLineEdit):
    """Reliable search box with consistent glassmorphism styling."""

    def __init__(self, placeholder: str = "Search...", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)

        self.style_builder = get_reliable_style_builder()
        self.shadow_manager = get_shadow_manager()

        # Set cursor for better UX
        self.setCursor(Qt.CursorShape.IBeamCursor)

        self._setup_styling()
        self._setup_effects()

    def _setup_styling(self):
        """Apply reliable glassmorphism styling."""
        self.setStyleSheet(
            f"""
            QLineEdit {{
                {self.style_builder.glass_surface("primary")}
                border-radius: {self.style_builder.tokens.RADIUS["lg"]}px;
                padding: 12px 20px;
                {self.style_builder.typography("base", "normal")}
                color: #ffffff;
            }}
            QLineEdit:hover {{
                {self.style_builder.glass_surface_hover("secondary")}
                border: {self.style_builder.tokens.BORDERS["hover"]};
            }}
            QLineEdit:focus {{
                {self.style_builder.glass_surface_hover("primary")}
                border: {self.style_builder.tokens.BORDERS["focus"]};
            }}
            QLineEdit::placeholder {{
                color: rgba(255, 255, 255, 0.5);
                font-style: italic;
            }}
        """
        )

    def _setup_effects(self):
        """Setup reliable visual effects."""
        self.shadow_manager.apply_card_shadow(self)

    def enterEvent(self, event):
        """Handle hover enter."""
        super().enterEvent(event)
        self.shadow_manager.apply_hover_shadow(self)

    def leaveEvent(self, event):
        """Handle hover leave."""
        super().leaveEvent(event)
        self.shadow_manager.reset_shadow(self)

    def focusInEvent(self, event):
        """Handle focus with reliable effects."""
        super().focusInEvent(event)
        self.shadow_manager.apply_hover_shadow(self)

    def focusOutEvent(self, event):
        """Handle focus out."""
        super().focusOutEvent(event)
        self.shadow_manager.reset_shadow(self)
