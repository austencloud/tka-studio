"""
Thumbnail Factory Service

Service for creating sequence thumbnail widgets with image loading.
"""

from typing import Optional

from desktop.modern.core.interfaces.browse_services import IThumbnailFactory
from desktop.modern.domain.models.sequence_data import SequenceData
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget


class ThumbnailFactoryService(IThumbnailFactory):
    """Service for creating sequence thumbnail widgets."""

    def create_thumbnail(
        self, sequence: SequenceData, thumbnail_width: int, sort_method: str
    ) -> QWidget:
        """Create a thumbnail widget for a sequence with actual image loading."""
        # Create container frame
        thumbnail = QFrame()
        thumbnail.setFixedSize(thumbnail_width, thumbnail_width)
        thumbnail.setStyleSheet(
            """
            QFrame {
                border: 1px solid #ccc;
                background-color: #f0f0f0;
                border-radius: 4px;
            }
            QFrame:hover {
                border-color: #007acc;
                background-color: #e6f3ff;
            }
        """
        )

        layout = QVBoxLayout(thumbnail)
        layout.setContentsMargins(4, 4, 4, 4)

        # Try to load actual thumbnail image
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setMinimumHeight(thumbnail_width - 40)  # Leave space for text

        # Load thumbnail image if available
        self._load_thumbnail_image(sequence, image_label, thumbnail_width)

        layout.addWidget(image_label)

        # Sequence name
        name_label = QLabel(sequence.word or f"Sequence {sequence.id[:8] if hasattr(sequence, 'id') else 'Unknown'}")
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("font-size: 10px; font-weight: bold;")
        layout.addWidget(name_label)

        # Beat count
        beat_count = sequence.sequence_length if hasattr(sequence, 'sequence_length') else 0
        count_label = QLabel(f"{beat_count} beats")
        count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        count_label.setStyleSheet("color: #666; font-size: 9px;")
        layout.addWidget(count_label)

        return thumbnail

    def _load_thumbnail_image(
        self, sequence: SequenceData, image_label: QLabel, thumbnail_width: int
    ) -> None:
        """Load and set the thumbnail image."""
        thumbnail_path = self._get_thumbnail_path(sequence)

        if thumbnail_path:
            pixmap = QPixmap(thumbnail_path)

            if not pixmap.isNull():
                # Scale image to fit while maintaining aspect ratio
                scaled_pixmap = pixmap.scaled(
                    thumbnail_width - 8,
                    thumbnail_width - 40,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                image_label.setPixmap(scaled_pixmap)
                return

        # Fallback to placeholder
        self._set_placeholder_image(sequence, image_label)

    def _get_thumbnail_path(self, sequence: SequenceData) -> Optional[str]:
        """Get the thumbnail path from sequence data."""
        if hasattr(sequence, "thumbnails") and sequence.thumbnails:
            return sequence.thumbnails[0]
        elif hasattr(sequence, "thumbnail_paths") and sequence.thumbnail_paths:
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
