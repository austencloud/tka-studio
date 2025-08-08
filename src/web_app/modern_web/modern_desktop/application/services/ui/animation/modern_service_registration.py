"""
Modern Animation Service Registration for Desktop Application

This module provides service registration for the modern animation system in the desktop application.
"""

from __future__ import annotations

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.animation_core_interfaces import (
    IAnimationEngine,
    IAnimationOrchestrator,
)


class ModernAnimationOrchestrator:
    """Simple animation orchestrator implementation."""

    def __init__(self, engine: IAnimationEngine):
        self.engine = engine

    async def fade_target(self, target, fade_in: bool, config=None):
        """Fade a target in or out."""
        # Simple implementation - just return an ID
        return "fade_animation_id"

    async def fade_targets(self, targets, fade_in: bool, config=None):
        """Fade multiple targets."""
        return [await self.fade_target(target, fade_in, config) for target in targets]

    async def transition_targets(self, targets, update_callback, config=None):
        """Fade out, update, then fade in."""
        # Execute the update callback immediately for now
        if update_callback:
            update_callback()

    async def execute_command(self, command):
        """Execute an animation command."""
        return True


def setup_modern_animation_services(container: DIContainer) -> None:
    """Register animation services in the DI container."""
    try:
        from desktop.modern.core.animation.animation_engine import (
            create_default_animation_engine,
        )

        # Register animation engine
        engine = create_default_animation_engine()
        container.register_instance(IAnimationEngine, engine)

        # Register animation orchestrator
        orchestrator = ModernAnimationOrchestrator(engine)
        container.register_instance(IAnimationOrchestrator, orchestrator)

    except Exception:
        # If registration fails, register a no-op orchestrator
        class NoOpOrchestrator:
            async def fade_target(self, target, fade_in: bool, config=None):
                return "noop_id"

            async def fade_targets(self, targets, fade_in: bool, config=None):
                return ["noop_id"] * len(targets)

            async def transition_targets(self, targets, update_callback, config=None):
                if update_callback:
                    update_callback()

            async def execute_command(self, command):
                return True

        container.register_instance(IAnimationOrchestrator, NoOpOrchestrator())


class AnimationSystemFactory:
    """Factory for creating animation system components."""

    pass


class ModernAnimationServiceRegistration:
    """Service registration helper."""

    pass


# Re-export for local imports
__all__ = [
    "AnimationSystemFactory",
    "ModernAnimationServiceRegistration",
    "setup_modern_animation_services",
]
