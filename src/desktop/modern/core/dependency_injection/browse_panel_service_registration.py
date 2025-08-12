"""
Browse Panel Service Registration

Register browse panel services with the dependency injection container.
"""

from __future__ import annotations

import logging

from desktop.modern.application.services.browse.layout_manager_service import (
    LayoutManagerService,
)
from desktop.modern.application.services.browse.loading_state_manager_service import (
    LoadingStateManagerService,
)
from desktop.modern.application.services.browse.navigation_handler_service import (
    NavigationHandlerService,
)
from desktop.modern.application.services.browse.progressive_loading_event_handler import (
    ProgressiveLoadingEventHandler,
)
from desktop.modern.application.services.browse.sequence_display_coordinator_service import (
    SequenceDisplayCoordinatorService,
)
from desktop.modern.application.services.browse.sequence_sorter_service import (
    SequenceSorterService,
)
from desktop.modern.application.services.browse.thumbnail_factory_service import (
    ThumbnailFactoryService,
)
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.browse_services import (
    ILayoutManager,
    ILoadingStateManager,
    INavigationHandler,
    ISequenceSorter,
    IThumbnailFactory,
)


logger = logging.getLogger(__name__)


def register_browse_panel_services(
    container: DIContainer,
    grid_layout=None,
    loading_widget=None,
    browsing_widget=None,
    loading_progress_bar=None,
    loading_label=None,
    scroll_area=None,
    navigation_sidebar=None,
    control_panel=None,
) -> None:
    """
    Register browse panel services with the DI container.

    Args:
        container: The dependency injection container
        grid_layout: Grid layout widget for thumbnails
        loading_widget: Loading state widget
        browsing_widget: Main browsing widget
        loading_progress_bar: Progress bar widget
        loading_label: Loading status label
        scroll_area: Scroll area widget
        navigation_sidebar: Navigation sidebar widget
        control_panel: Control panel widget
    """
    logger.info("Registering browse panel services...")

    try:
        # Register core services as singletons
        container.register_singleton(IThumbnailFactory, ThumbnailFactoryService)
        container.register_singleton(ISequenceSorter, SequenceSorterService)

        # Register layout manager with grid layout dependency
        if grid_layout:
            # Create instance directly to avoid constructor injection issues
            layout_manager_instance = LayoutManagerService(grid_layout)
            container.register_instance(ILayoutManager, layout_manager_instance)
        else:
            container.register_singleton(ILayoutManager, LayoutManagerService)

        # Register loading state manager with UI dependencies
        if all([loading_widget, browsing_widget, loading_progress_bar, loading_label]):
            # Get the already registered layout manager
            layout_manager = container.resolve(ILayoutManager)
            # Create instance directly to avoid constructor injection issues
            loading_state_manager_instance = LoadingStateManagerService(
                loading_widget=loading_widget,
                browsing_widget=browsing_widget,
                loading_progress_bar=loading_progress_bar,
                loading_label=loading_label,
                layout_manager=layout_manager,
            )
            container.register_instance(
                ILoadingStateManager, loading_state_manager_instance
            )
        else:
            container.register_singleton(
                ILoadingStateManager, LoadingStateManagerService
            )

        # Register navigation handler with UI dependencies
        if all([scroll_area, grid_layout, navigation_sidebar]):
            # Create instance directly to avoid constructor injection issues
            navigation_handler_instance = NavigationHandlerService(
                scroll_area=scroll_area,
                grid_layout=grid_layout,
                navigation_sidebar=navigation_sidebar,
            )
            container.register_instance(INavigationHandler, navigation_handler_instance)
        else:
            container.register_singleton(INavigationHandler, NavigationHandlerService)

        # Register sequence display coordinator
        container.register_factory(
            SequenceDisplayCoordinatorService,
            lambda c: SequenceDisplayCoordinatorService(
                thumbnail_factory=c.resolve(IThumbnailFactory),
                layout_manager=c.resolve(ILayoutManager),
                loading_state_manager=c.resolve(ILoadingStateManager),
                sequence_sorter=c.resolve(ISequenceSorter),
                navigation_handler=c.resolve(INavigationHandler),
                thumbnail_width=150,
            ),
        )

        # Register progressive loading event handler
        container.register_factory(
            ProgressiveLoadingEventHandler,
            lambda c: ProgressiveLoadingEventHandler(
                loading_state_manager=c.resolve(ILoadingStateManager),
                sequence_display_coordinator=c.resolve(
                    SequenceDisplayCoordinatorService
                ),
                sequence_sorter=c.resolve(ISequenceSorter),
                control_panel=control_panel,
                navigation_sidebar=navigation_sidebar,
            ),
        )

        logger.info("Browse panel services registration completed successfully")

    except Exception as e:
        logger.error(f"Failed to register browse panel services: {e}", exc_info=True)
        raise


def validate_browse_panel_service_registration(container: DIContainer) -> bool:
    """
    Validate that all browse panel services are properly registered.

    Args:
        container: The dependency injection container

    Returns:
        True if all services are registered and can be resolved
    """
    try:
        # Test core service resolution
        container.resolve(IThumbnailFactory)
        container.resolve(ISequenceSorter)
        container.resolve(ILayoutManager)
        container.resolve(ILoadingStateManager)
        container.resolve(INavigationHandler)
        container.resolve(SequenceDisplayCoordinatorService)
        container.resolve(ProgressiveLoadingEventHandler)

        logger.info("✅ Browse panel service registration validation successful")
        return True

    except Exception as e:
        logger.exception(f"❌ Browse panel service registration validation failed: {e}")
        return False
