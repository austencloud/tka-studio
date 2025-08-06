"""
TKA Coordinate Type Utilities

Provides clean conversion between PyQt6 QPointF and domain Point types.
Eliminates type mixing in positioning services.

"""

from __future__ import annotations

from PyQt6.QtCore import QPointF

from desktop.modern.core.types.geometry import Point


def qpoint_to_point(qpoint: QPointF) -> Point:
    """
    Convert PyQt6 QPointF to domain Point.

    Args:
        qpoint: PyQt6 QPointF instance

    Returns:
        Domain Point instance
    """
    return Point(qpoint.x(), qpoint.y())


def point_to_qpoint(point: Point) -> QPointF:
    """
    Convert domain Point to PyQt6 QPointF.

    Args:
        point: Domain Point instance

    Returns:
        PyQt6 QPointF instance
    """
    return QPointF(point.x, point.y)


# Type aliases removed - using simple Point and QPointF types directly

# Default values for fallback scenarios
DEFAULT_POINT = Point(0.0, 0.0)
DEFAULT_QPOINT = QPointF(0.0, 0.0)


def get_default_point() -> Point:
    """Get default point for fallback scenarios."""
    return DEFAULT_POINT


def get_default_qpoint() -> QPointF:
    """Get default QPointF for fallback scenarios."""
    return DEFAULT_QPOINT
