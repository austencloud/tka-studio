"""
Modern Animation Service Registration for Desktop Application

This module provides service registration for the modern animation system in the desktop application.
It imports from the shared animation system to avoid code duplication.
"""

# Import the shared implementation
from shared.application.services.ui.animation.modern_service_registration import (
    AnimationSystemFactory,
    ModernAnimationServiceRegistration,
    setup_modern_animation_services,
)

# Re-export for local imports
__all__ = [
    "AnimationSystemFactory",
    "ModernAnimationServiceRegistration",
    "setup_modern_animation_services",
]
