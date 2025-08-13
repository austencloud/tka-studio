"""
Framework-Agnostic Animation Service

This service handles animation logic without Qt dependencies.
It generates animation commands and data that can be executed
by any animation framework.
"""

import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class AnimationType(Enum):
    """Types of animations supported."""

    FADE = "fade"
    SLIDE = "slide"
    SCALE = "scale"
    ROTATE = "rotate"
    OPACITY = "opacity"
    CUSTOM = "custom"


class EasingType(Enum):
    """Animation easing types."""

    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    BOUNCE = "bounce"
    ELASTIC = "elastic"


class AnimationCommand:
    """Framework-agnostic animation command."""

    def __init__(
        self,
        command_id: str,
        target_id: str,
        animation_type: AnimationType,
        duration: float,
        start_values: dict[str, Any],
        end_values: dict[str, Any],
        easing: EasingType = EasingType.EASE_IN_OUT,
        delay: float = 0.0,
        metadata: dict[str, Any] | None = None,
    ):
        self.command_id = command_id
        self.target_id = target_id
        self.animation_type = animation_type
        self.duration = duration
        self.start_values = start_values
        self.end_values = end_values
        self.easing = easing
        self.delay = delay
        self.metadata = metadata or {}


class IAnimationService(ABC):
    """Interface for framework-agnostic animation service."""

    @abstractmethod
    def create_animation_command(
        self,
        target_id: str,
        animation_type: AnimationType,
        duration: float,
        start_values: dict[str, Any],
        end_values: dict[str, Any],
        **kwargs,
    ) -> AnimationCommand:
        """Create an animation command."""

    @abstractmethod
    def create_animation_sequence(
        self, commands: list[AnimationCommand]
    ) -> list[AnimationCommand]:
        """Create a sequence of animation commands."""

    @abstractmethod
    def calculate_animation_values(
        self, command: AnimationCommand, progress: float
    ) -> dict[str, Any]:
        """Calculate intermediate animation values."""


