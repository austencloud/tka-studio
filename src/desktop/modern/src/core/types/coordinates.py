"""
TKA Coordinate Type Utilities

Provides clean conversion between PyQt6 QPointF and domain Point types.
Eliminates type mixing in positioning services.

USAGE:
    from core.types.coordinates import qpoint_to_point, point_to_qpoint, PositionResult
    from core.types.geometry import Point
    
    # Convert PyQt6 to domain
    domain_point = qpoint_to_point(qpoint)
    
    # Convert domain to PyQt6 (only at UI boundary)
    ui_point = point_to_qpoint(domain_point)
    
    # Use consistent return types
    def calculate_position() -> PositionResult:
        try:
            point = Point(10.0, 20.0)
            return success(point)
        except Exception as e:
            return failure(app_error(
                ErrorType.POSITIONING_ERROR,
                f"Position calculation failed: {e}",
                cause=e
            ))
"""

from typing import Union
from core.types.geometry import Point
from core.types.result import Result, AppError, ErrorType, success, failure, app_error

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


def safe_qpoint_to_point(qpoint: Union[QPointF, None]) -> Result[Point, AppError]:
    """
    Safely convert QPointF to Point with error handling.
    
    Args:
        qpoint: PyQt6 QPointF instance or None
        
    Returns:
        Result containing Point or AppError
    """
    if qpoint is None:
        return failure(app_error(
            ErrorType.VALIDATION_ERROR,
            "Cannot convert None to Point",
            {"input": "None"}
        ))
    
    try:
        return success(qpoint_to_point(qpoint))
    except Exception as e:
        return failure(app_error(
            ErrorType.POSITIONING_ERROR,
            f"Failed to convert QPointF to Point: {e}",
            {"qpoint_x": getattr(qpoint, '_x', 'unknown'), "qpoint_y": getattr(qpoint, '_y', 'unknown')},
            e
        ))


def safe_point_to_qpoint(point: Union[Point, None]) -> Result[QPointF, AppError]:
    """
    Safely convert Point to QPointF with error handling.
    
    Args:
        point: Domain Point instance or None
        
    Returns:
        Result containing QPointF or AppError
    """
    if point is None:
        return failure(app_error(
            ErrorType.VALIDATION_ERROR,
            "Cannot convert None to QPointF",
            {"input": "None"}
        ))
    
    try:
        return success(point_to_qpoint(point))
    except Exception as e:
        return failure(app_error(
            ErrorType.POSITIONING_ERROR,
            f"Failed to convert Point to QPointF: {e}",
            {"point_x": getattr(point, 'x', 'unknown'), "point_y": getattr(point, 'y', 'unknown')},
            e
        ))


# Type aliases for consistent positioning results
PositionResult = Result[Point, AppError]
QPointResult = Result[QPointF, AppError]

# Default values for fallback scenarios
DEFAULT_POINT = Point(0.0, 0.0)
DEFAULT_QPOINT = QPointF(0.0, 0.0)


def get_default_point() -> Point:
    """Get default Point for fallback scenarios."""
    return DEFAULT_POINT


def get_default_qpoint() -> QPointF:
    """Get default QPointF for fallback scenarios."""
    return DEFAULT_QPOINT
