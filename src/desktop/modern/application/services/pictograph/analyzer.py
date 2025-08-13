"""
Pictograph Analysis Service

This service analyzes pictograph data to extract information needed for
arrow positioning, dash location calculations, and other pictograph operations.
It provides comprehensive pictograph analysis functionality.
"""

from typing import Optional

from desktop.modern.domain.models import ArrowColor, LetterType, Location
from desktop.modern.domain.models.enums import GridMode
from desktop.modern.domain.models.pictograph_data import PictographData


class PictographAnalyzer:
    """
    Service to analyze pictograph data and extract positioning information.

    Provides methods to determine:
    - Letter types and special cases (Φ_DASH, Ψ_DASH, Λ)
    - Grid modes and shift arrow locations
    - Arrow colors and motion relationships

    IMPORTANT DATA ACCESS PATTERNS:
    - PictographData
    - BeatData: Access motion via beat_data.blue_motion
    - Never access pictograph_data.blue_motion (doesn't exist!)
    """

    def __init__(self):
        """Initialize the pictograph analysis service."""

    def get_letter_info(self, pictograph_data: PictographData) -> dict:
        """
        Extract letter information from beat data.

        Returns:
            dict with letter analysis including:
            - is_phi_dash: bool
            - is_psi_dash: bool
            - is_lambda: bool
            - is _lambda_dash: bool
            - letter_type: LetterType
        """
        letter = pictograph_data.letter.upper() if pictograph_data.letter else ""

        return {
            "is_phi_dash": letter in ["Φ-", "PHI_DASH", "Φ_DASH"],
            "is_psi_dash": letter in ["Ψ-", "PSI_DASH", "Ψ_DASH"],
            "is_lambda": letter in ["Λ", "LAMBDA"],
            "is_lambda_dash": letter in ["Λ-", "LAMBDA_DASH", "Λ_DASH"],
            "letter_type": self._determine_letter_type(pictograph_data),
        }

    def get_grid_info(self, pictograph_data: PictographData) -> dict:
        """
        Extract grid information from beat data.

        Returns:
            dict with grid analysis including:
            - grid_mode: GridMode
            - shift_location: Location (if applicable)
        """
        # For now, use diamond as default - this should be enhanced
        # to read from pictograph data or beat metadata
        grid_mode = GridMode.DIAMOND

        # Extract shift location if this is a Type 3 scenario
        shift_location = self._get_shift_location(pictograph_data)

        return {"grid_mode": grid_mode, "shift_location": shift_location}

    def get_arrow_color(self, is_blue_arrow: bool) -> ArrowColor:
        """Get arrow color enum based on boolean flag."""
        return ArrowColor.BLUE if is_blue_arrow else ArrowColor.RED

    def _determine_letter_type(self, pictograph_data: PictographData) -> LetterType:
        """
        Determine the letter type from pictograph data.

        This analyzes the motion patterns to determine if it's Type 3
        (one dash motion + one shift motion).

        Args:
            pictograph_data: PictographData object with arrows dictionary containing

        Returns:
            LetterType enum value (TYPE1, TYPE3, etc.)

        Note:
            Motion data must be accessed via pictograph_data.arrows["color"].motion_data,
            NOT pictograph_data.blue_motion (which doesn't exist on PictographData).
        """
        blue_motion = pictograph_data.motions.get("blue")
        red_motion = pictograph_data.motions.get("red")

        if not blue_motion or not red_motion:
            return LetterType.TYPE1  # Default fallback

        # Type 3 detection: one DASH motion + one shift motion
        blue_is_dash = blue_motion.motion_type.value == "dash"
        red_is_dash = red_motion.motion_type.value == "dash"

        blue_is_shift = blue_motion.motion_type.value in ["pro", "anti", "float"]
        red_is_shift = red_motion.motion_type.value in ["pro", "anti", "float"]

        # Check for Type 3 pattern
        if (blue_is_dash and red_is_shift) or (red_is_dash and blue_is_shift):
            # Additionally check for zero turns on the dash motion
            dash_motion = blue_motion if blue_is_dash else red_motion
            if getattr(dash_motion, "turns", 0) == 0:
                return LetterType.TYPE3
        # For now, default to TYPE1 - this could be enhanced with more analysis
        return LetterType.TYPE1

    def _get_shift_location(
        self, pictograph_data: PictographData
    ) -> Optional[Location]:
        """
        Extract shift arrow location for Type 3 calculations using proven algorithms.

        In Type 3 scenarios, we need the calculated location of the shift (non-dash) arrow
        using the frozen set quadrant mapping from the shift location calculation system.
        """
        blue_motion = pictograph_data.motions.get("blue")
        red_motion = pictograph_data.motions.get("red")

        if not blue_motion or not red_motion:
            return None

        # Find the shift motion (non-dash)
        blue_is_dash = blue_motion.motion_type.value == "dash"
        red_is_dash = red_motion.motion_type.value == "dash"

        shift_motion = None
        if blue_is_dash and not red_is_dash:
            # Red is the shift motion
            shift_motion = red_motion
        elif red_is_dash and not blue_is_dash:
            # Blue is the shift motion
            shift_motion = blue_motion

        if not shift_motion:
            return None

        # Use the proven shift location calculation algorithm
        # Direction pairs mapping from ShiftLocationCalculator
        direction_pairs = {
            frozenset({Location.NORTH, Location.EAST}): Location.NORTHEAST,
            frozenset({Location.EAST, Location.SOUTH}): Location.SOUTHEAST,
            frozenset({Location.SOUTH, Location.WEST}): Location.SOUTHWEST,
            frozenset({Location.WEST, Location.NORTH}): Location.NORTHWEST,
            frozenset({Location.NORTHEAST, Location.NORTHWEST}): Location.NORTH,
            frozenset({Location.NORTHEAST, Location.SOUTHEAST}): Location.EAST,
            frozenset({Location.SOUTHWEST, Location.SOUTHEAST}): Location.SOUTH,
            frozenset({Location.NORTHWEST, Location.SOUTHWEST}): Location.WEST,
        }

        # Calculate shift location using start and end locations
        start_loc = shift_motion.start_loc
        end_loc = shift_motion.end_loc

        return direction_pairs.get(frozenset({start_loc, end_loc}), start_loc)
