"""
Dependency injection configuration for animation services.
"""

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.animation_interfaces import (
    IAnimationFactory,
    IAnimationService,
    IFadeOrchestrator,
    IFadeSettingsProvider,
    IGraphicsEffectManager,
    IStackAnimationService,
)

from .animation_service import AnimationService
from .core_components import AnimationFactory, GraphicsEffectManager
from .fade_orchestrator import FadeOrchestrator, LegacyFadeManagerAdapter
from .settings_provider import FadeSettingsProvider
from .stack_animation_service import StackAnimationService


class AnimationServiceRegistration:
    """Registers all animation services with the DI container."""

    @staticmethod
    def register_services(container: DIContainer) -> None:
        """Register all animation services with the DI container."""

        # Register core components as singletons
        container.register(
            IGraphicsEffectManager, GraphicsEffectManager, lifecycle="singleton"
        )

        container.register(IAnimationFactory, AnimationFactory, lifecycle="singleton")

        # Register settings provider (depends on ISettingsCoordinator)
        container.register(
            IFadeSettingsProvider, FadeSettingsProvider, lifecycle="singleton"
        )

        # Register main animation service
        container.register(IAnimationService, AnimationService, lifecycle="singleton")

        # Register stack animation service
        container.register(
            IStackAnimationService, StackAnimationService, lifecycle="singleton"
        )

        # Register high-level orchestrator
        container.register(IFadeOrchestrator, FadeOrchestrator, lifecycle="singleton")

        # Register legacy adapter for migration
        container.register(
            LegacyFadeManagerAdapter, LegacyFadeManagerAdapter, lifecycle="singleton"
        )


# For testing purposes, create a simple factory function
