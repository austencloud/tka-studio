"""
Sequence Card Widget

Individual sequence card display widget with optimized image loading.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QSizePolicy

from desktop.modern.core.interfaces.sequence_card_services import (
    ISequenceCardCacheService,
    SequenceCardData,
)

from .image_loader import ImageLoader


logger = logging.getLogger(__name__)


class SequenceCardWidget(QLabel):
    """Widget for displaying individual sequence card."""

    def __init__(
        self,
        sequence_data: SequenceCardData,
        image_loader: ImageLoader | None = None,
        cache_service: ISequenceCardCacheService | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self.sequence_data = sequence_data
        self.image_loader = image_loader
        self.cache_service = cache_service
        self.is_image_loaded = False
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # BALANCED FIX: Set a reasonable minimum size that scales with container
        # Cards should take up a good portion of their grid cell (60-80%)
        # Start with a base minimum that will be adjusted by parent
        self.setMinimumSize(80, 60)  # Base minimum - will be scaled by parent

        # Use preferred policy to respect minimum size without expanding too much
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
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

    def set_cache_service(self, cache_service: ISequenceCardCacheService):
        """Set the cache service for optimized image loading."""
        self.cache_service = cache_service

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
        """Load image with maximum performance optimizations and caching (legacy behavior)."""
        if self.is_image_loaded:
            return

        try:
            # Safety check: ensure widget still exists
            if not self or self.isVisible() is None:
                return

            path_str = str(self.sequence_data.path)

            # CRITICAL: Check cache first (legacy pattern)
            if self.cache_service:
                cached_image_data = self.cache_service.get_cached_image(
                    self.sequence_data.path
                )
                if cached_image_data:
                    # Load from cache
                    pixmap = QPixmap()
                    if pixmap.loadFromData(cached_image_data):
                        self.setPixmap(pixmap)
                        self.setText("")  # Clear placeholder text
                        self.setStyleSheet("")  # Clear placeholder styling
                        self.is_image_loaded = True
                        logger.debug(f"Cache hit for image: {path_str}")
                        return

            # Cache miss - load from disk and cache
            pixmap = QPixmap()
            if pixmap.load(path_str, "PNG"):  # Explicit format hint
                # Cache the loaded image for future use
                if self.cache_service:
                    # Convert pixmap to bytes for caching
                    from PyQt6.QtCore import QBuffer, QIODevice

                    buffer = QBuffer()
                    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
                    pixmap.save(buffer, "PNG")
                    image_data = buffer.data().data()
                    self.cache_service.cache_image(self.sequence_data.path, image_data)
                    logger.debug(f"Cached image: {path_str}")

                # LEGACY BEHAVIOR: Scale pixmap to fit grid cell size
                widget_size = self.size()
                if widget_size.width() > 0 and widget_size.height() > 0:
                    # Scale to fit current widget size (determined by grid layout)
                    scaled_pixmap = pixmap.scaled(
                        widget_size,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                    self.setPixmap(scaled_pixmap)
                else:
                    # Widget not sized yet, set pixmap directly
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
            # LEGACY BEHAVIOR: Scale pixmap to fit grid cell size
            # Get current widget size (determined by grid layout)
            widget_size = self.size()

            # Only scale if widget has been sized by layout
            if widget_size.width() > 0 and widget_size.height() > 0:
                scaled_pixmap = pixmap.scaled(
                    widget_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                self.setPixmap(scaled_pixmap)
            else:
                # Widget not sized yet, set pixmap directly
                self.setPixmap(pixmap)

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
