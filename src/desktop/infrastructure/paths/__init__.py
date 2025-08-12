"""
TKA Infrastructure - Path Management
=====================================

Centralized path management for the TKA application.

This module provides the universal path management system that automatically
configures all TKA paths for any Python environment.

Usage:
    # Automatic setup on import:
    from src.infrastructure.paths import tka_paths

    # Manual setup:
    from src.infrastructure.paths.tka_paths import setup_all_paths
    setup_all_paths()
"""

# Re-export for convenience
from .tka_paths import (
    find_tka_root,
    get_all_tka_paths,
    get_debug_info,
    print_debug_info,
    setup_all_paths,
)

__all__ = [
    "setup_all_paths",
    "find_tka_root",
    "get_all_tka_paths",
    "get_debug_info",
    "print_debug_info",
]
