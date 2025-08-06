"""
Animation Orchestrator for Desktop Modern Application

This module provides the animation orchestrator implementation for the desktop modern application.
"""

# Use the local implementation from modern_service_registration
from __future__ import annotations

from .modern_service_registration import ModernAnimationOrchestrator


class LegacyFadeManagerWrapper:
    """Legacy wrapper for compatibility."""

    def __init__(self, orchestrator: ModernAnimationOrchestrator):
        self.orchestrator = orchestrator
        self.widget_fader = self  # For legacy compatibility

    def fade_widgets(self, widgets, fade_in: bool):
        """Legacy fade widgets method."""
        import asyncio

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Create a task if loop is already running
                asyncio.create_task(self.orchestrator.fade_targets(widgets, fade_in))
            else:
                # Run in new loop if no loop is running
                loop.run_until_complete(
                    self.orchestrator.fade_targets(widgets, fade_in)
                )
        except Exception:
            # Fallback - do nothing
            pass


def create_modern_animation_system(container):
    """Create a modern animation system."""
    from desktop.modern.core.interfaces.animation_core_interfaces import (
        IAnimationOrchestrator,
    )

    orchestrator = container.resolve(IAnimationOrchestrator)
    return {
        "orchestrator": orchestrator,
        "legacy_wrapper": LegacyFadeManagerWrapper(orchestrator),
    }


# Re-export for local imports
__all__ = [
    "LegacyFadeManagerWrapper",
    "ModernAnimationOrchestrator",
    "create_modern_animation_system",
]
