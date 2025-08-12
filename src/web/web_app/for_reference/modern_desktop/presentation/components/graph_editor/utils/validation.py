#!/usr/bin/env python3
"""
Graph Editor Validation Utilities
=================================

Provides comprehensive input validation for graph editor components
following TKA architectural patterns and error handling best practices.
"""

from __future__ import annotations

from dataclasses import dataclass
import logging
from pathlib import Path

# Import domain models for validation
import sys
from typing import Any


modern_src = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(modern_src))

from desktop.modern.domain.models import BeatData, Orientation, SequenceData


logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors with context."""

    def __init__(
        self,
        message: str,
        field: str = None,
        value: Any = None,
        context: dict[str, Any] = None,
    ):
        self.message = message
        self.field = field
        self.value = value
        self.context = context or {}
        super().__init__(self.message)

    def __str__(self):
        parts = [self.message]
        if self.field:
            parts.append(f"Field: {self.field}")
        if self.value is not None:
            parts.append(f"Value: {self.value}")
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            parts.append(f"Context: {context_str}")
        return " | ".join(parts)


@dataclass
class ValidationResult:
    """Result of a validation operation."""

    is_valid: bool
    errors: list[ValidationError]
    warnings: list[str]

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0

    def add_error(
        self,
        message: str,
        field: str = None,
        value: Any = None,
        context: dict[str, Any] = None,
    ):
        """Add a validation error."""
        error = ValidationError(message, field, value, context)
        self.errors.append(error)
        self.is_valid = False

    def add_warning(self, message: str):
        """Add a validation warning."""
        self.warnings.append(message)


class GraphEditorValidator:
    """
    Comprehensive validator for graph editor components.

    Provides validation methods for all data types used in the graph editor
    with detailed error reporting and context information.
    """

    @staticmethod
    def validate_beat_data(
        beat_data: BeatData | None,
        allow_none: bool = True,
        context: dict[str, Any] = None,
    ) -> ValidationResult:
        """
        Validate beat data with comprehensive checks.

        Args:
            beat_data: Beat data to validate (can be None if allow_none=True)
            allow_none: Whether None values are acceptable
            context: Additional context for error reporting

        Returns:
            ValidationResult with detailed validation information
        """
        result = ValidationResult(is_valid=True, errors=[], warnings=[])
        ctx = context or {}

        # Check None handling
        if beat_data is None:
            if not allow_none:
                result.add_error("Beat data cannot be None", "beat_data", None, ctx)
            return result

        # Validate beat data structure
        try:
            # Check required attributes
            if not hasattr(beat_data, "beat_number"):
                result.add_error(
                    "Beat data missing beat_number attribute", "beat_number", None, ctx
                )
            elif not isinstance(beat_data.beat_number, int):
                result.add_error(
                    "Beat number must be an integer",
                    "beat_number",
                    beat_data.beat_number,
                    ctx,
                )
            elif beat_data.beat_number < 1:
                result.add_error(
                    "Beat number must be positive",
                    "beat_number",
                    beat_data.beat_number,
                    ctx,
                )

            if not hasattr(beat_data, "letter"):
                result.add_error(
                    "Beat data missing letter attribute", "letter", None, ctx
                )
            elif not isinstance(beat_data.letter, str):
                result.add_error(
                    "Beat letter must be a string", "letter", beat_data.letter, ctx
                )
            elif not beat_data.letter:
                result.add_error(
                    "Beat letter cannot be empty", "letter", beat_data.letter, ctx
                )

            if not hasattr(beat_data, "duration"):
                result.add_error(
                    "Beat data missing duration attribute", "duration", None, ctx
                )
            elif not isinstance(beat_data.duration, (int, float)):
                result.add_error(
                    "Beat duration must be a number",
                    "duration",
                    beat_data.duration,
                    ctx,
                )
            elif beat_data.duration <= 0:
                result.add_error(
                    "Beat duration must be positive",
                    "duration",
                    beat_data.duration,
                    ctx,
                )

            # Validate motion data if present
            if hasattr(beat_data, "blue_motion") and beat_data.blue_motion is not None:
                motion_result = GraphEditorValidator._validate_motion_data(
                    beat_data.blue_motion, "blue_motion", ctx
                )
                result.errors.extend(motion_result.errors)
                result.warnings.extend(motion_result.warnings)
                if motion_result.has_errors:
                    result.is_valid = False

            if hasattr(beat_data, "red_motion") and beat_data.red_motion is not None:
                motion_result = GraphEditorValidator._validate_motion_data(
                    beat_data.red_motion, "red_motion", ctx
                )
                result.errors.extend(motion_result.errors)
                result.warnings.extend(motion_result.warnings)
                if motion_result.has_errors:
                    result.is_valid = False

            # Check for at least one motion
            if (
                not hasattr(beat_data, "blue_motion") or beat_data.blue_motion is None
            ) and (
                not hasattr(beat_data, "red_motion") or beat_data.red_motion is None
            ):
                result.add_warning("Beat has no motion data (blue or red)")

        except Exception as e:
            result.add_error(
                f"Unexpected error validating beat data: {e!s}",
                "beat_data",
                beat_data,
                ctx,
            )

        return result

    @staticmethod
    def _validate_motion_data(
        motion_data: Any, field_name: str, context: dict[str, Any]
    ) -> ValidationResult:
        """Validate motion data structure."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        try:
            # Check required motion attributes
            if not hasattr(motion_data, "motion_type"):
                result.add_error(
                    "Motion data missing motion_type",
                    f"{field_name}.motion_type",
                    None,
                    context,
                )

            if not hasattr(motion_data, "turns"):
                result.add_error(
                    "Motion data missing turns", f"{field_name}.turns", None, context
                )
            elif not isinstance(motion_data.turns, (int, float)):
                result.add_error(
                    "Motion turns must be a number",
                    f"{field_name}.turns",
                    motion_data.turns,
                    context,
                )
            elif motion_data.turns < 0:
                result.add_error(
                    "Motion turns cannot be negative",
                    f"{field_name}.turns",
                    motion_data.turns,
                    context,
                )

        except Exception as e:
            result.add_error(
                f"Error validating motion data: {e!s}",
                field_name,
                motion_data,
                context,
            )

        return result

    @staticmethod
    def validate_sequence_data(
        sequence_data: SequenceData | None,
        allow_none: bool = True,
        context: dict[str, Any] = None,
    ) -> ValidationResult:
        """
        Validate sequence data with comprehensive checks.

        Args:
            sequence_data: Sequence data to validate
            allow_none: Whether None values are acceptable
            context: Additional context for error reporting

        Returns:
            ValidationResult with detailed validation information
        """
        result = ValidationResult(is_valid=True, errors=[], warnings=[])
        ctx = context or {}

        # Check None handling
        if sequence_data is None:
            if not allow_none:
                result.add_error(
                    "Sequence data cannot be None", "sequence_data", None, ctx
                )
            return result

        try:
            # Validate sequence structure
            if not hasattr(sequence_data, "name"):
                result.add_error(
                    "Sequence data missing name attribute", "name", None, ctx
                )
            elif not isinstance(sequence_data.name, str):
                result.add_error(
                    "Sequence name must be a string", "name", sequence_data.name, ctx
                )
            elif not sequence_data.name.strip():
                result.add_error(
                    "Sequence name cannot be empty", "name", sequence_data.name, ctx
                )

            if not hasattr(sequence_data, "word"):
                result.add_error(
                    "Sequence data missing word attribute", "word", None, ctx
                )
            elif not isinstance(sequence_data.word, str):
                result.add_error(
                    "Sequence word must be a string", "word", sequence_data.word, ctx
                )

            if not hasattr(sequence_data, "beats"):
                result.add_error(
                    "Sequence data missing beats attribute", "beats", None, ctx
                )
            elif not isinstance(sequence_data.beats, list):
                result.add_error(
                    "Sequence beats must be a list",
                    "beats",
                    type(sequence_data.beats),
                    ctx,
                )
            else:
                # Validate each beat in the sequence
                for i, beat in enumerate(sequence_data.beats):
                    beat_context = {**ctx, "sequence_beat_index": i}
                    beat_result = GraphEditorValidator.validate_beat_data(
                        beat, allow_none=False, context=beat_context
                    )
                    result.errors.extend(beat_result.errors)
                    result.warnings.extend(beat_result.warnings)
                    if beat_result.has_errors:
                        result.is_valid = False

                # Check for empty sequence
                if len(sequence_data.beats) == 0:
                    result.add_warning("Sequence has no beats")

        except Exception as e:
            result.add_error(
                f"Unexpected error validating sequence data: {e!s}",
                "sequence_data",
                sequence_data,
                ctx,
            )

        return result

    @staticmethod
    def validate_beat_index(
        beat_index: int,
        sequence_length: int = None,
        allow_negative: bool = True,
        context: dict[str, Any] = None,
    ) -> ValidationResult:
        """
        Validate beat index with bounds checking.

        Args:
            beat_index: Index to validate
            sequence_length: Length of sequence for bounds checking
            allow_negative: Whether negative indices are allowed (e.g., -1 for start position)
            context: Additional context for error reporting

        Returns:
            ValidationResult with detailed validation information
        """
        result = ValidationResult(is_valid=True, errors=[], warnings=[])
        ctx = context or {}

        try:
            # Check type
            if not isinstance(beat_index, int):
                result.add_error(
                    "Beat index must be an integer", "beat_index", beat_index, ctx
                )
                return result

            # Check negative values
            if beat_index < 0 and not allow_negative:
                result.add_error(
                    "Beat index cannot be negative", "beat_index", beat_index, ctx
                )
            elif beat_index < -1 and allow_negative:
                result.add_error(
                    "Beat index cannot be less than -1", "beat_index", beat_index, ctx
                )

            # Check bounds if sequence length provided
            if sequence_length is not None:
                if beat_index >= sequence_length > 0:
                    result.add_error(
                        f"Beat index {beat_index} exceeds sequence length {sequence_length}",
                        "beat_index",
                        beat_index,
                        {**ctx, "sequence_length": sequence_length},
                    )
                elif beat_index > 0 and sequence_length == 0:
                    result.add_error(
                        "Cannot have positive beat index with empty sequence",
                        "beat_index",
                        beat_index,
                        {**ctx, "sequence_length": sequence_length},
                    )

        except Exception as e:
            result.add_error(
                f"Error validating beat index: {e!s}", "beat_index", beat_index, ctx
            )

        return result

    @staticmethod
    def validate_arrow_id(
        arrow_id: str | None, allow_none: bool = True, context: dict[str, Any] = None
    ) -> ValidationResult:
        """
        Validate arrow ID.

        Args:
            arrow_id: Arrow ID to validate
            allow_none: Whether None values are acceptable
            context: Additional context for error reporting

        Returns:
            ValidationResult with detailed validation information
        """
        result = ValidationResult(is_valid=True, errors=[], warnings=[])
        ctx = context or {}

        # Check None handling
        if arrow_id is None:
            if not allow_none:
                result.add_error("Arrow ID cannot be None", "arrow_id", None, ctx)
            return result

        try:
            # Check type
            if not isinstance(arrow_id, str):
                result.add_error("Arrow ID must be a string", "arrow_id", arrow_id, ctx)
                return result

            # Check valid arrow IDs
            valid_arrow_ids = ["blue", "red"]
            if arrow_id not in valid_arrow_ids:
                result.add_error(
                    f"Arrow ID must be one of {valid_arrow_ids}",
                    "arrow_id",
                    arrow_id,
                    ctx,
                )

        except Exception as e:
            result.add_error(
                f"Error validating arrow ID: {e!s}", "arrow_id", arrow_id, ctx
            )

        return result

    @staticmethod
    def validate_orientation(
        orientation: Any, allow_none: bool = True, context: dict[str, Any] = None
    ) -> ValidationResult:
        """
        Validate orientation value (enum or string).

        Args:
            orientation: Orientation to validate (Orientation enum, string, or None)
            allow_none: Whether None values are allowed
            context: Additional context for error reporting

        Returns:
            ValidationResult: Validation result with errors/warnings
        """
        result = ValidationResult(is_valid=True, errors=[], warnings=[])
        ctx = context or {}

        try:
            if orientation is None:
                if not allow_none:
                    result.add_error(
                        "Orientation cannot be None", "orientation", orientation, ctx
                    )
                return result

            # Handle Orientation enum
            if isinstance(orientation, Orientation):
                # Valid enum value
                return result

            # Handle string values
            if isinstance(orientation, str):
                if not orientation.strip():
                    result.add_error(
                        "Orientation string cannot be empty or whitespace",
                        "orientation",
                        orientation,
                        ctx,
                    )
                    return result

                # Validate against enum values
                valid_orientations = {o.value for o in Orientation}
                if orientation not in valid_orientations:
                    result.add_error(
                        f"Invalid orientation value: '{orientation}'. Valid values: {sorted(valid_orientations)}",
                        "orientation",
                        orientation,
                        ctx,
                    )
                    return result

                return result

            # Invalid type
            result.add_error(
                f"Orientation must be Orientation enum or string, got {type(orientation).__name__}",
                "orientation",
                orientation,
                ctx,
            )

        except Exception as e:
            result.add_error(
                f"Error validating orientation: {e!s}",
                "orientation",
                orientation,
                ctx,
            )

        return result


