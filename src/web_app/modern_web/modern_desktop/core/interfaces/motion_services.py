"""
Motion Service Interfaces

Interface definitions for motion services following TKA's clean architecture.
These interfaces define contracts for motion calculation and management operations
that must behave identically across desktop and web platforms.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from desktop.modern.domain.models.enums import MotionType, Orientation
from desktop.modern.domain.models.motion_data import MotionData


class IOrientationCalculator(ABC):
    """Interface for motion orientation calculation operations."""

    @abstractmethod
    def calculate_motion_orientation(
        self, motion: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> Orientation:
        """
        Calculate end orientation for a motion.

        Args:
            motion: Motion data containing motion information
            start_orientation: Starting orientation (default: IN)

        Returns:
            Calculated end orientation

        Note:
            Web implementation: Same mathematical logic, different coordinate systems
        """

    @abstractmethod
    def flip_orientation(self, orientation: Orientation) -> Orientation:
        """
        Flip orientation between IN and OUT.

        Args:
            orientation: Orientation to flip

        Returns:
            Flipped orientation

        Note:
            Web implementation: Identical logic across platforms
        """

    @abstractmethod
    def calculate_orientation_for_motion_type(
        self,
        motion_type: MotionType,
        turns: int | float,
        start_orientation: Orientation,
    ) -> Orientation:
        """
        Calculate orientation for specific motion type and turn count.

        Args:
            motion_type: Type of motion
            turns: Number of turns (can be fractional)
            start_orientation: Starting orientation

        Returns:
            Calculated end orientation

        Note:
            Web implementation: Core business logic must be identical
        """

    @abstractmethod
    def get_orientation_flip_rules(self) -> dict[str, Any]:
        """
        Get orientation flip rules configuration.

        Returns:
            Dictionary containing orientation flip rules

        Note:
            Web implementation: Rules loaded from JSON or constants
        """

    @abstractmethod
    def validate_orientation_transition(
        self,
        start_orientation: Orientation,
        end_orientation: Orientation,
        motion: MotionData,
    ) -> bool:
        """
        Validate if an orientation transition is valid for given motion.

        Args:
            start_orientation: Starting orientation
            end_orientation: Ending orientation
            motion: Motion data

        Returns:
            True if transition is valid, False otherwise

        Note:
            Web implementation: Same validation logic, may use different error handling
        """


class ITurnIntensityManager(ABC):
    """Interface for turn intensity management operations."""

    @abstractmethod
    def allocate_turns_for_blue_and_red(
        self,
    ) -> tuple[list[int | float | str], list[int | float | str]]:
        """
        Allocate turns for blue and red based on level and intensity.

        Returns:
            Tuple of (blue_turns_list, red_turns_list)

        Note:
            Web implementation: Uses same random generation logic with web-compatible RNG
        """

    @abstractmethod
    def get_possible_turns_for_level(self, level: int) -> list[int | float | str]:
        """
        Get possible turn values for a given level.

        Args:
            level: Difficulty level (2 or 3)

        Returns:
            List of possible turn values for the level

        Note:
            Web implementation: Same turn values, may be stored as constants
        """

    @abstractmethod
    def validate_turn_intensity(
        self, turn_value: int | float | str, max_intensity: float
    ) -> bool:
        """
        Validate if a turn value is within the maximum intensity limit.

        Args:
            turn_value: Turn value to validate
            max_intensity: Maximum allowed intensity

        Returns:
            True if valid, False otherwise

        Note:
            Web implementation: Same validation logic across platforms
        """

    @abstractmethod
    def get_turn_distribution_stats(self) -> dict[str, Any]:
        """
        Get statistics about turn distribution in current allocation.

        Returns:
            Dictionary with turn distribution statistics

        Note:
            Web implementation: Same statistical calculations
        """

    @abstractmethod
    def reset_turn_allocation(self) -> None:
        """
        Reset turn allocation to initial state.

        Note:
            Web implementation: Clears allocated turns arrays
        """

    @abstractmethod
    def get_word_length(self) -> int:
        """
        Get the word length for current allocation.

        Returns:
            Number of beats/motions in the sequence
        """

    @abstractmethod
    def get_level(self) -> int:
        """
        Get the difficulty level for current allocation.

        Returns:
            Difficulty level (2 or 3)
        """

    @abstractmethod
    def get_max_turn_intensity(self) -> float:
        """
        Get the maximum turn intensity for current allocation.

        Returns:
            Maximum turn intensity value
        """


class ITurnIntensityManagerFactory(ABC):
    """Interface for turn intensity manager factory operations."""

    @abstractmethod
    def create_for_generation(
        self, length: int, level: int, turn_intensity: float
    ) -> ITurnIntensityManager:
        """
        Create TurnIntensityManager for generation with given parameters.

        Args:
            length: Sequence length
            level: Difficulty level
            turn_intensity: Maximum turn intensity

        Returns:
            ITurnIntensityManager instance

        Note:
            Web implementation: Creates web-compatible manager instance
        """

    @abstractmethod
    def allocate_turns_for_blue_and_red(
        self, length: int, level: int, turn_intensity: float
    ) -> tuple[list[int | float | str], list[int | float | str]]:
        """
        Convenience method to allocate turns without creating manager instance.

        Args:
            length: Sequence length
            level: Difficulty level
            turn_intensity: Maximum turn intensity

        Returns:
            Tuple of (blue_turns_list, red_turns_list)

        Note:
            Web implementation: Same interface for generation services
        """

    @abstractmethod
    def get_default_parameters(self) -> dict[str, Any]:
        """
        Get default parameters for turn intensity management.

        Returns:
            Dictionary with default parameters

        Note:
            Web implementation: May be stored as configuration constants
        """

    @abstractmethod
    def validate_generation_parameters(
        self, length: int, level: int, turn_intensity: float
    ) -> bool:
        """
        Validate parameters for turn intensity generation.

        Args:
            length: Sequence length
            level: Difficulty level
            turn_intensity: Maximum turn intensity

        Returns:
            True if parameters are valid, False otherwise

        Note:
            Web implementation: Same validation logic across platforms
        """
