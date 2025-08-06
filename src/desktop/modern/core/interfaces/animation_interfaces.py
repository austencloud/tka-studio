"""
Animation service interfaces for TKA modern desktop app.
These interfaces define the contracts for fade and animation services.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any

from desktop.modern.core.types import (
    AnimationGroupType,
    OpacityEffectType,
    PropertyAnimationType,
    StackWidget,
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
    callback: Callable[[], None] | None = None
    start_opacity: float | None = None
    end_opacity: float | None = None


@dataclass
class StackFadeOptions(FadeOptions):
    """Configuration options for stack fade animations."""

    resize_layout: bool = False
    layout_ratio: tuple[int, int] | None = None


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
    def apply_fade_effect(self, widget: WidgetType) -> dict[str, Any]:
        """Apply a fade effect to a widget."""

    @abstractmethod
    def remove_effects(self, widgets: list[WidgetType]) -> None:
        """Remove graphics effects from widgets."""

    @abstractmethod
    def cleanup_all(self) -> None:
        """Cleanup all managed effects."""


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

    @abstractmethod
    def create_parallel_group(self) -> AnimationGroupType:
        """Create a parallel animation group."""


class IFadeSettingsProvider(ABC):
    """Interface for fade animation settings."""

    @abstractmethod
    def get_fades_enabled(self) -> bool:
        """Check if fade animations are enabled."""

    @abstractmethod
    def get_default_duration(self) -> int:
        """Get default animation duration."""

    @abstractmethod
    def get_default_easing(self) -> EasingType:
        """Get default easing type."""


class IAnimationService(ABC):
    """Core animation service interface."""

    @abstractmethod
    async def fade_widget(
        self, widget: WidgetType, fade_in: bool, options: FadeOptions | None = None
    ) -> None:
        """Fade a single widget in or out."""

    @abstractmethod
    async def fade_widgets(
        self,
        widgets: list[WidgetType],
        fade_in: bool,
        options: FadeOptions | None = None,
    ) -> None:
        """Fade multiple widgets in or out."""

    @abstractmethod
    async def fade_to_opacity(
        self, widget: WidgetType, opacity: float, options: FadeOptions | None = None
    ) -> None:
        """Fade widget to specific opacity."""

    @abstractmethod
    async def cross_fade(
        self,
        out_widget: WidgetType,
        in_widget: WidgetType,
        options: FadeOptions | None = None,
    ) -> None:
        """Cross-fade between two widgets."""

    @abstractmethod
    def fade_widget_sync(
        self, widget: WidgetType, fade_in: bool, options: FadeOptions | None = None
    ) -> None:
        """Synchronous fade for backward compatibility."""


class IStackAnimationService(ABC):
    """Interface for stack widget animations."""

    @abstractmethod
    async def fade_stack(
        self,
        stack: StackWidget,
        new_index: int,
        options: StackFadeOptions | None = None,
    ) -> None:
        """Fade transition between stack widgets."""

    @abstractmethod
    async def fade_parallel_stacks(self, operation: ParallelStackOperation) -> None:
        """Fade transition for parallel stacks with layout changes."""


class IFadeOrchestrator(ABC):
    """High-level fade orchestration interface - replaces legacy FadeManager."""

    @abstractmethod
    async def fade_widgets_and_update(
        self,
        widgets: list[WidgetType],
        update_callback: Callable[[], None],
        options: FadeOptions | None = None,
    ) -> None:
        """Fade out, execute callback, fade in (legacy fade_and_update replacement)."""

    @abstractmethod
    async def fade_stack_transition(
        self,
        stack: StackWidget,
        new_index: int,
        options: StackFadeOptions | None = None,
    ) -> None:
        """High-level stack transition."""

    @abstractmethod
    async def fade_parallel_stack_transition(
        self, operation: ParallelStackOperation
    ) -> None:
        """High-level parallel stack transition."""

    @abstractmethod
    def get_fades_enabled(self) -> bool:
        """Check if fades are enabled (legacy compatibility)."""
