"""
Animation Orchestrator for Desktop Modern Application

This module provides the animation orchestrator implementation for the desktop modern application.
It imports from the shared animation system to avoid code duplication while providing
desktop-specific integration.
"""

# Import the shared implementation
from shared.application.services.ui.animation.animation_orchestrator import (
    ModernAnimationOrchestrator,
    LegacyFadeManagerWrapper,
    create_modern_animation_system
)

# Re-export for local imports
__all__ = [
    'ModernAnimationOrchestrator',
    'LegacyFadeManagerWrapper', 
    'create_modern_animation_system'
]
