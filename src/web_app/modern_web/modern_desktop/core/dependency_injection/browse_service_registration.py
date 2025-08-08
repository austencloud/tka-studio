"""
Browse Service Registration

Register browse-related services with the dependency injection container.
"""

from __future__ import annotations

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
    ISequenceImageRenderer,
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

        # Register complete image export services (including ISequenceImageRenderer)
        from desktop.modern.core.dependency_injection.image_export_service_registration import (
            register_image_export_services,
        )

        register_image_export_services(container)

        # Register browse service
        from desktop.modern.application.services.browse.browse_service import (
            BrowseService,
        )

        container.register_factory(IBrowseService, lambda: BrowseService(sequences_dir))

        # Register dictionary data manager
        from application.services.browse.dictionary_data_manager import (
            DictionaryDataManager,
        )

        container.register_factory(
            IDictionaryDataManager, lambda: DictionaryDataManager(data_dir)
        )

        # Register progressive loading service
        from desktop.modern.application.services.browse.progressive_loading_service import (
            ProgressiveLoadingService,
        )

        container.register_factory(
            IProgressiveLoadingService,
            lambda c: ProgressiveLoadingService(c.resolve(IDictionaryDataManager)),
        )

        # Register data manager
        from desktop.modern.presentation.managers.browse.browse_data_manager import (
            BrowseDataManager,
        )

        container.register_factory(
            IBrowseDataManager,
            lambda c: BrowseDataManager(data_dir, c.resolve(IDictionaryDataManager)),
        )

        # Register navigation manager if stacked widget provided
        # NOTE: viewer_panel will be set later via set_viewer_panel() after creation
        if stacked_widget is not None:
            from desktop.modern.presentation.managers.browse.browse_navigation_manager import (
                BrowseNavigationManager,
            )

            # CRITICAL FIX: Register as instance, not factory
            # This ensures all components get the same instance
            nav_manager = BrowseNavigationManager(stacked_widget, viewer_panel)
            if viewer_panel is None:
                logger.warning(
                    "⚠️ Navigation manager created without viewer panel - will be set later"
                )

            container.register_instance(
                IBrowseNavigationManager,
                nav_manager,
            )

        # Register action handler if parent widget provided
        if parent_widget:
            from desktop.modern.presentation.managers.browse.browse_action_handler import (
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

        # Test image export services
        container.resolve(ISequenceImageExporter)
        container.resolve(ISequenceMetadataExtractor)
        container.resolve(ISequenceImageRenderer)

        logger.info("✅ Browse service registration validation successful")
        return True

    except Exception as e:
        logger.error(f"❌ Browse service registration validation failed: {e}")
        return False
