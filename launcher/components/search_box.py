"""
ModernSearchBox component for TKA Launcher.

This component provides a premium search box with glassmorphism styling 
and micro-interactions.
"""

import logging
from PyQt6.QtWidgets import QLineEdit

logger = logging.getLogger(__name__)

# Check for enhanced UI availability
ENHANCED_UI_AVAILABLE = False
try:
    from ui.reliable_design_system import get_style_builder, get_theme_manager
    from ui.reliable_effects import HoverAnimationMixin, get_effect_manager

    ENHANCED_UI_AVAILABLE = True
except ImportError as e:
    logger.debug(f"Enhanced UI components not available: {e}")


class ModernSearchBox(
    QLineEdit, HoverAnimationMixin if ENHANCED_UI_AVAILABLE else object
):
    """Premium search box with glassmorphism styling and micro-interactions."""

    def __init__(self, placeholder="Search...", parent=None):
        super().__init__(parent)
        if ENHANCED_UI_AVAILABLE:
            HoverAnimationMixin.__init__(self)

        self.setPlaceholderText(placeholder)
        self._setup_styling()
        self._setup_animations()
        self._setup_effects()

    def _setup_styling(self):
        """Apply premium glassmorphism styling with design system."""
        if ENHANCED_UI_AVAILABLE:
            try:
                style_builder = get_style_builder()
                theme = get_theme_manager().get_current_theme()

                self.setStyleSheet(
                    f"""
                    QLineEdit {{
                        {style_builder.glassmorphism_surface('primary')}
                        border-radius: {theme['radius']['lg']};
                        padding: {theme['spacing']['md']} {theme['spacing']['lg']};
                        {style_builder.typography('base', 'normal')}
                        color: #ffffff;
                        selection-background-color: {theme['accent']['surface']};
                    }}
                    QLineEdit:focus {{
                        {style_builder.glassmorphism_surface('primary', hover=True)}
                        border: 2px solid {theme['accent']['primary']};
                        outline: none;
                    }}
                    QLineEdit::placeholder {{
                        color: rgba(255, 255, 255, 0.5);
                        font-style: italic;
                    }}
                """
                )
            except Exception as e:
                logger.warning(f"Could not apply enhanced styling: {e}")
                self._apply_fallback_styling()
        else:
            self._apply_fallback_styling()

    def _apply_fallback_styling(self):
        """Apply fallback styling when enhanced UI is not available."""
        self.setStyleSheet(
            """
            QLineEdit {
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                padding: 14px 20px;
                font-family: 'Inter', sans-serif;
                font-size: 14px;
                color: #ffffff;
                font-weight: 400;
            }
            QLineEdit:focus {
                background: rgba(255, 255, 255, 0.18);
                border: 2px solid rgba(59, 130, 246, 0.6);
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.5);
                font-style: italic;
            }
        """
        )

    def _setup_animations(self):
        """Setup micro-interactions and animations."""
        if ENHANCED_UI_AVAILABLE:
            try:
                self.setup_hover_animations(self)
            except Exception as e:
                logger.warning(f"Could not setup animations: {e}")

    def _setup_effects(self):
        """Setup visual effects."""
        if ENHANCED_UI_AVAILABLE:
            try:
                effect_manager = get_effect_manager()
                effect_manager.apply_glassmorphism(self, "subtle")
            except Exception as e:
                logger.warning(f"Could not apply effects: {e}")

    def enterEvent(self, event):
        """Enhanced hover enter with animations."""
        super().enterEvent(event)
        if ENHANCED_UI_AVAILABLE and hasattr(self, "animate_hover_enter"):
            self.animate_hover_enter(self)

    def leaveEvent(self, event):
        """Enhanced hover leave with animations."""
        super().leaveEvent(event)
        if ENHANCED_UI_AVAILABLE and hasattr(self, "animate_hover_leave"):
            self.animate_hover_leave(self)
