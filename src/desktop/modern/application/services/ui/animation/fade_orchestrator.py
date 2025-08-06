"""
Fade Orchestrator for Desktop Modern Application

This module provides the fade orchestrator implementation for the desktop modern application.
"""

# Use the local implementation
from __future__ import annotations

from .animation_orchestrator import LegacyFadeManagerWrapper
from .modern_service_registration import ModernAnimationOrchestrator


class FadeOrchestrator:
    """Legacy fade orchestrator for compatibility."""

    def __init__(self, orchestrator: ModernAnimationOrchestrator):
        self.orchestrator = orchestrator

    async def fade_and_update(self, widgets, update_callback):
        """Legacy fade and update method."""
        await self.orchestrator.transition_targets(widgets, update_callback)


# Re-export for local imports
__all__ = ["FadeOrchestrator", "LegacyFadeManagerWrapper"]
