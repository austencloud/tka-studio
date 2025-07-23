"""
Sequence Card Widget

Individual sequence card display widget with optimized image loading.
"""

import logging
from typing import Optional

from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from core.interfaces.sequence_card_services import SequenceCardData
from ..image_loading.image_loader import ImageLoader

logger = logging.getLogger(__name__)


class SequenceCardWidget(QLabel):
    """Widget for displaying individual sequence card."""

    def __init__(
        self,
        sequence_data: SequenceCardData,
        image_loader: Optional[ImageLoader] = None,
        parent=None,
    ):
        super().__init__(parent)
        self.sequence_data = sequence_data
        self.image_loader = image_loader
        self.is_image_loaded = False
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(150, 100)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._apply_styling()

        # Show word text initially, load image asynchronously
        self.setText(self.sequence_data.word)

        # Connect to image loader signals if provided
        self._connect_image_loader_signals()

    def _connect_image_loader_signals(self):
        """Connect to image loader signals if available."""
        if self.image_loader:
            self.image_loader.image_loaded.connect(self._on_image_loaded)
            self.image_loader.image_failed.connect(self._on_image_failed)

    def set_image_loader(self, image_loader: ImageLoader):
        """Set the image loader and connect signals."""
        self.image_loader = image_loader
        self._connect_image_loader_signals()

    def load_image_async(self):
        """Request image to be loaded asynchronously."""
        if not self.is_image_loaded and self.image_loader:
            self.image_loader.load_image(self.sequence_data.path)

    def show_placeholder(self):
        """Show placeholder content immediately for instant UI response."""
        if not self.is_image_loaded:
            # Show word text with enhanced styling for immediate feedback
            self.setText(self.sequence_data.word)
            self.setStyleSheet(
                """
                QLabel {
                    background-color: #f8f9fa;
                    border: 2px dashed #dee2e6;
                    border-radius: 4px;
                    color: #6c757d;
                    font-weight: bold;
                    font-size: 12px;
                    padding: 8px;
                }
            """
            )

    def load_image_optimized(self):
        """Load image with maximum performance optimizations."""
        if self.is_image_loaded:
            return

        try:
            # Safety check: ensure widget still exists
            if not self or self.isVisible() is None:
                return
                
            # Ultra-optimized loading: Use the fastest possible method
            path_str = str(self.sequence_data.path)

            # Load with format hint for faster processing
            pixmap = QPixmap()
            if pixmap.load(path_str, "PNG"):  # Explicit format hint
                # Set pixmap directly without any processing
                self.setPixmap(pixmap)
                self.setText("")  # Clear placeholder text
                self.setStyleSheet("")  # Clear placeholder styling
                self.is_image_loaded = True
            else:
                # Keep placeholder if image fails to load
                self.setText(f"❌ {self.sequence_data.word}")

        except RuntimeError as e:
            # Widget has been deleted
            logger.debug(f"Widget deleted during image loading: {e}")
        except Exception as e:
            logger.warning(
                f"Failed to load image optimized {self.sequence_data.path}: {e}"
            )
            try:
                self.setText(f"❌ {self.sequence_data.word}")
            except RuntimeError:
                # Widget deleted, ignore
                pass

    def _on_image_loaded(self, path_str: str, pixmap: QPixmap):
        """Handle successful image loading."""
        if str(self.sequence_data.path) == path_str and not self.is_image_loaded:
            # Scale pixmap to fit while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.setPixmap(scaled_pixmap)
            self.setText("")  # Clear text when image is loaded
            self.is_image_loaded = True

    def _on_image_failed(self, path_str: str):
        """Handle failed image loading."""
        if str(self.sequence_data.path) == path_str:
            self.setText(f"Error:\n{self.sequence_data.word}")

    def _apply_styling(self):
        """Apply card styling."""
        self.setStyleSheet(
            """
            QLabel {
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 5px;
                margin: 5px;
            }
            
            QLabel:hover {
                border: 2px solid #3498db;
                background: #f8f9fa;
            }
        """
        )
