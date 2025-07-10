"""
Modern Image Export Tab with Live Preview.

This tab provides comprehensive image export configuration with real-time pictograph preview
that updates as options are toggled, following the legacy functionality but with modern
clean architecture and glassmorphism design.
"""

from typing import Dict, Union

from core.interfaces.tab_settings_interfaces import IImageExporter
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QCursor, QFont, QPainter, QPixmap
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSplitter,
    QVBoxLayout,
    QWidget,
)


class ImageExportPreviewPanel(QFrame):
    """Live preview panel that shows how the exported image will look."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._current_pixmap = None

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Preview label
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumSize(400, 300)
        self.preview_label.setStyleSheet(
            """
            QLabel {
                background: rgba(0, 0, 0, 0.3);
                border: 2px dashed rgba(255, 255, 255, 0.3);
                border-radius: 12px;
                color: rgba(255, 255, 255, 0.6);
                font-size: 16px;
                font-weight: 500;
            }
        """
        )
        self.preview_label.setText(
            "Preview will appear here\nwhen a sequence is available"
        )

        layout.addWidget(self.preview_label)

    def update_preview(self, pixmap: QPixmap):
        """Update the preview with a new pixmap."""
        if pixmap and not pixmap.isNull():
            # Scale pixmap to fit the preview area while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(
                self.preview_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.preview_label.setPixmap(scaled_pixmap)
            self._current_pixmap = scaled_pixmap
        else:
            self.preview_label.clear()
            self.preview_label.setText("No preview available")
            self._current_pixmap = None


class ExportToggle(QCheckBox):
    """Enhanced export toggle with modern styling."""

    def __init__(self, label: str, tooltip: Union[str, None] = None, parent=None):
        super().__init__(label, parent)
        if tooltip:
            self.setToolTip(tooltip)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._apply_styling()

    def _apply_styling(self):
        self.setStyleSheet(
            """
            QCheckBox {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                font-weight: 500;
                font-family: "Inter", "Segoe UI", sans-serif;
                spacing: 12px;
                padding: 12px;
                border-radius: 10px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.08),
                    stop:1 rgba(255, 255, 255, 0.04));
                border: 1px solid rgba(255, 255, 255, 0.1);
            }

            QCheckBox:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.12),
                    stop:1 rgba(255, 255, 255, 0.08));
                border-color: rgba(255, 255, 255, 0.2);
            }

            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid rgba(255, 255, 255, 0.4);
                border-radius: 6px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.12),
                    stop:1 rgba(255, 255, 255, 0.06));
            }

            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(42, 130, 218, 0.9),
                    stop:1 rgba(42, 130, 218, 0.7));
                border-color: rgba(42, 130, 218, 1.0);
            }

            QCheckBox::indicator:hover {
                border-color: rgba(255, 255, 255, 0.6);
            }
        """
        )


class ImageExportTab(QWidget):
    """Modern image export tab with live preview like the legacy version."""

    export_option_changed = pyqtSignal(str, object)
    setting_changed = pyqtSignal(str, object)

    def __init__(self, export_service: IImageExporter, parent=None):
        super().__init__(parent)
        self.export_service = export_service
        self.option_toggles: Dict[str, ExportToggle] = {}

        # Create preview panel
        self.preview_panel = ImageExportPreviewPanel(self)

        # Update timer for preview
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self._update_preview)

        self._setup_ui()
        self._load_settings()
        self._setup_connections()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        # Title
        title = QLabel("Image Export")
        title.setObjectName("section_title")
        title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        main_layout.addWidget(title)

        # Description
        description = QLabel(
            "Configure export options and preview the result in real-time"
        )
        description.setObjectName("description")
        description.setWordWrap(True)
        main_layout.addWidget(description)

        # Main content with splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left side - Control panel
        control_panel = self._create_control_panel()
        splitter.addWidget(control_panel)

        # Right side - Preview panel
        preview_container = QFrame()
        preview_container.setObjectName("preview_container")
        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setContentsMargins(20, 20, 20, 20)

        preview_title = QLabel("Live Preview")
        preview_title.setObjectName("subsection_title")
        preview_title.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        preview_layout.addWidget(preview_title)

        preview_layout.addWidget(self.preview_panel)
        splitter.addWidget(preview_container)

        # Set splitter proportions (40% control, 60% preview)
        splitter.setSizes([400, 600])

        main_layout.addWidget(splitter)
        self._apply_styling()

    def _create_control_panel(self):
        """Create the control panel with export options and settings."""
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.setSpacing(20)

        # Scroll area for controls
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)

        # Export options section
        options_section = self._create_options_section()
        scroll_layout.addWidget(options_section)

        # User settings section
        settings_section = self._create_settings_section()
        scroll_layout.addWidget(settings_section)

        # Export actions section
        actions_section = self._create_actions_section()
        scroll_layout.addWidget(actions_section)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)

        control_layout.addWidget(scroll_area)
        return control_widget

    def _create_options_section(self):
        """Create the export options section."""
        section = QFrame()
        section.setObjectName("settings_section")
        layout = QVBoxLayout(section)

        title = QLabel("Export Options")
        title.setObjectName("subsection_title")
        layout.addWidget(title)

        # Export options with descriptions (like legacy)
        export_options = [
            (
                "include_start_position",
                "Start Position",
                "Show the starting position in exports",
            ),
            ("add_beat_numbers", "Beat Numbers", "Add numbers to each beat"),
            ("add_reversal_symbols", "Reversal Symbols", "Show reversal indicators"),
            ("add_user_info", "User Info", "Include user name in export"),
            ("add_word", "Word", "Add word descriptions"),
            ("add_difficulty_level", "Difficulty Level", "Show difficulty rating"),
            ("combined_grids", "Combined Grids", "Use combined grid layouts"),
        ]

        for option_key, label, tooltip in export_options:
            toggle = ExportToggle(label, tooltip)
            toggle.toggled.connect(
                lambda checked, key=option_key: self._on_option_changed(key, checked)
            )
            self.option_toggles[option_key] = toggle
            layout.addWidget(toggle)

        return section

    def _create_settings_section(self):
        """Create the user settings section."""
        section = QFrame()
        section.setObjectName("settings_section")
        layout = QVBoxLayout(section)

        title = QLabel("User Settings")
        title.setObjectName("subsection_title")
        layout.addWidget(title)

        # Directory preference
        self.remember_dir_toggle = ExportToggle(
            "Remember Last Directory", "Remember the last directory used for saving"
        )
        self.remember_dir_toggle.toggled.connect(
            lambda checked: self._on_option_changed("use_last_save_directory", checked)
        )
        layout.addWidget(self.remember_dir_toggle)

        # User name input
        user_layout = QVBoxLayout()
        user_label = QLabel("User Name:")
        user_label.setObjectName("input_label")
        user_layout.addWidget(user_label)

        self.user_combo_box = QComboBox()
        self.user_combo_box.setEditable(True)
        self.user_combo_box.setObjectName("export_input")
        self.user_combo_box.addItems(["Default User", "User 1", "User 2"])
        user_layout.addWidget(self.user_combo_box)

        layout.addLayout(user_layout)

        # Custom note input
        note_layout = QVBoxLayout()
        note_label = QLabel("Notes:")
        note_label.setObjectName("input_label")
        note_layout.addWidget(note_label)

        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Add a custom note to exports")
        self.note_input.setObjectName("export_input")
        note_layout.addWidget(self.note_input)

        layout.addLayout(note_layout)

        return section

    def _create_actions_section(self):
        """Create the export actions section."""
        section = QFrame()
        section.setObjectName("settings_section")
        layout = QVBoxLayout(section)

        title = QLabel("Export Actions")
        title.setObjectName("subsection_title")
        layout.addWidget(title)

        # Export current sequence button
        self.export_current_btn = QPushButton("Export Current Sequence")
        self.export_current_btn.setObjectName("action_button")
        self.export_current_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        layout.addWidget(self.export_current_btn)

        # Export all pictographs button
        self.export_all_btn = QPushButton("Export All Pictographs")
        self.export_all_btn.setObjectName("action_button")
        self.export_all_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        layout.addWidget(self.export_all_btn)

        return section

    def _apply_styling(self):
        self.setStyleSheet(
            """
            QWidget {
                background: transparent;
                color: white;
            }
            
            QLabel#section_title {
                color: white;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            
            QLabel#description {
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
                margin-bottom: 20px;
            }
            
            QLabel#subsection_title {
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 15px;
            }
            
            QLabel#input_label {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                font-weight: 500;
                margin-bottom: 5px;
                margin-top: 10px;
            }
            
            QFrame#settings_section {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 20px;
                margin: 5px;
                min-width: 300px;
            }
            
            QLineEdit#export_input {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                padding: 10px;
                color: white;
                font-size: 14px;
                margin-bottom: 10px;
            }
            
            QLineEdit#export_input:focus {
                border-color: rgba(59, 130, 246, 0.8);
            }
            
            QPushButton#action_button {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(59, 130, 246, 0.8),
                    stop:1 rgba(59, 130, 246, 0.6));
                border: 2px solid rgba(59, 130, 246, 0.3);
                border-radius: 8px;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 12px;
                margin: 5px 0;
            }
            
            QPushButton#action_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(59, 130, 246, 1.0),
                    stop:1 rgba(59, 130, 246, 0.8));
                border-color: rgba(59, 130, 246, 0.8);
            }
            
            QPushButton#action_button:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(59, 130, 246, 0.6),
                    stop:1 rgba(59, 130, 246, 0.4));
            }
        """
        )

    def _load_settings(self):
        """Load current settings from the service."""
        # Load export options
        for option_key, toggle in self.option_toggles.items():
            value = self.export_service.get_export_option(option_key)
            toggle.setChecked(bool(value))

        # Load directory preference
        remember_dir = self.export_service.get_export_option("use_last_save_directory")
        self.remember_dir_toggle.setChecked(bool(remember_dir))

        # Load user inputs with defaults
        self.user_combo_box.setCurrentText("Default User")
        self.note_input.setText("")

    def _setup_connections(self):
        """Setup signal connections."""
        # Export option toggles are connected in _create_options_section

        # Connect user controls
        self.user_combo_box.currentTextChanged.connect(
            lambda text: self._on_user_changed(text)
        )

        self.note_input.textChanged.connect(lambda text: self._on_note_changed(text))

        # Connect action buttons
        self.export_current_btn.clicked.connect(self._export_current)
        self.export_all_btn.clicked.connect(self._export_all)

    def _on_option_changed(self, option_key: str, value: bool):
        """Handle export option changes and trigger preview update."""
        self.export_service.set_export_option(option_key, value)
        self.export_option_changed.emit(option_key, value)
        self.setting_changed.emit(option_key, value)

        # Trigger preview update with a small delay
        self.update_timer.start(300)

    def _on_user_changed(self, text: str):
        """Handle user name changes."""
        self.export_option_changed.emit("user_name", text)
        self.setting_changed.emit("user_name", text)
        self.update_timer.start(300)

    def _on_note_changed(self, text: str):
        """Handle note changes."""
        self.export_option_changed.emit("custom_note", text)
        self.setting_changed.emit("custom_note", text)
        self.update_timer.start(300)

    def _update_preview(self):
        """Update the preview image based on current settings."""
        # This would integrate with the actual image generation system
        # For now, we'll create a placeholder
        try:
            # Get current export options
            options = self._get_current_export_options()

            # In a real implementation, this would generate the actual preview
            # using the image export manager from the legacy system
            placeholder_pixmap = self._create_placeholder_preview(options)
            self.preview_panel.update_preview(placeholder_pixmap)

        except Exception as e:
            print(f"Error updating preview: {e}")

    def _get_current_export_options(self) -> Dict[str, Union[bool, str]]:
        """Get current export options as a dictionary."""
        options = {}
        for option_key, toggle in self.option_toggles.items():
            options[option_key] = toggle.isChecked()

        options["user_name"] = self.user_combo_box.currentText()
        options["notes"] = self.note_input.text()
        options["use_last_save_directory"] = self.remember_dir_toggle.isChecked()

        return options

    def _create_placeholder_preview(
        self, options: Dict[str, Union[bool, str]]
    ) -> QPixmap:
        """Create a placeholder preview image."""
        pixmap = QPixmap(400, 300)
        pixmap.fill(Qt.GlobalColor.darkGray)

        painter = QPainter(pixmap)
        painter.setPen(Qt.GlobalColor.white)
        painter.drawText(
            pixmap.rect(),
            Qt.AlignmentFlag.AlignCenter,
            f"Preview\n{len([k for k, v in options.items() if v])} options enabled",
        )
        painter.end()

        return pixmap

    def _export_current(self):
        """Export the current sequence."""
        self.export_option_changed.emit("action", "export_current")

    def _export_all(self):
        """Export all pictographs."""
        self.export_option_changed.emit("action", "export_all")

    def update_preview(self):
        """Public method to trigger preview update."""
        self._update_preview()
