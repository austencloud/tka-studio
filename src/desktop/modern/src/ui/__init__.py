"""
UI layer modules for the TKA modern desktop application.

This package contains UI-specific adapters and utilities that bridge between
the clean architecture core types and the PyQt6 UI framework.
"""

from .adapters import (
    QtGeometryAdapter,
    QtTypeConverter,
    to_qsize,
    from_qsize,
    to_qpointf,
    from_qpointf,
)

__all__ = [
    "QtGeometryAdapter",
    "QtTypeConverter",
    "to_qsize",
    "from_qsize",
    "to_qpointf",
    "from_qpointf",
]
