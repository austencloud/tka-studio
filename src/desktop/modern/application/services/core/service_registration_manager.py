"""
Service Registration Manager

Pure service for managing dependency injection service registration.
Extracted from KineticConstructorModern to follow single responsibility principle.

PROVIDES:
- Core service registration
- Motion service registration
- Layout service registration
- Pictograph service registration
- Event system registration

REFACTORING NOTE:
This file is being refactored into specialized registrars following microservices architecture.
The goal is to split this large manager into focused, domain-specific registrars.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import logging
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


# ============================================================================
# BASE REGISTRATION INFRASTRUCTURE
# ============================================================================


class IServiceRegistrar(ABC):
    """
    Interface for service registrars in the microservices registration architecture.

    Each registrar is responsible for registering a specific domain of services
    (e.g., positioning services, data services, etc.) following single responsibility principle.
    """

    @abstractmethod
    def register_services(self, container: DIContainer) -> None:
        """Register all services for this domain in the DI container."""

    @abstractmethod
    def get_domain_name(self) -> str:
        """Get the name of the service domain this registrar handles."""

    @abstractmethod
    def get_registered_services(self) -> list[str]:
        """Get list of service names registered by this registrar."""

    @abstractmethod
    def is_critical(self) -> bool:
        """Return True if this registrar's services are critical for application startup."""


class BaseServiceRegistrar(IServiceRegistrar):
    """
    Base implementation for service registrars providing common functionality.

    Provides:
    - Progress tracking integration
    - Service availability tracking
    - Graceful degradation for optional services
    - Standardized error handling
    """

    def __init__(self, progress_callback: callable | None = None):
        """Initialize with optional progress callback."""
        self.progress_callback = progress_callback
        self._service_availability: dict[str, bool] = {}
        self._registered_services: list[str] = []

    def get_registered_services(self) -> list[str]:
        """Get list of service names registered by this registrar."""
        return self._registered_services.copy()

    def get_service_availability(self) -> dict[str, bool]:
        """Get availability status of services in this domain."""
        return self._service_availability.copy()

    def _update_progress(self, message: str) -> None:
        """Update progress if callback is available."""
        if self.progress_callback:
            self.progress_callback(message)

    def _mark_service_available(self, service_name: str) -> None:
        """Mark a service as successfully registered."""
        self._service_availability[service_name] = True
        if service_name not in self._registered_services:
            self._registered_services.append(service_name)

    def _mark_service_unavailable(self, service_name: str) -> None:
        """Mark a service as failed to register."""
        self._service_availability[service_name] = False

    def _handle_service_unavailable(
        self, service_name: str, error: Exception, functionality_impact: str
    ) -> None:
        """
        Standardized handling for unavailable optional services.

        Args:
            service_name: Name of the service that failed to register
            error: The exception that occurred
            functionality_impact: Description of what functionality is affected
        """
        logger.warning(f"{service_name} not available: {error}")
        logger.warning(f"Impact: {service_name} will not be available")
        logger.warning(f"Functionality affected: {functionality_impact}")
        self._mark_service_unavailable(service_name)


# ============================================================================
# NEW REGISTRATION COORDINATOR (LIGHTWEIGHT)
# ============================================================================


