"""
SequenceBeatOperations

Handles beat-level operations on sequences.
Responsible for adding, removing, and modifying beats within sequences.
"""

from typing import Optional, Callable
from PyQt6.QtCore import QObject, pyqtSignal

from domain.models.core_models import SequenceData, BeatData
from application.services.option_picker.orientation_update_service import (
    OptionOrientationUpdateService,
)
from application.services.core.sequence_persistence_service import (
    SequencePersistenceService,
)


class SequenceBeatOperations(QObject):
    """
    Service for handling beat-level operations on sequences.

    Responsibilities:
    - Adding beats to sequences
    - Removing beats from sequences
    - Updating beat properties (turns, orientations)
    - Managing beat numbering and sequencing
    """

    beat_added = pyqtSignal(object, int)  # BeatData, position
    beat_removed = pyqtSignal(int)  # position
    beat_updated = pyqtSignal(object, int)  # BeatData, position

    def __init__(
        self,
        workbench_getter: Optional[Callable[[], object]] = None,
        workbench_setter: Optional[Callable[[SequenceData], None]] = None,
        data_converter: Optional[object] = None,
    ):
        super().__init__()
        self.workbench_getter = workbench_getter
        self.workbench_setter = workbench_setter
        self.data_converter = data_converter
        self.orientation_update_service = OptionOrientationUpdateService()
        self.persistence_service = SequencePersistenceService()

    def add_beat_to_sequence(self, beat_data: BeatData):
        """Add a beat to the current sequence"""
        current_sequence = self._get_current_sequence()
        if current_sequence is None:
            current_sequence = SequenceData.empty()

        try:
            # Add beat to sequence
            new_sequence = current_sequence.add_beat(beat_data)

            # Update workbench
            if self.workbench_setter:
                self.workbench_setter(new_sequence)

            # Save to persistence
            self._save_sequence_to_persistence(new_sequence)

            # Emit signal
            position = len(new_sequence.beats) - 1
            self.beat_added.emit(beat_data, position)

            print(f"✅ Added beat {beat_data.letter} to sequence (position {position})")

        except Exception as e:
            print(f"❌ Error adding beat to sequence: {e}")
            import traceback

            traceback.print_exc()

    def remove_beat(self, beat_index: int):
        """Remove a beat from the sequence - exactly like legacy"""
        try:
            current_sequence = self._get_current_sequence()
            if not current_sequence or beat_index >= len(current_sequence.beats):
                return

            # Remove beat from sequence
            beat_to_remove = current_sequence.beats[beat_index]
            new_beats = current_sequence.beats.copy()
            new_beats.pop(beat_index)

            # Update beat numbers for remaining beats
            for i, beat in enumerate(new_beats):
                new_beats[i] = beat.update(beat_number=i + 1)

            new_sequence = current_sequence.update(beats=new_beats)

            # Update workbench
            if self.workbench_setter:
                self.workbench_setter(new_sequence)

            # Save to persistence
            self._save_sequence_to_persistence(new_sequence)

            # Remove from persistence service
            self.persistence_service.remove_beat_at_index(beat_index)

            # Emit signal
            self.beat_removed.emit(beat_index)

            print(f"✅ Removed beat {beat_to_remove.letter} from position {beat_index}")

        except Exception as e:
            print(f"❌ Failed to remove beat: {e}")
            import traceback

            traceback.print_exc()

    def update_beat_turns(self, beat_index: int, color: str, new_turns: int):
        """Update the number of turns for a specific beat - exactly like legacy"""
        try:
            current_sequence = self._get_current_sequence()
            if not current_sequence or beat_index >= len(current_sequence.beats):
                return

            beat = current_sequence.beats[beat_index]

            # Update the appropriate motion based on color
            if color.lower() == "blue" and beat.blue_motion:
                updated_motion = beat.blue_motion.update(turns=new_turns)
                updated_beat = beat.update(blue_motion=updated_motion)
            elif color.lower() == "red" and beat.red_motion:
                updated_motion = beat.red_motion.update(turns=new_turns)
                updated_beat = beat.update(red_motion=updated_motion)
            else:
                print(f"⚠️ Invalid color '{color}' or missing motion data")
                return

            # Update sequence
            new_beats = current_sequence.beats.copy()
            new_beats[beat_index] = updated_beat
            new_sequence = current_sequence.update(beats=new_beats)

            # Update workbench
            if self.workbench_setter:
                self.workbench_setter(new_sequence)

            # Save to persistence
            self._save_sequence_to_persistence(new_sequence)

            # Emit signal
            self.beat_updated.emit(updated_beat, beat_index)

            print(f"✅ Updated {color} turns for beat {beat.letter} to {new_turns}")

        except Exception as e:
            print(f"❌ Failed to update beat turns: {e}")
            import traceback

            traceback.print_exc()

    def update_beat_orientation(
        self, beat_index: int, color: str, new_orientation: int
    ):
        """Update the orientation for a specific beat"""
        try:
            current_sequence = self._get_current_sequence()
            if not current_sequence or beat_index >= len(current_sequence.beats):
                return

            beat = current_sequence.beats[beat_index]

            # Update the appropriate motion based on color
            if color.lower() == "blue" and beat.blue_motion:
                updated_motion = beat.blue_motion.update(
                    start_orientation=new_orientation, end_orientation=new_orientation
                )
                updated_beat = beat.update(blue_motion=updated_motion)
            elif color.lower() == "red" and beat.red_motion:
                updated_motion = beat.red_motion.update(
                    start_orientation=new_orientation, end_orientation=new_orientation
                )
                updated_beat = beat.update(red_motion=updated_motion)
            else:
                print(f"⚠️ Invalid color '{color}' or missing motion data")
                return

            # Update sequence
            new_beats = current_sequence.beats.copy()
            new_beats[beat_index] = updated_beat
            new_sequence = current_sequence.update(beats=new_beats)

            # Update workbench
            if self.workbench_setter:
                self.workbench_setter(new_sequence)

            # Save to persistence
            self._save_sequence_to_persistence(new_sequence)

            # Emit signal
            self.beat_updated.emit(updated_beat, beat_index)

            print(
                f"✅ Updated {color} orientation for beat {beat.letter} to {new_orientation}"
            )

        except Exception as e:
            print(f"❌ Failed to update beat orientation: {e}")
            import traceback

            traceback.print_exc()

    def _get_current_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence from workbench"""
        if self.workbench_getter:
            try:
                workbench = self.workbench_getter()
                if workbench and hasattr(workbench, "get_sequence"):
                    return workbench.get_sequence()
            except Exception as e:
                print(f"❌ Error getting current sequence: {e}")
        return None

    def _save_sequence_to_persistence(self, sequence: SequenceData):
        """Convert modern SequenceData to legacy format and save to current_sequence.json"""
        if not self.data_converter:
            print("⚠️ No data converter available for persistence")
            return

        try:
            # Load existing sequence to preserve start position
            existing_sequence = self.persistence_service.load_current_sequence()

            # Check if there's an existing start position (beat 0)
            existing_start_position = None
            if len(existing_sequence) > 1 and existing_sequence[1].get("beat") == 0:
                existing_start_position = existing_sequence[1]
                print(
                    f"✅ Preserving existing start position: {existing_start_position.get('sequence_start_position', 'unknown')}"
                )

            # Convert beats to legacy format (these will be beat 1, 2, 3, etc.)
            legacy_beats = []
            for i, beat in enumerate(sequence.beats):
                beat_dict = self.data_converter.convert_beat_data_to_legacy_format(
                    beat, i + 1
                )
                legacy_beats.append(beat_dict)

            # Create metadata
            metadata = {
                "word": self._calculate_sequence_word(sequence),
                "author": "modern",
                "level": 0,
                "prop_type": "staff",
                "grid_mode": "diamond",
            }

            # Build complete sequence
            complete_sequence = [metadata]

            # Add start position if it exists
            if existing_start_position:
                complete_sequence.append(existing_start_position)

            # Add beats
            complete_sequence.extend(legacy_beats)

            # Save to persistence
            self.persistence_service.save_current_sequence(complete_sequence)

            print(f"✅ Saved sequence with {len(legacy_beats)} beats to persistence")

        except Exception as e:
            print(f"❌ Failed to save sequence to persistence: {e}")
            import traceback

            traceback.print_exc()

    def _calculate_sequence_word(self, sequence: SequenceData) -> str:
        """Calculate sequence word from beat letters exactly like legacy"""
        if not sequence.beats:
            return ""

        # Extract letters from beats exactly like legacy calculate_word method
        word = "".join(beat.letter for beat in sequence.beats)

        # Apply word simplification for circular sequences like legacy
        return self._simplify_repeated_word(word)

    def _simplify_repeated_word(self, word: str) -> str:
        """Simplify repeated patterns exactly like legacy WordSimplifier"""

        def can_form_by_repeating(s: str, pattern: str) -> bool:
            pattern_len = len(pattern)
            return all(
                s[i : i + pattern_len] == pattern for i in range(0, len(s), pattern_len)
            )

        n = len(word)
        for i in range(1, n // 2 + 1):
            pattern = word[:i]
            if n % i == 0 and can_form_by_repeating(word, pattern):
                return pattern
        return word

    def _save_sequence_to_persistence(self, sequence: SequenceData):
        """Convert modern SequenceData to legacy format and save to current_sequence.json"""
        try:
            import json
            from pathlib import Path

            # Convert to legacy format using data converter
            legacy_data = self.data_converter.convert_sequence_to_legacy_format(
                sequence
            )

            # Save to current_sequence.json (same location as legacy)
            sequence_file = Path("src/desktop/modern/current_sequence.json")
            with open(sequence_file, "w") as f:
                json.dump(legacy_data, f, indent=2)

            print(
                f"✅ [BEAT_OPERATIONS] Sequence saved to persistence: {len(legacy_data)} items"
            )

        except Exception as e:
            print(f"❌ [BEAT_OPERATIONS] Failed to save sequence to persistence: {e}")
            import traceback

            traceback.print_exc()
