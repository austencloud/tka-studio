"""
Sequence Card Services Dependency Injection Registration

Registers all sequence card services with the DI container following
the established patterns for service registration.
"""

from __future__ import annotations

import logging

from shared.application.services.sequence_card.sequence_cache_service import (
    SequenceCardCacheService,
)
from shared.application.services.sequence_card.sequence_data_service import (
    SequenceCardDataService,
)
from shared.application.services.sequence_card.sequence_display_service import (
    SequenceCardDisplayService,
)
from shared.application.services.sequence_card.sequence_settings_service import (
    SequenceCardSettingsService,
)

from desktop.modern.application.services.sequence_card.sequence_export_service import (
    SequenceCardExportService,
)
from desktop.modern.application.services.sequence_card.sequence_layout_service import (
    SequenceCardLayoutService,
)
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.sequence_card_services import (
    ISequenceCardCacheService,
    ISequenceCardDataService,
    ISequenceCardDisplayService,
    ISequenceCardExportService,
    ISequenceCardLayoutService,
    ISequenceCardSettingsService,
)

# Import the actual tab component
from desktop.modern.presentation.views.sequence_card.sequence_card_tab import (
    SequenceCardTab,
)


logger = logging.getLogger(__name__)


def register_sequence_card_services(container: DIContainer) -> None:
    """
    Register all sequence card services with the DI container.

    Args:
        container: DI container to register services with
    """
    try:
        # Core data and cache services (singleton for performance)
        container.register_singleton(ISequenceCardDataService, SequenceCardDataService)
        container.register_singleton(
            ISequenceCardCacheService, SequenceCardCacheService
        )
        container.register_singleton(
            ISequenceCardLayoutService, SequenceCardLayoutService
        )

        # Settings service (singleton for state consistency)
        container.register_singleton(
            ISequenceCardSettingsService, SequenceCardSettingsService
        )

        # Display service (singleton, depends on multiple services)
        container.register_singleton(
            ISequenceCardDisplayService, SequenceCardDisplayService
        )

        # Export service (singleton for operation consistency)
        container.register_singleton(
            ISequenceCardExportService, SequenceCardExportService
        )

        # Register Qt adaptor for display service
        from desktop.modern.presentation.adaptors.sequence_card_display_adaptor import (
            SequenceCardDisplayAdaptor,
        )

        container.register_factory(
            SequenceCardDisplayAdaptor,
            lambda c: SequenceCardDisplayAdaptor(
                c.resolve(ISequenceCardDisplayService)
            ),
        )

        # Register the actual tab component with factory to inject dependencies
        container.register_factory(
            SequenceCardTab,
            lambda c: SequenceCardTab(
                data_service=c.resolve(ISequenceCardDataService),
                cache_service=c.resolve(ISequenceCardCacheService),
                layout_service=c.resolve(ISequenceCardLayoutService),
                display_service=c.resolve(ISequenceCardDisplayService),
                display_adaptor=c.resolve(SequenceCardDisplayAdaptor),
                export_service=c.resolve(ISequenceCardExportService),
                settings_service=c.resolve(ISequenceCardSettingsService),
            ),
        )

    except Exception as e:
        logger.error(f"Failed to register sequence card services: {e}")
        raise


def validate_sequence_card_service_registration(container: DIContainer) -> bool:
    """
    Validate that all sequence card services are properly registered and can be resolved.

    Args:
        container: DI container to validate

    Returns:
        True if all services can be resolved, False otherwise
    """
    try:
        logger.info("Validating sequence card service registration...")

        # Test core service resolution
        data_service = container.resolve(ISequenceCardDataService)
        cache_service = container.resolve(ISequenceCardCacheService)
        layout_service = container.resolve(ISequenceCardLayoutService)
        settings_service = container.resolve(ISequenceCardSettingsService)
        display_service = container.resolve(ISequenceCardDisplayService)
        export_service = container.resolve(ISequenceCardExportService)

        # Test tab component resolution
        sequence_card_tab = container.resolve(SequenceCardTab)

        # Verify services have expected interfaces
        services_to_check = [
            (data_service, ISequenceCardDataService),
            (cache_service, ISequenceCardCacheService),
            (layout_service, ISequenceCardLayoutService),
            (settings_service, ISequenceCardSettingsService),
            (display_service, ISequenceCardDisplayService),
            (export_service, ISequenceCardExportService),
        ]

        for service, interface in services_to_check:
            if not isinstance(service, interface):
                logger.error(f"Service {service} does not implement {interface}")
                return False

        # Verify tab component was created successfully
        if sequence_card_tab is None:
            logger.error("SequenceCardTab could not be created")
            return False

        # Test basic functionality with modern path service
        try:
            from shared.application.services.sequence_card.path_service import (
                SequenceCardPathService,
            )

            path_service = SequenceCardPathService()
            dictionary_path = path_service.get_dictionary_path()

            if dictionary_path.exists():
                sequences = data_service.get_all_sequences(dictionary_path)
                logger.info(f"Found {len(sequences)} sequences in dictionary")
            else:
                logger.warning(f"Dictionary path does not exist: {dictionary_path}")
        except Exception as e:
            logger.warning(f"Could not test dictionary functionality: {e}")

        # Test cache stats
        cache_stats = cache_service.get_cache_stats()
        logger.info(f"Cache initialized with stats: {cache_stats}")

        # Test layout calculations
        grid_dims = layout_service.calculate_grid_dimensions(16)
        logger.info(f"Grid dimensions for length 16: {grid_dims}")

        # Test settings
        last_length = settings_service.get_last_selected_length()
        logger.info(f"Last selected length: {last_length}")

        logger.info(
            "Sequence card service registration validation completed successfully"
        )
        return True

    except Exception as e:
        logger.error(f"Sequence card service registration validation failed: {e}")
        return False


def get_sequence_card_service_dependencies() -> dict:
    """
    Get information about sequence card service dependencies for documentation.

    Returns:
        Dictionary describing service dependencies
    """
    return {
        "core_services": {
            ISequenceCardDataService.__name__: {
                "implementation": SequenceCardDataService.__name__,
                "dependencies": [],
                "description": "Manages sequence data loading and metadata extraction",
            },
            ISequenceCardCacheService.__name__: {
                "implementation": SequenceCardCacheService.__name__,
                "dependencies": [],
                "description": "Provides multi-level LRU caching for images",
            },
            ISequenceCardLayoutService.__name__: {
                "implementation": SequenceCardLayoutService.__name__,
                "dependencies": [],
                "description": "Calculates layout dimensions and scaling",
            },
            ISequenceCardSettingsService.__name__: {
                "implementation": SequenceCardSettingsService.__name__,
                "dependencies": [],
                "description": "Manages settings persistence",
            },
        },
        "coordination_services": {
            ISequenceCardDisplayService.__name__: {
                "implementation": SequenceCardDisplayService.__name__,
                "dependencies": [
                    ISequenceCardDataService.__name__,
                    ISequenceCardCacheService.__name__,
                    ISequenceCardLayoutService.__name__,
                ],
                "description": "Coordinates display operations with batch processing",
            },
            ISequenceCardExportService.__name__: {
                "implementation": SequenceCardExportService.__name__,
                "dependencies": [],
                "description": "Handles export and regeneration operations",
            },
        },
        "external_dependencies": [
            "PIL (Pillow) for image metadata extraction",
            "PyQt6 for UI components",
            "pathlib for modern path handling",
        ],
    }
