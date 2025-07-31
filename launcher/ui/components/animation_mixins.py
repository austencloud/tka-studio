#!/usr/bin/env python3
"""
Animation Mixins - Premium Micro-Interactions
=============================================

Reusable animation patterns for TKA Launcher components.
Implements premium 2025 micro-interactions with:
- Spring physics animations
- Staggered entrance effects
- Hover anticipation
- Launch feedback
- Magnetic snap effects

Architecture:
- AnimationMixin: Base animation functionality
- HoverAnimationMixin: Hover state animations
- EntranceAnimationMixin: Staggered entrance effects
- FeedbackAnimationMixin: User interaction feedback
- MagneticMixin: Magnetic snap effects
"""

import logging

from PyQt6.QtCore import (
    QEasingCurve,
    QObject,
    QParallelAnimationGroup,
    QPoint,
    QPropertyAnimation,
    QRect,
    QSequentialAnimationGroup,
    QTimer,
)
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget

logger = logging.getLogger(__name__)


class AnimationMixin:
    """
    Base animation mixin providing core animation functionality.

    Features:
    - Hardware-accelerated animations
    - Spring physics simulation
    - Animation state management
    - Performance optimization
    """

    def __init__(self):
        self._animations = {}
        self._animation_groups = {}
        self._is_animating = False

    def create_property_animation(
        self,
        target: QObject,
        property_name: bytes,
        duration: int = 300,
        easing: QEasingCurve.Type = QEasingCurve.Type.OutCubic,
    ) -> QPropertyAnimation:
        """Create a property animation with optimized settings."""
        animation = QPropertyAnimation(target, property_name)
        animation.setDuration(duration)
        animation.setEasingCurve(easing)

        # Store reference to prevent garbage collection
        anim_key = f"{target.__class__.__name__}_{property_name.decode()}"
        self._animations[anim_key] = animation

        return animation

    def create_spring_animation(
        self,
        target: QObject,
        property_name: bytes,
        damping: float = 0.8,
        stiffness: float = 100.0,
    ) -> QPropertyAnimation:
        """Create a spring physics animation."""
        animation = self.create_property_animation(target, property_name, duration=400)

        # Simulate spring physics with custom easing
        # This is a simplified spring curve - for true spring physics,
        # we'd need a custom QEasingCurve implementation
        animation.setEasingCurve(QEasingCurve.Type.OutElastic)

        return animation

    def create_stagger_group(
        self, animations: list[QPropertyAnimation], stagger_delay: int = 50
    ) -> QSequentialAnimationGroup:
        """Create a staggered animation group."""
        group = QSequentialAnimationGroup()

        for i, animation in enumerate(animations):
            if i > 0:
                # Add delay between animations
                delay_timer = QTimer()
                delay_timer.setSingleShot(True)
                delay_timer.timeout.connect(lambda: None)  # No-op
                QTimer.singleShot(stagger_delay * i, animation.start)

            group.addAnimation(animation)

        return group

    def stop_all_animations(self):
        """Stop all running animations."""
        for animation in self._animations.values():
            if animation.state() == QPropertyAnimation.State.Running:
                animation.stop()

        for group in self._animation_groups.values():
            if group.state() == QSequentialAnimationGroup.State.Running:
                group.stop()


