"""
SequenceBeatOperations

Handles beat-level operations on sequences.
Responsible for adding, removing, and modifying beats within sequences.
"""

from typing import Callable, Optional

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.sequence_data import SequenceData
from shared.application.services.data.modern_to_legacy_converter import (
    ModernToLegacyConverter,
)
from shared.application.services.option_picker.option_orientation_updater import (
    OptionOrientationUpdater,
)
from shared.application.services.sequence.beat_factory import BeatFactory
from shared.application.services.sequence.sequence_beat_service import (
    SequenceBeatService,
)
from shared.application.services.sequence.sequence_persister import SequencePersister


class SequenceBeatOperations(QObject):
    """
    Service for handling beat-level operations on sequences.

    Responsibilities:
    - Adding beats to sequences
    - Removing beats from sequences
    - Updating beat properties (turns, orientations)
    - Managing beat numbering and sequencing
    """

    beat_added = pyqtSignal(object, int, object)  # BeatData, position, SequenceData
    beat_removed = pyqtSignal(int)  # position
    beat_updated = pyqtSignal(object, int)  # BeatData, position

    def __init__(
        self,
        workbench_getter: Optional[Callable[[], object]] = None,
        workbench_setter: Optional[Callable[[SequenceData], None]] = None,
        modern_to_legacy_converter: Optional[ModernToLegacyConverter] = None,
    ):
        super().__init__()
        self.workbench_getter: Callable[[], object] = workbench_getter
        self.workbench_setter = workbench_setter
        self.modern_to_legacy_converter = (
            modern_to_legacy_converter or ModernToLegacyConverter()
        )
        self.orientation_update_service = OptionOrientationUpdater()
        self.persistence_service = SequencePersister()

        # Guard to prevent duplicate beat additions
        self._adding_beat = False

    def add_pictograph_to_sequence(self, pictograph_data: PictographData):
        """Add pictograph to sequence by creating beat with embedded pictograph."""

        try:
            # Calculate beat number
            current_sequence = self.get_current_sequence()
            beat_number = self._calculate_next_beat_number(current_sequence)

            # Create beat data with embedded pictograph using factory
            beat_data = BeatFactory.create_from_pictograph(
                pictograph_data=pictograph_data, beat_number=beat_number
            )

            # Use existing beat addition logic
            self.add_beat_to_sequence(beat_data)

        except Exception as e:
            print(f"❌ Error adding pictograph to sequence: {e}")
            import traceback

            traceback.print_exc()

    def _calculate_next_beat_number(
        self, current_sequence: Optional[SequenceData]
    ) -> int:
        """Calculate the next beat number for a new beat."""
        if current_sequence and current_sequence.beats:
            # Check if first beat is a start position (beat_number=0)
            has_start_position = (
                current_sequence.beats[0].metadata.get("is_start_position", False)
                and current_sequence.beats[0].beat_number == 0
            )

            if has_start_position:
                # Regular beats start from 1, so beat_number = number of non-start-position beats + 1
                regular_beats_count = len(current_sequence.beats) - 1
                beat_number = regular_beats_count + 1
            else:
                # No start position, so beat_number = total beats + 1
                beat_number = len(current_sequence.beats) + 1
        else:
            # Empty sequence, first beat is beat 1
            beat_number = 1

        return beat_number

    def add_beat_to_sequence(self, beat_data: BeatData):
        """Add beat to sequence using the most appropriate method"""
        print(
            f"🎯 [BEAT_OPERATIONS] add_beat_to_sequence called for: {beat_data.letter}"
        )
        print(
            f"🎯 [BEAT_OPERATIONS] Has workbench_setter: {self.workbench_setter is not None}"
        )
        try:
            # If we have a workbench setter, use direct manipulation for immediate UI updates
            if self.workbench_setter:
                print(
                    f"🎯 [BEAT_OPERATIONS] Using direct manipulation via workbench setter"
                )
                self._add_beat_direct(beat_data)
                return

            # Otherwise, try command system for undo/redo support
            # Import command system
            from desktop.modern.core.commands.sequence_commands import AddBeatCommand
            from desktop.modern.core.service_locator import get_sequence_state_manager

            # Command processor and event bus removed - using Qt signals instead
            # Get services
            state_manager = get_sequence_state_manager()

            if not state_manager:
                print(
                    "⚠️ Command system not available, falling back to direct manipulation"
                )
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
                event_bus=event_bus,
            )

            result = command_processor.execute(command)

            if result.success:
                print(f"✅ Beat added via command: {beat_data.letter}")
                # Emit signal with updated sequence from command result
                position = len(current_sequence.beats)
                updated_sequence = result  # Command returns the updated sequence
                self.beat_added.emit(beat_data, position, updated_sequence)
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
        # Guard against duplicate calls
        if self._adding_beat:
            return

        self._adding_beat = True
        try:
            current_sequence = self.get_current_sequence()
            if current_sequence is None:
                current_sequence = SequenceData.empty()
                print(f"🎯 [BEAT_OPERATIONS] Creating empty sequence")

            print(
                f"🎯 [BEAT_OPERATIONS] Current sequence length before adding: {len(current_sequence.beats)}"
            )

            try:
                # Add beat to sequence
                new_sequence = current_sequence.add_beat(beat_data)
                print(
                    f"🎯 [BEAT_OPERATIONS] New sequence length after adding: {len(new_sequence.beats)}"
                )

                # Update workbench
                if self.workbench_setter:
                    print(
                        f"🎯 [BEAT_OPERATIONS] Calling workbench setter with sequence length: {len(new_sequence.beats)}"
                    )

                    # Add stack trace to see what happens after workbench setter
                    import traceback

                    print(
                        "🔍 [BEAT_OPERATIONS] About to call workbench setter, call stack:"
                    )
                    for line in traceback.format_stack()[-2:]:  # Show current context
                        print(f"    {line.strip()}")

                    self.workbench_setter(new_sequence)
                    print(f"🎯 [BEAT_OPERATIONS] Workbench setter completed")

                # Save to persistence
                self._save_sequence_to_persistence(new_sequence)

                # Emit signal with updated sequence
                position = len(new_sequence.beats) - 1
                print(
                    f"🎯 [BEAT_OPERATIONS] Emitting beat_added signal for position: {position}"
                )
                self.beat_added.emit(beat_data, position, new_sequence)

            except Exception as e:
                print(
                    f"❌ [BEAT_OPERATIONS] Error adding beat to sequence (direct): {e}"
                )
                import traceback

                traceback.print_exc()
        finally:
            # Always reset the guard flag
            self._adding_beat = False

    def update_beat_turns(self, beat_index: int, color: str, new_turns: int):
        """Update the number of turns for a specific beat - exactly like legacy"""
        try:
            current_sequence = self.get_current_sequence()
            if not current_sequence or beat_index >= len(current_sequence.beats):
                return

            beat = current_sequence.beats[beat_index]

            # Update the appropriate motion based on color
            if beat.has_pictograph and color.lower() in beat.pictograph_data.motions:
                motion = beat.pictograph_data.motions[color.lower()]
                updated_motion = motion.update(turns=new_turns)

                # Update the motion in pictograph data
                updated_motions = {
                    **beat.pictograph_data.motions,
                    color.lower(): updated_motion,
                }
                updated_pictograph = beat.pictograph_data.update(
                    motions=updated_motions
                )
                updated_beat = beat.update(pictograph_data=updated_pictograph)
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
            current_sequence = self.get_current_sequence()
            if not current_sequence or beat_index >= len(current_sequence.beats):
                return

            beat = current_sequence.beats[beat_index]

            # Update the appropriate motion based on color
            if beat.has_pictograph and color.lower() in beat.pictograph_data.motions:
                motion = beat.pictograph_data.motions[color.lower()]
                updated_motion = motion.update(
                    start_ori=new_orientation, end_ori=new_orientation
                )

                # Update the motion in pictograph data
                updated_motions = {
                    **beat.pictograph_data.motions,
                    color.lower(): updated_motion,
                }
                updated_pictograph = beat.pictograph_data.update(
                    motions=updated_motions
                )
                updated_beat = beat.update(pictograph_data=updated_pictograph)
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

    def remove_beat(self, beat_index: int):
        """Remove a beat from the sequence"""
        try:
            current_sequence = self.get_current_sequence()
            if not current_sequence or beat_index >= len(current_sequence.beats):
                print(
                    f"⚠️ Cannot remove beat at index {beat_index}: invalid index or empty sequence"
                )
                return

            print(f"🗑️ [BEAT_OPERATIONS] Removing beat at index {beat_index}")

            # Get the beat to remove for logging
            beat_to_remove = current_sequence.beats[beat_index]

            # Remove the beat
            updated_beats = list(current_sequence.beats)
            updated_beats.pop(beat_index)

            # Renumber remaining beats
            for i, beat in enumerate(updated_beats):
                updated_beats[i] = beat.update(beat_number=i + 1)

            updated_sequence = current_sequence.update(beats=updated_beats)

            # Update workbench
            if self.workbench_setter:
                self.workbench_setter(updated_sequence)

            # Save to persistence
            self._save_sequence_to_persistence(updated_sequence)

            # Emit signal
            self.beat_removed.emit(beat_index)

            print(
                f"✅ [BEAT_OPERATIONS] Successfully removed beat {beat_to_remove.letter} from position {beat_index}"
            )

        except Exception as e:
            print(f"❌ [BEAT_OPERATIONS] Failed to remove beat: {e}")
            import traceback

            traceback.print_exc()

    def delete_beat(self, sequence: SequenceData, beat_index: int) -> SequenceData:
        """
        Delete beat and all following beats from the sequence (legacy behavior).

        This matches the exact behavior from the legacy version where deleting a beat
        removes that beat and all subsequent beats from the sequence.

        Args:
            sequence: The sequence to modify
            beat_index: Index of the beat to delete (and all following)

        Returns:
            Updated sequence with beat and following beats removed

        Raises:
            ValueError: If beat_index is invalid
        """
        if not sequence or beat_index < 0 or beat_index >= len(sequence.beats):
            raise ValueError(f"Invalid beat index: {beat_index}")

        print(
            f"🗑️ [BEAT_OPERATIONS] Deleting beat at index {beat_index} and all following beats"
        )

        # Get the beat being deleted for logging
        beat_to_delete = sequence.beats[beat_index]
        beats_to_remove = sequence.beats[beat_index:]

        print(
            f"🗑️ [BEAT_OPERATIONS] Removing {len(beats_to_remove)} beats starting from {beat_to_delete.letter}"
        )

        # Keep only beats before the deletion point
        remaining_beats = list(sequence.beats[:beat_index])

        # Create updated sequence with remaining beats
        updated_sequence = sequence.update(beats=remaining_beats)

        print(
            f"✅ [BEAT_OPERATIONS] Successfully deleted beat {beat_to_delete.letter} and {len(beats_to_remove) - 1} following beats"
        )
        print(f"📊 [BEAT_OPERATIONS] Sequence now has {len(remaining_beats)} beats")

        return updated_sequence

    def get_current_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence from workbench"""
        print(f"🔍 [BEAT_OPERATIONS] Getting current sequence...")
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
                else:
                    print(f"   ❌ Workbench is None or has no get_sequence method")
            except Exception as e:
                print(f"❌ Error getting current sequence: {e}")
                import traceback

                traceback.print_exc()
        else:
            print(f"   ❌ No workbench getter configured")
        return None

    def _save_sequence_to_persistence(self, sequence: SequenceData):
        """Convert modern SequenceData to legacy format and save to current_sequence.json"""

        try:
            # Load existing sequence to preserve start position
            existing_sequence = self.persistence_service.load_current_sequence()

            # Check if there's an existing start position (beat 0)
            existing_start_position = None
            if len(existing_sequence) > 1 and existing_sequence[1].get("beat") == 0:
                existing_start_position = existing_sequence[1]

            # Convert beats to legacy format (these will be beat 1, 2, 3, etc.)
            legacy_beats = []
            # Removed repetitive log statements
            for i, beat in enumerate(sequence.beats):
                try:
                    beat_dict = self.modern_to_legacy_converter.convert_beat_data_to_legacy_format(
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

    def get_beat_service(self) -> SequenceBeatService:
        """Get the pure beat service for interface-based operations."""
        if not hasattr(self, "_beat_service"):
            self._beat_service = SequenceBeatService(
                sequence_getter=self.get_current_sequence,
                sequence_setter=self.workbench_setter,
                persister=self.persister,
            )
        return self._beat_service
