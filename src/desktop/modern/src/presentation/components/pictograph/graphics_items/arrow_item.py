"""
Selectable Arrow Graphics Item

Custom QGraphicsSvgItem that supports selection highlighting for the graph editor.
"""

from typing import Optional
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QPen, QColor, QPainter


class ArrowItem(QGraphicsSvgItem):
    """Custom arrow graphics item with selection highlighting support"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Arrow properties
        self.arrow_color: Optional[str] = None
        self.is_highlighted = False
        self.highlight_color = QColor("#FFD700")  # Gold
        self.highlight_pen_width = 3

        # Enable selection and hover
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, True)
        self.setAcceptHoverEvents(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def add_selection_highlight(self, color: str = "#FFD700"):
        """Add selection highlighting with specified color"""
        self.highlight_color = QColor(color)
        self.is_highlighted = True
        self.update()  # Trigger repaint

    def clear_selection_highlight(self):
        """Clear selection highlighting"""
        self.is_highlighted = False
        self.update()  # Trigger repaint

    def paint(self, painter: QPainter, option, widget=None):
        """Custom paint method to add selection highlighting"""
        # Paint the normal SVG content first
        super().paint(painter, option, widget)

        # Add selection highlight if needed
        if self.is_highlighted:
            painter.save()

            # Create highlight pen
            highlight_pen = QPen(self.highlight_color)
            highlight_pen.setWidth(self.highlight_pen_width)
            highlight_pen.setStyle(Qt.PenStyle.SolidLine)

            painter.setPen(highlight_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)

            # Draw highlight border around the arrow
            bounds = self.boundingRect()
            painter.drawRect(bounds)

            painter.restore()

    def hoverEnterEvent(self, event):
        """Handle hover enter - could add hover effects"""
        super().hoverEnterEvent(event)
        # Could add subtle hover effect here if desired

    def hoverLeaveEvent(self, event):
        """Handle hover leave"""
        super().hoverLeaveEvent(event)
        # Remove hover effects if any

    def mousePressEvent(self, event):
        """Handle mouse press for selection"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Emit selection signal through scene if available
            if self.scene() and hasattr(self.scene(), "arrow_selected"):
                self.scene().arrow_selected.emit(self.arrow_color)

        super().mousePressEvent(event)
