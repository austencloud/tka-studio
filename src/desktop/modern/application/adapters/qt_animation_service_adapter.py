"""
Qt Adapter for Animation Service

This adapter bridges the framework-agnostic animation service with Qt's
animation system, maintaining backward compatibility while enabling
framework independence.
"""

from __future__ import annotations

import logging
from typing import Any

from PyQt6.QtCore import QObject, QPropertyAnimation, QTimer, pyqtSignal
from PyQt6.QtWidgets import QWidget

from desktop.modern.application.services.core.animation_service import (
    AnimationCommand,
    AnimationType,
    EasingType,
    create_animation_service,
)


logger = logging.getLogger(__name__)


class QtAnimationServiceAdapter(QObject):
    """
    Qt adapter for animation service.

    Bridges the framework-agnostic core animation service with Qt's
    QPropertyAnimation system, maintaining backward compatibility.
    """

    # Signals for animation events
    animation_started = pyqtSignal(str)  # command_id
    animation_finished = pyqtSignal(str)  # command_id
    animation_progress = pyqtSignal(str, float)  # command_id, progress

    def __init__(self, parent=None):
        """Initialize the adapter with core services."""
        super().__init__(parent)

        # Initialize core service (framework-agnostic)
        self._core_service = create_animation_service()

        # Qt-specific animation management
        self._active_animations: dict[str, QPropertyAnimation] = {}
        self._widget_references: dict[str, QWidget] = {}
        self._timers: dict[str, QTimer] = {}

        # Performance tracking
        self._animation_count = 0

        logger.debug("🎬 [QT_ANIMATION_ADAPTER] Initialized Qt animation adapter")

    def animate_widget(
        self,
        widget: QWidget,
        property_name: str,
        start_value: Any,
        end_value: Any,
        duration: int,
        easing_curve=None,
    ) -> str:
        """
        Animate a Qt widget property (legacy interface).

        This maintains compatibility with existing Qt animation code
        while using the framework-agnostic service internally.
        """
        try:
            # Generate unique target ID
            widget_id = f"widget_{id(widget)}"
            self._widget_references[widget_id] = widget

            # Convert Qt parameters to core service format
            animation_type = self._map_property_to_animation_type(property_name)
            duration_seconds = duration / 1000.0  # Qt uses milliseconds

            start_values = {property_name: start_value}
            end_values = {property_name: end_value}

            # Create animation command using core service
            command = self._core_service.create_animation_command(
                target_id=widget_id,
                animation_type=animation_type,
                duration=duration_seconds,
                start_values=start_values,
                end_values=end_values,
                easing=EasingType.EASE_IN_OUT,  # Default easing
                metadata={
                    "qt_property": property_name,
                    "qt_duration": duration,
                    "qt_easing": str(easing_curve) if easing_curve else None,
                },
            )

            # Execute animation using Qt
            self._execute_qt_animation(command, widget, property_name, easing_curve)

            self._animation_count += 1
            logger.debug(
                f"🎬 [QT_ANIMATION_ADAPTER] Started widget animation: {command.command_id}"
            )

            return command.command_id

        except Exception as e:
            logger.exception(f"❌ [QT_ANIMATION_ADAPTER] Failed to animate widget: {e}")
            return ""

    def stop_animation(self, animation_id: str):
        """Stop a running animation."""
        try:
            if animation_id in self._active_animations:
                animation = self._active_animations[animation_id]
                animation.stop()
                del self._active_animations[animation_id]
                logger.debug(
                    f"🎬 [QT_ANIMATION_ADAPTER] Stopped animation: {animation_id}"
                )

            if animation_id in self._timers:
                timer = self._timers[animation_id]
                timer.stop()
                del self._timers[animation_id]

        except Exception as e:
            logger.exception(f"❌ [QT_ANIMATION_ADAPTER] Failed to stop animation: {e}")

    def _execute_qt_animation(
        self,
        command: AnimationCommand,
        widget: QWidget,
        property_name: str,
        easing_curve=None,
    ):
        """Execute animation command using Qt's QPropertyAnimation."""
        try:
            # Handle delay if present
            if command.delay > 0:
                timer = QTimer()
                timer.timeout.connect(
                    lambda: self._start_qt_property_animation(
                        command, widget, property_name, easing_curve
                    )
                )
                timer.start(int(command.delay * 1000))
                self._timers[command.command_id] = timer
            else:
                self._start_qt_property_animation(
                    command, widget, property_name, easing_curve
                )

        except Exception as e:
            logger.exception(
                f"❌ [QT_ANIMATION_ADAPTER] Failed to execute Qt animation: {e}"
            )

    def _start_qt_property_animation(
        self,
        command: AnimationCommand,
        widget: QWidget,
        property_name: str,
        easing_curve=None,
    ):
        """Start Qt property animation."""
        try:
            # Handle special properties
            if property_name == "opacity":
                target = widget.graphicsEffect() or widget
            else:
                target = widget

            # Create Qt animation
            animation = QPropertyAnimation(target, property_name.encode("utf-8"))
            animation.setDuration(int(command.duration * 1000))

            # Set values
            start_val = command.start_values.get(property_name)
            end_val = command.end_values.get(property_name)

            if start_val is not None:
                animation.setStartValue(start_val)
            if end_val is not None:
                animation.setEndValue(end_val)

            # Set easing curve
            if easing_curve:
                animation.setEasingCurve(easing_curve)

            # Connect signals
            animation.started.connect(
                lambda: self.animation_started.emit(command.command_id)
            )
            animation.finished.connect(
                lambda: self._on_animation_finished(command.command_id)
            )
            animation.valueChanged.connect(
                lambda value: self._on_animation_progress(
                    command.command_id, animation.currentTime(), animation.duration()
                )
            )

            # Start animation
            self._active_animations[command.command_id] = animation
            animation.start()

        except Exception as e:
            logger.exception(
                f"❌ [QT_ANIMATION_ADAPTER] Failed to start Qt property animation: {e}"
            )

    def _on_animation_finished(self, animation_id: str):
        """Handle animation finished."""
        try:
            if animation_id in self._active_animations:
                del self._active_animations[animation_id]

            self.animation_finished.emit(animation_id)
            logger.debug(
                f"🎬 [QT_ANIMATION_ADAPTER] Animation finished: {animation_id}"
            )

        except Exception as e:
            logger.exception(
                f"❌ [QT_ANIMATION_ADAPTER] Error handling animation finished: {e}"
            )

    def _on_animation_progress(
        self, animation_id: str, current_time: int, duration: int
    ):
        """Handle animation progress."""
        try:
            if duration > 0:
                progress = current_time / duration
                self.animation_progress.emit(animation_id, progress)

        except Exception as e:
            logger.exception(
                f"❌ [QT_ANIMATION_ADAPTER] Error handling animation progress: {e}"
            )

    def _map_property_to_animation_type(self, property_name: str) -> AnimationType:
        """Map Qt property name to animation type."""
        property_map = {
            "opacity": AnimationType.OPACITY,
            "pos": AnimationType.SLIDE,
            "geometry": AnimationType.SLIDE,
            "size": AnimationType.SCALE,
            "rotation": AnimationType.ROTATE,
        }
        return property_map.get(property_name, AnimationType.CUSTOM)

    def get_performance_stats(self) -> dict[str, Any]:
        """Get performance statistics."""
        core_stats = self._core_service.get_performance_stats()
        return {
            **core_stats,
            "qt_animations": self._animation_count,
            "active_animations": len(self._active_animations),
            "active_timers": len(self._timers),
        }
