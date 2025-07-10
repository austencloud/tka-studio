"""
SequenceBeatOperations

Handles beat-level operations on sequences.
Responsible for adding, removing, and modifying beats within sequences.
"""

from typing import Callable, Optional

from application.services.core.sequence_persistence_service import (
    SequencePersistenceService,
)
from application.services.option_picker.orientation_update_service import (
    OptionOrientationUpdateService,
)
from PyQt6.QtCore import QObject, pyqtSignal

from domain.models.beat_data import BeatData
from domain.models.sequence_models import SequenceData


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
        """Add beat via command pattern instead of direct manipulation"""
        try:
            # Import command system
            from core.commands.sequence_commands import AddBeatCommand
            from core.service_locator import get_command_processor, get_event_bus, get_sequence_state_manager
            
            # Get services
            command_processor = get_command_processor()
            event_bus = get_event_bus()
            state_manager = get_sequence_state_manager()
            
            if not command_processor or not event_bus:
                print("⚠️ Command system not available, falling back to direct manipulation")
                self._add_beat_direct(beat_data)
                return
                
            # Get current sequence from state manager
            current_sequence = state_manager.get_sequence() if state_manager else None
            if not current_sequence:
                current_sequence = SequenceData.empty()
                print("📝 Creating new empty sequence for first beat")
            
            # Create and execute command
            command = AddBeatCommand(
                sequence=current_sequence,
                beat=beat_data,
                position=len(current_sequence.beats),
                event_bus=event_bus
            )
            
            result = command_processor.execute(command)
            
            if result.success:
                print(f"✅ Beat added via command: {beat_data.letter}")
                # Emit legacy signal for backward compatibility
                position = len(current_sequence.beats)
                self.beat_added.emit(beat_data, position)
            else:
                print(f"❌ Failed to add beat via command: {result.error_message}")
                # Fallback to direct manipulation
                self._add_beat_direct(beat_data)
                
        except Exception as e:
            print(f"❌ Error in command-based beat addition: {e}")
            # Fallback to direct manipulation
            self._add_beat_direct(beat_data)
            
    def _add_beat_direct(self, beat_data: BeatData):
        """Fallback method: Add beat via direct manipulation (original logic)"""
        current_sequence = self._get_current_sequence()
        if current_sequence is None:
            current_sequence = SequenceData.empty()

        try:
            # Add beat to sequence
            new_sequence = current_sequence.add_beat(beat_data)

            # Update workbench
            if self.workbench_setter:
                self.workbench_setter(new_sequence)
                print(f"✅ [BEAT_OPERATIONS] Updated workbench (direct)")

            # Save to persistence
            self._save_sequence_to_persistence(new_sequence)

            # Emit signal
            position = len(new_sequence.beats) - 1
            self.beat_added.emit(beat_data, position)

            print(f"✅ [BEAT_OPERATIONS] Added beat {beat_data.letter} to sequence (direct, position {position})")

        except Exception as e:
            print(f"❌ [BEAT_OPERATIONS] Error adding beat to sequence (direct): {e}")
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
            # Removed repetitive log statements
            for i, beat in enumerate(sequence.beats):
                try:
                    beat_dict = self.data_converter.convert_beat_data_to_legacy_format(
                        beat, i + 1
                    )
                    legacy_beats.append(beat_dict)
                except Exception as e:
                    print(
                        f"❌ [PERSISTENCE] Failed to convert beat {i} ({beat.letter}): {e}"
                    )
                    import traceback

                    traceback.print_exc()

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

            # Removed repetitive log statements

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
