"""
Enhanced Export Preview Card - Proportional sizing without fixed dimensions

Uses Qt size policies and layout system for responsive sizing.
"""

from typing import Optional

from PyQt6.QtCore import Qt, QThread, QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout

from desktop.modern.domain.models.sequence_data import SequenceData


class PreviewGenerationWorker(QThread):
    """Worker thread for generating preview images without blocking UI."""

    preview_ready = pyqtSignal(QPixmap)
    preview_failed = pyqtSignal(str)

    def __init__(self, export_service, sequence, settings, parent=None):
        super().__init__(parent)
        self.export_service = export_service
        self.sequence = sequence
        self.settings = settings

    def run(self):
        """Generate preview in background thread."""
        try:
            # Convert settings to export options
            from datetime import datetime

            from desktop.modern.core.interfaces.image_export_services import (
                ImageExportOptions,
            )

            options = ImageExportOptions(
                add_word=self.settings.get("add_word", True),
                add_user_info=self.settings.get("add_user_info", True),
                add_difficulty_level=True,
                add_date=True,
                add_note=bool(self.settings.get("custom_note", "")),
                add_beat_numbers=self.settings.get("add_beat_numbers", True),
                add_reversal_symbols=self.settings.get("add_reversal_symbols", True),
                include_start_position=self.settings.get(
                    "include_start_position", True
                ),
                combined_grids=False,
                user_name=self.settings.get("user_name", "Default User"),
                export_date=datetime.now().strftime("%m-%d-%Y"),
                notes=self.settings.get("custom_note", ""),
                png_compression=1,
                high_quality=True,
            )

            # Convert sequence to export format
            sequence_data = (
                self.export_service._data_transformer.to_image_export_format(
                    self.sequence
                )
            )
            word = getattr(self.sequence, "word", "Preview")

            # Set up export container
            export_container = (
                self.export_service._container_manager.setup_export_container()
            )

            try:
                # Set as global container
                self.export_service._container_manager.set_as_global_container(
                    export_container
                )

                # Get image export service
                image_export_service = (
                    self.export_service._container_manager.get_image_export_service(
                        export_container
                    )
                )

                # Generate the actual export image
                q_image = image_export_service.create_sequence_image(
                    sequence_data, word, options
                )

                if q_image and not q_image.isNull():
                    # Convert to pixmap
                    pixmap = QPixmap.fromImage(q_image)
                    self.preview_ready.emit(pixmap)
                else:
                    self.preview_failed.emit("Failed to generate preview image")

            finally:
                # Restore original container
                self.export_service._container_manager.restore_original_container()

        except Exception as e:
            self.preview_failed.emit(f"Preview generation error: {str(e)}")


class EnhancedExportPreviewCard(QFrame):
    """
    Export preview card with responsive sizing using Qt layout system.
    """

    preview_update_requested = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("enhanced_export_preview_card")

        # Preview state
        self.current_sequence: Optional[SequenceData] = None
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

        # Use size policy for responsive sizing instead of fixed sizes
        self.preview_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.preview_label.setMinimumHeight(150)  # Just a reasonable minimum
        self.preview_label.setScaledContents(False)
        self.preview_label.setText("Create a sequence to see preview")

        layout.addWidget(self.preview_label, 1)  # Give it stretch

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
        """Apply responsive styling without fixed sizes."""
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
        """Set the export service for generating previews."""
        self.export_service = export_service
        print("🔌 [PREVIEW] Export service connected")

    def set_sequence_data(
        self, sequence: Optional[SequenceData], word: str = "Preview"
    ):
        """Set the current sequence data."""
        self.current_sequence = sequence
        self.current_word = word
        print(
            f"📊 [PREVIEW] Sequence data set: {sequence.length if sequence else 0} beats, word: {word}"
        )

        # Trigger preview generation if we have export service
        if sequence and sequence.beats and self.export_service:
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
            self.update_timer.start(500)  # Longer delay for settings changes

        self.set_status("Settings updated", "updating")

    def _generate_preview(self):
        """Generate real preview using export service."""
        if not self.export_service:
            self.set_status("Export service not available", "error")
            return

        if not self.current_sequence or not self.current_sequence.beats:
            self.preview_label.setText("Create a sequence to see preview")
            self.set_status("No sequence available", "ready")
            return

        # Cancel any existing worker
        if self.preview_worker and self.preview_worker.isRunning():
            self.preview_worker.terminate()
            self.preview_worker.wait()

        print(
            f"🖼️ [PREVIEW] Generating real preview with {len(self.current_sequence.beats)} beats"
        )
        self.set_status("Generating preview...", "updating")

        # Start worker thread to generate preview
        self.preview_worker = PreviewGenerationWorker(
            self.export_service, self.current_sequence, self.last_settings, self
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
            original_size = pixmap.size()
            settings_count = len(
                [k for k, v in self.last_settings.items() if isinstance(v, bool) and v]
            )
            format_name = self.last_settings.get("export_format", "PNG")
            quality = self.last_settings.get("export_quality", "300 DPI")

            self.info_label.setText(
                f"Export: {original_size.width()}×{original_size.height()} • "
                f"{format_name} • {quality} • {settings_count} options"
            )
            self.set_status("Preview ready", "ready")

            # Update style
            self.preview_label.style().unpolish(self.preview_label)
            self.preview_label.style().polish(self.preview_label)

            print(
                f"✅ [PREVIEW] Real preview generated: {original_size.width()}×{original_size.height()}"
            )

        except Exception as e:
            print(f"❌ [PREVIEW] Error displaying preview: {e}")
            self._on_preview_failed(f"Display error: {str(e)}")

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
