"""
Simplified ConstructTab

Clean, focused ConstructTab that uses service-based architecture.
Eliminates the None initialization anti-pattern and SignalCoordinator dependency.
"""

from __future__ import annotations

from collections.abc import Callable

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from desktop.modern.application.services.construct_tab.construct_tab_component_factory import (
    ConstructTabComponentFactory,
)
from desktop.modern.application.services.construct_tab.construct_tab_coordination_service import (
    ConstructTabCoordinationService,
)
from desktop.modern.application.services.construct_tab.construct_tab_layout_service import (
    ConstructTabLayoutService,
)
from desktop.modern.application.services.sequence.sequence_beat_operations import (
    SequenceBeatOperations,
)
from desktop.modern.application.services.sequence.sequence_start_position_manager import (
    SequenceStartPositionManager,
)
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.domain.models import BeatData, SequenceData
from desktop.modern.presentation.adapters.qt.sequence_loader_adapter import (
    QtSequenceLoaderAdapter,
)


class SimplifiedConstructTab(QWidget):
    """
    Simplified ConstructTab using service-based architecture.

    Responsibilities (ONLY):
    - Service coordination
    - Signal forwarding
    - Public API for external interactions

    All business logic and UI management delegated to services.
    """

    # Public signals (forwarded from services)
    sequence_created = pyqtSignal(object)
    sequence_modified = pyqtSignal(object)
    start_position_set = pyqtSignal(str)
    start_position_loaded_from_persistence = pyqtSignal(str, object)
    generation_completed = pyqtSignal(bool, str)

    def __init__(
        self,
        container: DIContainer,
        progress_callback: Callable[[int, str], None] | None = None,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self._container = container

        # Create services with proper dependency injection
        self._component_factory = ConstructTabComponentFactory(
            container, progress_callback
        )
        self._layout_service = ConstructTabLayoutService(
            container, self._component_factory, progress_callback
        )

        # Resolve business services
        beat_operations = container.resolve(SequenceBeatOperations)
        start_position_manager = container.resolve(SequenceStartPositionManager)

        self._coordination_service = ConstructTabCoordinationService(
            beat_operations, start_position_manager, self._layout_service
        )

        # Loading service
        self._loading_service = container.resolve(QtSequenceLoaderAdapter)

        # Initialize flag
        self._initialized = False

    def initialize(self) -> None:
        """Initialize the construct tab."""
        if self._initialized:
            return

        try:
            # Setup layout through service
            self._layout_service.setup_layout(self)

            # Get components from layout service
            components = {
                "workbench": self._layout_service.get_component("workbench"),
                "start_position_picker": self._layout_service.get_component(
                    "start_position_picker"
                ),
                "option_picker": self._layout_service.get_component("option_picker"),
                "graph_editor": self._layout_service.get_component("graph_editor"),
                "generate_panel": self._layout_service.get_component("generate_panel"),
                "export_panel": self._layout_service.get_component("export_panel"),
            }

            # Setup coordination between components
            self._coordination_service.setup_component_coordination(components)

            # Connect service signals to our public signals
            self._connect_service_signals()

            # Load sequence on startup
            self._loading_service.load_sequence_on_startup()

            self._initialized = True
            print("✅ SimplifiedConstructTab: Initialized successfully")

        except Exception as e:
            print(f"❌ SimplifiedConstructTab: Initialization failed: {e}")
            raise

    def _connect_service_signals(self):
        """Connect service signals to our public signals."""
        # Forward coordination service signals
        self._coordination_service.sequence_created.connect(self.sequence_created.emit)
        self._coordination_service.sequence_modified.connect(
            self.sequence_modified.emit
        )
        self._coordination_service.start_position_set.connect(
            self.start_position_set.emit
        )
        self._coordination_service.generation_completed.connect(
            self.generation_completed.emit
        )

    # Public API methods (delegate to services)

    def add_beat_to_sequence(self, beat_data: BeatData) -> None:
        """Add beat to sequence."""
        self._coordination_service.handle_beat_added(beat_data)

    def set_start_position(self, start_position_data: BeatData) -> None:
        """Set start position."""
        self._coordination_service.handle_start_position_set(start_position_data)

    def get_current_sequence(self) -> SequenceData | None:
        """Get current sequence."""
        workbench = self._layout_service.get_component("workbench")
        if workbench and hasattr(workbench, "get_sequence"):
            return workbench.get_sequence()
        return None

    def update_beat_turns(self, beat_index: int, color: str, new_turns: int) -> None:
        """Update beat turns."""
        # Delegate to beat operations through coordination service
        workbench = self._layout_service.get_component("workbench")
        if workbench and hasattr(workbench, "execute_operation"):
            workbench.execute_operation(
                "update_beat_turns",
                beat_index=beat_index,
                color=color,
                new_turns=new_turns,
            )

    def update_beat_orientation(
        self, beat_index: int, color: str, new_orientation: int
    ) -> None:
        """Update beat orientation."""
        # Delegate to beat operations through coordination service
        workbench = self._layout_service.get_component("workbench")
        if workbench and hasattr(workbench, "execute_operation"):
            workbench.execute_operation(
                "update_beat_orientation",
                beat_index=beat_index,
                color=color,
                new_orientation=new_orientation,
            )

    def handle_generation_request(self, generation_config) -> None:
        """Handle generation request."""
        self._coordination_service.handle_generation_request(generation_config)

    def force_picker_update(self) -> None:
        """Force picker update (compatibility method)."""
        # Transition to current picker to refresh
        self._layout_service.transition_to_option_picker()

    # Transition methods (delegate to layout service)

    def transition_to_start_position_picker(self) -> None:
        """Transition to start position picker."""
        self._layout_service.transition_to_start_position_picker()

    def transition_to_option_picker(self) -> None:
        """Transition to option picker."""
        self._layout_service.transition_to_option_picker()

    def transition_to_graph_editor(self) -> None:
        """Transition to graph editor."""
        self._layout_service.transition_to_graph_editor()

    def transition_to_generate_controls(self) -> None:
        """Transition to generate controls."""
        self._layout_service.transition_to_generate_controls()

    def transition_to_export_panel(self) -> None:
        """Transition to export panel."""
        self._layout_service.transition_to_export_panel()

    # Cleanup
    def cleanup(self) -> None:
        """Clean up resources."""
        try:
            # Cleanup components
            workbench = self._layout_service.get_component("workbench")
            if workbench and hasattr(workbench, "cleanup"):
                workbench.cleanup()

            print("✅ SimplifiedConstructTab: Cleanup completed")
        except Exception as e:
            print(f"❌ SimplifiedConstructTab: Cleanup failed: {e}")
