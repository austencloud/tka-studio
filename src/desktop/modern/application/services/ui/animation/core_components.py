"""
Core animation components for the modern fade system.
"""

from __future__ import annotations

import asyncio

from PyQt6.QtCore import QParallelAnimationGroup, QPropertyAnimation
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget

from desktop.modern.core.interfaces.animation_interfaces import (
    FadeOptions,
    IAnimationFactory,
    IGraphicsEffectManager,
)


class FadableOpacityEffect(QGraphicsOpacityEffect):
    """Custom opacity effect for fade animations."""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.in_animation = False


class GraphicsEffectManager(IGraphicsEffectManager):
    """Manages graphics effects lifecycle with automatic cleanup."""

    def __init__(self):
        self._managed_effects: dict[QWidget, QGraphicsOpacityEffect] = {}

    def apply_fade_effect(self, widget: QWidget) -> QGraphicsOpacityEffect:
        """Apply a fade effect to a widget, reusing existing effects when possible."""
        if not widget:
            raise ValueError("Widget cannot be None")

        # Check for existing effect
        existing_effect = widget.graphicsEffect()
        if existing_effect and isinstance(existing_effect, QGraphicsOpacityEffect):
            self._managed_effects[widget] = existing_effect
            return existing_effect

        # Create new effect
        effect = FadableOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        self._managed_effects[widget] = effect
        return effect

    def remove_effects(self, widgets: list[QWidget]) -> None:
        """Safely remove graphics effects from widgets."""
        for widget in widgets:
            if widget and hasattr(widget, "setGraphicsEffect"):
                try:
                    widget.setGraphicsEffect(None)
                    self._managed_effects.pop(widget, None)
                except RuntimeError:
                    # Widget was deleted, just remove from tracking
                    self._managed_effects.pop(widget, None)

    def cleanup_all(self) -> None:
        """Cleanup all managed effects."""
        widgets_to_clean = list(self._managed_effects.keys())
        self.remove_effects(widgets_to_clean)
        self._managed_effects.clear()


class AnimationFactory(IAnimationFactory):
    """Factory for creating Qt animations with consistent configuration."""

    def create_opacity_animation(
        self,
        effect: QGraphicsOpacityEffect,
        options: FadeOptions,
        start_value: float,
        end_value: float,
    ) -> QPropertyAnimation:
        """Create a properly configured opacity animation."""
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(options.duration)
        animation.setStartValue(start_value)
        animation.setEndValue(end_value)
        animation.setEasingCurve(options.easing.value)
        return animation

    def create_parallel_group(self) -> QParallelAnimationGroup:
        """Create a parallel animation group."""
        return QParallelAnimationGroup()


class AnimationAwaiter:
    """Utility class to convert Qt animations to async/await pattern."""

    @staticmethod
    async def wait_for_animation(animation) -> None:
        """Wait for a Qt animation to complete using asyncio."""
        future = asyncio.Future()

        def on_finished():
            if not future.done():
                future.set_result(None)

        animation.finished.connect(on_finished)

        # If animation is already finished, complete immediately
        if hasattr(animation, "state") and animation.state() == animation.State.Stopped:
            return

        await future
