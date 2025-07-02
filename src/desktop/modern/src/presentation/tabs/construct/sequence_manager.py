"""
SequenceManager (Refactored)

Coordinates sequence operations through specialized service classes.
Acts as a facade for sequence loading, beat operations, start position management, and data conversion.
"""

from typing import Optional, Callable
from PyQt6.QtCore import QObject, pyqtSignal

from domain.models.core_models import SequenceData, BeatData
from .sequence_loading_service import SequenceLoadingService
from .sequence_beat_operations import SequenceBeatOperations
from .sequence_start_position_manager import SequenceStartPositionManager
from .sequence_data_converter import SequenceDataConverter


class SequenceManager(QObject):
    """
    Refactored sequence manager that coordinates specialized service classes.

    Responsibilities:
    - Coordinating sequence loading, beat operations, and start position management
    - Providing a unified interface for sequence operations
    - Managing signal emissions and workbench interactions
    - Delegating specialized tasks to appropriate service classes

    Signals:
    - sequence_modified: Emitted when sequence is modified
    - sequence_cleared: Emitted when sequence is cleared
    """

    sequence_modified = pyqtSignal(object)  # SequenceData object
    sequence_cleared = pyqtSignal()
    start_position_loaded_from_persistence = pyqtSignal(
        str, object
    )  # position_key, BeatData

    def __init__(
        self,
        workbench_getter: Optional[Callable[[], object]] = None,
        workbench_setter: Optional[Callable[[SequenceData], None]] = None,
        start_position_handler: Optional[object] = None,
    ):
        super().__init__()
        self.workbench_getter = workbench_getter
        self.workbench_setter = workbench_setter
        self.start_position_handler = start_position_handler
        self._emitting_signal = False

        # Initialize specialized service classes
        self.data_converter = SequenceDataConverter()

        self.loading_service = SequenceLoadingService(
            workbench_getter=workbench_getter,
            workbench_setter=workbench_setter,
            data_converter=self.data_converter,
        )

        self.beat_operations = SequenceBeatOperations(
            workbench_getter=workbench_getter,
            workbench_setter=workbench_setter,
            data_converter=self.data_converter,
        )

        self.start_position_manager = SequenceStartPositionManager(
            workbench_getter=workbench_getter,
            workbench_setter=workbench_setter,
            data_converter=self.data_converter,
        )

        # Connect service signals to our signals
        self._connect_service_signals()

    def _connect_service_signals(self):
        """Connect service signals to our main signals"""
        # Connect loading service signals
        self.loading_service.sequence_loaded.connect(self.sequence_modified.emit)
        self.loading_service.start_position_loaded.connect(
            self._on_start_position_loaded
        )

        # Connect beat operations signals
        self.beat_operations.beat_added.connect(self._on_beat_added)
        self.beat_operations.beat_removed.connect(self._on_beat_removed)
        self.beat_operations.beat_updated.connect(self._on_beat_updated)

        # Connect start position manager signals
        self.start_position_manager.start_position_set.connect(
            self._on_start_position_set
        )
        self.start_position_manager.start_position_updated.connect(
            self._on_start_position_updated
        )

    def _on_start_position_loaded(
        self, start_position_data: BeatData, position_key: str
    ):
        """Handle start position loaded signal"""
        print(
            f"🎯 [SEQUENCE_MANAGER] Start position loaded: {start_position_data.letter} ({position_key})"
        )
        # CRITICAL FIX: Emit signal for option picker population
        self.start_position_loaded_from_persistence.emit(
            position_key, start_position_data
        )

    def _on_beat_added(self, beat_data: BeatData, position: int):
        """Handle beat added signal"""
        current_sequence = self.get_current_sequence_from_workbench()
        if current_sequence:
            self.sequence_modified.emit(current_sequence)

    def _on_beat_removed(self, position: int):
        """Handle beat removed signal"""
        current_sequence = self.get_current_sequence_from_workbench()
        if current_sequence:
            self.sequence_modified.emit(current_sequence)

    def _on_beat_updated(self, beat_data: BeatData, position: int):
        """Handle beat updated signal"""
        current_sequence = self.get_current_sequence_from_workbench()
        if current_sequence:
            self.sequence_modified.emit(current_sequence)

    def _on_start_position_set(self, start_position_data: BeatData):
        """Handle start position set signal"""
        print(f"🎯 [SEQUENCE_MANAGER] Start position set: {start_position_data.letter}")

    def _on_start_position_updated(self, start_position_data: BeatData):
        """Handle start position updated signal"""
        print(
            f"🎯 [SEQUENCE_MANAGER] Start position updated: {start_position_data.letter}"
        )

    def handle_workbench_modified(self, sequence: SequenceData):
        """Handle workbench sequence modification with circular emission protection"""
        if self._emitting_signal:
            return

        try:
            self._emitting_signal = True
            # Update current_sequence.json file when sequence is modified - exactly like legacy
            self._save_sequence_to_persistence(sequence)
            self.sequence_modified.emit(sequence)
        except Exception as e:
            print(f"❌ Sequence manager: Signal emission failed: {e}")
            import traceback

            traceback.print_exc()
        finally:
            self._emitting_signal = False

    def _save_sequence_to_persistence(self, sequence: SequenceData):
        """Convert modern SequenceData to legacy format and save to current_sequence.json"""
        try:
            # Delegate to beat operations service which has the persistence logic
            self.beat_operations._save_sequence_to_persistence(sequence)
        except Exception as e:
            print(f"❌ Failed to save sequence to persistence: {e}")
            import traceback

            traceback.print_exc()

    # Delegate methods to appropriate services
    def add_beat_to_sequence(self, beat_data: BeatData):
        """Add a beat to the current sequence"""
        self.beat_operations.add_beat_to_sequence(beat_data)

    def remove_beat(self, beat_index: int):
        """Remove a beat from the sequence"""
        self.beat_operations.remove_beat(beat_index)

    def update_beat_turns(self, beat_index: int, color: str, new_turns: int):
        """Update the number of turns for a specific beat"""
        self.beat_operations.update_beat_turns(beat_index, color, new_turns)

    def update_beat_orientation(
        self, beat_index: int, color: str, new_orientation: int
    ):
        """Update the orientation for a specific beat"""
        self.beat_operations.update_beat_orientation(beat_index, color, new_orientation)

    def set_start_position(self, start_position_data: BeatData):
        """Set the start position"""
        self.start_position_manager.set_start_position(start_position_data)

    def update_start_position_orientation(self, color: str, new_orientation: int):
        """Update start position orientation for a specific color"""
        self.start_position_manager.update_start_position_orientation(
            color, new_orientation
        )

    def get_current_start_position(self) -> Optional[BeatData]:
        """Get the current start position"""
        return self.start_position_manager.get_current_start_position()

    def clear_start_position(self):
        """Clear the current start position"""
        self.start_position_manager.clear_start_position()

    def has_start_position(self) -> bool:
        """Check if a start position is currently set"""
        return self.start_position_manager.has_start_position()

    def load_sequence_on_startup(self):
        """Load sequence from current_sequence.json on startup"""
        self.loading_service.load_sequence_on_startup()

    def get_current_sequence_from_workbench(self) -> Optional[SequenceData]:
        """Get the current sequence from workbench"""
        return self.loading_service.get_current_sequence_from_workbench()

    def clear_sequence(self):
        """Clear the current sequence - exactly like legacy"""
        try:
            # Clear sequence in workbench
            if self.workbench_setter:
                empty_sequence = SequenceData.empty()
                self.workbench_setter(empty_sequence)
                print("✅ Cleared sequence in workbench")

            # Clear start position
            self.clear_start_position()

            # Clear persistence
            from application.services.core.sequence_persistence_service import (
                SequencePersistenceService,
            )

            persistence_service = SequencePersistenceService()
            persistence_service.clear_current_sequence()
            print("✅ Cleared sequence persistence")

            # Emit signal
            self.sequence_cleared.emit()
            print("✅ Sequence cleared successfully")

        except Exception as e:
            print(f"❌ Failed to clear sequence: {e}")
            import traceback

            traceback.print_exc()

    def _emit_sequence_modified(self, sequence: SequenceData):
        """Emit sequence modified signal with protection against recursive calls"""
        if not self._emitting_signal:
            self._emitting_signal = True
            try:
                self.sequence_modified.emit(sequence)
            finally:
                self._emitting_signal = False

    # Legacy compatibility methods (delegate to data converter)
    def _convert_legacy_to_beat_data(
        self, beat_dict: dict, beat_number: int
    ) -> BeatData:
        """Convert legacy JSON format to modern BeatData"""
        return self.data_converter.convert_legacy_to_beat_data(beat_dict, beat_number)

    def _convert_legacy_start_position_to_beat_data(
        self, start_pos_dict: dict
    ) -> BeatData:
        """Convert legacy start position to modern BeatData"""
        return self.data_converter.convert_legacy_start_position_to_beat_data(
            start_pos_dict
        )

    def _convert_beat_data_to_legacy_format(
        self, beat: BeatData, beat_number: int
    ) -> dict:
        """Convert modern BeatData to legacy JSON format"""
        return self.data_converter.convert_beat_data_to_legacy_format(beat, beat_number)

    def _convert_start_position_to_legacy_format(
        self, start_position_data: BeatData
    ) -> dict:
        """Convert start position BeatData to legacy format"""
        return self.data_converter.convert_start_position_to_legacy_format(
            start_position_data
        )
