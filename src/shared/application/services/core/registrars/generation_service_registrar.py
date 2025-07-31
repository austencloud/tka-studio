"""
Generation Service Registrar

Handles registration of generation-related services following microservices architecture.
This registrar manages sequence generation services required for the Generate panel functionality.

Services Registered:
- IGenerationService: Main generation service interface
- GenerationService: Core generation service implementation
"""

import logging
from typing import TYPE_CHECKING

from ..service_registration_manager import BaseServiceRegistrar

if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class GenerationServiceRegistrar(BaseServiceRegistrar):
    """
    Registrar for generation-related services.

    Critical registrar handling sequence generation services required for
    the Generate panel functionality in the application.
    """

    def get_domain_name(self) -> str:
        """Get the name of the service domain this registrar handles."""
        return "Generation Services"

    def is_critical(self) -> bool:
        """Generation services are critical for Generate panel functionality."""
        return True

    def register_services(self, container: "DIContainer") -> None:
        """Register generation services."""
        self._update_progress("Registering generation services...")

        # Register core generation services
        self._register_core_generation_services(container)

        self._update_progress("Generation services registered successfully")

    def _register_core_generation_services(self, container: "DIContainer") -> None:
        """Register core generation services."""
        try:
            # Import service interfaces
            # Import service implementations
            from desktop.modern.application.services.generation.generation_service import (
                GenerationService,
            )
            from desktop.modern.core.interfaces.generation_services import (
                IGenerationService,
            )

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

            self._mark_service_available("IGenerationService")
            logger.info("✅ Core generation services registered successfully")

        except ImportError as e:
            self._handle_service_unavailable(
                "Core generation service", e, "Sequence generation functionality"
            )
        except Exception as e:
            logger.error(f"❌ Failed to register core generation services: {str(e)}")
            raise

    def get_registered_services(self) -> list[str]:
        """Get list of service names registered by this registrar."""
        return [
            "IGenerationService",
            "GenerationService",
        ]

    def get_service_dependencies(self) -> list[str]:
        """
        Get list of service domains this registrar depends on.

        Returns:
            List of dependency domain names
        """
        return [
            "Data Services",  # For pictograph data
            "Positioning Services",  # For arrow positioning
            "Core Services",  # For basic infrastructure
        ]

    def validate_registration(self, container: "DIContainer") -> bool:
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
            logger.error(
                f"❌ Generation service registration validation failed: {str(e)}"
            )
            return False
