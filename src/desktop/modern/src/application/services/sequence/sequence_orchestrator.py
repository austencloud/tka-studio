"""
Sequence Orchestrator - Core Business Operations and Coordination

Orchestrates all sequence-related business operations by coordinating multiple
services and operations. This service consolidates functionality from:
- SequenceManager (core business operations)
- SequenceBeatOperations (beat-level operations)
- SequenceLoader (loading from persistence)
- SequenceStartPositionManager (start position handling)

ARCHITECTURE:
Application Layer → SequenceOrchestrator → [SequencePersister, Transformer, Validator]
Presentation Layer → SequenceOrchestratorQtAdapter → SequenceOrchestrator
"""

import logging
from typing import Callable, List, Optional

from application.services.option_picker.option_orientation_updater import (
    OptionOrientationUpdater,
)
from application.services.sequence.sequence_persister import SequencePersister
from application.services.sequence.sequence_transformer import SequenceTransformer
from application.services.sequence.sequence_validator import SequenceValidator
from domain.models.beat_data import BeatData
from domain.models.pictograph_data import PictographData
from domain.models.sequence_data import SequenceData

logger = logging.getLogger(__name__)


class ISequenceOrchestratorSignals:
    """Interface for sequence orchestrator signal emission."""

    def emit_sequence_modified(self, sequence: SequenceData) -> None:
        """Emit signal when sequence is modified."""
        pass

    def emit_sequence_cleared(self) -> None:
        """Emit signal when sequence is cleared."""
        pass

    def emit_beat_added(self, beat_data: BeatData, position: int) -> None:
        """Emit signal when beat is added."""
        pass

    def emit_beat_removed(self, position: int) -> None:
        """Emit signal when beat is removed."""
        pass

    def emit_beat_updated(self, beat_data: BeatData, position: int) -> None:
        """Emit signal when beat is updated."""
        pass

    def emit_start_position_set(self, start_position_data: BeatData) -> None:
        """Emit signal when start position is set."""
        pass

    def emit_sequence_loaded(self, sequence: SequenceData) -> None:
        """Emit signal when sequence is loaded."""
        pass


