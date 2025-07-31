"""
Reliable Effects System - Proven Qt Visual Effects
=================================================

Implements reliable visual effects using only standard QGraphicsEffect
classes that are guaranteed to work in PyQt6.
"""

from typing import Optional

from PyQt6.QtCore import QEasingCurve, QObject, QPropertyAnimation
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QWidget


class ReliableShadowManager(QObject):
    """Manages drop shadow effects reliably."""

    def __init__(self):
        super().__init__()
        self.active_shadows = {}  # widget_id -> effect

    def apply_card_shadow(self, widget: QWidget) -> QGraphicsDropShadowEffect:
        """Apply reliable card shadow."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 4)

        widget.setGraphicsEffect(shadow)
        self.active_shadows[id(widget)] = shadow
        return shadow

    def apply_hover_shadow(
        self, widget: QWidget
    ) -> Optional[QGraphicsDropShadowEffect]:
        """Apply hover state shadow."""
        shadow = self.active_shadows.get(id(widget))
        if shadow:
            # Animate existing shadow
            self._animate_shadow_change(shadow, blur=20, offset=(0, 8), opacity=70)
        return shadow

    def apply_pressed_shadow(
        self, widget: QWidget
    ) -> Optional[QGraphicsDropShadowEffect]:
        """Apply pressed state shadow."""
        shadow = self.active_shadows.get(id(widget))
        if shadow:
            self._animate_shadow_change(shadow, blur=8, offset=(0, 2), opacity=30)
        return shadow

    def reset_shadow(self, widget: QWidget) -> Optional[QGraphicsDropShadowEffect]:
        """Reset to default shadow."""
        shadow = self.active_shadows.get(id(widget))
        if shadow:
            self._animate_shadow_change(shadow, blur=15, offset=(0, 4), opacity=50)
        return shadow

    def apply_glow(
        self, widget: QWidget, color: QColor
    ) -> Optional[QGraphicsDropShadowEffect]:
        """Apply glow effect using shadow."""
        shadow = self.active_shadows.get(id(widget))
        if shadow:
            self._animate_shadow_change(shadow, blur=12, offset=(0, 0), color=color)
        return shadow

    def _animate_shadow_change(
        self,
        shadow: QGraphicsDropShadowEffect,
        blur: int,
        offset: tuple,
        opacity: Optional[int] = None,
        color: Optional[QColor] = None,
    ):
        """Animate shadow property changes."""
        # Note: QGraphicsDropShadowEffect properties are not animatable
        # So we do instant changes - still looks good
        shadow.setBlurRadius(blur)
        shadow.setOffset(*offset)
        if opacity is not None:
            current_color = shadow.color()
            new_color = QColor(
                current_color.red(),
                current_color.green(),
                current_color.blue(),
                opacity,
            )
            shadow.setColor(new_color)
        if color is not None:
            shadow.setColor(color)

    def remove_effects(self, widget: QWidget):
        """Remove all effects from widget."""
        widget.setGraphicsEffect(None)
        if id(widget) in self.active_shadows:
            del self.active_shadows[id(widget)]


class ReliableAnimationManager:
    """Manages reliable animations using proven Qt patterns."""

    @staticmethod
    def smooth_hover_scale(
        widget: QWidget, scale_factor: float = 1.02
    ) -> QPropertyAnimation:
        """Create smooth hover scale animation."""
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(200)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        original = widget.geometry()
        center = original.center()

        # Calculate scaled geometry
        new_width = int(original.width() * scale_factor)
        new_height = int(original.height() * scale_factor)
        new_x = center.x() - new_width // 2
        new_y = center.y() - new_height // 2

        scaled = original.__class__(new_x, new_y, new_width, new_height)

        animation.setStartValue(original)
        animation.setEndValue(scaled)

        return animation

    @staticmethod
    def smooth_fade(widget: QWidget, fade_in: bool = True) -> QPropertyAnimation:
        """Create smooth fade animation."""
        if not widget.graphicsEffect():
            effect = QGraphicsOpacityEffect()
            widget.setGraphicsEffect(effect)

        effect = widget.graphicsEffect()
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(300)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        if fade_in:
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)
        else:
            animation.setStartValue(1.0)
            animation.setEndValue(0.0)

        return animation

    @staticmethod
    def button_press_feedback(button: QWidget) -> QPropertyAnimation:
        """Create reliable button press animation."""
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(100)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        original = button.geometry()
        pressed = original.adjusted(1, 1, -2, -2)  # Shrink by 1px on all sides

        animation.setStartValue(original)
        animation.setEndValue(pressed)

        # Auto-return to normal
        def return_to_normal():
            return_anim = QPropertyAnimation(button, b"geometry")
            return_anim.setDuration(100)
            return_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            return_anim.setStartValue(pressed)
            return_anim.setEndValue(original)
            return_anim.start()

        animation.finished.connect(return_to_normal)
        return animation


# Global managers
_shadow_manager = ReliableShadowManager()
_animation_manager = ReliableAnimationManager()


def get_shadow_manager() -> ReliableShadowManager:
    """Get the global shadow manager."""
    return _shadow_manager


def get_animation_manager() -> ReliableAnimationManager:
    """Get the global animation manager."""
    return _animation_manager
