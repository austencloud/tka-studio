"""
Core types module for framework-agnostic data structures.
"""

from __future__ import annotations

from .animation import (
    AnimationGroup,
    AnimationGroupType,
    DesktopImplementationHints,
    OpacityEffect,
    OpacityEffectType,
    PropertyAnimation,
    PropertyAnimationType,
    StackContainer,
    StackWidget,
    WebImplementationHints,
)
from .geometry import (
    Point,
    PointType,
    Rect,
    RectType,
    Size,
    SizeType,
    Widget,
    WidgetType,
)


__all__ = [
    # Geometry types
    "Size",
    "Point",
    "Rect",
    "Widget",
    "SizeType",
    "PointType",
    "RectType",
    "WidgetType",
    # Animation types
    "StackWidget",
    "OpacityEffectType",
    "PropertyAnimationType",
    "AnimationGroupType",
    "StackContainer",
    "OpacityEffect",
    "PropertyAnimation",
    "AnimationGroup",
    "WebImplementationHints",
    "DesktopImplementationHints",
]
