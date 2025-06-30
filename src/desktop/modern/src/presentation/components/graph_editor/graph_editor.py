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
- Comprehensive error handling and recovery mechanisms
"""

import logging
from typing import Optional, TYPE_CHECKING, Dict, Any, Tuple

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSplitter, QLabel
from PyQt6.QtCore import pyqtSignal, Qt

from domain.models.core_models import SequenceData, BeatData, Orientation
from core.interfaces.workbench_services import IGraphEditorService

# Import refactored components
from .components.pictograph_display_section import PictographDisplaySection
from .components.main_adjustment_panel import MainAdjustmentPanel

# Import validation utilities
from .utils.validation import (
    ValidationError,
    ValidationResult,
    validate_beat_data,
    validate_sequence_data,
    validate_beat_index,
    validate_orientation,
)

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

    # Internal signal for sequence updates
    sequence_updated = pyqtSignal(object)  # sequence_data

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

        # Error handling and recovery state
        self._initialization_successful = False
        self._component_errors: Dict[str, str] = {}
        self._recovery_attempts = 0
        self._max_recovery_attempts = 3
        self._fallback_mode_enabled = False
        self._last_known_good_state: Optional[Dict[str, Any]] = None

        # Initialize with comprehensive error handling
        try:
            self._initialize_with_error_handling(workbench_width, workbench_height)
            self._initialization_successful = True
            logger.info(
                "Professional graph editor initialized successfully (refactored)"
            )
        except Exception as e:
            self._handle_initialization_error(e)

    def _initialize_with_error_handling(
        self, workbench_width: int, workbench_height: int
    ) -> None:
        """Initialize the graph editor with comprehensive error handling."""
        try:
            # Set up the UI with error handling
            self._setup_ui_safe()

            # Apply styling with error handling
            self._setup_styling_safe()

            # Connect signals with error handling
            self._connect_signals_safe()

            # Connect internal signals
            self._connect_internal_signals_safe()

            # Set initial size with validation
            self._set_initial_size_safe(workbench_width, workbench_height)

        except Exception as e:
            logger.error(f"Error during graph editor initialization: {e}")
            raise

    def _handle_initialization_error(self, error: Exception) -> None:
        """Handle initialization errors with fallback mechanisms."""
        logger.error(f"Graph editor initialization failed: {error}")
        self._component_errors["initialization"] = str(error)

        try:
            # Attempt minimal fallback initialization
            self._create_fallback_ui()
            self._fallback_mode_enabled = True
            logger.warning(
                "Graph editor running in fallback mode due to initialization error"
            )
        except Exception as fallback_error:
            logger.critical(f"Fallback initialization also failed: {fallback_error}")
            # Create absolute minimal UI
            self._create_minimal_error_ui(error)

    def _setup_ui_safe(self) -> None:
        """Set up the professional user interface with comprehensive error handling."""
        try:
            # Validate parent widget state
            if not self.isWidgetType():
                raise RuntimeError(
                    "Graph editor widget is not in valid state for UI setup"
                )

            # Main layout with error handling
            main_layout = self._create_main_layout_safe()

            # Create vertical splitter with error handling
            main_splitter = self._create_main_splitter_safe()

            # Create components with error handling
            self._create_components_safe(main_splitter)

            # Finalize layout
            main_layout.addWidget(main_splitter)

            logger.debug("UI setup completed successfully")

        except Exception as e:
            logger.error(f"Error during UI setup: {e}")
            self._component_errors["ui_setup"] = str(e)
            raise

    def _create_main_layout_safe(self) -> QVBoxLayout:
        """Create main layout with error handling."""
        try:
            main_layout = QVBoxLayout(self)
            main_layout.setContentsMargins(10, 10, 10, 10)
            main_layout.setSpacing(10)
            return main_layout
        except Exception as e:
            logger.error(f"Failed to create main layout: {e}")
            raise RuntimeError(f"Main layout creation failed: {e}")

    def _create_main_splitter_safe(self) -> QSplitter:
        """Create main splitter with error handling."""
        try:
            main_splitter = QSplitter(Qt.Orientation.Vertical)
            main_splitter.setChildrenCollapsible(False)
            return main_splitter
        except Exception as e:
            logger.error(f"Failed to create main splitter: {e}")
            raise RuntimeError(f"Main splitter creation failed: {e}")

    def _create_components_safe(self, main_splitter: QSplitter) -> None:
        """Create UI components with comprehensive error handling."""
        try:
            # Create pictograph display section with error handling
            self._create_pictograph_display_safe(main_splitter)

            # Create adjustment panel with error handling
            self._create_adjustment_panel_safe(main_splitter)

            # Set splitter proportions
            main_splitter.setSizes(
                [150, 150]
            )  # Equal proportions for 300px total height

        except Exception as e:
            logger.error(f"Error creating components: {e}")
            self._component_errors["component_creation"] = str(e)
            raise

    def _create_pictograph_display_safe(self, main_splitter: QSplitter) -> None:
        """Create pictograph display section with error handling."""
        try:
            self._pictograph_display = PictographDisplaySection(parent=self)
            if self._pictograph_display is None:
                raise RuntimeError("PictographDisplaySection creation returned None")
            main_splitter.addWidget(self._pictograph_display)
            logger.debug("Pictograph display section created successfully")
        except Exception as e:
            logger.error(f"Failed to create pictograph display section: {e}")
            self._component_errors["pictograph_display"] = str(e)
            self._fallback_mode_enabled = (
                True  # Enable fallback mode on component failure
            )
            # Create fallback label
            fallback_label = QLabel("Pictograph display unavailable")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fallback_label.setStyleSheet("color: red; padding: 20px;")
            main_splitter.addWidget(fallback_label)

    def _create_adjustment_panel_safe(self, main_splitter: QSplitter) -> None:
        """Create adjustment panel with error handling."""
        try:
            self._adjustment_panel = MainAdjustmentPanel(parent=self)
            if self._adjustment_panel is None:
                raise RuntimeError("MainAdjustmentPanel creation returned None")
            main_splitter.addWidget(self._adjustment_panel)
            logger.debug("Adjustment panel created successfully")
        except Exception as e:
            logger.error(f"Failed to create adjustment panel: {e}")
            self._component_errors["adjustment_panel"] = str(e)
            self._fallback_mode_enabled = (
                True  # Enable fallback mode on component failure
            )
            # Create fallback label
            fallback_label = QLabel("Adjustment panel unavailable")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fallback_label.setStyleSheet("color: red; padding: 20px;")
            main_splitter.addWidget(fallback_label)

    def _setup_ui(self) -> None:
        """Legacy UI setup method - redirects to safe version."""
        self._setup_ui_safe()

    def _connect_signals_safe(self) -> None:
        """Connect signals from components with comprehensive error handling."""
        try:
            # Connect pictograph display signals with error handling
            self._connect_pictograph_signals_safe()

            # Connect adjustment panel signals with error handling
            self._connect_adjustment_panel_signals_safe()

            logger.debug("Signal connections completed successfully")

        except Exception as e:
            logger.error(f"Error during signal connection: {e}")
            self._component_errors["signal_connection"] = str(e)
            raise

    def _connect_pictograph_signals_safe(self) -> None:
        """Connect pictograph display signals with error handling."""
        if self._pictograph_display:
            try:
                # Check if signals exist before connecting
                if hasattr(self._pictograph_display, "pictograph_updated"):
                    self._pictograph_display.pictograph_updated.connect(
                        self._on_pictograph_updated_safe
                    )
                else:
                    logger.warning(
                        "Pictograph display missing pictograph_updated signal"
                    )

                if hasattr(self._pictograph_display, "info_panel_updated"):
                    self._pictograph_display.info_panel_updated.connect(
                        self._on_info_panel_updated_safe
                    )
                else:
                    logger.warning(
                        "Pictograph display missing info_panel_updated signal"
                    )

                logger.debug("Pictograph display signals connected successfully")

            except Exception as e:
                logger.error(f"Failed to connect pictograph display signals: {e}")
                self._component_errors["pictograph_signals"] = str(e)
        else:
            logger.warning(
                "Pictograph display component not available for signal connection"
            )

    def _connect_adjustment_panel_signals_safe(self) -> None:
        """Connect adjustment panel signals with error handling."""
        if self._adjustment_panel:
            try:
                # Check if signals exist before connecting
                signal_connections = [
                    ("orientation_changed", self._on_orientation_changed_safe),
                    ("turn_amount_changed", self._on_turn_amount_changed_safe),
                    (
                        "rotation_direction_changed",
                        self._on_rotation_direction_changed_safe,
                    ),
                    ("beat_data_updated", self._on_beat_data_updated_safe),
                ]

                for signal_name, handler in signal_connections:
                    if hasattr(self._adjustment_panel, signal_name):
                        signal = getattr(self._adjustment_panel, signal_name)
                        signal.connect(handler)
                    else:
                        logger.warning(f"Adjustment panel missing {signal_name} signal")

                logger.debug("Adjustment panel signals connected successfully")

            except Exception as e:
                logger.error(f"Failed to connect adjustment panel signals: {e}")
                self._component_errors["adjustment_panel_signals"] = str(e)
        else:
            logger.warning(
                "Adjustment panel component not available for signal connection"
            )

    def _connect_internal_signals_safe(self) -> None:
        """Connect internal signals for sequence updates."""
        try:
            # Connect sequence update signal to update method
            self.sequence_updated.connect(self._on_sequence_updated_safe)

            # Connect to parent workbench sequence_modified signal if available
            self._connect_to_parent_workbench_safe()

            logger.debug("Internal signals connected successfully")
        except Exception as e:
            logger.error(f"Error connecting internal signals: {e}")
            self._component_errors["internal_signals"] = str(e)

    def _connect_to_parent_workbench_safe(self) -> None:
        """Connect to parent workbench sequence_modified signal if available."""
        try:
            if self._parent_workbench and hasattr(
                self._parent_workbench, "sequence_modified"
            ):
                # Connect workbench sequence_modified signal to our notification method
                self._parent_workbench.sequence_modified.connect(
                    self._on_workbench_sequence_modified_safe
                )
                logger.debug("Connected to parent workbench sequence_modified signal")
            else:
                logger.debug(
                    "No parent workbench or sequence_modified signal available"
                )
        except Exception as e:
            logger.error(f"Error connecting to parent workbench signals: {e}")
            self._component_errors["parent_workbench_signals"] = str(e)

    def _on_workbench_sequence_modified_safe(
        self, sequence: Optional[SequenceData]
    ) -> None:
        """Handle sequence modification signals from parent workbench."""
        try:
            # Use our existing notification method to update the sequence
            success = self.notify_sequence_updated(sequence)
            if success:
                logger.debug(
                    f"Successfully updated sequence from workbench: {sequence.name if sequence else 'None'}"
                )
            else:
                logger.warning("Failed to update sequence from workbench signal")
        except Exception as e:
            logger.error(f"Error handling workbench sequence modification: {e}")
            self._component_errors["workbench_sequence_modified"] = str(e)

    def _on_sequence_updated_safe(self, sequence: Optional[SequenceData]) -> None:
        """Handle sequence update signals safely."""
        try:
            success = self.update_current_sequence(sequence)
            if not success:
                logger.warning("Failed to update current sequence from signal")
        except Exception as e:
            logger.error(f"Error handling sequence update signal: {e}")
            self._component_errors["sequence_update_signal"] = str(e)

    def _connect_signals(self):
        """Legacy signal connection method - redirects to safe version."""
        self._connect_signals_safe()

    def _on_pictograph_updated_safe(self, beat_data: BeatData):
        """Handle pictograph update signals with error handling."""
        try:
            if beat_data is None:
                logger.warning("Received None beat_data in pictograph update")
                return

            if hasattr(beat_data, "letter"):
                logger.debug(f"Pictograph updated: {beat_data.letter}")
            else:
                logger.warning(
                    "Beat data missing letter attribute in pictograph update"
                )

        except Exception as e:
            logger.error(f"Error handling pictograph update: {e}")
            self._component_errors["pictograph_update"] = str(e)

    def _on_info_panel_updated_safe(self, beat_index: int, beat_data: BeatData):
        """Handle info panel update signals with error handling."""
        try:
            # Validate inputs
            if not isinstance(beat_index, int):
                logger.warning(f"Invalid beat_index type: {type(beat_index)}")
                return

            if beat_data is None:
                logger.warning("Received None beat_data in info panel update")
                return

            logger.debug(f"Info panel updated for beat {beat_index}")

        except Exception as e:
            logger.error(f"Error handling info panel update: {e}")
            self._component_errors["info_panel_update"] = str(e)

    def _on_orientation_changed_safe(self, color: str, orientation):
        """Handle orientation change signals with error handling."""
        try:
            # Validate inputs
            if not isinstance(color, str) or not color:
                logger.warning(f"Invalid color parameter: {color}")
                return

            # Validate orientation using validation utility
            orientation_validation = validate_orientation(orientation, allow_none=False)
            if not orientation_validation.is_valid:
                logger.warning(
                    f"Invalid orientation parameter: {orientation_validation.errors}"
                )
                return

            # Get orientation value for signal emission
            if isinstance(orientation, Orientation):
                orientation_value = orientation.value
            else:
                orientation_value = orientation  # Already validated as string

            # Emit legacy signal for backward compatibility (using string value)
            orientation_data = {
                "color": color,
                "orientation": orientation_value,
                "type": "orientation_change",
            }
            self.arrow_selected.emit(orientation_data)
            logger.debug(f"{color.title()} orientation changed to: {orientation_value}")

        except Exception as e:
            logger.error(f"Error handling orientation change: {e}")
            self._component_errors["orientation_change"] = str(e)

    def _on_turn_amount_changed_safe(self, color: str, amount: float):
        """Handle turn amount change signals with error handling."""
        try:
            # Validate inputs
            if not isinstance(color, str) or not color:
                logger.warning(f"Invalid color parameter: {color}")
                return

            if not isinstance(amount, (int, float)):
                logger.warning(f"Invalid amount parameter: {amount}")
                return

            # Emit legacy signal for backward compatibility
            turn_data = {"color": color, "amount": amount, "type": "turn_amount"}
            self.beat_modified.emit(0, turn_data)  # Use 0 as placeholder beat index
            logger.debug(f"{color.title()} turn amount changed to: {amount}")

        except Exception as e:
            logger.error(f"Error handling turn amount change: {e}")
            self._component_errors["turn_amount_change"] = str(e)

    def _on_rotation_direction_changed_safe(self, color: str, direction: str):
        """Handle rotation direction change signals with error handling."""
        try:
            # Validate inputs
            if not isinstance(color, str) or not color:
                logger.warning(f"Invalid color parameter: {color}")
                return

            if not isinstance(direction, str) or not direction:
                logger.warning(f"Invalid direction parameter: {direction}")
                return

            # Emit legacy signal for backward compatibility
            rotation_data = {
                "color": color,
                "direction": direction,
                "type": "rotation_direction",
            }
            self.beat_modified.emit(0, rotation_data)  # Use 0 as placeholder beat index
            logger.debug(f"{color.title()} rotation direction changed to: {direction}")

        except Exception as e:
            logger.error(f"Error handling rotation direction change: {e}")
            self._component_errors["rotation_direction_change"] = str(e)

    def _on_beat_data_updated_safe(self, beat_data: BeatData):
        """Handle beat data update signals with error handling."""
        try:
            # Validate beat data
            validation_result = validate_beat_data(beat_data, allow_none=False)
            if not validation_result.is_valid:
                logger.warning(
                    f"Invalid beat data in update: {validation_result.errors}"
                )
                return

            self._selected_beat_data = beat_data

            # Update pictograph display with new data
            if self._pictograph_display:
                try:
                    self._pictograph_display.update_pictograph_only(beat_data)
                except Exception as display_error:
                    logger.error(
                        f"Failed to update pictograph display: {display_error}"
                    )
                    self._component_errors["pictograph_display_update"] = str(
                        display_error
                    )

            logger.debug("Beat data updated and pictograph refreshed")

        except Exception as e:
            logger.error(f"Error handling beat data update: {e}")
            self._component_errors["beat_data_update"] = str(e)

    # Legacy signal handlers (redirect to safe versions)
    def _on_pictograph_updated(self, beat_data: BeatData):
        """Legacy handler - redirects to safe version."""
        self._on_pictograph_updated_safe(beat_data)

    def _on_info_panel_updated(self, beat_index: int, beat_data: BeatData):
        """Legacy handler - redirects to safe version."""
        self._on_info_panel_updated_safe(beat_index, beat_data)

    def _on_orientation_changed(self, color: str, orientation):
        """Legacy handler - redirects to safe version."""
        self._on_orientation_changed_safe(color, orientation)

    def _on_turn_amount_changed(self, color: str, amount: float):
        """Legacy handler - redirects to safe version."""
        self._on_turn_amount_changed_safe(color, amount)

    def _on_rotation_direction_changed(self, color: str, direction: str):
        """Legacy handler - redirects to safe version."""
        self._on_rotation_direction_changed_safe(color, direction)

    def _on_beat_data_updated(self, beat_data: BeatData):
        """Legacy handler - redirects to safe version."""
        self._on_beat_data_updated_safe(beat_data)

    def _setup_styling_safe(self) -> None:
        """Apply glassmorphism styling with error handling."""
        try:
            self._setup_styling()
            logger.debug("Styling applied successfully")
        except Exception as e:
            logger.error(f"Error applying styling: {e}")
            self._component_errors["styling"] = str(e)
            # Apply minimal fallback styling
            try:
                self.setStyleSheet(
                    "QFrame { background: white; border: 1px solid gray; }"
                )
                logger.warning("Applied fallback styling due to error")
            except Exception as fallback_error:
                logger.error(f"Fallback styling also failed: {fallback_error}")

    def _set_initial_size_safe(
        self, workbench_width: int, workbench_height: int
    ) -> None:
        """Set initial size with validation and error handling."""
        try:
            # Validate input parameters
            if not isinstance(workbench_width, int) or workbench_width <= 0:
                logger.warning(
                    f"Invalid workbench_width: {workbench_width}, using default"
                )
                workbench_width = 800

            if not isinstance(workbench_height, int) or workbench_height <= 0:
                logger.warning(
                    f"Invalid workbench_height: {workbench_height}, using default"
                )
                workbench_height = 600

            # Set minimum size with validation
            min_width, min_height = 400, 300
            self.setMinimumSize(min_width, min_height)

            # Set initial size
            self.resize(workbench_width, min_height)  # Fixed height for embedded mode

            logger.debug(f"Initial size set: {workbench_width}x{min_height}")

        except Exception as e:
            logger.error(f"Error setting initial size: {e}")
            self._component_errors["initial_size"] = str(e)
            # Try minimal fallback sizing
            try:
                self.setMinimumSize(400, 300)
                self.resize(800, 300)
                logger.warning("Applied fallback sizing due to error")
            except Exception as fallback_error:
                logger.error(f"Fallback sizing also failed: {fallback_error}")

    def _create_fallback_ui(self) -> None:
        """Create minimal fallback UI when normal initialization fails."""
        try:
            # Clear any existing layout
            if self.layout():
                self.layout().deleteLater()

            # Create simple layout
            layout = QVBoxLayout(self)
            layout.setContentsMargins(10, 10, 10, 10)

            # Add fallback message
            fallback_label = QLabel("Graph Editor (Fallback Mode)")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fallback_label.setStyleSheet(
                """
                QLabel {
                    background: rgba(255, 255, 0, 0.2);
                    border: 2px solid orange;
                    border-radius: 8px;
                    padding: 20px;
                    font-size: 14px;
                    font-weight: bold;
                    color: #333;
                }
            """
            )
            layout.addWidget(fallback_label)

            # Add error details if available
            if self._component_errors:
                error_text = "Errors:\n" + "\n".join(
                    f"• {k}: {v}" for k, v in self._component_errors.items()
                )
                error_label = QLabel(error_text)
                error_label.setWordWrap(True)
                error_label.setStyleSheet("color: red; font-size: 10px; padding: 10px;")
                layout.addWidget(error_label)

            logger.info("Fallback UI created successfully")

        except Exception as e:
            logger.critical(f"Failed to create fallback UI: {e}")
            raise

    def _create_minimal_error_ui(self, original_error: Exception) -> None:
        """Create absolute minimal error UI when all else fails."""
        try:
            # Clear any existing layout
            if self.layout():
                self.layout().deleteLater()

            # Create minimal layout
            layout = QVBoxLayout(self)

            # Add error message
            error_label = QLabel(f"Graph Editor Error: {str(original_error)[:100]}...")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_label.setStyleSheet("color: red; font-weight: bold; padding: 20px;")
            layout.addWidget(error_label)

            logger.critical("Minimal error UI created as last resort")

        except Exception as e:
            logger.critical(f"Even minimal error UI creation failed: {e}")
            # At this point, we can't do much more

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

    # Public API Methods (maintaining compatibility with comprehensive error handling)
    def set_sequence(self, sequence: Optional[SequenceData]) -> bool:
        """Set the sequence data for the graph editor with error handling.

        Returns:
            bool: True if sequence was set successfully, False otherwise
        """
        try:
            # Validate sequence data if provided
            if sequence is not None:
                validation_result = validate_sequence_data(sequence, allow_none=False)
                if not validation_result.is_valid:
                    logger.error(f"Invalid sequence data: {validation_result.errors}")
                    return False

            self._current_sequence = sequence
            logger.info(f"Sequence set: {sequence.name if sequence else 'None'}")
            return True

        except Exception as e:
            logger.error(f"Error setting sequence: {e}")
            self._component_errors["set_sequence"] = str(e)
            return False

    def update_current_sequence(self, sequence: Optional[SequenceData]) -> bool:
        """Update the current sequence when it's modified externally.

        This method is called when beats are added/removed/modified to keep
        the graph editor's sequence reference in sync.

        Returns:
            bool: True if sequence was updated successfully, False otherwise
        """
        try:
            # Validate sequence data if provided
            if sequence is not None:
                validation_result = validate_sequence_data(sequence, allow_none=False)
                if not validation_result.is_valid:
                    logger.warning(
                        f"Invalid sequence data in update: {validation_result.errors}"
                    )
                    return False

            # Update the current sequence reference
            old_sequence_name = (
                self._current_sequence.name if self._current_sequence else None
            )
            self._current_sequence = sequence
            new_sequence_name = sequence.name if sequence else None

            logger.debug(
                f"Sequence updated: {old_sequence_name} -> {new_sequence_name}"
            )
            return True

        except Exception as e:
            logger.error(f"Error updating current sequence: {e}")
            self._component_errors["update_current_sequence"] = str(e)
            return False

    def set_selected_beat_data(
        self, beat_index: int, beat_data: Optional[BeatData]
    ) -> bool:
        """Set the selected beat data and update the UI with comprehensive error handling.

        Returns:
            bool: True if beat data was set successfully, False otherwise
        """
        try:
            # Validate beat index
            sequence_length = (
                len(self._current_sequence.beats) if self._current_sequence else 0
            )
            index_validation = validate_beat_index(
                beat_index, sequence_length, allow_negative=True
            )
            if not index_validation.is_valid:
                logger.error(f"Invalid beat index: {index_validation.errors}")
                return False

            # Validate beat data if provided
            if beat_data is not None:
                beat_validation = validate_beat_data(beat_data, allow_none=False)
                if not beat_validation.is_valid:
                    logger.error(f"Invalid beat data: {beat_validation.errors}")
                    return False

            self._selected_beat_index = beat_index
            self._selected_beat_data = beat_data

            # Update pictograph display section with error handling
            if self._pictograph_display:
                try:
                    self._pictograph_display.update_display(beat_index, beat_data)
                except Exception as display_error:
                    logger.error(
                        f"Failed to update pictograph display: {display_error}"
                    )
                    self._component_errors["pictograph_display_update"] = str(
                        display_error
                    )

            # Update adjustment panel with error handling
            if self._adjustment_panel:
                try:
                    self._adjustment_panel.set_beat_data(beat_index, beat_data)
                except Exception as panel_error:
                    logger.error(f"Failed to update adjustment panel: {panel_error}")
                    self._component_errors["adjustment_panel_update"] = str(panel_error)

            logger.info(
                f"Beat selected: {beat_index} - {beat_data.letter if beat_data else 'None'}"
            )
            return True

        except Exception as e:
            logger.error(f"Error setting selected beat data: {e}")
            self._component_errors["set_selected_beat_data"] = str(e)
            return False

    def set_selected_start_position(self, start_position_data) -> bool:
        """Set the selected start position data with error handling.

        Returns:
            bool: True if start position was set successfully, False otherwise
        """
        try:
            # Validate start position data if it's a BeatData instance
            if hasattr(start_position_data, "letter"):  # Duck typing check for BeatData
                validation_result = validate_beat_data(
                    start_position_data, allow_none=False
                )
                if not validation_result.is_valid:
                    logger.error(
                        f"Invalid start position data: {validation_result.errors}"
                    )
                    return False

            # Update pictograph display section with error handling
            if self._pictograph_display:
                try:
                    self._pictograph_display.update_display(-1, start_position_data)
                except Exception as display_error:
                    logger.error(
                        f"Failed to update pictograph display for start position: {display_error}"
                    )
                    self._component_errors["start_position_display_update"] = str(
                        display_error
                    )

            # Update adjustment panel with error handling (force orientation mode for start positions)
            if self._adjustment_panel:
                try:
                    self._adjustment_panel.set_beat_data(-1, start_position_data)
                except Exception as panel_error:
                    logger.error(
                        f"Failed to update adjustment panel for start position: {panel_error}"
                    )
                    self._component_errors["start_position_panel_update"] = str(
                        panel_error
                    )

            logger.info(f"Start position set: {start_position_data}")
            return True

        except Exception as e:
            logger.error(f"Error setting start position: {e}")
            self._component_errors["set_selected_start_position"] = str(e)
            return False

    def notify_sequence_updated(self, sequence: Optional[SequenceData]) -> bool:
        """Notify the graph editor that the sequence has been updated externally.

        This method should be called by parent components when beats are added,
        removed, or modified to keep the graph editor's sequence reference in sync.

        Args:
            sequence: The updated sequence data

        Returns:
            bool: True if notification was processed successfully, False otherwise
        """
        try:
            # Emit the internal signal to trigger the update
            self.sequence_updated.emit(sequence)
            return True
        except Exception as e:
            logger.error(f"Error notifying sequence update: {e}")
            self._component_errors["notify_sequence_updated"] = str(e)
            return False

    def toggle_visibility(self) -> bool:
        """Toggle graph editor visibility with error handling.

        Returns:
            bool: True if visibility was toggled successfully, False otherwise
        """
        try:
            if self.isVisible():
                self.hide()
            else:
                self.show()

            # Emit signal with error handling
            try:
                self.visibility_changed.emit(self.isVisible())
            except Exception as signal_error:
                logger.error(
                    f"Failed to emit visibility changed signal: {signal_error}"
                )
                # Don't return False here as the visibility change itself succeeded

            logger.debug(f"Visibility toggled to: {self.isVisible()}")
            return True

        except Exception as e:
            logger.error(f"Error toggling visibility: {e}")
            self._component_errors["toggle_visibility"] = str(e)
            return False

    def get_preferred_height(self) -> int:
        """Get the preferred height for the graph editor"""
        return 300

    def update_workbench_size(self, width: int, height: int) -> None:
        """Update workbench size reference when workbench resizes"""
        # Not needed for embedded mode - parameters kept for interface compatibility
        # Suppress unused parameter warnings by referencing them
        _ = width, height

    def sync_width_with_workbench(self) -> None:
        """Synchronize graph editor width with parent workbench width"""
        pass  # Not needed for embedded mode

    # Error handling and recovery utility methods
    def get_component_errors(self) -> Dict[str, str]:
        """Get current component errors for debugging.

        Returns:
            Dict[str, str]: Dictionary of component names to error messages
        """
        return self._component_errors.copy()

    def clear_component_errors(self) -> None:
        """Clear all component errors."""
        self._component_errors.clear()
        logger.debug("Component errors cleared")

    def is_initialization_successful(self) -> bool:
        """Check if initialization was successful.

        Returns:
            bool: True if initialization completed without errors
        """
        return self._initialization_successful

    def is_fallback_mode_enabled(self) -> bool:
        """Check if the graph editor is running in fallback mode.

        Returns:
            bool: True if running in fallback mode due to errors
        """
        return self._fallback_mode_enabled

    def attempt_component_recovery(self) -> bool:
        """Attempt to recover from component errors.

        Returns:
            bool: True if recovery was successful, False otherwise
        """
        if self._recovery_attempts >= self._max_recovery_attempts:
            logger.warning("Maximum recovery attempts reached, cannot attempt recovery")
            return False

        try:
            self._recovery_attempts += 1
            logger.info(
                f"Attempting component recovery (attempt {self._recovery_attempts})"
            )

            # Clear previous errors
            self.clear_component_errors()

            # Attempt to reinitialize components
            if not self._pictograph_display:
                try:
                    self._pictograph_display = PictographDisplaySection(parent=self)
                    logger.info("Successfully recovered pictograph display component")
                except Exception as e:
                    logger.error(f"Failed to recover pictograph display: {e}")
                    self._component_errors["pictograph_recovery"] = str(e)

            if not self._adjustment_panel:
                try:
                    self._adjustment_panel = MainAdjustmentPanel(parent=self)
                    logger.info("Successfully recovered adjustment panel component")
                except Exception as e:
                    logger.error(f"Failed to recover adjustment panel: {e}")
                    self._component_errors["adjustment_panel_recovery"] = str(e)

            # Reconnect signals if components were recovered
            if self._pictograph_display or self._adjustment_panel:
                try:
                    self._connect_signals_safe()
                    logger.info("Successfully reconnected signals after recovery")
                except Exception as e:
                    logger.error(f"Failed to reconnect signals after recovery: {e}")
                    self._component_errors["signal_recovery"] = str(e)

            # Check if recovery was successful
            recovery_successful = len(self._component_errors) == 0
            if recovery_successful:
                logger.info("Component recovery completed successfully")
                self._fallback_mode_enabled = False
            else:
                logger.warning(
                    f"Component recovery partially failed: {self._component_errors}"
                )

            return recovery_successful

        except Exception as e:
            logger.error(f"Component recovery attempt failed: {e}")
            self._component_errors["recovery_failure"] = str(e)
            return False

    def get_error_summary(self) -> str:
        """Get a summary of current errors for user display.

        Returns:
            str: Human-readable error summary
        """
        if not self._component_errors:
            return "No errors detected"

        error_count = len(self._component_errors)
        if error_count == 1:
            error_name, error_msg = next(iter(self._component_errors.items()))
            return f"Error in {error_name}: {error_msg[:100]}..."

        # Include component names for better debugging
        component_names = ", ".join(self._component_errors.keys())
        return f"{error_count} component errors detected in: {component_names}. Check logs for details."

    def validate_current_state(self) -> ValidationResult:
        """Validate the current state of the graph editor.

        Returns:
            ValidationResult: Comprehensive validation result
        """
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        try:
            # Check initialization state
            if not self._initialization_successful:
                result.add_error(
                    "Graph editor initialization failed", "initialization", None
                )

            # Check component availability
            if not self._pictograph_display:
                result.add_error(
                    "Pictograph display component not available",
                    "pictograph_display",
                    None,
                )

            if not self._adjustment_panel:
                result.add_error(
                    "Adjustment panel component not available", "adjustment_panel", None
                )

            # Check for component errors
            if self._component_errors:
                for component, error in self._component_errors.items():
                    result.add_error(f"Component error: {error}", component, None)

            # Check fallback mode
            if self._fallback_mode_enabled:
                result.add_warning("Graph editor is running in fallback mode")

            # Validate current data
            if self._current_sequence:
                seq_validation = validate_sequence_data(self._current_sequence)
                if not seq_validation.is_valid:
                    result.errors.extend(seq_validation.errors)
                    result.is_valid = False

            if self._selected_beat_data:
                beat_validation = validate_beat_data(self._selected_beat_data)
                if not beat_validation.is_valid:
                    result.errors.extend(beat_validation.errors)
                    result.is_valid = False

        except Exception as e:
            result.add_error(
                f"Error during state validation: {str(e)}", "validation", None
            )

        return result

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
