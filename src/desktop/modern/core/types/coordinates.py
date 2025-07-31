"""
TKA Coordinate Type Utilities

Provides clean conversion between PyQt6 QPointF and domain Point types.
Eliminates type mixing in positioning services.

"""

from desktop.modern.core.types.geometry import Point

# Conditional PyQt6 imports for testing compatibility
try:
    from PyQt6.QtCore import QPointF

    QT_AVAILABLE = True
except ImportError:
    # Create mock QPointF for testing when Qt is not available
    class QPointF:
        def __init__(self, x=0.0, y=0.0):
            self._x = x
            self._y = y

        def x(self):
            return self._x

        def y(self):
            return self._y

    QT_AVAILABLE = False


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
