"""
Browse Service Registration

Register browse-related services with the dependency injection container.
"""

import logging
from pathlib import Path

from desktop.modern.application.services.browse.sequence_deletion_service import (
    SequenceDeletionService,
)
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.browse_services import (
    IBrowseActionHandler,
    IBrowseDataManager,
    IBrowseNavigationManager,
    IBrowseService,
    IDictionaryDataManager,
    IProgressiveLoadingService,
    ISequenceDeletionService,
)
from desktop.modern.core.interfaces.image_export_services import (
    ISequenceImageExporter,
    ISequenceMetadataExtractor,
)

logger = logging.getLogger(__name__)


def register_browse_services(
    container: DIContainer,
    sequences_dir: Path,
    data_dir: Path,
    stacked_widget=None,
    viewer_panel=None,
    parent_widget=None,
) -> None:
    """
    Register browse services with the DI container.

    Args:
        container: The dependency injection container
        sequences_dir: Directory containing sequence files
        data_dir: Directory containing dictionary data
        stacked_widget: Optional stacked widget for navigation
        viewer_panel: Optional viewer panel
        parent_widget: Optional parent widget for dialogs
    """
    logger.info("Registering browse services...")

    try:
        # Register core services
        container.register_factory(
            ISequenceDeletionService, lambda: SequenceDeletionService(sequences_dir)
        )

        # Register image export services
        from desktop.modern.application.services.image_export.sequence_image_exporter import (
            SequenceImageExporter,
        )
        from shared.application.services.image_export.sequence_metadata_extractor import (
            SequenceMetadataExtractor,
        )

        container.register_singleton(ISequenceImageExporter, SequenceImageExporter)
        container.register_singleton(
            ISequenceMetadataExtractor, SequenceMetadataExtractor
        )

        # Register browse service
        from desktop.modern.presentation.tabs.browse.services.browse_service import (
            BrowseService,
        )

        container.register_factory(IBrowseService, lambda: BrowseService(sequences_dir))

        # Register dictionary data manager
        from desktop.modern.presentation.tabs.browse.services.modern_dictionary_data_manager import (
            ModernDictionaryDataManager,
        )

        container.register_factory(
            IDictionaryDataManager, lambda: ModernDictionaryDataManager(data_dir)
        )

        # Register progressive loading service
        from desktop.modern.presentation.tabs.browse.services.progressive_loading_service import (
            ProgressiveLoadingService,
        )

        container.register_factory(
            IProgressiveLoadingService,
            lambda c: ProgressiveLoadingService(c.resolve(IDictionaryDataManager)),
        )

        # Register data manager
        from desktop.modern.presentation.tabs.browse.managers.browse_data_manager import (
            BrowseDataManager,
        )

        container.register_factory(
            IBrowseDataManager,
            lambda c: BrowseDataManager(data_dir, c.resolve(IDictionaryDataManager)),
        )

        # Register navigation manager if stacked widget provided
        if stacked_widget is not None:
            from desktop.modern.presentation.tabs.browse.managers.browse_navigation_manager import (
                BrowseNavigationManager,
            )

            container.register_factory(
                IBrowseNavigationManager,
                lambda: BrowseNavigationManager(stacked_widget, viewer_panel),
            )

        # Register action handler if parent widget provided
        if parent_widget:
            from desktop.modern.presentation.tabs.browse.managers.browse_action_handler import (
                BrowseActionHandler,
            )

            container.register_factory(
                IBrowseActionHandler,
                lambda: BrowseActionHandler(container, sequences_dir, parent_widget),
            )

        logger.info("Browse services registration completed successfully")

    except Exception as e:
        logger.error(f"Failed to register browse services: {e}", exc_info=True)
        raise


def validate_browse_service_registration(container: DIContainer) -> bool:
    """
    Validate that all browse services are properly registered.

    Args:
        container: The dependency injection container

    Returns:
        True if all services are registered and can be resolved
    """
    try:
        # Test core service resolution
        container.resolve(ISequenceDeletionService)
        container.resolve(IBrowseService)
        container.resolve(IDictionaryDataManager)
        container.resolve(IProgressiveLoadingService)
        container.resolve(IBrowseDataManager)

        logger.info("✅ Browse service registration validation successful")
        return True

    except Exception as e:
        logger.error(f"❌ Browse service registration validation failed: {e}")
        return False