class ServiceRegistrationCoordinator:
    """
    Lightweight coordinator for the new microservices registration architecture.

    Delegates registration to specialized registrars while maintaining:
    - Progress tracking across all registrars
    - Service availability monitoring
    - Graceful degradation for optional services
    - Dependency ordering

    This replaces the monolithic ServiceRegistrationManager with a clean,
    maintainable architecture following single responsibility principle.
    """

    def __init__(self, progress_callback: callable | None = None):
        """Initialize coordinator with optional progress callback."""
        self.progress_callback = progress_callback
        self._registrars: list[IServiceRegistrar] = []
        self._registration_completed = False
        self._initialize_registrars()

    def _initialize_registrars(self) -> None:
        """Initialize all specialized registrars in dependency order."""
        from .registrars import (
            AnimationServiceRegistrar,
            CoreServiceRegistrar,
            DataServiceRegistrar,
            GenerationServiceRegistrar,
            GraphEditorServiceRegistrar,
            LearnServiceRegistrar,
            MotionServiceRegistrar,
            OptionPickerServiceRegistrar,
            PictographServiceRegistrar,
            PositioningServiceRegistrar,
            SequenceCardServiceRegistrar,
            SequenceServiceRegistrar,
            StartPositionServiceRegistrar,
            WorkbenchServiceRegistrar,
            WriteServiceRegistrar,
        )

        # Initialize registrars in dependency order
        # Critical services first, then optional services
        self._registrars = [
            # Phase 1: Foundation services (no dependencies)
            MotionServiceRegistrar(self.progress_callback),
            DataServiceRegistrar(self.progress_callback),
            # Phase 2: Core services (may depend on data/motion)
            CoreServiceRegistrar(self.progress_callback),
            SequenceServiceRegistrar(self.progress_callback),
            PictographServiceRegistrar(self.progress_callback),
            StartPositionServiceRegistrar(
                self.progress_callback
            ),  # Add start position services
            WorkbenchServiceRegistrar(self.progress_callback),
            # Phase 3: Complex services (depend on core services)
            PositioningServiceRegistrar(self.progress_callback),
            GenerationServiceRegistrar(
                self.progress_callback
            ),  # Add generation services
            OptionPickerServiceRegistrar(self.progress_callback),
            # Phase 4: Optional services
            GraphEditorServiceRegistrar(self.progress_callback),
            AnimationServiceRegistrar(self.progress_callback),
            LearnServiceRegistrar(self.progress_callback),
            SequenceCardServiceRegistrar(self.progress_callback),
            WriteServiceRegistrar(self.progress_callback),
        ]

    def register_all_services(self, container: DIContainer) -> None:
        """Register all services using specialized registrars."""
        # Prevent multiple registrations
        if self._registration_completed:
            logger.info(
                "[SERVICE_MANAGER] Services already registered, skipping duplicate registration"
            )
            return

        self._update_progress("Configuring services with new registrar architecture...")

        critical_failures = []
        optional_failures = []

        for registrar in self._registrars:
            try:
                print(f"[SERVICE_MANAGER] Registering {registrar.get_domain_name()}...")
                registrar.register_services(container)
                self._update_progress(f"{registrar.get_domain_name()} configured")
                print(f"[SERVICE_MANAGER] {registrar.get_domain_name()} completed")

            except Exception as e:
                if registrar.is_critical():
                    critical_failures.append((registrar.get_domain_name(), e))
                else:
                    optional_failures.append((registrar.get_domain_name(), e))
                    logger.warning(
                        f"Optional service domain failed: {registrar.get_domain_name()}: {e}"
                    )

        # Report results
        if critical_failures:
            error_msg = f"Critical service registration failures: {critical_failures}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        if optional_failures:
            logger.warning(
                f"Optional service failures (application will continue): {optional_failures}"
            )

        self._update_progress("Services configured with new registrar architecture")
        self._registration_completed = True

    def get_registration_status(self) -> dict:
        """Get comprehensive status of service registration across all registrars."""
        status = {
            "registrar_count": len(self._registrars),
            "registrars": {},
            "total_services": 0,
            "available_services": 0,
            "critical_registrars": 0,
            "optional_registrars": 0,
        }

        for registrar in self._registrars:
            domain_name = registrar.get_domain_name()
            registrar_services = registrar.get_registered_services()

            if hasattr(registrar, "get_service_availability"):
                availability = registrar.get_service_availability()
                available_count = sum(availability.values())
            else:
                available_count = len(registrar_services)
                availability = dict.fromkeys(registrar_services, True)

            status["registrars"][domain_name] = {
                "is_critical": registrar.is_critical(),
                "services": registrar_services,
                "service_count": len(registrar_services),
                "available_count": available_count,
                "availability": availability,
            }

            status["total_services"] += len(registrar_services)
            status["available_services"] += available_count

            if registrar.is_critical():
                status["critical_registrars"] += 1
            else:
                status["optional_registrars"] += 1

        return status

    def _update_progress(self, message: str) -> None:
        """Update progress if callback is available."""
        if self.progress_callback:
            self.progress_callback(message)


