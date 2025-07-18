"""
Animation service interfaces for TKA modern desktop app.
These interfaces define the contracts for fade and animation services.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union

from core.types import (
    AnimationGroupType,
    OpacityEffectType,
    PropertyAnimationType,
    StackWidget,
    Widget,
    WidgetType,
)


class EasingType(Enum):
    """Animation easing types - web compatible."""

    LINEAR = "linear"
    IN_OUT_QUAD = "ease-in-out"
    IN_OUT_CUBIC = "cubic-bezier(0.645, 0.045, 0.355, 1)"
    IN_OUT_QUART = "cubic-bezier(0.77, 0, 0.175, 1)"


@dataclass
class FadeOptions:
    """Configuration options for fade animations."""

    duration: int = 250
    easing: EasingType = EasingType.IN_OUT_QUAD
    callback: Optional[Callable[[], None]] = None
    start_opacity: Optional[float] = None
    end_opacity: Optional[float] = None


@dataclass
class StackFadeOptions(FadeOptions):
    """Configuration options for stack fade animations."""

    resize_layout: bool = False
    layout_ratio: Optional[tuple[int, int]] = None


@dataclass
class ParallelStackOperation:
    """Configuration for parallel stack fade operations."""

    left_stack: StackWidget
    left_new_index: int
    right_stack: StackWidget
    right_new_index: int
    layout_ratio: tuple[int, int]
    options: StackFadeOptions


class IGraphicsEffectManager(ABC):
    """Interface for managing graphics effects lifecycle."""

    @abstractmethod
    def apply_fade_effect(self, widget: WidgetType) -> Dict[str, Any]:
        """Apply a fade effect to a widget."""
        pass

    @abstractmethod
    def remove_effects(self, widgets: List[WidgetType]) -> None:
        """Remove graphics effects from widgets."""
        pass

    @abstractmethod
    def cleanup_all(self) -> None:
        """Cleanup all managed effects."""
        pass


class IAnimationFactory(ABC):
    """Interface for creating animations."""

    @abstractmethod
    def create_opacity_animation(
        self,
        effect: OpacityEffectType,
        options: FadeOptions,
        start_value: float,
        end_value: float,
    ) -> PropertyAnimationType:
        """Create an opacity animation."""
        pass

    @abstractmethod
    def create_parallel_group(self) -> AnimationGroupType:
        """Create a parallel animation group."""
        pass


class IFadeSettingsProvider(ABC):
    """Interface for fade animation settings."""

    @abstractmethod
    def get_fades_enabled(self) -> bool:
        """Check if fade animations are enabled."""
        pass

    @abstractmethod
    def get_default_duration(self) -> int:
        """Get default animation duration."""
        pass

    @abstractmethod
    def get_default_easing(self) -> EasingType:
        """Get default easing type."""
        pass


class IAnimationService(ABC):
    """Core animation service interface."""

    @abstractmethod
    async def fade_widget(
        self, widget: WidgetType, fade_in: bool, options: Optional[FadeOptions] = None
    ) -> None:
        """Fade a single widget in or out."""
        pass

    @abstractmethod
    async def fade_widgets(
        self,
        widgets: List[WidgetType],
        fade_in: bool,
        options: Optional[FadeOptions] = None,
    ) -> None:
        """Fade multiple widgets in or out."""
        pass

    @abstractmethod
    async def fade_to_opacity(
        self, widget: WidgetType, opacity: float, options: Optional[FadeOptions] = None
    ) -> None:
        """Fade widget to specific opacity."""
        pass

    @abstractmethod
    async def cross_fade(
        self,
        out_widget: WidgetType,
        in_widget: WidgetType,
        options: Optional[FadeOptions] = None,
    ) -> None:
        """Cross-fade between two widgets."""
        pass

    @abstractmethod
    def fade_widget_sync(
        self, widget: WidgetType, fade_in: bool, options: Optional[FadeOptions] = None
    ) -> None:
        """Synchronous fade for backward compatibility."""
        pass


class IStackAnimationService(ABC):
    """Interface for stack widget animations."""

    @abstractmethod
    async def fade_stack(
        self,
        stack: StackWidget,
        new_index: int,
        options: Optional[StackFadeOptions] = None,
    ) -> None:
        """Fade transition between stack widgets."""
        pass

    @abstractmethod
    async def fade_parallel_stacks(self, operation: ParallelStackOperation) -> None:
        """Fade transition for parallel stacks with layout changes."""
        pass


class IFadeOrchestrator(ABC):
    """High-level fade orchestration interface - replaces legacy FadeManager."""

    @abstractmethod
    async def fade_widgets_and_update(
        self,
        widgets: List[WidgetType],
        update_callback: Callable[[], None],
        options: Optional[FadeOptions] = None,
    ) -> None:
        """Fade out, execute callback, fade in (legacy fade_and_update replacement)."""
        pass

    @abstractmethod
    async def fade_stack_transition(
        self,
        stack: StackWidget,
        new_index: int,
        options: Optional[StackFadeOptions] = None,
    ) -> None:
        """High-level stack transition."""
        pass

    @abstractmethod
    async def fade_parallel_stack_transition(
        self, operation: ParallelStackOperation
    ) -> None:
        """High-level parallel stack transition."""
        pass

    @abstractmethod
    def get_fades_enabled(self) -> bool:
        """Check if fades are enabled (legacy compatibility)."""
        pass
