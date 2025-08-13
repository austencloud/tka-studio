"""
Pictograph Checker Service - Legacy Compatible

Faithful port of legacy PictographChecker for orientation, layer, and letter condition checks.
Updated to work with the modern domain models and letter type classification system.
"""

import logging

from desktop.modern.core.interfaces.pictograph_services import IPictographValidator
from desktop.modern.domain.models.enums import Orientation
from desktop.modern.domain.models.letter_condition import LetterCondition
from desktop.modern.domain.models.motion_data import MotionData
from desktop.modern.domain.models.pictograph_data import PictographData

logger = logging.getLogger(__name__)


class PictographValidator(IPictographValidator):
    """
    Service for checking pictograph properties and conditions.

    This is a faithful port of the legacy PictographChecker, adapted to work
    with the modern domain models and letter classification system.
    """

    def __init__(
        self,
        pictograph_data: PictographData,
        orientation_calculator=None,
    ):
        """Initialize with pictograph data and optional dependencies."""
        self.pictograph_data = pictograph_data
        self.orientation_calculator = orientation_calculator

    def ends_with_beta(self) -> bool:
        """
        Check if pictograph ends with beta position.

        Uses exact legacy logic: check if letter is in BETA_ENDING condition mapping.
        """
        try:
            letter = self.pictograph_data.letter
            if not letter:
                return False

            # Use exact legacy logic: check letter_condition_mappings
            beta_ending_letters = self._get_letters_by_condition(
                LetterCondition.BETA_ENDING
            )
            return letter in beta_ending_letters
        except (AttributeError, ValueError):
            return False

    def ends_with_alpha(self) -> bool:
        """
        Check if pictograph ends with alpha position.

        Uses exact legacy logic: check if letter is in ALPHA_ENDING condition mapping.
        """
        try:
            letter = self.pictograph_data.letter
            if not letter:
                return False

            # Use exact legacy logic: check letter_condition_mappings
            alpha_ending_letters = self._get_letters_by_condition(
                LetterCondition.ALPHA_ENDING
            )
            return letter in alpha_ending_letters
        except (AttributeError, ValueError):
            return False

    def ends_with_gamma(self) -> bool:
        """
        Check if pictograph ends with gamma position.

        Uses exact legacy logic: check if letter is in GAMMA_ENDING condition mapping.
        """
        try:
            letter = self.pictograph_data.letter
            if not letter:
                return False

            # Use exact legacy logic: check letter_condition_mappings
            gamma_ending_letters = self._get_letters_by_condition(
                LetterCondition.GAMMA_ENDING
            )
            return letter in gamma_ending_letters
        except (AttributeError, ValueError):
            return False

    def ends_with_layer3(self) -> bool:
        try:
            blue_arrow = self.pictograph_data.arrows.get("blue")
            red_arrow = self.pictograph_data.arrows.get("red")
            blue_motion = self.pictograph_data.motions.get("blue")
            red_motion = self.pictograph_data.motions.get("red")

            if not (blue_arrow and red_arrow):
                return False

            b_ori = self._get_arrow_end_orientation(blue_motion)
            r_ori = self._get_arrow_end_orientation(red_motion)

            # normalize to enum
            b_enum = b_ori if isinstance(b_ori, Orientation) else Orientation(b_ori)
            r_enum = r_ori if isinstance(r_ori, Orientation) else Orientation(r_ori)

            in_out = {Orientation.IN, Orientation.OUT}
            clock_counter = {Orientation.CLOCK, Orientation.COUNTER}

            return (b_enum in in_out and r_enum in clock_counter) or (
                b_enum in clock_counter and r_enum in in_out
            )
        except (AttributeError, ValueError):
            return False

    def ends_with_radial_ori(self) -> bool:
        """
        Check if pictograph has radial orientation properties.

        Legacy logic: all props are radial (IN/OUT orientations)
        """
        try:
            # Check if any arrows have valid motion data
            valid_arrows = [
                arrow for arrow in self.pictograph_data.arrows.values() if arrow
            ]
            if not valid_arrows:
                return False

            # Check if all props are radial
            for arrow_data in valid_arrows:
                # Check if motion data exists for this arrow color
                if arrow_data.color not in self.pictograph_data.motions:
                    # No motion data means static arrow - not radial
                    return False

                end_ori = self._get_arrow_end_orientation(
                    self.pictograph_data.motions[arrow_data.color]
                )
                if end_ori not in [Orientation.IN, Orientation.OUT]:
                    return False
            return True
        except (AttributeError, ValueError):
            return False

    def ends_with_nonradial_ori(self) -> bool:
        """
        Check if pictograph has non-radial orientation properties.

        Legacy logic: all props are nonradial (CLOCK/COUNTER orientations)
        """
        try:
            # Check if any arrows have valid motion data
            valid_arrows = [
                arrow for arrow in self.pictograph_data.arrows.values() if arrow
            ]
            if not valid_arrows:
                return False

            # Check if all props are nonradial
            for arrow_data in valid_arrows:
                # Check if motion data exists for this arrow color
                if arrow_data.color not in self.pictograph_data.motions:
                    # No motion data means static arrow - not nonradial
                    return False

                end_ori = self._get_arrow_end_orientation(
                    self.pictograph_data.motions[arrow_data.color]
                )
                if end_ori not in [Orientation.CLOCK, Orientation.COUNTER]:
                    return False
            return True
        except (AttributeError, ValueError):
            return False

    def _get_letters_by_condition(self, condition: LetterCondition) -> list[str]:
        """
        Get letters by condition using exact legacy letter_condition_mappings.

        This replicates the legacy Letter.get_letters_by_condition() method.
        """
        # Legacy letter condition mappings (exact copy from legacy system)
        letter_condition_mappings = {
            LetterCondition.ALPHA_ENDING: [
                "A",
                "B",
                "C",
                "D",
                "E",
                "F",
                "W",
                "X",
                "W-",
                "X-",
                "Φ",
                "Φ-",
                "α",
            ],
            LetterCondition.BETA_ENDING: [
                "G",
                "H",
                "I",
                "J",
                "K",
                "L",
                "Y",
                "Z",
                "Y-",
                "Z-",
                "Ψ",
                "Ψ-",
                "β",
            ],
            LetterCondition.GAMMA_ENDING: [
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
                "Σ",
                "Δ",
                "θ",
                "Ω",
                "Σ-",
                "Δ-",
                "θ-",
                "Ω-",
                "Λ",
                "Λ-",
                "Γ",
            ],
        }

        return letter_condition_mappings.get(condition, [])

    def _get_arrow_end_orientation(self, motion_data: MotionData) -> Orientation:
        """Calculate end orientation for an arrow's motion data."""
        if not motion_data:
            return Orientation.IN  # Default

        # Use the orientation calculator to get end orientation
        if self.orientation_calculator is None:
            from desktop.modern.application.services.positioning.arrows.calculation.orientation_calculator import (
                OrientationCalculator,
            )

            orientation_service = OrientationCalculator()
        else:
            orientation_service = self.orientation_calculator

        start_ori = getattr(motion_data, "start_ori", Orientation.IN)
        if isinstance(start_ori, str):
            start_ori = getattr(Orientation, start_ori.upper(), Orientation.IN)

        end_ori = orientation_service.calculate_end_orientation(motion_data, start_ori)
        return end_ori
