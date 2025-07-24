"""
SignalCoordinator

Manages signal connections, emissions, and coordination between construct tab components.
Responsible for connecting signals between components and handling signal routing.
"""

from application.services.sequence.sequence_beat_operations import (
    SequenceBeatOperations,
)
from application.services.sequence.sequence_start_position_manager import (
    SequenceStartPositionManager,
)
from domain.models import SequenceData
from domain.models.beat_data import BeatData

# Import services from application layer (moved from presentation)
from presentation.adapters.qt.sequence_loader_adapter import QtSequenceLoaderAdapter
from PyQt6.QtCore import QObject, pyqtSignal

from ...components.option_picker.option_picker_manager import OptionPickerManager
from ...components.start_position_picker.start_position_selection_handler import (
    StartPositionSelectionHandler,
)
from .layout_manager import ConstructTabLayoutManager


class SignalCoordinator(QObject):
    """
    Coordinates signals between construct tab components.

    Responsibilities:
    - Connecting signals between components
    - Managing signal routing and forwarding
    - Handling component state changes
    - Coordinating transitions between UI states

    Signals:
    - sequence_created: Emitted when a new sequence is created
    - sequence_modified: Emitted when sequence is modified
    - start_position_set: Emitted when start position is set
    """

    sequence_created = pyqtSignal(object)  # SequenceData object
    sequence_modified = pyqtSignal(object)  # SequenceData object
    start_position_set = pyqtSignal(str)  # position key

    def __init__(
        self,
        layout_manager: ConstructTabLayoutManager,
        start_position_handler: StartPositionSelectionHandler,
        option_picker_manager: OptionPickerManager,
        loading_service: QtSequenceLoaderAdapter,
        beat_operations: SequenceBeatOperations,
        start_position_manager: SequenceStartPositionManager,
    ):
        super().__init__()
        self.layout_manager = layout_manager
        self.start_position_handler = start_position_handler
        self.option_picker_manager = option_picker_manager
        self.loading_service = loading_service
        self.beat_operations = beat_operations
        self.start_position_manager = start_position_manager

        # Add signal emission protection to prevent cascade refreshes
        self._handling_sequence_modification = False

        # Track current operation type to prevent unwanted tab switching
        self._current_operation_type = None

        self._setup_signal_connections()

    def connect_construct_tab_signals(self, construct_tab_widget):
        """Connect to construct tab signals after initialization."""
        # Connect to construct tab signals (which bridge loading service callbacks)
        # NOTE: Removed construct_tab_widget.sequence_modified connection to prevent circular signals
        # The construct tab forwards our signals, so connecting back creates a loop
        construct_tab_widget.start_position_loaded_from_persistence.connect(
            self._handle_start_position_loaded_from_persistence
        )

    def _setup_signal_connections(self):
        """Setup all signal connections between components"""

        # Start position picker to start position handler
        if self.layout_manager.start_position_picker:
            self.layout_manager.start_position_picker.start_position_selected.connect(
                self.start_position_handler.handle_start_position_selected
            )

        # Start position handler signals
        self.start_position_handler.start_position_created.connect(
            self._handle_start_position_created
        )
        self.start_position_handler.transition_requested.connect(
            self.layout_manager.transition_to_option_picker
        )

        # Option picker manager signals - Prevent duplicate connections
        try:
            self.option_picker_manager.pictograph_selected.disconnect(
                self.beat_operations.add_pictograph_to_sequence
            )
        except TypeError:
            # Signal was not connected, which is fine
            pass

        self.option_picker_manager.pictograph_selected.connect(
            self.beat_operations.add_pictograph_to_sequence
        )

        # Connect to construct tab signals (which bridge loading service callbacks)
        # Note: construct_tab_widget will be set after initialization
        # These connections will be made in set_construct_tab_widget method

        # Beat operations signals
        self.beat_operations.beat_added.connect(self._on_beat_modified)
        self.beat_operations.beat_removed.connect(self._on_beat_modified)
        self.beat_operations.beat_updated.connect(self._on_beat_modified)

        # Start position manager signals
        self.start_position_manager.start_position_set.connect(
            self._on_start_position_set
        )
        self.start_position_manager.start_position_updated.connect(
            self._on_start_position_updated
        )

        # Workbench signals (SINGLE PATH) - Prevent cascade refreshes
        if self.layout_manager.workbench:
            # Connect to beat operations for sequence modifications
            self.layout_manager.workbench.sequence_modified.connect(
                self._handle_workbench_modified
            )

            # Connect to new signal that includes operation type
            if hasattr(
                self.layout_manager.workbench, "sequence_modified_with_operation"
            ):
                self.layout_manager.workbench.sequence_modified_with_operation.connect(
                    self._handle_workbench_modified_with_operation
                )

            # Operation completion events (non-sequence events)
            self.layout_manager.workbench.operation_completed.connect(
                self._handle_operation_completed
            )

            # Connect new 3-panel system signals from workbench (legacy)
            if hasattr(self.layout_manager.workbench, "picker_mode_requested"):
                self.layout_manager.workbench.picker_mode_requested.connect(
                    self._handle_picker_mode_request
                )
            if hasattr(self.layout_manager.workbench, "graph_editor_requested"):
                self.layout_manager.workbench.graph_editor_requested.connect(
                    self.layout_manager.transition_to_graph_editor
                )
            if hasattr(self.layout_manager.workbench, "generate_requested"):
                self.layout_manager.workbench.generate_requested.connect(
                    self.layout_manager.transition_to_generate_controls
                )

            # Connect tab widget signals (new tab-based navigation)
            if (
                hasattr(self.layout_manager, "tab_widget")
                and self.layout_manager.tab_widget
            ):
                self.layout_manager.tab_widget.picker_tab_clicked.connect(
                    self._handle_picker_mode_request
                )
                self.layout_manager.tab_widget.graph_editor_tab_clicked.connect(
                    self.layout_manager.transition_to_graph_editor
                )
                self.layout_manager.tab_widget.generate_controls_tab_clicked.connect(
                    self.layout_manager.transition_to_generate_controls
                )

            # Clear sequence signal - connect to signal coordinator
            if hasattr(self.layout_manager.workbench, "clear_sequence_requested"):
                self.layout_manager.workbench.clear_sequence_requested.connect(
                    self.clear_sequence
                )
                print(
                    "✅ [SIGNAL_COORDINATOR] Connected workbench clear_sequence_requested signal"
                )

    def _handle_start_position_created(
        self, position_key: str, start_position_beat_data: BeatData
    ):
        """Handle start position creation with pre-loaded transition"""
        print(
            f"🎯 [SIGNAL_COORDINATOR] _handle_start_position_created called with position: {position_key}"
        )

        # PAGINATION DEBUG: Track consecutive selections of the same position
        if not hasattr(self, "_last_selected_position"):
            self._last_selected_position = None
            self._consecutive_selections = 0

        if self._last_selected_position == position_key:
            self._consecutive_selections += 1
            print(
                f"🔍 [PAGINATION_DEBUG] SignalCoordinator: Consecutive selection #{self._consecutive_selections} of position '{position_key}'"
            )
        else:
            self._consecutive_selections = 1
            print(
                f"🔍 [PAGINATION_DEBUG] SignalCoordinator: First selection of position '{position_key}'"
            )

        self._last_selected_position = position_key

        self.start_position_manager.set_start_position(start_position_beat_data)

        # Pre-load option picker content WITHOUT animations to avoid double fade
        print(
            f"🎯 [SIGNAL_COORDINATOR] Calling option_picker_manager.prepare_from_start_position..."
        )
        self.option_picker_manager.prepare_from_start_position(
            position_key, start_position_beat_data
        )

        # Transition to option picker with content already loaded
        print(f"🎯 [SIGNAL_COORDINATOR] Transitioning to option picker...")
        self.layout_manager.transition_to_option_picker()
        self.start_position_set.emit(position_key)

    def _handle_start_position_loaded_from_persistence(
        self, position_key: str, start_position_data
    ):
        """Handle start position loaded from persistence during startup"""
        print(
            f"🔍 [SIGNAL_COORDINATOR] Handling start position loaded: position_key={position_key}, start_position_data={start_position_data}"
        )

        self.option_picker_manager.populate_from_start_position(
            position_key, start_position_data
        )
        self.layout_manager.transition_to_option_picker()

    def _handle_sequence_modified(self, sequence: SequenceData):
        """Handle sequence modification from sequence manager"""

        start_position_set = False
        workbench = self.layout_manager.workbench

        if workbench and hasattr(workbench, "_beat_frame_section"):
            beat_frame_section = workbench._beat_frame_section
            if beat_frame_section and hasattr(
                beat_frame_section, "_start_position_data"
            ):
                start_position_set = beat_frame_section._start_position_data is not None
        else:
            pass

        has_beats = (
            sequence is not None
            and sequence.length > 0
            and not (
                sequence.length == 1 and sequence.beats[0].is_blank
                if sequence.beats
                else False
            )
            and sequence.metadata.get("cleared") is not True
        )

        if start_position_set or has_beats:

            # Pre-load option picker content before transition
            self.option_picker_manager.refresh_from_sequence(sequence)
            # Ensure we're showing the option picker when start position is set OR beats exist
            self.layout_manager.transition_to_option_picker()
        else:

            self.layout_manager.transition_to_start_position_picker()

        # Emit external signal
        self.sequence_modified.emit(sequence)

    def _handle_sequence_cleared(self):
        """Handle sequence clearing"""
        self.layout_manager.transition_to_start_position_picker()

    def _handle_operation_completed(self, message: str):
        """Handle workbench operation completion"""

    def _handle_picker_mode_request(self):
        """Handle picker mode request from workbench button panel with smart switching."""
        # Get current sequence state
        sequence = None
        if hasattr(self.beat_operations, "get_current_sequence"):
            sequence = self.beat_operations.get_current_sequence()

        # Check if start position is set in workbench
        start_position_set = False
        workbench = self.layout_manager.workbench
        if workbench and hasattr(workbench, "_beat_frame_section"):
            beat_frame_section = workbench._beat_frame_section
            if beat_frame_section and hasattr(
                beat_frame_section, "_start_position_data"
            ):
                start_position_set = beat_frame_section._start_position_data is not None

        has_beats = sequence and sequence.beats and len(sequence.beats) > 0

        if start_position_set or has_beats:
            # Start position is set OR beats exist → show option picker
            print(
                f"🎯 [SIGNAL_COORDINATOR] Smart switching to option picker (start_pos_set={start_position_set}, has_beats={has_beats})"
            )
            self.layout_manager.transition_to_option_picker()
        else:
            # Completely empty (no start position AND no beats) → show start position picker
            print(
                f"🎯 [SIGNAL_COORDINATOR] Smart switching to start position picker (completely empty)"
            )
            self.layout_manager.transition_to_start_position_picker()

    def clear_sequence(self):
        """Clear the current sequence (public interface)"""
        try:

            # Clear persistence FIRST
            from application.services.sequence.sequence_persister import (
                SequencePersister,
            )

            persistence_service = SequencePersister()
            persistence_service.clear_current_sequence()

            # Clear sequence in workbench
            print(
                f"🔍 [SIGNAL_COORDINATOR] Loading service: {self.loading_service is not None}"
            )
            if hasattr(self.loading_service, "workbench_setter"):
                workbench_setter = self.loading_service.workbench_setter
                print(
                    f"🔍 [SIGNAL_COORDINATOR] Workbench setter: {workbench_setter is not None}"
                )
                if workbench_setter:
                    empty_sequence = SequenceData.empty()
                    print(
                        f"🔍 [SIGNAL_COORDINATOR] Calling workbench setter with empty sequence"
                    )
                    workbench_setter(empty_sequence)
                    print(
                        f"✅ [SIGNAL_COORDINATOR] Workbench setter called successfully"
                    )
                else:
                    print(f"❌ [SIGNAL_COORDINATOR] Workbench setter is None")
            else:
                print(
                    f"❌ [SIGNAL_COORDINATOR] Loading service has no workbench_setter attribute"
                )

            # Clear start position
            self.start_position_manager.clear_start_position()

            # Transition to start position picker
            self._handle_sequence_cleared()

        except Exception as e:
            print(f"❌ [SIGNAL_COORDINATOR] Failed to clear sequence: {e}")
            import traceback

            traceback.print_exc()

    def force_picker_state_update(self, sequence=None):
        """Force an update of the picker state based on current or provided sequence"""
        if sequence is None:
            # Get current sequence from loading service
            if hasattr(self.loading_service, "get_current_sequence_from_workbench"):
                sequence = self.loading_service.get_current_sequence_from_workbench()

        # Handle None case
        if sequence is None:
            sequence = SequenceData.empty()

        print(
            f"🔧 Force updating picker state for sequence with {sequence.length} beats"
        )
        self._handle_sequence_modified(sequence)

    def _on_beat_modified(self, *args):
        """Handle any beat modification (added, removed, updated)."""
        # For beat_added signal, we now receive (beat_data, position, updated_sequence)
        # For other signals, fall back to fetching from workbench
        if len(args) >= 3:
            # beat_added signal with updated sequence
            beat_data, position, updated_sequence = args[0], args[1], args[2]
            self._handle_sequence_modified(updated_sequence)
        else:
            # Other beat modification signals - fetch from workbench
            current_sequence = (
                self.loading_service.get_current_sequence_from_workbench()
            )
            if current_sequence:
                self._handle_sequence_modified(current_sequence)

    def _on_start_position_set(self, start_position_data):
        """Handle start position set."""
        print(
            f"🎯 [SIGNAL_COORDINATOR] Start position set: {start_position_data.letter}"
        )

    def _on_start_position_updated(self, start_position_data):
        """Handle start position updated."""
        print(
            f"🎯 [SIGNAL_COORDINATOR] Start position updated: {start_position_data.letter}"
        )

    def _handle_workbench_modified_with_operation(
        self, sequence: SequenceData, operation_type: str
    ):
        """Handle workbench sequence modification with operation type information"""
        print(
            f"🔄 [SIGNAL_COORDINATOR] _handle_workbench_modified_with_operation called with sequence length: {len(sequence.beats)}, operation: {operation_type}"
        )

        if self._handling_sequence_modification:
            print(
                "🔄 [SIGNAL_COORDINATOR] Already handling sequence modification - skipping"
            )
            return

        try:
            self._handling_sequence_modification = True
            self._current_operation_type = operation_type

            # Save sequence to persistence
            self._save_sequence_to_persistence(sequence)

            # Only trigger tab switching for non-delete-beat operations
            if operation_type != "delete_beat":
                self._handle_sequence_modified(sequence)
            else:
                print(
                    f"🎯 [SIGNAL_COORDINATOR] Skipping tab switch for delete_beat operation"
                )
                # Still emit the external signal for other listeners
                self.sequence_modified.emit(sequence)

        except Exception as e:
            print(f"❌ Signal coordinator: Workbench modification failed: {e}")
            import traceback

            traceback.print_exc()
        finally:
            self._handling_sequence_modification = False
            self._current_operation_type = None

    def _handle_workbench_modified(self, sequence: SequenceData):
        """Handle workbench sequence modification with circular emission protection"""

        if self._handling_sequence_modification:
            return

        try:
            self._handling_sequence_modification = True
            # Save sequence to persistence
            self._save_sequence_to_persistence(sequence)
            self._handle_sequence_modified(sequence)
        except Exception as e:
            print(f"❌ Signal coordinator: Workbench modification failed: {e}")
            import traceback

            traceback.print_exc()
        finally:
            self._handling_sequence_modification = False

    def _save_sequence_to_persistence(self, sequence: SequenceData):
        """Convert modern SequenceData to legacy format and save to current_sequence.json"""
        try:
            # Delegate to beat operations service which has the persistence logic
            if hasattr(self.beat_operations, "_save_sequence_to_persistence"):
                self.beat_operations._save_sequence_to_persistence(sequence)
        except Exception as e:
            print(f"❌ Failed to save sequence to persistence: {e}")
            import traceback

            traceback.print_exc()

    def connect_external_workbench_signals(self, workbench):
        """Connect signals to an external workbench if needed (simplified to prevent cascades)"""
        if workbench:
            # Connect workbench to our handler (single signal path)
            workbench.sequence_modified.connect(self._handle_workbench_modified)
            workbench.operation_completed.connect(self._handle_operation_completed)

            # Connect new 3-panel system signals
            if hasattr(workbench, "picker_mode_requested"):
                workbench.picker_mode_requested.connect(
                    self._handle_picker_mode_request
                )
            if hasattr(workbench, "graph_editor_requested"):
                workbench.graph_editor_requested.connect(
                    self.layout_manager.transition_to_graph_editor
                )
            if hasattr(workbench, "generate_requested"):
                workbench.generate_requested.connect(
                    self.layout_manager.transition_to_generate_controls
                )
