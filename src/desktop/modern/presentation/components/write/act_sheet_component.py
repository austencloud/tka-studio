"""
Act Sheet Component

Main component for editing acts, including header and sequence grid.
Displays the current act's sequences and provides editing capabilities.
"""

from __future__ import annotations

import logging
from typing import Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.core.interfaces.write_services import ActData, IWriteTabCoordinator


logger = logging.getLogger(__name__)


class ActHeaderComponent(QFrame):
    """Header component for act metadata editing."""

    act_info_changed = pyqtSignal(str, str)  # name, description
    music_load_requested = pyqtSignal()

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.current_act: ActData | None = None

        self._setup_ui()
        self._setup_styling()
        self._connect_signals()

    def _setup_ui(self):
        """Setup the header UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)

        # Title row
        title_layout = QHBoxLayout()

        # Act name editor
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Act Name")
        self.name_edit.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title_layout.addWidget(self.name_edit, 1)

        # Music button
        self.music_button = QPushButton("🎵 Load Music")
        self.music_button.setMinimumHeight(32)
        title_layout.addWidget(self.music_button)

        layout.addLayout(title_layout)

        # Description editor
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Act description...")
        self.description_edit.setMaximumHeight(80)
        self.description_edit.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.description_edit)

        # Info bar
        info_layout = QHBoxLayout()

        self.sequence_count_label = QLabel("0 sequences")
        self.sequence_count_label.setFont(QFont("Segoe UI", 9))
        info_layout.addWidget(self.sequence_count_label)

        info_layout.addStretch()

        self.music_status_label = QLabel("No music loaded")
        self.music_status_label.setFont(QFont("Segoe UI", 9))
        info_layout.addWidget(self.music_status_label)

        layout.addLayout(info_layout)

        # Initially disabled
        self.setEnabled(False)

    def _setup_styling(self):
        """Setup header styling."""
        self.setStyleSheet("""
            ActHeaderComponent {
                background: rgba(30, 30, 40, 0.9);
                border: 1px solid rgba(80, 80, 100, 0.3);
                border-radius: 6px;
            }
            QLineEdit {
                background: rgba(50, 50, 60, 0.8);
                border: 1px solid rgba(100, 100, 120, 0.5);
                border-radius: 4px;
                padding: 8px;
                color: rgba(255, 255, 255, 0.9);
            }
            QLineEdit:focus {
                border-color: rgba(100, 150, 200, 0.8);
            }
            QTextEdit {
                background: rgba(50, 50, 60, 0.8);
                border: 1px solid rgba(100, 100, 120, 0.5);
                border-radius: 4px;
                padding: 8px;
                color: rgba(255, 255, 255, 0.9);
            }
            QTextEdit:focus {
                border-color: rgba(100, 150, 200, 0.8);
            }
            QPushButton {
                background: rgba(70, 130, 180, 0.8);
                border: 1px solid rgba(100, 150, 200, 0.6);
                border-radius: 4px;
                padding: 6px 12px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(80, 140, 190, 0.9);
            }
            QPushButton:pressed {
                background: rgba(60, 120, 170, 0.9);
            }
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                background: transparent;
                border: none;
            }
        """)

    def _connect_signals(self):
        """Connect internal signals."""
        self.name_edit.textChanged.connect(self._on_info_changed)
        self.description_edit.textChanged.connect(self._on_info_changed)
        self.music_button.clicked.connect(self.music_load_requested.emit)

    def _on_info_changed(self):
        """Handle act info changes."""
        name = self.name_edit.text().strip()
        description = self.description_edit.toPlainText().strip()
        self.act_info_changed.emit(name, description)

    def set_act(self, act: ActData | None):
        """Set the current act to edit."""
        self.current_act = act

        if act is None:
            self.setEnabled(False)
            self._clear_fields()
        else:
            self.setEnabled(True)
            self._populate_fields(act)

    def _populate_fields(self, act: ActData):
        """Populate fields with act data."""
        # Temporarily disconnect signals to avoid triggering changes
        self.name_edit.textChanged.disconnect()
        self.description_edit.textChanged.disconnect()

        try:
            self.name_edit.setText(act.name)
            self.description_edit.setPlainText(act.description)

            # Update info labels
            seq_count = len(act.sequences)
            self.sequence_count_label.setText(
                f"{seq_count} sequence{'s' if seq_count != 1 else ''}"
            )

            if act.music_file:
                self.music_status_label.setText(f"♪ {act.music_file.name}")
                self.music_status_label.setStyleSheet(
                    "color: rgba(100, 200, 100, 0.9);"
                )
            else:
                self.music_status_label.setText("No music loaded")
                self.music_status_label.setStyleSheet(
                    "color: rgba(255, 255, 255, 0.6);"
                )

        finally:
            # Reconnect signals
            self.name_edit.textChanged.connect(self._on_info_changed)
            self.description_edit.textChanged.connect(self._on_info_changed)

    def _clear_fields(self):
        """Clear all fields."""
        self.name_edit.clear()
        self.description_edit.clear()
        self.sequence_count_label.setText("0 sequences")
        self.music_status_label.setText("No music loaded")
        self.music_status_label.setStyleSheet("color: rgba(255, 255, 255, 0.6);")

    def update_sequence_count(self, count: int):
        """Update the sequence count display."""
        self.sequence_count_label.setText(
            f"{count} sequence{'s' if count != 1 else ''}"
        )


class SequenceThumbnailWidget(QFrame):
    """Widget representing a sequence in the act."""

    clicked = pyqtSignal(int)  # position
    remove_requested = pyqtSignal(int)  # position

    def __init__(
        self, position: int, sequence_data: dict[str, Any], parent: QWidget = None
    ):
        super().__init__(parent)

        self.position = position
        self.sequence_data = sequence_data

        self._setup_ui()
        self._setup_styling()

    def _setup_ui(self):
        """Setup the thumbnail UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)

        # Header with position
        header_layout = QHBoxLayout()

        self.position_label = QLabel(f"#{self.position + 1}")
        self.position_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        header_layout.addWidget(self.position_label)

        header_layout.addStretch()

        # Remove button (×)
        self.remove_button = QPushButton("×")
        self.remove_button.setFixedSize(18, 18)
        self.remove_button.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.remove_button.clicked.connect(
            lambda: self.remove_requested.emit(self.position)
        )
        header_layout.addWidget(self.remove_button)

        layout.addLayout(header_layout)

        # Sequence preview (placeholder)
        self.preview_label = QLabel("🎭")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setFont(QFont("Segoe UI", 20))
        self.preview_label.setMinimumSize(100, 70)
        layout.addWidget(self.preview_label, 1)

        # Sequence info
        beats_count = len(self.sequence_data.get("beats", []))
        self.info_label = QLabel(f"{beats_count} beats")
        self.info_label.setFont(QFont("Segoe UI", 8))
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)

        self.setFixedSize(120, 110)

    def _setup_styling(self):
        """Setup thumbnail styling."""
        self.setStyleSheet("""
            SequenceThumbnailWidget {
                background: rgba(50, 50, 60, 0.8);
                border: 2px solid rgba(80, 80, 100, 0.5);
                border-radius: 6px;
            }
            SequenceThumbnailWidget:hover {
                background: rgba(70, 70, 80, 0.9);
                border-color: rgba(120, 120, 140, 0.8);
            }
            QPushButton {
                background: rgba(200, 80, 80, 0.8);
                border: none;
                border-radius: 9px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(220, 100, 100, 0.9);
            }
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                background: transparent;
                border: none;
            }
        """)

    def mousePressEvent(self, event):
        """Handle thumbnail click."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.position)
        super().mousePressEvent(event)


class SequenceGridComponent(QScrollArea):
    """Component for displaying sequences in a grid."""

    sequence_clicked = pyqtSignal(int)  # position
    sequence_remove_requested = pyqtSignal(int)  # position

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.sequence_widgets: list[SequenceThumbnailWidget] = []

        self._setup_ui()
        self._setup_styling()

    def _setup_ui(self):
        """Setup the grid UI."""
        # Content widget
        self.content_widget = QWidget()
        self.content_layout = QGridLayout(self.content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(10)

        # Configure scroll area
        self.setWidget(self.content_widget)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Empty state
        self.empty_label = QLabel(
            "No sequences in this act\n\nAdd sequences from the Construct tab"
        )
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setFont(QFont("Segoe UI", 12))
        self.empty_label.setStyleSheet("color: rgba(255, 255, 255, 0.6);")
        self.content_layout.addWidget(self.empty_label, 0, 0)

    def _setup_styling(self):
        """Setup grid styling."""
        self.setStyleSheet("""
            SequenceGridComponent {
                background: rgba(25, 25, 35, 0.8);
                border: 1px solid rgba(60, 60, 80, 0.3);
                border-radius: 4px;
            }
            QScrollBar {
                background: rgba(40, 40, 50, 0.5);
                border-radius: 6px;
            }
            QScrollBar::handle {
                background: rgba(100, 100, 120, 0.8);
                border-radius: 6px;
                min-height: 20px;
                min-width: 20px;
            }
            QScrollBar::handle:hover {
                background: rgba(120, 120, 140, 0.9);
            }
        """)

    def set_sequences(self, sequences: list[dict[str, Any]]):
        """Set the sequences to display."""
        self._clear_widgets()

        if not sequences:
            self.empty_label.show()
            return

        self.empty_label.hide()

        # Calculate grid dimensions
        cols = max(1, (self.width() - 40) // 140)  # 140 = widget width + spacing

        for i, sequence_data in enumerate(sequences):
            widget = SequenceThumbnailWidget(i, sequence_data, self.content_widget)
            widget.clicked.connect(self.sequence_clicked.emit)
            widget.remove_requested.connect(self.sequence_remove_requested.emit)

            row = i // cols
            col = i % cols

            self.content_layout.addWidget(widget, row, col)
            self.sequence_widgets.append(widget)

        logger.debug(f"Displayed {len(sequences)} sequences in grid")

    def _clear_widgets(self):
        """Clear existing sequence widgets."""
        for widget in self.sequence_widgets:
            widget.setParent(None)
            widget.deleteLater()

        self.sequence_widgets.clear()


class ActSheetComponent(QFrame):
    """
    Main act sheet component combining header and sequence grid.

    Provides the main editing interface for acts.
    """

    act_info_changed = pyqtSignal(str, str)  # name, description
    music_load_requested = pyqtSignal()
    sequence_clicked = pyqtSignal(int)  # position
    sequence_remove_requested = pyqtSignal(int)  # position

    def __init__(self, coordinator: IWriteTabCoordinator, parent: QWidget = None):
        super().__init__(parent)

        self.coordinator = coordinator

        self._setup_ui()
        self._setup_styling()
        self._connect_signals()

    def _setup_ui(self):
        """Setup the act sheet UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Act header
        self.header = ActHeaderComponent()
        layout.addWidget(self.header)

        # Sequence grid
        self.sequence_grid = SequenceGridComponent()
        layout.addWidget(self.sequence_grid, 1)

    def _setup_styling(self):
        """Setup act sheet styling."""
        self.setStyleSheet("""
            ActSheetComponent {
                background: transparent;
                border: none;
            }
        """)

    def _connect_signals(self):
        """Connect component signals."""
        self.header.act_info_changed.connect(self.act_info_changed.emit)
        self.header.music_load_requested.connect(self.music_load_requested.emit)
        self.sequence_grid.sequence_clicked.connect(self.sequence_clicked.emit)
        self.sequence_grid.sequence_remove_requested.connect(
            self.sequence_remove_requested.emit
        )

    def set_act(self, act: ActData | None):
        """Set the current act to display."""
        self.header.set_act(act)

        if act is None:
            self.sequence_grid.set_sequences([])
        else:
            self.sequence_grid.set_sequences(act.sequences)

    def refresh_sequences(self):
        """Refresh the sequence grid display."""
        current_act = self.coordinator.get_current_act()
        if current_act:
            self.sequence_grid.set_sequences(current_act.sequences)
            self.header.update_sequence_count(len(current_act.sequences))
