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
    "AnimationGroup",
    "AnimationGroupType",
    "DesktopImplementationHints",
    "OpacityEffect",
    "OpacityEffectType",
    "Point",
    "PointType",
    "PropertyAnimation",
    "PropertyAnimationType",
    "Rect",
    "RectType",
    # Geometry types
    "Size",
    "SizeType",
    "StackContainer",
    # Animation types
    "StackWidget",
    "WebImplementationHints",
    "Widget",
    "WidgetType",
]
