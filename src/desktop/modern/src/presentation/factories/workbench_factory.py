from __future__ import annotations

from typing import TYPE_CHECKING


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
from desktop.modern.application.services.graph_editor.graph_editor_coordinator import (
    GraphEditorCoordinator,
)
from desktop.modern.application.services.sequence.loader import SequenceLoader
from desktop.modern.application.services.sequence.sequence_beat_operations import (
    SequenceBeatOperations,
)
from desktop.modern.application.services.sequence.sequence_dictionary_service import (
    SequenceDictionaryService,
)
from desktop.modern.application.services.sequence.sequence_start_position_manager import (
    SequenceStartPositionManager,
)
from desktop.modern.application.services.ui.full_screen_viewer import FullScreenViewer
from desktop.modern.application.services.ui.sequence_state_reader import (
    MockSequenceStateReader,
)
from desktop.modern.application.services.ui.thumbnail_generation_service import (
    MockThumbnailGenerationService,
)
from desktop.modern.application.services.workbench.beat_selection_service import (
    BeatSelectionService,
)
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.core_services import ILayoutService, IUIStateManager
from desktop.modern.core.interfaces.workbench_services import (
    IFullScreenViewer,
    IGraphEditorService,
)
from desktop.modern.presentation.components.ui.full_screen import (
    FullScreenOverlayFactory,
)
from desktop.modern.presentation.components.workbench import SequenceWorkbench


def create_modern_workbench(
    container: DIContainer, parent: QWidget | None = None
) -> SequenceWorkbench:
    """Factory function to create a fully configured modern sequence workbench"""

    # Configure all services if not already done
    configure_workbench_services(container)

    # Get services from container
    layout_service = container.resolve(ILayoutService)
    beat_selection_service = container.resolve(BeatSelectionService)

    # Get microservices directly instead of interfaces
    beat_operations = container.resolve(SequenceBeatOperations)
    start_position_manager = container.resolve(SequenceStartPositionManager)
    sequence_loader = container.resolve(SequenceLoader)
    dictionary_service = container.resolve(SequenceDictionaryService)

    fullscreen_service = container.resolve(IFullScreenViewer)
    graph_service = container.resolve(IGraphEditorService)

    # Create and return configured workbench with microservices directly
    return SequenceWorkbench(
        layout_service=layout_service,
        beat_selection_service=beat_selection_service,
        beat_operations=beat_operations,
        start_position_manager=start_position_manager,
        sequence_loader=sequence_loader,
        dictionary_service=dictionary_service,
        fullscreen_service=fullscreen_service,
        graph_service=graph_service,
        parent=parent,
    )


def configure_workbench_services(container: DIContainer) -> None:
    """Configure workbench services in the dependency injection container"""

    # Get UI state service for services that need it
    ui_state_service = container.resolve(IUIStateManager)

    # Register microservices directly (CLEAN MICROSERVICES ARCHITECTURE)
    # Components should inject only the specific microservices they need
    beat_operations = SequenceBeatOperations()
    start_position_manager = SequenceStartPositionManager()
    sequence_loader = SequenceLoader()
    dictionary_service = SequenceDictionaryService()

    # Register microservices for direct injection
    container.register_instance(SequenceBeatOperations, beat_operations)
    container.register_instance(SequenceStartPositionManager, start_position_manager)
    container.register_instance(SequenceLoader, sequence_loader)
    container.register_instance(SequenceDictionaryService, dictionary_service)

    # TODO: Remove these legacy interface registrations once components are updated
    # to use microservices directly instead of going through interfaces
    # container.register_instance(ISequenceWorkbenchService, ???)
    # container.register_instance(IBeatDeletionService, ???)
    # container.register_instance(IDictionaryService, ???)

    # Create full screen service with dependencies
    fullscreen_service = _create_fullscreen_service(container)
    container.register_instance(IFullScreenViewer, fullscreen_service)

    # Register GraphEditorService with UI state service dependency
    graph_editor_service = GraphEditorCoordinator(ui_state_service)
    container.register_instance(IGraphEditorService, graph_editor_service)

    # ILayoutService should already be registered in main.py
    # No need to register again - using the service registered in main.py


def _create_fullscreen_service(container: DIContainer) -> IFullScreenViewer:
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
        fullscreen_service = FullScreenViewer(
            thumbnail_generator=thumbnail_generator,
            sequence_state_reader=sequence_state_reader,
            overlay_factory=overlay_factory,
        )

        return fullscreen_service

    except Exception as e:
        # Fallback to a basic implementation if creation fails
        import logging

        logger = logging.getLogger(__name__)
        logger.exception(f"Failed to create full screen service: {e}")

        # Return a minimal working service
        thumbnail_generator = MockThumbnailGenerationService()
        sequence_state_reader = MockSequenceStateReader()
        overlay_factory = FullScreenOverlayFactory()

        return FullScreenViewer(
            thumbnail_generator=thumbnail_generator,
            sequence_state_reader=sequence_state_reader,
            overlay_factory=overlay_factory,
        )
