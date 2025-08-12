"""
Core application module for TKA.

Contains application factory and related utilities.
"""
from __future__ import annotations

from .application_factory import (
    ApplicationFactory,
    ApplicationMode,
    get_headless_app,
    get_production_app,
    get_test_app,
)


__all__ = [
    "ApplicationFactory",
    "ApplicationMode",
    "get_headless_app",
    "get_production_app",
    "get_test_app",
]
