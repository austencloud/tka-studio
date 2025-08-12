"""
Sequence Option Service - Pure Business Logic

Handles sequence state analysis and option generation without Qt dependencies.
Extracted from option_picker_scroll.py to maintain clean architecture.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)

from desktop.modern.core.interfaces.sequence_operation_services import (
    ISequenceOptionService,
)
from desktop.modern.domain.models.enums import (
    Location,
    MotionType,
    Orientation,
    RotationDirection,
)
from desktop.modern.domain.models.letter_type_classifier import LetterTypeClassifier
from desktop.modern.domain.models.motion_data import MotionData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.components.option_picker.types.letter_types import (
    LetterType,
)
from shared.application.services.option_picker.option_orientation_updater import (
    OptionOrientationUpdater,
)
from shared.application.services.positioning.arrows.calculation.orientation_calculator import (
    OrientationCalculator,
)
from shared.application.services.positioning.arrows.utilities.pictograph_position_matcher import (
    PictographPositionMatcher,
)
from shared.application.services.sequence.sequence_orientation_validator import (
    SequenceOrientationValidator,
)


class SequenceOptionService(ISequenceOptionService):
    """
    Pure service for generating options based on sequence state.

    No Qt dependencies - returns domain data only.
    """

    def __init__(self, position_matcher: PictographPositionMatcher):
        """Initialize with position matcher dependency."""
        self._position_matcher = position_matcher
        self._orientation_updater = OptionOrientationUpdater()
        self._orientation_calculator = OrientationCalculator()
        self._sequence_orientation_validator = SequenceOrientationValidator()

    def get_options_for_sequence(
        self, sequence_data: SequenceData | list[dict]
    ) -> dict[LetterType, list[PictographData]]:
        """
        Get options organized by letter type for given sequence state.

        Handles both modern SequenceData and legacy list format.

        Returns pure domain data - no Qt objects.
        """
        try:
            # Extract end position from sequence
            end_position = self._extract_end_position(sequence_data)

            if not end_position:
                print(
                    "❌ [SEQUENCE_OPTION] Could not extract end position from sequence"
                )
                return {}

            # Get all valid next options
            all_options = self._position_matcher.get_next_options(end_position)

            # FIXED: Use the new sequence orientation validator for proper orientation handling
            # More robust check for SequenceData - handle module path inconsistencies
            is_sequence_data = isinstance(sequence_data, SequenceData) or (
                hasattr(sequence_data, "__class__")
                and sequence_data.__class__.__name__ == "SequenceData"
                and hasattr(sequence_data, "beats")
                and hasattr(sequence_data, "length")
            )

            # DEBUG: Check sequence data type detection
            print(f"🔍 [SEQUENCE_OPTION] Sequence data type: {type(sequence_data)}")
            print(
                f"🔍 [SEQUENCE_OPTION] Sequence data class name: {sequence_data.__class__.__name__}"
            )
            print(f"🔍 [SEQUENCE_OPTION] Is SequenceData: {is_sequence_data}")
            print(f"🔍 [SEQUENCE_OPTION] Has beats: {hasattr(sequence_data, 'beats')}")
            if hasattr(sequence_data, "beats"):
                print(
                    f"🔍 [SEQUENCE_OPTION] Number of beats: {len(sequence_data.beats)}"
                )

            if is_sequence_data:
                print(
                    f"✅ [SEQUENCE_OPTION] Using modern SequenceData with {len(sequence_data.beats)} beats"
                )
                logger.debug(
                    f"Using modern SequenceData with {len(sequence_data.beats)} beats"
                )

                # Use modern sequence orientation validator for accurate orientation continuity
                updated_options = self._sequence_orientation_validator.calculate_option_start_orientations(
                    sequence_data, all_options
                )
                logger.debug(
                    f"Orientation validator returned {len(updated_options)} options"
                )

            else:
                # Fallback for legacy format - use old method
                end_orientations = self._extract_end_orientations(sequence_data)
                updated_options = self._update_option_orientations(
                    all_options, end_orientations
                )
                print("Using legacy format - orientation handling may be less accurate")

            # Group by letter type
            grouped_options = self._group_options_by_type(updated_options)
            total_grouped = sum(len(options) for options in grouped_options.values())

            # DEBUG: Check if orientations are preserved after grouping
            if grouped_options:
                for letter_type, options_list in grouped_options.items():
                    if options_list:
                        first_option = options_list[0]
                        blue_motion = first_option.motions.get("blue")
                        red_motion = first_option.motions.get("red")
                        logger.debug(
                            f"After grouping - {letter_type} first option ({first_option.letter}): Blue={blue_motion.start_ori if blue_motion else 'None'}, Red={red_motion.start_ori if red_motion else 'None'}"
                        )
                        break  # Only check first group

            return grouped_options

        except Exception as e:
            print(f"❌ [SEQUENCE_OPTION] Error getting options for sequence: {e}")
            import traceback

            traceback.print_exc()
            return {}

    def _extract_end_position(self, sequence_data: SequenceData) -> str:
        """
        Extract end position from sequence data.

        Handles both modern SequenceData and legacy list format.

        Pure data extraction logic - no Qt dependencies.
        """
        try:
            # If sequence has no data, use alpha1
            if not sequence_data:
                raise ValueError("Sequence data is empty")

            # Handle modern SequenceData format
            if hasattr(sequence_data, "length") and sequence_data.length == 0:
                return "alpha1"

            if (
                not hasattr(sequence_data, "beats")
                or not sequence_data.beats
                or len(sequence_data.beats) == 0
            ):
                return "alpha1"

            # Get the last beat from the beats list
            last_beat = sequence_data.beats[-1]

            # BeatData objects have pictograph_data with end_pos
            if hasattr(last_beat, "pictograph_data") and last_beat.pictograph_data:
                end_pos = last_beat.pictograph_data.end_position
                return end_pos or "alpha1"
            # Fallback for dict-based data
            elif isinstance(last_beat, dict) and "end_pos" in last_beat:
                return last_beat["end_pos"]
            elif isinstance(last_beat, dict) and "end_position" in last_beat:
                return last_beat["end_position"]

            return "alpha1"  # Default fallback

        except Exception as e:
            print(f"❌ [SEQUENCE_OPTION] Error extracting end position: {e}")
            return "alpha1"

    def _extract_end_orientations(
        self, sequence_data: SequenceData | list[dict]
    ) -> dict:
        """Extract the end orientations from the last beat in the sequence.

        Handles both modern SequenceData and legacy list format.
        """
        try:
            # Default orientations if no sequence
            default_orientations = {"blue": "in", "red": "out"}

            if not sequence_data:
                return default_orientations

            # Handle legacy format (list of dictionaries)
            if isinstance(sequence_data, list):
                if len(sequence_data) <= 1:
                    return default_orientations

                # Get the last beat (skip metadata at index 0)
                last_beat = sequence_data[-1]
                if isinstance(last_beat, dict):
                    # Try to extract orientations from legacy format
                    end_orientations = {}

                    # Look for blue and red attributes in legacy format
                    for color in ["blue", "red"]:
                        color_attrs = last_beat.get(f"{color}_attributes", {})
                        end_ori = color_attrs.get("end_ori") or color_attrs.get(
                            "end_orientation"
                        )

                        if end_ori:
                            # Convert numeric orientations to string if needed
                            if isinstance(end_ori, (int, float)):
                                # Legacy numeric orientations: 0=in, 180=out, 90=clock, 270=counter
                                orientation_map = {
                                    0: "in",
                                    180: "out",
                                    90: "clock",
                                    270: "counter",
                                }
                                end_orientations[color] = orientation_map.get(
                                    int(end_ori), default_orientations[color]
                                )
                            else:
                                end_orientations[color] = str(end_ori).lower()
                        else:
                            end_orientations[color] = default_orientations[color]

                    return end_orientations

                return default_orientations

            # Handle modern SequenceData format
            if (
                not hasattr(sequence_data, "beats")
                or not sequence_data.beats
                or len(sequence_data.beats) == 0
            ):
                return default_orientations

            last_beat = sequence_data.beats[-1]

            if hasattr(last_beat, "pictograph_data") and last_beat.pictograph_data:
                pictograph_data = last_beat.pictograph_data
                end_orientations = {}

                # Extract end orientations from motions
                for color in ["blue", "red"]:
                    if color in pictograph_data.motions:
                        motion = pictograph_data.motions[color]
                        end_ori = getattr(motion, "end_ori", None)
                        if end_ori:
                            end_orientations[color] = (
                                end_ori.value
                                if hasattr(end_ori, "value")
                                else str(end_ori)
                            )
                        else:
                            end_orientations[color] = default_orientations[color]
                    else:
                        end_orientations[color] = default_orientations[color]

                return end_orientations

            return default_orientations

        except Exception as e:
            print(f"❌ [SEQUENCE_OPTION] Error extracting end orientations: {e}")
            return {"blue": "in", "red": "out"}

    def _update_option_orientations(
        self, options: list[PictographData], end_orientations: dict
    ) -> list[PictographData]:
        """Update all option orientations to match the sequence's end state."""
        try:
            updated_options = []

            for option in options:
                # Create updated motions with correct start orientations
                updated_motions = {}

                for color in ["blue", "red"]:
                    if color in option.motions:
                        original_motion = option.motions[color]

                        # The start orientation should match the end orientation from the sequence
                        new_start_ori = end_orientations.get(
                            color, "in" if color == "blue" else "out"
                        )

                        # Use motion orientation calculator to determine end orientation
                        # based on the motion's turns and the new start orientation
                        new_end_ori = self._calculate_end_orientation(
                            new_start_ori,
                            original_motion.turns,
                            original_motion.motion_type,
                        )

                        # Update the motion with correct orientations
                        updated_motion = original_motion.update(
                            start_ori=new_start_ori, end_ori=new_end_ori
                        )
                        updated_motions[color] = updated_motion

                    else:
                        start_ori = end_orientations.get(
                            color, "in" if color == "blue" else "out"
                        )
                        updated_motions[color] = MotionData(
                            motion_type=MotionType.STATIC,
                            prop_rot_dir=RotationDirection.NO_ROTATION,
                            start_loc=Location.SOUTH,
                            end_loc=Location.SOUTH,
                            turns=0.0,
                            start_ori=Orientation(start_ori),
                            end_ori=Orientation(start_ori),
                        )

                # Also update prop orientations to match the sequence end orientations
                updated_props = option.props.copy()

                for color in ["blue", "red"]:
                    if color in updated_props:
                        prop = updated_props[color]
                        # Update prop orientation to match sequence end orientation
                        new_orientation_str = end_orientations.get(
                            color, "in" if color == "blue" else "out"
                        )

                        # Convert string to Orientation enum
                        from desktop.modern.domain.models.enums import Orientation

                        try:
                            new_orientation = Orientation(new_orientation_str)
                            from dataclasses import replace

                            updated_prop = replace(prop, orientation=new_orientation)
                            updated_props[color] = updated_prop
                        except (ValueError, AttributeError):
                            # Keep original prop if conversion fails
                            pass

                # Create updated pictograph with new motions and props
                updated_option = option.update(
                    motions=updated_motions, props=updated_props
                )
                updated_options.append(updated_option)

            return updated_options

        except Exception as e:
            print(f"❌ [SEQUENCE_OPTION] Error updating option orientations: {e}")
            import traceback

            traceback.print_exc()
            return options  # Return original options if update fails

    def _calculate_end_orientation(
        self, start_ori: str, turns: float, motion_type
    ) -> str:
        """Calculate end orientation based on start orientation, turns, and motion type."""
        try:
            # Convert string to Orientation enum
            start_orientation = Orientation(start_ori)

            # Create a temporary MotionData object for calculation
            from desktop.modern.domain.models.enums import Location, RotationDirection
            from desktop.modern.domain.models.motion_data import MotionData

            temp_motion = MotionData(
                motion_type=motion_type,
                turns=turns,
                start_ori=start_orientation,
                end_ori=start_orientation,  # Will be calculated
                start_loc=Location.NORTH,  # Default values for calculation
                end_loc=Location.SOUTH,
                prop_rot_dir=RotationDirection.CLOCKWISE,
            )

            # Calculate end orientation using the correct orientation calculator
            end_orientation = self._orientation_calculator.calculate_end_orientation(
                temp_motion, start_orientation
            )

            return end_orientation.value

        except Exception as e:
            print(f"❌ [SEQUENCE_OPTION] Error calculating end orientation: {e}")
            # Fallback: if we can't calculate, keep the same orientation
            return start_ori

    def _group_options_by_type(
        self, options: list[PictographData]
    ) -> dict[LetterType, list[PictographData]]:
        """
        Group options by their letter type.

        Pure data processing - no Qt dependencies.
        """
        options_by_type = {}

        for option in options:
            letter = option.letter
            if letter:
                letter_type_str = LetterTypeClassifier.get_letter_type(letter)

                # Ensure letter_type is set on the pictograph data for glyph rendering
                if not option.letter_type:
                    from desktop.modern.domain.models.enums import LetterType

                    letter_type_enum = getattr(
                        LetterType, letter_type_str.upper(), None
                    )

                    # Create new instance with letter_type set (dataclass is frozen)
                    option = PictographData(
                        id=option.id,
                        grid_data=option.grid_data,
                        arrows=option.arrows,
                        props=option.props,
                        motions=option.motions,
                        letter=option.letter,
                        letter_type=letter_type_enum,  # Set the letter type
                        start_position=option.start_position,
                        end_position=option.end_position,
                        beat=option.beat,
                        timing=option.timing,
                        direction=option.direction,
                        duration=option.duration,
                        is_blank=option.is_blank,
                        is_mirrored=option.is_mirrored,
                        metadata=option.metadata,
                    )

                if letter_type_str not in options_by_type:
                    options_by_type[letter_type_str] = []
                options_by_type[letter_type_str].append(option)

        return options_by_type

    def validate_sequence_state(self, sequence_data: SequenceData) -> bool:
        """
        Validate that sequence data is in a valid state for option generation.

        Pure validation logic - no Qt dependencies.
        """
        try:
            if not sequence_data:
                return False

            # Check if we can extract a valid end position
            end_position = self._extract_end_position(sequence_data)
            return bool(end_position and end_position != "")

        except Exception as e:
            print(f"❌ [SEQUENCE_OPTION] Error validating sequence state: {e}")
            return False

    # Interface implementation methods
    def get_sequence_options(self, sequence_state: Any) -> list[Any]:
        """Get options for sequence state (interface implementation)."""
        if isinstance(sequence_state, SequenceData):
            return self.get_options_for_sequence(sequence_state)
        else:
            # Handle other sequence state formats
            return []

    def filter_options_by_continuity(
        self, options: list[Any], last_beat: Any
    ) -> list[Any]:
        """Filter options to maintain sequence continuity (interface implementation)."""
        if not last_beat or not options:
            return options

        filtered_options = []
        for option in options:
            if self.validate_option_continuity(option, last_beat):
                filtered_options.append(option)

        return filtered_options

    def validate_option_continuity(self, option: Any, last_beat: Any) -> bool:
        """Validate if option maintains continuity (interface implementation)."""
        try:
            # Check if option's start position matches last beat's end position
            if hasattr(option, "start_position") and hasattr(last_beat, "end_position"):
                return option.start_position == last_beat.end_position

            # For pictograph data, check grid positions
            if hasattr(option, "grid_data") and hasattr(last_beat, "grid_data"):
                option_start = getattr(option.grid_data, "start_position", None)
                beat_end = getattr(last_beat.grid_data, "end_position", None)
                return option_start == beat_end

            return True  # Default to allowing if we can't determine
        except Exception:
            return False
