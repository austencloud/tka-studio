"""
OptionPickerSectionAnimationHandler

Handles all animation logic for OptionPickerSection including:
- Fade in/out transitions using Qt animation groups
- Async animation orchestrator integration
- Animation state management
- Fallback to direct updates when animations fail

Extracted from OptionPickerSection to follow Single Responsibility Principle.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable

from PyQt6.QtCore import QParallelAnimationGroup, QPropertyAnimation, QTimer
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget

from desktop.modern.core.interfaces.animation_core_interfaces import (
    AnimationConfig,
    EasingType,
    IAnimationOrchestrator,
)
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.presentation.components.option_picker.components.option_pictograph import (
    OptionPictograph,
)
from desktop.modern.presentation.components.option_picker.types.letter_types import (
    LetterType,
)


class OptionPickerSectionAnimationHandler:
    """
    Handles animation logic for OptionPickerSection.

    Responsibilities:
    - Qt-based fade in/out animations
    - Async animation orchestrator integration
    - Animation state management
    - Error handling and fallbacks
    """

    def __init__(
        self,
        parent_widget: QWidget,
        letter_type: LetterType,
        animation_orchestrator: IAnimationOrchestrator | None = None,
    ):
        """Initialize animation handler."""
        self._parent_widget = parent_widget
        self._letter_type = letter_type
        self._animation_orchestrator = animation_orchestrator

        # Animation state
        self._current_fade_animation: QParallelAnimationGroup | None = None
        self._is_animating = False

    def animate_content_update(
        self,
        existing_frames: list[OptionPictograph],
        update_callback: Callable[[], None],
        fade_in_callback: Callable[[], None],
    ) -> bool:
        """
        Animate content update with fade out -> update -> fade in.

        Args:
            existing_frames: Current frames to fade out
            update_callback: Function to call after fade out (updates content)
            fade_in_callback: Function to call after content update (fades in new content)

        Returns:
            True if animation started successfully, False if fallback needed
        """
        if not self._animation_orchestrator or not existing_frames:
            return False

        try:
            return self._start_qt_fade_animation(
                existing_frames, update_callback, fade_in_callback
            )
        except Exception as e:
            print(
                f"❌ [ANIMATION] Qt fade animation failed for {self._letter_type}: {e}"
            )
            return False

    def _start_qt_fade_animation(
        self,
        existing_frames: list[OptionPictograph],
        update_callback: Callable[[], None],
        fade_in_callback: Callable[[], None],
    ) -> bool:
        """Start Qt-based fade animation."""
        # Create fade out animations for existing frames
        fade_out_group = QParallelAnimationGroup(self._parent_widget)
        animations_added = 0

        for frame in existing_frames:
            if self._setup_frame_for_fade_out(frame, fade_out_group):
                animations_added += 1

        if animations_added == 0:
            return False

        # Set up completion callback
        def on_fade_out_complete():
            self._is_animating = False
            update_callback()
            QTimer.singleShot(50, fade_in_callback)  # Small delay for content update

        # Store reference to prevent garbage collection
        self._current_fade_animation = fade_out_group
        self._is_animating = True

        fade_out_group.finished.connect(on_fade_out_complete)
        fade_out_group.start()

        return True

    def _setup_frame_for_fade_out(
        self, frame: OptionPictograph, fade_out_group: QParallelAnimationGroup
    ) -> bool:
        """Setup a single frame for fade out animation."""
        try:
            # Validate frame is still valid and visible
            if not frame or frame.isHidden() or not frame.parent():
                return False

            # Create opacity effect if not present
            if not frame.graphicsEffect():
                effect = QGraphicsOpacityEffect()
                effect.setOpacity(1.0)  # Ensure it starts visible
                frame.setGraphicsEffect(effect)

            # Validate graphics effect is properly set
            graphics_effect = frame.graphicsEffect()
            if not graphics_effect:
                print(
                    f"⚠️ [FADE] No graphics effect for fade-out frame in {self._letter_type}"
                )
                return False

            # Create fade out animation
            animation = QPropertyAnimation(graphics_effect, b"opacity")
            animation.setDuration(200)  # 200ms to match legacy
            animation.setStartValue(1.0)
            animation.setEndValue(0.0)
            fade_out_group.addAnimation(animation)

            return True

        except Exception as e:
            print(
                f"⚠️ [FADE] Skipping invalid fade-out frame in {self._letter_type}: {e}"
            )
            return False

    def fade_in_frames(self, frames: list[OptionPictograph]) -> None:
        """Fade in newly loaded frames."""
        if not frames:
            return

        try:
            fade_in_group = QParallelAnimationGroup(self._parent_widget)
            valid_animations = 0

            for frame in frames:
                if self._setup_frame_for_fade_in(frame, fade_in_group):
                    valid_animations += 1

            if valid_animations > 0:
                fade_in_group.start()
            else:
                print(f"⚠️ [FADE] No valid frames to animate for {self._letter_type}")

        except Exception as e:
            print(f"❌ [FADE] Fade in failed for {self._letter_type}: {e}")

    def _setup_frame_for_fade_in(
        self, frame: OptionPictograph, fade_in_group: QParallelAnimationGroup
    ) -> bool:
        """Setup a single frame for fade in animation."""
        try:
            # Validate frame is still valid and visible
            if not frame or frame.isHidden() or not frame.parent():
                return False

            # Create opacity effect if not present
            if not frame.graphicsEffect():
                effect = QGraphicsOpacityEffect()
                frame.setGraphicsEffect(effect)
                effect.setOpacity(0.0)  # Start invisible

            # Validate graphics effect is properly set
            graphics_effect = frame.graphicsEffect()
            if not graphics_effect:
                print(f"⚠️ [FADE] No graphics effect for frame in {self._letter_type}")
                return False

            # Create fade in animation
            animation = QPropertyAnimation(graphics_effect, b"opacity")
            animation.setDuration(200)  # 200ms to match legacy
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)
            fade_in_group.addAnimation(animation)

            return True

        except Exception as e:
            print(f"⚠️ [FADE] Skipping invalid frame in {self._letter_type}: {e}")
            return False

    async def animate_with_async_orchestrator(
        self,
        pictographs_for_section: list[PictographData],
        existing_frames: list[OptionPictograph],
        update_callback: Callable[[list[PictographData]], None],
        get_new_frames_callback: Callable[[], list[OptionPictograph]],
    ) -> None:
        """
        Animate using async animation orchestrator.

        This method provides async animation support for advanced scenarios.
        """
        try:
            # Animation config matching legacy timing (200ms)
            config = AnimationConfig(duration=0.2, easing=EasingType.EASE_IN_OUT)

            # Fade out existing frames
            if existing_frames:
                fade_out_tasks = []
                for frame in existing_frames:
                    if frame.isVisible():
                        task = self._animation_orchestrator.fade_target(
                            frame, fade_in=False, config=config
                        )
                        fade_out_tasks.append(task)

                # Wait for all fade outs to complete
                if fade_out_tasks:
                    await asyncio.gather(*fade_out_tasks)

            # Update content (equivalent to legacy callback)
            update_callback(pictographs_for_section)

            # Fade in new frames
            new_frames = get_new_frames_callback()
            if new_frames:
                fade_in_tasks = []
                for frame in new_frames:
                    if frame.isVisible():
                        task = self._animation_orchestrator.fade_target(
                            frame, fade_in=True, config=config
                        )
                        fade_in_tasks.append(task)

                # Start all fade ins
                if fade_in_tasks:
                    await asyncio.gather(*fade_in_tasks)

        except Exception as e:
            print(
                f"❌ [ANIMATION] Error in async fade transition for {self._letter_type}: {e}"
            )
            # Fallback to direct update
            update_callback(pictographs_for_section)

    def is_animating(self) -> bool:
        """Check if animation is currently in progress."""
        return self._is_animating

    def cleanup(self) -> None:
        """Clean up animation resources."""
        if self._current_fade_animation:
            self._current_fade_animation.stop()
            self._current_fade_animation = None
        self._is_animating = False
