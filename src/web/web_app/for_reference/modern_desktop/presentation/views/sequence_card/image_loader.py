"""
Image Loading Components for Sequence Cards

Handles background image loading for sequence card widgets.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QPixmap


logger = logging.getLogger(__name__)


class ImageLoader(QThread):
    """Background thread for loading sequence card images."""

    image_loaded = pyqtSignal(str, QPixmap)  # path, pixmap
    image_failed = pyqtSignal(str)  # path

    def __init__(self):
        super().__init__()
        self.image_queue = []
        self.is_loading = False

    def load_image(self, image_path: Path):
        """Queue an image for loading."""
        path_str = str(image_path)
        if path_str not in self.image_queue:
            self.image_queue.append(path_str)
            if not self.is_loading:
                self.start()

    def run(self):
        """Load images in background thread."""
        self.is_loading = True
        while self.image_queue:
            path_str = self.image_queue.pop(0)
            try:
                pixmap = QPixmap(path_str)
                if not pixmap.isNull():
                    self.image_loaded.emit(path_str, pixmap)
                else:
                    self.image_failed.emit(path_str)
            except Exception as e:
                logger.warning(f"Failed to load image {path_str}: {e}")
                self.image_failed.emit(path_str)
        self.is_loading = False
