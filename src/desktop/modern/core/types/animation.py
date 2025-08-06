"""
Platform-agnostic animation types for web portability.

This module defines Protocol-based interfaces that can be implemented
by both Qt desktop components and web browser elements, enabling
seamless cross-platform animation support.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, Union


class StackContainer(Protocol):
    """Protocol for stack-like containers across platforms.

    Represents containers that can display one widget/element at a time
    from a collection, similar to QStackedWidget or tabbed interfaces.
    """

    def get_current_index(self) -> int:
        """Get the index of the currently visible widget/element."""
        ...

    def set_current_index(self, index: int) -> None:
        """Set which widget/element should be visible by index."""
        ...

    def get_widget_at(self, index: int) -> Any:
        """Get the widget/element at the specified index."""
        ...

    def get_widget_count(self) -> int:
        """Get the total number of widgets/elements in the stack."""
        ...


class OpacityEffect(Protocol):
    """Protocol for opacity effects across platforms.

    Represents objects that can control the opacity/transparency
    of UI elements, whether through Qt graphics effects or CSS.
    """

    def get_opacity(self) -> float:
        """Get the current opacity value (0.0 to 1.0)."""
        ...

    def set_opacity(self, opacity: float) -> None:
        """Set the opacity value (0.0 to 1.0)."""
        ...


class PropertyAnimation(Protocol):
    """Protocol for property animations across platforms.

    Represents animations that can change properties over time,
    whether through Qt property animations or CSS transitions.
    """

    def start(self) -> None:
        """Start the animation."""
        ...

    def stop(self) -> None:
        """Stop the animation."""
        ...

    def set_duration(self, duration: int) -> None:
        """Set the animation duration in milliseconds."""
        ...

    def set_start_value(self, value: Any) -> None:
        """Set the starting value for the animated property."""
        ...

    def set_end_value(self, value: Any) -> None:
        """Set the ending value for the animated property."""
        ...


class AnimationGroup(Protocol):
    """Protocol for animation groups across platforms.

    Represents collections of animations that can be coordinated,
    whether through Qt animation groups or CSS animation coordination.
    """

    def add_animation(self, animation: PropertyAnimation) -> None:
        """Add an animation to the group."""
        ...

    def start(self) -> None:
        """Start all animations in the group."""
        ...

    def stop(self) -> None:
        """Stop all animations in the group."""
        ...


# Type aliases for web compatibility and flexibility
StackWidget = Union[StackContainer, str, Any]  # Container, element ID, or object
OpacityEffectType = Union[OpacityEffect, str, Any]  # Effect, CSS property, or object
PropertyAnimationType = Union[
    PropertyAnimation, str, Any
]  # Animation, CSS transition, or object
AnimationGroupType = Union[AnimationGroup, str, Any]  # Group, CSS animation, or object


@dataclass
class WebImplementationHints:
    """Hints for web implementations of animation protocols.

    These hints help web adapters understand how to implement
    the animation protocols using web technologies.
    """

    stack_widget_strategy: str = "Toggle visibility using CSS display property"
    opacity_effect_strategy: str = "Use CSS opacity property directly"
    property_animation_strategy: str = "Use CSS transitions or Web Animations API"
    animation_group_strategy: str = "Coordinate multiple CSS animations"

    # Performance hints
    use_transform_for_gpu: bool = True
    respect_reduced_motion: bool = True
    fallback_to_immediate: bool = True  # For unsupported browsers


@dataclass
class DesktopImplementationHints:
    """Hints for desktop Qt implementations of animation protocols.

    These hints help Qt adapters understand how to wrap
    existing Qt animation components.
    """

    stack_widget_strategy: str = "Wrap QStackedWidget with adapter"
    opacity_effect_strategy: str = "Wrap QGraphicsOpacityEffect with adapter"
    property_animation_strategy: str = "Wrap QPropertyAnimation with adapter"
    animation_group_strategy: str = "Wrap QParallelAnimationGroup with adapter"

    # Qt-specific hints
    use_graphics_effects: bool = True
    enable_smooth_pixmap_transform: bool = True
    cleanup_effects_on_completion: bool = True
