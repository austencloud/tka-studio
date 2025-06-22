"""
ModernButton component for TKA Launcher.

This component provides a premium button with glassmorphism styling 
and spring animations.
"""

import logging
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve

logger = logging.getLogger(__name__)

# Check for enhanced UI availability
ENHANCED_UI_AVAILABLE = False
try:
    from ui.design_system import get_style_builder, get_theme_manager
    from ui.effects.glassmorphism import get_effect_manager
    from ui.components.animation_mixins import FeedbackAnimationMixin
    ENHANCED_UI_AVAILABLE = True
except ImportError as e:
    logger.debug(f"Enhanced UI components not available: {e}")


class ModernButton(
    QPushButton, FeedbackAnimationMixin if ENHANCED_UI_AVAILABLE else object
):
    """Premium button with glassmorphism styling and spring animations."""

    def __init__(self, text="", button_type="primary", parent=None):
        super().__init__(text, parent)
        if ENHANCED_UI_AVAILABLE:
            FeedbackAnimationMixin.__init__(self)

        self.button_type = button_type
        self._setup_styling()
        self._setup_animations()
        self._setup_effects()

    def _setup_styling(self):
        """Apply premium button styling with design system."""
        if ENHANCED_UI_AVAILABLE:
            try:
                style_builder = get_style_builder()
                theme = get_theme_manager().get_current_theme()

                button_css = style_builder.button_style(self.button_type)
                typography_css = style_builder.typography("base", "medium")

                self.setStyleSheet(
                    f"""
                    QPushButton {{
                        {button_css}
                        {typography_css}
                        border-radius: {theme['radius']['md']};
                        padding: {theme['spacing']['md']} {theme['spacing']['lg']};
                    }}
                    QPushButton:hover {{
                        background-color: {theme['accent']['primary'] if self.button_type == 'primary' else theme['glass']['surface_hover']};
                    }}
                    QPushButton:pressed {{
                        background-color: {theme['accent']['secondary'] if self.button_type == 'primary' else theme['glass']['surface_pressed']};
                    }}
                """
                )
            except Exception as e:
                logger.warning(f"Could not apply enhanced button styling: {e}")
                self._apply_fallback_styling()
        else:
            self._apply_fallback_styling()

    def _apply_fallback_styling(self):
        """Apply fallback styling when enhanced UI is not available."""
        if self.button_type == "primary":
            self.setStyleSheet(
                """
                QPushButton {
                    background: linear-gradient(135deg, rgba(59, 130, 246, 0.8), rgba(37, 99, 235, 0.8));
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 12px;
                    padding: 12px 24px;
                    font-family: 'Inter', sans-serif;
                    font-size: 14px;
                    font-weight: 500;
                    color: #ffffff;
                }
                QPushButton:hover {
                    background: linear-gradient(135deg, rgba(59, 130, 246, 0.9), rgba(37, 99, 235, 0.9));
                    border: 1px solid rgba(255, 255, 255, 0.3);
                }
                QPushButton:pressed {
                    background: linear-gradient(135deg, rgba(37, 99, 235, 0.9), rgba(29, 78, 216, 0.9));
                }
            """
            )
        else:  # secondary
            self.setStyleSheet(
                """
                QPushButton {
                    background: rgba(255, 255, 255, 0.08);
                    border: 1px solid rgba(255, 255, 255, 0.18);
                    border-radius: 12px;
                    padding: 12px 24px;
                    font-family: 'Inter', sans-serif;
                    font-size: 14px;
                    font-weight: 500;
                    color: rgba(255, 255, 255, 0.9);
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.12);
                    border: 1px solid rgba(255, 255, 255, 0.28);
                }
                QPushButton:pressed {
                    background: rgba(255, 255, 255, 0.16);
                }
            """
            )

    def _setup_animations(self):
        """Setup premium micro-interactions."""
        if ENHANCED_UI_AVAILABLE:
            try:
                # Spring animation for button press
                self.press_animation = self.create_spring_animation(
                    self, b"geometry", damping=0.9, stiffness=200
                )
            except Exception as e:
                logger.warning(f"Could not setup button animations: {e}")
        else:
            # Fallback animation
            self.animation = QPropertyAnimation(self, b"geometry")
            self.animation.setDuration(200)
            self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def _setup_effects(self):
        """Setup visual effects."""
        if ENHANCED_UI_AVAILABLE:
            try:
                effect_manager = get_effect_manager()
                effect_manager.apply_contextual_shadow(self)
            except Exception as e:
                logger.warning(f"Could not apply button effects: {e}")

    def mousePressEvent(self, event):
        """Enhanced button press with spring feedback."""
        super().mousePressEvent(event)
        if ENHANCED_UI_AVAILABLE and hasattr(self, "animate_button_press"):
            self.animate_button_press(self)

    def enterEvent(self, event):
        """Enhanced hover enter."""
        super().enterEvent(event)
        # Add subtle glow effect on hover
        if ENHANCED_UI_AVAILABLE:
            try:
                effect_manager = get_effect_manager()
                edge_effect = effect_manager.apply_edge_lighting(self)
                edge_effect.start_glow(0.3)
            except Exception as e:
                logger.debug(f"Could not apply hover glow: {e}")

    def leaveEvent(self, event):
        """Enhanced hover leave."""
        super().leaveEvent(event)
        # Remove glow effect
        if ENHANCED_UI_AVAILABLE:
            try:
                effect_manager = get_effect_manager()
                effect_manager.remove_effects(self)
                self._setup_effects()  # Restore base effects
            except Exception as e:
                logger.debug(f"Could not remove hover glow: {e}")
