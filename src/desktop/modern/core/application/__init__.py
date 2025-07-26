"""
Core application module for TKA.

Contains application factory and related utilities.
"""

from .application_factory import (
    ApplicationFactory,
    ApplicationMode,
    get_production_app,
    get_test_app,
    get_headless_app,
)

__all__ = [
    "ApplicationFactory",
    "ApplicationMode",
    "get_production_app",
    "get_test_app",
    "get_headless_app",
]
