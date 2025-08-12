"""
Qt/PyQt6 adapters for the framework-agnostic animation system.
These adapters connect the core animation engine to Qt widgets.
"""

from __future__ import annotations

import asyncio
from typing import Any

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QStackedWidget, QWidget

from desktop.modern.core.interfaces.animation_core_interfaces import (
    AnimationConfig,
    AnimationTarget,
    IAnimationRenderer,
    IAnimationScheduler,
    ITargetAdapter,
)


class QtTargetAdapter(ITargetAdapter):
    """Adapter for converting Qt widgets to AnimationTarget."""

    def adapt_target(self, framework_target: Any) -> AnimationTarget:
        """Convert Qt widget to AnimationTarget."""
        if not isinstance(framework_target, QWidget):
            raise ValueError(f"Expected QWidget, got {type(framework_target)}")

        widget = framework_target

        # Create unique ID for the widget
        widget_id = f"qt_widget_{id(widget)}"

        # Extract widget properties
        properties = {
            "class_name": widget.__class__.__name__,
            "object_name": widget.objectName(),
            "visible": widget.isVisible(),
            "enabled": widget.isEnabled(),
            "geometry": {
                "x": widget.x(),
                "y": widget.y(),
                "width": widget.width(),
                "height": widget.height(),
            },
        }

        # Store reference to actual widget for later use
        properties["_qt_widget_ref"] = widget

        return AnimationTarget(
            id=widget_id, element_type="qt_widget", properties=properties
        )

    def apply_animation(
        self, target: AnimationTarget, property_name: str, value: Any
    ) -> bool:
        """Apply animation value to the Qt widget."""
        widget = target.properties.get("_qt_widget_ref")
        if not widget or not isinstance(widget, QWidget):
            return False

        try:
            if property_name == "opacity":
                self._apply_opacity(widget, value)
            elif property_name == "x":
                widget.move(int(value), widget.y())
            elif property_name == "y":
                widget.move(widget.x(), int(value))
            elif property_name == "width":
                widget.resize(int(value), widget.height())
            elif property_name == "height":
                widget.resize(widget.width(), int(value))
            elif property_name == "scale":
                self._apply_scale(widget, value)
            # Try to set as widget property
            elif hasattr(widget, property_name):
                setattr(widget, property_name, value)
            else:
                return False

            return True
        except Exception as e:
            print(f"Error applying animation property {property_name}: {e}")
            return False

    def _apply_opacity(self, widget: QWidget, opacity: float) -> None:
        """Apply opacity using graphics effect."""
        effect = widget.graphicsEffect()

        if not effect or not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)

        effect.setOpacity(opacity)

    def _apply_scale(self, widget: QWidget, scale: float) -> None:
        """Apply scale transform (simplified implementation)."""
        # Note: Qt doesn't have simple scale property like web CSS
        # This is a simplified implementation that scales size
        original_size = widget.sizeHint()
        if original_size.isValid():
            new_width = int(original_size.width() * scale)
            new_height = int(original_size.height() * scale)
            widget.resize(new_width, new_height)


class QtAnimationRenderer(IAnimationRenderer):
    """Qt-specific animation renderer."""

    def __init__(self, target_adapter: QtTargetAdapter):
        self.target_adapter = target_adapter
        self._supported_properties = {"opacity", "x", "y", "width", "height", "scale"}

    async def render_frame(
        self, target: AnimationTarget, property_name: str, value: Any, progress: float
    ) -> bool:
        """Render a single animation frame."""
        return self.target_adapter.apply_animation(target, property_name, value)

    def supports_property(self, property_name: str) -> bool:
        """Check if this renderer supports the given property."""
        return property_name in self._supported_properties


class QtAnimationScheduler(IAnimationScheduler):
    """Qt-specific animation scheduler using QTimer."""

    def __init__(self, fps: int = 60):
        self.fps = fps
        self.frame_interval_ms = int(1000 / fps)
        self._timers: dict[str, QTimer] = {}

    async def schedule_animation(
        self, animation_id: str, config: AnimationConfig, frame_callback: callable
    ) -> None:
        """Schedule animation frames using QTimer."""
        timer = QTimer()
        self._timers[animation_id] = timer

        start_time = self.get_current_time()

        def timer_callback():
            current_time = self.get_current_time()
            elapsed = current_time - start_time

            # Calculate progress
            if elapsed < config.delay:
                progress = 0.0
            else:
                animation_elapsed = elapsed - config.delay
                if animation_elapsed >= config.duration:
                    progress = 1.0
                else:
                    progress = (
                        animation_elapsed / config.duration
                        if config.duration > 0
                        else 1.0
                    )

            # Call frame callback
            frame_callback(progress)

            # Stop timer if animation is complete
            if progress >= 1.0:
                timer.stop()
                self._timers.pop(animation_id, None)

        timer.timeout.connect(timer_callback)
        timer.start(self.frame_interval_ms)

        # Create future that completes when animation finishes
        future = asyncio.Future()

        def on_finished():
            if not future.done():
                future.set_result(None)

        # Connect timer finished signal to future completion
        original_stop = timer.stop

        def stop_with_callback():
            original_stop()
            on_finished()

        timer.stop = stop_with_callback

        await future

    def get_current_time(self) -> float:
        """Get current time in seconds."""
        import time

        return time.time()


