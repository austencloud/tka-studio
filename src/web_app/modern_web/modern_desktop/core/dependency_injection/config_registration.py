"""
Configuration Registration for DI Container

Provides utilities for registering configuration objects in the dependency injection container.
Supports both singleton configuration instances and factory-based configuration creation.

USAGE:
    from desktop.modern.core.dependency_injection.config_registration import register_configurations
    from desktop.modern.core.dependency_injection.di_container import get_container

    container = get_container()
    register_configurations(container)

    # Now services can inject configurations
    class MyService:
        def __init__(self, app_config: AppConfig, data_config: DataConfig):
            self.app_config = app_config
            self.data_config = data_config
"""

from __future__ import annotations

import logging

from shared.application.services.data.data_service import DataManager

from desktop.modern.core.config.app_config import (
    AppConfig,
    LoggingConfig,
    PositioningConfig,
    UIConfig,
    create_app_config,
)
from desktop.modern.core.config.data_config import DataConfig, create_data_config
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.positioning_services import IPositionMapper


# Removed Result pattern imports - using simple exceptions

logger = logging.getLogger(__name__)


def register_configurations(
    container, config_override: AppConfig | None = None
) -> None:
    """
    Register all configuration objects in the DI container.

    Args:
        container: DI container instance
        config_override: Optional configuration override for testing

    Raises:
        Exception: If configuration registration fails
    """
    try:
        # Use provided config or create from environment
        if config_override:
            app_config = config_override
        else:
            try:
                app_config = create_app_config()
            except Exception as e:
                logger.error(f"Failed to create app config: {e}")
                raise

        # Register the main app configuration
        container.register_instance(AppConfig, app_config)

        # Register individual configuration components
        container.register_instance(DataConfig, app_config.data_config)
        container.register_instance(PositioningConfig, app_config.positioning)
        container.register_instance(UIConfig, app_config.ui)
        container.register_instance(LoggingConfig, app_config.logging)

        # Register data service with configuration injection
        container.register_factory(
            DataManager, lambda: DataManager(app_config.data_config)
        )

        logger.info("Successfully registered all configurations in DI container")

    except Exception as e:
        logger.error(f"Failed to register configurations: {e}")
        raise


def register_data_config_only(container, data_config: DataConfig | None = None) -> None:
    """
    Register only data configuration (useful for services that only need data access).

    Args:
        container: DI container instance
        data_config: Optional data configuration override

    Returns:
        Result indicating success or failure
    """
    try:
        # Use provided config or create default
        if data_config:
            config = data_config
        else:
            try:
                config = create_data_config()
            except Exception as e:
                logger.error(f"Failed to create data config: {e}")
                raise

        # Register data configuration
        container.register_instance(DataConfig, config)

        # Register data service with configuration injection
        container.register_factory(DataManager, lambda: DataManager(config))

        logger.info("Successfully registered data configuration in DI container")

    except Exception as e:
        logger.error(f"Failed to register data configuration: {e}")
        raise


def register_positioning_services_with_config(
    container: DIContainer, positioning_config: PositioningConfig | None = None
) -> None:
    """
    Register positioning services with configuration injection.

    Args:
        container: DI container instance
        positioning_config: Optional positioning configuration override

    Returns:
        Result indicating success or failure
    """
    try:
        # Use provided config or create default
        if positioning_config:
            config = positioning_config
        else:
            config = PositioningConfig()

        # Register positioning configuration
        container.register_instance(PositioningConfig, config)

        # Note: ArrowAdjustmentLookup and related services are now registered
        # in PositioningServiceRegistrar to ensure proper dependency order

        logger.info("Successfully registered positioning services with configuration")

    except Exception as e:
        logger.error(f"Failed to register positioning services: {e}")
        raise


def create_configured_container(config_override: AppConfig | None = None):
    """
    Create a fully configured DI container with all configurations registered.

    Args:
        config_override: Optional configuration override for testing

    Returns:
        Configured DI container instance

    Raises:
        Exception: If configuration registration fails
    """
    from desktop.modern.core.dependency_injection.di_container import DIContainer

    container = DIContainer()

    # Register configurations
    config_result = register_configurations(container, config_override)
    if config_result.is_failure():
        raise Exception(f"Failed to configure container: {config_result.error}")

    # Register positioning services
    positioning_result = register_positioning_services_with_config(container)
    if positioning_result.is_failure():
        raise Exception(
            f"Failed to register positioning services: {positioning_result.error}"
        )

    return container


