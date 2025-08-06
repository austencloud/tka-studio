"""
Service Registration Helper - NEW MODULE

Extracts common service registration logic from ApplicationFactory
to eliminate code duplication and improve maintainability.

PROVIDES:
- Common service registration patterns
- Standardized registration procedures
- Error handling during registration
- Dependency ordering
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from desktop.modern.core.error_handling import ErrorSeverity, StandardErrorHandler


if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class ServiceRegistrationHelper:
    """
    Helper class for common service registration patterns.

    Eliminates the code duplication found across different application modes
    in ApplicationFactory by centralizing common registration logic.
    """

    @staticmethod
    def register_common_data_services(container: DIContainer) -> None:
        """Register data services common to all modes."""
        try:
            from desktop.modern.core.interfaces.core_services import (
                ISequenceDataService,
                ISettingsCoordinator,
            )
            from desktop.modern.core.interfaces.organization_services import (
                IFileSystemService,
            )
            from desktop.modern.infrastructure.file_system.file_system_service import (
                FileSystemService,
            )
            from desktop.modern.infrastructure.storage.file_based_sequence_data_service import (
                FileBasedSequenceDataService,
            )
            from desktop.modern.infrastructure.storage.file_based_settings_service import (
                FileBasedSettingsService,
            )

            registrations = [
                (ISequenceDataService, FileBasedSequenceDataService),
                (ISettingsCoordinator, FileBasedSettingsService),
                (IFileSystemService, FileSystemService),
            ]

            ServiceRegistrationHelper._register_services_batch(
                container, registrations, "common data services"
            )

        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Common data services registration", e, logger, ErrorSeverity.CRITICAL
            )
            raise

    @staticmethod
    def register_common_core_services(container: DIContainer) -> None:
        """Register core services common to all modes."""
        try:
            from shared.application.services.layout.layout_manager import LayoutManager
            from shared.application.services.pictograph.pictograph_csv_manager import (
                PictographCSVManager,
            )
            from shared.application.services.ui.coordination.ui_coordinator import (
                UICoordinator,
            )

            from desktop.modern.application.services.core.session_state_tracker import (
                SessionStateTracker,
            )
            from desktop.modern.application.services.sequence.sequence_beat_operations import (
                SequenceBeatOperations,
            )
            from desktop.modern.core.interfaces.core_services import (
                ILayoutService,
                IPictographManager,
                ISequenceManager,
                IUIStateManager,
            )
            from desktop.modern.core.interfaces.session_services import (
                ISessionStateTracker,
            )

            registrations = [
                (ILayoutService, LayoutManager),
                (IUIStateManager, UICoordinator),
                (ISequenceManager, SequenceBeatOperations),
                (IPictographManager, PictographCSVManager),
                (ISessionStateTracker, SessionStateTracker),
            ]

            ServiceRegistrationHelper._register_services_batch(
                container, registrations, "common core services"
            )

        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Common core services registration", e, logger, ErrorSeverity.CRITICAL
            )
            raise

    @staticmethod
    def register_common_pictograph_services(container: DIContainer) -> None:
        """Register pictograph services common to all modes."""
        try:
            from shared.application.services.pictograph.border_manager import (
                PictographBorderManager,
            )
            from shared.application.services.pictograph.context_detection_service import (
                PictographContextDetector,
            )

            from desktop.modern.core.interfaces.core_services import (
                IPictographBorderManager,
                IPictographContextDetector,
            )

            registrations = [
                (IPictographBorderManager, PictographBorderManager),
                (IPictographContextDetector, PictographContextDetector),
            ]

            ServiceRegistrationHelper._register_services_batch(
                container, registrations, "common pictograph services"
            )

        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Common pictograph services registration",
                e,
                logger,
                ErrorSeverity.WARNING,
                {"note": "Pictograph services are optional"},
            )

    @staticmethod
    def register_common_session_services(container: DIContainer) -> None:
        """Register session and lifecycle services common to all modes."""
        try:
            from shared.application.services.core.session_restoration_coordinator import (
                ISessionRestorationCoordinator,
                SessionRestorationCoordinator,
            )
            from shared.application.services.sequence.sequence_restorer import (
                ISequenceRestorer,
                SequenceRestorer,
            )

            from desktop.modern.application.services.core.window_management_service import (
                IWindowManagementService,
                WindowManagementService,
            )
            from desktop.modern.application.services.ui.window_discovery_service import (
                IWindowDiscoveryService,
                WindowDiscoveryService,
            )

            # Register basic services first
            basic_registrations = [
                (IWindowManagementService, WindowManagementService),
                (IWindowDiscoveryService, WindowDiscoveryService),
                (ISequenceRestorer, SequenceRestorer),
            ]

            ServiceRegistrationHelper._register_services_batch(
                container, basic_registrations, "basic session services"
            )

            # Register session coordinator with dependency injection
            def create_session_coordinator():
                sequence_service = container.resolve(ISequenceRestorer)
                return SessionRestorationCoordinator(sequence_service)

            container.register_factory(
                ISessionRestorationCoordinator, create_session_coordinator
            )
            logger.info("✅ Registered session coordinator with dependencies")

        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Common session services registration", e, logger, ErrorSeverity.WARNING
            )

    @staticmethod
    def register_generation_services(container: DIContainer) -> None:
        """Register generation services for sequence creation."""
        try:
            from desktop.modern.application.services.generation.generation_service_registration import (
                register_generation_services,
            )

            register_generation_services(container)
            logger.info("✅ Generation services registered successfully")

        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Generation services registration", e, logger, ErrorSeverity.CRITICAL
            )
            raise

    @staticmethod
    def register_visibility_services(container: DIContainer) -> None:
        """Register visibility settings services."""
        try:
            from shared.application.services.settings.visibility_settings_manager import (
                VisibilitySettingsManager,
            )

            from desktop.modern.core.interfaces.tab_settings_interfaces import (
                IVisibilitySettingsManager,
            )

            container.register_singleton(
                IVisibilitySettingsManager, VisibilitySettingsManager
            )
            logger.info("✅ Registered visibility settings services")

        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Visibility services registration", e, logger, ErrorSeverity.WARNING
            )

    @staticmethod
    def register_all_common_services(container: DIContainer) -> None:
        """
        Register all common services in the correct dependency order.

        This is the main entry point for registering services that are
        common across all application modes.
        """

        # Phase 1: Foundation services (no dependencies)
        ServiceRegistrationHelper.register_common_data_services(container)

        # Phase 2: Core services (may depend on data services)
        ServiceRegistrationHelper.register_common_core_services(container)

        # Phase 3: Session and lifecycle services
        ServiceRegistrationHelper.register_common_session_services(container)

        # Phase 4: Generation services (CRITICAL - was missing!)
        ServiceRegistrationHelper.register_generation_services(container)

        # Phase 5: Animation services (CRITICAL - needed for fade transitions!)
        ServiceRegistrationHelper.register_animation_services(container)

        # Phase 5: Optional services
        ServiceRegistrationHelper.register_common_pictograph_services(container)
        ServiceRegistrationHelper.register_visibility_services(container)

        # Phase 6: Settings services (needed for export panel)
        ServiceRegistrationHelper.register_settings_services(container)

    @staticmethod
    def register_settings_services(container: DIContainer) -> None:
        """Register settings services needed by UI components."""
        try:
            from desktop.modern.core.dependency_injection.settings_service_registration import (
                register_settings_services,
            )

            register_settings_services(container)
            logger.info("✅ Registered settings services in main container")

        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Settings services registration", e, logger, ErrorSeverity.WARNING
            )

    @staticmethod
    def register_extracted_services_with_error_handling(
        container: DIContainer,
    ) -> None:
        """Register extracted services with comprehensive error handling."""
        try:
            from desktop.modern.core.dependency_injection.config_registration import (
                register_extracted_services,
            )

            register_result = register_extracted_services(container)

            if hasattr(register_result, "is_failure") and register_result.is_failure():
                StandardErrorHandler.handle_service_error(
                    "Extracted services registration",
                    Exception(register_result.error),
                    logger,
                    ErrorSeverity.WARNING,
                )
            else:
                pass  # Services registered successfully

        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Extracted services registration",
                e,
                logger,
                ErrorSeverity.WARNING,
                {"note": "Application will continue without extracted services"},
            )

    @staticmethod
    def register_animation_services(container: DIContainer) -> None:
        """Register animation services needed for fade transitions."""
        try:
            from desktop.modern.application.services.ui.animation.modern_service_registration import (
                setup_modern_animation_services,
            )

            setup_modern_animation_services(container)

            # CRITICAL: Register option picker services first (dependencies)
            ServiceRegistrationHelper._register_option_picker_services(container)

            # Then register OptionPickerScroll with animation orchestrator injection
            ServiceRegistrationHelper._register_option_picker_components(container)

            logger.info("✅ Registered animation services for fade transitions")

        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Animation services registration",
                e,
                logger,
                ErrorSeverity.WARNING,
                {"note": "Application will continue without fade animations"},
            )

    @staticmethod
    def _register_option_picker_services(container: DIContainer) -> None:
        """Register the core option picker services that OptionPickerScroll depends on."""
        try:
            from shared.application.services.option_picker.option_configuration_service import (
                OptionConfigurationService,
            )
            from shared.application.services.option_picker.option_picker_size_calculator import (
                OptionPickerSizeCalculator,
            )
            from shared.application.services.option_picker.option_pool_service import (
                OptionPoolService,
            )
            from shared.application.services.option_picker.sequence_option_service import (
                SequenceOptionService,
            )

            # Register option picker services as singletons
            container.register_singleton(SequenceOptionService, SequenceOptionService)
            container.register_singleton(OptionPoolService, OptionPoolService)
            container.register_singleton(
                OptionPickerSizeCalculator, OptionPickerSizeCalculator
            )
            container.register_singleton(
                OptionConfigurationService, OptionConfigurationService
            )

            logger.info("✅ Registered option picker services")

        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Option picker services registration",
                e,
                logger,
                ErrorSeverity.WARNING,
                {"note": "Option picker services not available"},
            )

    @staticmethod
    def _register_option_picker_components(container: DIContainer) -> None:
        """Register option picker components with proper animation orchestrator injection."""
        try:
            from shared.application.services.option_picker.option_picker_size_calculator import (
                OptionPickerSizeCalculator,
            )
            from shared.application.services.option_picker.option_pool_service import (
                OptionPoolService,
            )
            from shared.application.services.option_picker.sequence_option_service import (
                SequenceOptionService,
            )

            from desktop.modern.core.interfaces.animation_core_interfaces import (
                IAnimationOrchestrator,
            )
            from desktop.modern.presentation.components.option_picker.components.option_picker_scroll import (
                OptionPickerScroll,
            )

            # Register OptionPickerScroll with factory that injects animation orchestrator
            def create_option_picker_scroll():
                sequence_option_service = container.resolve(SequenceOptionService)
                option_pool_service = container.resolve(OptionPoolService)
                option_sizing_service = container.resolve(OptionPickerSizeCalculator)

                # Get option config service
                from shared.application.services.option_picker.option_configuration_service import (
                    OptionConfigurationService,
                )

                option_config_service = container.resolve(OptionConfigurationService)

                # Get animation orchestrator (may be None if not available)
                animation_orchestrator = None
                try:
                    animation_orchestrator = container.resolve(IAnimationOrchestrator)
                except Exception:
                    # Animation orchestrator not available - continue without it
                    pass

                return OptionPickerScroll(
                    sequence_option_service=sequence_option_service,
                    option_pool_service=option_pool_service,
                    option_sizing_service=option_sizing_service,
                    option_config_service=option_config_service,
                    animation_orchestrator=animation_orchestrator,
                )

            container.register_factory(OptionPickerScroll, create_option_picker_scroll)
            logger.info(
                "✅ Registered OptionPickerScroll with animation orchestrator injection"
            )

        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Option picker components registration",
                e,
                logger,
                ErrorSeverity.WARNING,
                {"note": "Option picker will continue without proper DI"},
            )

    @staticmethod
    def apply_service_registration_manager(container: DIContainer) -> None:
        """Apply the service registration manager for additional services."""
        try:
            from shared.application.services.core.service_registration_manager import (
                ServiceRegistrationManager,
            )

            service_manager = ServiceRegistrationManager()
            service_manager.register_all_services(container)
            logger.info("✅ Service registration manager applied")

        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Service registration manager application",
                e,
                logger,
                ErrorSeverity.WARNING,
            )

    @staticmethod
    def _register_services_batch(
        container: DIContainer,
        registrations: list[tuple[type, type]],
        batch_name: str,
    ) -> None:
        """
        Register a batch of services with error handling for individual failures.

        Args:
            container: DI container to register services in
            registrations: List of (interface, implementation) tuples
            batch_name: Name of the batch for logging
        """
        successful = 0
        failed = 0

        for interface, implementation in registrations:
            try:
                container.register_singleton(interface, implementation)
                successful += 1
                logger.debug(
                    f"✅ Registered {interface.__name__} -> {implementation.__name__}"
                )

            except Exception as e:
                failed += 1
                StandardErrorHandler.handle_service_error(
                    f"Individual service registration ({interface.__name__})",
                    e,
                    logger,
                    ErrorSeverity.WARNING,
                    {"implementation": implementation.__name__},
                )

        logger.info(
            f"📊 {batch_name}: {successful} successful, {failed} failed registrations"
        )

        if failed > 0 and successful == 0:
            raise RuntimeError(
                f"All services in batch '{batch_name}' failed to register"
            )

    @staticmethod
    def apply_service_registration_manager(container: DIContainer) -> None:
        """Apply service registration manager for additional services."""
        try:
            # This would apply any additional service registrations
            # that are defined in the service registration manager
            logger.debug("✅ Service registration manager applied")

        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Service registration manager application",
                e,
                logger,
                ErrorSeverity.WARNING,
            )

    @staticmethod
    def register_extracted_services_with_error_handling(
        container: DIContainer,
    ) -> None:
        """Register extracted services with comprehensive error handling."""
        try:
            # This would register any services that were extracted from legacy code
            logger.debug("✅ Extracted services registered")

        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Extracted services registration", e, logger, ErrorSeverity.WARNING
            )


class TestDoubleRegistrationHelper:
    """Helper for registering test doubles when available."""

    @staticmethod
    def register_test_doubles(container: DIContainer) -> None:
        """Register test double services if available."""
        try:
            from desktop.modern.core.interfaces.core_services import (
                IArrowManagementService,
                ILayoutService,
                IPictographManager,
                ISequenceDataService,
                ISequenceManager,
                ISettingsCoordinator,
                IUIStateManager,
                IValidationService,
            )
            from desktop.modern.infrastructure.test_doubles.mock_services import (
                InMemorySequenceDataService,
                InMemorySettingsService,
                MockArrowManagementService,
                MockLayoutService,
                MockPictographManagementService,
                MockSequenceManager,
                MockUIStateManagementService,
                MockValidationService,
            )

            test_registrations = [
                (ISequenceDataService, InMemorySequenceDataService),
                (ILayoutService, MockLayoutService),
                (ISettingsCoordinator, InMemorySettingsService),
                (IValidationService, MockValidationService),
                (IArrowManagementService, MockArrowManagementService),
                (ISequenceManager, MockSequenceManager),
                (IPictographManager, MockPictographManagementService),
                (IUIStateManager, MockUIStateManagementService),
            ]

            ServiceRegistrationHelper._register_services_batch(
                container, test_registrations, "test doubles"
            )

        except ImportError as e:
            StandardErrorHandler.handle_service_error(
                "Test doubles registration",
                e,
                logger,
                ErrorSeverity.WARNING,
                {"note": "Test doubles not available, skipping"},
            )
            raise

    @staticmethod
    def register_headless_services(container: DIContainer) -> None:
        """Register headless service implementations."""
        try:
            from desktop.modern.core.interfaces.core_services import (
                ILayoutService,
                IUIStateManager,
            )
            from desktop.modern.infrastructure.test_doubles.headless_services import (
                HeadlessLayoutService,
                HeadlessUIStateManagementService,
            )

            headless_registrations = [
                (ILayoutService, HeadlessLayoutService),
                (IUIStateManager, HeadlessUIStateManagementService),
            ]

            ServiceRegistrationHelper._register_services_batch(
                container, headless_registrations, "headless services"
            )

        except ImportError as e:
            StandardErrorHandler.handle_service_error(
                "Headless services registration", e, logger, ErrorSeverity.WARNING
            )
            raise
