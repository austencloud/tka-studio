"""
Core animation system interfaces - Framework Agnostic
These interfaces define the canonical animation system that can be adapted to any UI framework.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any


class EasingType(Enum):
    """Framework-agnostic easing types."""

    LINEAR = "linear"
    EASE_IN_OUT = "ease-in-out"
    EASE_IN = "ease-in"
    EASE_OUT = "ease-out"
    CUBIC_BEZIER = "cubic-bezier"
    SPRING = "spring"


class AnimationType(Enum):
    """Types of animations supported."""

    OPACITY = "opacity"
    TRANSFORM = "transform"
    POSITION = "position"
    SCALE = "scale"
    ROTATION = "rotation"
    COLOR = "color"
    CUSTOM = "custom"


class AnimationState(Enum):
    """Animation lifecycle states."""

    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


@dataclass
class AnimationTarget:
    """Framework-agnostic representation of an animation target."""

    id: str
    element_type: str
    properties: dict[str, Any]

    def __hash__(self):
        return hash(self.id)


@dataclass
class AnimationConfig:
    """Configuration for animations - framework agnostic."""

    duration: float = 0.25  # seconds
    easing: EasingType = EasingType.EASE_IN_OUT
    delay: float = 0.0
    repeat: int = 1
    reverse: bool = False
    start_value: Any = None
    end_value: Any = None
    property_name: str = "opacity"
    animation_type: AnimationType = AnimationType.OPACITY


@dataclass
class AnimationEvent:
    """Event data for animation lifecycle events."""

    animation_id: str
    target: AnimationTarget
    state: AnimationState
    progress: float = 0.0
    timestamp: float = 0.0
    metadata: dict[str, Any] = None


class IAnimationCommand(ABC):
    """Base interface for animation commands (Command Pattern)."""

    @property
    @abstractmethod
    def command_id(self) -> str:
        """Unique identifier for this command."""

    @abstractmethod
    async def execute(self) -> bool:
        """Execute the animation command."""

    @abstractmethod
    async def undo(self) -> bool:
        """Undo the animation command (if possible)."""

    @abstractmethod
    def can_undo(self) -> bool:
        """Check if this command can be undone."""


class IAnimationEngine(ABC):
    """Core animation engine - framework agnostic."""

    @abstractmethod
    async def animate_target(
        self, target: AnimationTarget, config: AnimationConfig
    ) -> str:
        """Start animation on target. Returns animation ID."""

    @abstractmethod
    async def animate_targets(
        self, targets: list[AnimationTarget], config: AnimationConfig
    ) -> list[str]:
        """Animate multiple targets. Returns list of animation IDs."""

    @abstractmethod
    def pause_animation(self, animation_id: str) -> bool:
        """Pause a running animation."""

    @abstractmethod
    def resume_animation(self, animation_id: str) -> bool:
        """Resume a paused animation."""

    @abstractmethod
    def cancel_animation(self, animation_id: str) -> bool:
        """Cancel an animation."""

    @abstractmethod
    def get_animation_state(self, animation_id: str) -> AnimationState | None:
        """Get current state of an animation."""


class ITargetAdapter(ABC):
    """Adapter for converting framework-specific targets to AnimationTarget."""

    @abstractmethod
    def adapt_target(self, framework_target: Any) -> AnimationTarget:
        """Convert framework-specific target to AnimationTarget."""

    @abstractmethod
    def apply_animation(
        self, target: AnimationTarget, property_name: str, value: Any
    ) -> bool:
        """Apply animation value to the actual target."""


class IAnimationRenderer(ABC):
    """Platform-specific animation renderer."""

    @abstractmethod
    async def render_frame(
        self, target: AnimationTarget, property_name: str, value: Any, progress: float
    ) -> bool:
        """Render a single animation frame."""

    @abstractmethod
    def supports_property(self, property_name: str) -> bool:
        """Check if this renderer supports the given property."""


class IAnimationScheduler(ABC):
    """Scheduler for managing animation timing."""

    @abstractmethod
    async def schedule_animation(
        self,
        animation_id: str,
        config: AnimationConfig,
        frame_callback: Callable[[float], None],
    ) -> None:
        """Schedule animation frames."""

    @abstractmethod
    def get_current_time(self) -> float:
        """Get current time in seconds."""


class ISettingsProvider(ABC):
    """Provider for animation settings."""

    @abstractmethod
    def get_animations_enabled(self) -> bool:
        """Check if animations are globally enabled."""

    @abstractmethod
    def get_default_duration(self) -> float:
        """Get default animation duration."""

    @abstractmethod
    def get_default_easing(self) -> EasingType:
        """Get default easing type."""

    @abstractmethod
    def get_reduced_motion(self) -> bool:
        """Check if user prefers reduced motion."""


# Command Implementations


@dataclass
class FadeCommand(IAnimationCommand):
    """Command to fade target in or out."""

    target: AnimationTarget
    fade_in: bool
    config: AnimationConfig
    engine: IAnimationEngine
    _animation_id: str | None = None

    @property
    def command_id(self) -> str:
        return f"fade_{self.target.id}_{self.fade_in}"

    async def execute(self) -> bool:
        config = AnimationConfig(
            duration=self.config.duration,
            easing=self.config.easing,
            start_value=0.0 if self.fade_in else 1.0,
            end_value=1.0 if self.fade_in else 0.0,
            property_name="opacity",
            animation_type=AnimationType.OPACITY,
        )
        self._animation_id = await self.engine.animate_target(self.target, config)
        return self._animation_id is not None

    async def undo(self) -> bool:
        if not self.can_undo():
            return False

        # Create reverse animation
        reverse_config = AnimationConfig(
            duration=self.config.duration,
            easing=self.config.easing,
            start_value=1.0 if self.fade_in else 0.0,
            end_value=0.0 if self.fade_in else 1.0,
            property_name="opacity",
            animation_type=AnimationType.OPACITY,
        )
        undo_id = await self.engine.animate_target(self.target, reverse_config)
        return undo_id is not None

    def can_undo(self) -> bool:
        return self._animation_id is not None


@dataclass
class TransitionCommand(IAnimationCommand):
    """Command to transition between two states."""

    target: AnimationTarget
    from_state: dict[str, Any]
    to_state: dict[str, Any]
    config: AnimationConfig
    engine: IAnimationEngine
    _animation_ids: list[str] = None

    @property
    def command_id(self) -> str:
        return f"transition_{self.target.id}"

    async def execute(self) -> bool:
        self._animation_ids = []

        for property_name, end_value in self.to_state.items():
            start_value = self.from_state.get(property_name)

            config = AnimationConfig(
                duration=self.config.duration,
                easing=self.config.easing,
                start_value=start_value,
                end_value=end_value,
                property_name=property_name,
                animation_type=self._get_animation_type(property_name),
            )

            animation_id = await self.engine.animate_target(self.target, config)
            if animation_id:
                self._animation_ids.append(animation_id)

        return len(self._animation_ids) > 0

    async def undo(self) -> bool:
        if not self.can_undo():
            return False

        # Animate back to original state
        for property_name, start_value in self.from_state.items():
            config = AnimationConfig(
                duration=self.config.duration,
                easing=self.config.easing,
                start_value=self.to_state.get(property_name),
                end_value=start_value,
                property_name=property_name,
                animation_type=self._get_animation_type(property_name),
            )
            await self.engine.animate_target(self.target, config)

        return True

    def can_undo(self) -> bool:
        return self._animation_ids is not None and len(self._animation_ids) > 0

    def _get_animation_type(self, property_name: str) -> AnimationType:
        """Map property names to animation types."""
        mapping = {
            "opacity": AnimationType.OPACITY,
            "x": AnimationType.POSITION,
            "y": AnimationType.POSITION,
            "scale": AnimationType.SCALE,
            "rotation": AnimationType.ROTATION,
            "color": AnimationType.COLOR,
        }
        return mapping.get(property_name, AnimationType.CUSTOM)


# High-level service interfaces


class IAnimationOrchestrator(ABC):
    """High-level animation orchestration service."""

    @abstractmethod
    async def fade_target(
        self,
        target: Any,  # Framework-specific target
        fade_in: bool,
        config: AnimationConfig | None = None,
    ) -> str:
        """Fade a target in or out."""

    @abstractmethod
    async def fade_targets(
        self,
        targets: list[Any],
        fade_in: bool,
        config: AnimationConfig | None = None,
    ) -> list[str]:
        """Fade multiple targets."""

    @abstractmethod
    async def transition_targets(
        self,
        targets: list[Any],
        update_callback: Callable[[], None],
        config: AnimationConfig | None = None,
    ) -> None:
        """Fade out, update, then fade in."""

    @abstractmethod
    async def execute_command(self, command: IAnimationCommand) -> bool:
        """Execute an animation command."""

    @abstractmethod
    async def undo_last_command(self) -> bool:
        """Undo the last executed command."""


class IAnimationServiceFactory(ABC):
    """Factory for creating animation services for specific frameworks."""

    @abstractmethod
    def create_target_adapter(self, framework_name: str) -> ITargetAdapter:
        """Create target adapter for specific framework."""

    @abstractmethod
    def create_renderer(self, framework_name: str) -> IAnimationRenderer:
        """Create renderer for specific framework."""

    @abstractmethod
    def create_scheduler(self, framework_name: str) -> IAnimationScheduler:
        """Create scheduler for specific framework."""
