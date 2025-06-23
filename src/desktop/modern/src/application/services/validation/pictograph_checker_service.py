"""
Pictograph Checker Service - Legacy Compatible

Faithful port of legacy PictographChecker for orientation, layer, and letter condition checks.
Updated to work with the modern domain models and letter type classification system.
"""

import logging
from typing import Optional

from domain.models.core_models import Orientation, MotionType
from domain.models.pictograph_models import PictographData
from domain.models.letter_condition import LetterCondition
from domain.models.letter_type_classifier import LetterTypeClassifier

logger = logging.getLogger(__name__)


class PictographCheckerService:
    """
    Service for checking pictograph properties and conditions.

    This is a faithful port of the legacy PictographChecker, adapted to work
    with the modern domain models and letter classification system.
    """

    def __init__(self, pictograph_data: PictographData):
        """Initialize with pictograph data."""
        self.pictograph_data = pictograph_data

    def ends_with_beta(self) -> bool:
        """Check if pictograph ends with beta position."""
        try:
            letter = self.pictograph_data.letter
            if not letter:
                return False

            # Check if letter ends with β or is a beta-ending type
            return (
                letter.endswith("β")
                or letter.endswith("beta")
                or self._is_beta_ending_letter(letter)
            )
        except (AttributeError, ValueError):
            return False

    def ends_with_alpha(self) -> bool:
        """Check if pictograph ends with alpha position."""
        try:
            letter = self.pictograph_data.letter
            if not letter:
                return False

            # Check if letter ends with α or is an alpha-ending type
            return (
                letter.endswith("α")
                or letter.endswith("alpha")
                or self._is_alpha_ending_letter(letter)
            )
        except (AttributeError, ValueError):
            return False

    def ends_with_gamma(self) -> bool:
        """Check if pictograph ends with gamma position."""
        try:
            letter = self.pictograph_data.letter
            if not letter:
                return False

            # Check if letter ends with Γ or is a gamma-ending type
            return (
                letter.endswith("Γ")
                or letter.endswith("gamma")
                or self._is_gamma_ending_letter(letter)
            )
        except (AttributeError, ValueError):
            return False

    def ends_with_layer3(self) -> bool:
        """Check if pictograph ends with layer3 (hybrid orientation)."""
        try:
            letter = self.pictograph_data.letter
            if not letter:
                return False

            # Layer3 letters are hybrid types (TYPE2+)
            letter_type = LetterTypeClassifier.get_letter_type(letter)
            return letter_type in ["Type2", "Type3", "Type4", "Type5", "Type6"]
        except (AttributeError, ValueError):
            return False

    def ends_with_radial_ori(self) -> bool:
        """Check if pictograph has radial orientation properties."""
        try:
            # Check if any arrow has radial orientation (in/out)
            for arrow_data in self.pictograph_data.arrows.values():
                if arrow_data.motion_data:
                    end_ori = getattr(arrow_data.motion_data, "end_ori", None)
                    if end_ori in ["in", "out"]:
                        return True
            return False
        except (AttributeError, ValueError):
            return False

    def ends_with_nonradial_ori(self) -> bool:
        """Check if pictograph has non-radial orientation properties."""
        try:
            # Check if any arrow has non-radial orientation (clock/counter)
            for arrow_data in self.pictograph_data.arrows.values():
                if arrow_data.motion_data:
                    end_ori = getattr(arrow_data.motion_data, "end_ori", None)
                    if end_ori in ["clock", "counter"]:
                        return True
            return False
        except (AttributeError, ValueError):
            return False

    def _is_beta_ending_letter(self, letter: str) -> bool:
        """Check if letter is classified as beta-ending."""
        # In legacy, these would be letters that end in beta positions
        # For now, use Type6 as these are typically beta letters
        return LetterTypeClassifier.get_letter_type(letter) == "Type6"

    def _is_alpha_ending_letter(self, letter: str) -> bool:
        """Check if letter is classified as alpha-ending."""
        # Alpha letters are typically single character letters (Type1)
        return LetterTypeClassifier.get_letter_type(letter) == "Type1"

    def _is_gamma_ending_letter(self, letter: str) -> bool:
        """Check if letter is classified as gamma-ending."""
        # Gamma letters are typically the Type6 Greek letters
        return letter in ["α", "β", "Γ"]
