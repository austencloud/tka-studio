"""
Fade Orchestrator for Desktop Modern Application

This module provides the fade orchestrator implementation for the desktop modern application.
It imports from the shared animation system to avoid code duplication.
"""

# Import the shared implementation
from shared.application.services.ui.animation.fade_orchestrator import (
    FadeOrchestrator,
    LegacyFadeManagerWrapper
)

# Re-export for local imports
__all__ = [
    'FadeOrchestrator',
    'LegacyFadeManagerWrapper'
]
