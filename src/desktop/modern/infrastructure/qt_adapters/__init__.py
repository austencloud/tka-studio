"""
Qt-specific adapters for platform-agnostic animation protocols.

This module provides Qt implementations of the animation protocols
defined in core.types.animation, enabling desktop Qt functionality
while maintaining web portability.
"""

from .animation_adapters import (
    QtStackAdapter,
    QtOpacityEffectAdapter,
    QtPropertyAnimationAdapter,
    QtAnimationGroupAdapter,
)

__all__ = [
    "QtStackAdapter",
    "QtOpacityEffectAdapter", 
    "QtPropertyAnimationAdapter",
    "QtAnimationGroupAdapter",
]
