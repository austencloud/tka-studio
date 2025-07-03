"""
Turn Intensity Manager - Modern Implementation

Direct port of turn allocation algorithm from legacy TurnIntensityManager.
Handles turn allocation for sequence generation based on level and intensity.
"""

import random
from typing import List, Union, Tuple


class TurnIntensityManager:
    """
    Manages turn allocation for sequence generation.
    
    Direct port from legacy turn_intensity_manager.py
    """
    
    def __init__(self, word_length: int, level: int, max_turn_intensity: float):
        """
        Initialize the TurnIntensityManager.
        
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

    def allocate_turns_for_blue_and_red(self) -> Tuple[List[Union[int, float, str]], List[Union[int, float, str]]]:
        """
        Allocate turns for blue and red based on level and intensity.
        
        Direct port from legacy allocate_turns_for_blue_and_red method.
        
        Returns:
            Tuple of (blue_turns_list, red_turns_list)
        """
        # Determine possible turns based on level (exact logic from legacy)
        if self.level == 2:
            possible_turns = [0, 1, 2, 3]
        elif self.level == 3:
            possible_turns = [0, 0.5, 1, 1.5, 2, 2.5, 3, "fl"]
        else:
            possible_turns = [0]

        # Allocate turns for each beat
        for i in range(self.word_length):
            # Blue turn allocation
            turn_blue = random.choice([
                t for t in possible_turns
                if t == "fl" or (isinstance(t, (int, float)) and t <= self.max_turn_intensity)
            ])
            self.turns_allocated_blue[i] = turn_blue

            # Red turn allocation  
            turn_red = random.choice([
                t for t in possible_turns
                if t == "fl" or (isinstance(t, (int, float)) and t <= self.max_turn_intensity)
            ])
            self.turns_allocated_red[i] = turn_red

        return self.turns_allocated_blue, self.turns_allocated_red


class TurnIntensityManagerFactory:
    """Factory for creating TurnIntensityManager instances."""
    
    @staticmethod
    def create_for_generation(length: int, level: int, turn_intensity: float) -> TurnIntensityManager:
        """Create TurnIntensityManager for generation with given parameters."""
        return TurnIntensityManager(
            word_length=length,
            level=level, 
            max_turn_intensity=turn_intensity
        )
    
    @staticmethod
    def allocate_turns_for_blue_and_red(length: int, level: int, turn_intensity: float) -> Tuple[List[Union[int, float, str]], List[Union[int, float, str]]]:
        """
        Convenience method to allocate turns without creating manager instance.
        
        This matches the interface expected by the generation services.
        """
        manager = TurnIntensityManagerFactory.create_for_generation(length, level, turn_intensity)
        return manager.allocate_turns_for_blue_and_red()
