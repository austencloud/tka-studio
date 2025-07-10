"""
Modern Codex Exporter Tab for settings dialog.

This tab provides functionality to export pictographs with turn configurations,
following TKA's modern clean architecture and glassmorphism design.
"""

from core.interfaces.core_services import IUIStateManager
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class CodexExporterTab(QWidget):
    """Modern Codex Exporter tab with glassmorphism design."""

    export_requested = pyqtSignal(dict)  # Emits export configuration

    def __init__(self, ui_state_service: IUIStateManager, parent=None):
        super().__init__(parent)
        self.ui_state_service = ui_state_service
        self._setup_ui()
        self._load_settings()
        self._setup_connections()

    def _setup_ui(self):
        """Setup the codex exporter tab UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        # Title
        title = QLabel("Codex Exporter")
        title.setObjectName("section_title")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        main_layout.addWidget(title)

        # Description
        description = QLabel(
            "Export all pictographs with customizable turn configurations"
        )
        description.setObjectName("description")
        description.setWordWrap(True)
        main_layout.addWidget(description)

        # Turn Configuration Section
        self._create_turn_config_section(main_layout)

        # Grid Mode Section
        self._create_grid_mode_section(main_layout)

        # Export Options Section
        self._create_export_options_section(main_layout)

        # Export Button
        self._create_export_button(main_layout)

        main_layout.addStretch()

    def _create_turn_config_section(self, parent_layout):
        """Create the turn configuration section."""
        group = QGroupBox("Turn Configuration")
        group.setObjectName("settings_group")
        layout = QGridLayout(group)
        layout.setSpacing(15)

        # Red turns
        red_label = QLabel("Red Turns:")
        red_label.setObjectName("setting_label")
        self.red_turns_spin = QDoubleSpinBox()
        self.red_turns_spin.setRange(0.0, 4.0)
        self.red_turns_spin.setSingleStep(0.25)
        self.red_turns_spin.setValue(1.0)
        self.red_turns_spin.setObjectName("setting_control")

        layout.addWidget(red_label, 0, 0)
        layout.addWidget(self.red_turns_spin, 0, 1)

        # Blue turns
        blue_label = QLabel("Blue Turns:")
        blue_label.setObjectName("setting_label")
        self.blue_turns_spin = QDoubleSpinBox()
        self.blue_turns_spin.setRange(0.0, 4.0)
        self.blue_turns_spin.setSingleStep(0.25)
        self.blue_turns_spin.setValue(0.0)
        self.blue_turns_spin.setObjectName("setting_control")

        layout.addWidget(blue_label, 1, 0)
        layout.addWidget(self.blue_turns_spin, 1, 1)

        # Generate all combinations
        self.generate_all_checkbox = QCheckBox("Generate All Turn Combinations")
        self.generate_all_checkbox.setObjectName("setting_checkbox")
        layout.addWidget(self.generate_all_checkbox, 2, 0, 1, 2)

        parent_layout.addWidget(group)

    def _create_grid_mode_section(self, parent_layout):
        """Create the grid mode selection section."""
        group = QGroupBox("Grid Mode")
        group.setObjectName("settings_group")
        layout = QHBoxLayout(group)

        grid_label = QLabel("Grid Type:")
        grid_label.setObjectName("setting_label")

        self.grid_mode_combo = QComboBox()
        self.grid_mode_combo.addItems(["Diamond", "Box"])
        self.grid_mode_combo.setObjectName("setting_control")

        layout.addWidget(grid_label)
        layout.addWidget(self.grid_mode_combo)
        layout.addStretch()

        parent_layout.addWidget(group)

    def _create_export_options_section(self, parent_layout):
        """Create the export options section."""
        group = QGroupBox("Export Options")
        group.setObjectName("settings_group")
        layout = QVBoxLayout(group)
        layout.setSpacing(10)

        # Quality settings
        quality_layout = QHBoxLayout()
        quality_label = QLabel("Image Quality:")
        quality_label.setObjectName("setting_label")

        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(1, 100)
        self.quality_spin.setValue(95)
        self.quality_spin.setSuffix("%")
        self.quality_spin.setObjectName("setting_control")

        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_spin)
        quality_layout.addStretch()

        layout.addLayout(quality_layout)

        # Include metadata
        self.include_metadata_checkbox = QCheckBox("Include Export Metadata")
        self.include_metadata_checkbox.setChecked(True)
        self.include_metadata_checkbox.setObjectName("setting_checkbox")
        layout.addWidget(self.include_metadata_checkbox)

        parent_layout.addWidget(group)

    def _create_export_button(self, parent_layout):
        """Create the export button."""
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.export_button = QPushButton("Export All Pictographs")
        self.export_button.setObjectName("primary_button")
        self.export_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.export_button.setMinimumSize(200, 45)

        button_layout.addWidget(self.export_button)
        parent_layout.addLayout(button_layout)

    def _load_settings(self):
        """Load current settings from the service."""
        # Load saved settings
        red_turns = self.ui_state_service.get_setting("codex_exporter/red_turns", 1.0)
        blue_turns = self.ui_state_service.get_setting("codex_exporter/blue_turns", 0.0)
        grid_mode = self.ui_state_service.get_setting(
            "codex_exporter/grid_mode", "diamond"
        )
        generate_all = self.ui_state_service.get_setting(
            "codex_exporter/generate_all", False
        )
        quality = self.ui_state_service.get_setting("codex_exporter/quality", 95)
        include_metadata = self.ui_state_service.get_setting(
            "codex_exporter/include_metadata", True
        )

        # Apply to controls
        self.red_turns_spin.setValue(red_turns)
        self.blue_turns_spin.setValue(blue_turns)
        self.grid_mode_combo.setCurrentText(grid_mode.title())
        self.generate_all_checkbox.setChecked(generate_all)
        self.quality_spin.setValue(quality)
        self.include_metadata_checkbox.setChecked(include_metadata)

    def _setup_connections(self):
        """Setup signal connections."""
        self.export_button.clicked.connect(self._on_export_clicked)

        # Save settings when changed
        self.red_turns_spin.valueChanged.connect(self._save_settings)
        self.blue_turns_spin.valueChanged.connect(self._save_settings)
        self.grid_mode_combo.currentTextChanged.connect(self._save_settings)
        self.generate_all_checkbox.toggled.connect(self._save_settings)
        self.quality_spin.valueChanged.connect(self._save_settings)
        self.include_metadata_checkbox.toggled.connect(self._save_settings)

    def _save_settings(self):
        """Save current settings."""
        self.ui_state_service.set_setting(
            "codex_exporter/red_turns", self.red_turns_spin.value()
        )
        self.ui_state_service.set_setting(
            "codex_exporter/blue_turns", self.blue_turns_spin.value()
        )
        self.ui_state_service.set_setting(
            "codex_exporter/grid_mode", self.grid_mode_combo.currentText().lower()
        )
        self.ui_state_service.set_setting(
            "codex_exporter/generate_all", self.generate_all_checkbox.isChecked()
        )
        self.ui_state_service.set_setting(
            "codex_exporter/quality", self.quality_spin.value()
        )
        self.ui_state_service.set_setting(
            "codex_exporter/include_metadata",
            self.include_metadata_checkbox.isChecked(),
        )

    def _on_export_clicked(self):
        """Handle export button click."""
        config = {
            "red_turns": self.red_turns_spin.value(),
            "blue_turns": self.blue_turns_spin.value(),
            "grid_mode": self.grid_mode_combo.currentText().lower(),
            "generate_all": self.generate_all_checkbox.isChecked(),
            "quality": self.quality_spin.value(),
            "include_metadata": self.include_metadata_checkbox.isChecked(),
        }

        self.export_requested.emit(config)

        # Show success message
        from PyQt6.QtWidgets import QMessageBox

        QMessageBox.information(
            self,
            "Export Started",
            "Pictograph export has been initiated. This may take several minutes to complete.",
            QMessageBox.StandardButton.Ok,
        )
