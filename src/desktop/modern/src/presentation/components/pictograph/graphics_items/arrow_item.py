"""
Simple Arrow Graphics Item

Dead simple approach like the legacy version:
- Arrows are non-selectable by default
- Graph editor explicitly enables selection when needed
- No complex context detection
"""

from typing import Optional
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QColor


class ArrowItem(QGraphicsSvgItem):
    """Simple arrow graphics item - matches legacy approach"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Arrow properties
        self.arrow_color: Optional[str] = None
        self.is_highlighted = False
        self.highlight_color = QColor("#FFD700")  # Gold
        self.highlight_pen_width = 3

        # Default: arrows are NOT selectable (safe default)
        # Graph editor will explicitly enable selection when needed
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, False)
        self.setAcceptHoverEvents(False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def enable_selection(self):
        """Enable arrow selection - called by graph editor container"""
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, True)
        self.setAcceptHoverEvents(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def disable_selection(self):
        """Disable arrow selection - default state"""
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, False)
        self.setAcceptHoverEvents(False)
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def mousePressEvent(self, event):
        """Handle mouse press - emit signal if selectable"""
        if event.button() == Qt.MouseButton.LeftButton:
            if self.flags() & self.GraphicsItemFlag.ItemIsSelectable:
                # Arrow is selectable - emit signal
                if hasattr(self.scene(), "arrow_selected"):
                    self.scene().arrow_selected.emit(self.arrow_color)
                event.accept()
                return
            else:
                # Arrow not selectable - pass through
                event.ignore()
                return

        # For non-left clicks, use default behavior if selectable
        if self.flags() & self.GraphicsItemFlag.ItemIsSelectable:
            super().mousePressEvent(event)
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        """Handle mouse release - only if selectable"""
        if self.flags() & self.GraphicsItemFlag.ItemIsSelectable:
            super().mouseReleaseEvent(event)
        else:
            event.ignore()

    def hoverEnterEvent(self, event):
        """Handle hover enter - only if hover events enabled"""
        if self.acceptHoverEvents():
            super().hoverEnterEvent(event)
        else:
            event.ignore()

    def hoverLeaveEvent(self, event):
        """Handle hover leave - only if hover events enabled"""
        if self.acceptHoverEvents():
            super().hoverLeaveEvent(event)
        else:
            event.ignore()

    def add_selection_highlight(self, color: QColor = None):
        """Add selection highlighting"""
        if color:
            self.highlight_color = color
        self.is_highlighted = True
        self.update()

    def remove_selection_highlight(self):
        """Remove selection highlighting"""
        self.is_highlighted = False
        self.update()

    def paint(self, painter, option, widget=None):
        """Custom paint to show selection highlight"""
        # Draw the SVG first
        super().paint(painter, option, widget)

        # Add highlight if selected
        if self.is_highlighted:
            painter.setPen(QPen(self.highlight_color, self.highlight_pen_width))
            painter.drawRect(self.boundingRect())
