from __future__ import annotations

from PyQt6.QtWidgets import QWidget
from shared.application.services.graph_editor.graph_editor_coordinator import (
    GraphEditorCoordinator,
)
from shared.application.services.sequence.sequence_dictionary_manager import (
    SequenceDictionaryManager,
)
from shared.application.services.ui.full_screen_viewer import FullScreenViewer
from shared.application.services.ui.sequence_state_reader import SequenceStateReader
from shared.application.services.ui.thumbnail_generation_service import (
    ThumbnailGenerationService,
)
from shared.application.services.workbench.beat_selection_service import (
    BeatSelectionService,
)
from shared.application.services.workbench.workbench_state_manager import (
    WorkbenchStateManager,
)

from desktop.modern.application.services.sequence.loader import SequenceLoader
from desktop.modern.application.services.sequence.sequence_beat_operations import (
    SequenceBeatOperations,
)
from desktop.modern.application.services.sequence.sequence_start_position_manager import (
    SequenceStartPositionManager,
)
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.core_services import ILayoutService, IUIStateManager
from desktop.modern.core.interfaces.workbench_services import (
    IFullScreenViewer,
    IGraphEditorService,
    IWorkbenchStateManager,
)
from desktop.modern.presentation.components.sequence_workbench.sequence_workbench import (
    SequenceWorkbench,
)
from desktop.modern.presentation.components.ui.full_screen import (
    FullScreenOverlayFactory,
)


def create_modern_workbench(
    container: DIContainer, parent: QWidget | None = None
) -> SequenceWorkbench:
    """Factory function to create a fully configured modern sequence workbench"""

    # Configure all services if not already done
    configure_workbench_services(container)

    # Get required services from container
    layout_service = container.resolve(ILayoutService)
    beat_selection_service = container.resolve(BeatSelectionService)

    # Create and return configured workbench with simplified constructor
    workbench = SequenceWorkbench(
        container=container,
        layout_service=layout_service,
        beat_selection_service=beat_selection_service,
        parent=parent,
    )

    # Initialize the workbench
    workbench.initialize()

    return workbench


def configure_workbench_services(container: DIContainer) -> None:
    """Configure workbench services in the dependency injection container"""

    # Get UI state service for services that need it
    ui_state_service = container.resolve(IUIStateManager)

    # Create and register workbench state manager first (needed by other services)
    # CRITICAL FIX: Inject SequenceStateTracker to ensure signal flow works
    try:
        from desktop.modern.core.service_locator import get_sequence_state_manager

        sequence_state_tracker = get_sequence_state_manager()

        workbench_state_manager = WorkbenchStateManager(
            sequence_state_tracker=sequence_state_tracker
        )
    except Exception as e:
        print(f"⚠️ [WORKBENCH_FACTORY] Failed to get SequenceStateTracker: {e}")
        workbench_state_manager = WorkbenchStateManager()

    container.register_instance(IWorkbenchStateManager, workbench_state_manager)
    container.register_instance(WorkbenchStateManager, workbench_state_manager)

    # Register microservices directly (CLEAN MICROSERVICES ARCHITECTURE)
    # Components should inject only the specific microservices they need
    beat_operations = SequenceBeatOperations()
    start_position_manager = SequenceStartPositionManager(workbench_state_manager)
    sequence_loader = SequenceLoader()
    dictionary_service = SequenceDictionaryManager()

    # Register microservices for direct injection
    container.register_instance(SequenceBeatOperations, beat_operations)
    container.register_instance(SequenceStartPositionManager, start_position_manager)
    container.register_instance(SequenceLoader, sequence_loader)
    container.register_instance(SequenceDictionaryManager, dictionary_service)

    # Legacy interface registrations removed - components now use microservices directly

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
        # Create thumbnail generation service - use real implementation
        thumbnail_generator = ThumbnailGenerationService()

        # Create sequence state reader - use real implementation
        sequence_state_reader = SequenceStateReader()

        # Create overlay factory
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
        logger.error(f"Failed to create full screen service: {e}")

        # Return a minimal working service
        thumbnail_generator = ThumbnailGenerationService()
        sequence_state_reader = SequenceStateReader()
        overlay_factory = FullScreenOverlayFactory()

        return FullScreenViewer(
            thumbnail_generator=thumbnail_generator,
            sequence_state_reader=sequence_state_reader,
            overlay_factory=overlay_factory,
        )
