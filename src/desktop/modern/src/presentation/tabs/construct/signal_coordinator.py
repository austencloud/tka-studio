"""
SignalCoordinator

Manages signal connections, emissions, and coordination between construct tab components.
Responsible for connecting signals between components and handling signal routing.
"""

from PyQt6.QtCore import QObject, pyqtSignal

from domain.models.core_models import SequenceData
from .start_position_handler import StartPositionHandler
from .option_picker_manager import OptionPickerManager
from .sequence_manager import SequenceManager
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
        start_position_handler: StartPositionHandler,
        option_picker_manager: OptionPickerManager,
        sequence_manager: SequenceManager,
    ):
        super().__init__()
        self.layout_manager = layout_manager
        self.start_position_handler = start_position_handler
        self.option_picker_manager = option_picker_manager
        self.sequence_manager = sequence_manager

        # Add signal emission protection to prevent cascade refreshes
        self._handling_sequence_modification = False

        self._setup_signal_connections()

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

        # Option picker manager signals
        self.option_picker_manager.beat_data_selected.connect(
            self.sequence_manager.add_beat_to_sequence
        )

        # Sequence manager signals
        self.sequence_manager.sequence_modified.connect(self._handle_sequence_modified)
        self.sequence_manager.sequence_cleared.connect(self._handle_sequence_cleared)
        self.sequence_manager.start_position_loaded_from_persistence.connect(
            self._handle_start_position_loaded_from_persistence
        )

        # Workbench signals (SINGLE PATH) - Prevent cascade refreshes
        if self.layout_manager.workbench:
            # ONLY connect to sequence manager - let sequence manager handle the rest
            self.layout_manager.workbench.sequence_modified.connect(
                self.sequence_manager.handle_workbench_modified
            )
            # Operation completion events (non-sequence events)
            self.layout_manager.workbench.operation_completed.connect(
                self._handle_operation_completed
            )
            # Edit/Construct toggle signal
            self.layout_manager.workbench.edit_construct_toggle_requested.connect(
                self._handle_edit_construct_toggle
            )

    def _handle_start_position_created(self, position_key: str, start_position_data):
        """Handle start position creation"""
        print(f"✅ Signal coordinator: Start position created: {position_key}")

        # Save start position to current_sequence.json exactly like legacy
        self.sequence_manager.set_start_position(start_position_data)

        # Populate option picker with valid combinations
        self.option_picker_manager.populate_from_start_position(
            position_key, start_position_data
        )

        # Emit external signal
        self.start_position_set.emit(position_key)

    def _handle_start_position_loaded_from_persistence(
        self, position_key: str, start_position_data
    ):
        """Handle start position loaded from persistence during startup"""
        print(
            f"🎯 [SIGNAL_COORDINATOR] Start position loaded from persistence: {position_key}"
        )

        # CRITICAL FIX: Populate option picker with valid combinations
        # This ensures the option picker shows motion options when start position is restored
        self.option_picker_manager.populate_from_start_position(
            position_key, start_position_data
        )

        print(
            f"✅ [SIGNAL_COORDINATOR] Option picker populated for restored start position: {position_key}"
        )

    def _handle_sequence_modified(self, sequence: SequenceData):
        """Handle sequence modification from sequence manager with cascade prevention"""
        if self._handling_sequence_modification:
            print(
                "🔄 Signal coordinator: Preventing cascade refresh (already handling)"
            )
            return

        try:
            self._handling_sequence_modification = True

            print(
                f"✅ Signal coordinator: Sequence modified with {sequence.length if sequence else 0} beats"
            )

            # CRITICAL FIX: Use legacy-compatible logic for sequence modification handling
            # Check if start position is set in workbench
            start_position_set = False
            if hasattr(self.sequence_manager, "workbench_getter"):
                workbench = self.sequence_manager.workbench_getter()
                if workbench and hasattr(workbench, "_start_position_data"):
                    start_position_set = workbench._start_position_data is not None

            has_beats = (
                sequence is not None
                and sequence.length > 0
                and not (sequence.length == 1 and sequence.beats[0].is_blank)
                and sequence.metadata.get("cleared") is not True
            )

            if start_position_set or has_beats:
                print(
                    f"📊 [SIGNAL_COORDINATOR] Sequence content detected (start_pos_set={start_position_set}, has_beats={has_beats})"
                )
                # Ensure we're showing the option picker when start position is set OR beats exist
                self.layout_manager.transition_to_option_picker()
                # Refresh option picker based on sequence state
                self.option_picker_manager.refresh_from_sequence(sequence)
            else:
                print(
                    "🗑️ [SIGNAL_COORDINATOR] Completely empty sequence, transitioning to start position picker"
                )
                self.layout_manager.transition_to_start_position_picker()

            # Emit external signal
            self.sequence_modified.emit(sequence)

        finally:
            self._handling_sequence_modification = False

    def _handle_sequence_cleared(self):
        """Handle sequence clearing"""
        print("✅ Signal coordinator: Sequence cleared")
        self.layout_manager.transition_to_start_position_picker()

    def _handle_operation_completed(self, message: str):
        """Handle workbench operation completion"""
        print(f"✅ Signal coordinator: Operation completed: {message}")

    def _handle_edit_construct_toggle(self, edit_mode: bool):
        """Handle Edit/Construct toggle from workbench button panel"""
        print(
            f"✅ Signal coordinator: Edit/Construct toggle: {'Edit' if edit_mode else 'Construct'}"
        )

        if edit_mode:
            # Switch to graph editor (index 2)
            self.layout_manager.transition_to_graph_editor()
        else:
            # Switch back to appropriate picker based on sequence state
            sequence = None
            if hasattr(self.sequence_manager, "_get_current_sequence"):
                sequence = self.sequence_manager._get_current_sequence()

            # CRITICAL FIX: Use legacy-compatible logic for picker selection
            # Show start position picker ONLY when completely empty (no start position AND no beats)
            # Show option picker when start position is set OR beats exist

            # Check if start position is set in workbench
            start_position_set = False
            if hasattr(self.sequence_manager, "workbench_getter"):
                workbench = self.sequence_manager.workbench_getter()
                if workbench and hasattr(workbench, "_start_position_data"):
                    start_position_set = workbench._start_position_data is not None

            has_beats = sequence and sequence.beats and len(sequence.beats) > 0

            if start_position_set or has_beats:
                # Start position is set OR beats exist → show option picker
                print(
                    f"🎯 [SIGNAL_COORDINATOR] Showing option picker (start_pos_set={start_position_set}, has_beats={has_beats})"
                )
                self.layout_manager.transition_to_option_picker()
            else:
                # Completely empty (no start position AND no beats) → show start position picker
                print(
                    f"🎯 [SIGNAL_COORDINATOR] Showing start position picker (completely empty)"
                )
                self.layout_manager.transition_to_start_position_picker()

    def clear_sequence(self):
        """Clear the current sequence (public interface)"""
        self.sequence_manager.clear_sequence()

    def force_picker_state_update(self, sequence=None):
        """Force an update of the picker state based on current or provided sequence"""
        if sequence is None:
            # Get current sequence from sequence manager
            if hasattr(self.sequence_manager, "_get_current_sequence"):
                sequence = self.sequence_manager._get_current_sequence()

        # Handle None case
        if sequence is None:
            from domain.models.core_models import SequenceData

            sequence = SequenceData.empty()

        print(
            f"🔧 Force updating picker state for sequence with {sequence.length} beats"
        )
        self._handle_sequence_modified(sequence)

    def connect_external_workbench_signals(self, workbench):
        """Connect signals to an external workbench if needed (simplified to prevent cascades)"""
        if workbench:
            # Only connect workbench to sequence manager (single signal path)
            workbench.sequence_modified.connect(
                self.sequence_manager.handle_workbench_modified
            )
            workbench.operation_completed.connect(self._handle_operation_completed)