class HoverAnimationMixin(AnimationMixin):
    """
    Hover animation mixin for smooth hover effects.

    Features:
    - Smooth scale transitions
    - Glow effects
    - Color temperature shifts
    - Anticipation animations
    """

    def __init__(self):
        super().__init__()
        self._hover_scale_animation = None
        self._hover_glow_animation = None
        self._is_hovered = False

    def setup_hover_animations(self, widget: QWidget):
        """Setup hover animations for a widget."""
        # Scale animation
        self._hover_scale_animation = self.create_spring_animation(
            widget, b"geometry", damping=0.7, stiffness=120
        )

        # Glow effect animation (using opacity effect)
        glow_effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(glow_effect)

        self._hover_glow_animation = self.create_property_animation(
            glow_effect, b"opacity", duration=250
        )

    def animate_hover_enter(self, widget: QWidget):
        """Animate hover enter state."""
        if self._is_hovered or not self._hover_scale_animation:
            return

        self._is_hovered = True

        # Scale up slightly
        current_rect = widget.geometry()
        hover_rect = QRect(
            current_rect.x() - 2,
            current_rect.y() - 2,
            current_rect.width() + 4,
            current_rect.height() + 4,
        )

        self._hover_scale_animation.setStartValue(current_rect)
        self._hover_scale_animation.setEndValue(hover_rect)
        self._hover_scale_animation.start()

        # Glow effect
        if self._hover_glow_animation:
            self._hover_glow_animation.setStartValue(1.0)
            self._hover_glow_animation.setEndValue(1.2)
            self._hover_glow_animation.start()

    def animate_hover_leave(self, widget: QWidget):
        """Animate hover leave state."""
        if not self._is_hovered or not self._hover_scale_animation:
            return

        self._is_hovered = False

        # Scale back to normal
        current_rect = widget.geometry()
        normal_rect = QRect(
            current_rect.x() + 2,
            current_rect.y() + 2,
            current_rect.width() - 4,
            current_rect.height() - 4,
        )

        self._hover_scale_animation.setStartValue(current_rect)
        self._hover_scale_animation.setEndValue(normal_rect)
        self._hover_scale_animation.start()

        # Remove glow
        if self._hover_glow_animation:
            self._hover_glow_animation.setStartValue(1.2)
            self._hover_glow_animation.setEndValue(1.0)
            self._hover_glow_animation.start()


class EntranceAnimationMixin(AnimationMixin):
    """
    Entrance animation mixin for staggered card appearances.

    Features:
    - Staggered fade-in effects
    - Slide-up animations
    - Scale entrance effects
    - Performance-optimized batching
    """

    def __init__(self):
        super().__init__()
        self._entrance_animations = []

    def create_entrance_animation(
        self, widget: QWidget, delay: int = 0, animation_type: str = "fade_slide"
    ) -> QParallelAnimationGroup:
        """Create an entrance animation for a widget."""
        group = QParallelAnimationGroup()

        if animation_type == "fade_slide":
            # Opacity animation
            opacity_effect = QGraphicsOpacityEffect()
            widget.setGraphicsEffect(opacity_effect)

            opacity_anim = self.create_property_animation(
                opacity_effect, b"opacity", duration=400
            )
            opacity_anim.setStartValue(0.0)
            opacity_anim.setEndValue(1.0)

            # Slide up animation
            original_pos = widget.pos()
            start_pos = QPoint(original_pos.x(), original_pos.y() + 20)

            slide_anim = self.create_property_animation(widget, b"pos", duration=400)
            slide_anim.setStartValue(start_pos)
            slide_anim.setEndValue(original_pos)

            group.addAnimation(opacity_anim)
            group.addAnimation(slide_anim)

        elif animation_type == "scale":
            # Scale animation
            scale_anim = self.create_spring_animation(
                widget, b"geometry", damping=0.6, stiffness=150
            )

            original_rect = widget.geometry()
            start_rect = QRect(
                original_rect.center().x() - 10, original_rect.center().y() - 10, 20, 20
            )

            scale_anim.setStartValue(start_rect)
            scale_anim.setEndValue(original_rect)

            group.addAnimation(scale_anim)

        # Add delay if specified
        if delay > 0:
            QTimer.singleShot(delay, group.start)

        return group

    def animate_staggered_entrance(
        self,
        widgets: list[QWidget],
        stagger_delay: int = 50,
        animation_type: str = "fade_slide",
    ):
        """Animate staggered entrance for multiple widgets."""
        self._entrance_animations.clear()

        for i, widget in enumerate(widgets):
            delay = i * stagger_delay
            animation = self.create_entrance_animation(widget, delay, animation_type)
            self._entrance_animations.append(animation)

        logger.info(f"🎬 Started staggered entrance for {len(widgets)} widgets")


