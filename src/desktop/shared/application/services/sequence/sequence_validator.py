"""
Sequence Validator - Validation Rules and Integrity Checks

Handles all sequence validation operations and business rules.
Extracted from the monolithic sequence management service to focus
solely on validation logic and sequence integrity checks.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors."""


class ISequenceValidator(ABC):
    """Interface for sequence validation operations."""

    @abstractmethod
    def validate_sequence(self, sequence: SequenceData) -> bool:
        """Validate a complete sequence against all rules."""

    @abstractmethod
    def validate_beat(self, beat: BeatData, position: int | None = None) -> bool:
        """Validate a single beat against validation rules."""

    @abstractmethod
    def check_sequence_integrity(self, sequence: SequenceData) -> list[str]:
        """Check sequence integrity and return list of issues."""

    @abstractmethod
    def is_valid_sequence_length(self, length: int) -> bool:
        """Check if sequence length is valid."""

    @abstractmethod
    def validate_sequence_continuity(self, sequence: SequenceData) -> bool:
        """Validate that beats flow correctly in sequence."""


class SequenceValidator(ISequenceValidator):
    """
    Service for validating sequences and beats against business rules.

    Responsibilities:
    - Sequence structure validation
    - Beat data validation
    - Business rule enforcement
    - Integrity checks
    - Performance validation
    """

    def __init__(self):
        # Load validation rules
        self._sequence_validation_rules = self._load_validation_rules()

    def validate_sequence(self, sequence: SequenceData) -> bool:
        """
        Validate a complete sequence against all rules.

        Args:
            sequence: The sequence to validate

        Returns:
            bool: True if valid

        Raises:
            ValidationError: If validation fails
        """
        if not sequence:
            raise ValidationError("Sequence cannot be None")

        logger.debug(f"Validating sequence: {sequence.name}")

        # Validate basic structure
        self._validate_sequence_structure(sequence)

        # Validate sequence metadata
        self._validate_sequence_metadata(sequence)

        # Validate individual beats
        self._validate_beats(sequence.beats)

        # Validate sequence business rules
        self._validate_sequence_business_rules(sequence)

        logger.info(f"Sequence '{sequence.name}' passed all validations")
        return True

    def validate_beat(self, beat: BeatData, position: int | None = None) -> bool:
        """
        Validate a single beat against validation rules.

        Args:
            beat: The beat to validate
            position: Optional position in sequence for context

        Returns:
            bool: True if valid

        Raises:
            ValidationError: If validation fails
        """
        if not beat:
            raise ValidationError("Beat cannot be None")

        logger.debug(f"Validating beat: {beat.letter} at position {position}")

        # Validate beat structure
        self._validate_beat_structure(beat)

        # Validate beat data integrity
        self._validate_beat_data(beat)

        # Validate motion data if present
        if beat.blue_motion or beat.red_motion:
            self._validate_motion_data(beat)

        logger.debug(f"Beat {beat.letter} passed validation")
        return True

    def validate_sequence_name(self, name: str) -> bool:
        """Validate sequence name against naming rules."""
        if not isinstance(name, str):
            raise ValidationError("Sequence name must be a string")

        if not name.strip():
            raise ValidationError("Sequence name cannot be empty")

        max_length = self._sequence_validation_rules.get("max_name_length", 255)
        if len(name) > max_length:
            raise ValidationError(
                f"Sequence name cannot exceed {max_length} characters"
            )

        # Check for invalid characters
        invalid_chars = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]
        if any(char in name for char in invalid_chars):
            raise ValidationError(
                f"Sequence name contains invalid characters: {invalid_chars}"
            )

        return True

    def validate_sequence_length(self, length: int) -> bool:
        """Validate sequence length against limits."""
        if not isinstance(length, int):
            raise ValidationError("Sequence length must be an integer")

        min_length = self._sequence_validation_rules["min_length"]
        max_length = self._sequence_validation_rules["max_length"]

        if length < min_length:
            raise ValidationError(f"Sequence length must be at least {min_length}")

        if length > max_length:
            raise ValidationError(f"Sequence length cannot exceed {max_length}")

        return True

    def validate_beat_position(self, position: int, sequence_length: int) -> bool:
        """Validate beat position within sequence."""
        if not isinstance(position, int):
            raise ValidationError("Position must be an integer")

        if position < 0:
            raise ValidationError("Position cannot be negative")

        if position >= sequence_length:
            raise ValidationError(
                f"Position {position} is beyond sequence length {sequence_length}"
            )

        return True

    def _validate_sequence_structure(self, sequence: SequenceData) -> None:
        """Validate basic sequence structure."""
        required_fields = self._sequence_validation_rules["required_fields"]

        for field in required_fields:
            if not hasattr(sequence, field):
                raise ValidationError(f"Sequence missing required field: {field}")

        # Validate sequence length constraints
        self.validate_sequence_length(len(sequence.beats))

    def _validate_sequence_metadata(self, sequence: SequenceData) -> None:
        """Validate sequence metadata."""
        # Validate name
        self.validate_sequence_name(sequence.name)

        # Validate ID format (basic check)
        if not sequence.id or not isinstance(sequence.id, str):
            raise ValidationError("Sequence must have a valid ID")

    def _validate_beats(self, beats: list[BeatData]) -> None:
        """Validate all beats in a sequence."""
        if not isinstance(beats, list):
            raise ValidationError("Beats must be a list")

        # Validate beat numbering
        for i, beat in enumerate(beats):
            expected_number = i + 1
            if beat.beat_number != expected_number:
                raise ValidationError(
                    f"Beat {i} has incorrect beat_number: {beat.beat_number}, expected {expected_number}"
                )

            # Validate individual beat
            self.validate_beat(beat, i)

    def _validate_beat_structure(self, beat: BeatData) -> None:
        """Validate basic beat structure."""
        if not isinstance(beat.beat_number, int) or beat.beat_number < 0:
            raise ValidationError("Beat number must be a non-negative integer")

        if beat.duration is not None and (
            not isinstance(beat.duration, (int, float)) or beat.duration <= 0
        ):
            raise ValidationError("Beat duration must be a positive number")

    def _validate_beat_data(self, beat: BeatData) -> None:
        """Validate beat data integrity."""
        # Validate letter (can be empty for placeholder beats)
        if beat.letter is not None and not isinstance(beat.letter, str):
            raise ValidationError("Beat letter must be a string or None")

        # Validate boolean flags
        if not isinstance(beat.is_blank, bool):
            raise ValidationError("Beat is_blank must be a boolean")

    def _validate_motion_data(self, beat: BeatData) -> None:
        """Validate motion data if present."""
        if beat.blue_motion:
            self._validate_single_motion(beat.blue_motion, "blue", beat.beat_number)

        if beat.red_motion:
            self._validate_single_motion(beat.red_motion, "red", beat.beat_number)

    def _validate_single_motion(self, motion, color: str, beat_number: int) -> None:
        """Validate a single motion data object."""
        # This would validate the motion data structure
        # The actual validation would depend on the MotionData model structure
        logger.debug(f"Validating {color} motion for beat {beat_number}")

        # Basic validation - check if motion has required attributes
        if not hasattr(motion, "motion_type"):
            raise ValidationError(
                f"Motion data missing motion_type for {color} motion in beat {beat_number}"
            )

    def _validate_sequence_business_rules(self, sequence: SequenceData) -> None:
        """Validate sequence against business rules."""
        # Check for duplicate beat numbers
        beat_numbers = [beat.beat_number for beat in sequence.beats]
        if len(beat_numbers) != len(set(beat_numbers)):
            raise ValidationError("Sequence contains duplicate beat numbers")

        # Validate start position if present
        start_position_beats = [
            beat for beat in sequence.beats if beat.beat_number == 0
        ]
        if len(start_position_beats) > 1:
            raise ValidationError("Sequence cannot have multiple start positions")

        # Validate sequence continuity (beat numbers should be sequential)
        regular_beats = [beat for beat in sequence.beats if beat.beat_number > 0]
        if regular_beats:
            expected_numbers = list(range(1, len(regular_beats) + 1))
            actual_numbers = sorted([beat.beat_number for beat in regular_beats])
            if actual_numbers != expected_numbers:
                raise ValidationError(
                    f"Beat numbers are not sequential: {actual_numbers}"
                )

    def _load_validation_rules(self) -> dict[str, Any]:
        """Load sequence validation rules."""
        return {
            "max_length": 64,
            "min_length": 1,
            "max_name_length": 255,
            "required_fields": ["name", "beats", "id"],
            "allowed_beat_letters": None,  # None means all letters allowed
            "require_start_position": False,
            "allow_empty_beats": True,
            "max_turns_per_beat": 16,
        }

    def get_validation_rules(self) -> dict[str, Any]:
        """Get current validation rules."""
        return self._sequence_validation_rules.copy()

    def update_validation_rules(self, new_rules: dict[str, Any]) -> None:
        """Update validation rules (for testing or configuration)."""
        self._sequence_validation_rules.update(new_rules)
        logger.info("Validation rules updated")

    def is_valid_sequence(self, sequence: SequenceData) -> bool:
        """
        Check if sequence is valid without raising exceptions.

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            self.validate_sequence(sequence)
            return True
        except ValidationError:
            return False

    def is_valid_beat(self, beat: BeatData) -> bool:
        """
        Check if beat is valid without raising exceptions.

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            self.validate_beat(beat)
            return True
        except ValidationError:
            return False

    def get_validation_errors(self, sequence: SequenceData) -> list[str]:
        """
        Get list of validation errors for a sequence.

        Returns:
            List of error messages, empty if valid
        """
        errors = []

        try:
            self.validate_sequence(sequence)
        except ValidationError as e:
            errors.append(str(e))

        return errors

    def check_sequence_integrity(self, sequence: SequenceData) -> list[str]:
        """
        Check sequence integrity and return list of issues.

        Args:
            sequence: The sequence to check

        Returns:
            List of integrity issues, empty if intact
        """
        issues = []

        # Check for missing required fields
        required_fields = self._sequence_validation_rules["required_fields"]
        for field in required_fields:
            if not hasattr(sequence, field):
                issues.append(f"Missing required field: {field}")

        # Check for duplicate beat numbers
        beat_numbers = [beat.beat_number for beat in sequence.beats]
        if len(beat_numbers) != len(set(beat_numbers)):
            issues.append("Duplicate beat numbers found")

        # Check sequence continuity (beat numbers should be sequential)
        regular_beats = [beat for beat in sequence.beats if beat.beat_number > 0]
        if regular_beats:
            expected_numbers = list(range(1, len(regular_beats) + 1))
            actual_numbers = sorted([beat.beat_number for beat in regular_beats])
            if actual_numbers != expected_numbers:
                issues.append("Beat numbers are not sequential")

        return issues

    def is_valid_sequence_length(self, length: int) -> bool:
        """
        Check if sequence length is valid.

        Args:
            length: The length to check

        Returns:
            bool: True if valid
        """
        if not isinstance(length, int):
            return False

        min_length = self._sequence_validation_rules["min_length"]
        max_length = self._sequence_validation_rules["max_length"]

        return min_length <= length <= max_length
