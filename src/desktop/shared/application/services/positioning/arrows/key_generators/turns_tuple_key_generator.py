"""
Turns Tuple Generation Service

Generates turns tuples for special placement data structure navigation.
Handles the complex logic for different letter types and motion combinations.

Faithful port of the turns tuple generation logic from legacy special placement system.
"""

import logging

from desktop.modern.domain.models.letter_type_classifier import LetterTypeClassifier
from desktop.modern.domain.models.motion_data import MotionData
from desktop.modern.domain.models.pictograph_data import PictographData

logger = logging.getLogger(__name__)


class TurnsTupleKeyGenerator:
    """
    Service for generating turns tuples used in special placement lookups.

    This determines which section within a letter file to look in for adjustments.
    Format depends on letter type:
    - Non-hybrid letters: "(blue_turns, red_turns)"
    - Type1 hybrids: Use generator-specific logic
    - Type2+ hybrids: Use lead state logic
    """

    def generate_turns_tuple(self, pictograph_data: PictographData) -> str:
        """
        Generate turns tuple for special placement lookup.

        This determines which section within a letter file to look for adjustments.
        Based on the legacy turns tuple generation logic.

        Args:
            pictograph_data: Pictograph with motion data

        Returns:
            Turns tuple string (e.g., "(0, 1)", "(1.5, 0.5)")
        """
        letter = pictograph_data.letter
        blue_arrow = pictograph_data.arrows.get("blue")
        red_arrow = pictograph_data.arrows.get("red")

        if not letter or not blue_arrow or not red_arrow:
            logger.warning("Missing required data for turns tuple generation")
            return "(0, 0)"

        blue_motion = pictograph_data.motions.get("blue")
        red_motion = pictograph_data.motions.get("red")

        if not blue_motion or not red_motion:
            logger.warning("Missing motion data for turns tuple generation")
            return "(0, 0)"

        # Check if this is a non-hybrid letter
        if self._is_non_hybrid_letter(letter):
            # Simple tuple format for non-hybrid letters
            blue_turns = self._normalize_turns(blue_motion.turns)
            red_turns = self._normalize_turns(red_motion.turns)
            tuple_str = f"({blue_turns}, {red_turns})"
            logger.debug(f"Non-hybrid turns tuple: {tuple_str}")
            return tuple_str

        # For hybrid letters, determine the specific generation logic
        generator_key = self._get_generator_key(letter, blue_motion, red_motion)

        if generator_key.startswith("Type1"):
            return self._generate_type1_hybrid_tuple(
                blue_motion, red_motion, generator_key
            )
        else:
            return self._generate_lead_state_tuple(
                blue_motion, red_motion, generator_key
            )

    def _normalize_turns(self, turns) -> str:
        """Normalize turns value to string format."""
        if turns == "fl":
            return "fl"
        elif isinstance(turns, (int, float)):
            if turns == int(turns):
                return str(int(turns))
            else:
                return str(turns)
        else:
            return str(turns)

    def _get_generator_key(
        self, letter: str, blue_motion: MotionData, red_motion: MotionData
    ) -> str:
        """
        Determine which generator key to use for hybrid letters.

        This logic determines the format of the turns tuple based on the letter
        and motion combinations.

        Args:
            letter: The letter being processed
            blue_motion: Blue arrow motion data
            red_motion: Red arrow motion data

        Returns:
            Generator key string
        """
        # Get letter type classification
        letter_type = LetterTypeClassifier.get_letter_type(letter)

        # Type1 letters use specific generators
        if letter_type == "Type1":
            return f"Type1_{letter[:2]}"

        # Type2 and above are typically hybrid and use lead state logic
        return f"LeadState_{letter_type}"

    def _generate_type1_hybrid_tuple(
        self, blue_motion: MotionData, red_motion: MotionData, generator_key: str
    ) -> str:
        """
        Generate turns tuple for Type1 hybrid letters.

        These use specific generator logic based on the motion combinations.

        Args:
            blue_motion: Blue arrow motion data
            red_motion: Red arrow motion data
            generator_key: The generator key for this letter type

        Returns:
            Type1 formatted turns tuple
        """
        # For Type1 letters, use standard tuple format but may have special formatting
        blue_turns = self._normalize_turns(blue_motion.turns)
        red_turns = self._normalize_turns(red_motion.turns)

        # Type1 tuples are typically standard format
        tuple_str = f"({blue_turns}, {red_turns})"
        logger.debug(f"Type1 hybrid tuple: {tuple_str}")

        return tuple_str

    def _generate_lead_state_tuple(
        self, blue_motion: MotionData, red_motion: MotionData, generator_key: str
    ) -> str:
        """
        Generate turns tuple for lead state logic.

        These use lead state determination to format the tuple.
        For hybrid letters (Type2+), the tuple format may depend on which
        arrow is the "lead" arrow.

        Args:
            blue_motion: Blue arrow motion data
            red_motion: Red arrow motion data
            generator_key: The generator key for this letter type

        Returns:
            Lead state formatted turns tuple
        """
        blue_turns = self._normalize_turns(blue_motion.turns)
        red_turns = self._normalize_turns(red_motion.turns)

        # For lead state, typically use standard tuple format
        # but could have different logic based on which arrow leads
        tuple_str = f"({blue_turns}, {red_turns})"
        logger.debug(f"Lead state tuple: {tuple_str}")

        return tuple_str

    def _is_non_hybrid_letter(self, letter: str) -> bool:
        """
        Check if letter is in non-hybrid category.

        Non-hybrid letters are typically Type1 letters without complex
        orientation mixing.

        Args:
            letter: The letter to check

        Returns:
            True if letter is non-hybrid
        """
        letter_type = LetterTypeClassifier.get_letter_type(letter)

        # Type1 letters are typically non-hybrid
        # But some Type1 letters can be hybrid, so we also check the letter itself
        if letter_type == "Type1":
            # Most single character Type1 letters are non-hybrid
            return len(letter) <= 2 and letter.isalpha()

        # Type2+ letters are typically hybrid
        return False
