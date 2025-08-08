"""
Generation Service Registration

Registers all generation-related services in the dependency injection container.
Part of the modern TKA application's service registration system.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


def register_generation_services(container: DIContainer) -> None:
    """
    Register all generation services in the dependency injection container.

    Args:
        container: DI container to register services in
    """
    try:
        # Import service interfaces
        from desktop.modern.core.interfaces.generation_services import (
            IGenerationService,
            ISequenceConfigurationService,
        )

        # Import service implementations
        from .generation_service import GenerationService
        from .sequence_configuration_service import SequenceConfigurationService

        # Register core generation services with container injection
        # Create a wrapper class that the DI container can instantiate
        class ContainerAwareGenerationService(GenerationService):
            def __init__(self):
                # Get the container from the service locator
                try:
                    from desktop.modern.core.dependency_injection.di_container import (
                        get_container,
                    )

                    container = get_container()
                    super().__init__(container)
                except Exception:
                    # Fallback to no container
                    super().__init__(None)

        container.register_singleton(
            IGenerationService, ContainerAwareGenerationService
        )

        # Register real sequence configuration service
        container.register_singleton(
            ISequenceConfigurationService, SequenceConfigurationService
        )

        logger.info("✅ Generation services registered successfully")

    except Exception as e:
        logger.exception(f"❌ Failed to register generation services: {e!s}")
        raise


class GenerationServiceRegistrationHelper:
    """
    Helper class for generation service registration.

    Provides utilities for registering generation services.
    """

    @staticmethod
    def register_generation_services(container: DIContainer) -> None:
        """Register generation services."""
        register_generation_services(container)

    @staticmethod
    def validate_registration(container: DIContainer) -> bool:
        """
        Validate that generation services are properly registered.

        Args:
            container: DI container to validate

        Returns:
            True if all services are registered correctly
        """
        try:
            from desktop.modern.core.interfaces.generation_services import (
                IGenerationService,
            )

            # Check that all required services can be resolved
            container.resolve(IGenerationService)

            logger.info("✅ Generation service registration validation passed")
            return True

        except Exception as e:
            logger.exception(
                f"❌ Generation service registration validation failed: {e!s}"
            )
            return False
