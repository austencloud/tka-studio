"""
Thumbnail Factory Service

Service for creating sequence thumbnail widgets with image loading.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout, QWidget

from desktop.modern.core.interfaces.browse_services import IThumbnailFactory
from desktop.modern.domain.models.sequence_data import SequenceData


class ThumbnailFactoryService(IThumbnailFactory):
    """Service for creating sequence thumbnail widgets."""

    def create_thumbnail(
        self, sequence: SequenceData, thumbnail_width: int, sort_method: str
    ) -> QWidget:
        """Create a thumbnail widget for a sequence with responsive sizing and modern styling."""
        # Create container frame with responsive sizing
        thumbnail = QFrame()

        # Set responsive sizing - width expands, height follows aspect ratio
        thumbnail.setMinimumSize(150, 150)
        thumbnail.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        # Modern attractive styling (Qt-compatible CSS)
        thumbnail.setStyleSheet(
            """
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.95),
                    stop:1 rgba(245, 248, 252, 0.95)
                );
                border: 1px solid rgba(200, 220, 240, 0.8);
                border-radius: 12px;
                padding: 8px;
            }
            QFrame:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(240, 248, 255, 0.98),
                    stop:1 rgba(230, 245, 255, 0.98)
                );
                border: 2px solid rgba(100, 150, 255, 0.6);
            }
        """
        )

        layout = QVBoxLayout(thumbnail)
        layout.setContentsMargins(0, 0, 0, 0)

        # Try to load actual thumbnail image with aspect ratio preservation
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        # Image label should expand to fill container width but maintain aspect ratio

        # Load thumbnail image if available - will scale to fill available width
        self._load_thumbnail_image(sequence, image_label, thumbnail_width)

        layout.addWidget(image_label, 1)  # Give image most of the space

        # Sequence name with modern styling
        name_label = QLabel(
            sequence.word
            or f"Sequence {sequence.id[:8] if hasattr(sequence, 'id') else 'Unknown'}"
        )
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet(
            """
            QLabel {
                font-size: 11px;
                font-weight: 600;
                color: rgba(60, 80, 120, 0.9);
                background: transparent;
                padding: 4px 2px;
                border-radius: 4px;
            }
            """
        )
        layout.addWidget(name_label, 0)  # Fixed size for text

        # Beat count
        beat_count = (
            sequence.sequence_length if hasattr(sequence, "sequence_length") else 0
        )
        count_label = QLabel(f"{beat_count} beats")
        count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        count_label.setStyleSheet("color: #666; font-size: 9px;")
        layout.addWidget(count_label)

        return thumbnail

    def _load_thumbnail_image(
        self, sequence: SequenceData, image_label: QLabel, thumbnail_width: int
    ) -> None:
        """Load and set the thumbnail image with proper aspect ratio scaling."""
        # thumbnail_width parameter kept for interface compatibility
        thumbnail_path = self._get_thumbnail_path(sequence)

        if thumbnail_path:
            pixmap = QPixmap(thumbnail_path)

            if not pixmap.isNull():
                # Scale to fill the full thumbnail_width - the QLabel will expand to fill container
                # and the image will scale to fill the QLabel width while maintaining aspect ratio
                target_width = max(150, thumbnail_width or 350)

                scaled_pixmap = pixmap.scaledToWidth(
                    target_width, Qt.TransformationMode.SmoothTransformation
                )
                image_label.setPixmap(scaled_pixmap)
                return

        # Fallback to placeholder
        self._set_placeholder_image(sequence, image_label)

    def _get_thumbnail_path(self, sequence: SequenceData) -> str | None:
        """Get the thumbnail path from sequence data."""
        if hasattr(sequence, "thumbnails") and sequence.thumbnails:
            return sequence.thumbnails[0]
        if hasattr(sequence, "thumbnail_paths") and sequence.thumbnail_paths:
            return sequence.thumbnail_paths[0]
        return None

    def _set_placeholder_image(
        self, sequence: SequenceData, image_label: QLabel
    ) -> None:
        """Set a placeholder when no image is available."""
        # Check if image loading failed or no image available
        if self._get_thumbnail_path(sequence):
            # Image loading failed
            placeholder_text = f"❌\n{sequence.word or 'Sequence'}"
            style = """
                color: #999;
                font-size: 12px;
                background-color: #f8f8f8;
                border: 1px dashed #ddd;
                border-radius: 4px;
                padding: 8px;
            """
        else:
            # No thumbnail available
            placeholder_text = f"📄\n{sequence.word or 'Sequence'}"
            style = """
                color: #666;
                font-size: 14px;
                font-weight: bold;
                background-color: #f8f8f8;
                border: 1px dashed #ccc;
                border-radius: 4px;
                padding: 10px;
            """

        image_label.setText(placeholder_text)
        image_label.setStyleSheet(style)
