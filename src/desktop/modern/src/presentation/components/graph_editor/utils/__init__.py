"""
Graph Editor Utilities Package
=============================

Provides utility functions and classes for graph editor components.

Available utilities:
- validation: Input validation and error handling utilities
- logging: Structured logging utilities
"""

from .validation import (
    GraphEditorValidator,
    ValidationError,
    validate_beat_data,
    validate_sequence_data,
    validate_beat_index,
    validate_arrow_id,
)

from .logging import (
    GraphEditorLogger,
    create_component_logger,
    log_method_call,
    log_error_with_context,
)

__all__ = [
    # Validation
    "GraphEditorValidator",
    "ValidationError",
    "validate_beat_data",
    "validate_sequence_data", 
    "validate_beat_index",
    "validate_arrow_id",
    # Logging
    "GraphEditorLogger",
    "create_component_logger",
    "log_method_call",
    "log_error_with_context",
]
