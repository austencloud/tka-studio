"""
Modern Sequence Viewer Panel

A clean, modern sequence viewer with glassmorphism styling.
Displays selected sequences with image preview, metadata, and action buttons.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.application.services.browse.browse_state_service import (
    BrowseStateService,
)
from desktop.modern.domain.models.sequence_data import SequenceData


class ModernSequenceImageViewer(QFrame):
    """Modern image viewer with navigation controls."""

    # Signals
    variation_changed = pyqtSignal(int)  # variation_index

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.current_thumbnails: list[str] = []
        self.current_index = 0

        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self) -> None:
        """Setup the image viewer UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Image display area
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(300, 200)
        self.image_label.setScaledContents(False)
        layout.addWidget(self.image_label)

        # Navigation controls
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(10)

        self.prev_button = QPushButton("◀")
        self.prev_button.setFixedSize(32, 32)
        self.prev_button.clicked.connect(self._prev_variation)

        self.variation_label = QLabel("1 / 1")
        self.variation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.variation_label.setMinimumWidth(60)

        self.next_button = QPushButton("▶")
        self.next_button.setFixedSize(32, 32)
        self.next_button.clicked.connect(self._next_variation)

        nav_layout.addStretch()
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.variation_label)
        nav_layout.addWidget(self.next_button)
        nav_layout.addStretch()

        layout.addLayout(nav_layout)

        # Set default state
        self._show_placeholder()

    def _apply_styling(self) -> None:
        """Apply modern styling to the image viewer."""
        self.setStyleSheet(
            """
            ModernSequenceImageViewer {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
            }

            QLabel {
                color: rgba(255, 255, 255, 0.8);
                background: transparent;
                border: none;
            }

            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }

            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }

            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.15);
            }

            QPushButton:disabled {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                color: rgba(255, 255, 255, 0.3);
            }
        """
        )

    def _show_placeholder(self) -> None:
        """Show placeholder when no image is selected."""
        self.image_label.setText("🎭\n\nSelect a sequence\nto view details")
        self.image_label.setStyleSheet(
            """
            QLabel {
                color: rgba(255, 255, 255, 0.5);
                font-size: 16px;
                font-weight: bold;
                text-align: center;
            }
        """
        )
        self.variation_label.setText("0 / 0")
        self.prev_button.setEnabled(False)
        self.next_button.setEnabled(False)

    def set_thumbnails(self, thumbnails: list[str]) -> None:
        """Set the thumbnails for navigation."""
        self.current_thumbnails = thumbnails
        self.current_index = 0

        if not thumbnails:
            self._show_placeholder()
            return

        self._update_display()

    def _update_display(self) -> None:
        """Update the current image display."""
        if not self.current_thumbnails:
            self._show_placeholder()
            return

        # Load and display current image
        current_path = self.current_thumbnails[self.current_index]
        pixmap = QPixmap(current_path)

        if not pixmap.isNull():
            # Scale image to fit while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setStyleSheet("QLabel { color: white; }")
        else:
            self.image_label.setText("❌\n\nImage not found")
            self.image_label.setStyleSheet(
                "QLabel { color: rgba(255, 100, 100, 0.8); }"
            )

        # Update navigation
        total = len(self.current_thumbnails)
        self.variation_label.setText(f"{self.current_index + 1} / {total}")
        self.prev_button.setEnabled(self.current_index > 0)
        self.next_button.setEnabled(self.current_index < total - 1)

    def _prev_variation(self) -> None:
        """Go to previous variation."""
        if self.current_index > 0:
            self.current_index -= 1
            self._update_display()
            self.variation_changed.emit(self.current_index)

    def _next_variation(self) -> None:
        """Go to next variation."""
        if self.current_index < len(self.current_thumbnails) - 1:
            self.current_index += 1
            self._update_display()
            self.variation_changed.emit(self.current_index)


