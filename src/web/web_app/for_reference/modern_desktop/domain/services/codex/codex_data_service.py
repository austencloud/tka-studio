"""
Codex Data Service

Provides pictograph data for the codex, converting legacy letter mappings
to modern PictographData objects.
"""

from __future__ import annotations

import logging

from legacy.data.constants import (
    ALPHA1,
    ALPHA3,
    ALPHA5,
    ALPHA7,
    ANTI,
    BETA1,
    BETA3,
    BETA5,
    BETA7,
    BLUE,
    DASH,
    END_POS,
    GAMMA1,
    GAMMA3,
    GAMMA5,
    GAMMA7,
    GAMMA11,
    GAMMA13,
    GAMMA15,
    MOTION_TYPE,
    PRO,
    RED,
    START_POS,
    STATIC,
)
from legacy.enums.letter.letter import Letter
from legacy.enums.letter.letter_type import LetterType

from desktop.modern.domain.models.pictograph_data import PictographData


logger = logging.getLogger(__name__)


class CodexDataService:
    """
    Service for managing codex pictograph data.

    Converts legacy letter mappings to modern PictographData objects
    and provides organized access to all codex pictographs.
    """

    # Letter organization from legacy codex
    ROWS = [
        ["A", "B", "C", "D", "E", "F"],
        ["G", "H", "I", "J", "K", "L"],
        ["M", "N", "O", "P", "Q", "R"],
        ["S", "T", "U", "V"],
        ["W", "X", "Y", "Z"],
        ["Σ", "Δ", "θ", "Ω"],
        ["W-", "X-", "Y-", "Z-"],
        ["Σ-", "Δ-", "θ-", "Ω-"],
        ["Φ", "Ψ", "Λ"],
        ["Φ-", "Ψ-", "Λ-"],
        ["α", "β", "Γ"],
    ]

    def __init__(self, pictograph_data_service=None):
        self._pictograph_cache: dict[str, PictographData | None] = {}
        self.pictograph_data_service = pictograph_data_service
        self._initialize_pictograph_data()

    def _initialize_pictograph_data(self) -> None:
        """Initialize pictograph data for all letters."""
        logger.debug("Initializing codex pictograph data")

        # Get all letters from the Letter enum
        letters = [letter.value for letter in Letter]

        for letter in letters:
            try:
                # Get the legacy parameters for this letter
                legacy_params = self._get_legacy_pictograph_params(letter)
                if legacy_params:
                    # Use dataset service to get real pictograph data
                    pictograph_data = self._get_pictograph_from_dataset(
                        letter, legacy_params
                    )
                    self._pictograph_cache[letter] = pictograph_data
                else:
                    self._pictograph_cache[letter] = None
                    logger.debug(f"No parameters found for letter: {letter}")
            except Exception as e:
                logger.warning(f"Failed to initialize data for letter {letter}: {e}")
                self._pictograph_cache[letter] = None

    def _get_legacy_pictograph_params(self, letter: str) -> dict | None:
        """Get legacy pictograph parameters for a letter."""
        # Import additional constants here to avoid IDE auto-formatting issues

        # This is the complete mapping from the legacy CodexDataManager
        params_map = {
            "A": {
                START_POS: ALPHA1,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": PRO,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "B": {
                START_POS: ALPHA1,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "C": {
                START_POS: ALPHA1,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "D": {
                START_POS: BETA1,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": PRO,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "E": {
                START_POS: BETA1,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "F": {
                START_POS: BETA1,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "G": {
                START_POS: BETA3,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": PRO,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "H": {
                START_POS: BETA3,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "I": {
                START_POS: BETA3,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "J": {
                START_POS: ALPHA3,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": PRO,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "K": {
                START_POS: ALPHA3,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "L": {
                START_POS: ALPHA3,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "M": {
                START_POS: GAMMA11,
                END_POS: GAMMA1,
                f"{BLUE}_{MOTION_TYPE}": PRO,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "N": {
                START_POS: GAMMA11,
                END_POS: GAMMA1,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "O": {
                START_POS: GAMMA11,
                END_POS: GAMMA1,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "P": {
                START_POS: GAMMA1,
                END_POS: GAMMA15,
                f"{BLUE}_{MOTION_TYPE}": PRO,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "Q": {
                START_POS: GAMMA1,
                END_POS: GAMMA15,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "R": {
                START_POS: GAMMA1,
                END_POS: GAMMA15,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "S": {
                START_POS: GAMMA13,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": PRO,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "T": {
                START_POS: GAMMA13,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "U": {
                START_POS: GAMMA13,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "V": {
                START_POS: GAMMA13,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": PRO,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "W": {
                START_POS: GAMMA13,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "X": {
                START_POS: GAMMA13,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "Y": {
                START_POS: GAMMA11,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "Z": {
                START_POS: GAMMA11,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "Σ": {
                START_POS: ALPHA3,
                END_POS: GAMMA13,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "Δ": {
                START_POS: ALPHA3,
                END_POS: GAMMA13,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "θ": {
                START_POS: BETA5,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "Ω": {
                START_POS: BETA5,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "W-": {
                START_POS: GAMMA5,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "X-": {
                START_POS: GAMMA5,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "Y-": {
                START_POS: GAMMA3,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "Z-": {
                START_POS: GAMMA3,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "Σ-": {
                START_POS: BETA3,
                END_POS: GAMMA13,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "Δ-": {
                START_POS: BETA3,
                END_POS: GAMMA13,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "θ-": {
                START_POS: ALPHA5,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "Ω-": {
                START_POS: ALPHA5,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "Φ": {
                START_POS: BETA7,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": DASH,
            },
            "Ψ": {
                START_POS: ALPHA1,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": DASH,
            },
            "Λ": {
                START_POS: GAMMA7,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": DASH,
            },
            "Φ-": {
                START_POS: ALPHA3,
                END_POS: ALPHA7,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": DASH,
            },
            "Ψ-": {
                START_POS: BETA1,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": DASH,
            },
            "Λ-": {
                START_POS: GAMMA15,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": DASH,
            },
            "α": {
                START_POS: ALPHA3,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": STATIC,
            },
            "β": {
                START_POS: BETA5,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": STATIC,
            },
            "Γ": {
                START_POS: GAMMA11,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": STATIC,
            },
        }

        return params_map.get(letter)

    def _create_pictograph_data(
        self, letter: str, legacy_params: dict
    ) -> PictographData:
        """Create PictographData from legacy parameters."""
        try:
            logger.debug(
                f"Creating pictograph data for {letter} with params: {legacy_params}"
            )

            from desktop.modern.domain.models.arrow_data import ArrowData
            from desktop.modern.domain.models.enums import (
                ArrowType,
                GridMode,
                GridPosition,
                MotionType,
                Orientation,
                RotationDirection,
            )
            from desktop.modern.domain.models.grid_data import GridData
            from desktop.modern.domain.models.motion_data import MotionData

            # Extract motion parameters
            start_pos = legacy_params[START_POS]
            end_pos = legacy_params[END_POS]
            blue_motion_type = legacy_params[f"{BLUE}_{MOTION_TYPE}"]
            red_motion_type = legacy_params[f"{RED}_{MOTION_TYPE}"]

            # Create motion data for blue and red
            motions = {}
            arrows = {}

            # Create blue motion and arrow (always create both for turns tuple service)
            if blue_motion_type != STATIC:
                # Convert string values to enums
                motion_type_enum = (
                    MotionType.PRO if blue_motion_type == PRO else MotionType.ANTI
                )
                start_loc_enum = GridPosition(start_pos)
                end_loc_enum = GridPosition(end_pos)

                # Debug logging
                logger.debug(
                    f"Creating blue motion: type={motion_type_enum}, start={start_loc_enum}, end={end_loc_enum}"
                )

                blue_motion = MotionData(
                    motion_type=motion_type_enum,
                    prop_rot_dir=RotationDirection.CLOCKWISE,  # Default rotation
                    start_loc=start_loc_enum,
                    end_loc=end_loc_enum,
                    start_ori=Orientation.IN,
                    end_ori=Orientation.OUT,
                    turns=0,
                )
            else:
                # Create static motion for turns tuple service compatibility
                blue_motion = MotionData(
                    motion_type=MotionType.STATIC,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=GridPosition(start_pos),
                    end_loc=GridPosition(start_pos),  # Same position for static
                    start_ori=Orientation.IN,
                    end_ori=Orientation.IN,
                    turns=0,
                )

            motions["blue"] = blue_motion
            blue_arrow = ArrowData(
                color="blue",
                arrow_type=ArrowType.BLUE,
                turns=0.0,
            )
            arrows["blue"] = blue_arrow

            # Create red motion and arrow (always create both for turns tuple service)
            if red_motion_type != STATIC:
                # Convert string values to enums
                motion_type_enum = (
                    MotionType.PRO if red_motion_type == PRO else MotionType.ANTI
                )
                start_loc_enum = GridPosition(start_pos)
                end_loc_enum = GridPosition(end_pos)

                red_motion = MotionData(
                    motion_type=motion_type_enum,
                    prop_rot_dir=RotationDirection.CLOCKWISE,  # Default rotation
                    start_loc=start_loc_enum,
                    end_loc=end_loc_enum,
                    start_ori=Orientation.IN,
                    end_ori=Orientation.OUT,
                    turns=0,
                )
            else:
                # Create static motion for turns tuple service compatibility
                red_motion = MotionData(
                    motion_type=MotionType.STATIC,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=GridPosition(start_pos),
                    end_loc=GridPosition(start_pos),  # Same position for static
                    start_ori=Orientation.IN,
                    end_ori=Orientation.IN,
                    turns=0,
                )

            motions["red"] = red_motion
            red_arrow = ArrowData(
                color="red",
                arrow_type=ArrowType.RED,
                turns=0.0,
            )
            arrows["red"] = red_arrow

            # Create grid data

            grid_data = GridData(grid_mode=GridMode.DIAMOND)

            # Create the pictograph data using from_dict to handle enum conversions
            pictograph_dict = {
                "letter": letter,
                "start_position": start_pos,
                "end_position": end_pos,
                "grid_data": grid_data.to_dict(),
                "arrows": {k: v.to_dict() for k, v in arrows.items()},
                "motions": {k: v.to_dict() for k, v in motions.items()},
                "props": {},
                "metadata": {"source": "codex_legacy_conversion"},
            }

            return PictographData.from_dict(pictograph_dict)

        except Exception as e:
            logger.error(f"Error creating pictograph data for {letter}: {e}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    def _get_pictograph_from_dataset(
        self, letter: str, legacy_params: dict
    ) -> PictographData | None:
        """Get real pictograph data using the injected dataset service."""
        if not self.pictograph_data_service:
            # Fallback to basic data creation if no dataset service
            logger.debug(
                "No pictograph data service available, using fallback data creation"
            )
            return self._create_pictograph_data(letter, legacy_params)

        try:
            # Get all data from the PictographDataManager
            all_data = self.pictograph_data_service.get_all_data()

            # Find matching pictograph data
            matching_entry = self._find_matching_csv_entry(
                all_data, letter, legacy_params
            )

            if matching_entry:
                logger.debug(f"Found matching dataset entry for letter {letter}")
                # Convert the CSV data to PictographData
                return self._convert_csv_data_to_pictograph(letter, matching_entry)

            # No exact match found, try to get any entry for this letter
            letter_entries = [
                entry for entry in all_data if entry.get("letter") == letter
            ]

            if letter_entries:
                logger.debug(
                    f"No exact match for {letter}, using first available entry"
                )
                first_entry = letter_entries[0]
                return self._convert_csv_data_to_pictograph(letter, first_entry)

            # No data found, fallback to basic creation
            logger.debug(f"No dataset entry found for letter {letter}, using fallback")
            return self._create_pictograph_data(letter, legacy_params)

        except Exception as e:
            logger.warning(f"Failed to get pictograph from dataset for {letter}: {e}")
            return self._create_pictograph_data(letter, legacy_params)

    def _find_matching_csv_entry(
        self, all_data: list[dict], letter: str, legacy_params: dict
    ) -> dict | None:
        """Find CSV entry that matches the legacy parameters."""
        for entry in all_data:
            if entry.get("letter") == letter and self._matches_csv_entry_params(
                entry, legacy_params
            ):
                return entry
        return None

    def _matches_csv_entry_params(self, csv_entry: dict, legacy_params: dict) -> bool:
        """Check if a CSV entry matches the legacy parameters."""
        try:
            # CSV format uses different field names than legacy format
            return (
                csv_entry.get("start_pos") == legacy_params.get(START_POS)
                and csv_entry.get("end_pos") == legacy_params.get(END_POS)
                and csv_entry.get("blue_motion_type")
                == legacy_params.get(f"{BLUE}_{MOTION_TYPE}")
                and csv_entry.get("red_motion_type")
                == legacy_params.get(f"{RED}_{MOTION_TYPE}")
            )
        except Exception as e:
            logger.debug(f"Error matching CSV entry params: {e}")
            return False

    def _convert_csv_data_to_pictograph(
        self, letter: str, csv_entry: dict
    ) -> PictographData | None:
        """Convert CSV data entry to PictographData."""
        try:
            from desktop.modern.domain.models.arrow_data import ArrowData
            from desktop.modern.domain.models.enums import GridPosition
            from desktop.modern.domain.models.grid_data import GridData, GridMode
            from desktop.modern.domain.models.motion_data import MotionData

            # Extract positions
            start_pos = GridPosition(csv_entry.get("start_pos", "alpha1"))
            end_pos = GridPosition(csv_entry.get("end_pos", "alpha3"))

            # Create motion data from CSV
            motions = {}

            # Blue motion
            blue_motion_type_str = csv_entry.get("blue_motion_type", "pro")
            blue_motion_type = self._convert_motion_type_string(blue_motion_type_str)

            from desktop.modern.domain.models.enums import Location

            blue_prop_rot_dir_str = csv_entry.get("blue_prop_rot_dir", "cw")
            blue_prop_rot_dir = self._convert_rotation_direction_string(
                blue_prop_rot_dir_str
            )

            blue_motion = MotionData(
                motion_type=blue_motion_type,
                start_loc=Location(csv_entry.get("blue_start_loc", "s")),
                end_loc=Location(csv_entry.get("blue_end_loc", "w")),
                prop_rot_dir=blue_prop_rot_dir,
            )
            motions["blue"] = blue_motion

            # Red motion
            red_motion_type_str = csv_entry.get("red_motion_type", "pro")
            red_motion_type = self._convert_motion_type_string(red_motion_type_str)

            red_prop_rot_dir_str = csv_entry.get("red_prop_rot_dir", "cw")
            red_prop_rot_dir = self._convert_rotation_direction_string(
                red_prop_rot_dir_str
            )

            red_motion = MotionData(
                motion_type=red_motion_type,
                start_loc=Location(csv_entry.get("red_start_loc", "n")),
                end_loc=Location(csv_entry.get("red_end_loc", "e")),
                prop_rot_dir=red_prop_rot_dir,
            )
            motions["red"] = red_motion

            # Create arrows (simplified for now)
            arrows = {}
            blue_arrow = ArrowData(
                location=blue_motion.end_loc,
                color="blue",
            )
            arrows["blue"] = blue_arrow

            red_arrow = ArrowData(
                location=red_motion.end_loc,
                color="red",
            )
            arrows["red"] = red_arrow

            # Create grid data
            grid_data = GridData(grid_mode=GridMode.DIAMOND)

            # Determine letter type for TKA glyph rendering
            from desktop.modern.domain.models.enums import LetterType
            from desktop.modern.domain.models.letter_type_classifier import (
                LetterTypeClassifier,
            )

            letter_type_str = LetterTypeClassifier.get_letter_type(letter)

            # Convert string to LetterType enum (e.g., "Type1" -> LetterType.TYPE1)
            letter_type_enum_name = letter_type_str.upper()  # "Type1" -> "TYPE1"
            letter_type = getattr(LetterType, letter_type_enum_name, None)

            # Create the pictograph data
            pictograph_dict = {
                "letter": letter,
                "letter_type": letter_type,
                "start_position": start_pos,
                "end_position": end_pos,
                "grid_data": grid_data.to_dict(),
                "arrows": {k: v.to_dict() for k, v in arrows.items()},
                "motions": {k: v.to_dict() for k, v in motions.items()},
                "props": {},
                "metadata": {"source": "csv_data_conversion"},
            }

            return PictographData.from_dict(pictograph_dict)

        except Exception as e:
            logger.error(f"Error converting CSV data to pictograph for {letter}: {e}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
            return None

    def _convert_motion_type_string(self, motion_type_str: str):
        """Convert CSV motion type string to MotionType enum."""
        from desktop.modern.domain.models.enums import MotionType

        motion_type_map = {
            "pro": MotionType.PRO,
            "anti": MotionType.ANTI,
            "static": MotionType.STATIC,
            "dash": MotionType.DASH,
            "float": MotionType.FLOAT,
        }
        return motion_type_map.get(motion_type_str.lower(), MotionType.STATIC)

    def _convert_rotation_direction_string(self, rot_dir_str: str):
        """Convert CSV rotation direction string to RotationDirection enum."""
        from desktop.modern.domain.models.enums import RotationDirection

        rot_dir_map = {
            "cw": RotationDirection.CLOCKWISE,
            "ccw": RotationDirection.COUNTER_CLOCKWISE,
            "no_rot": RotationDirection.NO_ROTATION,
        }
        return rot_dir_map.get(rot_dir_str.lower(), RotationDirection.NO_ROTATION)

    def _matches_legacy_params(
        self, pictograph_entry: dict, legacy_params: dict
    ) -> bool:
        """Check if a pictograph entry matches legacy parameters."""
        try:
            # Handle different data formats
            if isinstance(pictograph_entry, dict):
                if "data" in pictograph_entry:
                    # Extract from nested data structure
                    data = pictograph_entry["data"]
                    if hasattr(data, "to_dict"):
                        entry_dict = data.to_dict()
                    else:
                        entry_dict = data
                else:
                    entry_dict = pictograph_entry
            else:
                # Assume it has a to_dict method
                entry_dict = pictograph_entry.to_dict()

            # Check start_pos, end_pos, and motion types
            return (
                entry_dict.get(START_POS) == legacy_params.get(START_POS)
                and entry_dict.get(END_POS) == legacy_params.get(END_POS)
                and entry_dict.get(f"{BLUE}_{MOTION_TYPE}")
                == legacy_params.get(f"{BLUE}_{MOTION_TYPE}")
                and entry_dict.get(f"{RED}_{MOTION_TYPE}")
                == legacy_params.get(f"{RED}_{MOTION_TYPE}")
            )
        except Exception as e:
            logger.debug(f"Error matching legacy params: {e}")
            return False

    def get_pictograph_data(self, letter: str) -> PictographData | None:
        """Get pictograph data for a specific letter."""
        return self._pictograph_cache.get(letter)

    def get_all_pictograph_data(self) -> dict[str, PictographData | None]:
        """Get all pictograph data."""
        return self._pictograph_cache.copy()

    def get_letters_by_row(self) -> list[list[str]]:
        """Get letters organized by rows for grid display."""
        return self.ROWS

    def get_letters_by_type(self, letter_type: LetterType) -> list[str]:
        """Get letters filtered by letter type."""
        # This would need to be implemented based on how letter types are determined
        # For now, return all letters
        return [
            letter
            for letter in self._pictograph_cache.keys()
            if self._pictograph_cache[letter] is not None
        ]

    def refresh_data(self) -> None:
        """Refresh all pictograph data."""
        self._pictograph_cache.clear()
        self._initialize_pictograph_data()
        logger.info("Codex pictograph data refreshed")
