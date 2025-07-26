"""
TransitionAnimator

Handles smooth transitions between panels in the construct tab.
Manages fade animations and graphics effects cleanup.
"""

from typing import Callable, Optional

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, QTimer
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QStackedWidget, QWidget


class TransitionAnimator:
    """
    Handles smooth transitions between panels.

    Responsibilities:
    - Managing fade in/out animations
    - Cleaning up graphics effects to prevent QPainter conflicts
    - Handling fallback direct transitions
    - Managing transition state
    """

    def __init__(self):
        self._is_transitioning = False
        self._current_animation = None

    def is_transitioning(self) -> bool:
        """Check if a transition is currently in progress."""
        return self._is_transitioning

    def fade_to_panel(
        self,
        stack: QStackedWidget,
        target_index: int,
        target_name: str,
        on_complete: Optional[Callable] = None,
    ):
        """
        Perform smooth fade transition to target panel.

        Args:
            stack: The QStackedWidget containing the panels
            target_index: Index of the target panel
            target_name: Name of the target panel for logging
            on_complete: Optional callback to call when transition completes
        """
        if self._is_transitioning:
            print(
                f"🎭 [FADE] Skipping transition to {target_name} - already transitioning"
            )
            return

        if stack.currentIndex() == target_index:
            print(f"🎭 [FADE] Skipping transition to {target_name} - already current")
            return

        current_widget = stack.currentWidget()
        next_widget = stack.widget(target_index)

        if not current_widget or not next_widget:
            print(f"🎭 [FADE] Invalid widgets for transition to {target_name}")
            self._fallback_transition(stack, target_index, target_name, on_complete)
            return

        self._is_transitioning = True
        print(f"🎭 [FADE] Starting fade transition to {target_name}")

        # Clean up graphics effects before starting animation
        self._clear_graphics_effects([current_widget, next_widget])

        # Disable pictograph updates during transition
        self._disable_pictograph_updates(current_widget, True)

        def on_fade_out_finished():
            print(f"🎭 [FADE] Fade out complete, switching to {target_name}")

            # Clean up again before switching
            self._clear_graphics_effects([current_widget, next_widget])

            # Switch to target panel
            stack.setCurrentIndex(target_index)

            # Re-enable pictograph updates
            self._disable_pictograph_updates(current_widget, False)

            # Fade in the new panel
            self._fade_in_widget(next_widget, target_name, on_complete)

        # Start fade out animation
        self._fade_out_widget(current_widget, on_fade_out_finished)

    def _fade_out_widget(self, widget: QWidget, callback: Callable):
        """Fade out a widget using QPropertyAnimation."""
        try:
            effect = self._ensure_opacity_effect(widget)
            effect.setOpacity(1.0)

            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(200)
            animation.setStartValue(1.0)
            animation.setEndValue(0.0)
            animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

            self._current_animation = animation

            def on_animation_finished():
                self._clear_graphics_effects([widget])
                callback()

            animation.finished.connect(on_animation_finished)
            animation.start()

        except Exception as e:
            print(f"❌ [FADE] Fade out animation failed: {e}")
            self._clear_graphics_effects([widget])
            callback()

    def _fade_in_widget(
        self, widget: QWidget, target_name: str, on_complete: Optional[Callable]
    ):
        """Fade in a widget using QPropertyAnimation."""
        try:
            effect = self._ensure_opacity_effect(widget)
            effect.setOpacity(0.0)

            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(200)
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)
            animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

            def on_animation_complete():
                print(f"✅ [FADE] Fade transition completed to {target_name}")
                self._clear_graphics_effects([widget])
                self._reset_transition_state()
                if on_complete:
                    on_complete()

            self._current_animation = animation
            animation.finished.connect(on_animation_complete)
            animation.start()

        except Exception as e:
            print(f"❌ [FADE] Fade in animation failed for {target_name}: {e}")
            self._clear_graphics_effects([widget])
            self._reset_transition_state()
            if on_complete:
                on_complete()

    def _ensure_opacity_effect(self, widget: QWidget) -> QGraphicsOpacityEffect:
        """Ensure widget has an opacity effect."""
        effect = widget.graphicsEffect()
        if effect and isinstance(effect, QGraphicsOpacityEffect):
            return effect

        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        return effect

    def _clear_graphics_effects(self, widgets: list[QWidget]):
        """
        Recursively clear graphics effects from widgets and all their children.
        This prevents QPainter conflicts with complex widgets.
        """
        for widget in widgets:
            if widget and hasattr(widget, "setGraphicsEffect"):
                self._remove_all_graphics_effects_recursive(widget)

    def _remove_all_graphics_effects_recursive(self, widget: QWidget):
        """Recursively remove graphics effects from widget and all child widgets."""
        try:
            if widget is None or not hasattr(widget, "setGraphicsEffect"):
                return

            widget.setGraphicsEffect(None)

            if hasattr(widget, "findChildren"):
                for child in widget.findChildren(QWidget):
                    if child and child.graphicsEffect():
                        try:
                            child.setGraphicsEffect(None)
                        except (RuntimeError, AttributeError):
                            pass

        except (RuntimeError, AttributeError):
            pass

    def _disable_pictograph_updates(self, widget: QWidget, disable: bool):
        """Temporarily disable pictograph updates to prevent QPainter conflicts."""
        try:
            if hasattr(widget, "content") and hasattr(widget.content, "apply_sizing"):
                if disable:
                    if not hasattr(widget.content, "_original_apply_sizing"):
                        widget.content._original_apply_sizing = (
                            widget.content.apply_sizing
                        )
                        widget.content.apply_sizing = lambda *args, **kwargs: None
                else:
                    if hasattr(widget.content, "_original_apply_sizing"):
                        widget.content.apply_sizing = (
                            widget.content._original_apply_sizing
                        )
                        delattr(widget.content, "_original_apply_sizing")
        except Exception as e:
            print(f"❌ [FADE] Error managing pictograph updates: {e}")

    def _fallback_transition(
        self,
        stack: QStackedWidget,
        target_index: int,
        target_name: str,
        on_complete: Optional[Callable],
    ):
        """Fallback to direct transition if animations fail."""
        print(f"🔄 [FALLBACK] Using direct transition to {target_name}")
        stack.setCurrentIndex(target_index)
        print(f"✅ [FALLBACK] Direct transition completed to {target_name}")

        def complete_callback():
            self._reset_transition_state()
            if on_complete:
                on_complete()

        QTimer.singleShot(250, complete_callback)

    def _reset_transition_state(self):
        """Reset the transition state."""
        self._is_transitioning = False
        self._current_animation = None
