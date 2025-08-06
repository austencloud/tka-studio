"""
Qt Signal-Based Coordinator for ConstructTab

Replaces event bus architecture with pure PyQt6 signals for component coordination.
Provides clean signal/slot communication between ConstructTab components.
"""

from __future__ import annotations

import logging
from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.domain.models.beat_data import BeatData


logger = logging.getLogger(__name__)


class ConstructTabSignalCoordinator(QObject):
    """
    Qt signal-based coordinator for ConstructTab components.

    Replaces event bus with pure PyQt6 signals for clean component communication.
    All components connect to these signals for coordination.
    """

    # Sequence signals
    sequence_created = pyqtSignal(str, str, int)  # sequence_id, name, length
    sequence_updated = pyqtSignal(str, dict)  # sequence_id, update_data
    beat_added = pyqtSignal(
        str, object, int, int
    )  # sequence_id, beat_data, position, total_beats
    beat_updated = pyqtSignal(
        str, int, str, object, object
    )  # sequence_id, beat_number, field, old_value, new_value
    beat_removed = pyqtSignal(
        str, int, int
    )  # sequence_id, beat_number, remaining_beats

    # UI state signals
    start_position_selected = pyqtSignal(str)  # position_key
    option_picker_selection = pyqtSignal(object)  # pictograph_data
    component_visibility_changed = pyqtSignal(str, bool)  # component_name, visible

    # Layout signals
    layout_recalculated = pyqtSignal(dict)  # layout_data
    component_resized = pyqtSignal(str, object)  # component_name, new_size
    layout_transition_requested = pyqtSignal(
        str
    )  # target_view ("start_position_picker", "option_picker", etc.)

    # Generation signals
    generation_started = pyqtSignal(dict)  # generation_config
    generation_completed = pyqtSignal(list)  # generated_beats
    generation_failed = pyqtSignal(str)  # error_message

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

        # Component references for direct method calls when needed
        self.components: dict[str, Any] = {}

        self.logger.info("Qt signal coordinator initialized")

    def register_component(self, name: str, component: Any) -> None:
        """Register a component for coordination."""
        self.components[name] = component
        self.logger.debug(f"Registered component: {name}")

    def unregister_component(self, name: str) -> None:
        """Unregister a component."""
        if name in self.components:
            del self.components[name]
            self.logger.debug(f"Unregistered component: {name}")

    # Signal emission methods (called by components to notify others)

    def emit_sequence_created(self, sequence_id: str, name: str, length: int) -> None:
        """Emit sequence creation signal."""
        self.sequence_created.emit(sequence_id, name, length)
        self.logger.info(f"Emitted sequence_created: {sequence_id}")

    def emit_sequence_updated(self, sequence_id: str, update_data: dict) -> None:
        """Emit sequence update signal."""
        self.sequence_updated.emit(sequence_id, update_data)
        self.logger.info(f"Emitted sequence_updated: {sequence_id}")

    def emit_beat_added(
        self, sequence_id: str, beat_data: BeatData, position: int, total_beats: int
    ) -> None:
        """Emit beat addition signal."""
        self.beat_added.emit(sequence_id, beat_data, position, total_beats)
        self.logger.info(
            f"Emitted beat_added: sequence {sequence_id}, position {position}"
        )

    def emit_beat_updated(
        self,
        sequence_id: str,
        beat_number: int,
        field: str,
        old_value: Any,
        new_value: Any,
    ) -> None:
        """Emit beat update signal."""
        self.beat_updated.emit(sequence_id, beat_number, field, old_value, new_value)
        self.logger.info(
            f"Emitted beat_updated: sequence {sequence_id}, beat {beat_number}, field {field}"
        )

    def emit_beat_removed(
        self, sequence_id: str, beat_number: int, remaining_beats: int
    ) -> None:
        """Emit beat removal signal."""
        self.beat_removed.emit(sequence_id, beat_number, remaining_beats)
        self.logger.info(
            f"Emitted beat_removed: sequence {sequence_id}, beat {beat_number}"
        )

    def emit_start_position_selected(self, position_key: str) -> None:
        """Emit start position selection signal."""
        self.start_position_selected.emit(position_key)
        self.logger.info(f"Emitted start_position_selected: {position_key}")

    def emit_option_picker_selection(self, pictograph_data: Any) -> None:
        """Emit option picker selection signal."""
        self.option_picker_selection.emit(pictograph_data)
        self.logger.info(
            f"Emitted option_picker_selection: {getattr(pictograph_data, 'letter', 'unknown')}"
        )

    def emit_component_visibility_changed(
        self, component_name: str, visible: bool
    ) -> None:
        """Emit component visibility change signal."""
        self.component_visibility_changed.emit(component_name, visible)
        self.logger.info(
            f"Emitted component_visibility_changed: {component_name} = {visible}"
        )

    def emit_layout_recalculated(self, layout_data: dict) -> None:
        """Emit layout recalculation signal."""
        self.layout_recalculated.emit(layout_data)
        self.logger.info("Emitted layout_recalculated")

    def emit_component_resized(self, component_name: str, new_size: Any) -> None:
        """Emit component resize signal."""
        self.component_resized.emit(component_name, new_size)
        self.logger.info(f"Emitted component_resized: {component_name}")

    def emit_layout_transition_requested(self, target_view: str) -> None:
        """Emit layout transition request signal."""
        self.layout_transition_requested.emit(target_view)
        self.logger.info(f"Emitted layout_transition_requested: {target_view}")

    def emit_generation_started(self, generation_config: dict) -> None:
        """Emit generation started signal."""
        self.generation_started.emit(generation_config)
        self.logger.info("Emitted generation_started")

    def emit_generation_completed(self, generated_beats: list) -> None:
        """Emit generation completed signal."""
        self.generation_completed.emit(generated_beats)
        self.logger.info(f"Emitted generation_completed: {len(generated_beats)} beats")

    def emit_generation_failed(self, error_message: str) -> None:
        """Emit generation failed signal."""
        self.generation_failed.emit(error_message)
        self.logger.error(f"Emitted generation_failed: {error_message}")

    # Convenience methods for common coordination patterns

    def request_transition_to_option_picker(self) -> None:
        """Request transition to option picker view."""
        self.emit_layout_transition_requested("option_picker")

    def request_transition_to_start_position_picker(self) -> None:
        """Request transition to start position picker view."""
        self.emit_layout_transition_requested("start_position_picker")

    def get_component(self, name: str) -> Any | None:
        """Get a registered component by name."""
        return self.components.get(name)

    def cleanup(self) -> None:
        """Cleanup coordinator resources."""
        self.components.clear()
        self.logger.info("Qt signal coordinator cleaned up")
