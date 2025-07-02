"""
Application Factory for creating different TKA application variants.

This factory creates different "flavors" of the application:
- Production: Full PyQt UI with file persistence
- Test: Mock services with in-memory storage
- Headless: Real logic without UI components
- Recording: Production services with recording layer
"""

from typing import Optional
import sys
import logging
from core.dependency_injection.di_container import (
    DIContainer,
    get_container,
    reset_container,
)

logger = logging.getLogger(__name__)

# Import existing service interfaces
from core.interfaces.core_services import (
    ILayoutService,
    ISettingsService,
    ISequenceDataService,
    IValidationService,
    IArrowManagementService,
    ISequenceManagementService,
    IPictographManagementService,
    IUIStateManagementService,
)
from core.interfaces.session_services import ISessionStateService

# Import production services
from application.services.layout.layout_management_service import (
    LayoutManagementService,
)
from application.services.ui.ui_state_management_service import UIStateManagementService
from application.services.core.sequence_management_service import (
    SequenceManagementService,
)
from application.services.core.pictograph_management_service import (
    PictographManagementService,
)
from application.services.core.session_state_service import SessionStateService
from application.services.settings.settings_service import SettingsService

# Import file-based storage services
from infrastructure.storage.file_based_sequence_data_service import (
    FileBasedSequenceDataService,
)
from infrastructure.storage.file_based_settings_service import FileBasedSettingsService

# Import file system services
from core.interfaces.organization_services import IFileSystemService
from infrastructure.file_system.file_system_service import FileSystemService

logger = logging.getLogger(__name__)
# Import test doubles (to be created) - using try/except for graceful fallback
try:
    from infrastructure.test_doubles.mock_services import (
        InMemorySequenceDataService,
        MockLayoutService,
        InMemorySettingsService,
        MockValidationService,
        MockArrowManagementService,
        MockSequenceManagementService,
        MockPictographManagementService,
        MockUIStateManagementService,
    )

    from infrastructure.test_doubles.headless_services import (
        HeadlessLayoutService,
        HeadlessUIStateManagementService,
    )

    TEST_DOUBLES_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Test doubles not available: {e}")
    TEST_DOUBLES_AVAILABLE = False


class ApplicationMode:
    """Application mode constants."""

    PRODUCTION = "production"
    TEST = "test"
    HEADLESS = "headless"
    RECORDING = "recording"


