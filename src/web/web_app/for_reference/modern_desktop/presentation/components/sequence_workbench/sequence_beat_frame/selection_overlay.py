"""
Simple Selection Overlay - Legacy Style

Clean, simple gold border overlay for selection state only.
No hover effects, no scaling, no blue borders - just like the legacy version.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QWidget


class SelectionOverlay(QWidget):
    """
    Simple overlay widget that shows a gold border for selection state.

    Replicates the clean, working legacy approach:
    - Gold border for selection only
    - No hover effects
    - No scaling
    - No blue borders
    """

    # Visual constants - legacy style
    BORDER_WIDTH = 4
    SELECTION_COLOR = QColor(255, 215, 0)  # Gold

    def __init__(self, parent_view):
        super().__init__(parent_view)

        # Simple state tracking - only selection matters
        self._is_selected = False

        # Make transparent to mouse events so clicks go through to parent
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.hide()

    def show_selection(self):
        """Show selection overlay - simple legacy style"""
        self._is_selected = True
        self._update_position()
        self.show()

    def hide_selection(self):
        """Hide selection overlay"""
        self._is_selected = False
        self.hide()

    # Legacy compatibility methods (do nothing - no hover effects)
    def show_hover(self):
        """Legacy compatibility - no hover effects in simple mode"""

    def hide_hover_only(self):
        """Legacy compatibility - no hover effects in simple mode"""

    def hide_all(self):
        """Hide selection overlay"""
        self.hide_selection()

    def _update_position(self):
        """Update overlay position to match parent geometry - legacy style"""
        if self.parent():
            self.setGeometry(self.parent().rect())
            self.raise_()  # Ensure overlay is on top

    def paintEvent(self, event):
        """Draw the gold border - simple legacy style"""
        if not self._is_selected:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create gold pen - exactly like legacy
        pen = QPen(self.SELECTION_COLOR, self.BORDER_WIDTH)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        # Calculate border rectangle (inset by half border width) - legacy style
        rect = self.rect().adjusted(
            self.BORDER_WIDTH // 2,
            self.BORDER_WIDTH // 2,
            -self.BORDER_WIDTH // 2,
            -self.BORDER_WIDTH // 2,
        )

        # Draw the border rectangle
        painter.drawRect(rect)
        painter.end()

    def showEvent(self, event):
        """When shown, update position to match parent"""
        super().showEvent(event)
        self._update_position()

    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        # Trigger repaint when resized
        self.update()
