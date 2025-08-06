"""
Professional Graph Editor for TKA - Clean Component Architecture
================================================================

A visually rich, pictograph-centered graph editor component designed for embedded use
in stack widgets. Features a modern UI with pictograph display and dual adjustment panels.

This version uses clean component-based architecture with:
- 6 specialized components with single responsibilities
- Signal-based communication between components
- Simple error handling without over-engineering
- Backward compatible public API
- Maintainable and readable code structure
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout

from desktop.modern.core.interfaces.session_services import ISessionStateTracker
from desktop.modern.core.interfaces.workbench_services import IGraphEditorService
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData

from .components.main_adjustment_panel import MainAdjustmentPanel

# Import core components
from .components.pictograph_display_section import PictographDisplaySection

# Import essential utilities
from .utils.validation import (
    validate_sequence_data,
)


if TYPE_CHECKING:
    from desktop.modern.presentation.components.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )

logger = logging.getLogger(__name__)


class GraphEditor(QFrame):
    """
    Professional Graph Editor for TKA - Clean Component Architecture

    A visually rich, pictograph-centered graph editor component with modern UI design.
    This version uses clean component-based architecture with simple error handling
    and maintains full backward compatibility.

    Components:
    - PictographDisplaySection: Manages pictograph and info panel display
    - MainAdjustmentPanel: Orchestrates orientation and turn controls

    Features:
    - Signal-based communication between components
    - Simple error handling without over-engineering
    - Backward compatible public API
    - Clean, maintainable code structure
    """

    # Signals for external communication (preserved for backward compatibility)
    beat_modified = pyqtSignal(int, object)  # beat_index, beat_data
    arrow_selected = pyqtSignal(object)  # arrow_data
    visibility_changed = pyqtSignal(bool)  # is_visible

    # Internal signal for sequence updates
    sequence_updated = pyqtSignal(object)  # sequence_data

    def __init__(
        self,
        graph_service: Optional[IGraphEditorService] = None,
        parent: Optional[SequenceWorkbench] = None,
        workbench_width: int = 800,
        workbench_height: int = 600,
        session_service: Optional[ISessionStateTracker] = None,
    ):
        super().__init__(parent)
        self._graph_service = graph_service
        self._parent_workbench = parent
        self._session_service = session_service

        # Core state
        self._current_sequence: Optional[SequenceData] = None
        self._selected_beat_index: Optional[int] = None
        self._selected_beat_data: Optional[BeatData] = None

        # Component references
        self._pictograph_display: Optional[PictographDisplaySection] = None
        self._adjustment_panel: Optional[MainAdjustmentPanel] = None

        # Initialize with simple error handling
        try:
            self._setup_ui()
            self._connect_signals()
            self._apply_styling()
            self.resize(workbench_width, 300)
        except Exception as e:
            logger.error(f"Graph editor initialization failed: {e}")
            self._create_minimal_error_ui(str(e))

    def _setup_ui(self) -> None:
        """Simple UI setup with VBox layout and fixed proportions."""
        # Create main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Create components (let them fail naturally if there are real problems)
        self._pictograph_display = PictographDisplaySection(parent=self)
        self._adjustment_panel = MainAdjustmentPanel(parent=self)

        # Add components with stretch factors for 65/35 split
        # Stretch factor of 65 for pictograph display (top 65%)
        layout.addWidget(self._pictograph_display, 65)
        # Stretch factor of 35 for adjustment panel (bottom 35%)
        layout.addWidget(self._adjustment_panel, 35)

        logger.debug("UI setup completed with VBox layout")

    def _connect_signals(self) -> None:
        """Simple signal connections."""
        try:
            if self._pictograph_display:
                # Connect pictograph display signals
                self._pictograph_display.pictograph_updated.connect(
                    self._on_pictograph_updated
                )

            if self._adjustment_panel:
                # Connect adjustment panel signals
                self._adjustment_panel.orientation_changed.connect(
                    self._on_orientation_changed
                )
                self._adjustment_panel.turn_amount_changed.connect(
                    self._on_turn_amount_changed
                )

            logger.debug("Signals connected successfully")

        except Exception as e:
            logger.warning(f"Some signal connections failed: {e}")

    def _apply_styling(self) -> None:
        """Apply glassmorphism styling."""
        try:
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
            """
            )
            logger.debug("Styling applied successfully")
        except Exception as e:
            logger.warning(f"Failed to apply styling: {e}")

    def _create_minimal_error_ui(self, error_msg: str) -> None:
        """Create simple error display if initialization fails."""
        try:
            # Clear any existing layout
            if self.layout():
                self.layout().deleteLater()

            # Create simple layout
            layout = QVBoxLayout(self)
            layout.setContentsMargins(10, 10, 10, 10)

            # Add error message
            error_label = QLabel(f"Graph Editor Error: {error_msg}")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_label.setStyleSheet(
                """
                QLabel {
                    background: rgba(255, 0, 0, 0.2);
                    border: 2px solid red;
                    border-radius: 8px;
                    padding: 20px;
                    font-size: 14px;
                    font-weight: bold;
                    color: #333;
                }
            """
            )
            layout.addWidget(error_label)

            logger.warning(f"Minimal error UI created: {error_msg}")

        except Exception as e:
            logger.critical(f"Even minimal error UI creation failed: {e}")

    # Signal handlers - simple and direct
    def _on_pictograph_updated(self, beat_index: int, beat_data: BeatData) -> None:
        """Handle pictograph updates - simple and direct."""
        try:
            self.beat_modified.emit(beat_index, beat_data)
            logger.debug(f"Pictograph updated for beat {beat_index}")
        except Exception as e:
            logger.warning(f"Error handling pictograph update: {e}")

    def _on_orientation_changed(self, color: str, orientation) -> None:
        """Handle orientation changes - simple and direct."""
        try:
            # Convert enum to string for compatibility
            orientation_str = (
                orientation.value if hasattr(orientation, "value") else str(orientation)
            )

            orientation_data = {
                "color": color,
                "orientation": orientation_str,
                "type": "orientation_change",
            }
            self.arrow_selected.emit(orientation_data)
            logger.debug(f"{color} orientation changed to: {orientation_str}")

            # Trigger pictograph update immediately
            if self._selected_beat_data and self._pictograph_display:
                self._pictograph_display.update_pictograph_only(
                    self._selected_beat_index or 0, self._selected_beat_data
                )

        except Exception as e:
            logger.warning(f"Error handling orientation change: {e}")

    def _on_turn_amount_changed(self, color: str, turn_amount: int) -> None:
        """Handle turn amount changes - simple and direct."""
        try:
            turn_data = {
                "color": color,
                "turn_amount": turn_amount,
                "type": "turn_change",
            }
            self.arrow_selected.emit(turn_data)
            logger.debug(f"{color} turn amount changed to: {turn_amount}")
        except Exception as e:
            logger.warning(f"Error handling turn amount change: {e}")

    # Public API Methods - Clean and Simple
    def set_sequence(self, sequence: Optional[SequenceData]) -> bool:
        """Set the sequence data with clean error handling."""
        try:
            # Basic input validation (keep simple)
            if sequence is not None:
                validation_result = validate_sequence_data(sequence, allow_none=False)
                if not validation_result.is_valid:
                    logger.warning(f"Invalid sequence data: {validation_result.errors}")
                    return False

            # Core logic (the actual work)
            self._current_sequence = sequence

            logger.debug(f"Sequence set: {sequence.name if sequence else 'None'}")
            return True

        except Exception as e:
            logger.error(f"Error setting sequence: {e}")
            return False

    def update_current_sequence(self, sequence: Optional[SequenceData]) -> bool:
        """Update the current sequence when it's modified externally."""
        return self.set_sequence(sequence)

    def set_selected_beat_data(
        self, beat_index: int, beat_data: Optional[BeatData]
    ) -> bool:
        """Set the selected beat data with clean error handling."""
        try:
            # Basic input validation (keep simple)
            if beat_index < -1:
                logger.warning(f"Invalid beat index: {beat_index}")
                return False

            # Core logic (the actual work)
            self._selected_beat_index = beat_index
            self._selected_beat_data = beat_data

            # Update components
            if self._pictograph_display:
                self._pictograph_display.update_display(beat_index, beat_data)
            if self._adjustment_panel:
                self._adjustment_panel.set_beat_data(beat_index, beat_data)

            # Update session state
            if self._session_service:
                self._session_service.update_graph_editor_state(
                    visible=self.isVisible(),
                    beat_index=beat_index,
                    selected_arrow=self._get_current_selected_arrow(),
                    height=self.height(),
                )

            logger.debug(f"Beat data set successfully: {beat_index}")
            return True

        except Exception as e:
            logger.error(f"Error setting beat data: {e}")
            return False

    def get_current_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence data."""
        return self._current_sequence

    def get_selected_beat_index(self) -> Optional[int]:
        """Get the currently selected beat index."""
        return self._selected_beat_index

    def _get_current_selected_arrow(self) -> Optional[str]:
        """Get the currently selected arrow identifier."""
        # Try to get selected arrow from adjustment panel
        if self._adjustment_panel and hasattr(
            self._adjustment_panel, "get_selected_arrow"
        ):
            return self._adjustment_panel.get_selected_arrow()

        # Default to None if no arrow is selected
        return None
