import logging
from typing import Optional, TYPE_CHECKING
from PyQt6.QtCore import QObject, pyqtSignal

from domain.models.core_models import SequenceData, BeatData

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ..graph_editor import GraphEditor


class GraphEditorSignalCoordinator(QObject):
    """
    Manages all signal connections and coordination between graph editor components.

    Responsibilities:
    - Connect internal component signals
    - Handle data flow service signals
    - Handle hotkey service signals
    - Coordinate signal emissions between components
    - Act as signal mediator/router
    """

    # Re-exposed signals from graph editor (for external consumption)
    beat_modified = pyqtSignal(BeatData)
    arrow_selected = pyqtSignal(str)  # arrow_id
    visibility_changed = pyqtSignal(bool)  # is_visible

    def __init__(self, graph_editor: "GraphEditor", parent: Optional[QObject] = None):
        super().__init__(parent)
        self._graph_editor = graph_editor

        # Will be set during initialization
        self._data_flow_service = None
        self._hotkey_service = None

        self._layout_manager = None
        self._state_manager = None

    def set_dependencies(
        self,
        data_flow_service,
        hotkey_service,
        layout_manager,
        state_manager,
    ) -> None:
        """Set component dependencies after initialization"""
        self._data_flow_service = data_flow_service
        self._hotkey_service = hotkey_service
        self._layout_manager = layout_manager
        self._state_manager = state_manager

        # Connect all signals now that dependencies are available
        self._connect_all_signals()

    def _connect_all_signals(self) -> None:
        """Connect all component signals"""
        self._connect_data_flow_signals()
        self._connect_hotkey_signals()

        self._connect_ui_component_signals()

    def _connect_data_flow_signals(self) -> None:
        """Connect data flow service signals to UI updates"""
        if self._data_flow_service:
            self._data_flow_service.beat_data_updated.connect(
                self._on_beat_data_updated
            )
            self._data_flow_service.pictograph_refresh_needed.connect(
                self._on_pictograph_refresh_needed
            )
            self._data_flow_service.sequence_modified.connect(
                self._on_sequence_modified
            )

    def _connect_hotkey_signals(self) -> None:
        """Connect hotkey service signals"""
        if self._hotkey_service:
            self._hotkey_service.arrow_moved.connect(self._on_arrow_moved)
            self._hotkey_service.rotation_override_requested.connect(
                self._on_rotation_override
            )
            self._hotkey_service.special_placement_removal_requested.connect(
                self._on_special_placement_removal
            )
            self._hotkey_service.prop_placement_override_requested.connect(
                self._on_prop_placement_override
            )

    def _connect_ui_component_signals(self) -> None:
        """Connect UI component signals (pictograph container, adjustment panels)"""

        # Pictograph container signals
        if (
            hasattr(self._graph_editor, "_pictograph_container")
            and self._graph_editor._pictograph_container
        ):
            self._graph_editor._pictograph_container.arrow_selected.connect(
                self._on_arrow_selected
            )

        # Adjustment panel signals
        self._connect_adjustment_panel_signals()

    def _connect_adjustment_panel_signals(self) -> None:
        """Connect both adjustment panel signals"""
        # Left adjustment panel
        if (
            hasattr(self._graph_editor, "_left_adjustment_panel")
            and self._graph_editor._left_adjustment_panel
        ):
            self._graph_editor._left_adjustment_panel.beat_modified.connect(
                self._on_beat_modified
            )
            self._graph_editor._left_adjustment_panel.turn_applied.connect(
                self._on_turn_applied
            )

        # Right adjustment panel
        if (
            hasattr(self._graph_editor, "_right_adjustment_panel")
            and self._graph_editor._right_adjustment_panel
        ):
            self._graph_editor._right_adjustment_panel.beat_modified.connect(
                self._on_beat_modified
            )
            self._graph_editor._right_adjustment_panel.turn_applied.connect(
                self._on_turn_applied
            )

    # Data Flow Signal Handlers
    def _on_beat_data_updated(self, beat_data: BeatData, beat_index: int) -> None:
        """Handle beat data updates from data flow service"""
        # Update state
        self._state_manager.set_selected_beat_data(beat_data, beat_index)

        # Update UI components
        self._update_all_components_with_beat(beat_data)

    def _on_pictograph_refresh_needed(self, beat_data: BeatData) -> None:
        """Handle pictograph refresh requests"""
        if (
            hasattr(self._graph_editor, "_pictograph_container")
            and self._graph_editor._pictograph_container
        ):
            self._graph_editor._pictograph_container.refresh_display(beat_data)

    def _on_sequence_modified(self, sequence: SequenceData) -> None:
        """Handle sequence modification from data flow service"""
        self._state_manager.set_current_sequence(sequence)

        # Emit signal to notify parent workbench
        selected_beat = self._state_manager.get_selected_beat()
        if selected_beat:
            self.beat_modified.emit(selected_beat)

    # Hotkey Signal Handlers
    def _on_arrow_moved(self, arrow_id: str, delta_x: int, delta_y: int) -> None:
        """Handle arrow movement from hotkeys"""
        logger.debug("Moving arrow %s by (%d, %d)", arrow_id, delta_x, delta_y)
        # TODO: Implement arrow position adjustment
        # This should update the arrow's position in the pictograph

    def _on_rotation_override(self, arrow_id: str) -> None:
        """Handle rotation override (X key)"""
        logger.debug("Rotation override for arrow %s", arrow_id)
        # TODO: Implement rotation override logic

    def _on_special_placement_removal(self, arrow_id: str) -> None:
        """Handle special placement removal (Z key)"""
        logger.debug("Removing special placement for arrow %s", arrow_id)
        # TODO: Implement special placement removal

    def _on_prop_placement_override(self, arrow_id: str) -> None:
        """Handle prop placement override (C key)"""
        logger.debug("Prop placement override for arrow %s", arrow_id)
        # TODO: Implement prop placement override

    # UI Component Signal Handlers

    def _on_arrow_selected(self, arrow_id: str) -> None:
        """Handle arrow selection from pictograph container"""
        # Update state
        self._state_manager.set_selected_arrow_id(arrow_id)

        # Update service
        self._graph_editor._graph_service.set_arrow_selection(arrow_id)

        # Update adjustment panels
        self._update_adjustment_panels_for_arrow(arrow_id)

        # Emit signal
        self.arrow_selected.emit(arrow_id)

    def _on_beat_modified(self, beat_data: BeatData) -> None:
        """Handle beat modification from adjustment panel"""
        # Update state
        self._state_manager.set_selected_beat_data(beat_data)

        # Apply modifications through service
        updated_beat = self._graph_editor._graph_service.update_beat_adjustments(
            beat_data
        )

        # Update pictograph display
        if (
            hasattr(self._graph_editor, "_pictograph_container")
            and self._graph_editor._pictograph_container
        ):
            self._graph_editor._pictograph_container.set_beat(updated_beat)

        # Emit signal
        self.beat_modified.emit(updated_beat)

    def _on_turn_applied(self, arrow_color: str, turn_value: float) -> None:
        """Handle turn adjustment application"""
        success = self._graph_editor._graph_service.apply_turn_adjustment(
            arrow_color, turn_value
        )
        if success:
            selected_beat = self._state_manager.get_selected_beat()
            if selected_beat:
                self._refresh_display()

    # Helper Methods
    def _update_all_components_with_beat(self, beat_data: BeatData) -> None:
        """Update all UI components with new beat data"""
        # Update pictograph container
        if (
            hasattr(self._graph_editor, "_pictograph_container")
            and self._graph_editor._pictograph_container
        ):
            self._graph_editor._pictograph_container.set_beat(beat_data)

        # Update adjustment panels
        if (
            hasattr(self._graph_editor, "_left_adjustment_panel")
            and self._graph_editor._left_adjustment_panel
        ):
            self._graph_editor._left_adjustment_panel.set_beat(beat_data)
        if (
            hasattr(self._graph_editor, "_right_adjustment_panel")
            and self._graph_editor._right_adjustment_panel
        ):
            self._graph_editor._right_adjustment_panel.set_beat(beat_data)

    def _update_adjustment_panels_for_arrow(self, arrow_id: str) -> None:
        """Update adjustment panels for selected arrow"""
        if (
            hasattr(self._graph_editor, "_left_adjustment_panel")
            and self._graph_editor._left_adjustment_panel
        ):
            self._graph_editor._left_adjustment_panel.set_selected_arrow(arrow_id)
        if (
            hasattr(self._graph_editor, "_right_adjustment_panel")
            and self._graph_editor._right_adjustment_panel
        ):
            self._graph_editor._right_adjustment_panel.set_selected_arrow(arrow_id)

    def _refresh_display(self) -> None:
        """Refresh display after modifications"""
        selected_beat = self._state_manager.get_selected_beat()
        if selected_beat:
            updated_beat = self._graph_editor._graph_service.get_selected_beat()
            if updated_beat:
                self._state_manager.set_selected_beat_data(updated_beat)
                self._update_all_components_with_beat(updated_beat)

    # Public methods for reconnecting signals when components are created/destroyed
    def reconnect_ui_component_signals(self) -> None:
        """Reconnect UI component signals (useful after component recreation)"""
        self._connect_ui_component_signals()

    def emit_beat_modified(self, beat_data: BeatData) -> None:
        """Emit beat modified signal (for external triggering)"""
        self.beat_modified.emit(beat_data)

    def emit_arrow_selected(self, arrow_id: str) -> None:
        """Emit arrow selected signal (for external triggering)"""
        self.arrow_selected.emit(arrow_id)

    def emit_visibility_changed(self, is_visible: bool) -> None:
        """Emit visibility changed signal (for external triggering)"""
        self.visibility_changed.emit(is_visible)
