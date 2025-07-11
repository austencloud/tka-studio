from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QWidget

# Conditional PyQt6 imports for testing compatibility
try:
    from PyQt6.QtWidgets import QWidget

    QT_AVAILABLE = True
except ImportError:
    # Create mock QWidget for testing when Qt is not available
    class QWidget:
        def __init__(self, parent=None):
            self.parent = parent

    QT_AVAILABLE = False
from application.services.graph_editor.graph_editor_coordinator import (
    GraphEditorCoordinator,
)
from application.services.sequence.sequence_manager import SequenceManager
from application.services.ui.full_screen_viewer import FullScreenService
from application.services.ui.sequence_state_reader import (
    MockSequenceStateReader,
    SequenceStateReader,
)
from application.services.ui.thumbnail_generation_service import (
    MockThumbnailGenerationService,
    ThumbnailGenerationService,
)
from application.services.workbench.beat_selection_service import BeatSelectionService
from core.dependency_injection.di_container import DIContainer
from core.interfaces.core_services import ILayoutService, IUIStateManager
from core.interfaces.workbench_services import (
    IBeatDeletionService,
    IDictionaryService,
    IFullScreenService,
    IGraphEditorService,
    ISequenceWorkbenchService,
)
from presentation.components.ui.full_screen import FullScreenOverlayFactory
from presentation.components.workbench import SequenceWorkbench


def create_modern_workbench(
    container: DIContainer, parent: Optional[QWidget] = None
) -> SequenceWorkbench:
    """Factory function to create a fully configured modern sequence workbench"""

    # Configure all services if not already done
    configure_workbench_services(container)

    # Get services from container
    layout_service = container.resolve(ILayoutService)
    beat_selection_service = container.resolve(BeatSelectionService)
    workbench_service = container.resolve(ISequenceWorkbenchService)
    fullscreen_service = container.resolve(IFullScreenService)
    deletion_service = container.resolve(IBeatDeletionService)
    graph_service = container.resolve(IGraphEditorService)
    dictionary_service = container.resolve(IDictionaryService)

    # Create and return configured workbench
    return SequenceWorkbench(
        layout_service=layout_service,
        beat_selection_service=beat_selection_service,
        workbench_service=workbench_service,
        fullscreen_service=fullscreen_service,
        deletion_service=deletion_service,
        graph_service=graph_service,
        dictionary_service=dictionary_service,
        parent=parent,
    )


def configure_workbench_services(container: DIContainer) -> None:
    """Configure workbench services in the dependency injection container"""

    # Get UI state service for services that need it
    ui_state_service = container.resolve(IUIStateManager)

    # Create sequence management service
    sequence_service = SequenceManager()
    container.register_instance(ISequenceWorkbenchService, sequence_service)
    container.register_instance(IBeatDeletionService, sequence_service)
    container.register_instance(IDictionaryService, sequence_service)

    # Create full screen service with dependencies
    fullscreen_service = _create_fullscreen_service(container)
    container.register_instance(IFullScreenService, fullscreen_service)

    # Register GraphEditorService with UI state service dependency
    graph_editor_service = GraphEditorCoordinator(ui_state_service)
    container.register_instance(IGraphEditorService, graph_editor_service)

    # ILayoutService should already be registered in main.py
    # No need to register again - using the service registered in main.py


def _create_fullscreen_service(container: DIContainer) -> IFullScreenService:
    """
    Create and configure the full screen service with all dependencies.

    Args:
        container: DI container for resolving dependencies

    Returns:
        Configured FullScreenService instance
    """
    try:
        # Create thumbnail generation service
        # For now, use the mock implementation until legacy integration is complete
        thumbnail_generator = MockThumbnailGenerationService()

        # Create sequence state reader
        # For now, use the mock implementation until workbench integration is complete
        sequence_state_reader = MockSequenceStateReader()

        # Create overlay factory
        # TODO: Get main window reference for proper parent widget
        overlay_factory = FullScreenOverlayFactory(main_window_getter=None)

        # Create the full screen service
        fullscreen_service = FullScreenService(
            thumbnail_generator=thumbnail_generator,
            sequence_state_reader=sequence_state_reader,
            overlay_factory=overlay_factory,
        )

        return fullscreen_service

    except Exception as e:
        # Fallback to a basic implementation if creation fails
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"Failed to create full screen service: {e}")

        # Return a minimal working service
        thumbnail_generator = MockThumbnailGenerationService()
        sequence_state_reader = MockSequenceStateReader()
        overlay_factory = FullScreenOverlayFactory()

        return FullScreenService(
            thumbnail_generator=thumbnail_generator,
            sequence_state_reader=sequence_state_reader,
            overlay_factory=overlay_factory,
        )
