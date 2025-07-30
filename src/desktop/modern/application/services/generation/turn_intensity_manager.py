"""
Turn Intensity Manager - Modern Implementation - FIXED

Handles turn intensity calculations and allocation for sequence generation.
FIXED: Now matches legacy TurnIntensityManager interface exactly.
"""

import random
from typing import List, Tuple, Union

from desktop.modern.core.interfaces.generation_services import ITurnIntensityManager


class TurnIntensityManager:
    """
    FIXED: Turn intensity manager that matches legacy interface exactly.
    
    This implementation matches the legacy TurnIntensityManager constructor
    and method signatures precisely for seamless integration.
    """

    def __init__(self, word_length: int, level: int, max_turn_intensity: float):
        """
        Initialize the TurnIntensityManager with legacy interface.
        FIXED: Matches legacy constructor exactly.
        
        Args:
            word_length: The number of motions (or beats) in the sequence
            level: The level which determines valid turn values (Level 2 or Level 3)
            max_turn_intensity: The maximum number of turns allowed for any single motion
        """
        self.word_length = word_length
        self.level = level
        self.max_turn_intensity = max_turn_intensity
        self.turns_allocated = [0] * word_length
        self.turns_allocated_blue = [0] * word_length
        self.turns_allocated_red = [0] * word_length

    def allocate_turns_for_blue_and_red(self) -> tuple[list[Union[int, float, str]], list[Union[int, float, str]]]:
        """
        FIXED: Exact implementation from legacy TurnIntensityManager.
        
        Returns:
            Tuple of (blue_turns, red_turns) lists with exact legacy logic
        """
        if self.level == 2:
            possible_turns = [0, 1, 2, 3]
        elif self.level == 3:
            possible_turns = [0, 0.5, 1, 1.5, 2, 2.5, 3, "fl"]
        else:
            possible_turns = [0]

        for i in range(self.word_length):
            turn_blue = random.choice(
                [
                    t
                    for t in possible_turns
                    if t == "fl"
                    or (isinstance(t, (int, float)) and t <= self.max_turn_intensity)
                ]
            )
            self.turns_allocated_blue[i] = turn_blue

            turn_red = random.choice(
                [
                    t
                    for t in possible_turns
                    if t == "fl"
                    or (isinstance(t, (int, float)) and t <= self.max_turn_intensity)
                ]
            )
            self.turns_allocated_red[i] = turn_red

        return self.turns_allocated_blue, self.turns_allocated_red


class ModernTurnIntensityManager(ITurnIntensityManager):
    """
    Modern wrapper around legacy TurnIntensityManager for interface compliance.
    
    This provides the modern interface while using the legacy implementation
    internally for compatibility.
    """

    def __init__(self):
        # Modern interface - no constructor parameters
        pass
    
    def calculate_turn_intensity(self, sequence_data: dict, level: int) -> float:
        """Calculate appropriate turn intensity for given sequence and level."""
        if level <= 1:
            return 0.0
        elif level == 2:
            return random.choice([1.0, 2.0, 3.0])
        else:  # level >= 3
            return random.choice([0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
    
    def apply_turn_intensity(self, sequence_data: dict, intensity: float) -> dict:
        """Apply turn intensity to sequence data."""
        return sequence_data
    
    def get_intensity_range(self, level: int) -> Tuple[float, float]:
        """Get valid intensity range for given level."""
        if level <= 1:
            return (0.0, 0.0)
        elif level == 2:
            return (0.0, 3.0)
        else:  # level >= 3
            return (0.0, 3.0)
    
    def validate_intensity(self, intensity: float, level: int) -> bool:
        """Validate if turn intensity is appropriate for given level."""
        min_intensity, max_intensity = self.get_intensity_range(level)
        return min_intensity <= intensity <= max_intensity
    
    def get_recommended_intensity(self, level: int) -> float:
        """Get recommended turn intensity for given level."""
        if level <= 1:
            return 0.0
        elif level == 2:
            return 1.0
        else:  # level >= 3
            return 1.5

    def allocate_turns_for_sequence(
        self,
        length: int,
        level: int,
        max_turn_intensity: float
    ) -> Tuple[List[Union[int, float, str]], List[Union[int, float, str]]]:
        """
        Allocate turns using legacy TurnIntensityManager.
        
        Args:
            length: Number of beats in sequence
            level: Difficulty level (1-6)
            max_turn_intensity: Maximum allowed turn value
            
        Returns:
            Tuple of (blue_turns, red_turns) lists
        """
        # Create legacy turn manager and delegate
        legacy_manager = TurnIntensityManager(length, level, max_turn_intensity)
        return legacy_manager.allocate_turns_for_blue_and_red()
