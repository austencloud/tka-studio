"""
Sequence Card Header Component

Modern implementation preserving exact legacy styling and functionality.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.core.interfaces.sequence_card_services import (
    ISequenceCardDisplayService,
    ISequenceCardExportService,
)


logger = logging.getLogger(__name__)


class SequenceCardHeaderComponent(QFrame):
    """Header component with exact legacy styling preserved."""

    export_requested = pyqtSignal()
    refresh_requested = pyqtSignal()
    regenerate_requested = pyqtSignal()

    def __init__(
        self,
        export_service: ISequenceCardExportService,
        display_service: ISequenceCardDisplayService,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.export_service = export_service
        self.display_service = display_service

        self._setup_ui()
        self._apply_legacy_styling()
        self._setup_connections()

    def _setup_ui(self) -> None:
        """Setup header UI with exact legacy layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)

        # Title label
        self.title_label = QLabel("Sequence Card Manager")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 0.5)
        self.title_label.setFont(title_font)
        layout.addWidget(self.title_label)

        # Description label
        self.description_label = QLabel("Select a sequence length to view cards")
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_font = QFont()
        desc_font.setPointSize(13)
        desc_font.setItalic(True)
        self.description_label.setFont(desc_font)
        layout.addWidget(self.description_label)

        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.setSpacing(10)

        # Action buttons
        self.export_button = self._create_action_button("Export All")
        self.refresh_button = self._create_action_button("Refresh")
        self.regenerate_button = self._create_action_button("Regenerate Images")

        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.regenerate_button)

        layout.addLayout(button_layout)

    def _create_action_button(self, text: str) -> QPushButton:
        """Create styled action button."""
        button = QPushButton(text)
        button.setMinimumWidth(100)
        button_font = QFont()
        button_font.setPointSize(12)
        button_font.setWeight(600)
        button.setFont(button_font)
        return button

    def _apply_legacy_styling(self) -> None:
        """Apply exact legacy styling."""
        self.setObjectName("sequenceCardHeader")
        self.setStyleSheet(
            """
            #sequenceCardHeader {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #34495e, stop:1 #2c3e50);
                border-radius: 10px;
                border: 1px solid #4a5568;
            }

            QLabel {
                color: #ffffff;
                background: transparent;
            }

            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: 1px solid #5dade2;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
                min-width: 100px;
            }

            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
            }

            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #1f618d);
            }

            QPushButton:disabled {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7f8c8d, stop:1 #95a5a6);
                color: #bdc3c7;
            }

            QProgressBar {
                border: none;
                border-radius: 6px;
                background: rgba(0, 0, 0, 0.15);
                height: 12px;
                text-align: center;
                color: rgba(255, 255, 255, 0.9);
                font-size: 10px;
                font-weight: bold;
            }

            QProgressBar::chunk {
                background: #3498db;
                border-radius: 6px;
            }
        """
        )

    def _setup_connections(self) -> None:
        """Setup button connections and service signals."""
        # Button connections
        self.export_button.clicked.connect(self._handle_export)
        self.refresh_button.clicked.connect(self._handle_refresh)
        self.regenerate_button.clicked.connect(self._handle_regenerate)

        # Service signal connections
        if hasattr(self.export_service, "export_progress_updated"):
            self.export_service.export_progress_updated.connect(
                self.update_export_progress
            )
        if hasattr(self.export_service, "export_completed"):
            self.export_service.export_completed.connect(self.export_completed)

        if hasattr(self.display_service, "loading_state_changed"):
            self.display_service.loading_state_changed.connect(self.set_loading_state)
        if hasattr(self.display_service, "progress_updated"):
            self.display_service.progress_updated.connect(self.update_progress)

    def _handle_export(self) -> None:
        """Handle export button click."""
        self.export_button.setEnabled(False)
        self.regenerate_button.setEnabled(False)
        self.description_label.setText("Exporting all sequence cards...")
        self.progress_bar.show()
        self.export_service.export_all_sequences()
        self.export_requested.emit()

    def _handle_refresh(self) -> None:
        """Handle refresh button click."""
        self.description_label.setText("Refreshing display...")
        self.refresh_requested.emit()

    def _handle_regenerate(self) -> None:
        """Handle regenerate button click."""
        self.export_button.setEnabled(False)
        self.regenerate_button.setEnabled(False)
        self.description_label.setText("Regenerating all images... Please wait")
        self.progress_bar.show()
        self.export_service.regenerate_all_images()
        self.regenerate_requested.emit()

    def set_loading_state(self, is_loading: bool) -> None:
        """Set loading state."""
        if is_loading:
            self.progress_bar.show()
            self.export_button.setEnabled(False)
            self.regenerate_button.setEnabled(False)
        else:
            self.progress_bar.hide()
            self.export_button.setEnabled(True)
            self.regenerate_button.setEnabled(True)

    def update_progress(self, current: int, total: int) -> None:
        """Update progress display."""
        if total > 0:
            percentage = int((current / total) * 100)
            self.progress_bar.setValue(percentage)
            self.description_label.setText(
                f"Loading... {current}/{total} ({percentage}%)"
            )

    def update_export_progress(self, current: int, total: int, message: str) -> None:
        """Update export progress."""
        if total > 0:
            percentage = int((current / total) * 100)
            self.progress_bar.setValue(percentage)
            self.description_label.setText(
                f"{message} {current}/{total} ({percentage}%)"
            )

    def export_completed(self, success: bool) -> None:
        """Handle export completion."""
        self.export_button.setEnabled(True)
        self.regenerate_button.setEnabled(True)
        self.progress_bar.hide()

        if success:
            self.description_label.setText("Export completed successfully!")
        else:
            self.description_label.setText("Export failed. Please try again.")

        # Reset message after 3 seconds
        QTimer.singleShot(
            3000,
            lambda: self.description_label.setText(
                "Select a sequence length to view cards"
            ),
        )

    def set_description_text(self, text: str) -> None:
        """Set description text."""
        self.description_label.setText(text)
