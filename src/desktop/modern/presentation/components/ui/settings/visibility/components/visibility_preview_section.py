"""
Visibility Preview Section for Visibility Settings.

Focused component handling interactive pictograph preview management.
Extracted from the monolithic visibility tab following TKA clean architecture principles.
"""

import logging
from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from desktop.modern.presentation.components.ui.settings.visibility.visibility_pictograph_preview import (
    VisibilityPictographPreview,
)

logger = logging.getLogger(__name__)


class VisibilityPreviewSection(QWidget):
    """
    Interactive pictograph preview section.

    Handles preview widget creation, update coordination, and real-time visibility changes.
    Follows TKA single-responsibility principle and clean component organization.
    """

    preview_updated = pyqtSignal()

    def __init__(self, parent=None):
        """
        Initialize visibility preview section.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        # UI components
        self.preview: Optional[VisibilityPictographPreview] = None

        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        """Setup the preview widget UI with compact layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        # Preview title
        title = QLabel("Interactive Preview")
        title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Create the actual pictograph preview
        self.preview = VisibilityPictographPreview()
        self.preview.setMinimumSize(200, 160)  # Minimum usable size
        layout.addWidget(self.preview)

    def _setup_connections(self):
        """Setup signal connections for preview updates."""
        if self.preview:
            self.preview.preview_updated.connect(self._on_preview_updated)

    def _on_preview_updated(self):
        """Handle preview update notifications."""
        logger.debug("Preview updated")
        self.preview_updated.emit()

    def update_visibility(self, element_name: str, visible: bool):
        """
        Update preview with visibility changes.

        Args:
            element_name: Name of the element to update
            visible: Whether the element should be visible
        """
        if self.preview:
            try:
                self.preview.update_visibility(element_name, visible)
                logger.debug(f"Preview updated for {element_name}: {visible}")
            except Exception as e:
                logger.error(f"Error updating preview visibility: {e}")

    def refresh_preview(self):
        """Force refresh the preview display."""
        if self.preview:
            try:
                self.preview.refresh_preview()
                logger.debug("Preview refreshed")
            except Exception as e:
                logger.error(f"Error refreshing preview: {e}")

    def cleanup(self):
        """Clean up preview resources."""
        if self.preview:
            try:
                self.preview.cleanup()
                logger.debug("Preview section cleaned up")
            except Exception as e:
                logger.error(f"Error during preview cleanup: {e}")

    def get_preview_widget(self) -> Optional[VisibilityPictographPreview]:
        """
        Get the preview widget for direct access if needed.

        Returns:
            The VisibilityPictographPreview widget or None
        """
        return self.preview
