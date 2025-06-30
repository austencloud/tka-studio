"""
Professional Graph Editor for TKA - Refactored Architecture
===========================================================

A visually rich, pictograph-centered graph editor component designed for embedded use
in stack widgets. Features a modern UI with pictograph display and dual adjustment panels.

This refactored version follows TKA clean architecture patterns with proper component
separation, dependency injection, and maintainable code structure.

Architecture:
- PictographDisplaySection: Manages pictograph and info panel display
- MainAdjustmentPanel: Orchestrates orientation and turn controls
- Component-based design with clear separation of concerns
- Signal-based communication between components
- Preserved public API for backward compatibility
"""

import logging
from typing import Optional, TYPE_CHECKING

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSplitter
from PyQt6.QtCore import pyqtSignal, Qt

from domain.models.core_models import SequenceData, BeatData
from core.interfaces.workbench_services import IGraphEditorService

# Import refactored components
from .components.pictograph_display_section import PictographDisplaySection
from .components.main_adjustment_panel import MainAdjustmentPanel

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from presentation.components.workbench.workbench import SequenceWorkbench


class GraphEditor(QFrame):
    """
    Professional Graph Editor for TKA - Refactored Architecture

    A visually rich, pictograph-centered graph editor component with modern UI design.
    Features pictograph display area and dual adjustment panels for beat and arrow properties.

    This refactored version uses component-based architecture while maintaining full
    backward compatibility with the existing API.

    Components:
    - PictographDisplaySection: Manages pictograph and info panel
    - MainAdjustmentPanel: Orchestrates orientation and turn controls
    """

    # Signals for external communication (preserved for backward compatibility)
    beat_modified = pyqtSignal(int, object)  # beat_index, beat_data
    arrow_selected = pyqtSignal(object)  # arrow_data
    visibility_changed = pyqtSignal(bool)  # is_visible

    def __init__(
        self,
        graph_service: Optional[IGraphEditorService] = None,
        parent: Optional["SequenceWorkbench"] = None,
        workbench_width: int = 800,
        workbench_height: int = 600,
    ):
        super().__init__(parent)
        self._graph_service = graph_service
        self._parent_workbench = parent
        self._current_sequence: Optional[SequenceData] = None
        self._selected_beat_index: Optional[int] = None
        self._selected_beat_data: Optional[BeatData] = None

        # Component references (new architecture)
        self._pictograph_display: Optional[PictographDisplaySection] = None
        self._adjustment_panel: Optional[MainAdjustmentPanel] = None

        # Set up the UI
        self._setup_ui()
        self._setup_styling()
        self._connect_signals()

        # Set initial size
        self.setMinimumSize(400, 300)
        self.resize(workbench_width, 300)  # Fixed height for embedded mode

        logger.info("Professional graph editor initialized successfully (refactored)")

    def _setup_ui(self) -> None:
        """Set up the professional user interface using refactored components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Create vertical splitter for main sections
        main_splitter = QSplitter(Qt.Orientation.Vertical)
        main_splitter.setChildrenCollapsible(False)

        # Top Section: Pictograph Display Section (component)
        self._pictograph_display = PictographDisplaySection(parent=self)
        main_splitter.addWidget(self._pictograph_display)

        # Bottom Section: Main Adjustment Panel (component)
        self._adjustment_panel = MainAdjustmentPanel(parent=self)
        main_splitter.addWidget(self._adjustment_panel)

        # Set splitter proportions (50/50 split)
        main_splitter.setSizes([150, 150])  # Equal proportions for 300px total height

        main_layout.addWidget(main_splitter)

    def _connect_signals(self):
        """Connect signals from components to maintain backward compatibility"""
        if self._pictograph_display:
            # Connect pictograph display signals
            self._pictograph_display.pictograph_updated.connect(
                self._on_pictograph_updated
            )
            self._pictograph_display.info_panel_updated.connect(
                self._on_info_panel_updated
            )

        if self._adjustment_panel:
            # Connect adjustment panel signals
            self._adjustment_panel.orientation_changed.connect(
                self._on_orientation_changed
            )
            self._adjustment_panel.turn_amount_changed.connect(
                self._on_turn_amount_changed
            )
            self._adjustment_panel.rotation_direction_changed.connect(
                self._on_rotation_direction_changed
            )
            self._adjustment_panel.beat_data_updated.connect(self._on_beat_data_updated)

    def _on_pictograph_updated(self, beat_data: BeatData):
        """Handle pictograph update signals"""
        logger.debug(f"Pictograph updated: {beat_data.letter}")

    def _on_info_panel_updated(self, beat_index: int, beat_data: BeatData):
        """Handle info panel update signals"""
        logger.debug(f"Info panel updated for beat {beat_index}")

    def _on_orientation_changed(self, color: str, orientation: str):
        """Handle orientation change signals"""
        # Emit legacy signal for backward compatibility
        orientation_data = {
            "color": color,
            "orientation": orientation,
            "type": "orientation_change",
        }
        self.arrow_selected.emit(orientation_data)
        logger.debug(f"{color.title()} orientation changed to: {orientation}")

    def _on_turn_amount_changed(self, color: str, amount: float):
        """Handle turn amount change signals"""
        # Emit legacy signal for backward compatibility
        turn_data = {"color": color, "amount": amount, "type": "turn_amount"}
        self.beat_modified.emit(0, turn_data)  # Use 0 as placeholder beat index
        logger.debug(f"{color.title()} turn amount changed to: {amount}")

    def _on_rotation_direction_changed(self, color: str, direction: str):
        """Handle rotation direction change signals"""
        # Emit legacy signal for backward compatibility
        rotation_data = {
            "color": color,
            "direction": direction,
            "type": "rotation_direction",
        }
        self.beat_modified.emit(0, rotation_data)  # Use 0 as placeholder beat index
        logger.debug(f"{color.title()} rotation direction changed to: {direction}")

    def _on_beat_data_updated(self, beat_data: BeatData):
        """Handle beat data update signals"""
        self._selected_beat_data = beat_data
        # Update pictograph display with new data
        if self._pictograph_display:
            self._pictograph_display.update_pictograph_only(beat_data)
        logger.debug("Beat data updated and pictograph refreshed")

    def _setup_styling(self) -> None:
        """Apply glassmorphism styling to the graph editor for animated background"""
        self.setStyleSheet(
            """
            /* Main Graph Editor Frame - Glassmorphism */
            GraphEditor {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
            }

            /* Group Boxes - Glass panels */
            QGroupBox {
                font-weight: bold;
                font-size: 12px;
                color: rgba(255, 255, 255, 0.9);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                margin-top: 12px;
                padding-top: 8px;
                background: rgba(255, 255, 255, 0.1);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 6px 16px;
                background: rgba(255, 255, 255, 0.25);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                color: rgba(255, 255, 255, 0.95);
                font-weight: bold;
                font-size: 13px;
            }

            /* Buttons - Glass effect */
            QPushButton {
                background: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 11px;
                color: rgba(255, 255, 255, 0.9);
                font-weight: 500;
                min-height: 20px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.25);
                border-color: rgba(255, 255, 255, 0.4);
                color: rgba(255, 255, 255, 1.0);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.35);
                border-color: rgba(255, 255, 255, 0.5);
            }
            QPushButton:checked {
                background: rgba(0, 102, 204, 0.3);
                border-color: rgba(0, 102, 204, 0.6);
                color: rgba(255, 255, 255, 1.0);
            }

            /* Labels - Glass text */
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 11px;
                font-weight: 500;
            }

            /* Stacked Widget - Transparent */
            QStackedWidget {
                background: transparent;
                border: none;
            }

            /* Container Widgets - Transparent */
            QWidget {
                background: transparent;
                border: none;
            }
        """
        )

    # Public API Methods (maintaining compatibility)
    def set_sequence(self, sequence: Optional[SequenceData]) -> None:
        """Set the sequence data for the graph editor"""
        self._current_sequence = sequence
        logger.info(f"Sequence set: {sequence.name if sequence else 'None'}")

    def set_selected_beat_data(self, beat_index: int, beat_data: BeatData) -> None:
        """Set the selected beat data and update the UI using refactored components"""
        self._selected_beat_index = beat_index
        self._selected_beat_data = beat_data

        # Update pictograph display section
        if self._pictograph_display:
            self._pictograph_display.update_display(beat_index, beat_data)

        # Update adjustment panel
        if self._adjustment_panel:
            self._adjustment_panel.set_beat_data(beat_index, beat_data)

        logger.info(
            f"Beat selected: {beat_index} - {beat_data.letter if beat_data else 'None'}"
        )

    def set_selected_start_position(self, start_position_data) -> None:
        """Set the selected start position data using refactored components"""
        # Update pictograph display section
        if self._pictograph_display:
            self._pictograph_display.update_display(-1, start_position_data)

        # Update adjustment panel (force orientation mode for start positions)
        if self._adjustment_panel:
            self._adjustment_panel.set_beat_data(-1, start_position_data)

        logger.info(f"Start position set: {start_position_data}")

    def toggle_visibility(self) -> None:
        """Toggle graph editor visibility"""
        if self.isVisible():
            self.hide()
        else:
            self.show()
        self.visibility_changed.emit(self.isVisible())

    def get_preferred_height(self) -> int:
        """Get the preferred height for the graph editor"""
        return 300

    def update_workbench_size(self, width: int, height: int) -> None:
        """Update workbench size reference when workbench resizes"""
        # Not needed for embedded mode - parameters kept for interface compatibility
        pass

    def sync_width_with_workbench(self) -> None:
        """Synchronize graph editor width with parent workbench width"""
        pass  # Not needed for embedded mode

    # Compatibility properties for existing tests
    @property
    def _pictograph_component(self):
        """Compatibility property for tests - access to pictograph component"""
        return (
            self._pictograph_display.get_pictograph_component()
            if self._pictograph_display
            else None
        )

    @property
    def _blue_turn_amount(self):
        """Compatibility property for tests - blue turn amount"""
        turn_controls = (
            self._adjustment_panel.get_turn_controls()
            if self._adjustment_panel
            else None
        )
        return turn_controls._blue_turn_amount if turn_controls else 0.0

    @property
    def _red_turn_amount(self):
        """Compatibility property for tests - red turn amount"""
        turn_controls = (
            self._adjustment_panel.get_turn_controls()
            if self._adjustment_panel
            else None
        )
        return turn_controls._red_turn_amount if turn_controls else 0.0

    @property
    def _blue_orientation(self):
        """Compatibility property for tests - blue orientation"""
        orientation_picker = (
            self._adjustment_panel.get_orientation_picker()
            if self._adjustment_panel
            else None
        )
        return orientation_picker.get_blue_orientation() if orientation_picker else "IN"

    @property
    def _red_orientation(self):
        """Compatibility property for tests - red orientation"""
        orientation_picker = (
            self._adjustment_panel.get_orientation_picker()
            if self._adjustment_panel
            else None
        )
        return orientation_picker.get_red_orientation() if orientation_picker else "IN"

    def _adjust_turn_amount(self, color: str, delta: float):
        """Compatibility method for tests - adjust turn amount"""
        turn_controls = (
            self._adjustment_panel.get_turn_controls()
            if self._adjustment_panel
            else None
        )
        if turn_controls:
            turn_controls._adjust_turn_amount(color, delta)

    @property
    def _info_panel(self):
        """Compatibility property for tests - access to info panel"""
        return (
            self._pictograph_display.get_info_panel()
            if self._pictograph_display
            else None
        )

    def _set_orientation(self, color: str, orientation: str):
        """Compatibility method for tests - set orientation"""
        orientation_picker = (
            self._adjustment_panel.get_orientation_picker()
            if self._adjustment_panel
            else None
        )
        if orientation_picker:
            orientation_picker._set_orientation(color, orientation)

    @property
    def _adjustment_stack(self):
        """Compatibility property for tests - access to adjustment stack widget"""
        return (
            self._adjustment_panel._stacked_widget if self._adjustment_panel else None
        )
