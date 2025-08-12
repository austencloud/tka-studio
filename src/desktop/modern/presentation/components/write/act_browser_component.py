"""
Act Browser Component

Component for browsing and selecting existing acts.
Displays acts as thumbnails with metadata.
"""

from __future__ import annotations

import logging
from typing import Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.core.interfaces.write_services import IWriteTabCoordinator


logger = logging.getLogger(__name__)


class ActThumbnailWidget(QFrame):
    """Widget representing a single act thumbnail."""

    clicked = pyqtSignal(str)  # file path

    def __init__(self, act_info: dict[str, Any], parent: QWidget = None):
        super().__init__(parent)

        self.act_info = act_info
        self.file_path = act_info.get("file_path", "")

        self._setup_ui()
        self._setup_styling()

    def _setup_ui(self):
        """Setup the thumbnail UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        # Act name (title)
        self.name_label = QLabel(self.act_info.get("name", "Untitled"))
        self.name_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.name_label.setWordWrap(True)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label)

        # Thumbnail area (placeholder for now)
        self.thumbnail_label = QLabel("🎭")
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail_label.setFont(QFont("Segoe UI", 24))
        self.thumbnail_label.setMinimumSize(120, 80)
        layout.addWidget(self.thumbnail_label, 1)

        # Metadata
        metadata_layout = QVBoxLayout()

        # Sequence count
        seq_count = self.act_info.get("sequence_count", 0)
        self.sequence_label = QLabel(f"📋 {seq_count} sequences")
        self.sequence_label.setFont(QFont("Segoe UI", 8))
        metadata_layout.addWidget(self.sequence_label)

        # Has music indicator
        if self.act_info.get("has_music", False):
            self.music_label = QLabel("🎵 Has music")
            self.music_label.setFont(QFont("Segoe UI", 8))
            metadata_layout.addWidget(self.music_label)

        # Description preview
        description = self.act_info.get("description", "")
        if description:
            preview = description[:50] + "..." if len(description) > 50 else description
            self.desc_label = QLabel(preview)
            self.desc_label.setFont(QFont("Segoe UI", 8))
            self.desc_label.setWordWrap(True)
            self.desc_label.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
            metadata_layout.addWidget(self.desc_label)

        layout.addLayout(metadata_layout)

        # Set fixed size for uniform grid
        self.setFixedSize(160, 180)

    def _setup_styling(self):
        """Setup the thumbnail styling."""
        self.setStyleSheet("""
            ActThumbnailWidget {
                background: rgba(40, 40, 50, 0.8);
                border: 2px solid rgba(80, 80, 100, 0.5);
                border-radius: 8px;
            }
            ActThumbnailWidget:hover {
                background: rgba(60, 60, 70, 0.9);
                border-color: rgba(120, 120, 140, 0.8);
            }
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                background: transparent;
                border: none;
            }
        """)

    def mousePressEvent(self, event):
        """Handle mouse click."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.file_path)
        super().mousePressEvent(event)


class ActBrowserComponent(QScrollArea):
    """
    Component for browsing existing acts.

    Displays acts in a grid layout with thumbnails and metadata.
    """

    act_selected = pyqtSignal(str)  # file path

    def __init__(self, coordinator: IWriteTabCoordinator, parent: QWidget = None):
        super().__init__(parent)

        self.coordinator = coordinator
        self.thumbnail_widgets: list[ActThumbnailWidget] = []

        self._setup_ui()
        self._setup_styling()
        self._load_acts()

    def _setup_ui(self):
        """Setup the browser UI."""
        # Scroll content widget
        self.content_widget = QWidget()
        self.content_layout = QGridLayout(self.content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(10)

        # Configure scroll area
        self.setWidget(self.content_widget)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Set minimum width to accommodate thumbnails
        self.setMinimumWidth(200)

        # Create empty state label
        self.empty_label = QLabel("No acts found\n\nCreate a new act to get started")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setFont(QFont("Segoe UI", 12))
        self.empty_label.setStyleSheet("color: rgba(255, 255, 255, 0.6);")
        self.content_layout.addWidget(self.empty_label, 0, 0)
        self.empty_label.hide()

    def _setup_styling(self):
        """Setup the browser styling."""
        self.setStyleSheet("""
            ActBrowserComponent {
                background: rgba(20, 20, 30, 0.8);
                border: 1px solid rgba(60, 60, 80, 0.3);
                border-radius: 4px;
            }
            QScrollBar:vertical {
                background: rgba(40, 40, 50, 0.5);
                width: 12px;
                border-radius: 6px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: rgba(100, 100, 120, 0.8);
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(120, 120, 140, 0.9);
            }
        """)

    def _load_acts(self):
        """Load and display available acts."""
        try:
            acts_info = self.coordinator.get_available_acts()

            if not acts_info:
                self._show_empty_state()
                return

            self._hide_empty_state()
            self._clear_thumbnails()

            # Calculate grid layout
            cols = max(1, (self.width() - 40) // 180)  # 180 = thumbnail width + spacing

            for i, act_info in enumerate(acts_info):
                thumbnail = ActThumbnailWidget(act_info, self.content_widget)
                thumbnail.clicked.connect(self.act_selected.emit)

                row = i // cols
                col = i % cols

                self.content_layout.addWidget(thumbnail, row, col)
                self.thumbnail_widgets.append(thumbnail)

            logger.info(f"Loaded {len(acts_info)} acts in browser")

        except Exception as e:
            logger.exception(f"Failed to load acts: {e}")
            self._show_empty_state()

    def _clear_thumbnails(self):
        """Clear existing thumbnail widgets."""
        for thumbnail in self.thumbnail_widgets:
            thumbnail.setParent(None)
            thumbnail.deleteLater()

        self.thumbnail_widgets.clear()

    def _show_empty_state(self):
        """Show empty state message."""
        self.empty_label.show()

    def _hide_empty_state(self):
        """Hide empty state message."""
        self.empty_label.hide()

    def refresh(self):
        """Refresh the acts list."""
        logger.info("Refreshing acts browser")
        self._load_acts()

    def resizeEvent(self, event):
        """Handle resize events to adjust grid layout."""
        super().resizeEvent(event)

        # Reflow thumbnails on resize
        if self.thumbnail_widgets:
            self._reflow_thumbnails()

    def _reflow_thumbnails(self):
        """Reflow thumbnails in the grid after resize."""
        try:
            # Calculate new column count
            cols = max(1, (self.width() - 40) // 180)

            # Re-arrange thumbnails
            for i, thumbnail in enumerate(self.thumbnail_widgets):
                row = i // cols
                col = i % cols

                # Remove from current position and add to new position
                self.content_layout.addWidget(thumbnail, row, col)

        except Exception as e:
            logger.exception(f"Failed to reflow thumbnails: {e}")