# ============================================================================
# LEGACY INTERFACE (BACKWARD COMPATIBILITY)
# ============================================================================


class IServiceRegistrationManager(ABC):
    """Interface for service registration operations."""

    @abstractmethod
    def register_all_services(self, container: DIContainer) -> None:
        """Register all application services in the DI container."""


class ServiceRegistrationManager(IServiceRegistrationManager):
    """
    BACKWARD COMPATIBILITY WRAPPER for the new microservices registration architecture.

    This class maintains the same interface as the original ServiceRegistrationManager
    but delegates to the new ServiceRegistrationCoordinator internally. This allows
    existing code to continue working without changes while benefiting from the new
    architecture.

    MIGRATION NOTE: New code should use ServiceRegistrationCoordinator directly.
    This wrapper will be deprecated once all consumers are migrated.
    """

    def __init__(self, progress_callback: callable | None = None):
        """Initialize with optional progress callback."""
        self.progress_callback = progress_callback
        self._registration_completed = False

        # Delegate to the new coordinator
        self._coordinator = ServiceRegistrationCoordinator(progress_callback)

        # Legacy service availability tracking for backward compatibility
        self._service_availability = {
            "event_system": False,
            "arrow_positioning": False,
            "prop_management": False,
            "prop_orchestration": False,
        }

    def register_all_services(self, container: DIContainer) -> None:
        """
        Register all application services in the DI container.

        BACKWARD COMPATIBILITY: Delegates to the new ServiceRegistrationCoordinator
        while maintaining the same interface for existing code.
        """
        # Prevent multiple registrations
        if self._registration_completed:
            logger.info(
                "[SERVICE_MANAGER] Services already registered, skipping duplicate registration"
            )
            return

        # Delegate to the new coordinator for most services
        self._coordinator.register_all_services(container)

        # Register remaining services that haven't been migrated to registrars yet
        self._register_remaining_legacy_services(container)

        self._update_progress("Services configured")
        self._registration_completed = True

    def _register_remaining_legacy_services(self, container: DIContainer) -> None:
        """Register services that haven't been migrated to specialized registrars yet."""
        # All services are now handled by specialized registrars!
        # This method is kept for backward compatibility but no longer needed.

    def get_registration_status(self) -> dict:
        """
        Get comprehensive status of service registration.

        BACKWARD COMPATIBILITY: Combines status from the new coordinator
        with legacy service availability tracking.
        """
        # Get status from the new coordinator
        coordinator_status = self._coordinator.get_registration_status()

        # Combine with legacy format for backward compatibility
        legacy_status = {
            "event_system_available": self._service_availability["event_system"],
            "arrow_positioning_available": self._service_availability[
                "arrow_positioning"
            ],
            "prop_management_available": self._service_availability["prop_management"],
            "prop_orchestration_available": self._service_availability[
                "prop_orchestration"
            ],
            "services_registered": True,
            "availability_summary": {
                "total_optional_services": len(self._service_availability),
                "available_services": sum(self._service_availability.values()),
                "missing_services": [
                    service
                    for service, available in self._service_availability.items()
                    if not available
                ],
            },
        }

        # Merge coordinator status with legacy status
        legacy_status.update(
            {
                "coordinator_status": coordinator_status,
                "total_services_new_architecture": coordinator_status["total_services"],
                "available_services_new_architecture": coordinator_status[
                    "available_services"
                ],
            }
        )

        return legacy_status

    def _update_progress(self, message: str) -> None:
        """Update progress if callback is available."""
        if self.progress_callback:
            self.progress_callback(message)

    def _handle_service_unavailable(
        self, service_name: str, error: Exception, functionality_impact: str
    ) -> None:
        """
        Standardized handling for unavailable optional services.

        Args:
            service_name: Name of the service that failed to register
            error: The exception that occurred
            functionality_impact: Description of what functionality is affected
        """
        logger.warning(f"{service_name} not available: {error}")
        logger.warning(f"Impact: {service_name} will not be available")
        logger.warning(f"Functionality affected: {functionality_impact}")

        # Update availability tracking
        service_key = service_name.lower().replace(" ", "_")
        if service_key in self._service_availability:
            self._service_availability[service_key] = False
