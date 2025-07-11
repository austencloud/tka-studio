"""
Selectable Arrow Graphics Item

Custom QGraphicsSvgItem that supports selection highlighting for the graph editor.
Context-aware behavior: only clickable in graph editor, transparent elsewhere.
"""

import logging
from typing import Optional

from application.services.pictograph.scaling_service import RenderingContext
from core.interfaces.core_services import IPictographContextDetector
from PyQt6.QtCore import QObject, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

logger = logging.getLogger(__name__)


class ArrowItem(QGraphicsSvgItem):
    """Custom arrow graphics item - simple approach like legacy version"""

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
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def _determine_context(self) -> RenderingContext:
        """
        Determine context using the robust context service.

        Falls back to safe detection if service is not available.
        """
        try:
            # Try to get context service from DI container
            if not self._context_service:
                from core.application.application_factory import get_container

                container = get_container()
                if container:
                    self._context_service = container.resolve(
                        IPictographContextDetector
                    )
                    print(
                        f"✅ [ARROW_ITEM] Successfully resolved IPictographContextService: {type(self._context_service).__name__}"
                    )
                else:
                    print("❌ [ARROW_ITEM] No DI container available")

            # Use service-based context detection
            if self._context_service and self.scene():
                context = self._context_service.determine_context_from_scene(
                    self.scene()
                )
                logger.debug(f"Context service determined: {context.value}")
                return context

        except Exception as e:
            logger.warning(f"Context service unavailable, using fallback: {e}")

        # Fallback to safe detection for backward compatibility
        return self._safe_fallback_context_detection()

    def _safe_fallback_context_detection(self) -> RenderingContext:
        """
        Safe fallback context detection with minimal string matching.

        This provides backward compatibility while encouraging migration
        to explicit context declaration.
        """
        try:
            scene = self.scene()
            if not scene:
                logger.debug("No scene available for context detection")
                return RenderingContext.UNKNOWN

            # Check if scene has explicit context
            if hasattr(scene, "rendering_context"):
                context = getattr(scene, "rendering_context")
                if isinstance(context, RenderingContext):
                    logger.debug(f"Scene has explicit context: {context.value}")
                    return context

            # Very limited, safe parent checking
            parent = getattr(scene, "parent", lambda: None)()
            if parent:
                class_name = parent.__class__.__name__

                # Only check for very specific, stable class names
                if class_name == "GraphEditorWidget":
                    logger.debug("Detected graph editor via safe fallback")
                    return RenderingContext.GRAPH_EDITOR
                elif class_name == "BeatFrameWidget":
                    logger.debug("Detected beat frame via safe fallback")
                    return RenderingContext.BEAT_FRAME

            logger.debug("No context detected, returning UNKNOWN")
            return RenderingContext.UNKNOWN

        except Exception as e:
            logger.error(f"Fallback context detection failed: {e}")
            return RenderingContext.UNKNOWN

    def _update_behavior_for_context(self):
        """Update behavior based on detected context"""
        self._context_type = self._determine_context()

        if self._context_type == RenderingContext.GRAPH_EDITOR:
            # Graph editor: arrows are clickable and show pointer cursor
            self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, True)
            self.setAcceptHoverEvents(True)
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            logger.debug("Arrow configured for graph editor context")
        else:
            # All other contexts: arrows are transparent to events
            self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, False)
            self.setAcceptHoverEvents(False)
            self.setCursor(Qt.CursorShape.ArrowCursor)
            # CRITICAL: Make arrows not interfere with parent's cursor
            self.setFlag(self.GraphicsItemFlag.ItemIgnoresTransformations, False)
            logger.debug(
                f"Arrow configured for non-interactive context: {self._context_type.value}"
            )

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
        if self.is_highlighted and self._context_type == RenderingContext.GRAPH_EDITOR:
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
            self.setCursor(Qt.CursorShape.PointingHandCursor)
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
            if self._context_type == RenderingContext.GRAPH_EDITOR:
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
        if self._context_type == RenderingContext.GRAPH_EDITOR:
            super().mousePressEvent(event)
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        """Handle mouse release - only in graph editor context"""
        if self._context_type == RenderingContext.GRAPH_EDITOR:
            super().mouseReleaseEvent(event)
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        """Handle mouse move - only in graph editor context"""
        if self._context_type == RenderingContext.GRAPH_EDITOR:
            super().mouseMoveEvent(event)
        else:
            event.ignore()

    def wheelEvent(self, event):
        """Handle wheel events - only in graph editor context"""
        if self._context_type == "graph_editor":
            super().wheelEvent(event)
        else:
            event.ignore()