class FeedbackAnimationMixin(AnimationMixin):
    """
    Feedback animation mixin for user interaction responses.

    Features:
    - Button press feedback
    - Launch pulse effects
    - Success/error state animations
    - Ripple effects
    """

    def __init__(self):
        super().__init__()
        self._feedback_animations = {}

    def animate_button_press(self, button: QWidget):
        """Animate button press with spring feedback."""
        press_anim = self.create_spring_animation(
            button, b"geometry", damping=0.9, stiffness=200
        )

        original_rect = button.geometry()
        pressed_rect = QRect(
            original_rect.x() + 1,
            original_rect.y() + 1,
            original_rect.width() - 2,
            original_rect.height() - 2,
        )

        press_anim.setStartValue(original_rect)
        press_anim.setEndValue(pressed_rect)

        # Return to normal after short delay
        def return_to_normal():
            return_anim = self.create_spring_animation(
                button, b"geometry", damping=0.8, stiffness=150
            )
            return_anim.setStartValue(pressed_rect)
            return_anim.setEndValue(original_rect)
            return_anim.start()

        press_anim.finished.connect(return_to_normal)
        press_anim.start()

    def animate_launch_pulse(self, widget: QWidget):
        """Animate launch pulse effect."""
        pulse_anim = self.create_property_animation(widget, b"geometry", duration=600)
        pulse_anim.setEasingCurve(QEasingCurve.Type.OutElastic)

        original_rect = widget.geometry()
        pulse_rect = QRect(
            original_rect.x() - 8,
            original_rect.y() - 8,
            original_rect.width() + 16,
            original_rect.height() + 16,
        )

        # Pulse out and back
        pulse_anim.setStartValue(original_rect)
        pulse_anim.setEndValue(pulse_rect)

        def pulse_back():
            back_anim = self.create_property_animation(
                widget, b"geometry", duration=400
            )
            back_anim.setStartValue(pulse_rect)
            back_anim.setEndValue(original_rect)
            back_anim.start()

        pulse_anim.finished.connect(pulse_back)
        pulse_anim.start()

        logger.info("🚀 Launch pulse animation started")


class MagneticMixin(AnimationMixin):
    """
    Magnetic interaction mixin for premium feel.

    Features:
    - Magnetic snap to mouse
    - Smooth follow animations
    - Distance-based attraction
    - Performance-optimized tracking
    """

    def __init__(self):
        super().__init__()
        self._magnetic_animation = None
        self._magnetic_enabled = True
        self._attraction_distance = 50

    def setup_magnetic_effect(self, widget: QWidget):
        """Setup magnetic effect for a widget."""
        self._magnetic_animation = self.create_property_animation(
            widget, b"pos", duration=200
        )
        self._magnetic_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def update_magnetic_position(self, widget: QWidget, mouse_pos: QPoint):
        """Update widget position based on mouse proximity."""
        if not self._magnetic_enabled or not self._magnetic_animation:
            return

        widget_center = widget.geometry().center()
        distance = (
            (mouse_pos.x() - widget_center.x()) ** 2
            + (mouse_pos.y() - widget_center.y()) ** 2
        ) ** 0.5

        if distance < self._attraction_distance:
            # Calculate magnetic offset
            attraction_strength = 1.0 - (distance / self._attraction_distance)
            offset_x = (mouse_pos.x() - widget_center.x()) * attraction_strength * 0.1
            offset_y = (mouse_pos.y() - widget_center.y()) * attraction_strength * 0.1

            new_pos = QPoint(
                widget.pos().x() + int(offset_x), widget.pos().y() + int(offset_y)
            )

            self._magnetic_animation.setStartValue(widget.pos())
            self._magnetic_animation.setEndValue(new_pos)
            self._magnetic_animation.start()

    def set_magnetic_enabled(self, enabled: bool):
        """Enable or disable magnetic effect."""
        self._magnetic_enabled = enabled

    def set_attraction_distance(self, distance: int):
        """Set the magnetic attraction distance."""
        self._attraction_distance = distance
