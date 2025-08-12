"""
UI Setup Helper - Simple extraction from SequenceWorkbench

Extracted UI setup methods without any changes to functionality.
Just moves the code to reduce the main file size.
"""

from __future__ import annotations

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from .beat_frame_section import WorkbenchBeatFrameSection
from .button_interface import WorkbenchButtonInterfaceAdapter
from .indicator_section import WorkbenchIndicatorSection


class UISetupHelper:
    """Helper class for workbench UI setup - simple extraction."""

    def __init__(self, workbench):
        self.workbench = workbench

    def setup_ui_minimal(self):
        """Setup minimal UI for fast startup."""
        # Create main widget only
        self.workbench._widget = QWidget(self.workbench.parent())
        self.workbench._main_layout = QVBoxLayout(self.workbench._widget)
        self.workbench._main_layout.setSpacing(8)
        self.workbench._main_layout.setContentsMargins(8, 8, 8, 8)

        # Add placeholder for sections (will be created in deferred initialization)
        placeholder = QLabel("Loading workbench...")
        placeholder.setStyleSheet("color: #888; font-size: 14px; padding: 20px;")
        self.workbench._main_layout.addWidget(placeholder)
        self.workbench._placeholder = placeholder

    def complete_ui_setup(self):
        """Complete UI setup with all components."""

        # Remove placeholder
        if hasattr(self.workbench, "_placeholder"):
            self.workbench._main_layout.removeWidget(self.workbench._placeholder)
            self.workbench._placeholder.deleteLater()
            del self.workbench._placeholder

        # Create sections using existing components
        self.workbench._indicator_section = WorkbenchIndicatorSection(
            dictionary_service=self.workbench._safe_resolve(
                "SequenceDictionaryService"
            ),
            parent=self.workbench._widget,
        )
        self.workbench._main_layout.addWidget(self.workbench._indicator_section, 0)

        self.workbench._beat_frame_section = WorkbenchBeatFrameSection(
            layout_service=self.workbench._layout_service,
            beat_selection_service=self.workbench._beat_selection_service,
            parent=self.workbench._widget,
        )
        self.workbench._main_layout.addWidget(self.workbench._beat_frame_section, 1)


    def setup_button_interface(self):
        """Setup button interface adapter."""
        self.workbench._button_interface = WorkbenchButtonInterfaceAdapter(
            self.workbench._widget
        )
        if self.workbench._button_interface.signals:
            self.workbench._button_interface.signals.sequence_modified.connect(
                self.workbench.sequence_modified
            )
            self.workbench._button_interface.signals.operation_completed.connect(
                self.workbench.operation_completed
            )
            self.workbench._button_interface.signals.operation_failed.connect(
                self.workbench.error_occurred
            )
