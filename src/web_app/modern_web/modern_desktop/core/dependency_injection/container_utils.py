"""
DI Container Utilities

Provides utility functions for working with the dependency injection container,
including initialization helpers for testing and development.
"""

from __future__ import annotations

import logging


logger = logging.getLogger(__name__)


def ensure_container_initialized(force_reinit: bool = False) -> bool:
    """
    Ensure the DI container is properly initialized with all services.

    This function checks if the container has services registered and initializes
    them if needed. Useful for testing and development scenarios where you need
    a fully configured container.

    Args:
        force_reinit: If True, force re-registration of services even if already present

    Returns:
        bool: True if container is properly initialized, False if initialization failed
    """
    try:
        from desktop.modern.core.dependency_injection.di_container import get_container
        from desktop.modern.core.interfaces.positioning_services import (
            IArrowLocationCalculator,
        )

        container = get_container()

        # Check if services are already registered (unless forcing reinit)
        if not force_reinit:
            try:
                # Try to resolve a key service to check if container is initialized
                container.resolve(IArrowLocationCalculator)
                logger.debug("DI container already initialized with services")
                return True
            except Exception:
                # Services not registered, need to initialize
                pass

        # Register all services
        logger.info("Initializing DI container with all services...")
        from shared.application.services.core.service_registration_manager import (
            ServiceRegistrationManager,
        )

        service_manager = ServiceRegistrationManager()
        service_manager.register_all_services(container)

        # Verify initialization by testing a key service
        container.resolve(IArrowLocationCalculator)
        logger.info("DI container successfully initialized with all services")
        return True

    except Exception as e:
        logger.error(f"Failed to initialize DI container: {e}")
        return False


def get_initialized_container():
    """
    Get a DI container that is guaranteed to be initialized with all services.

    This is a convenience function that combines getting the container and
    ensuring it's initialized. Useful for testing and development.

    Returns:
        DIContainer: Fully initialized container

    Raises:
        RuntimeError: If container initialization fails
    """
    if not ensure_container_initialized():
        raise RuntimeError("Failed to initialize DI container with services")

    from desktop.modern.core.dependency_injection.di_container import get_container

    return get_container()


def validate_positioning_services() -> bool:
    """
    Validate that all positioning services can be resolved from the container.

    This function attempts to resolve all positioning service interfaces to
    ensure they're properly registered and can be instantiated.

    Returns:
        bool: True if all positioning services are available, False otherwise
    """
    try:
        from desktop.modern.core.dependency_injection.di_container import get_container
        from desktop.modern.core.interfaces.positioning_services import (
            IArrowAdjustmentCalculator,
            IArrowCoordinateSystemService,
            IArrowLocationCalculator,
            IArrowPositioningOrchestrator,
            IArrowRotationCalculator,
        )

        container = get_container()

        # Test all positioning service interfaces
        positioning_services = [
            IArrowLocationCalculator,
            IArrowRotationCalculator,
            IArrowAdjustmentCalculator,
            IArrowCoordinateSystemService,
            IArrowPositioningOrchestrator,
        ]

        for service_interface in positioning_services:
            try:
                service = container.resolve(service_interface)
                if service is None:
                    logger.error(
                        f"Service {service_interface.__name__} resolved to None"
                    )
                    return False
            except Exception as e:
                logger.error(f"Failed to resolve {service_interface.__name__}: {e}")
                return False

        logger.debug("All positioning services validated successfully")
        return True

    except Exception as e:
        logger.error(f"Error during positioning services validation: {e}")
        return False


def reset_container_for_testing():
    """
    Reset the global DI container for testing purposes.

    This function clears the global container state, useful for ensuring
    clean state between tests.
    """
    try:
        from desktop.modern.core.dependency_injection.di_container import (
            reset_container,
        )

        reset_container()
        logger.debug("DI container reset for testing")
    except Exception as e:
        logger.warning(f"Failed to reset DI container: {e}")


def create_test_container():
    """
    Create a fresh DI container for testing with all services registered.

    This function creates a new container instance and registers all services,
    useful for isolated testing scenarios.

    Returns:
        DIContainer: Fresh container with all services registered

    Raises:
        RuntimeError: If container creation or service registration fails
    """
    try:
        from shared.application.services.core.service_registration_manager import (
            ServiceRegistrationManager,
        )

        from desktop.modern.core.dependency_injection.di_container import DIContainer

        # Create fresh container
        container = DIContainer()

        # Register all services
        service_manager = ServiceRegistrationManager()
        service_manager.register_all_services(container)

        logger.debug("Created fresh test container with all services")
        return container

    except Exception as e:
        logger.error(f"Failed to create test container: {e}")
        raise RuntimeError(f"Test container creation failed: {e}")


def get_service_registration_status() -> dict:
    """
    Get the current status of service registration in the DI container.

    Returns a dictionary with information about which services are registered
    and available for resolution.

    Returns:
        dict: Status information about registered services
    """
    try:
        from desktop.modern.core.dependency_injection.di_container import get_container
        from desktop.modern.core.interfaces.positioning_services import (
            IArrowAdjustmentCalculator,
            IArrowCoordinateSystemService,
            IArrowLocationCalculator,
            IArrowPositioningOrchestrator,
            IArrowRotationCalculator,
        )

        container = get_container()
        status = {
            "container_available": True,
            "services": {},
            "total_registered": 0,
            "positioning_services_available": 0,
        }

        # Check positioning services
        positioning_services = {
            "IArrowLocationCalculator": IArrowLocationCalculator,
            "IArrowRotationCalculator": IArrowRotationCalculator,
            "IArrowAdjustmentCalculator": IArrowAdjustmentCalculator,
            "IArrowCoordinateSystemService": IArrowCoordinateSystemService,
            "IArrowPositioningOrchestrator": IArrowPositioningOrchestrator,
        }

        for service_name, service_interface in positioning_services.items():
            try:
                service = container.resolve(service_interface)
                status["services"][service_name] = {
                    "available": True,
                    "type": type(service).__name__,
                }
                status["positioning_services_available"] += 1
            except Exception as e:
                status["services"][service_name] = {
                    "available": False,
                    "error": str(e),
                }

        status["total_registered"] = len(
            [s for s in status["services"].values() if s["available"]]
        )

        return status

    except Exception as e:
        return {
            "container_available": False,
            "error": str(e),
            "services": {},
            "total_registered": 0,
            "positioning_services_available": 0,
        }
