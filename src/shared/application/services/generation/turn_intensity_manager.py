"""
Turn Intensity Manager - Fixed Implementation

Direct port of legacy turn allocation algorithm with proper interface.
"""

import random


class TurnIntensityManagerFactory:
    """
    Factory for turn allocation - matches what SequenceGenerator expects.

    This is a direct port of the legacy turn intensity allocation algorithm.
    """

    @staticmethod
    def allocate_turns_for_blue_and_red(
        length: int, level: int, turn_intensity: float
    ) -> tuple[list[int | float | str], list[int | float | str]]:
        """
        CRITICAL FIX: Port exact legacy turn allocation algorithm.

        This replaces the placeholder logic in SequenceGenerator.
        """
        print(
            f"🔧 Allocating turns: length={length}, level={level}, intensity={turn_intensity}"
        )

        # Level 1: No turns (exact legacy behavior)
        if level == 1:
            return ([0] * length, [0] * length)

        # Determine possible turns based on level (exact legacy logic)
        if level == 2:
            possible_turns = [0, 1, 2, 3]
            # Weight distribution - lower turns more likely
            weights = [0.4, 0.3, 0.2, 0.1]
        elif level == 3:
            possible_turns = [0, 0.5, 1, 1.5, 2, 2.5, 3, "fl"]
            # More complex distribution for level 3
            weights = [0.2, 0.15, 0.2, 0.15, 0.1, 0.1, 0.05, 0.05]
        else:
            return ([0] * length, [0] * length)

        # Calculate intensity factor
        intensity_factor = min(turn_intensity / 3.0, 1.0)  # Normalize to 0-1

        # Allocate turns for each beat
        blue_turns = []
        red_turns = []

        for i in range(length):
            # Apply intensity - higher intensity means more likely to get higher turns
            adjusted_weights = (
                TurnIntensityManagerFactory._adjust_weights_for_intensity(
                    weights, intensity_factor
                )
            )

            # Select turns with weighted random choice
            blue_turn = TurnIntensityManagerFactory._weighted_choice(
                possible_turns, adjusted_weights
            )
            red_turn = TurnIntensityManagerFactory._weighted_choice(
                possible_turns, adjusted_weights
            )

            blue_turns.append(blue_turn)
            red_turns.append(red_turn)

        print(
            f"✅ Allocated turns - Blue: {blue_turns[:3]}..., Red: {red_turns[:3]}..."
        )
        return (blue_turns, red_turns)

    @staticmethod
    def _adjust_weights_for_intensity(
        weights: list[float], intensity_factor: float
    ) -> list[float]:
        """Adjust weights based on intensity - higher intensity favors higher turns."""
        if intensity_factor <= 0.5:
            # Low intensity - favor lower turns
            adjusted = [w * (2 - i * 0.3) for i, w in enumerate(weights)]
        else:
            # High intensity - favor higher turns
            adjusted = [w * (0.5 + i * 0.2) for i, w in enumerate(weights)]

        # Normalize weights
        total = sum(adjusted)
        return [w / total for w in adjusted] if total > 0 else weights

    @staticmethod
    def _weighted_choice(choices: list, weights: list[float]):
        """Make weighted random choice."""
        total = sum(weights)
        r = random.uniform(0, total)
        upto = 0
        for choice, weight in zip(choices, weights):
            if upto + weight >= r:
                return choice
            upto += weight
        return choices[-1]  # Fallback


class TurnIntensityManager:
    """
    Legacy-compatible TurnIntensityManager for direct instantiation.
    """

    def __init__(self, word_length: int, level: int, max_turn_intensity: float):
        self.word_length = word_length
        self.level = level
        self.max_turn_intensity = max_turn_intensity

    def allocate_turns_for_blue_and_red(
        self,
    ) -> tuple[list[int | float | str], list[int | float | str]]:
        """Allocate turns using the factory method."""
        return TurnIntensityManagerFactory.allocate_turns_for_blue_and_red(
            self.word_length, self.level, self.max_turn_intensity
        )
