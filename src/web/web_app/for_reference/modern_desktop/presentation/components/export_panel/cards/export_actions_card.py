"""
Export Actions Card - Export buttons component

Handles the export action button for current sequence.
Part of the refactored export panel system.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout


class ExportActionsCard(QFrame):
    """
    Export actions card containing export button.

    Provides button for:
    - Export current sequence (replaces the save image button)
    """

    # Signals
    export_current_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("export_actions_card")

        # Button reference
        self.export_current_btn = None

        self._setup_ui()
        self._setup_connections()
        self._apply_styling()

    def _setup_ui(self):
        """Setup the UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel("Export Actions")
        title.setObjectName("subsection_title")
        title.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # Export current sequence button (replaces save image button)
        self.export_current_btn = QPushButton("🔤 Export Current Sequence")
        self.export_current_btn.setObjectName("action_button")
        self.export_current_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        layout.addWidget(self.export_current_btn)

    def _setup_connections(self):
        """Setup signal connections."""
        self.export_current_btn.clicked.connect(self.export_current_requested.emit)

    def _apply_styling(self):
        """Apply glassmorphism styling."""
        self.setStyleSheet("""
            QFrame#export_actions_card {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                margin: 5px;
            }

            QLabel#subsection_title {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 10px;
                background: transparent;
                border: none;
            }

            QPushButton#action_button {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(100, 200, 255, 0.8),
                    stop:1 rgba(50, 150, 255, 0.6));
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: white;
                font-size: 14px;
                font-weight: 600;
                padding: 12px 20px;
                margin: 3px;
            }

            QPushButton#action_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(120, 220, 255, 0.9),
                    stop:1 rgba(70, 170, 255, 0.7));
                border: 1px solid rgba(255, 255, 255, 0.3);
            }

            QPushButton#action_button:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(80, 180, 255, 0.7),
                    stop:1 rgba(30, 130, 255, 0.5));
            }

            QPushButton#action_button:disabled {
                background: rgba(100, 100, 100, 0.3);
                color: rgba(255, 255, 255, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }

            QPushButton#secondary_button {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                font-weight: 500;
                padding: 10px 20px;
                margin: 3px;
            }

            QPushButton#secondary_button:hover {
                background: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: white;
            }

            QPushButton#secondary_button:pressed {
                background: rgba(255, 255, 255, 0.08);
            }
        """)

    def set_export_current_loading(self, loading: bool):
        """Set the export current button to loading state."""
        if loading:
            self.export_current_btn.setText("🔄 Exporting...")
            self.export_current_btn.setEnabled(False)
        else:
            self.export_current_btn.setText("🔤 Export Current Sequence")
            self.export_current_btn.setEnabled(True)
