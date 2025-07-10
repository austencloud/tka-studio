"""
Sequence Manager - Pure Business Logic for Sequence Operations

This service contains the core business logic for managing sequence operations
without any Qt dependencies. It implements sequence management functionality
and uses dependency injection for signal emission.

ARCHITECTURE:
Application Layer → SequenceManager → SequencePersister
Presentation Layer → SequenceManagerQtAdapter → SequenceManager
"""

import logging
from typing import Callable, List, Optional

from application.services.option_picker.option_orientation_updater import (
    OptionOrientationUpdater,
)
from application.services.sequence.persister import SequencePersister
from domain.models.beat_data import BeatData
from domain.models.sequence_models import SequenceData

logger = logging.getLogger(__name__)


class ISequenceManagerSignals:
    """Interface for sequence manager signal emission."""

    def emit_sequence_modified(self, sequence: SequenceData) -> None:
        """Emit signal when sequence is modified."""
        pass

    def emit_sequence_cleared(self) -> None:
        """Emit signal when sequence is cleared."""
        pass


class SequenceManager:
    """
    Pure business service for managing sequence operations.

    This service contains all the business logic for sequence operations
    without any Qt dependencies. Signal emission is abstracted through
    the ISequenceManagerSignals interface.
    """

    def __init__(
        self,
        workbench_getter: Optional[Callable[[], object]] = None,
        workbench_setter: Optional[Callable[[SequenceData], None]] = None,
        start_position_handler: Optional[object] = None,
        signal_emitter: Optional[ISequenceManagerSignals] = None,
    ):
        """
        Initialize the sequence manager.

        Args:
            workbench_getter: Function to get current workbench
            workbench_setter: Function to set workbench sequence
            start_position_handler: Handler for start position operations
            signal_emitter: Optional signal emitter for notifications
        """
        self.workbench_getter = workbench_getter
        self.workbench_setter = workbench_setter
        self.start_position_handler = start_position_handler
        self._signal_emitter = signal_emitter
        self._emitting_signal = False
        self.orientation_update_service = OptionOrientationUpdater()

        # Initialize sequence persistence service - exactly like legacy
        self.persistence_service = SequencePersister()

    def add_beat_to_sequence(self, beat_data: BeatData):
        """Add a beat to the current sequence"""
        current_sequence = self._get_current_sequence()
        if current_sequence is None:
            current_sequence = SequenceData.empty()

        try:
            if current_sequence.length > 0:
                updated_beats = (
                    self.orientation_update_service.update_option_orientations(
                        current_sequence, [beat_data]
                    )
                )
                beat_data = updated_beats[0]

            new_beat = beat_data.update(
                beat_number=current_sequence.length + 1,
                duration=1.0,
            )

            updated_beats = current_sequence.beats + [new_beat]
            updated_sequence = current_sequence.update(beats=updated_beats)

            # Update current_sequence.json file - exactly like legacy
            self._save_sequence_to_persistence(updated_sequence)

            if self.workbench_setter:
                self.workbench_setter(updated_sequence)
            else:
                self._emit_sequence_modified(updated_sequence)

        except Exception as e:
            logger.error(f"Error adding beat to sequence: {e}")
            raise

    def clear_sequence(self):
        """Clear the current sequence - V1 behavior: hide all beats, keep start position visible"""
        # Clear current_sequence.json file - exactly like legacy
        self.persistence_service.clear_all_beats()

        if self.workbench_setter:
            self.workbench_setter(SequenceData.empty())

        if self._signal_emitter:
            self._signal_emitter.emit_sequence_cleared()

    def handle_workbench_modified(self, sequence: SequenceData):
        """Handle workbench sequence modification with circular emission protection"""
        if self._emitting_signal:
            return

        try:
            self._emitting_signal = True
            # Update current_sequence.json file when sequence is modified - exactly like legacy
            self._save_sequence_to_persistence(sequence)
            if self._signal_emitter:
                self._signal_emitter.emit_sequence_modified(sequence)
        except Exception as e:
            logger.error(f"Signal emission failed: {e}")
            raise
        finally:
            self._emitting_signal = False

    def update_beat_turns(self, beat_index: int, color: str, new_turns: int):
        """Update the number of turns for a specific beat - exactly like legacy"""
        try:
            current_sequence = self._get_current_sequence()
            if not current_sequence or beat_index >= len(current_sequence.beats):
                return

            # Update the beat in memory
            updated_beats = list(current_sequence.beats)
            beat = updated_beats[beat_index]

            # Update the turn count for the specified color
            if color == "blue":
                updated_beat = beat.update(blue_turns=new_turns)
            elif color == "red":
                updated_beat = beat.update(red_turns=new_turns)
            else:
                return

            updated_beats[beat_index] = updated_beat
            updated_sequence = current_sequence.update(beats=updated_beats)

            # Save to persistence and update workbench
            self._save_sequence_to_persistence(updated_sequence)

            if self.workbench_setter:
                self.workbench_setter(updated_sequence)

            logger.info(f"Updated {color} turns for beat {beat_index} to {new_turns}")

        except Exception as e:
            logger.error(f"Failed to update beat turns: {e}")
            raise

    def remove_beat(self, beat_index: int):
        """Remove a beat from the sequence - exactly like legacy"""
        try:
            current_sequence = self._get_current_sequence()
            if not current_sequence or beat_index >= len(current_sequence.beats):
                return

            # Remove the beat
            updated_beats = list(current_sequence.beats)
            updated_beats.pop(beat_index)

            # Renumber remaining beats
            for i, beat in enumerate(updated_beats):
                updated_beats[i] = beat.update(beat_number=i + 1)

            updated_sequence = current_sequence.update(beats=updated_beats)

            # Save to persistence and update workbench
            self._save_sequence_to_persistence(updated_sequence)

            if self.workbench_setter:
                self.workbench_setter(updated_sequence)

            logger.info(f"Removed beat {beat_index}")

        except Exception as e:
            logger.error(f"Failed to remove beat: {e}")
            raise

    def set_start_position(self, start_position_data: BeatData):
        """Set the start position - exactly like legacy"""
        try:
            # Convert start position to legacy format and save as beat 0
            start_pos_dict = self._convert_start_position_to_legacy_format(
                start_position_data
            )

            # Load current sequence to preserve existing beats
            sequence = self.persistence_service.load_current_sequence()

            # Find where to insert/replace start position
            if len(sequence) == 1:  # Only metadata
                sequence.append(start_pos_dict)
                logger.info("Inserted start position as beat 0")
            elif len(sequence) > 1 and sequence[1].get("beat") == 0:
                # Replace existing start position
                sequence[1] = start_pos_dict
                logger.info("Replaced existing start position")
            else:
                # Insert start position, shifting existing beats
                sequence.insert(1, start_pos_dict)
                logger.info(
                    f"Inserted start position, preserving {len(sequence) - 2} existing beats"
                )

            # Save updated sequence (preserves existing beats)
            self.persistence_service.save_current_sequence(sequence)
            logger.info(f"Set start position: {start_position_data.letter}")

        except Exception as e:
            logger.error(f"Failed to set start position: {e}")
            raise

    def load_sequence_on_startup(self):
        """Load sequence from current_sequence.json on startup - exactly like legacy"""
        try:
            # Load sequence from persistence
            sequence_data = self.persistence_service.load_current_sequence()

            if len(sequence_data) <= 1:
                logger.info("No sequence to load on startup")
                return

            logger.info(
                f"Loading sequence from current_sequence.json with {len(sequence_data)} items"
            )

            # Extract metadata and beats
            metadata = sequence_data[0]
            sequence_word = metadata.get("word", "")
            logger.info(f"Sequence word: '{sequence_word}'")

            # Find start position (beat 0) and actual beats (beat 1+)
            start_position_data = None
            beats_data = []

            for item in sequence_data[1:]:
                if item.get("beat") == 0:
                    start_position_data = item
                    logger.info(
                        f"Found start position: {item.get('sequence_start_position', 'unknown')}"
                    )
                elif "letter" in item and not item.get("is_placeholder", False):
                    beats_data.append(item)
                    logger.info(
                        f"Found beat {item.get('beat', '?')}: {item.get('letter', '?')}"
                    )

            # Convert beats to modern format with full pictograph data
            beat_objects = []
            for i, beat_dict in enumerate(beats_data):
                try:
                    # Convert legacy format back to modern BeatData with full data
                    beat_obj = self._convert_legacy_to_beat_data(beat_dict, i + 1)
                    beat_objects.append(beat_obj)
                    logger.info(f"Converted beat {beat_obj.letter} with motion data")
                except Exception as e:
                    logger.warning(
                        f"Failed to convert beat {beat_dict.get('letter', '?')}: {e}"
                    )
                    # Create fallback beat with proper numbering
                    fallback_beat = BeatData.empty().update(
                        letter=beat_dict.get("letter", "?"),
                        beat_number=i + 1,  # Sequential numbering
                        duration=beat_dict.get("duration", 1.0),
                    )
                    beat_objects.append(fallback_beat)

            # Handle start position loading INDEPENDENTLY of beats
            if start_position_data:
                try:
                    # Extract the position key from the start position data
                    position_key = start_position_data.get(
                        "sequence_start_position", "alpha"
                    )
                    end_pos = start_position_data.get("end_pos", "alpha1")

                    logger.info(f"Loading start position: {position_key} -> {end_pos}")

                    # Create start position BeatData from the saved data
                    start_position_beat = (
                        self._convert_legacy_start_position_to_beat_data(
                            start_position_data
                        )
                    )

                    # Set start position directly in workbench (don't trigger selection flow)
                    workbench = (
                        self.workbench_getter() if self.workbench_getter else None
                    )
                    if workbench and hasattr(workbench, "set_start_position"):
                        workbench.set_start_position(start_position_beat)
                        logger.info(f"Start position loaded into workbench: {end_pos}")
                    else:
                        logger.warning(
                            "Workbench doesn't have set_start_position method"
                        )

                except Exception as e:
                    logger.error(f"Failed to load start position: {e}")
                    raise

            # Create and set the sequence (even if empty, to maintain state)
            loaded_sequence = SequenceData(
                id="loaded_sequence",
                name=sequence_word or "Loaded Sequence",
                beats=beat_objects,  # May be empty, that's fine
            )

            logger.info(
                f"Created sequence: '{loaded_sequence.name}' with {len(beat_objects)} beats"
            )

            # Set sequence in workbench
            if self.workbench_setter:
                self.workbench_setter(loaded_sequence)
                logger.info("Sequence loaded into workbench")

            # Handle UI state transition based on what was loaded
            if start_position_data and not beat_objects:
                logger.info(
                    "Start position loaded with no beats - should show option picker"
                )
            elif not start_position_data and not beat_objects:
                logger.info("No start position or beats found - empty sequence")

        except Exception as e:
            logger.error(f"Failed to load sequence on startup: {e}")
            raise

    def get_current_sequence_length(self) -> int:
        """Get the length of the current sequence"""
        current_sequence = self._get_current_sequence()
        return current_sequence.length if current_sequence else 0

    def _get_current_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence from workbench"""
        if self.workbench_getter:
            try:
                workbench = self.workbench_getter()
                if workbench and hasattr(workbench, "get_sequence"):
                    return workbench.get_sequence()
            except Exception as e:
                logger.error(f"Error getting current sequence: {e}")
        return None

    def _emit_sequence_modified(self, sequence: SequenceData):
        """Emit sequence modified signal with circular emission protection"""
        if not self._emitting_signal and self._signal_emitter:
            try:
                self._emitting_signal = True
                self._signal_emitter.emit_sequence_modified(sequence)
            finally:
                self._emitting_signal = False

    def _save_sequence_to_persistence(self, sequence: SequenceData):
        """Convert modern SequenceData to legacy format and save to current_sequence.json"""
        try:
            # Load existing sequence to preserve start position
            existing_sequence = self.persistence_service.load_current_sequence()

            # Calculate word from beat letters exactly like legacy
            word = self._calculate_sequence_word(sequence)

            # Update metadata with calculated word
            metadata = (
                existing_sequence[0]
                if existing_sequence
                else self.persistence_service.get_default_sequence()[0]
            )
            metadata["word"] = word

            # Check if there's an existing start position (beat 0)
            existing_start_position = None
            if len(existing_sequence) > 1 and existing_sequence[1].get("beat") == 0:
                existing_start_position = existing_sequence[1]
                logger.info(
                    f"Preserving existing start position: {existing_start_position.get('sequence_start_position', 'unknown')}"
                )

            # Convert beats to legacy format (these will be beat 1, 2, 3, etc.)
            legacy_beats = []
            for i, beat in enumerate(sequence.beats):
                beat_dict = self._convert_beat_data_to_legacy_format(beat, i + 1)
                legacy_beats.append(beat_dict)

            # Build final sequence: [metadata, start_position (if exists), beat1, beat2, ...]
            final_sequence = [metadata]
            if existing_start_position:
                final_sequence.append(existing_start_position)
            final_sequence.extend(legacy_beats)

            # Save the complete sequence
            self.persistence_service.save_current_sequence(final_sequence)
            logger.info(
                f"Saved sequence to current_sequence.json: {len(final_sequence)} items (word: '{word}')"
            )

        except Exception as e:
            logger.error(f"Failed to save sequence to persistence: {e}")
            raise

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

    # Legacy conversion methods remain the same...
    def _convert_legacy_to_beat_data(
        self, beat_dict: dict, beat_number: int
    ) -> BeatData:
        """Convert legacy JSON format back to modern BeatData with full pictograph data"""
        from domain.models import (
            BeatData,
            GlyphData,
            Location,
            MotionData,
            MotionType,
            Orientation,
            RotationDirection,
        )

        letter = beat_dict.get("letter", "?")
        duration = beat_dict.get("duration", 1.0)
        start_pos = beat_dict.get("start_pos", "")
        end_pos = beat_dict.get("end_pos", "")
        timing = beat_dict.get("timing", "tog")
        direction = beat_dict.get("direction", "same")

        # Create glyph data with position information
        glyph_data = GlyphData(
            start_position=start_pos,
            end_position=end_pos,
        )

        # Convert blue attributes to MotionData
        blue_motion = None
        blue_attrs = beat_dict.get("blue_attributes", {})
        if blue_attrs:
            try:
                blue_motion = MotionData(
                    motion_type=MotionType(blue_attrs.get("motion_type", "static")),
                    prop_rot_dir=RotationDirection(
                        blue_attrs.get("prop_rot_dir", "no_rot")
                    ),
                    start_loc=Location(blue_attrs.get("start_loc", "s")),
                    end_loc=Location(blue_attrs.get("end_loc", "s")),
                    turns=float(blue_attrs.get("turns", 0)),
                    start_ori=Orientation(blue_attrs.get("start_ori", "in")),
                    end_ori=Orientation(blue_attrs.get("end_ori", "in")),
                )
            except Exception as e:
                logger.warning(f"Failed to create blue motion data: {e}")
                # Fallback to static motion
                blue_motion = MotionData(
                    motion_type=MotionType.STATIC,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.SOUTH,
                    end_loc=Location.SOUTH,
                    start_ori=Orientation.IN,
                    end_ori=Orientation.IN,
                )

        # Convert red attributes to MotionData
        red_motion = None
        red_attrs = beat_dict.get("red_attributes", {})
        if red_attrs:
            try:
                red_motion = MotionData(
                    motion_type=MotionType(red_attrs.get("motion_type", "static")),
                    prop_rot_dir=RotationDirection(
                        red_attrs.get("prop_rot_dir", "no_rot")
                    ),
                    start_loc=Location(red_attrs.get("start_loc", "s")),
                    end_loc=Location(red_attrs.get("end_loc", "s")),
                    turns=float(red_attrs.get("turns", 0)),
                    start_ori=Orientation(red_attrs.get("start_ori", "in")),
                    end_ori=Orientation(red_attrs.get("end_ori", "in")),
                )
            except Exception as e:
                logger.warning(f"Failed to create red motion data: {e}")
                # Fallback to static motion
                red_motion = MotionData(
                    motion_type=MotionType.STATIC,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.SOUTH,
                    end_loc=Location.SOUTH,
                    start_ori=Orientation.IN,
                    end_ori=Orientation.IN,
                )

        # Create BeatData with all the extracted data
        beat_data = BeatData(
            beat_number=beat_number,
            letter=letter,
            duration=duration,
            blue_motion=blue_motion,
            red_motion=red_motion,
            glyph_data=glyph_data,
            metadata={
                "timing": timing,
                "direction": direction,
                "original_beat_number": beat_dict.get("beat", beat_number),
            },
        )

        return beat_data

    def _convert_legacy_start_position_to_beat_data(
        self, start_pos_dict: dict
    ) -> BeatData:
        """Convert legacy start position JSON back to modern BeatData with full data"""
        from domain.models import (
            BeatData,
            GlyphData,
            Location,
            MotionData,
            MotionType,
            RotationDirection,
        )

        letter = start_pos_dict.get("letter", "α")
        sequence_start_position = start_pos_dict.get("sequence_start_position", "alpha")
        end_pos = start_pos_dict.get("end_pos", "alpha1")

        # Create glyph data with position information
        glyph_data = GlyphData(
            start_position=sequence_start_position,
            end_position=end_pos,
        )

        # Convert blue attributes to MotionData (start positions usually static)
        blue_motion = None
        blue_attrs = start_pos_dict.get("blue_attributes", {})
        if blue_attrs:
            try:
                blue_motion = MotionData(
                    motion_type=MotionType(blue_attrs.get("motion_type", "static")),
                    prop_rot_dir=RotationDirection(
                        blue_attrs.get("prop_rot_dir", "no_rot")
                    ),
                    start_loc=Location(blue_attrs.get("start_loc", "s")),
                    end_loc=Location(blue_attrs.get("end_loc", "s")),
                    turns=float(blue_attrs.get("turns", 0)),
                    start_ori=blue_attrs.get("start_ori", "in"),
                    end_ori=blue_attrs.get("end_ori", "in"),
                )
            except Exception as e:
                logger.warning(
                    f"Failed to create blue motion data for start position: {e}"
                )
                blue_motion = MotionData(
                    motion_type=MotionType.STATIC,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.SOUTH,
                    end_loc=Location.SOUTH,
                )

        # Convert red attributes to MotionData
        red_motion = None
        red_attrs = start_pos_dict.get("red_attributes", {})
        if red_attrs:
            try:
                red_motion = MotionData(
                    motion_type=MotionType(red_attrs.get("motion_type", "static")),
                    prop_rot_dir=RotationDirection(
                        red_attrs.get("prop_rot_dir", "no_rot")
                    ),
                    start_loc=Location(red_attrs.get("start_loc", "s")),
                    end_loc=Location(red_attrs.get("end_loc", "s")),
                    turns=float(red_attrs.get("turns", 0)),
                    start_ori=red_attrs.get("start_ori", "in"),
                    end_ori=red_attrs.get("end_ori", "in"),
                )
            except Exception as e:
                logger.warning(
                    f"Failed to create red motion data for start position: {e}"
                )
                red_motion = MotionData(
                    motion_type=MotionType.STATIC,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.SOUTH,
                    end_loc=Location.SOUTH,
                )

        # Create BeatData for start position
        start_position_beat = BeatData(
            beat_number=0,  # Start position is beat 0
            letter=letter,
            duration=1.0,
            blue_motion=blue_motion,
            red_motion=red_motion,
            glyph_data=glyph_data,
            metadata={
                "is_start_position": True,
                "sequence_start_position": sequence_start_position,
                "timing": start_pos_dict.get("timing", "none"),
                "direction": start_pos_dict.get("direction", "none"),
            },
        )

        return start_position_beat

    def _convert_beat_data_to_legacy_format(
        self, beat: BeatData, beat_number: int
    ) -> dict:
        """Convert modern BeatData to legacy JSON format exactly like legacy pictograph_data"""
        # Extract position data from glyph_data if available
        start_pos = ""
        end_pos = ""
        if beat.glyph_data:
            start_pos = beat.glyph_data.start_position or ""
            end_pos = beat.glyph_data.end_position or ""

        # Extract motion data from blue_motion and red_motion
        blue_attrs = {
            "motion_type": "static",
            "start_ori": "in",
            "end_ori": "in",
            "prop_rot_dir": "no_rot",
            "start_loc": "s",
            "end_loc": "s",
            "turns": 0,
        }

        red_attrs = {
            "motion_type": "static",
            "start_ori": "in",
            "end_ori": "in",
            "prop_rot_dir": "no_rot",
            "start_loc": "s",
            "end_loc": "s",
            "turns": 0,
        }

        # Extract blue motion data if available
        if beat.blue_motion:
            blue_attrs.update(
                {
                    "motion_type": beat.blue_motion.motion_type.value,
                    "start_ori": beat.blue_motion.start_ori,
                    "end_ori": beat.blue_motion.end_ori,
                    "prop_rot_dir": beat.blue_motion.prop_rot_dir.value,
                    "start_loc": beat.blue_motion.start_loc.value,
                    "end_loc": beat.blue_motion.end_loc.value,
                    "turns": int(beat.blue_motion.turns),
                }
            )

        # Extract red motion data if available
        if beat.red_motion:
            red_attrs.update(
                {
                    "motion_type": beat.red_motion.motion_type.value,
                    "start_ori": beat.red_motion.start_ori,
                    "end_ori": beat.red_motion.end_ori,
                    "prop_rot_dir": beat.red_motion.prop_rot_dir.value,
                    "start_loc": beat.red_motion.start_loc.value,
                    "end_loc": beat.red_motion.end_loc.value,
                    "turns": int(beat.red_motion.turns),
                }
            )

        # Determine timing and direction from motion data
        timing = "tog"  # Default
        direction = "same"  # Default

        # If we have motion data, try to determine timing/direction
        if beat.blue_motion and beat.red_motion:
            # Check if blue and red are moving in same direction
            if (
                beat.blue_motion.motion_type == beat.red_motion.motion_type
                and beat.blue_motion.prop_rot_dir == beat.red_motion.prop_rot_dir
            ):
                direction = "same"
            else:
                direction = "opp"

            # For now, default to "tog" timing - this could be enhanced later
            timing = "tog"

        return {
            "beat": beat_number,
            "letter": beat.letter or "?",
            "letter_type": "Type1",  # Default for now - could extract from glyph_data.letter_type
            "duration": int(beat.duration),
            "start_pos": start_pos,
            "end_pos": end_pos,
            "timing": timing,
            "direction": direction,
            "blue_attributes": blue_attrs,
            "red_attributes": red_attrs,
        }

    def _convert_start_position_to_legacy_format(
        self, start_position_data: BeatData
    ) -> dict:
        """Convert start position BeatData to legacy format exactly like JsonStartPositionHandler"""
        # Extract start position type (alpha, beta, gamma) from glyph_data if available
        end_pos = "alpha1"  # Default
        sequence_start_position = "alpha"  # Default

        if (
            start_position_data.glyph_data
            and start_position_data.glyph_data.end_position
        ):
            end_pos = start_position_data.glyph_data.end_position
            if end_pos.startswith("alpha"):
                sequence_start_position = "alpha"
            elif end_pos.startswith("beta"):
                sequence_start_position = "beta"
            elif end_pos.startswith("gamma"):
                sequence_start_position = "gamma"
            else:
                sequence_start_position = end_pos.rstrip("0123456789")

        # Extract motion data for start position (usually static)
        blue_attrs = {
            "start_loc": "s",
            "end_loc": "s",
            "start_ori": "in",
            "end_ori": "in",
            "prop_rot_dir": "no_rot",
            "turns": 0,
            "motion_type": "static",
        }

        red_attrs = {
            "start_loc": "s",
            "end_loc": "s",
            "start_ori": "in",
            "end_ori": "in",
            "prop_rot_dir": "no_rot",
            "turns": 0,
            "motion_type": "static",
        }

        # Extract blue motion data if available (though start positions are usually static)
        if start_position_data.blue_motion:
            blue_attrs.update(
                {
                    "start_loc": start_position_data.blue_motion.start_loc.value,
                    "end_loc": start_position_data.blue_motion.end_loc.value,
                    "start_ori": start_position_data.blue_motion.start_ori,
                    "end_ori": start_position_data.blue_motion.end_ori,
                    "prop_rot_dir": start_position_data.blue_motion.prop_rot_dir.value,
                    "turns": int(start_position_data.blue_motion.turns),
                    "motion_type": start_position_data.blue_motion.motion_type.value,
                }
            )

        # Extract red motion data if available
        if start_position_data.red_motion:
            red_attrs.update(
                {
                    "start_loc": start_position_data.red_motion.start_loc.value,
                    "end_loc": start_position_data.red_motion.end_loc.value,
                    "start_ori": start_position_data.red_motion.start_ori,
                    "end_ori": start_position_data.red_motion.end_ori,
                    "prop_rot_dir": start_position_data.red_motion.prop_rot_dir.value,
                    "turns": int(start_position_data.red_motion.turns),
                    "motion_type": start_position_data.red_motion.motion_type.value,
                }
            )

        return {
            "beat": 0,
            "sequence_start_position": sequence_start_position,
            "letter": start_position_data.letter or "α",
            "end_pos": end_pos,
            "timing": "none",
            "direction": "none",
            "blue_attributes": blue_attrs,
            "red_attributes": red_attrs,
        }