class ApplicationFactory:
    """
    Factory for creating different variants of the TKA application.

    Uses the existing DI container to register different service implementations
    based on the application mode required.
    """

    @staticmethod
    def create_production_app() -> DIContainer:
        """
        Create production application with full PyQt UI and file persistence.

        Returns:
            DIContainer configured with production services
        """
        container = DIContainer()

        # Register file-based data services
        container.register_singleton(ISequenceDataService, FileBasedSequenceDataService)
        container.register_singleton(ISettingsService, FileBasedSettingsService)
        container.register_singleton(IFileSystemService, FileSystemService)

        # Register production services
        container.register_singleton(ILayoutService, LayoutManagementService)
        container.register_singleton(
            IUIStateManagementService, UIStateManagementService
        )
        container.register_singleton(
            ISequenceManagementService, SequenceManagementService
        )
        container.register_singleton(
            IPictographManagementService, PictographManagementService
        )

        # Register session service
        container.register_singleton(ISessionStateService, SessionStateService)

        # Register visibility service
        from core.interfaces.tab_settings_interfaces import IVisibilityService
        from application.services.settings.visibility_service import VisibilityService

        container.register_singleton(IVisibilityService, VisibilityService)

        # Register pictograph context service
        from core.interfaces.core_services import IPictographContextService
        from application.services.ui.pictograph_context_service import (
            PictographContextService,
        )

        container.register_singleton(
            IPictographContextService, PictographContextService
        )

        # TODO: Register remaining production services when identified:
        # container.register_singleton(IValidationService, ProductionValidationService)
        # container.register_singleton(IArrowManagementService, ProductionArrowManagementService)

        logger.info("Created production application container")
        return container

    @staticmethod
    def create_test_app() -> DIContainer:
        """
        Create test application with mock services and in-memory storage.
        Perfect for AI agent testing - no UI, no files, fast execution.

        Returns:
            DIContainer configured with test double services
        """
        if not TEST_DOUBLES_AVAILABLE:
            raise ImportError(
                "Test doubles are not available. Cannot create test application."
            )

        container = DIContainer()

        # Register test doubles
        container.register_singleton(ISequenceDataService, InMemorySequenceDataService)
        container.register_singleton(ILayoutService, MockLayoutService)
        container.register_singleton(ISettingsService, InMemorySettingsService)
        container.register_singleton(IValidationService, MockValidationService)
        container.register_singleton(
            IArrowManagementService, MockArrowManagementService
        )
        container.register_singleton(
            ISequenceManagementService, MockSequenceManagementService
        )
        container.register_singleton(
            IPictographManagementService, MockPictographManagementService
        )
        container.register_singleton(
            IUIStateManagementService, MockUIStateManagementService
        )
        container.register_singleton(IFileSystemService, FileSystemService)

        # Register session service
        container.register_singleton(ISessionStateService, SessionStateService)

        # Register visibility service
        from core.interfaces.tab_settings_interfaces import IVisibilityService
        from application.services.settings.visibility_service import VisibilityService

        container.register_singleton(IVisibilityService, VisibilityService)

        # Register pictograph context service
        from core.interfaces.core_services import IPictographContextService
        from application.services.ui.pictograph_context_service import (
            PictographContextService,
        )

        container.register_singleton(
            IPictographContextService, PictographContextService
        )

        logger.info("Created test application container")
        return container

    @staticmethod
    def create_headless_app() -> DIContainer:
        """
        Create headless application with real business logic but no UI.
        Useful for server-side processing or CI/CD environments.

        Returns:
            DIContainer configured with headless services
        """
        if not TEST_DOUBLES_AVAILABLE:
            raise ImportError(
                "Test doubles are not available. Cannot create headless application."
            )

        container = DIContainer()

        # Register file-based data services (same as production)
        container.register_singleton(ISequenceDataService, FileBasedSequenceDataService)
        container.register_singleton(ISettingsService, FileBasedSettingsService)
        container.register_singleton(IFileSystemService, FileSystemService)

        # Real business logic services
        container.register_singleton(
            ISequenceManagementService, SequenceManagementService
        )
        container.register_singleton(
            IPictographManagementService, PictographManagementService
        )

        # Headless UI services
        container.register_singleton(ILayoutService, HeadlessLayoutService)
        container.register_singleton(
            IUIStateManagementService, HeadlessUIStateManagementService
        )

        # Register session service
        container.register_singleton(ISessionStateService, SessionStateService)

        # Register visibility service
        from core.interfaces.tab_settings_interfaces import IVisibilityService
        from application.services.settings.visibility_service import VisibilityService

        container.register_singleton(IVisibilityService, VisibilityService)

        # Register pictograph context service
        from core.interfaces.core_services import IPictographContextService
        from application.services.ui.pictograph_context_service import (
            PictographContextService,
        )

        container.register_singleton(
            IPictographContextService, PictographContextService
        )

        # TODO: Register remaining production services when identified:
        # container.register_singleton(IValidationService, ProductionValidationService)
        # container.register_singleton(IArrowManagementService, ProductionArrowManagementService)

        logger.info("Created headless application container")
        return container

    @staticmethod
    def create_recording_app() -> DIContainer:
        """
        Create recording application that wraps production services with recording.
        Used for capturing user workflows to convert into automated tests.

        Returns:
            DIContainer configured with recording-wrapped services
        """
        # Start with production app
        container = ApplicationFactory.create_production_app()

        # TODO: Wrap services with recording decorators (implement in future hack)
        # This is placeholder for Hack #4

        logger.info("Created recording application container")
        return container

    @staticmethod
    def create_app(mode: str = ApplicationMode.PRODUCTION) -> DIContainer:
        """
        Create application based on mode string.

        Args:
            mode: Application mode (production, test, headless, recording)

        Returns:
            DIContainer configured for the specified mode

        Raises:
            ValueError: If mode is not recognized
        """
        if mode == ApplicationMode.PRODUCTION:
            return ApplicationFactory.create_production_app()
        elif mode == ApplicationMode.TEST:
            return ApplicationFactory.create_test_app()
        elif mode == ApplicationMode.HEADLESS:
            return ApplicationFactory.create_headless_app()
        elif mode == ApplicationMode.RECORDING:
            return ApplicationFactory.create_recording_app()
        else:
            raise ValueError(f"Unknown application mode: {mode}")

    @staticmethod
    def create_app_from_args(args: Optional[list] = None) -> DIContainer:
        """
        Create application based on command line arguments.

        Args:
            args: Command line arguments (defaults to sys.argv)

        Returns:
            DIContainer configured based on command line arguments
        """
        if args is None:
            args = sys.argv

        if "--test" in args:
            return ApplicationFactory.create_test_app()
        elif "--headless" in args:
            return ApplicationFactory.create_headless_app()
        elif "--record" in args:
            return ApplicationFactory.create_recording_app()
        else:
            return ApplicationFactory.create_production_app()


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
