"""
Export Preview Card - Live preview display component

Handles the live preview of export output with real-time updates.
Part of the refactored export panel system.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget


class ExportPreviewCard(QFrame):
    """
    Export preview card containing live preview display.

    Provides:
    - Live preview of export output
    - Preview information and status
    - Real-time updates when settings change
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("export_preview_card")

        # Preview components
        self.preview_label = None
        self.info_label = None
        self.status_label = None

        # Preview state
        self.current_pixmap = None
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self._update_preview)

        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self):
        """Setup the UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel("Live Preview")
        title.setObjectName("subsection_title")
        title.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # Preview display
        self.preview_label = QLabel()
        self.preview_label.setObjectName("preview_display")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumHeight(200)
        self.preview_label.setScaledContents(False)
        self.preview_label.setText(
            "No preview available\nCreate a sequence to see preview"
        )
        layout.addWidget(self.preview_label)

        # Preview info
        self.info_label = QLabel()
        self.info_label.setObjectName("preview_info")
        self.info_label.setWordWrap(True)
        self.info_label.setText(
            "Preview will update automatically when settings change"
        )
        layout.addWidget(self.info_label)

        # Status label
        self.status_label = QLabel()
        self.status_label.setObjectName("preview_status")
        self.status_label.setText("Ready")
        layout.addWidget(self.status_label)

    def _apply_styling(self):
        """Apply glassmorphism styling."""
        self.setStyleSheet("""
            QFrame#export_preview_card {
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

            QLabel#preview_display {
                background: rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: rgba(255, 255, 255, 0.7);
                font-size: 13px;
                padding: 20px;
                min-height: 200px;
            }

            QLabel#preview_info {
                color: rgba(255, 255, 255, 0.7);
                font-size: 12px;
                background: transparent;
                border: none;
                margin-top: 5px;
            }

            QLabel#preview_status {
                color: rgba(100, 200, 255, 0.8);
                font-size: 11px;
                font-weight: 500;
                background: transparent;
                border: none;
                margin-top: 3px;
            }
        """)

    def update_preview(self, pixmap: QPixmap | None = None, delay_ms: int = 500):
        """
        Update the preview with optional delay for debouncing.

        Args:
            pixmap: New pixmap to display, or None to regenerate
            delay_ms: Delay in milliseconds before updating
        """
        if pixmap:
            self.current_pixmap = pixmap

        # Debounce updates
        self.update_timer.stop()
        self.update_timer.start(delay_ms)

        # Update status
        self.status_label.setText("Updating preview...")

    def _update_preview(self):
        """Internal method to actually update the preview display."""
        if self.current_pixmap and not self.current_pixmap.isNull():
            # Scale pixmap to fit preview area while maintaining aspect ratio
            scaled_pixmap = self.current_pixmap.scaled(
                self.preview_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.preview_label.setPixmap(scaled_pixmap)
            self.preview_label.setText("")

            # Update info
            size = self.current_pixmap.size()
            self.info_label.setText(f"Preview: {size.width()}x{size.height()} pixels")
            self.status_label.setText("Preview updated")
        else:
            # No preview available
            self.preview_label.clear()
            self.preview_label.setText(
                "No preview available\nCreate a sequence to see preview"
            )
            self.info_label.setText(
                "Preview will update automatically when settings change"
            )
            self.status_label.setText("No sequence")

    def set_preview_from_widget(self, widget: QWidget):
        """
        Generate preview from a widget (like the workbench).

        Args:
            widget: Widget to capture for preview
        """
        if widget and widget.isVisible():
            try:
                # Capture widget as pixmap
                pixmap = widget.grab()
                if not pixmap.isNull():
                    self.update_preview(pixmap)
                    return
            except Exception as e:
                print(f"Failed to capture preview: {e}")

        # Fallback to no preview
        self.update_preview(None)

    def set_status(self, status: str):
        """Set the status message."""
        self.status_label.setText(status)

    def clear_preview(self):
        """Clear the current preview."""
        self.current_pixmap = None
        self._update_preview()
