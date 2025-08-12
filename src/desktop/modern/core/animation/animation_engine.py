"""
Core Animation Engine - Framework Agnostic Implementation
This is the canonical animation system that works across platforms.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from dataclasses import dataclass, field
import math
import time
from typing import Any
import uuid

from desktop.modern.core.interfaces.animation_core_interfaces import (
    AnimationConfig,
    AnimationEvent,
    AnimationState,
    AnimationTarget,
    EasingType,
    IAnimationEngine,
    IAnimationScheduler,
    ISettingsProvider,
)


class EasingFunctions:
    """Collection of easing functions for animations."""

    @staticmethod
    def linear(t: float) -> float:
        """Linear easing - no acceleration."""
        return t

    @staticmethod
    def ease_in_out(t: float) -> float:
        """Ease in-out cubic easing."""
        if t < 0.5:
            return 4 * t * t * t
        return 1 - pow(-2 * t + 2, 3) / 2

    @staticmethod
    def ease_in(t: float) -> float:
        """Ease in cubic easing."""
        return t * t * t

    @staticmethod
    def ease_out(t: float) -> float:
        """Ease out cubic easing."""
        return 1 - pow(1 - t, 3)

    @staticmethod
    def spring(t: float, tension: float = 0.8, friction: float = 0.1) -> float:
        """Spring easing with configurable tension and friction."""
        # Simplified spring calculation
        if t in {0, 1}:
            return t

        # Damped harmonic oscillator
        omega = math.sqrt(tension)
        zeta = friction

        if zeta < 1:  # Underdamped
            omega_d = omega * math.sqrt(1 - zeta * zeta)
            return 1 - math.exp(-zeta * omega * t) * math.cos(omega_d * t)
        # Critically damped or overdamped
        return 1 - math.exp(-omega * t) * (1 + omega * t)

    @classmethod
    def get_easing_function(cls, easing_type: EasingType) -> Callable[[float], float]:
        """Get easing function by type."""
        mapping = {
            EasingType.LINEAR: cls.linear,
            EasingType.EASE_IN_OUT: cls.ease_in_out,
            EasingType.EASE_IN: cls.ease_in,
            EasingType.EASE_OUT: cls.ease_out,
            EasingType.SPRING: cls.spring,
            EasingType.CUBIC_BEZIER: cls.ease_in_out,  # Default to ease_in_out
        }
        return mapping.get(easing_type, cls.linear)


@dataclass
class ActiveAnimation:
    """Represents an active animation."""

    id: str
    target: AnimationTarget
    config: AnimationConfig
    start_time: float
    state: AnimationState = AnimationState.PENDING
    current_progress: float = 0.0
    pause_time: float | None = None
    total_paused_duration: float = 0.0
    completion_callbacks: list[Callable] = field(default_factory=list)

    def get_elapsed_time(self, current_time: float) -> float:
        """Get elapsed time accounting for pauses."""
        if self.state == AnimationState.PAUSED:
            return (
                (self.pause_time or current_time)
                - self.start_time
                - self.total_paused_duration
            )
        return current_time - self.start_time - self.total_paused_duration

    def calculate_progress(self, current_time: float) -> float:
        """Calculate animation progress (0.0 to 1.0)."""
        elapsed = self.get_elapsed_time(current_time)
        if elapsed < self.config.delay:
            return 0.0

        animation_elapsed = elapsed - self.config.delay
        if animation_elapsed >= self.config.duration:
            return 1.0

        return (
            animation_elapsed / self.config.duration
            if self.config.duration > 0
            else 1.0
        )


class DefaultAnimationScheduler(IAnimationScheduler):
    """Default animation scheduler using asyncio."""

    def __init__(self, fps: int = 60):
        self.fps = fps
        self.frame_interval = 1.0 / fps

    async def schedule_animation(
        self,
        animation_id: str,
        config: AnimationConfig,
        frame_callback: Callable[[float], None],
    ) -> None:
        """Schedule animation frames."""
        start_time = self.get_current_time()
        last_frame_time = start_time

        while True:
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

            # Check if animation is complete
            if progress >= 1.0:
                break

            # Wait for next frame
            next_frame_time = last_frame_time + self.frame_interval
            sleep_time = max(0, next_frame_time - current_time)
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
            last_frame_time = current_time

    def get_current_time(self) -> float:
        """Get current time in seconds."""
        return time.time()


class CoreAnimationEngine(IAnimationEngine):
    """Core animation engine - framework agnostic."""

    def __init__(
        self,
        scheduler: IAnimationScheduler,
        settings_provider: ISettingsProvider,
    ):
        self.scheduler = scheduler
        self.settings_provider = settings_provider
        self.active_animations: dict[str, ActiveAnimation] = {}
        self._animation_tasks: dict[str, asyncio.Task] = {}

    async def animate_target(
        self, target: AnimationTarget, config: AnimationConfig
    ) -> str:
        """Start animation on target."""
        # Check if animations are disabled
        if not self.settings_provider.get_animations_enabled():
            return await self._instant_animation(target, config)

        # Create animation
        animation_id = str(uuid.uuid4())
        animation = ActiveAnimation(
            id=animation_id,
            target=target,
            config=config,
            start_time=self.scheduler.get_current_time(),
            state=AnimationState.PENDING,
        )

        self.active_animations[animation_id] = animation

        # Start animation task
        task = asyncio.create_task(self._run_animation(animation))
        self._animation_tasks[animation_id] = task

        return animation_id

    async def animate_targets(
        self, targets: list[AnimationTarget], config: AnimationConfig
    ) -> list[str]:
        """Animate multiple targets simultaneously."""
        animation_ids = []

        for target in targets:
            animation_id = await self.animate_target(target, config)
            animation_ids.append(animation_id)

        return animation_ids

    def pause_animation(self, animation_id: str) -> bool:
        """Pause a running animation."""
        animation = self.active_animations.get(animation_id)
        if not animation or animation.state != AnimationState.RUNNING:
            return False

        animation.state = AnimationState.PAUSED
        animation.pause_time = self.scheduler.get_current_time()

        self._emit_animation_event(animation, AnimationState.PAUSED)
        return True

    def resume_animation(self, animation_id: str) -> bool:
        """Resume a paused animation."""
        animation = self.active_animations.get(animation_id)
        if not animation or animation.state != AnimationState.PAUSED:
            return False

        if animation.pause_time:
            pause_duration = self.scheduler.get_current_time() - animation.pause_time
            animation.total_paused_duration += pause_duration
            animation.pause_time = None

        animation.state = AnimationState.RUNNING
        self._emit_animation_event(animation, AnimationState.RUNNING)
        return True

    def cancel_animation(self, animation_id: str) -> bool:
        """Cancel an animation."""
        animation = self.active_animations.get(animation_id)
        if not animation:
            return False

        animation.state = AnimationState.CANCELLED

        # Cancel task
        task = self._animation_tasks.get(animation_id)
        if task and not task.done():
            task.cancel()

        self._emit_animation_event(animation, AnimationState.CANCELLED)
        self._cleanup_animation(animation_id)
        return True

    def get_animation_state(self, animation_id: str) -> AnimationState | None:
        """Get current state of an animation."""
        animation = self.active_animations.get(animation_id)
        return animation.state if animation else None

    async def _instant_animation(
        self, target: AnimationTarget, config: AnimationConfig
    ) -> str:
        """Perform instant animation when animations are disabled."""
        animation_id = str(uuid.uuid4())

        # Emit events for instant completion
        AnimationEvent(
            animation_id=animation_id,
            target=target,
            state=AnimationState.COMPLETED,
            progress=1.0,
            timestamp=self.scheduler.get_current_time(),
        )

        # Animation completed immediately (no events needed)

        return animation_id

    async def _run_animation(self, animation: ActiveAnimation) -> None:
        """Run a single animation."""
        try:
            animation.state = AnimationState.RUNNING
            self._emit_animation_event(animation, AnimationState.RUNNING)

            easing_func = EasingFunctions.get_easing_function(animation.config.easing)

            def frame_callback(raw_progress: float):
                if animation.state == AnimationState.CANCELLED:
                    return

                # Apply easing
                eased_progress = easing_func(raw_progress)
                animation.current_progress = eased_progress

                # Calculate current value
                current_value = self._interpolate_value(
                    animation.config.start_value,
                    animation.config.end_value,
                    eased_progress,
                )

                # Emit frame event with current value
                AnimationEvent(
                    animation_id=animation.id,
                    target=animation.target,
                    state=AnimationState.RUNNING,
                    progress=eased_progress,
                    timestamp=self.scheduler.get_current_time(),
                    metadata={
                        "property": animation.config.property_name,
                        "value": current_value,
                        "animation_type": animation.config.animation_type,
                    },
                )
                # Frame update (no events needed)

            # Run the animation
            await self.scheduler.schedule_animation(
                animation.id, animation.config, frame_callback
            )

            # Animation completed
            if animation.state != AnimationState.CANCELLED:
                animation.state = AnimationState.COMPLETED
                self._emit_animation_event(animation, AnimationState.COMPLETED)

        except asyncio.CancelledError:
            animation.state = AnimationState.CANCELLED
            self._emit_animation_event(animation, AnimationState.CANCELLED)
        except Exception as e:
            animation.state = AnimationState.FAILED
            AnimationEvent(
                animation_id=animation.id,
                target=animation.target,
                state=AnimationState.FAILED,
                progress=animation.current_progress,
                timestamp=self.scheduler.get_current_time(),
                metadata={"error": str(e)},
            )
            # Animation failed (no events needed)
        finally:
            self._cleanup_animation(animation.id)

    def _interpolate_value(
        self, start_value: Any, end_value: Any, progress: float
    ) -> Any:
        """Interpolate between start and end values."""
        if start_value is None or end_value is None:
            return end_value

        # Handle numeric interpolation
        if isinstance(start_value, (int, float)) and isinstance(
            end_value, (int, float)
        ):
            return start_value + (end_value - start_value) * progress

        # Handle other types (colors, etc.) - simplified for now
        return end_value if progress >= 1.0 else start_value

    def _emit_animation_event(
        self, animation: ActiveAnimation, state: AnimationState
    ) -> None:
        """Emit animation lifecycle event."""
        AnimationEvent(
            animation_id=animation.id,
            target=animation.target,
            state=state,
            progress=animation.current_progress,
            timestamp=self.scheduler.get_current_time(),
        )

        # Animation state changed (no events needed)

    def _cleanup_animation(self, animation_id: str) -> None:
        """Clean up completed/cancelled animation."""
        self.active_animations.pop(animation_id, None)
        task = self._animation_tasks.pop(animation_id, None)
        if task and not task.done():
            task.cancel()


class DefaultSettingsProvider(ISettingsProvider):
    """Default settings provider with reasonable defaults."""

    def __init__(
        self,
        animations_enabled: bool = True,
        default_duration: float = 0.25,
        default_easing: EasingType = EasingType.EASE_IN_OUT,
        reduced_motion: bool = False,
    ):
        self._animations_enabled = animations_enabled
        self._default_duration = default_duration
        self._default_easing = default_easing
        self._reduced_motion = reduced_motion

    def get_animations_enabled(self) -> bool:
        return self._animations_enabled

    def get_default_duration(self) -> float:
        return self._default_duration

    def get_default_easing(self) -> EasingType:
        return self._default_easing

    def get_reduced_motion(self) -> bool:
        return self._reduced_motion

    def set_animations_enabled(self, enabled: bool) -> None:
        self._animations_enabled = enabled

    def set_default_duration(self, duration: float) -> None:
        self._default_duration = duration

    def set_default_easing(self, easing: EasingType) -> None:
        self._default_easing = easing


def create_default_animation_engine() -> IAnimationEngine:
    """Create a default animation engine with all dependencies."""
    scheduler = DefaultAnimationScheduler(fps=60)
    settings_provider = DefaultSettingsProvider()

    return CoreAnimationEngine(scheduler, settings_provider)
