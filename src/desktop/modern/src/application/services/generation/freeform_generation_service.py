"""
Freeform Generation Service - Modern Implementation

Direct port of freeform sequence generation algorithm from legacy.
Implements IGenerationService interface for freeform mode.
"""

import random
from copy import deepcopy
from typing import List, Dict, Any, Set

from core.interfaces.generation_services import (
    IGenerationService,
    PropContinuity,
    LetterType,
)
from domain.models.generation_models import GenerationConfig, GenerationResult
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, LETTER
from tka_types import RotationDirection


class FreeformGenerationService(IGenerationService):
    """Service for generating freeform sequences using legacy algorithm."""

    def __init__(
        self,
        construct_tab_provider,
        turn_intensity_manager,
        orientation_calculator,
        sequence_data_manager,
        sequence_workbench_updater,
    ):
        """Initialize with required dependencies."""
        self.construct_tab_provider = construct_tab_provider
        self.turn_intensity_manager = turn_intensity_manager
        self.orientation_calculator = orientation_calculator
        self.sequence_data_manager = sequence_data_manager
        self.sequence_workbench_updater = sequence_workbench_updater

    def generate_freeform_sequence(self, config: GenerationConfig) -> GenerationResult:
        """
        Generate freeform sequence using exact legacy algorithm.

        Direct port from FreeFormSequenceBuilder.build_sequence()
        """
        try:
            # Load current sequence (equivalent to self.sequence = load_current_sequence())
            sequence = self.sequence_data_manager.get_current_sequence()

            # Initialize sequence if needed (from base_sequence_builder.initialize_sequence)
            if len(sequence) == 1:
                self._add_start_position_if_needed()
                sequence = self.sequence_data_manager.get_current_sequence()

            # Set rotation directions based on prop continuity (lines 31-35 in legacy)
            if config.prop_continuity == PropContinuity.CONTINUOUS:
                blue_rot_dir = random.choice(
                    [RotationDirection.CLOCKWISE, RotationDirection.COUNTER_CLOCKWISE]
                )
                red_rot_dir = random.choice(
                    [RotationDirection.CLOCKWISE, RotationDirection.COUNTER_CLOCKWISE]
                )
            else:  # PropContinuity.RANDOM
                blue_rot_dir = None
                red_rot_dir = None

            # Calculate how many beats to generate
            length_of_sequence_upon_start = len(sequence) - 2
            beats_to_generate = config.length - length_of_sequence_upon_start

            # Allocate turns using TurnIntensityManager (lines 39-40 in legacy)
            turns_blue, turns_red = (
                self.turn_intensity_manager.allocate_turns_for_blue_and_red(
                    length=beats_to_generate,
                    level=config.level,
                    turn_intensity=config.turn_intensity,
                )
            )

            # Generation loop (lines 42-58 in legacy)
            generated_beats = []
            for i in range(beats_to_generate):
                next_pictograph = self._generate_next_pictograph(
                    sequence=sequence,
                    level=config.level,
                    turn_blue=turns_blue[i],
                    turn_red=turns_red[i],
                    prop_continuity=config.prop_continuity,
                    blue_rot_dir=blue_rot_dir,
                    red_rot_dir=red_rot_dir,
                    letter_types=config.letter_types,
                )

                # Add to sequence
                sequence.append(next_pictograph)
                generated_beats.append(next_pictograph)

                # Update sequence workbench (equivalent to beat_factory.create_new_beat_and_add_to_sequence)
                self.sequence_workbench_updater.add_beat_to_sequence(
                    next_pictograph,
                    override_grow_sequence=True,
                    update_image_export_preview=False,
                )

            # Update construct tab options (line 60 in legacy)
            self.sequence_workbench_updater.update_construct_tab_options()

            return GenerationResult(
                success=True,
                sequence_data=generated_beats,
                metadata={
                    "algorithm": "freeform",
                    "beats_generated": len(generated_beats),
                    "prop_continuity": config.prop_continuity.value,
                    "blue_rot_dir": blue_rot_dir,
                    "red_rot_dir": red_rot_dir,
                },
            )

        except Exception as e:
            return GenerationResult(
                success=False, error_message=f"Freeform generation failed: {str(e)}"
            )

    def _generate_next_pictograph(
        self,
        sequence: List[Dict],
        level: int,
        turn_blue: float,
        turn_red: float,
        prop_continuity: PropContinuity,
        blue_rot_dir: str,
        red_rot_dir: str,
        letter_types: Set[LetterType],
    ) -> Dict:
        """
        Generate next pictograph using exact legacy algorithm.

        Direct port from FreeFormSequenceBuilder._generate_next_pictograph()
        """
        # Get option dicts (equivalent to self._get_option_dicts())
        option_dicts = self.construct_tab_provider.get_all_next_option_dicts(sequence)
        option_dicts = [deepcopy(option) for option in option_dicts]

        # Filter options by letter type (equivalent to self._filter_options_by_letter_type())
        option_dicts = self._filter_options_by_letter_type(option_dicts, letter_types)

        # Filter by rotation if continuous prop continuity
        if prop_continuity == PropContinuity.CONTINUOUS:
            option_dicts = self._filter_options_by_rotation(
                option_dicts, blue_rot_dir, red_rot_dir
            )

        # Get last beat for orientation continuity
        last_beat = sequence[-1]

        # Random selection (equivalent to random.choice(option_dicts))
        next_beat = random.choice(option_dicts)

        # Set turns if level 2 or 3 (equivalent to self.set_turns())
        if level == 2 or level == 3:
            next_beat = self._set_turns(next_beat, turn_blue, turn_red)

        # Update orientations (from base_sequence_builder)
        next_beat = self._update_start_orientations(next_beat, last_beat)
        next_beat = self._update_dash_static_prop_rot_dirs(
            next_beat, prop_continuity, blue_rot_dir, red_rot_dir
        )
        next_beat = self._update_end_orientations(next_beat)
        next_beat = self._update_beat_number(next_beat, sequence)

        return next_beat

    def _filter_options_by_letter_type(
        self, options: List[Dict], letter_types: Set[LetterType]
    ) -> List[Dict]:
        """Filter options based on selected letter types."""
        # Convert LetterType enums to actual letters
        selected_letters = []
        for letter_type in letter_types:
            # Map LetterType to actual letters - this would need the actual mapping
            # For now, using a simplified approach
            if letter_type == LetterType.TYPE1:
                selected_letters.extend(
                    [
                        "A",
                        "B",
                        "C",
                        "D",
                        "E",
                        "F",
                        "G",
                        "H",
                        "I",
                        "J",
                        "K",
                        "L",
                        "M",
                        "N",
                        "O",
                        "P",
                        "Q",
                        "R",
                        "S",
                        "T",
                        "U",
                        "V",
                    ]
                )
            elif letter_type == LetterType.TYPE2:
                selected_letters.extend(["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"])
            elif letter_type == LetterType.TYPE3:
                selected_letters.extend(
                    ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"]
                )
            elif letter_type == LetterType.TYPE4:
                selected_letters.extend(["Φ", "Ψ", "Λ"])
            elif letter_type == LetterType.TYPE5:
                selected_letters.extend(["Φ-", "Ψ-", "Λ-"])
            elif letter_type == LetterType.TYPE6:
                selected_letters.extend(["α", "β", "Γ"])

        # Filter options
        filtered_options = [
            option for option in options if option.get(LETTER) in selected_letters
        ]

        return filtered_options if filtered_options else options

    def _filter_options_by_rotation(
        self, options: List[Dict], blue_rot_dir: str, red_rot_dir: str
    ) -> List[Dict]:
        """Filter options to match rotation directions (from base_sequence_builder)."""
        from data.constants import PROP_ROT_DIR, BLUE_ATTRS, RED_ATTRS, NO_ROT

        filtered = [
            opt
            for opt in options
            if (
                opt[BLUE_ATTRS].get(PROP_ROT_DIR) in [blue_rot_dir, NO_ROT]
                and opt[RED_ATTRS].get(PROP_ROT_DIR) in [red_rot_dir, NO_ROT]
            )
        ]

        return filtered if filtered else options

    def _set_turns(self, beat: Dict, turn_blue: float, turn_red: float) -> Dict:
        """Set turns for both colors (from base_sequence_builder)."""
        from data.constants import (
            BLUE_ATTRS,
            RED_ATTRS,
            TURNS,
            MOTION_TYPE,
            FLOAT,
            NO_ROT,
            PROP_ROT_DIR,
            PREFLOAT_MOTION_TYPE,
            PREFLOAT_PROP_ROT_DIR,
        )

        # Handle blue turns
        if turn_blue == "fl":
            if beat[BLUE_ATTRS].get(MOTION_TYPE) in ["pro", "anti"]:
                beat[BLUE_ATTRS][TURNS] = "fl"
                beat[BLUE_ATTRS][PREFLOAT_MOTION_TYPE] = beat[BLUE_ATTRS][MOTION_TYPE]
                beat[BLUE_ATTRS][PREFLOAT_PROP_ROT_DIR] = beat[BLUE_ATTRS][PROP_ROT_DIR]
                beat[BLUE_ATTRS][MOTION_TYPE] = FLOAT
                beat[BLUE_ATTRS][PROP_ROT_DIR] = NO_ROT
            else:
                beat[BLUE_ATTRS][TURNS] = 0
        else:
            beat[BLUE_ATTRS][TURNS] = turn_blue

        # Handle red turns
        if turn_red == "fl":
            if beat[RED_ATTRS].get(MOTION_TYPE) in ["pro", "anti"]:
                beat[RED_ATTRS][TURNS] = "fl"
                beat[RED_ATTRS][PREFLOAT_MOTION_TYPE] = beat[RED_ATTRS][MOTION_TYPE]
                beat[RED_ATTRS][PREFLOAT_PROP_ROT_DIR] = beat[RED_ATTRS][PROP_ROT_DIR]
                beat[RED_ATTRS][MOTION_TYPE] = FLOAT
                beat[RED_ATTRS][PROP_ROT_DIR] = NO_ROT
            else:
                beat[RED_ATTRS][TURNS] = 0
        else:
            beat[RED_ATTRS][TURNS] = turn_red

        return beat

    def _update_start_orientations(self, next_beat: Dict, last_beat: Dict) -> Dict:
        """Update start orientations from end of last beat."""
        from data.constants import BLUE_ATTRS, RED_ATTRS, START_ORI, END_ORI

        next_beat[BLUE_ATTRS][START_ORI] = last_beat[BLUE_ATTRS][END_ORI]
        next_beat[RED_ATTRS][START_ORI] = last_beat[RED_ATTRS][END_ORI]
        return next_beat

    def _update_end_orientations(self, beat: Dict) -> Dict:
        """Calculate end orientations using orientation calculator."""
        from data.constants import BLUE, RED

        blue_end_ori = self.orientation_calculator.calculate_end_orientation(beat, BLUE)
        red_end_ori = self.orientation_calculator.calculate_end_orientation(beat, RED)

        beat["blue_attributes"]["end_ori"] = blue_end_ori
        beat["red_attributes"]["end_ori"] = red_end_ori
        return beat

    def _update_dash_static_prop_rot_dirs(
        self,
        beat: Dict,
        prop_continuity: PropContinuity,
        blue_rot_dir: str,
        red_rot_dir: str,
    ) -> Dict:
        """Update prop rotation directions for dash/static motions."""
        from data.constants import (
            BLUE_ATTRS,
            RED_ATTRS,
            MOTION_TYPE,
            DASH,
            STATIC,
            TURNS,
            PROP_ROT_DIR,
            NO_ROT,
        )

        # Update blue
        if beat[BLUE_ATTRS].get(MOTION_TYPE) in [DASH, STATIC]:
            turns = beat[BLUE_ATTRS].get(TURNS, 0)
            if prop_continuity == PropContinuity.CONTINUOUS:
                beat[BLUE_ATTRS][PROP_ROT_DIR] = blue_rot_dir if turns > 0 else NO_ROT
            else:
                if turns > 0:
                    beat[BLUE_ATTRS][PROP_ROT_DIR] = random.choice(
                        [CLOCKWISE, COUNTER_CLOCKWISE]
                    )
                else:
                    beat[BLUE_ATTRS][PROP_ROT_DIR] = NO_ROT

        # Update red
        if beat[RED_ATTRS].get(MOTION_TYPE) in [DASH, STATIC]:
            turns = beat[RED_ATTRS].get(TURNS, 0)
            if prop_continuity == PropContinuity.CONTINUOUS:
                beat[RED_ATTRS][PROP_ROT_DIR] = red_rot_dir if turns > 0 else NO_ROT
            else:
                if turns > 0:
                    beat[RED_ATTRS][PROP_ROT_DIR] = random.choice(
                        [CLOCKWISE, COUNTER_CLOCKWISE]
                    )
                else:
                    beat[RED_ATTRS][PROP_ROT_DIR] = NO_ROT

        return beat

    def _update_beat_number(self, beat: Dict, sequence: List[Dict]) -> Dict:
        """Set beat number based on sequence length."""
        from data.constants import BEAT

        beat[BEAT] = len(sequence) - 1
        return beat

    def _add_start_position_if_needed(self):
        """Add start position if sequence only has one beat."""
        # This would call the start position manager
        # For now, placeholder implementation

    # Required interface methods (not implemented in Phase 1)
    def generate_circular_sequence(self, config: GenerationConfig) -> GenerationResult:
        """Not implemented in Phase 1."""
        return GenerationResult(
            success=False, error_message="Circular generation not implemented yet"
        )

    def auto_complete_sequence(self, current_sequence: Any) -> GenerationResult:
        """Not implemented in Phase 1."""
        return GenerationResult(
            success=False, error_message="Auto-complete not implemented yet"
        )

    def validate_generation_parameters(self, config: GenerationConfig) -> Any:
        """Basic validation."""
        return {"is_valid": True}
