"""
Selectable Arrow Graphics Item

Custom QGraphicsSvgItem that supports selection highlighting for the graph editor.
Context-aware behavior: only clickable in graph editor, transparent elsewhere.
"""

from typing import Optional
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QPen, QColor, QPainter


class ArrowItem(QGraphicsSvgItem):
    """Custom arrow graphics item with context-aware click and cursor behavior"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Arrow properties
        self.arrow_color: Optional[str] = None
        self.is_highlighted = False
        self.highlight_color = QColor("#FFD700")  # Gold
        self.highlight_pen_width = 3

        # Context will be determined when added to scene
        self._context_type = "unknown"
        self._setup_default_behavior()

    def _setup_default_behavior(self):
        """Setup safe default behavior - arrows not clickable"""
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, False)
        self.setAcceptHoverEvents(False)
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def _determine_context(self) -> str:
        """Determine context by checking parent hierarchy"""
        parent = self.scene().parent() if self.scene() else None
        
        while parent:
            class_name = parent.__class__.__name__.lower()
            
            if "graph" in class_name and "editor" in class_name:
                return "graph_editor"
            elif "clickable" in class_name and "pictograph" in class_name:
                return "option_picker"
            elif "beat" in class_name and ("view" in class_name or "frame" in class_name):
                return "beat_frame"
            elif "preview" in class_name:
                return "preview"
                
            parent = parent.parent() if hasattr(parent, "parent") else None
        
        return "unknown"

    def _update_behavior_for_context(self):
        """Update behavior based on detected context"""
        self._context_type = self._determine_context()
        
        if self._context_type == "graph_editor":
            # Graph editor: arrows are clickable and show pointer cursor
            self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, True)
            self.setAcceptHoverEvents(True)
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            # All other contexts: arrows are transparent to events
            self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, False)
            self.setAcceptHoverEvents(False)
            self.setCursor(Qt.CursorShape.ArrowCursor)
            # CRITICAL: Make arrows not interfere with parent's cursor
            self.setFlag(self.GraphicsItemFlag.ItemIgnoresTransformations, False)

    def setParentItem(self, parent):
        """Override to update context when parent changes"""
        super().setParentItem(parent)
        if self.scene():
            self._update_behavior_for_context()

    def itemChange(self, change, value):
        """Override to update context when scene changes"""
        result = super().itemChange(change, value)
        if change == self.GraphicsItemChange.ItemSceneChange and value is not None:
            # Schedule context update for after scene is fully set up
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(0, self._update_behavior_for_context)
        return result

    def add_selection_highlight(self, color: str = "#FFD700"):
        """Add selection highlighting with specified color"""
        self.highlight_color = QColor(color)
        self.is_highlighted = True
        self.update()

    def clear_selection_highlight(self):
        """Clear selection highlighting"""
        self.is_highlighted = False
        self.update()

    def paint(self, painter: QPainter, option, widget=None):
        """Custom paint method to add selection highlighting"""
        # Paint the normal SVG content first
        super().paint(painter, option, widget)

        # Add selection highlight if needed and in graph editor context
        if self.is_highlighted and self._context_type == "graph_editor":
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
        """Handle hover enter - only in graph editor context"""
        if self._context_type == "graph_editor":
            super().hoverEnterEvent(event)
            # Could add subtle hover effect here if desired
        else:
            # In other contexts, completely ignore hover to let it pass through
            event.ignore()

    def hoverLeaveEvent(self, event):
        """Handle hover leave - only in graph editor context"""
        if self._context_type == "graph_editor":
            super().hoverLeaveEvent(event)
        else:
            # In other contexts, completely ignore hover to let it pass through
            event.ignore()

    def mousePressEvent(self, event):
        """Handle mouse press - only clickable in graph editor"""
        if event.button() == Qt.MouseButton.LeftButton:
            if self._context_type == "graph_editor":
                # Graph editor context - handle arrow selection
                if hasattr(self.scene(), "arrow_selected"):
                    self.scene().arrow_selected.emit(self.arrow_color)
                event.accept()
                return
            else:
                # All other contexts - ignore event so it passes through to parent
                event.ignore()
                return
        
        # For non-left clicks, use default behavior
        if self._context_type == "graph_editor":
            super().mousePressEvent(event)
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        """Handle mouse release - only in graph editor context"""
        if self._context_type == "graph_editor":
            super().mouseReleaseEvent(event)
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        """Handle mouse move - only in graph editor context"""
        if self._context_type == "graph_editor":
            super().mouseMoveEvent(event)
        else:
            event.ignore()

    def wheelEvent(self, event):
        """Handle wheel events - only in graph editor context"""
        if self._context_type == "graph_editor":
            super().wheelEvent(event)
        else:
            event.ignore()
