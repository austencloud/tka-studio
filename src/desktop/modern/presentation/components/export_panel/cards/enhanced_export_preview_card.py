"""
Enhanced Export Preview Card - Simplified preview generation

Creates a fallback preview that shows sequence information instead of trying
to use the complex export service which has method signature issues.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, QThread, QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QColor, QFont, QImage, QPainter, QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout

from desktop.modern.domain.models.sequence_data import SequenceData


class PreviewGenerationWorker(QThread):
    """Worker thread for generating simple preview images."""

    preview_ready = pyqtSignal(QPixmap)
    preview_failed = pyqtSignal(str)

    def __init__(self, sequence, settings, parent=None):
        super().__init__(parent)
        self.sequence = sequence
        self.settings = settings

    def run(self):
        """Generate a simple preview showing sequence info."""
        try:
            # Create a simple preview image showing sequence information
            pixmap = self._create_sequence_info_preview()
            self.preview_ready.emit(pixmap)

        except Exception as e:
            self.preview_failed.emit(f"Preview generation error: {e!s}")

    def _create_sequence_info_preview(self) -> QPixmap:
        """Create a simple preview showing sequence information."""
        # Create a reasonably sized image
        width, height = 400, 300
        image = QImage(width, height, QImage.Format.Format_ARGB32)
        image.fill(QColor(40, 40, 40))  # Dark background

        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set up fonts
        title_font = QFont("Inter", 16, QFont.Weight.Bold)
        info_font = QFont("Inter", 12)

        # Draw title
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(title_font)
        title_rect = painter.fontMetrics().boundingRect("Export Preview")
        title_x = (width - title_rect.width()) // 2
        painter.drawText(title_x, 40, "Export Preview")

        # Draw sequence info
        painter.setFont(info_font)
        y_pos = 80

        # Sequence details
        word = getattr(self.sequence, "word", "Sequence")
        beat_count = len(self.sequence.beats) if self.sequence.beats else 0

        info_lines = [
            f"Word: {word}",
            f"Beats: {beat_count}",
            "",
            "Export Settings:",
        ]

        # Add settings info
        for key, value in self.settings.items():
            if isinstance(value, bool) and value:
                display_key = key.replace("_", " ").title()
                info_lines.append(f"✓ {display_key}")
            elif (
                isinstance(value, str)
                and value
                and key in ["export_format", "export_quality", "user_name"]
            ):
                display_key = key.replace("_", " ").title()
                info_lines.append(f"{display_key}: {value}")

        # Draw info lines
        painter.setPen(QColor(200, 200, 200))
        line_height = painter.fontMetrics().height() + 4

        for line in info_lines:
            if line.startswith("✓"):
                painter.setPen(QColor(100, 255, 150))  # Green for enabled options
            elif line.endswith(":") and not line.startswith("✓"):
                painter.setPen(QColor(255, 255, 255))  # White for headers
            else:
                painter.setPen(QColor(200, 200, 200))  # Gray for values

            painter.drawText(20, y_pos, line)
            y_pos += line_height

        # Draw a simple border
        painter.setPen(QColor(100, 150, 255, 100))
        painter.drawRect(10, 10, width - 20, height - 20)

        painter.end()

        return QPixmap.fromImage(image)


class EnhancedExportPreviewCard(QFrame):
    """
    Export preview card with simplified preview generation.
    """

    preview_update_requested = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("enhanced_export_preview_card")

        # Preview state
        self.current_sequence: SequenceData | None = None
        self.current_word: str = "Preview"
        self.last_settings = {}
        self.export_service = None

        # Worker thread for preview generation
        self.preview_worker = None

        # Update timer for debouncing
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self._generate_preview)

        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self):
        """Setup UI with responsive sizing."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Title
        title = QLabel("Live Preview")
        title.setObjectName("preview_title")
        title.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # Preview display with responsive sizing
        self.preview_label = QLabel()
        self.preview_label.setObjectName("preview_display")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Use size policy for responsive sizing
        self.preview_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.preview_label.setMinimumHeight(150)
        self.preview_label.setScaledContents(False)
        self.preview_label.setText("Create a sequence to see preview")

        layout.addWidget(self.preview_label, 1)

        # Compact status info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(3)

        self.info_label = QLabel()
        self.info_label.setObjectName("preview_info")
        self.info_label.setWordWrap(True)
        self.info_label.setText(
            "Preview will show current sequence with selected settings"
        )
        info_layout.addWidget(self.info_label)

        self.status_label = QLabel()
        self.status_label.setObjectName("preview_status")
        self.status_label.setText("Ready")
        info_layout.addWidget(self.status_label)

        layout.addLayout(info_layout)

    def _apply_styling(self):
        """Apply responsive styling."""
        self.setStyleSheet("""
            QFrame#enhanced_export_preview_card {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 12px;
                margin: 2px;
            }

            QLabel#preview_title {
                color: rgba(255, 255, 255, 0.95);
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 5px;
                background: transparent;
                border: none;
            }

            QLabel#preview_display {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(30, 30, 30, 0.7),
                    stop:1 rgba(20, 20, 20, 0.8));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: rgba(255, 255, 255, 0.8);
                font-size: 13px;
                padding: 10px;
                min-height: 150px;
            }

            QLabel#preview_display[hasPixmap="true"] {
                border: 2px solid rgba(100, 200, 255, 0.3);
                background: rgba(0, 0, 0, 0.3);
                padding: 5px;
            }

            QLabel#preview_info {
                color: rgba(255, 255, 255, 0.7);
                font-size: 11px;
                background: transparent;
                border: none;
                margin-top: 3px;
            }

            QLabel#preview_status {
                color: rgba(100, 200, 255, 0.9);
                font-size: 10px;
                font-weight: 500;
                background: transparent;
                border: none;
                margin-top: 2px;
            }
        """)

    def set_export_service(self, export_service):
        """Set the export service (for compatibility)."""
        self.export_service = export_service
        print("[PREVIEW] Export service connected (fallback preview mode)")

    def set_sequence_data(self, sequence: SequenceData | None, word: str = "Preview"):
        """Set the current sequence data."""
        self.current_sequence = sequence
        self.current_word = word


        # Trigger preview generation if we have a sequence
        if sequence and sequence.beats:
            self._generate_preview()
        else:
            self.preview_label.setText("Create a sequence to see preview")
            self.set_status("No sequence", "ready")

    def update_preview_settings(self, settings: dict, immediate: bool = False):
        """Update preview with new settings."""
        self.last_settings = settings.copy()

        if immediate:
            self._generate_preview()
        else:
            self.update_timer.start(300)

        self.set_status("Settings updated", "updating")

    def _generate_preview(self):
        """Generate simplified preview."""
        if not self.current_sequence or not self.current_sequence.beats:
            self.preview_label.setText("Create a sequence to see preview")
            self.set_status("No sequence available", "ready")
            return

        # Cancel any existing worker
        if self.preview_worker and self.preview_worker.isRunning():
            self.preview_worker.terminate()
            self.preview_worker.wait()

        print(
            f"🖼️ [PREVIEW] Generating preview with {len(self.current_sequence.beats)} beats"
        )
        self.set_status("Generating preview...", "updating")

        # Start worker thread to generate preview
        self.preview_worker = PreviewGenerationWorker(
            self.current_sequence, self.last_settings, self
        )
        self.preview_worker.preview_ready.connect(self._on_preview_ready)
        self.preview_worker.preview_failed.connect(self._on_preview_failed)
        self.preview_worker.start()

    @pyqtSlot(QPixmap)
    def _on_preview_ready(self, pixmap):
        """Handle preview image ready."""
        try:
            # Scale to fit available space while maintaining aspect ratio
            available_size = self.preview_label.size()
            if available_size.width() > 50 and available_size.height() > 50:
                scaled_pixmap = pixmap.scaled(
                    available_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            else:
                # Use a reasonable default if size isn't available yet
                scaled_pixmap = pixmap.scaled(
                    400,
                    300,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

            self.preview_label.setPixmap(scaled_pixmap)
            self.preview_label.setText("")
            self.preview_label.setProperty("hasPixmap", True)

            # Update info
            settings_count = len(
                [k for k, v in self.last_settings.items() if isinstance(v, bool) and v]
            )
            format_name = self.last_settings.get("export_format", "PNG")
            quality = self.last_settings.get("export_quality", "300 DPI")

            self.info_label.setText(
                f"Preview: {format_name} • {quality} • {settings_count} options enabled"
            )
            self.set_status("Preview ready", "ready")

            # Update style
            self.preview_label.style().unpolish(self.preview_label)
            self.preview_label.style().polish(self.preview_label)

            print("✅ [PREVIEW] Preview generated successfully")

        except Exception as e:
            print(f"❌ [PREVIEW] Error displaying preview: {e}")
            self._on_preview_failed(f"Display error: {e!s}")

    @pyqtSlot(str)
    def _on_preview_failed(self, error_message):
        """Handle preview generation failure."""
        print(f"❌ [PREVIEW] Preview generation failed: {error_message}")

        self.preview_label.clear()
        self.preview_label.setPixmap(QPixmap())
        self.preview_label.setText(f"Preview failed:\n{error_message}")
        self.preview_label.setProperty("hasPixmap", False)

        self.info_label.setText("Unable to generate preview")
        self.set_status(f"Error: {error_message}", "error")

        # Update style
        self.preview_label.style().unpolish(self.preview_label)
        self.preview_label.style().polish(self.preview_label)

    def set_status(self, status: str, status_type: str = "ready"):
        """Set the status message."""
        self.status_label.setText(status)
        self.status_label.setProperty("status", status_type)

    def clear_preview(self):
        """Clear the current preview."""
        self.preview_label.clear()
        self.preview_label.setPixmap(QPixmap())
        self.preview_label.setText("Create a sequence to see preview")
        self.preview_label.setProperty("hasPixmap", False)
        self.set_status("Ready", "ready")

        # Update style
        self.preview_label.style().unpolish(self.preview_label)
        self.preview_label.style().polish(self.preview_label)