class QtStackWidgetAdapter:
    """Specialized adapter for QStackedWidget animations."""

    def __init__(self, target_adapter: QtTargetAdapter):
        self.target_adapter = target_adapter

    def prepare_stack_transition(
        self, stack: QStackedWidget, new_index: int
    ) -> tuple[AnimationTarget | None, AnimationTarget | None]:
        """Prepare stack transition and return current/next targets."""
        current_widget = stack.currentWidget()
        next_widget = stack.widget(new_index)

        if not current_widget or not next_widget or stack.currentIndex() == new_index:
            return None, None

        current_target = self.target_adapter.adapt_target(current_widget)
        next_target = self.target_adapter.adapt_target(next_widget)

        return current_target, next_target

    def switch_stack_index(self, stack: QStackedWidget, new_index: int) -> None:
        """Switch the stack to the new index."""
        stack.setCurrentIndex(new_index)


class QtGraphicsEffectManager:
    """Manager for Qt graphics effects used in animations."""

    def __init__(self):
        self._managed_effects: dict[QWidget, QGraphicsOpacityEffect] = {}

    def ensure_opacity_effect(self, widget: QWidget) -> QGraphicsOpacityEffect:
        """Ensure widget has an opacity effect and return it."""
        if widget in self._managed_effects:
            return self._managed_effects[widget]

        existing_effect = widget.graphicsEffect()
        if existing_effect and isinstance(existing_effect, QGraphicsOpacityEffect):
            self._managed_effects[widget] = existing_effect
            return existing_effect

        # Create new effect
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        self._managed_effects[widget] = effect
        return effect

    def remove_effects(self, widgets: list[QWidget]) -> None:
        """Remove graphics effects from widgets."""
        for widget in widgets:
            if widget and hasattr(widget, "setGraphicsEffect"):
                try:
                    widget.setGraphicsEffect(None)
                    self._managed_effects.pop(widget, None)
                except RuntimeError:
                    # Widget was deleted
                    self._managed_effects.pop(widget, None)

    def cleanup_all(self) -> None:
        """Clean up all managed effects."""
        widgets_to_clean = list(self._managed_effects.keys())
        self.remove_effects(widgets_to_clean)
        self._managed_effects.clear()


class QtSettingsIntegration:
    """Integration with Qt settings systems."""

    def __init__(self, settings_coordinator=None):
        self.settings_coordinator = settings_coordinator
        self._defaults = {
            "animations_enabled": True,
            "default_duration": 0.25,
            "default_easing": "ease-in-out",
            "reduced_motion": False,
        }

    def get_animations_enabled(self) -> bool:
        """Get animations enabled setting."""
        if self.settings_coordinator:
            return self.settings_coordinator.get_setting(
                "ui.animations.enabled", self._defaults["animations_enabled"]
            )
        return self._defaults["animations_enabled"]

    def get_default_duration(self) -> float:
        """Get default animation duration."""
        if self.settings_coordinator:
            return self.settings_coordinator.get_setting(
                "ui.animations.default_duration", self._defaults["default_duration"]
            )
        return self._defaults["default_duration"]

    def get_reduced_motion(self) -> bool:
        """Check if user prefers reduced motion."""
        if self.settings_coordinator:
            return self.settings_coordinator.get_setting(
                "ui.animations.reduced_motion", self._defaults["reduced_motion"]
            )
        return self._defaults["reduced_motion"]


def create_qt_animation_components(settings_coordinator=None):
    """Factory function to create all Qt animation components."""
    target_adapter = QtTargetAdapter()
    renderer = QtAnimationRenderer(target_adapter)
    scheduler = QtAnimationScheduler(fps=60)
    stack_adapter = QtStackWidgetAdapter(target_adapter)
    effect_manager = QtGraphicsEffectManager()
    settings_integration = QtSettingsIntegration(settings_coordinator)

    return {
        "target_adapter": target_adapter,
        "renderer": renderer,
        "scheduler": scheduler,
        "stack_adapter": stack_adapter,
        "effect_manager": effect_manager,
        "settings_integration": settings_integration,
    }
