"""
SignalCoordinator

Manages signal connections, emissions, and coordination between construct tab components.
Responsible for connecting signals between components and handling signal routing.
"""

from application.services.sequences.sequence_beat_operations import (
    SequenceBeatOperations,
)

# Import services from application layer (moved from presentation)
from application.services.sequences.sequence_loading_service import (
    SequenceLoadingService,
)
from application.services.sequences.sequence_start_position_manager import (
    SequenceStartPositionManager,
)
from domain.models import SequenceData
from PyQt6.QtCore import QObject, pyqtSignal

from .layout_manager import ConstructTabLayoutManager
from .option_picker_manager import OptionPickerManager
from .start_position_handler import StartPositionHandler


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
        loading_service: SequenceLoadingService,
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
        self.option_picker_manager.pictograph_selected.connect(
            self.beat_operations.add_pictograph_to_sequence
        )

        # Loading service signals
        self.loading_service.sequence_loaded.connect(self._handle_sequence_modified)
        self.loading_service.start_position_loaded.connect(
            self._handle_start_position_loaded_from_persistence
        )

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
        print(
            f"🔄 [SIGNAL_COORDINATOR] _handle_start_position_created called with: {position_key}"
        )
        print(f"✅ Signal coordinator: Start position created: {position_key}")

        # Save start position to current_sequence.json exactly like legacy
        print(
            f"🔄 [SIGNAL_COORDINATOR] Calling start_position_manager.set_start_position..."
        )
        self.start_position_manager.set_start_position(start_position_data)
        print(
            f"✅ [SIGNAL_COORDINATOR] start_position_manager.set_start_position completed"
        )

        # Populate option picker with valid combinations
        print(f"🔄 [SIGNAL_COORDINATOR] Populating option picker...")
        self.option_picker_manager.populate_from_start_position(
            position_key, start_position_data
        )
        print(f"✅ [SIGNAL_COORDINATOR] Option picker populated")

        # Transition to option picker since start position is now set
        print(
            f"🎯 [SIGNAL_COORDINATOR] Transitioning to option picker (start position created)"
        )
        self.layout_manager.transition_to_option_picker()

        # Emit external signal
        self.start_position_set.emit(position_key)
        print(
            f"✅ [SIGNAL_COORDINATOR] External signal emitted for position: {position_key}"
        )

    def _handle_start_position_loaded_from_persistence(
        self, start_position_data, position_key: str
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

        # Transition to option picker since start position is loaded
        print(
            f"🎯 [SIGNAL_COORDINATOR] Transitioning to option picker (start position loaded)"
        )
        self.layout_manager.transition_to_option_picker()

        print(
            f"✅ [SIGNAL_COORDINATOR] Option picker populated for restored start position: {position_key}"
        )

    def _handle_sequence_modified(self, sequence: SequenceData):
        """Handle sequence modification from sequence manager"""
        print(
            f"✅ Signal coordinator: Sequence modified with {sequence.length if sequence else 0} beats"
        )

        # CRITICAL FIX: Use direct workbench access for more reliable start position detection
        # Check if start position is set in workbench
        start_position_set = False
        workbench = self.layout_manager.workbench
        # Removed repetitive log statements

        if workbench and hasattr(workbench, "_start_position_data"):
            start_position_set = workbench._start_position_data is not None
            # Removed repetitive log statements
        else:
            # Removed repetitive log statements
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

        # Removed repetitive log statements

        if start_position_set or has_beats:
            print(
                f"📊 [SIGNAL_COORDINATOR] Sequence content detected - transitioning to option picker"
            )
            # Ensure we're showing the option picker when start position is set OR beats exist
            self.layout_manager.transition_to_option_picker()
            # Refresh option picker based on sequence state
            self.option_picker_manager.refresh_from_sequence(sequence)
        else:
            print(
                "🗑️ [SIGNAL_COORDINATOR] Completely empty sequence - transitioning to start position picker"
            )
            self.layout_manager.transition_to_start_position_picker()

        # Emit external signal
        self.sequence_modified.emit(sequence)

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

            # Check if start position is set in workbench (using direct access)
            start_position_set = False
            workbench = self.layout_manager.workbench
            if workbench and hasattr(workbench, "_start_position_data"):
                start_position_set = workbench._start_position_data is not None

            has_beats = sequence and sequence.beats and len(sequence.beats) > 0

            # Removed repetitive log statements

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
        try:
            print("🔄 [SIGNAL_COORDINATOR] Clearing sequence...")

            # Clear persistence FIRST
            from application.services.sequences.sequence_persistence_service import (
                SequencePersistenceService,
            )

            persistence_service = SequencePersistenceService()
            persistence_service.clear_current_sequence()
            print("✅ [SIGNAL_COORDINATOR] Cleared sequence persistence")

            # Clear sequence in workbench
            if hasattr(self.loading_service, "workbench_setter"):
                workbench_setter = self.loading_service.workbench_setter
                if workbench_setter:
                    empty_sequence = SequenceData.empty()
                    workbench_setter(empty_sequence)
                    print("✅ [SIGNAL_COORDINATOR] Cleared sequence in workbench")

            # Clear start position
            self.start_position_manager.clear_start_position()
            print("✅ [SIGNAL_COORDINATOR] Cleared start position")

            # Transition to start position picker
            self._handle_sequence_cleared()

            print("✅ [SIGNAL_COORDINATOR] Sequence cleared successfully")

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
        current_sequence = self.loading_service.get_current_sequence_from_workbench()
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

    def _handle_workbench_modified(self, sequence: SequenceData):
        """Handle workbench sequence modification with circular emission protection"""
        print(
            f"🔄 [SIGNAL_COORDINATOR] Workbench modified signal received: seq_length={sequence.length if sequence else 0}"
        )

        if self._handling_sequence_modification:
            print(
                "🔄 [SIGNAL_COORDINATOR] Already handling sequence modification - skipping"
            )
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
