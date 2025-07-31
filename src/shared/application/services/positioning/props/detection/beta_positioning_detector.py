"""
Beta Positioning Detector Service

Pure service for detecting when beta positioning should be applied.
Extracted from PropManagementService to follow single responsibility principle.

PROVIDES:
- Beta-ending letter detection
- Beta positioning condition evaluation
- Clean separation of detection logic
"""

from abc import ABC, abstractmethod

from desktop.modern.domain.models import BeatData


class IBetaPositioningDetector(ABC):
    """Interface for beta positioning detection operations."""

    @abstractmethod
    def should_apply_beta_positioning(self, beat_data: BeatData) -> bool:
        """Determine if beta positioning should be applied."""

    @abstractmethod
    def is_beta_ending_letter(self, letter: str) -> bool:
        """Check if letter ends at beta positions."""

    @abstractmethod
    def get_beta_ending_letters(self) -> list[str]:
        """Get list of letters that end at beta positions."""


class BetaPositioningDetector(IBetaPositioningDetector):
    """
    Pure service for beta positioning detection.

    Handles detection of when beta positioning should be applied
    based on letter types and positioning requirements.
    """

    def __init__(self):
        """Initialize with beta-ending letter constants."""
        self._beta_ending_letters = [
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
        ]

    def should_apply_beta_positioning(self, beat_data: BeatData) -> bool:
        """
        Determine if beta positioning should be applied.

        Beta positioning is applied when:
        1. Letter is one that ends at beta positions (G, H, I, J, K, L, Y, Z, Y-, Z-, Ψ, Ψ-, β)
        2. Beat data is valid and contains letter information
        """
        if not beat_data or not beat_data.letter:
            return False

        return self.is_beta_ending_letter(beat_data.letter)

    def is_beta_ending_letter(self, letter: str) -> bool:
        """Check if letter ends at beta positions."""
        if not letter:
            return False

        return letter in self._beta_ending_letters

    def get_beta_ending_letters(self) -> list[str]:
        """Get list of letters that end at beta positions."""
        return self._beta_ending_letters.copy()