class ModernSequenceMetadata(QFrame):
    """Modern metadata display panel."""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self) -> None:
        """Setup the metadata UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Title
        self.title_label = QLabel("Sequence Details")
        self.title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(self.title_label)

        # Metadata container
        self.metadata_container = QWidget()
        self.metadata_layout = QVBoxLayout(self.metadata_container)
        self.metadata_layout.setContentsMargins(0, 0, 0, 0)
        self.metadata_layout.setSpacing(6)

        # Scroll area for metadata
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.metadata_container)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        layout.addWidget(scroll_area)

        # Set default state
        self._show_placeholder()

    def _apply_styling(self) -> None:
        """Apply modern styling to the metadata panel."""
        self.setStyleSheet(
            """
            ModernSequenceMetadata {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
            }

            QLabel {
                color: rgba(255, 255, 255, 0.8);
                background: transparent;
                border: none;
            }

            QScrollArea {
                background: transparent;
                border: none;
            }

            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.1);
                width: 12px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.3);
                border-radius: 6px;
            }
        """
        )

    def _show_placeholder(self) -> None:
        """Show placeholder when no sequence is selected."""
        self._clear_metadata()
        placeholder = QLabel("Select a sequence to view details")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: rgba(255, 255, 255, 0.5);")
        self.metadata_layout.addWidget(placeholder)

    def _clear_metadata(self) -> None:
        """Clear all metadata widgets."""
        while self.metadata_layout.count():
            child = self.metadata_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def set_sequence_data(self, sequence_data: SequenceData) -> None:
        """Set the sequence data to display."""
        self._clear_metadata()

        # Create metadata items
        metadata_items = [
            ("Word", sequence_data.word or "Unknown"),
            ("Length", str(sequence_data.sequence_length)),
            ("Level", getattr(sequence_data, "difficulty_level", "Unknown")),
            (
                "Variations",
                str(len(sequence_data.thumbnails) if sequence_data.thumbnails else 0),
            ),
            ("Date Added", getattr(sequence_data, "date_added", "Unknown")),
            ("Author", getattr(sequence_data, "author", "Unknown")),
        ]

        for label, value in metadata_items:
            self._add_metadata_item(label, value)

    def _add_metadata_item(self, label: str, value: str) -> None:
        """Add a metadata item to the display."""
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(0, 0, 0, 0)
        item_layout.setSpacing(8)

        # Label
        label_widget = QLabel(f"{label}:")
        label_widget.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        label_widget.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        label_widget.setMinimumWidth(80)

        # Value
        value_widget = QLabel(str(value))
        value_widget.setFont(QFont("Segoe UI", 10))
        value_widget.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        value_widget.setWordWrap(True)

        item_layout.addWidget(label_widget)
        item_layout.addWidget(value_widget, 1)

        self.metadata_layout.addWidget(item_widget)


class ModernSequenceActionPanel(QFrame):
    """Modern action button panel."""

    # Signals
    edit_sequence = pyqtSignal(str)  # sequence_id
    save_image = pyqtSignal(str)  # sequence_id
    delete_variation = pyqtSignal(str, int)  # sequence_id, variation_index
    view_fullscreen = pyqtSignal(str, int)  # sequence_id, variation_index

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.current_sequence_id: str | None = None
        self.current_variation_index = 0

        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self) -> None:
        """Setup the action panel UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Action buttons
        self.edit_button = QPushButton("✏️ Edit")
        self.edit_button.setMinimumSize(80, 36)
        self.edit_button.clicked.connect(self._on_edit_clicked)

        self.save_button = QPushButton("💾 Save")
        self.save_button.setMinimumSize(80, 36)
        self.save_button.clicked.connect(self._on_save_clicked)

        self.delete_button = QPushButton("🗑️ Delete")
        self.delete_button.setMinimumSize(80, 36)
        self.delete_button.clicked.connect(self._on_delete_clicked)

        self.fullscreen_button = QPushButton("🔍 View")
        self.fullscreen_button.setMinimumSize(80, 36)
        self.fullscreen_button.clicked.connect(self._on_fullscreen_clicked)

        layout.addWidget(self.edit_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.fullscreen_button)

        # Set initial state
        self._set_buttons_enabled(False)

    def _apply_styling(self) -> None:
        """Apply modern styling to the action panel."""
        self.setStyleSheet(
            """
            ModernSequenceActionPanel {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
            }

            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: white;
                font-weight: bold;
                font-size: 11px;
                padding: 8px 12px;
            }

            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }

            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.15);
            }

            QPushButton:disabled {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                color: rgba(255, 255, 255, 0.3);
            }
        """
        )

    def set_sequence(self, sequence_id: str, variation_index: int = 0) -> None:
        """Set the current sequence and variation."""
        self.current_sequence_id = sequence_id
        self.current_variation_index = variation_index
        self._set_buttons_enabled(True)

    def clear_sequence(self) -> None:
        """Clear the current sequence."""
        self.current_sequence_id = None
        self.current_variation_index = 0
        self._set_buttons_enabled(False)

    def _set_buttons_enabled(self, enabled: bool) -> None:
        """Enable or disable all action buttons."""
        self.edit_button.setEnabled(enabled)
        self.save_button.setEnabled(enabled)
        self.delete_button.setEnabled(enabled)
        self.fullscreen_button.setEnabled(enabled)

    def _on_edit_clicked(self) -> None:
        """Handle edit button click."""
        if self.current_sequence_id:
            self.edit_sequence.emit(self.current_sequence_id)

    def _on_save_clicked(self) -> None:
        """Handle save button click."""
        if self.current_sequence_id:
            self.save_image.emit(self.current_sequence_id)

    def _on_delete_clicked(self) -> None:
        """Handle delete button click."""
        if self.current_sequence_id:
            self.delete_variation.emit(
                self.current_sequence_id, self.current_variation_index
            )

    def _on_fullscreen_clicked(self) -> None:
        """Handle fullscreen button click."""
        if self.current_sequence_id:
            self.view_fullscreen.emit(
                self.current_sequence_id, self.current_variation_index
            )


