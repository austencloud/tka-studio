"""
OptionPickerAnimator

Handles smooth fade animations for option picker content.
Manages fade transitions and graphics effects cleanup.
"""

from __future__ import annotations

from collections.abc import Callable

from PyQt6.QtCore import QParallelAnimationGroup, QPropertyAnimation, QTimer
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget


class OptionPickerAnimator:
    """
    Handles animations for option picker content.

    Responsibilities:
    - Managing fade in/out animations for pictographs
    - Cleaning up graphics effects to prevent QPainter conflicts
    - Handling animation timing and callbacks
    - Managing transition state
    """

    def __init__(self, parent: QWidget):
        self._parent = parent
        self._is_animating = False
        self._pending_fade_callback: Callable | None = None
        self._pending_fade_frames: list[QWidget] = []

    def is_animating(self) -> bool:
        """Check if an animation is currently in progress."""
        return self._is_animating

    def fade_out_and_update(
        self,
        pictograph_frames: list[QWidget],
        update_callback: Callable,
        fade_in_callback: Callable | None = None,
    ) -> None:
        """
        Fade out pictographs, call update callback, then fade in new content.

        Args:
            pictograph_frames: List of pictograph frames to fade out
            update_callback: Function to call after fade out completes
            fade_in_callback: Optional function to call after fade in completes
        """
        if self._is_animating:
            print("🎭 [ANIMATOR] Animation already in progress, skipping")
            return

        if not pictograph_frames:
            print("🎭 [ANIMATOR] No frames to animate, calling update directly")
            update_callback()
            return

        self._is_animating = True
        self._pending_fade_callback = fade_in_callback

        try:
            # Create fade out animation group
            fade_out_group = QParallelAnimationGroup(self._parent)

            for frame in pictograph_frames:
                # Ensure opacity effect exists
                if not frame.graphicsEffect():
                    effect = QGraphicsOpacityEffect()
                    effect.setOpacity(1.0)
                    frame.setGraphicsEffect(effect)

                # Create fade out animation
                animation = QPropertyAnimation(frame.graphicsEffect(), b"opacity")
                animation.setDuration(200)
                animation.setStartValue(1.0)
                animation.setEndValue(0.0)
                fade_out_group.addAnimation(animation)

            def on_fade_out_complete():
                # Small delay to ensure fade out animation fully completes
                QTimer.singleShot(
                    10,
                    lambda: self._complete_fade_transition(
                        pictograph_frames, update_callback
                    ),
                )

            fade_out_group.finished.connect(on_fade_out_complete)
            fade_out_group.start()

        except Exception as e:
            print(f"❌ [ANIMATOR] Fade out failed: {e}")
            self._is_animating = False
            update_callback()

    def _complete_fade_transition(
        self, old_frames: list[QWidget], update_callback: Callable
    ):
        """Complete the fade transition after fade out is done."""
        try:
            # Clear graphics effects from old frames
            for frame in old_frames:
                if frame.graphicsEffect():
                    frame.setGraphicsEffect(None)

            # Call update callback to change content
            update_callback()

            # Start fade in for new content
            if self._pending_fade_callback:
                # Use the provided fade_in_callback if available
                print("🎭 [ANIMATOR] Using provided fade_in_callback")
                self._pending_fade_callback()
                self._pending_fade_callback = None
                self._is_animating = False
            else:
                # Fallback to automatic fade in
                self._fade_in_new_content()

        except Exception:
            self._is_animating = False

    def _fade_in_new_content(self):
        """Fade in new pictograph content."""
        try:
            # Get new pictograph frames from parent
            new_frames = self._get_current_pictograph_frames()

            if not new_frames:
                self._is_animating = False
                if self._pending_fade_callback:
                    self._pending_fade_callback()
                return

            # Create fade in animation group
            fade_in_group = QParallelAnimationGroup(self._parent)

            for frame in new_frames:
                # Ensure opacity effect exists and is set to 0
                if not frame.graphicsEffect():
                    effect = QGraphicsOpacityEffect()
                    effect.setOpacity(0.0)
                    frame.setGraphicsEffect(effect)

                # Create fade in animation
                animation = QPropertyAnimation(frame.graphicsEffect(), b"opacity")
                animation.setDuration(200)
                animation.setStartValue(0.0)
                animation.setEndValue(1.0)
                fade_in_group.addAnimation(animation)

            def on_fade_in_complete():
                # Clear graphics effects after fade in completes
                for frame in new_frames:
                    if frame.graphicsEffect():
                        frame.setGraphicsEffect(None)

                self._is_animating = False
                if self._pending_fade_callback:
                    self._pending_fade_callback()
                    self._pending_fade_callback = None

            fade_in_group.finished.connect(on_fade_in_complete)
            fade_in_group.start()

        except Exception as e:
            print(f"❌ [ANIMATOR] Fade in failed: {e}")
            self._is_animating = False

    def _get_current_pictograph_frames(self) -> list[QWidget]:
        """Get current pictograph frames from parent sections."""
        frames = []
        if hasattr(self._parent, "sections"):
            for section in self._parent.sections.values():
                if hasattr(section, "pictographs") and section.pictographs:
                    frames.extend(section.pictographs.values())
        return frames

    def cleanup(self):
        """Clean up any ongoing animations."""
        self._is_animating = False
        self._pending_fade_callback = None
        self._pending_fade_frames.clear()
