"""
PyQt6 adapters for converting between framework-agnostic types and PyQt6 types.

These adapters are used in the UI layer to bridge between the clean architecture
core types and the PyQt6 framework types.
"""
from __future__ import annotations

from desktop.modern.core.types import Point, Rect, Size


try:
    from PyQt6.QtCore import QPointF, QRect, QSize

    QT_AVAILABLE = True
except ImportError:
    QT_AVAILABLE = False

    # Create stub classes for testing
    class QSize:
        def __init__(self, width=0, height=0):
            self._width = width
            self._height = height

        def width(self):
            return self._width

        def height(self):
            return self._height

    class QPointF:
        def __init__(self, x=0.0, y=0.0):
            self._x = x
            self._y = y

        def x(self):
            return self._x

        def y(self):
            return self._y

    class QRect:
        def __init__(self, x=0, y=0, width=0, height=0):
            self._x = x
            self._y = y
            self._width = width
            self._height = height

        def x(self):
            return self._x

        def y(self):
            return self._y

        def width(self):
            return self._width

        def height(self):
            return self._height


class QtGeometryAdapter:
    """Adapter for converting between core types and PyQt6 geometry types."""

    @staticmethod
    def size_to_qsize(size: Size) -> QSize:
        """Convert core Size to QSize."""
        return QSize(size.width, size.height)

    @staticmethod
    def qsize_to_size(qsize: QSize) -> Size:
        """Convert QSize to core Size."""
        return Size(width=qsize.width(), height=qsize.height())

    @staticmethod
    def point_to_qpointf(point: Point) -> QPointF:
        """Convert core Point to QPointF."""
        return QPointF(point.x, point.y)

    @staticmethod
    def qpointf_to_point(qpoint: QPointF) -> Point:
        """Convert QPointF to core Point."""
        return Point(x=qpoint.x(), y=qpoint.y())

    @staticmethod
    def rect_to_qrect(rect: Rect) -> QRect:
        """Convert core Rect to QRect."""
        return QRect(rect.x, rect.y, rect.width, rect.height)

    @staticmethod
    def qrect_to_rect(qrect: QRect) -> Rect:
        """Convert QRect to core Rect."""
        return Rect(
            x=qrect.x(), y=qrect.y(), width=qrect.width(), height=qrect.height()
        )

    @staticmethod
    def widget_size_to_size(widget) -> Size:
        """Extract Size from QWidget size."""
        if not QT_AVAILABLE:
            return Size(800, 600)  # Default for testing

        qsize = widget.size()
        return Size(width=qsize.width(), height=qsize.height())

    @staticmethod
    def size_to_widget_size(size: Size, widget) -> None:
        """Apply Size to QWidget."""
        if QT_AVAILABLE and hasattr(widget, "resize"):
            widget.resize(QtGeometryAdapter.size_to_qsize(size))


class QtTypeConverter:
    """High-level converter for common UI operations."""

    @staticmethod
    def get_widget_geometry(widget) -> Rect:
        """Get widget geometry as core Rect."""
        if not QT_AVAILABLE:
            return Rect(0, 0, 800, 600)

        qrect = widget.geometry()
        return QtGeometryAdapter.qrect_to_rect(qrect)

    @staticmethod
    def set_widget_geometry(widget, rect: Rect) -> None:
        """Set widget geometry from core Rect."""
        if QT_AVAILABLE and hasattr(widget, "setGeometry"):
            widget.setGeometry(QtGeometryAdapter.rect_to_qrect(rect))

    @staticmethod
    def calculate_center_point(size: Size) -> Point:
        """Calculate center point of a size."""
        return Point(x=size.width / 2, y=size.height / 2)

    @staticmethod
    def fit_size_to_container(content_size: Size, container_size: Size) -> Size:
        """Fit content size to container while maintaining aspect ratio."""
        if not content_size.is_valid() or not container_size.is_valid():
            return container_size

        # Calculate scaling factors
        width_scale = container_size.width / content_size.width
        height_scale = container_size.height / content_size.height

        # Use the smaller scale to maintain aspect ratio
        scale = min(width_scale, height_scale)

        return content_size.scaled(scale)


# Convenience functions for common conversions
def to_qsize(size: Size) -> QSize:
    """Quick conversion from Size to QSize."""
    return QtGeometryAdapter.size_to_qsize(size)


def from_qsize(qsize: QSize) -> Size:
    """Quick conversion from QSize to Size."""
    return QtGeometryAdapter.qsize_to_size(qsize)


def to_qpointf(point: Point) -> QPointF:
    """Quick conversion from Point to QPointF."""
    return QtGeometryAdapter.point_to_qpointf(point)


def from_qpointf(qpoint: QPointF) -> Point:
    """Quick conversion from QPointF to Point."""
    return QtGeometryAdapter.qpointf_to_point(qpoint)
