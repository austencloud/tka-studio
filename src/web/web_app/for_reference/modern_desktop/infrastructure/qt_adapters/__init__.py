"""
Qt-specific adapters for platform-agnostic animation protocols.

This module provides Qt implementations of the animation protocols
defined in core.types.animation, enabling desktop Qt functionality
while maintaining web portability.
"""

from __future__ import annotations

from .animation_adapters import (
    QtAnimationGroupAdapter,
    QtOpacityEffectAdapter,
    QtPropertyAnimationAdapter,
    QtStackAdapter,
)


__all__ = [
    "QtAnimationGroupAdapter",
    "QtOpacityEffectAdapter",
    "QtPropertyAnimationAdapter",
    "QtStackAdapter",
]
