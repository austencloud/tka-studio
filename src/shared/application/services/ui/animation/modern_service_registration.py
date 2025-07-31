"""
Dependency Injection configuration for the modern animation system.
"""

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.animation_core_interfaces import (
    IAnimationOrchestrator,
)

from .animation_orchestrator import (
    LegacyFadeManagerWrapper,
    create_modern_animation_system,
)


class AnimationSystemFactory:
    """Factory interface for animation system creation."""


class ModernAnimationServiceRegistration:
    """Registers modern animation services with the DI container."""

    @staticmethod
    def register_services(container: DIContainer) -> None:
        """Register all modern animation services."""

        # Register factory function that creates the complete system
        def create_animation_system(container):
            # Get settings coordinator if available
            settings_coordinator = None
            try:
                from desktop.modern.core.interfaces.settings_interfaces import (
                    ISettingsCoordinator,
                )

                settings_coordinator = container.resolve(ISettingsCoordinator)
            except:
                pass  # Settings coordinator not available

            orchestrator, legacy_wrapper = create_modern_animation_system(
                settings_coordinator
            )
            return orchestrator, legacy_wrapper

        # Register as factory (singleton behavior handled by caching)
        container.register_factory(AnimationSystemFactory, create_animation_system)

        # Register orchestrator
        def orchestrator_factory(container):
            orchestrator, _ = container.resolve(AnimationSystemFactory)
            return orchestrator

        container.register_factory(IAnimationOrchestrator, orchestrator_factory)

        # Register legacy wrapper for migration
        def legacy_wrapper_factory(container):
            _, legacy_wrapper = container.resolve(AnimationSystemFactory)
            return legacy_wrapper

        container.register_factory(LegacyFadeManagerWrapper, legacy_wrapper_factory)


def setup_modern_animation_services(container: DIContainer) -> None:
    """
    Setup function for modern animation services.

    Call this from your main DI configuration.
    """
    ModernAnimationServiceRegistration.register_services(container)