class CoreAnimationService(IAnimationService):
    """
    Framework-agnostic animation service.

    Handles all animation logic without framework dependencies:
    - Animation command creation
    - Easing calculations
    - Sequence coordination
    - Value interpolation
    """

    def __init__(self):
        """Initialize the animation service."""
        self._command_counter = 0
        self._performance_stats = {
            "commands_created": 0,
            "sequences_created": 0,
            "calculations_performed": 0,
            "errors": 0,
        }

    def create_animation_command(
        self,
        target_id: str,
        animation_type: AnimationType,
        duration: float,
        start_values: dict[str, Any],
        end_values: dict[str, Any],
        easing: EasingType = EasingType.EASE_IN_OUT,
        delay: float = 0.0,
        metadata: dict[str, Any] | None = None,
    ) -> AnimationCommand:
        """
        Create an animation command.

        Args:
            target_id: Identifier for the animation target
            animation_type: Type of animation
            duration: Animation duration in seconds
            start_values: Starting property values
            end_values: Ending property values
            easing: Easing function type
            delay: Delay before animation starts
            metadata: Additional metadata

        Returns:
            AnimationCommand object
        """
        try:
            self._command_counter += 1
            command_id = f"anim_{self._command_counter}"

            command = AnimationCommand(
                command_id=command_id,
                target_id=target_id,
                animation_type=animation_type,
                duration=duration,
                start_values=start_values.copy(),
                end_values=end_values.copy(),
                easing=easing,
                delay=delay,
                metadata=metadata or {},
            )

            self._performance_stats["commands_created"] += 1
            logger.debug(
                f"🎬 [ANIMATION_SERVICE] Created animation command: {command_id}"
            )

            return command

        except Exception as e:
            self._performance_stats["errors"] += 1
            logger.error(
                f"❌ [ANIMATION_SERVICE] Failed to create animation command: {e}"
            )
            raise

    def create_animation_sequence(
        self, commands: list[AnimationCommand]
    ) -> list[AnimationCommand]:
        """
        Create a sequence of animation commands.

        Args:
            commands: List of animation commands

        Returns:
            Optimized sequence of commands
        """
        try:
            # Sort commands by delay to ensure proper sequencing
            sorted_commands = sorted(commands, key=lambda cmd: cmd.delay)

            self._performance_stats["sequences_created"] += 1
            logger.debug(
                f"🎬 [ANIMATION_SERVICE] Created animation sequence with {len(commands)} commands"
            )

            return sorted_commands

        except Exception as e:
            self._performance_stats["errors"] += 1
            logger.error(
                f"❌ [ANIMATION_SERVICE] Failed to create animation sequence: {e}"
            )
            return commands

    def calculate_animation_values(
        self, command: AnimationCommand, progress: float
    ) -> dict[str, Any]:
        """
        Calculate intermediate animation values.

        Args:
            command: Animation command
            progress: Animation progress (0.0 to 1.0)

        Returns:
            Dictionary of interpolated values
        """
        try:
            # Clamp progress to valid range
            progress = max(0.0, min(1.0, progress))

            # Apply easing function
            eased_progress = self._apply_easing(progress, command.easing)

            # Interpolate values
            interpolated_values = {}
            for key in command.start_values:
                if key in command.end_values:
                    start_val = command.start_values[key]
                    end_val = command.end_values[key]

                    # Interpolate based on value type
                    interpolated_values[key] = self._interpolate_value(
                        start_val, end_val, eased_progress
                    )

            self._performance_stats["calculations_performed"] += 1

            return interpolated_values

        except Exception as e:
            self._performance_stats["errors"] += 1
            logger.error(
                f"❌ [ANIMATION_SERVICE] Failed to calculate animation values: {e}"
            )
            return command.start_values.copy()

    def _apply_easing(self, progress: float, easing: EasingType) -> float:
        """Apply easing function to progress."""
        try:
            if easing == EasingType.LINEAR:
                return progress
            elif easing == EasingType.EASE_IN:
                return progress * progress
            elif easing == EasingType.EASE_OUT:
                return 1 - (1 - progress) * (1 - progress)
            elif easing == EasingType.EASE_IN_OUT:
                if progress < 0.5:
                    return 2 * progress * progress
                else:
                    return 1 - 2 * (1 - progress) * (1 - progress)
            elif easing == EasingType.BOUNCE:
                return self._bounce_easing(progress)
            elif easing == EasingType.ELASTIC:
                return self._elastic_easing(progress)
            else:
                return progress  # Fallback to linear

        except Exception:
            return progress  # Fallback to linear on error

    def _bounce_easing(self, progress: float) -> float:
        """Bounce easing function."""
        if progress < 1 / 2.75:
            return 7.5625 * progress * progress
        elif progress < 2 / 2.75:
            progress -= 1.5 / 2.75
            return 7.5625 * progress * progress + 0.75
        elif progress < 2.5 / 2.75:
            progress -= 2.25 / 2.75
            return 7.5625 * progress * progress + 0.9375
        else:
            progress -= 2.625 / 2.75
            return 7.5625 * progress * progress + 0.984375

    def _elastic_easing(self, progress: float) -> float:
        """Elastic easing function."""
        if progress == 0 or progress == 1:
            return progress

        import math

        period = 0.3
        amplitude = 1
        s = period / 4

        return (
            amplitude
            * math.pow(2, -10 * progress)
            * math.sin((progress - s) * (2 * math.pi) / period)
            + 1
        )

    def _interpolate_value(self, start_val: Any, end_val: Any, progress: float) -> Any:
        """Interpolate between two values."""
        try:
            # Numeric interpolation
            if isinstance(start_val, (int, float)) and isinstance(
                end_val, (int, float)
            ):
                return start_val + (end_val - start_val) * progress

            # Color interpolation (if hex colors)
            if isinstance(start_val, str) and isinstance(end_val, str):
                if start_val.startswith("#") and end_val.startswith("#"):
                    return self._interpolate_color(start_val, end_val, progress)

            # For other types, just return start or end based on progress
            return end_val if progress >= 0.5 else start_val

        except Exception:
            return start_val  # Fallback to start value

    def _interpolate_color(
        self, start_color: str, end_color: str, progress: float
    ) -> str:
        """Interpolate between two hex colors."""
        try:
            # Parse hex colors
            start_rgb = tuple(int(start_color[i : i + 2], 16) for i in (1, 3, 5))
            end_rgb = tuple(int(end_color[i : i + 2], 16) for i in (1, 3, 5))

            # Interpolate RGB values
            interpolated_rgb = tuple(
                int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * progress)
                for i in range(3)
            )

            # Convert back to hex
            return f"#{interpolated_rgb[0]:02x}{interpolated_rgb[1]:02x}{interpolated_rgb[2]:02x}"

        except Exception:
            return start_color  # Fallback to start color

    def get_performance_stats(self) -> dict[str, Any]:
        """Get performance statistics."""
        return self._performance_stats.copy()

    def reset_performance_stats(self):
        """Reset performance statistics."""
        self._performance_stats = {
            "commands_created": 0,
            "sequences_created": 0,
            "calculations_performed": 0,
            "errors": 0,
        }


# Factory function
def create_animation_service() -> CoreAnimationService:
    """Create framework-agnostic animation service."""
    return CoreAnimationService()
