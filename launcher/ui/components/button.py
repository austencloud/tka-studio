"""
Reliable Button Component
========================

Professional button with glassmorphism styling and animations.
"""

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt

from ..reliable_design_system import get_reliable_style_builder
from ..reliable_effects import get_shadow_manager, get_animation_manager


class ReliableButton(QPushButton):
    """Reliable button with consistent styling and animations."""

    def __init__(self, text: str = "", variant: str = "primary", parent=None):
        super().__init__(text, parent)
        self.variant = variant

        self.style_builder = get_reliable_style_builder()
        self.shadow_manager = get_shadow_manager()
        self.animation_manager = get_animation_manager()

        # Set cursor to pointer for better UX
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._setup_styling()
        self._setup_effects()

    def _setup_styling(self):
        """Apply reliable button styling."""
        if self.variant == "primary":
            base_style = self.style_builder.accent_button()
        else:
            base_style = self.style_builder.secondary_button()

        self.setStyleSheet(
            f"""
            QPushButton {{
                {base_style}
                border-radius: {self.style_builder.tokens.RADIUS['md']}px;
                padding: 10px 20px;
                {self.style_builder.typography('base', 'medium')}
                min-height: 36px;
            }}
            QPushButton:hover {{
                {self.style_builder.glass_surface_hover('primary') if self.variant != 'primary' else base_style}
                border: {self.style_builder.tokens.BORDERS['hover']};
            }}
            QPushButton:pressed {{
                {self.style_builder.glass_surface('pressed')}
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

    def mousePressEvent(self, event):
        """Handle mouse press with animation."""
        super().mousePressEvent(event)

        # Reliable button press animation
        press_anim = self.animation_manager.button_press_feedback(self)
        press_anim.start()

        self.shadow_manager.apply_pressed_shadow(self)