class SequenceOrchestrator:
    """
    Core business service for orchestrating sequence operations.

    This service coordinates all sequence-related operations including:
    - Beat management (add, remove, update)
    - Start position handling
    - Sequence loading and persistence
    - Workbench coordination
    - Signal emission coordination

    Signal emission is abstracted through the ISequenceOrchestratorSignals interface
    to maintain separation from Qt/UI frameworks.
    """

    def __init__(
        self,
        workbench_getter: Optional[Callable[[], object]] = None,
        workbench_setter: Optional[Callable[[SequenceData], None]] = None,
        data_converter: Optional[object] = None,
        signal_emitter: Optional[ISequenceOrchestratorSignals] = None,
    ):
        """
        Initialize the sequence orchestrator.

        Args:
            workbench_getter: Function to get current workbench
            workbench_setter: Function to set workbench sequence
            data_converter: Converter for legacy data format compatibility
            signal_emitter: Optional signal emitter for notifications
        """
        self.workbench_getter = workbench_getter
        self.workbench_setter = workbench_setter
        self.data_converter = data_converter
        self._signal_emitter = signal_emitter
        self._emitting_signal = False

        # Initialize dependent services
        self.persistence_service = SequencePersister()
        self.orientation_update_service = OptionOrientationUpdater()
        self.transformer = SequenceTransformer()
        self.validator = SequenceValidator()

        logger.info("SequenceOrchestrator initialized with all dependent services")

    # =============================================================================
    # BEAT OPERATIONS (Consolidated from SequenceBeatOperations)
    # =============================================================================

    def add_pictograph_to_sequence(self, pictograph_data: PictographData):
        """Add pictograph to sequence by converting to beat data first."""
        try:
            logger.debug(f"Adding pictograph {pictograph_data.letter} to sequence")

            # Convert PictographData to BeatData
            beat_data = self._convert_pictograph_to_beat_data(pictograph_data)

            # Use existing beat addition logic
            self.add_beat_to_sequence(beat_data)

            logger.info(
                f"Successfully added pictograph {pictograph_data.letter} to sequence"
            )

        except Exception as e:
            logger.error(f"Error adding pictograph to sequence: {e}")
            raise

    def add_beat_to_sequence(self, beat_data: BeatData):
        """Add a beat to the current sequence"""
        current_sequence = self._get_current_sequence()
        if current_sequence is None:
            current_sequence = SequenceData.empty()

        try:
            logger.debug(f"Adding beat {beat_data.letter} to sequence")

            # Validate the beat before adding
            self.validator.validate_beat(beat_data)

            # Update orientations if there are existing beats
            if current_sequence.length > 0:
                updated_beats = (
                    self.orientation_update_service.update_option_orientations(
                        current_sequence, [beat_data]
                    )
                )
                beat_data = updated_beats[0]

            # Create new beat with proper numbering
            new_beat = beat_data.update(
                beat_number=current_sequence.length + 1,
                duration=1.0,
            )

            # Add to sequence
            updated_beats = current_sequence.beats + [new_beat]
            updated_sequence = current_sequence.update(beats=updated_beats)

            # Validate the updated sequence
            self.validator.validate_sequence(updated_sequence)

            # Save to persistence
            self._save_sequence_to_persistence(updated_sequence)

            # Update workbench
            if self.workbench_setter:
                self.workbench_setter(updated_sequence)
            else:
                self._emit_sequence_modified(updated_sequence)

            # Emit beat added signal
            if self._signal_emitter:
                position = len(updated_sequence.beats) - 1
                self._signal_emitter.emit_beat_added(new_beat, position)

            logger.info(f"Successfully added beat {beat_data.letter} to sequence")

        except Exception as e:
            logger.error(f"Error adding beat to sequence: {e}")
            raise

    def remove_beat(self, beat_index: int):
        """Remove a beat from the sequence"""
        try:
            current_sequence = self._get_current_sequence()
            if not current_sequence or beat_index >= len(current_sequence.beats):
                logger.warning(
                    f"Cannot remove beat at index {beat_index}: invalid index or empty sequence"
                )
                return

            logger.debug(f"Removing beat at index {beat_index}")

            # Get the beat to remove for logging
            beat_to_remove = current_sequence.beats[beat_index]

            # Remove the beat
            updated_beats = list(current_sequence.beats)
            updated_beats.pop(beat_index)

            # Renumber remaining beats
            for i, beat in enumerate(updated_beats):
                updated_beats[i] = beat.update(beat_number=i + 1)

            updated_sequence = current_sequence.update(beats=updated_beats)

            # Validate the updated sequence
            self.validator.validate_sequence(updated_sequence)

            # Save to persistence and update workbench
            self._save_sequence_to_persistence(updated_sequence)

            if self.workbench_setter:
                self.workbench_setter(updated_sequence)

            # Emit beat removed signal
            if self._signal_emitter:
                self._signal_emitter.emit_beat_removed(beat_index)

            logger.info(
                f"Successfully removed beat {beat_to_remove.letter} from position {beat_index}"
            )

        except Exception as e:
            logger.error(f"Failed to remove beat: {e}")
            raise

    def update_beat_turns(self, beat_index: int, color: str, new_turns: int):
        """Update the number of turns for a specific beat"""
        try:
            current_sequence = self._get_current_sequence()
            if not current_sequence or beat_index >= len(current_sequence.beats):
                logger.warning(
                    f"Cannot update beat turns at index {beat_index}: invalid index or empty sequence"
                )
                return

            logger.debug(f"Updating {color} turns for beat {beat_index} to {new_turns}")

            # Update the beat in memory
            updated_beats = list(current_sequence.beats)
            beat = updated_beats[beat_index]

            # Update the turn count for the specified color
            if color.lower() == "blue" and beat.blue_motion:
                updated_motion = beat.blue_motion.update(turns=new_turns)
                updated_beat = beat.update(blue_motion=updated_motion)
            elif color.lower() == "red" and beat.red_motion:
                updated_motion = beat.red_motion.update(turns=new_turns)
                updated_beat = beat.update(red_motion=updated_motion)
            else:
                logger.warning(f"Invalid color '{color}' or missing motion data")
                return

            updated_beats[beat_index] = updated_beat
            updated_sequence = current_sequence.update(beats=updated_beats)

            # Validate the updated sequence
            self.validator.validate_sequence(updated_sequence)

            # Save to persistence and update workbench
            self._save_sequence_to_persistence(updated_sequence)

            if self.workbench_setter:
                self.workbench_setter(updated_sequence)

            # Emit beat updated signal
            if self._signal_emitter:
                self._signal_emitter.emit_beat_updated(updated_beat, beat_index)

            logger.info(f"Updated {color} turns for beat {beat.letter} to {new_turns}")

        except Exception as e:
            logger.error(f"Failed to update beat turns: {e}")
            raise

    def update_beat_orientation(
        self, beat_index: int, color: str, new_orientation: int
    ):
        """Update the orientation for a specific beat"""
        try:
            current_sequence = self._get_current_sequence()
            if not current_sequence or beat_index >= len(current_sequence.beats):
                logger.warning(
                    f"Cannot update beat orientation at index {beat_index}: invalid index or empty sequence"
                )
                return

            logger.debug(
                f"Updating {color} orientation for beat {beat_index} to {new_orientation}"
            )

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
                logger.warning(f"Invalid color '{color}' or missing motion data")
                return

            # Update sequence
            new_beats = current_sequence.beats.copy()
            new_beats[beat_index] = updated_beat
            new_sequence = current_sequence.update(beats=new_beats)

            # Validate and save
            self.validator.validate_sequence(new_sequence)
            self._save_sequence_to_persistence(new_sequence)

            if self.workbench_setter:
                self.workbench_setter(new_sequence)

            # Emit signal
            if self._signal_emitter:
                self._signal_emitter.emit_beat_updated(updated_beat, beat_index)

            logger.info(
                f"Updated {color} orientation for beat {beat.letter} to {new_orientation}"
            )

        except Exception as e:
            logger.error(f"Failed to update beat orientation: {e}")
            raise

    # =============================================================================
    # START POSITION OPERATIONS (Consolidated from SequenceStartPositionManager)
    # =============================================================================

    def set_start_position(self, start_position_data):
        """Set the start position - accepts both PictographData and BeatData"""
        try:
            logger.debug(f"Setting start position")

            # Convert PictographData to BeatData if needed
            if isinstance(start_position_data, PictographData):
                logger.debug("Converting PictographData to BeatData for start position")
                beat_data = self._convert_pictograph_to_start_position_beat_data(
                    start_position_data
                )
            else:
                beat_data = start_position_data

            # Validate start position data
            self.validator.validate_beat(beat_data)

            if not self.data_converter:
                logger.error("No data converter available for start position")
                raise ValueError(
                    "Data converter required for start position operations"
                )

            # Convert start position to legacy format and save as beat 0
            start_pos_dict = (
                self.data_converter.convert_start_position_to_legacy_format(beat_data)
            )

            # Load current sequence to preserve existing beats
            sequence = self.persistence_service.load_current_sequence()

            # Find where to insert/replace start position
            if len(sequence) == 1:  # Only metadata
                sequence.append(start_pos_dict)
                logger.debug("Inserted start position as beat 0")
            elif len(sequence) > 1 and sequence[1].get("beat") == 0:
                # Replace existing start position
                sequence[1] = start_pos_dict
                logger.debug("Replaced existing start position")
            else:
                # Insert start position, shifting existing beats
                sequence.insert(1, start_pos_dict)
                logger.debug(
                    f"Inserted start position, preserving {len(sequence) - 2} existing beats"
                )

            # Save updated sequence
            self.persistence_service.save_current_sequence(sequence)

            # Set start position in workbench
            workbench = self.workbench_getter() if self.workbench_getter else None
            if workbench and hasattr(workbench, "set_start_position"):
                workbench.set_start_position(beat_data)
                logger.debug(f"Start position set in workbench: {beat_data.letter}")

            # Emit signal
            if self._signal_emitter:
                self._signal_emitter.emit_start_position_set(beat_data)

            logger.info(f"Successfully set start position: {beat_data.letter}")

        except Exception as e:
            logger.error(f"Failed to set start position: {e}")
            raise

    def get_current_start_position(self) -> Optional[BeatData]:
        """Get the current start position from workbench"""
        try:
            workbench = self.workbench_getter()
            if workbench and hasattr(workbench, "_start_position_data"):
                return workbench._start_position_data
        except Exception as e:
            logger.error(f"Error getting current start position: {e}")
        return None

    def clear_start_position(self):
        """Clear the current start position"""
        try:
            logger.debug("Clearing start position")

            # Clear from workbench
            workbench = self.workbench_getter()
            if workbench and hasattr(workbench, "_start_position_data"):
                workbench._start_position_data = None
                logger.debug("Cleared start position from workbench")

                # Clear from beat frame if available
                if hasattr(workbench, "_beat_frame_section"):
                    beat_frame_section = workbench._beat_frame_section
                    if beat_frame_section and hasattr(
                        beat_frame_section, "initialize_cleared_start_position"
                    ):
                        beat_frame_section.initialize_cleared_start_position()
                        logger.debug("Cleared start position from beat frame")

            # Clear from persistence
            sequence = self.persistence_service.load_current_sequence()
            if len(sequence) > 1 and sequence[1].get("beat") == 0:
                sequence.pop(1)
                self.persistence_service.save_current_sequence(sequence)
                logger.debug("Cleared start position from persistence")

            logger.info("Start position cleared successfully")

        except Exception as e:
            logger.error(f"Failed to clear start position: {e}")
            raise

    # =============================================================================
    # SEQUENCE LOADING (Consolidated from SequenceLoader)
    # =============================================================================

    def load_sequence_on_startup(self):
        """Load sequence from current_sequence.json on startup"""
        try:
            logger.info("Loading sequence on startup")

            # Load sequence from persistence
            sequence_data = self.persistence_service.load_current_sequence()

            if len(sequence_data) <= 1:
                logger.info("No sequence to load on startup")
                return

            logger.debug(f"Loading sequence with {len(sequence_data)} items")

            # Extract metadata and beats
            metadata = sequence_data[0]
            sequence_word = metadata.get("word", "")
            logger.debug(f"Sequence word: '{sequence_word}'")

            # Find start position (beat 0) and actual beats (beat 1+)
            start_position_data = None
            beats_data = []

            for item in sequence_data[1:]:
                if item.get("beat") == 0:
                    start_position_data = item
                    logger.debug(
                        f"Found start position: {item.get('sequence_start_position', 'unknown')}"
                    )
                elif "letter" in item and not item.get("is_placeholder", False):
                    beats_data.append(item)
                    logger.debug(
                        f"Found beat {item.get('beat', '?')}: {item.get('letter', '?')}"
                    )

            # Convert beats to modern format with full pictograph data
            beat_objects = []
            if self.data_converter:
                for i, beat_dict in enumerate(beats_data):
                    try:
                        beat_obj = self.data_converter.convert_legacy_to_beat_data(
                            beat_dict, i + 1
                        )
                        beat_objects.append(beat_obj)
                        logger.debug(
                            f"Converted beat {beat_obj.letter} with motion data"
                        )
                    except Exception as e:
                        logger.warning(
                            f"Failed to convert beat {beat_dict.get('letter', '?')}: {e}"
                        )
                        # Create fallback beat
                        fallback_beat = BeatData(
                            beat_number=i + 1,
                            letter=beat_dict.get("letter", "?"),
                            duration=beat_dict.get("duration", 1.0),
                        )
                        beat_objects.append(fallback_beat)

            # Handle start position loading
            if start_position_data and self.data_converter:
                try:
                    start_position_beat = (
                        self.data_converter.convert_legacy_start_position_to_beat_data(
                            start_position_data
                        )
                    )

                    # Set start position in workbench
                    workbench = (
                        self.workbench_getter() if self.workbench_getter else None
                    )
                    if workbench and hasattr(workbench, "set_start_position"):
                        workbench.set_start_position(start_position_beat)
                        logger.debug(f"Start position loaded into workbench")

                except Exception as e:
                    logger.error(f"Failed to load start position: {e}")

            # Create and set the sequence
            loaded_sequence = SequenceData(
                id="loaded_sequence",
                name=sequence_word or "Loaded Sequence",
                beats=beat_objects,
            )

            # Validate the loaded sequence
            if beat_objects:  # Only validate if there are beats
                self.validator.validate_sequence(loaded_sequence)

            logger.debug(
                f"Created sequence: '{loaded_sequence.name}' with {len(beat_objects)} beats"
            )

            # Set sequence in workbench
            if self.workbench_setter:
                self.workbench_setter(loaded_sequence)
                logger.debug("Sequence loaded into workbench")

            # Emit sequence loaded signal
            if self._signal_emitter:
                self._signal_emitter.emit_sequence_loaded(loaded_sequence)

            logger.info(
                f"Successfully loaded sequence '{loaded_sequence.name}' with {len(beat_objects)} beats"
            )

        except Exception as e:
            logger.error(f"Failed to load sequence on startup: {e}")
            raise

    # =============================================================================
    # SEQUENCE MANAGEMENT OPERATIONS
    # =============================================================================

    def clear_sequence(self):
        """Clear the current sequence"""
        try:
            logger.debug("Clearing current sequence")

            # Clear current_sequence.json file
            self.persistence_service.clear_all_beats()

            # Update workbench
            if self.workbench_setter:
                self.workbench_setter(SequenceData.empty())

            # Emit signal
            if self._signal_emitter:
                self._signal_emitter.emit_sequence_cleared()

            logger.info("Sequence cleared successfully")

        except Exception as e:
            logger.error(f"Failed to clear sequence: {e}")
            raise

    def handle_workbench_modified(self, sequence: SequenceData):
        """Handle workbench sequence modification with circular emission protection"""
        if self._emitting_signal:
            return

        try:
            self._emitting_signal = True

            # Validate the modified sequence
            self.validator.validate_sequence(sequence)

            # Update persistence
            self._save_sequence_to_persistence(sequence)

            # Emit signal
            if self._signal_emitter:
                self._signal_emitter.emit_sequence_modified(sequence)

            logger.debug("Workbench modification handled successfully")

        except Exception as e:
            logger.error(f"Signal emission failed: {e}")
            raise
        finally:
            self._emitting_signal = False

    def get_current_sequence_length(self) -> int:
        """Get the length of the current sequence"""
        current_sequence = self._get_current_sequence()
        return current_sequence.length if current_sequence else 0

    # =============================================================================
    # WORKBENCH TRANSFORMATIONS
    # =============================================================================

    def apply_workbench_transformation(
        self, operation: str, **kwargs
    ) -> Optional[SequenceData]:
        """Apply workbench transformation to current sequence"""
        try:
            current_sequence = self._get_current_sequence()
            if not current_sequence:
                logger.warning("No current sequence to transform")
                return None

            logger.debug(f"Applying transformation: {operation}")

            # Apply transformation using the transformer service
            transformed_sequence = self.transformer.apply_workbench_operation(
                current_sequence, operation, **kwargs
            )

            # Validate the transformed sequence
            self.validator.validate_sequence(transformed_sequence)

            # Save and update workbench
            self._save_sequence_to_persistence(transformed_sequence)

            if self.workbench_setter:
                self.workbench_setter(transformed_sequence)

            logger.info(f"Successfully applied transformation: {operation}")
            return transformed_sequence

        except Exception as e:
            logger.error(f"Failed to apply transformation {operation}: {e}")
            raise

    # =============================================================================
    # PRIVATE HELPER METHODS
    # =============================================================================

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
        if not self.data_converter:
            logger.warning("No data converter available for persistence")
            return

        try:
            # Load existing sequence to preserve start position
            existing_sequence = self.persistence_service.load_current_sequence()

            # Calculate word from beat letters
            word = self._calculate_sequence_word(sequence)

            # Update metadata
            metadata = (
                existing_sequence[0]
                if existing_sequence
                else self.persistence_service.get_default_sequence()[0]
            )
            metadata["word"] = word

            # Check for existing start position
            existing_start_position = None
            if len(existing_sequence) > 1 and existing_sequence[1].get("beat") == 0:
                existing_start_position = existing_sequence[1]

            # Convert beats to legacy format
            legacy_beats = []
            for i, beat in enumerate(sequence.beats):
                beat_dict = self.data_converter.convert_beat_data_to_legacy_format(
                    beat, i + 1
                )
                legacy_beats.append(beat_dict)

            # Build final sequence
            final_sequence = [metadata]
            if existing_start_position:
                final_sequence.append(existing_start_position)
            final_sequence.extend(legacy_beats)

            # Save the complete sequence
            self.persistence_service.save_current_sequence(final_sequence)
            logger.debug(
                f"Saved sequence to persistence: {len(final_sequence)} items (word: '{word}')"
            )

        except Exception as e:
            logger.error(f"Failed to save sequence to persistence: {e}")
            raise

    def _calculate_sequence_word(self, sequence: SequenceData) -> str:
        """Calculate sequence word from beat letters"""
        if not sequence.beats:
            return ""

        word = "".join(beat.letter for beat in sequence.beats)
        return self._simplify_repeated_word(word)

    def _simplify_repeated_word(self, word: str) -> str:
        """Simplify repeated patterns in sequence words"""

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

    def _convert_pictograph_to_beat_data(
        self, pictograph_data: PictographData
    ) -> BeatData:
        """Convert PictographData to BeatData for sequence operations"""
        try:
            # Extract motion data from arrows
            blue_motion = None
            red_motion = None

            if hasattr(pictograph_data, "arrows") and pictograph_data.arrows:
                if "blue" in pictograph_data.arrows:
                    blue_motion = pictograph_data.motions["blue"]
                if "red" in pictograph_data.arrows:
                    red_motion = pictograph_data.motions["red"]

            # Get current sequence to determine beat number
            current_sequence = self._get_current_sequence()
            beat_number = 1

            if current_sequence and current_sequence.beats:
                # Check if first beat is a start position
                has_start_position = (
                    current_sequence.beats[0].metadata.get("is_start_position", False)
                    and current_sequence.beats[0].beat_number == 0
                )

                if has_start_position:
                    beat_number = len(current_sequence.beats)  # Exclude start position
                else:
                    beat_number = len(current_sequence.beats) + 1

            # Create metadata for regular beat
            beat_metadata = {
                "start_position": pictograph_data.start_position,
                "end_position": pictograph_data.end_position,
                "converted_from_pictograph": True,
            }

            if pictograph_data.metadata:
                for key, value in pictograph_data.metadata.items():
                    if key not in ["is_start_position"]:
                        beat_metadata[key] = value

            # Create BeatData
            beat_data = BeatData(
                beat_number=beat_number,
                letter=pictograph_data.letter or "?",
                pictograph_data=pictograph_data,  # NEW: Use pictograph data with motions
                glyph_data=pictograph_data.glyph_data,
                is_blank=pictograph_data.is_blank,
                metadata=beat_metadata,
            )

            return beat_data

        except Exception as e:
            logger.error(f"Error converting pictograph to beat data: {e}")
            # Return minimal beat data as fallback
            return BeatData(
                beat_number=1,
                letter="?",
                is_blank=True,
                metadata={"conversion_error": str(e)},
            )

    def _convert_pictograph_to_start_position_beat_data(
        self, pictograph_data: PictographData
    ) -> BeatData:
        """Convert PictographData to BeatData for start position operations"""
        try:
            # Extract motion data from arrows
            blue_motion = None
            red_motion = None

            if pictograph_data.arrows:
                if "blue" in pictograph_data.arrows:
                    arrow = pictograph_data.arrows["blue"]
                    from domain.models.enums import (
                        Location,
                        MotionType,
                        Orientation,
                        RotationDirection,
                    )
                    from domain.models.motion_models import MotionData

                    blue_motion = MotionData(
                        motion_type=getattr(arrow, "motion_type", MotionType.STATIC),
                        prop_rot_dir=RotationDirection.CLOCKWISE,
                        start_loc=getattr(arrow, "location", Location.NORTH),
                        start_ori=getattr(arrow, "orientation", Orientation.IN),
                        end_loc=getattr(arrow, "location", Location.NORTH),
                        end_ori=getattr(arrow, "orientation", Orientation.IN),
                        turns=0.0,
                    )

                if "red" in pictograph_data.arrows:
                    arrow = pictograph_data.arrows["red"]
                    from domain.models.enums import (
                        Location,
                        MotionType,
                        Orientation,
                        RotationDirection,
                    )
                    from domain.models.motion_models import MotionData

                    red_motion = MotionData(
                        motion_type=getattr(arrow, "motion_type", MotionType.STATIC),
                        prop_rot_dir=RotationDirection.CLOCKWISE,
                        start_loc=getattr(arrow, "location", Location.NORTH),
                        start_ori=getattr(arrow, "orientation", Orientation.IN),
                        end_loc=getattr(arrow, "location", Location.NORTH),
                        end_ori=getattr(arrow, "orientation", Orientation.IN),
                        turns=0.0,
                    )

            # Create glyph data for start position
            from domain.models.glyph_models import GlyphData

            glyph_data = GlyphData(
                start_position=pictograph_data.start_position,
                end_position=pictograph_data.end_position,
                show_tka=True,
                show_positions=True,
                show_vtg=True,
                show_elemental=True,
            )

            # Ensure metadata includes start position flag
            metadata = pictograph_data.metadata or {}
            metadata["is_start_position"] = True

            return BeatData(
                letter=pictograph_data.letter,
                beat_number=0,  # Start position is beat 0
                duration=1.0,
                pictograph_data=pictograph_data,  # NEW: Use pictograph data with motions
                glyph_data=glyph_data,
                is_blank=pictograph_data.is_blank,
                metadata=metadata,
            )

        except Exception as e:
            logger.error(
                f"Error converting pictograph to start position beat data: {e}"
            )
            raise
