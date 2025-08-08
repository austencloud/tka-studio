"""
SequenceWordCalculator - Focused Service for Word Calculation

Single Responsibility: Calculating sequence words from beat letters.
Extracted from SequenceBeatOperations God Object.
"""

from __future__ import annotations

from desktop.modern.domain.models.sequence_data import SequenceData


class SequenceWordCalculator:
    """
    Service focused solely on sequence word calculation.

    Responsibilities:
    - Calculating sequence words from beat letters
    - Simplifying repeated patterns in words
    - Managing word transformation logic
    """

    def calculate_word(self, sequence: SequenceData) -> str:
        """
        Calculate sequence word from beat letters exactly like legacy.

        Args:
            sequence: The sequence to calculate word for

        Returns:
            The calculated sequence word
        """
        if not sequence or not sequence.beats:
            return ""

        # Extract letters from beats exactly like legacy calculate_word method
        word = "".join(beat.letter for beat in sequence.beats)

        # Apply word simplification for circular sequences like legacy
        return self.simplify_repeated_word(word)

    def simplify_repeated_word(self, word: str) -> str:
        """
        Simplify repeated patterns exactly like legacy WordSimplifier.

        Args:
            word: The word to simplify

        Returns:
            Simplified word with repeated patterns reduced
        """
        if not word:
            return word

        def can_form_by_repeating(s: str, pattern: str) -> bool:
            """Check if string can be formed by repeating a pattern."""
            pattern_len = len(pattern)
            return all(
                s[i : i + pattern_len] == pattern for i in range(0, len(s), pattern_len)
            )

        n = len(word)

        # Try each possible pattern length from smallest to largest
        for i in range(1, n // 2 + 1):
            pattern = word[:i]
            if n % i == 0 and can_form_by_repeating(word, pattern):
                return pattern

        return word

    def extract_letters_from_sequence(self, sequence: SequenceData) -> str:
        """
        Extract just the letter sequence without simplification.

        Args:
            sequence: The sequence to extract letters from

        Returns:
            Raw letter sequence
        """
        if not sequence or not sequence.beats:
            return ""

        return "".join(beat.letter for beat in sequence.beats)
