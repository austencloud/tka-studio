"""
Interface definitions for validation services in TKA.

These interfaces define contracts for validation operations across the application,
supporting pictograph validation, beat validation, and sequence validation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from desktop.modern.domain.models.motion_data import MotionData


class IPictographValidator(ABC):
    """Interface for pictograph validation and condition checking operations."""

    @abstractmethod
    def validate_dependencies(self) -> bool:
        """
        Validate that all required dependencies are available.

        Returns:
            bool: True if all dependencies are valid, False otherwise
        """

    @abstractmethod
    def ends_with_beta(self) -> bool:
        """
        Check if pictograph ends with beta position.

        Returns:
            bool: True if pictograph ends in beta position, False otherwise
        """

    @abstractmethod
    def ends_with_alpha(self) -> bool:
        """
        Check if pictograph ends with alpha position.

        Returns:
            bool: True if pictograph ends in alpha position, False otherwise
        """

    @abstractmethod
    def ends_with_gamma(self) -> bool:
        """
        Check if pictograph ends with gamma position.

        Returns:
            bool: True if pictograph ends in gamma position, False otherwise
        """

    @abstractmethod
    def ends_with_layer3(self) -> bool:
        """
        Check if pictograph ends with layer3 configuration.

        Returns:
            bool: True if pictograph ends in layer3, False otherwise
        """

    @abstractmethod
    def ends_with_radial_ori(self) -> bool:
        """
        Check if pictograph has radial orientation properties.

        Returns:
            bool: True if all props are radial (IN/OUT orientations), False otherwise
        """

    @abstractmethod
    def ends_with_layer1(self) -> bool:
        """
        Check if pictograph ends with layer1 configuration.

        Returns:
            bool: True if all props have same radial/nonradial orientation, False otherwise
        """

    @abstractmethod
    def ends_with_layer2(self) -> bool:
        """
        Check if pictograph ends with layer2 configuration.

        Returns:
            bool: True if all props are nonradial, False otherwise
        """

    @abstractmethod
    def ends_with_nonradial_ori(self) -> bool:
        """
        Check if pictograph has non-radial orientation properties.

        Returns:
            bool: True if all props are nonradial (CLOCK/COUNTER orientations), False otherwise
        """


class ISequenceValidator(ABC):
    """Interface for sequence-level validation operations."""

    @abstractmethod
    def validate_sequence_continuity(self, sequence_data) -> bool:
        """
        Validate that sequence beats flow continuously.

        Args:
            sequence_data: The sequence to validate

        Returns:
            bool: True if sequence is continuous, False otherwise
        """

    @abstractmethod
    def validate_sequence_letters(self, sequence_data) -> list[str]:
        """
        Validate sequence letter combinations and return any issues.

        Args:
            sequence_data: The sequence to validate

        Returns:
            List[str]: List of validation issues (empty if valid)
        """

    @abstractmethod
    def is_valid_sequence_length(self, length: int) -> bool:
        """
        Check if sequence length is valid.

        Args:
            length: The sequence length to check

        Returns:
            bool: True if length is valid, False otherwise
        """


class IBeatValidator(ABC):
    """Interface for individual beat validation operations."""

    @abstractmethod
    def validate_beat_data(self, beat_data) -> list[str]:
        """
        Validate individual beat data and return any issues.

        Args:
            beat_data: The beat data to validate

        Returns:
            List[str]: List of validation issues (empty if valid)
        """

    @abstractmethod
    def validate_motion_data(self, motion_data: MotionData) -> bool:
        """
        Validate motion data for a beat.

        Args:
            motion_data: The motion data to validate

        Returns:
            bool: True if motion data is valid, False otherwise
        """

    @abstractmethod
    def check_beat_transitions(self, previous_beat, current_beat) -> bool:
        """
        Check if transition between beats is valid.

        Args:
            previous_beat: The previous beat in sequence
            current_beat: The current beat to check

        Returns:
            bool: True if transition is valid, False otherwise
        """
