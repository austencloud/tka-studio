"""
QT Thumbnail Factory Adapter

Bridges between the framework-agnostic core thumbnail service and QT-specific
presentation layer. Converts thumbnail data to QT widgets.
"""

from __future__ import annotations

import logging
import os

# Import framework-agnostic core
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget


sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../../"))

from desktop.modern.application.services.core.thumbnail_service import (
    CoreThumbnailService,
    IThumbnailImageLoader,
    ThumbnailData,
    ThumbnailSpec,
    convert_sequence_data_to_spec,
)
from desktop.modern.application.services.core.types import ImageData, ImageFormat, Size


logger = logging.getLogger(__name__)


# ============================================================================
# QT IMAGE LOADER IMPLEMENTATION
# ============================================================================


class QtImageLoader(IThumbnailImageLoader):
    """QT-specific image loader implementation."""

    def load_image(self, image_path: str, target_size: Size) -> ImageData | None:
        """Load and resize image using QT."""
        try:
            # Load with QPixmap
            pixmap = QPixmap(image_path)

            if pixmap.isNull():
                return None

            # Scale to target size
            scaled_pixmap = pixmap.scaled(
                target_size.width,
                target_size.height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            # Convert to bytes (in real implementation, you'd use QBuffer)
            # For now, return metadata about the loaded image
            return ImageData(
                width=scaled_pixmap.width(),
                height=scaled_pixmap.height(),
                format=ImageFormat.PNG,
                data=b"qt_pixmap_data",  # In real implementation: convert QPixmap to bytes
                metadata={
                    "qt_pixmap": scaled_pixmap,  # Store QPixmap for QT usage
                    "source_path": image_path,
                    "loader": "qt",
                },
            )

        except Exception as e:
            logger.exception(f"Qt image loading failed for {image_path}: {e}")
            return None

    def create_placeholder_image(self, text: str, size: Size, style: dict) -> ImageData:
        """Create placeholder image using QT."""
        try:
            # Create QPixmap for placeholder
            pixmap = QPixmap(size.width, size.height)
            pixmap.fill(Qt.GlobalColor.lightGray)

            return ImageData(
                width=size.width,
                height=size.height,
                format=ImageFormat.PNG,
                data=b"qt_placeholder_data",
                metadata={
                    "qt_pixmap": pixmap,
                    "placeholder_text": text,
                    "style": style,
                    "loader": "qt",
                },
            )

        except Exception as e:
            logger.exception(f"Qt placeholder creation failed: {e}")
            # Return empty image data
            return ImageData(
                width=size.width,
                height=size.height,
                format=ImageFormat.PNG,
                data=b"",
                metadata={"error": str(e)},
            )


# ============================================================================
# QT THUMBNAIL WIDGET FACTORY
# ============================================================================


class QtThumbnailWidgetFactory:
    """Creates QT widgets from framework-agnostic thumbnail data."""

    def create_thumbnail_widget(
        self, thumbnail_data: ThumbnailData, sort_method: str = "alphabetical"
    ) -> QWidget:
        """Create QT widget from thumbnail data."""
        try:
            # Create container frame
            thumbnail = QFrame()
            thumbnail.setFixedSize(
                thumbnail_data.spec.thumbnail_size.width,
                thumbnail_data.spec.thumbnail_size.height,
            )
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

            # Create image label
            image_label = QLabel()
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            image_label.setMinimumHeight(thumbnail_data.spec.thumbnail_size.height - 40)

            # Set image or placeholder
            self._set_thumbnail_image(image_label, thumbnail_data)
            layout.addWidget(image_label)

            # Sequence name
            name_label = QLabel(
                thumbnail_data.spec.sequence_name
                or f"Sequence {thumbnail_data.spec.sequence_id[:8]}"
            )
            name_label.setWordWrap(True)
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name_label.setStyleSheet("font-size: 10px; font-weight: bold;")
            layout.addWidget(name_label)

            # Beat count
            count_label = QLabel(f"{thumbnail_data.spec.beat_count} beats")
            count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            count_label.setStyleSheet("color: #666; font-size: 9px;")
            layout.addWidget(count_label)

            return thumbnail

        except Exception as e:
            logger.exception(f"Failed to create thumbnail widget: {e}")
            return self._create_error_widget(thumbnail_data.spec.thumbnail_size)

    def _set_thumbnail_image(self, image_label: QLabel, thumbnail_data: ThumbnailData):
        """Set image on the label from thumbnail data."""
        try:
            if thumbnail_data.has_error:
                # Show error
                image_label.setText("❌\nError")
                image_label.setStyleSheet(
                    """
                    color: #cc0000;
                    font-size: 12px;
                    background-color: #ffe6e6;
                    border: 1px dashed #cc0000;
                    border-radius: 4px;
                    padding: 8px;
                """
                )
            elif thumbnail_data.has_image:
                # Use actual image
                image_data = thumbnail_data.image_data

                # Check if we have a QT pixmap in metadata
                qt_pixmap = image_data.metadata.get("qt_pixmap")
                if qt_pixmap and isinstance(qt_pixmap, QPixmap):
                    image_label.setPixmap(qt_pixmap)
                else:
                    # Fallback: show placeholder text
                    placeholder_text = (
                        thumbnail_data.placeholder_text or "📄\nThumbnail"
                    )
                    image_label.setText(placeholder_text)
                    image_label.setStyleSheet(
                        """
                        color: #666;
                        font-size: 14px;
                        font-weight: bold;
                        background-color: #f8f8f8;
                        border: 1px dashed #ccc;
                        border-radius: 4px;
                        padding: 10px;
                    """
                    )
            else:
                # No image available
                image_label.setText("📄\nNo Image")
                image_label.setStyleSheet(
                    """
                    color: #999;
                    font-size: 12px;
                    background-color: #f8f8f8;
                    border: 1px dashed #ddd;
                    border-radius: 4px;
                    padding: 8px;
                """
                )

        except Exception as e:
            logger.exception(f"Failed to set thumbnail image: {e}")
            image_label.setText("❌\nError")

    def _create_error_widget(self, size: Size) -> QWidget:
        """Create error widget."""
        error_widget = QFrame()
        error_widget.setFixedSize(size.width, size.height)
        error_widget.setStyleSheet(
            "background-color: #ffe6e6; border: 1px solid #cc0000;"
        )

        layout = QVBoxLayout(error_widget)
        error_label = QLabel("❌\nError")
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(error_label)

        return error_widget


# ============================================================================
# MAIN QT THUMBNAIL ADAPTER
# ============================================================================


class QtThumbnailFactoryAdapter:
    """
    Main adapter that bridges core thumbnail service with QT presentation.

    This adapter:
    1. Uses the framework-agnostic core service to create thumbnail data
    2. Converts thumbnail data to QT widgets
    3. Provides the same interface as the original QT service for easy migration
    """

    def __init__(
        self,
        core_service: CoreThumbnailService | None = None,
        image_loader: QtImageLoader | None = None,
    ):
        """Initialize the adapter."""
        self.image_loader = image_loader or QtImageLoader()
        self.core_service = core_service or CoreThumbnailService(self.image_loader)
        self.widget_factory = QtThumbnailWidgetFactory()

        logger.info("QT thumbnail factory adapter initialized")

    # ========================================================================
    # LEGACY INTERFACE COMPATIBILITY
    # ========================================================================

    def create_thumbnail(
        self, sequence, thumbnail_width: int, sort_method: str = "alphabetical"
    ) -> QWidget:
        """Create thumbnail widget using core service + QT rendering (legacy interface)."""
        try:
            # Convert sequence data to framework-agnostic spec
            thumbnail_spec = convert_sequence_data_to_spec(sequence, thumbnail_width)

            # Use core service to create thumbnail data
            thumbnail_data = self.core_service.create_thumbnail_data(thumbnail_spec)

            # Convert to QT widget
            return self.widget_factory.create_thumbnail_widget(
                thumbnail_data, sort_method
            )

        except Exception as e:
            logger.exception(f"Failed to create thumbnail: {e}")
            return self.widget_factory._create_error_widget(
                Size(thumbnail_width, thumbnail_width)
            )

    # ========================================================================
    # NEW CAPABILITIES
    # ========================================================================

    def batch_create_thumbnails(
        self, sequences: list, thumbnail_width: int, sort_method: str = "alphabetical"
    ) -> list[QWidget]:
        """Create multiple thumbnails efficiently using core service."""
        try:
            # Convert all sequences to specs
            from desktop.modern.application.services.core.thumbnail_service import (
                batch_convert_sequences_to_specs,
            )

            specs = batch_convert_sequences_to_specs(sequences, thumbnail_width)

            # Use core service for batch processing
            thumbnail_data_list = self.core_service.batch_create_thumbnails(specs)

            # Convert all to QT widgets
            widgets = []
            for thumbnail_data in thumbnail_data_list:
                widget = self.widget_factory.create_thumbnail_widget(
                    thumbnail_data, sort_method
                )
                widgets.append(widget)

            logger.info(f"Created {len(widgets)} thumbnail widgets in batch")
            return widgets

        except Exception as e:
            logger.exception(f"Failed to create thumbnail batch: {e}")
            # Return error widgets
            error_size = Size(thumbnail_width, thumbnail_width)
            return [
                self.widget_factory._create_error_widget(error_size) for _ in sequences
            ]

    def get_thumbnail_data(self, sequence, thumbnail_width: int) -> ThumbnailData:
        """Get framework-agnostic thumbnail data (useful for testing/debugging)."""
        try:
            thumbnail_spec = convert_sequence_data_to_spec(sequence, thumbnail_width)
            return self.core_service.create_thumbnail_data(thumbnail_spec)
        except Exception as e:
            logger.exception(f"Failed to get thumbnail data: {e}")
            return ThumbnailData(
                thumbnail_id="error",
                spec=ThumbnailSpec(
                    sequence_id="unknown",
                    sequence_name="Error",
                    beat_count=0,
                    thumbnail_size=Size(thumbnail_width, thumbnail_width),
                ),
                error_message=str(e),
            )


# ============================================================================
# FACTORY FUNCTION FOR EASY INTEGRATION
# ============================================================================
