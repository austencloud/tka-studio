"""Blob Manager - Qt Presentation Layer

Thin wrapper for blob rendering - business logic delegated to AuroraBlobAnimation service.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPainterPath
from shared.application.services.backgrounds.aurora.blob_animation import (
    AuroraBlobAnimation,
)


class BlobManager:
    """Thin Qt wrapper for blob rendering - business logic in AuroraBlobAnimation service."""

    def __init__(self, num_blobs=3):
        self._animation_service = AuroraBlobAnimation(num_blobs)

    def animate(self):
        """Delegate animation logic to service."""
        self._animation_service.update_blobs()

    def draw(self, widget, painter: QPainter):
        """Draw blobs using Qt - get state from service."""
        blob_states = self._animation_service.get_blob_states()

        for blob in blob_states:
            blob_path = QPainterPath()
            blob_x = blob.position.x * widget.width()
            blob_y = blob.position.y * widget.height()

            blob_path.addEllipse(blob_x, blob_y, blob.size, blob.size)

            painter.setOpacity(blob.opacity)
            painter.setBrush(QColor(255, 255, 255, int(blob.opacity * 255)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPath(blob_path)

        painter.setOpacity(1.0)  # Reset opacity