def validate_configuration_registration(container) -> bool:
    """
    Validate that all required configurations are properly registered.

    Args:
        container: DI container instance

    Returns:
        Result indicating validation success or failure
    """
    try:
        required_configs = [
            AppConfig,
            DataConfig,
            PositioningConfig,
            UIConfig,
            LoggingConfig,
        ]

        for config_type in required_configs:
            try:
                instance = container.resolve(config_type)
                if instance is None:
                    logger.error(
                        f"Configuration {config_type.__name__} resolved to None"
                    )
                    return False
            except Exception as e:
                logger.error(
                    f"Failed to resolve configuration {config_type.__name__}: {e}"
                )
                return False

        # Validate data service can be resolved
        try:
            data_service = container.resolve(DataManager)
            if data_service is None:
                logger.error("DataService resolved to None")
                return False
        except Exception as e:
            logger.error(f"Failed to resolve DataService: {e}")
            return False

        logger.info("All configuration registrations validated successfully")
        return True

    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        raise


def register_start_position_services(container: DIContainer) -> None:
    """
    Register start position services in the DI container.

    Args:
        container: DI container instance

    Raises:
        Exception: If service registration fails
    """
    try:
        # Import start position interfaces
        # Import start position service implementations
        from shared.application.services.start_position.start_position_data_service import (
            StartPositionDataService,
        )
        from shared.application.services.start_position.start_position_selection_service import (
            StartPositionSelectionService,
        )

        from desktop.modern.application.services.start_position import (
            StartPositionOrchestrator,
            StartPositionSelectionService,
            StartPositionUIService,
        )
        from desktop.modern.core.interfaces.start_position_services import (
            IStartPositionDataService,
            IStartPositionOrchestrator,
            IStartPositionSelectionService,
            IStartPositionUIService,
        )

        # Register individual services
        container.register_singleton(
            IStartPositionDataService, StartPositionDataService
        )
        container.register_singleton(
            IStartPositionSelectionService, StartPositionSelectionService
        )
        container.register_singleton(IStartPositionUIService, StartPositionUIService)
        container.register_singleton(
            IStartPositionOrchestrator, StartPositionOrchestrator
        )

        logger.debug("Successfully registered start position services")

    except Exception as e:
        logger.error(f"Failed to register start position services: {e}")
        raise


def register_extracted_services(container: DIContainer) -> None:
    """
    Register extracted business logic services.

    Args:
        container: DI container instance

    Returns:
        Result indicating success or failure
    """
    try:
        # Register position matching service
        from shared.application.services.positioning.position_mapper import (
            PositionMapper,
        )

        container.register_singleton(IPositionMapper, PositionMapper)

        # Register start position services
        register_start_position_services(container)

        # Note: BeatLoadingService was removed during SRP refactoring
        # Its functionality was split into focused microservices

        # Register positioning services using ServiceRegistrationManager
        try:
            from shared.application.services.core.service_registration_manager import (
                ServiceRegistrationCoordinator,
            )

            registration_coordinator = ServiceRegistrationCoordinator()
            registration_coordinator.register_all_services(container)
            logger.debug(
                "Successfully registered all services including positioning services"
            )
        except Exception as e:
            logger.warning(f"Failed to register services: {e}")
            # Don't fail the entire registration process

        # Register sequence card services
        try:
            from desktop.modern.core.dependency_injection.sequence_card_service_registration import (
                register_sequence_card_services,
            )

            register_sequence_card_services(container)
            logger.debug("Successfully registered sequence card services")
        except Exception as e:
            logger.warning(f"Failed to register sequence card services: {e}")
            # Don't fail the entire registration process

        # Register construct tab services
        try:
            from desktop.modern.core.dependency_injection.construct_tab_service_registration import (
                register_construct_tab_services,
                register_legacy_compatibility_services,
            )

            register_construct_tab_services(container)
            register_legacy_compatibility_services(container)
            logger.debug("Successfully registered construct tab services")
        except Exception as e:
            logger.warning(f"Failed to register construct tab services: {e}")
            # Don't fail the entire registration process

        # DI registration log removed to reduce startup noise

    except Exception as e:
        logger.error(f"Failed to register extracted services: {e}")
        raise