# Convenience functions for quick validation
def validate_beat_data(
    beat_data: BeatData | None,
    allow_none: bool = True,
    context: dict[str, Any] = None,
) -> ValidationResult:
    """Quick validation function for beat data."""
    return GraphEditorValidator.validate_beat_data(beat_data, allow_none, context)


def validate_sequence_data(
    sequence_data: SequenceData | None,
    allow_none: bool = True,
    context: dict[str, Any] = None,
) -> ValidationResult:
    """Quick validation function for sequence data."""
    return GraphEditorValidator.validate_sequence_data(
        sequence_data, allow_none, context
    )


def validate_beat_index(
    beat_index: int,
    sequence_length: int = None,
    allow_negative: bool = True,
    context: dict[str, Any] = None,
) -> ValidationResult:
    """Quick validation function for beat index."""
    return GraphEditorValidator.validate_beat_index(
        beat_index, sequence_length, allow_negative, context
    )


def validate_arrow_id(
    arrow_id: str | None, allow_none: bool = True, context: dict[str, Any] = None
) -> ValidationResult:
    """Quick validation function for arrow ID."""
    return GraphEditorValidator.validate_arrow_id(arrow_id, allow_none, context)


def validate_orientation(
    orientation: Any, allow_none: bool = True, context: dict[str, Any] = None
) -> ValidationResult:
    """Quick validation function for orientation."""
    return GraphEditorValidator.validate_orientation(orientation, allow_none, context)
