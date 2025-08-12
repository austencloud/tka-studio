"""
Qt-specific implementations of animation protocols.

This module provides adapters that wrap Qt animation classes to implement
the platform-agnostic animation protocols, enabling seamless integration
with the existing Qt desktop infrastructure.
"""

from __future__ import annotations

from typing import Any

from PyQt6.QtCore import QParallelAnimationGroup, QPropertyAnimation
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QStackedWidget

from desktop.modern.core.types.animation import (
    PropertyAnimation,
)


class QtStackAdapter:
    """Adapter for Qt stack widgets to implement StackContainer protocol."""

    def __init__(self, qt_stack: QStackedWidget):
        """Initialize with a Qt stacked widget.

        Args:
            qt_stack: The QStackedWidget to wrap
        """
        self._qt_stack = qt_stack

    def get_current_index(self) -> int:
        """Get the index of the currently visible widget."""
        return self._qt_stack.currentIndex()

    def set_current_index(self, index: int) -> None:
        """Set which widget should be visible by index."""
        self._qt_stack.setCurrentIndex(index)

    def get_widget_at(self, index: int) -> Any:
        """Get the widget at the specified index."""
        return self._qt_stack.widget(index)

    def get_widget_count(self) -> int:
        """Get the total number of widgets in the stack."""
        return self._qt_stack.count()


class QtOpacityEffectAdapter:
    """Adapter for Qt opacity effects to implement OpacityEffect protocol."""

    def __init__(self, qt_effect: QGraphicsOpacityEffect):
        """Initialize with a Qt graphics opacity effect.

        Args:
            qt_effect: The QGraphicsOpacityEffect to wrap
        """
        self._qt_effect = qt_effect

    def get_opacity(self) -> float:
        """Get the current opacity value (0.0 to 1.0)."""
        return self._qt_effect.opacity()

    def set_opacity(self, opacity: float) -> None:
        """Set the opacity value (0.0 to 1.0)."""
        self._qt_effect.setOpacity(opacity)


class QtPropertyAnimationAdapter:
    """Adapter for Qt property animations to implement PropertyAnimation protocol."""

    def __init__(self, qt_animation: QPropertyAnimation):
        """Initialize with a Qt property animation.

        Args:
            qt_animation: The QPropertyAnimation to wrap
        """
        self._qt_animation = qt_animation

    def start(self) -> None:
        """Start the animation."""
        self._qt_animation.start()

    def stop(self) -> None:
        """Stop the animation."""
        self._qt_animation.stop()

    def set_duration(self, duration: int) -> None:
        """Set the animation duration in milliseconds."""
        self._qt_animation.setDuration(duration)

    def set_start_value(self, value: Any) -> None:
        """Set the starting value for the animated property."""
        self._qt_animation.setStartValue(value)

    def set_end_value(self, value: Any) -> None:
        """Set the ending value for the animated property."""
        self._qt_animation.setEndValue(value)


class QtAnimationGroupAdapter:
    """Adapter for Qt animation groups to implement AnimationGroup protocol."""

    def __init__(self, qt_group: QParallelAnimationGroup):
        """Initialize with a Qt parallel animation group.

        Args:
            qt_group: The QParallelAnimationGroup to wrap
        """
        self._qt_group = qt_group

    def add_animation(self, animation: PropertyAnimation) -> None:
        """Add an animation to the group.

        Args:
            animation: Animation to add (should be QtPropertyAnimationAdapter)
        """
        if isinstance(animation, QtPropertyAnimationAdapter):
            self._qt_group.addAnimation(animation._qt_animation)
        else:
            raise TypeError(
                f"Expected QtPropertyAnimationAdapter, got {type(animation)}"
            )

    def start(self) -> None:
        """Start all animations in the group."""
        self._qt_group.start()

    def stop(self) -> None:
        """Stop all animations in the group."""
        self._qt_group.stop()


# Factory functions for creating adapters
