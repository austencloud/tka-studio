"""
Graph Editor Utilities Package
=============================

Provides essential utility functions for graph editor components.

Available utilities:
- validation: Basic input validation utilities
- logging: Simple logging utilities
"""

from .validation import (
    ValidationError,
    ValidationResult,
    validate_beat_data,
    validate_sequence_data,
    validate_beat_index,
    validate_arrow_id,
)

from .logging import (
    create_component_logger,
    log_method_call,
    log_error_with_context,
)

__all__ = [
    # Validation
    "ValidationError",
    "ValidationResult",
    "validate_beat_data",
    "validate_sequence_data",
    "validate_beat_index",
    "validate_arrow_id",
    # Logging
    "create_component_logger",
    "log_method_call",
    "log_error_with_context",
]
