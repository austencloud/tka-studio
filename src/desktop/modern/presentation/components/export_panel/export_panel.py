"""
Export Panel - Proper proportional layout without fixed sizes

Uses Qt layout system properly with stretch factors and size policies.
"""

from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.settings_services import IImageExportSettingsManager
from desktop.modern.core.interfaces.workbench_export_services import (
    IWorkbenchExportService,
)

from .cards import (
    ConsolidatedExportSettingsCard,
    EnhancedExportPreviewCard,
    ExportActionsCard,
)


class ExportPanel(QWidget):
    """
    Export Panel with proper proportional layout using Qt layout system.
    """

    # Signals
    export_requested = pyqtSignal(str, dict)  # export_type, options
    setting_changed = pyqtSignal(str, object)  # setting_name, value

    def __init__(
        self,
        container: DIContainer,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self.container = container

        # Resolve export services
        try:
            self.workbench_export_service = container.resolve(IWorkbenchExportService)
            self.settings_manager = container.resolve(IImageExportSettingsManager)
            print("✅ [EXPORT_PANEL] Export services resolved successfully")
        except Exception as e:
            print(f"⚠️ [EXPORT_PANEL] Failed to resolve export services: {e}")
            self.workbench_export_service = None
            self.settings_manager = None

        # Update timer for preview
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self._update_preview)

        # Workbench reference
        self.workbench_widget = None

        self._setup_ui()
        self._load_settings()
        self._setup_connections()

    def _setup_ui(self):
        """Set up proportional layout using Qt layout system."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        # Compact header
        title = QLabel("Export")
        title.setObjectName("main_title")
        title.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        main_layout.addWidget(title)

        description = QLabel("Configure settings and export current sequence")
        description.setObjectName("main_description")
        main_layout.addWidget(description)

        # Main content with proportional layout
        content_layout = QHBoxLayout()
        content_layout.setSpacing(12)

        # Left: Settings column with proper size policy
        settings_container = QWidget()
        settings_container.setObjectName("settings_container")
        settings_container.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )

        settings_layout = QVBoxLayout(settings_container)
        settings_layout.setContentsMargins(0, 0, 0, 0)
        settings_layout.setSpacing(8)

        self.settings_card = ConsolidatedExportSettingsCard()
        settings_layout.addWidget(self.settings_card)

        self.actions_card = ExportActionsCard()
        settings_layout.addWidget(self.actions_card)

        settings_layout.addStretch()

        # Right: Preview with proper size policy
        self.preview_card = EnhancedExportPreviewCard()
        self.preview_card.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # Connect export service to preview card
        if self.workbench_export_service:
            self.preview_card.set_export_service(self.workbench_export_service)

        # Add to content layout with stretch factors for proportional sizing
        content_layout.addWidget(settings_container, 1)  # 1 part for settings
        content_layout.addWidget(
            self.preview_card, 2
        )  # 2 parts for preview (2:1 ratio)

        main_layout.addLayout(content_layout, 1)

        self._apply_styling()

    def _apply_styling(self):
        """Apply clean styling without fixed sizes."""
        self.setStyleSheet("""
            QWidget {
                background: transparent;
                color: white;
            }

            QLabel#main_title {
                color: rgba(255, 255, 255, 0.95);
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 2px;
                background: transparent;
                border: none;
            }

            QLabel#main_description {
                color: rgba(255, 255, 255, 0.7);
                font-size: 12px;
                margin-bottom: 8px;
                background: transparent;
                border: none;
            }

            QWidget#settings_container {
                background: transparent;
            }
        """)

    def _load_settings(self):
        """Load default settings."""
        default_settings = {
            "include_start_position": True,
            "add_beat_numbers": True,
            "add_reversal_symbols": True,
            "add_user_info": True,
            "add_word": True,
            "use_last_save_directory": True,
            "export_format": "PNG",
            "export_quality": "300 DPI",
            "user_name": "Default User",
            "custom_note": "",
        }

        self.settings_card.set_all_settings(default_settings)
        self._update_preview()

    def _setup_connections(self):
        """Setup signal connections."""
        self.settings_card.setting_changed.connect(self._on_setting_changed)
        self.preview_card.preview_update_requested.connect(
            self._on_preview_update_requested
        )
        self.actions_card.export_current_requested.connect(self._export_current)

    def _on_setting_changed(self, setting_name: str, value):
        """Handle setting changes."""
        print(f"🔧 Export setting changed: {setting_name} = {value}")

        # Apply to settings manager if available
        if self.settings_manager:
            try:
                if setting_name == "export_format":
                    self.settings_manager.set_export_format(value)
                elif setting_name == "export_quality":
                    if isinstance(value, str) and "DPI" in value.upper():
                        dpi = int("".join(filter(str.isdigit, value)))
                        quality = min(100, max(0, dpi // 3))
                    else:
                        quality = int(value) if value else 95
                    self.settings_manager.set_export_quality(quality)
            except (ValueError, AttributeError) as e:
                print(f"Warning: Failed to apply setting {setting_name}: {e}")

        self.setting_changed.emit(setting_name, value)
        self.update_timer.start(300)

    def _on_preview_update_requested(self, settings: dict):
        """Handle preview update requests."""
        self._update_preview()

    def _update_preview(self):
        """Update preview with current sequence and settings."""
        current_settings = self.settings_card.get_all_settings()

        # Get sequence from workbench
        current_sequence = None
        current_word = "Preview"

        if self.workbench_widget and hasattr(self.workbench_widget, "get_sequence"):
            try:
                current_sequence = self.workbench_widget.get_sequence()
                print(
                    f"📊 [EXPORT_PANEL] Got sequence: {current_sequence.length if current_sequence else 0} beats"
                )

                # Try to get word/name
                if hasattr(self.workbench_widget, "get_current_word"):
                    current_word = self.workbench_widget.get_current_word() or "Preview"

            except Exception as e:
                print(f"❌ [EXPORT_PANEL] Error getting sequence: {e}")

        # Update preview
        self.preview_card.set_sequence_data(current_sequence, current_word)
        self.preview_card.update_preview_settings(current_settings, immediate=True)

    def _export_current(self):
        """Export current sequence using the export service."""
        if not self.workbench_export_service:
            print("❌ [EXPORT_PANEL] No export service available")
            self.actions_card.export_current_btn.setText("❌ No Export Service")
            QTimer.singleShot(
                2000,
                lambda: self.actions_card.export_current_btn.setText(
                    "🔤 Export Current Sequence"
                ),
            )
            return

        if not self.workbench_widget or not hasattr(
            self.workbench_widget, "get_sequence"
        ):
            print("❌ [EXPORT_PANEL] No workbench available")
            self.actions_card.export_current_btn.setText("❌ No Workbench")
            QTimer.singleShot(
                2000,
                lambda: self.actions_card.export_current_btn.setText(
                    "🔤 Export Current Sequence"
                ),
            )
            return

        try:
            current_sequence = self.workbench_widget.get_sequence()
            if not current_sequence or not current_sequence.beats:
                print("❌ [EXPORT_PANEL] No sequence to export")
                self.actions_card.export_current_btn.setText("❌ No Sequence")
                QTimer.singleShot(
                    2000,
                    lambda: self.actions_card.export_current_btn.setText(
                        "🔤 Export Current Sequence"
                    ),
                )
                return

            # Show loading state
            self.actions_card.set_export_current_loading(True)

            # Export using the workbench export service
            success, message = self.workbench_export_service.export_sequence_image(
                current_sequence
            )

            if success:
                print(f"✅ [EXPORT_PANEL] Export successful: {message}")
                self.actions_card.export_current_btn.setText("✅ Exported!")
                QTimer.singleShot(
                    2000, lambda: self.actions_card.set_export_current_loading(False)
                )
            else:
                print(f"❌ [EXPORT_PANEL] Export failed: {message}")
                self.actions_card.export_current_btn.setText("❌ Export Failed")
                QTimer.singleShot(
                    2000, lambda: self.actions_card.set_export_current_loading(False)
                )

        except Exception as e:
            print(f"❌ [EXPORT_PANEL] Export error: {e}")
            self.actions_card.export_current_btn.setText("❌ Export Error")
            QTimer.singleShot(
                2000, lambda: self.actions_card.set_export_current_loading(False)
            )

    def set_workbench_widget(self, workbench_widget):
        """Connect workbench widget."""
        self.workbench_widget = workbench_widget
        print(
            f"🔗 [EXPORT_PANEL] Workbench connected: {type(workbench_widget).__name__}"
        )

        # Connect to sequence changes
        if hasattr(workbench_widget, "sequence_modified"):
            workbench_widget.sequence_modified.connect(
                self._on_workbench_sequence_changed
            )
            print("🔗 [EXPORT_PANEL] Connected to sequence changes")

        self._update_preview()

    def _on_workbench_sequence_changed(self, sequence):
        """Handle sequence changes from workbench."""
        print(
            f"📊 [EXPORT_PANEL] Sequence changed: {sequence.length if sequence else 0} beats"
        )
        self._update_preview()

    def update_preview_from_external(self, pixmap=None):
        """Update preview (for compatibility)."""
        self._update_preview()
