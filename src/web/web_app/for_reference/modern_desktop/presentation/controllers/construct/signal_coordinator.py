"""
SignalCoordinator

Manages signal connections, emissions, and coordination between construct tab components.
Responsible for connecting signals between components and handling signal routing.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import QObject, pyqtSignal


logger = logging.getLogger(__name__)

from desktop.modern.application.services.sequence.sequence_beat_operations import (
    SequenceBeatOperations,
)
from desktop.modern.application.services.sequence.sequence_start_position_manager import (
    SequenceStartPositionManager,
)
from desktop.modern.domain.models import SequenceData
from desktop.modern.domain.models.beat_data import BeatData

# Import services from application layer (moved from presentation)
from desktop.modern.presentation.adapters.qt.sequence_loader_adapter import (
    QtSequenceLoaderAdapter,
)
from desktop.modern.presentation.managers.construct.layout_manager import (
    ConstructTabLayoutManager,
)

from ...components.option_picker.option_picker_manager import OptionPickerManager
from ...components.start_position_picker.start_position_selection_handler import (
    StartPositionSelectionHandler,
)


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
        construct_tab_controller=None,
    ):
        super().__init__()
        self.layout_manager = layout_manager
        self.start_position_handler = start_position_handler
        self.option_picker_manager = option_picker_manager
        self.loading_service = loading_service
        self.beat_operations = beat_operations
        self.start_position_manager = start_position_manager
        self.construct_tab_controller = construct_tab_controller

        # Add signal emission protection to prevent cascade refreshes
        self._handling_sequence_modification = False

        # Track current operation type to prevent unwanted tab switching
        self._current_operation_type = None

        # Queue for start position signals when workbench is not ready
        self._pending_start_position_signals = []

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
        if self.option_picker_manager:
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

        # ComponentConnector signals - Connect generation requests and results
        if self.layout_manager.component_connector:
            # Old path: generate_requested -> ConstructTab (deprecated)
            self.layout_manager.component_connector.generate_requested.connect(
                self._handle_generation_request
            )

            # New path: sequence_generated -> ConstructTab (direct from controller)
            if hasattr(self.layout_manager.component_connector, "sequence_generated"):
                self.layout_manager.component_connector.sequence_generated.connect(
                    self._handle_sequence_generated
                )

        # Construct tab controller signals - Connect generation completion
        if self.construct_tab_controller:
            self.construct_tab_controller.generation_completed.connect(
                self._handle_generation_completed
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

    def _handle_start_position_created(
        self, position_key: str, start_position_beat_data: BeatData
    ):
        """Handle start position creation with pre-loaded transition"""

        self.start_position_manager.set_start_position(start_position_beat_data)

        # Pre-load option picker content WITHOUT animations to avoid double fade
        if self.option_picker_manager:
            self.option_picker_manager.prepare_from_start_position(
                position_key, start_position_beat_data
            )
        else:
            print(
                "⚠️ [SIGNAL_COORDINATOR] Option picker manager not ready, skipping prepare_from_start_position"
            )

        # Transition to option picker with content already loaded
        self.layout_manager.transition_to_option_picker()
        self.start_position_set.emit(position_key)

    def _handle_start_position_loaded_from_persistence(
        self, position_key: str, start_position_data
    ):
        # Only populate option picker if we have valid start position data
        if start_position_data is not None:
            self.option_picker_manager.populate_from_start_position(
                position_key, start_position_data
            )
            self.layout_manager.transition_to_option_picker()
        else:
            # Don't transition to option picker if there's no data
            pass

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
            # DEBUG: Add logging for option picker refresh
            print("🔍 [SIGNAL_COORDINATOR] Refreshing option picker with sequence")
            print(
                f"🔍 [SIGNAL_COORDINATOR] Sequence: {sequence.length if sequence else 0} beats"
            )
            if sequence and sequence.beats:
                for i, beat in enumerate(sequence.beats):
                    print(
                        f"🔍 [SIGNAL_COORDINATOR] Beat {i}: beat_number={beat.beat_number}, is_blank={beat.is_blank}"
                    )
                    if hasattr(beat, "pictograph_data") and beat.pictograph_data:
                        print(
                            f"🔍 [SIGNAL_COORDINATOR] Beat {i} pictograph: letter={beat.pictograph_data.letter}"
                        )

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
            self.layout_manager.transition_to_option_picker()
        else:
            # Completely empty (no start position AND no beats) → show start position picker
            self.layout_manager.transition_to_start_position_picker()

    def _handle_sequence_generated(self, sequence_data):
        """Handle sequence generated from ComponentConnector (NEW PATH)."""
        print(
            f"🎯 [SIGNAL_COORDINATOR] Handling generated sequence: {len(sequence_data)} beats"
        )

        # Route directly to construct tab's load_generated_sequence method
        if self.construct_tab_controller and hasattr(
            self.construct_tab_controller, "load_generated_sequence"
        ):
            self.construct_tab_controller.load_generated_sequence(sequence_data)
        else:
            print(
                "❌ [SIGNAL_COORDINATOR] No construct tab controller or load_generated_sequence method"
            )

    def _handle_generation_request(self, generation_config):
        """Handle generation request from ComponentConnector (DEPRECATED PATH)."""
        print(
            f"🎯 [SIGNAL_COORDINATOR] Handling generation request: {generation_config}"
        )

        # Use the construct tab controller reference
        if self.construct_tab_controller and hasattr(
            self.construct_tab_controller, "handle_generation_request"
        ):
            self.construct_tab_controller.handle_generation_request(generation_config)
        else:
            print(
                "❌ [SIGNAL_COORDINATOR] No construct tab controller or handle_generation_request method"
            )

    def _handle_generation_completed(self, success: bool, error_message: str):
        """Handle generation completion from construct tab controller."""
        print(f"🎯 [SIGNAL_COORDINATOR] Generation completed: success={success}")

        # Notify the generate panel through the component connector
        if self.layout_manager.component_connector:
            self.layout_manager.component_connector.notify_generation_completed(
                success, error_message
            )
        else:
            print("❌ [SIGNAL_COORDINATOR] No component connector to notify")

    def clear_sequence(self):
        """Clear the current sequence (public interface)"""
        try:
            # Clear persistence FIRST
            from shared.application.services.sequence.sequence_persister import (
                SequencePersister,
            )

            persistence_service = SequencePersister()
            persistence_service.clear_current_sequence()

            # Clear start position
            self.start_position_manager.clear_start_position()

            # Transition to start position picker
            self._handle_sequence_cleared()

        except Exception as e:
            print(f"❌ [SIGNAL_COORDINATOR] Failed to clear sequence: {e}")
            import traceback

            traceback.print_exc()

    def _on_beat_modified(self, *args):
        """Handle any beat modification (added, removed, updated)."""
        # For beat_added signal, we now receive (beat_data, position, updated_sequence)
        # For other signals, fall back to fetching from workbench
        if len(args) >= 3:
            # beat_added signal with updated sequence
            updated_sequence = args[2]
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
        # Update the workbench with the new start position
        if self.layout_manager.workbench and self._is_workbench_ready():
            self.layout_manager.workbench.set_start_position(start_position_data)
        else:
            # Queue the signal for when workbench becomes ready
            print(
                "🔄 [SIGNAL_COORDINATOR] Workbench not ready, queuing start position signal"
            )
            self._pending_start_position_signals.append(("set", start_position_data))
            self._setup_workbench_ready_callback()

    def _on_start_position_updated(self, start_position_data):
        """Handle start position updated."""
        # Update the workbench with the updated start position
        if self.layout_manager.workbench and self._is_workbench_ready():
            self.layout_manager.workbench.set_start_position(start_position_data)
        else:
            # Queue the signal for when workbench becomes ready
            print(
                "🔄 [SIGNAL_COORDINATOR] Workbench not ready, queuing start position update signal"
            )
            self._pending_start_position_signals.append(("update", start_position_data))
            self._setup_workbench_ready_callback()

    def _is_workbench_ready(self):
        """Check if workbench is ready to receive signals."""
        workbench = self.layout_manager.workbench
        if not workbench:
            return False

        # Check if workbench has completed deferred initialization
        return (
            hasattr(workbench, "_state_manager")
            and workbench._state_manager is not None
        )

    def _setup_workbench_ready_callback(self):
        """Setup callback to process pending signals when workbench becomes ready."""
        if hasattr(self, "_workbench_ready_timer"):
            return  # Already set up

        from PyQt6.QtCore import QTimer

        self._workbench_ready_timer = QTimer()
        self._workbench_ready_timer.timeout.connect(self._check_workbench_ready)
        self._workbench_ready_timer.start(50)  # Check every 50ms

    def _check_workbench_ready(self):
        """Check if workbench is ready and process pending signals."""
        if self._is_workbench_ready():
            print(
                f"✅ [SIGNAL_COORDINATOR] Workbench ready, processing {len(self._pending_start_position_signals)} pending signals"
            )

            # Process all pending signals
            for (
                signal_type,
                start_position_data,
            ) in self._pending_start_position_signals:
                if signal_type in {"set", "update"}:
                    self.layout_manager.workbench.set_start_position(
                        start_position_data
                    )

            # Clear pending signals
            self._pending_start_position_signals.clear()

            # Stop the timer
            self._workbench_ready_timer.stop()
            delattr(self, "_workbench_ready_timer")

    def _handle_workbench_modified_with_operation(
        self, sequence: SequenceData, operation_type: str
    ):
        """Handle workbench sequence modification with operation type information"""

        if self._handling_sequence_modification:
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
