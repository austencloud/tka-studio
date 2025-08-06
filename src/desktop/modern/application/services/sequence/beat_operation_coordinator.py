"""
BeatOperationCoordinator - Orchestrates Focused Beat Services

Single Responsibility: Coordinating beat operations using focused services.
Replaces the monolithic SequenceBeatOperations God Object.
"""

from __future__ import annotations

from collections.abc import Callable

from PyQt6.QtCore import QObject, pyqtSignal
from shared.application.services.option_picker.option_orientation_updater import (
    OptionOrientationUpdater,
)
from shared.application.services.sequence.sequence_persister import SequencePersister

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.sequence_data import SequenceData

from .beat_creation_service import BeatCreationService
from .beat_sequence_service import BeatSequenceService
from .sequence_word_calculator import SequenceWordCalculator


class BeatOperationCoordinator(QObject):
    """
    Coordinator service that orchestrates focused beat services.

    Responsibilities:
    - Coordinating operations between focused services
    - Emitting Qt signals for UI integration
    - Managing workbench integration
    - Providing backward-compatible API
    """

    # Qt signals for UI integration
    beat_added = pyqtSignal(object, int, object)  # BeatData, position, SequenceData
    beat_removed = pyqtSignal(int)  # position
    beat_updated = pyqtSignal(object, int)  # BeatData, position

    def __init__(
        self,
        workbench_getter: Callable[[], object] | None = None,
        workbench_setter: Callable[[SequenceData], None] | None = None,
        beat_creator: BeatCreationService | None = None,
        sequence_service: BeatSequenceService | None = None,
        word_calculator: SequenceWordCalculator | None = None,
        persistence: SequencePersister | None = None,
    ):
        super().__init__()

        # Workbench integration
        self.workbench_getter = workbench_getter
        self.workbench_setter = workbench_setter

        # Focused services - create defaults if not provided
        self.beat_creator = beat_creator or BeatCreationService()
        self.sequence_service = sequence_service or BeatSequenceService()
        self.word_calculator = word_calculator or SequenceWordCalculator()
        self.persistence = persistence or SequencePersister()

        # Legacy services still needed
        self.orientation_update_service = OptionOrientationUpdater()

        # Guard to prevent duplicate beat additions
        self._adding_beat = False

    def add_pictograph_to_sequence(self, pictograph_data: PictographData) -> None:
        """
        Add pictograph to sequence by creating beat with embedded pictograph.

        Args:
            pictograph_data: The pictograph to add as a beat
        """
        try:
            current_sequence = self.get_current_sequence()

            # Use focused service to create the beat
            beat_data = self.beat_creator.create_beat_from_pictograph(
                pictograph_data, current_sequence
            )

            # Use existing beat addition logic
            self.add_beat_to_sequence(beat_data)

        except Exception as e:
            print(f"❌ Error adding pictograph to sequence: {e}")
            import traceback

            traceback.print_exc()

    def add_beat_to_sequence(self, beat_data: BeatData) -> None:
        """
        Add beat to sequence using focused services.

        Args:
            beat_data: The beat to add to the sequence
        """
        print(f"🎯 [COORDINATOR] add_beat_to_sequence called for: {beat_data.letter}")

        # Guard against duplicate calls
        if self._adding_beat:
            return

        self._adding_beat = True
        try:
            current_sequence = self.get_current_sequence()
            if current_sequence is None:
                current_sequence = SequenceData.empty()
                print("🎯 [COORDINATOR] Creating empty sequence")

            # Use focused service to add beat
            new_sequence = self.sequence_service.add_beat(current_sequence, beat_data)

            # Calculate word using focused service
            word = self.word_calculator.calculate_word(new_sequence)

            # Update workbench if setter available
            if self.workbench_setter:
                print(
                    f"🎯 [COORDINATOR] Updating workbench with sequence length: {len(new_sequence.beats)}"
                )
                self.workbench_setter(new_sequence)

            # Save using focused service
            self.persistence.save_sequence(new_sequence, word)

            # Emit signal with updated sequence
            position = len(new_sequence.beats) - 1
            print(
                f"🎯 [COORDINATOR] Emitting beat_added signal for position: {position}"
            )
            self.beat_added.emit(beat_data, position, new_sequence)

        except Exception as e:
            print(f"❌ [COORDINATOR] Error adding beat to sequence: {e}")
            import traceback

            traceback.print_exc()
        finally:
            self._adding_beat = False

    def update_beat_turns(self, beat_index: int, color: str, new_turns: int) -> None:
        """
        Update the number of turns for a specific beat using focused services.

        Args:
            beat_index: Index of the beat to update
            color: Color/side of the motion to update
            new_turns: New number of turns
        """
        try:
            current_sequence = self.get_current_sequence()
            if not current_sequence:
                return

            # Use focused service to update beat
            updated_sequence = self.sequence_service.update_beat_turns(
                current_sequence, beat_index, color, new_turns
            )

            # Calculate word using focused service
            word = self.word_calculator.calculate_word(updated_sequence)

            # Update workbench
            if self.workbench_setter:
                self.workbench_setter(updated_sequence)

            # Save using focused service
            self.persistence.save_sequence(updated_sequence, word)

            # Emit signal
            updated_beat = updated_sequence.beats[beat_index]
            self.beat_updated.emit(updated_beat, beat_index)

            print(
                f"✅ Updated {color} turns for beat {updated_beat.letter} to {new_turns}"
            )

        except Exception as e:
            print(f"❌ Failed to update beat turns: {e}")
            import traceback

            traceback.print_exc()

    def update_beat_orientation(
        self, beat_index: int, color: str, new_orientation: int
    ) -> None:
        """
        Update the orientation for a specific beat using focused services.

        Args:
            beat_index: Index of the beat to update
            color: Color/side of the motion to update
            new_orientation: New orientation value
        """
        try:
            current_sequence = self.get_current_sequence()
            if not current_sequence:
                return

            # Use focused service to update beat
            updated_sequence = self.sequence_service.update_beat_orientation(
                current_sequence, beat_index, color, new_orientation
            )

            # Calculate word using focused service
            word = self.word_calculator.calculate_word(updated_sequence)

            # Update workbench
            if self.workbench_setter:
                self.workbench_setter(updated_sequence)

            # Save using focused service
            self.persistence.save_sequence(updated_sequence, word)

            # Emit signal
            updated_beat = updated_sequence.beats[beat_index]
            self.beat_updated.emit(updated_beat, beat_index)

            print(
                f"✅ Updated {color} orientation for beat {updated_beat.letter} to {new_orientation}"
            )

        except Exception as e:
            print(f"❌ Failed to update beat orientation: {e}")
            import traceback

            traceback.print_exc()

    def remove_beat(self, beat_index: int) -> None:
        """
        Remove a beat from the sequence using focused services.

        Args:
            beat_index: Index of the beat to remove
        """
        try:
            current_sequence = self.get_current_sequence()
            if not current_sequence:
                print(
                    f"⚠️ Cannot remove beat at index {beat_index}: no current sequence"
                )
                return

            print(f"🗑️ [COORDINATOR] Removing beat at index {beat_index}")

            # Get the beat to remove for logging
            beat_to_remove = current_sequence.beats[beat_index]

            # Use focused service to remove beat
            updated_sequence = self.sequence_service.remove_beat(
                current_sequence, beat_index
            )

            # Calculate word using focused service
            word = self.word_calculator.calculate_word(updated_sequence)

            # Update workbench
            if self.workbench_setter:
                self.workbench_setter(updated_sequence)

            # Save using focused service
            self.persistence.save_sequence(updated_sequence, word)

            # Emit signal
            self.beat_removed.emit(beat_index)

            print(
                f"✅ [COORDINATOR] Successfully removed beat {beat_to_remove.letter} from position {beat_index}"
            )

        except Exception as e:
            print(f"❌ [COORDINATOR] Failed to remove beat: {e}")
            import traceback

            traceback.print_exc()

    def delete_beat(self, sequence: SequenceData, beat_index: int) -> SequenceData:
        """
        Delete beat and all following beats using focused services.

        Args:
            sequence: The sequence to modify
            beat_index: Index of the beat to delete (and all following)

        Returns:
            Updated sequence with beat and following beats removed
        """
        try:
            print(
                f"🗑️ [COORDINATOR] Deleting beat at index {beat_index} and all following beats"
            )

            # Use focused service to delete beat and following
            updated_sequence = self.sequence_service.delete_beat_and_following(
                sequence, beat_index
            )

            print("✅ [COORDINATOR] Successfully deleted beat and following beats")
            print(
                f"📊 [COORDINATOR] Sequence now has {len(updated_sequence.beats)} beats"
            )

            return updated_sequence

        except Exception as e:
            print(f"❌ [COORDINATOR] Failed to delete beat: {e}")
            import traceback

            traceback.print_exc()
            raise

    def get_current_sequence(self) -> SequenceData | None:
        """
        Get the current sequence from workbench.

        Returns:
            Current sequence or None if not available
        """
        print("🔍 [COORDINATOR] Getting current sequence...")
        print(f"   Workbench getter: {self.workbench_getter}")

        if self.workbench_getter:
            try:
                workbench = self.workbench_getter()
                print(f"   Workbench from getter: {workbench}")

                if workbench and hasattr(workbench, "get_sequence"):
                    sequence = workbench.get_sequence()
                    if sequence:
                        print(f"   Sequence length: {sequence.length}")
                    return sequence
                print("   ❌ Workbench is None or has no get_sequence method")
            except Exception as e:
                print(f"❌ Error getting current sequence: {e}")
                import traceback

                traceback.print_exc()
        else:
            print("   ❌ No workbench getter configured")
        return None
