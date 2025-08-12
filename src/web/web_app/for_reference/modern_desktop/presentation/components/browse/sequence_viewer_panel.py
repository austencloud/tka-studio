"""
Sequence Viewer Panel - Right Side Component

Matches the Legacy sequence_viewer component that displays selected sequences.
Takes up 1/3 of the browse tab width (33.3%).
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget


class SequenceViewerPanel(QWidget):
    """
    Right-side panel for displaying selected sequences in detail.

    Matches Legacy SequenceViewer component functionality.
    """

    # Signals
    sequence_opened = pyqtSignal(str)  # sequence_id

    def __init__(self, parent: QWidget | None = None):
        """Initialize the sequence viewer panel."""
        super().__init__(parent)
        self.current_sequence_id: str | None = None

        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self) -> None:
        """Setup the UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header
        self.header_label = QLabel("Sequence Viewer")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setBold(True)
        font.setPointSize(14)
        self.header_label.setFont(font)

        # Content area
        self.content_frame = QFrame()
        self.content_frame.setFrameStyle(QFrame.Shape.StyledPanel)

        # Default content
        self.default_label = QLabel("Select a sequence to view details")
        self.default_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.default_label.setWordWrap(True)

        # Layout content frame
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.addWidget(self.default_label)

        # Add to main layout
        layout.addWidget(self.header_label)
        layout.addWidget(self.content_frame, 1)  # Expand to fill space

    def _apply_styling(self) -> None:
        """Apply glassmorphism styling to match Legacy modern look."""
        self.setStyleSheet(
            """
            SequenceViewerPanel {
                background: rgba(255, 255, 255, 0.02);
                border-left: 1px solid rgba(255, 255, 255, 0.1);
            }

            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 12px;
            }

            QLabel {
                color: rgba(255, 255, 255, 0.8);
                background: transparent;
                border: none;
            }
        """
        )

    def show_sequence(self, sequence_id: str, sequence_data: dict) -> None:
        """Display a selected sequence."""
        self.current_sequence_id = sequence_id

        # Clear default content
        self.default_label.hide()

        # Create sequence details (placeholder for now)
        details_label = QLabel(f"Sequence: {sequence_id}\nDetails coming soon...")
        details_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        details_label.setWordWrap(True)

        # Update content
        content_layout = self.content_frame.layout()
        content_layout.addWidget(details_label)

        print(f"🔍 Sequence viewer showing: {sequence_id}")

    def clear_sequence(self) -> None:
        """Clear the current sequence display."""
        self.current_sequence_id = None

        # Clear content and show default
        content_layout = self.content_frame.layout()
        while content_layout.count():
            child = content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        content_layout.addWidget(self.default_label)
        self.default_label.show()

        print("🔍 Sequence viewer cleared")
