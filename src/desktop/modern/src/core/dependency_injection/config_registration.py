"""
Configuration Registration for DI Container

Provides utilities for registering configuration objects in the dependency injection container.
Supports both singleton configuration instances and factory-based configuration creation.

USAGE:
    from core.dependency_injection.config_registration import register_configurations
    from core.dependency_injection.di_container import get_container

    container = get_container()
    register_configurations(container)

    # Now services can inject configurations
    class MyService:
        def __init__(self, app_config: AppConfig, data_config: DataConfig):
            self.app_config = app_config
            self.data_config = data_config
"""

import logging
from typing import Optional

from core.types.result import (
    Result,
    AppError,
    ErrorType,
    success,
    failure,
    app_error,
)
from core.config.app_config import (
    AppConfig,
    PositioningConfig,
    UIConfig,
    LoggingConfig,
    create_app_config,
)
from core.config.data_config import DataConfig, create_data_config
from application.services.data.data_service import DataService
from core.interfaces.positioning_services import IPositionMatchingService
from core.interfaces.core_services import IBeatLoadingService, IObjectPoolService

logger = logging.getLogger(__name__)


def register_configurations(
    container, config_override: Optional[AppConfig] = None
) -> Result[bool, AppError]:
    """
    Register all configuration objects in the DI container.

    Args:
        container: DI container instance
        config_override: Optional configuration override for testing

    Returns:
        Result indicating success or failure
    """
    try:
        # Use provided config or create from environment
        if config_override:
            app_config = config_override
        else:
            config_result = create_app_config()
            if config_result.is_failure():
                return failure(config_result.error)
            app_config = config_result.value

        # Register the main app configuration
        container.register_instance(AppConfig, app_config)

        # Register individual configuration components
        container.register_instance(DataConfig, app_config.data_config)
        container.register_instance(PositioningConfig, app_config.positioning)
        container.register_instance(UIConfig, app_config.ui)
        container.register_instance(LoggingConfig, app_config.logging)

        # Register data service with configuration injection
        container.register_factory(
            DataService, lambda: DataService(app_config.data_config)
        )

        logger.info("Successfully registered all configurations in DI container")
        return success(True)

    except Exception as e:
        return failure(
            app_error(
                ErrorType.DEPENDENCY_INJECTION_ERROR,
                f"Failed to register configurations: {e}",
                cause=e,
            )
        )


def register_data_config_only(
    container, data_config: Optional[DataConfig] = None
) -> Result[bool, AppError]:
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
            config_result = create_data_config()
            if config_result.is_failure():
                return failure(config_result.error)
            config = config_result.value

        # Register data configuration
        container.register_instance(DataConfig, config)

        # Register data service with configuration injection
        container.register_factory(DataService, lambda: DataService(config))

        logger.info("Successfully registered data configuration in DI container")
        return success(True)

    except Exception as e:
        return failure(
            app_error(
                ErrorType.DEPENDENCY_INJECTION_ERROR,
                f"Failed to register data configuration: {e}",
                cause=e,
            )
        )


def register_positioning_services_with_config(
    container, positioning_config: Optional[PositioningConfig] = None
) -> Result[bool, AppError]:
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

        # Register the new focused arrow adjustment services
        from application.services.positioning.arrows.orchestration.arrow_adjustment_lookup_service import (
            ArrowAdjustmentLookupService,
        )
        from application.services.positioning.arrows.orchestration.directional_tuple_processor import (
            DirectionalTupleProcessor,
        )
        from application.services.positioning.arrows.orchestration.arrow_adjustment_calculator_service import (
            ArrowAdjustmentCalculatorService,
        )

        # Register the focused services
        container.register_singleton(
            ArrowAdjustmentLookupService, ArrowAdjustmentLookupService
        )
        container.register_singleton(
            DirectionalTupleProcessor, DirectionalTupleProcessor
        )
        container.register_singleton(
            ArrowAdjustmentCalculatorService, ArrowAdjustmentCalculatorService
        )

        logger.info("Successfully registered positioning services with configuration")
        return success(True)

    except Exception as e:
        return failure(
            app_error(
                ErrorType.DEPENDENCY_INJECTION_ERROR,
                f"Failed to register positioning services: {e}",
                cause=e,
            )
        )


def create_configured_container(config_override: Optional[AppConfig] = None):
    """
    Create a fully configured DI container with all configurations registered.

    Args:
        config_override: Optional configuration override for testing

    Returns:
        Configured DI container instance

    Raises:
        Exception: If configuration registration fails
    """
    from core.dependency_injection.di_container import DIContainer

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


def validate_configuration_registration(container) -> Result[bool, AppError]:
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
                    return failure(
                        app_error(
                            ErrorType.DEPENDENCY_INJECTION_ERROR,
                            f"Configuration {config_type.__name__} resolved to None",
                            {"config_type": config_type.__name__},
                        )
                    )
            except Exception as e:
                return failure(
                    app_error(
                        ErrorType.DEPENDENCY_INJECTION_ERROR,
                        f"Failed to resolve configuration {config_type.__name__}: {e}",
                        {"config_type": config_type.__name__},
                        e,
                    )
                )

        # Validate data service can be resolved
        try:
            data_service = container.resolve(DataService)
            if data_service is None:
                return failure(
                    app_error(
                        ErrorType.DEPENDENCY_INJECTION_ERROR,
                        "DataService resolved to None",
                    )
                )
        except Exception as e:
            return failure(
                app_error(
                    ErrorType.DEPENDENCY_INJECTION_ERROR,
                    f"Failed to resolve DataService: {e}",
                    cause=e,
                )
            )

        logger.info("All configuration registrations validated successfully")
        return success(True)

    except Exception as e:
        return failure(
            app_error(
                ErrorType.DEPENDENCY_INJECTION_ERROR,
                f"Configuration validation failed: {e}",
                cause=e,
            )
        )


def register_extracted_services(container) -> Result[bool, AppError]:
    """
    Register extracted business logic services.

    Args:
        container: DI container instance

    Returns:
        Result indicating success or failure
    """
    try:
        # Register position matching service
        from application.services.positioning.position_matching_service import (
            PositionMatchingService,
        )

        container.register_singleton(IPositionMatchingService, PositionMatchingService)

        # Register beat loading service
        from application.services.data.beat_loading_service import BeatLoadingService

        container.register_singleton(IBeatLoadingService, BeatLoadingService)

        # Register object pool service
        from application.services.core.object_pool_service import ObjectPoolService

        container.register_singleton(IObjectPoolService, ObjectPoolService)

        logger.info("Successfully registered extracted services in DI container")
        return success(True)

    except Exception as e:
        return failure(
            app_error(
                ErrorType.DEPENDENCY_INJECTION_ERROR,
                f"Failed to register extracted services: {e}",
                cause=e,
            )
        )
