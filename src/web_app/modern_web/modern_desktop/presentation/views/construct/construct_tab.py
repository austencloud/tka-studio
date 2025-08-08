"""
ConstructTab - SIMPLIFIED UI WIDGET

The old ConstructTab was a 22KB god object handling 12+ responsibilities.
This version focuses ONLY on being a Qt widget with clean separation.

ELIMINATED:
- Complex service orchestration (moved to controller)
- Business logic (moved to controller)
- Signal coordination (moved to controller)
- Progress reporting mixed with UI (separated)
- Manual dependency injection (simplified)
- Complex multi-phase initialization (linearized)

PROVIDES:
- Clean Qt widget with single responsibility
- Simple initialization without choreography
- Clear separation between UI and business logic
- Testable components
"""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData

from .construct_tab_view import ConstructTabView


class ConstructTab(QWidget):
    """
    SIMPLIFIED ConstructTab - Pure Qt widget with single responsibility.

    No longer a god object! Business logic handled by existing services.
    UI creation moved to ConstructTabView.
    Coordination handled by existing SignalCoordinator.

    This class now ONLY handles:
    - Qt widget lifecycle
    - Signal forwarding between view and coordinator
    - Public API for external interactions
    """

    # Public signals for external listeners
    sequence_created = pyqtSignal(object)  # SequenceData
    sequence_modified = pyqtSignal(object)  # SequenceData
    start_position_set = pyqtSignal(str)  # position key
    start_position_loaded_from_persistence = pyqtSignal(
        str, object
    )  # position_key, start_position_data
    generation_completed = pyqtSignal(bool, str)  # success, error_message

    def __init__(
        self,
        container: DIContainer,
        parent: QWidget | None = None,
        progress_callback=None,
    ):
        """
        SIMPLIFIED initialization - no more complex choreography.
        """
        super().__init__(parent)

        # Create view (handles UI only)
        self._view = ConstructTabView(self)

        # Store container for signal coordinator creation
        self._container = container
        self._signal_coordinator = None

        # Setup the UI through the view
        self._view.setup_ui(
            container=container,
            progress_callback=progress_callback,
            option_picker_ready_callback=self._on_option_picker_ready,
        )

        # Setup will be completed when option picker is ready
        # This follows the existing pattern in the codebase

        # CRITICAL FIX: Don't hide the tab - let QTabWidget manage visibility
        # The tab should be visible when it's the active tab

    def _on_option_picker_ready(self, option_picker):
        """Handle option picker ready callback from layout manager."""
        try:
            print("🔧 ConstructTab: Creating signal coordinator with services...")

            # Import required services and components
            from shared.application.services.data.legacy_to_modern_converter import (
                LegacyToModernConverter,
            )

            from desktop.modern.application.services.sequence.sequence_start_position_manager import (
                SequenceStartPositionManager,
            )
            from desktop.modern.core.interfaces.workbench_services import (
                IWorkbenchStateManager,
            )
            from desktop.modern.presentation.adapters.qt.sequence_beat_operations_adapter import (
                QtSequenceBeatOperationsAdapter,
            )
            from desktop.modern.presentation.adapters.qt.sequence_loader_adapter import (
                QtSequenceLoaderAdapter,
            )
            from desktop.modern.presentation.components.option_picker.option_picker_manager import (
                OptionPickerManager,
            )
            from desktop.modern.presentation.components.start_position_picker.start_position_selection_handler import (
                StartPositionSelectionHandler,
            )
            from desktop.modern.presentation.controllers.construct.signal_coordinator import (
                SignalCoordinator,
            )

            # Resolve core services from DI container
            workbench_state_manager = self._container.resolve(IWorkbenchStateManager)
            legacy_converter = self._container.resolve(LegacyToModernConverter)

            # Create service adapters
            loading_service = QtSequenceLoaderAdapter(
                workbench_state_manager=workbench_state_manager,
                legacy_to_modern_converter=legacy_converter,
            )

            beat_operations = QtSequenceBeatOperationsAdapter(
                workbench_state_manager=workbench_state_manager,
            )

            start_position_manager = SequenceStartPositionManager(
                workbench_state_manager=workbench_state_manager,
            )

            # Create component managers
            option_picker_manager = OptionPickerManager(option_picker)
            start_position_handler = StartPositionSelectionHandler()

            # Create signal coordinator with all dependencies
            self._signal_coordinator = SignalCoordinator(
                layout_manager=self._view._layout_manager,
                start_position_handler=start_position_handler,
                option_picker_manager=option_picker_manager,
                loading_service=loading_service,
                beat_operations=beat_operations,
                start_position_manager=start_position_manager,
                construct_tab_controller=self,  # Pass self as controller
            )

            # Connect signal coordinator signals to our public signals
            self._signal_coordinator.sequence_created.connect(
                self.sequence_created.emit
            )
            self._signal_coordinator.sequence_modified.connect(
                self.sequence_modified.emit
            )
            self._signal_coordinator.start_position_set.connect(
                self.start_position_set.emit
            )
            if hasattr(
                self._signal_coordinator, "start_position_loaded_from_persistence"
            ):
                self._signal_coordinator.start_position_loaded_from_persistence.connect(
                    self.start_position_loaded_from_persistence.emit
                )

            # Connect construct tab signals
            self._signal_coordinator.connect_construct_tab_signals(self)

            # Load sequence on startup
            loading_service.load_sequence_on_startup()

            print("✅ ConstructTab: Signal coordinator created and services connected")

        except Exception as e:
            print(f"❌ ConstructTab: Failed to create signal coordinator: {e}")
            import traceback

            traceback.print_exc()

    # ============================================================================
    # PUBLIC API - Delegate to existing services via layout manager
    # ============================================================================

    def clear_sequence(self) -> None:
        """Clear the current sequence."""
        # Delegate to layout manager's workbench
        if (
            hasattr(self._view._layout_manager, "workbench")
            and self._view._layout_manager.workbench
        ):
            self._view._layout_manager.workbench.clear_sequence()

    def force_picker_update(self) -> None:
        """Force an update of the picker state."""
        # Delegate to view
        if hasattr(self._view, "force_picker_update"):
            self._view.force_picker_update()

    def add_beat_to_sequence(self, beat_data: BeatData) -> None:
        """Add beat to sequence."""
        if self._signal_coordinator and hasattr(
            self._signal_coordinator, "beat_operations"
        ):
            self._signal_coordinator.beat_operations.add_pictograph_to_sequence(
                beat_data
            )

    def set_start_position(self, start_position_data: BeatData) -> None:
        """Set start position."""
        if self._signal_coordinator and hasattr(
            self._signal_coordinator, "start_position_manager"
        ):
            self._signal_coordinator.start_position_manager.set_start_position(
                start_position_data
            )

    def get_current_sequence(self) -> SequenceData | None:
        """Get current sequence."""
        # Delegate to workbench state manager via container
        try:
            from desktop.modern.core.interfaces.workbench_services import (
                IWorkbenchStateManager,
            )

            workbench_state_manager = self._container.resolve(IWorkbenchStateManager)
            return workbench_state_manager.get_current_sequence()
        except Exception:
            return None

    def update_beat_turns(self, beat_index: int, color: str, new_turns: int) -> None:
        """Update beat turns."""
        if self._signal_coordinator and hasattr(
            self._signal_coordinator, "beat_operations"
        ):
            self._signal_coordinator.beat_operations.update_beat_turns(
                beat_index, color, new_turns
            )

    def update_beat_orientation(
        self, beat_index: int, color: str, new_orientation: int
    ) -> None:
        """Update beat orientation."""
        if self._signal_coordinator and hasattr(
            self._signal_coordinator, "beat_operations"
        ):
            self._signal_coordinator.beat_operations.update_beat_orientation(
                beat_index, color, new_orientation
            )

    def handle_generation_request(self, generation_config):
        """Handle generation request from signal coordinator."""
        # This method should not be called anymore since we're using the real GeneratePanel
        # The GeneratePanel's controller will handle the generation and emit sequence_generated
        print(
            f"⚠️ ConstructTab: Deprecated generation request handler called: {generation_config}"
        )
        print(
            "⚠️ ConstructTab: Generation should be handled by GeneratePanel controller"
        )

        # Don't emit fake success - let the real generation system work
        # self.generation_completed.emit(True, "")

    def load_generated_sequence(self, sequence_data):
        """Load a generated sequence into the construct tab workbench."""
        try:
            print(
                f"🎯 ConstructTab: Loading generated sequence with {len(sequence_data)} beats"
            )

            # Clear existing sequence first
            if self._signal_coordinator:
                self._signal_coordinator.clear_sequence()
                print("🧹 ConstructTab: Cleared existing sequence")

            # Add each beat from the generated sequence
            for i, pictograph_data in enumerate(sequence_data):
                try:
                    # Convert PictographData to BeatData for the workbench
                    from desktop.modern.domain.models.beat_data import BeatData

                    beat_data = BeatData(
                        beat=i + 1, pictograph_data=pictograph_data, has_pictograph=True
                    )

                    # Add beat to sequence via signal coordinator
                    if self._signal_coordinator and hasattr(
                        self._signal_coordinator, "beat_operations"
                    ):
                        self._signal_coordinator.beat_operations.add_pictograph_to_sequence(
                            beat_data
                        )
                        print(
                            f"✅ ConstructTab: Added beat {i + 1}: {pictograph_data.letter}"
                        )
                    else:
                        print(
                            f"❌ ConstructTab: No beat operations available for beat {i + 1}"
                        )

                except Exception as beat_error:
                    print(f"❌ ConstructTab: Failed to add beat {i + 1}: {beat_error}")

            print(
                f"✅ ConstructTab: Generated sequence loaded successfully ({len(sequence_data)} beats)"
            )

        except Exception as e:
            print(f"❌ ConstructTab: Failed to load generated sequence: {e}")
            import traceback

            traceback.print_exc()

    # ============================================================================
    # QT WIDGET EVENTS - Delegate to existing services
    # ============================================================================

    def resizeEvent(self, event) -> None:
        """Handle resize events."""
        super().resizeEvent(event)
        # Delegate to existing resize coordinator via container
        try:
            from desktop.modern.application.services.ui.window_resize_coordinator import (
                WindowResizeCoordinator,
            )

            resize_coordinator = self._container.resolve(WindowResizeCoordinator)
            if self.window():
                new_width = self.window().width()
                resize_coordinator.notify_window_resize(new_width)
        except Exception:
            pass  # Resize coordination is optional

    @property
    def workbench(self):
        """Access to workbench - for backward compatibility."""
        if hasattr(self._view._layout_manager, "workbench"):
            return self._view._layout_manager.workbench
        return None
