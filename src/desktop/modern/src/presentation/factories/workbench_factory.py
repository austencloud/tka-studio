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
from application.services.ui.full_screen_viewer import FullScreenViewer
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
    container.register_singleton(
        IFullScreenService, FullScreenViewer
    )  # Register GraphEditorService with UI state service dependency
    graph_editor_service = GraphEditorCoordinator(ui_state_service)
    container.register_instance(IGraphEditorService, graph_editor_service)

    # ILayoutService should already be registered in main.py
    # No need to register again - using the service registered in main.py
