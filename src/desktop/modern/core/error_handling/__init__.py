"""
Error Handling Module for TKA Application

Provides standardized error handling across all modules.
"""

from .standard_error_handler import ErrorSeverity, StandardErrorHandler

__all__ = ["StandardErrorHandler", "ErrorSeverity"]
