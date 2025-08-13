"""
Animation Service for Desktop Modern Application

This module provides the animation service implementation for the desktop modern application.
It imports from the shared animation system to avoid code duplication.
"""

# Import the shared implementation
from __future__ import annotations

from desktop.modern.application.services.ui.animation.animation_service import (
    AnimationService,
)


# Re-export for local imports
__all__ = ["AnimationService"]
