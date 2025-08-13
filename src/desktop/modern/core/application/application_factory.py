"""
Application Factory for creating different TKA application variants - FIXED VERSION

This factory creates different "flavors" of the application:
- Production: Full PyQt UI with file persistence
- Test: Mock services with in-memory storage
- Headless: Real logic without UI components
- Recording: Production services with recording layer

FIXES APPLIED:
- ✅ Extracted common service registration to eliminate duplication
- ✅ Standardized error handling using StandardErrorHandler
- ✅ Improved dependency ordering
- ✅ Better separation of concerns
"""

from __future__ import annotations

import logging
import sys

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.error_handling import ErrorSeverity, StandardErrorHandler

from .service_registration_helper import (
    ServiceRegistrationHelper,
    TestDoubleRegistrationHelper,
)


logger = logging.getLogger(__name__)


class ApplicationMode:
    """Application mode constants."""

    PRODUCTION = "production"
    TEST = "test"


class ApplicationFactory:
    """
    Factory for creating different variants of the TKA application.

    FIXED: Uses ServiceRegistrationHelper to eliminate code duplication
    and provides better error handling throughout.
    """

    @staticmethod
    def create_production_app() -> DIContainer:
        """
        Create production application with full PyQt UI and file persistence.

        Returns:
            DIContainer configured with production services
        """
        try:
            container = DIContainer()

            # CRITICAL: Set this container as the global container immediately
            ApplicationFactory._set_global_container(container)

            # Register configurations first (required by services)
            from desktop.modern.core.dependency_injection.config_registration import (
                register_configurations,
            )

            register_configurations(container)

            # Use helper to register common services (eliminates duplication)
            ServiceRegistrationHelper.register_all_common_services(container)

            # Register production-specific services
            ApplicationFactory._register_production_specific_services(container)

            # Apply service registration manager for additional services
            ServiceRegistrationHelper.apply_service_registration_manager(container)

            # Register extracted services
            ServiceRegistrationHelper.register_extracted_services_with_error_handling(
                container
            )

            logger.info("✅ Production application container created successfully")
            return container

        except Exception as e:
            StandardErrorHandler.handle_initialization_error(
                "Production application creation", e, logger, is_critical=True
            )
            raise

    @staticmethod
    def create_test_app() -> DIContainer:
        """
        Create test application with mock services and in-memory storage.
        Perfect for AI agent testing - no UI, no files, fast execution.

        Returns:
            DIContainer configured with test double services
        """
        try:
            container = DIContainer()

            # Register configurations first (required by services)
            from desktop.modern.core.dependency_injection.config_registration import (
                register_configurations,
            )

            register_configurations(container)

            # Register test doubles
            TestDoubleRegistrationHelper.register_test_doubles(container)

            # Register common services that work with test doubles
            ApplicationFactory._register_test_specific_services(container)

            # Register common services that are safe for testing
            ServiceRegistrationHelper.register_visibility_services(container)

            # Register extracted services
            ServiceRegistrationHelper.register_extracted_services_with_error_handling(
                container
            )

            # Set this container as the global container
            ApplicationFactory._set_global_container(container)

            logger.info("✅ Test application container created successfully")
            return container

        except ImportError as e:
            StandardErrorHandler.handle_initialization_error(
                "Test application creation",
                e,
                logger,
                is_critical=True,
                suggested_action="Ensure test doubles are available",
            )
            raise
        except Exception as e:
            StandardErrorHandler.handle_initialization_error(
                "Test application creation", e, logger, is_critical=True
            )
            raise

    @staticmethod
    def create_app(mode: str = ApplicationMode.PRODUCTION) -> DIContainer:
        """
        Create application based on mode string.

        Args:
            mode: Application mode (production, test, headless)

        Returns:
            DIContainer configured for the specified mode

        Raises:
            ValueError: If mode is not recognized
        """
        mode_creators = {
            ApplicationMode.PRODUCTION: ApplicationFactory.create_production_app,
            ApplicationMode.TEST: ApplicationFactory.create_test_app,
        }

        creator = mode_creators.get(mode)
        if not creator:
            raise ValueError(f"Unknown application mode: {mode}")

        try:
            return creator()
        except Exception as e:
            StandardErrorHandler.handle_initialization_error(
                f"Application creation (mode: {mode})", e, logger, is_critical=True
            )
            raise

    @staticmethod
    def create_app_from_args(args: list | None = None) -> DIContainer:
        """
        Create application based on command line arguments.

        Args:
            args: Command line arguments (defaults to sys.argv)

        Returns:
            DIContainer configured based on command line arguments
        """
        if args is None:
            args = sys.argv

        mode_mapping = {
            "--test": ApplicationMode.TEST,
        }

        for arg, mode in mode_mapping.items():
            if arg in args:
                return ApplicationFactory.create_app(mode)

        # Default to production
        return ApplicationFactory.create_app(ApplicationMode.PRODUCTION)

    # Helper methods for specific service registration

    @staticmethod
    def _set_global_container(container: DIContainer) -> None:
        """Set the global container with error handling."""
        try:
            from desktop.modern.core.dependency_injection.di_container import (
                set_container,
            )

            set_container(container)
            logger.debug(f"🌐 Global container set: {id(container)}")
        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Global container setting", e, logger, ErrorSeverity.WARNING
            )

    @staticmethod
    def _register_production_specific_services(container: DIContainer) -> None:
        """Register services specific to production mode."""
        # Production mode uses all the common services
        # Any production-specific services would go here
        logger.debug("🏭 Production-specific services registered")

    @staticmethod
    def _register_test_specific_services(container: DIContainer) -> None:
        """Register services specific to test mode."""
        try:
            from desktop.modern.application.services.core.session_state_tracker import (
                SessionStateTracker,
            )
            from desktop.modern.core.interfaces.organization_services import (
                IFileSystemService,
            )
            from desktop.modern.core.interfaces.session_services import (
                ISessionStateTracker,
            )
            from desktop.modern.infrastructure.file_system.file_system_service import (
                FileSystemService,
            )

            # Register some real services that are safe for testing
            container.register_singleton(IFileSystemService, FileSystemService)
            container.register_singleton(ISessionStateTracker, SessionStateTracker)

            logger.debug("🧪 Test-specific services registered")

        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Test-specific services registration", e, logger, ErrorSeverity.WARNING
            )

    @staticmethod
    def _register_headless_business_services(container: DIContainer) -> None:
        """Register real business logic services for headless mode."""
        try:
            from desktop.modern.application.services.core.session_state_tracker import (
                SessionStateTracker,
            )
            from desktop.modern.application.services.pictograph.pictograph_csv_manager import (
                PictographCSVManager,
            )
            from desktop.modern.application.services.sequence.sequence_beat_operations import (
                SequenceBeatOperations,
            )
            from desktop.modern.core.interfaces.core_services import (
                IPictographManager,
                ISequenceManager,
            )
            from desktop.modern.core.interfaces.session_services import (
                ISessionStateTracker,
            )

            container.register_singleton(ISequenceManager, SequenceBeatOperations)
            container.register_singleton(IPictographManager, PictographCSVManager)
            container.register_singleton(ISessionStateTracker, SessionStateTracker)

            logger.debug("💼 Headless business services registered")

        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Headless business services registration",
                e,
                logger,
                ErrorSeverity.WARNING,
            )


# Convenience functions for easy access
def get_production_app() -> DIContainer:
    """Get production application container."""
    return ApplicationFactory.create_production_app()


def get_test_app() -> DIContainer:
    """Get test application container."""
    return ApplicationFactory.create_test_app()


def get_headless_app() -> DIContainer:
    """Get headless application container."""
    return ApplicationFactory.create_headless_app()