class ModernSequenceViewerPanel(QFrame):
    """
    Modern sequence viewer panel with clean glassmorphism design.

    Features:
    - Image viewer with navigation
    - Metadata display
    - Action buttons
    - Modern styling
    """

    # Signals
    sequence_action = pyqtSignal(str, str)  # action_type, sequence_id
    back_to_browser = pyqtSignal()

    def __init__(
        self, state_service: BrowseStateService, parent: QWidget | None = None
    ):
        super().__init__(parent)

        self.state_service = state_service
        self.current_sequence_data: SequenceData | None = None

        self._setup_ui()
        self._apply_styling()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Setup the viewer panel UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header
        header_layout = QHBoxLayout()
        # center the contents
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.setSpacing(12)

        # Title
        self.title_label = QLabel("Sequence Viewer")
        self.title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: white;")
        header_layout.addWidget(self.title_label)
        layout.addLayout(header_layout)

        # Image viewer
        self.image_viewer = ModernSequenceImageViewer()
        layout.addWidget(self.image_viewer, 1)  # Take most of the space

        # Metadata panel
        self.metadata_panel = ModernSequenceMetadata()
        self.metadata_panel.setMaximumHeight(200)
        layout.addWidget(self.metadata_panel)

        # Action panel
        self.action_panel = ModernSequenceActionPanel()
        layout.addWidget(self.action_panel)

    def _apply_styling(self) -> None:
        """Apply modern glassmorphism styling."""
        self.setStyleSheet(
            """
            ModernSequenceViewerPanel {
                background: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
            }
        """
        )

    def _connect_signals(self) -> None:
        """Connect component signals."""
        self.image_viewer.variation_changed.connect(self._on_variation_changed)

        # Action panel signals
        self.action_panel.edit_sequence.connect(
            lambda seq_id: self.sequence_action.emit("edit", seq_id)
        )
        self.action_panel.save_image.connect(
            lambda seq_id: self.sequence_action.emit("save", seq_id)
        )
        self.action_panel.delete_variation.connect(
            lambda seq_id, idx: self.sequence_action.emit("delete", seq_id)
        )
        self.action_panel.view_fullscreen.connect(
            lambda seq_id, idx: self.sequence_action.emit("fullscreen", seq_id)
        )

    def show_sequence(self, sequence_data: SequenceData) -> None:
        """Display a sequence in the viewer."""
        self.current_sequence_data = sequence_data

        # Update title
        self.title_label.setText(f"Sequence: {sequence_data.word or 'Unknown'}")

        # Update image viewer
        thumbnails = sequence_data.thumbnails if sequence_data.thumbnails else []
        self.image_viewer.set_thumbnails(thumbnails)

        # Update metadata
        self.metadata_panel.set_sequence_data(sequence_data)

        # Update action panel
        self.action_panel.set_sequence(sequence_data.id)

        print(f"🎭 Sequence viewer showing: {sequence_data.word} ({sequence_data.id})")

    def clear_sequence(self) -> None:
        """Clear the current sequence display."""
        self.current_sequence_data = None

        # Reset title
        self.title_label.setText("Sequence Viewer")

        # Clear components
        self.image_viewer.set_thumbnails([])
        self.metadata_panel._show_placeholder()
        self.action_panel.clear_sequence()

        print("🎭 Sequence viewer cleared")

    def _on_variation_changed(self, variation_index: int) -> None:
        """Handle variation change in image viewer."""
        if self.current_sequence_data:
            self.action_panel.current_variation_index = variation_index
            print(f"🎭 Variation changed to: {variation_index}")
