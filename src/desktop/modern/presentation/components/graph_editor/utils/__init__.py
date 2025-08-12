"""
Graph Editor Utilities Package
=============================

Provides essential utility functions for graph editor components.

Available utilities:
- validation: Basic input validation utilities
- logging: Simple logging utilities
"""

from __future__ import annotations

from .logging import (
    create_component_logger,
    log_error_with_context,
    log_method_call,
)
from .validation import (
    ValidationError,
    ValidationResult,
    validate_arrow_id,
    validate_beat_data,
    validate_beat_index,
    validate_sequence_data,
)


__all__ = [
    # Validation
    "ValidationError",
    "ValidationResult",
    # Logging
    "create_component_logger",
    "log_error_with_context",
    "log_method_call",
    "validate_arrow_id",
    "validate_beat_data",
    "validate_beat_index",
    "validate_sequence_data",
]
