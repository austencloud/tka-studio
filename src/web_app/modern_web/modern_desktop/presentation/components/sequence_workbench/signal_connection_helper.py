"""
Signal Connection Helper - Simple extraction from SequenceWorkbench

Extracted signal connection methods without any changes to functionality.
Just moves the code to reduce the main file size.
"""

from __future__ import annotations

from shared.application.services.workbench.workbench_operation_coordinator import (
    OperationType,
)


class SignalConnectionHelper:
    """Helper class for workbench signal connections - simple extraction."""

    def __init__(self, workbench):
        self.workbench = workbench

    def connect_signals(self):
        """Connect component signals to business logic."""
        if self.workbench._beat_frame_section:
            # Beat frame signals -> business logic
            self.workbench._beat_frame_section.beat_selected.connect(
                self.workbench._on_beat_selected
            )
            self.workbench._beat_frame_section.beat_modified.connect(
                self.workbench._on_beat_modified
            )
            self.workbench._beat_frame_section.sequence_modified.connect(
                self.workbench._on_sequence_modified
            )

            # Operation signals -> operation coordinator
            self.workbench._beat_frame_section.add_to_dictionary_requested.connect(
                lambda: self.workbench._execute_operation(
                    OperationType.ADD_TO_DICTIONARY
                )
            )
            # save_image_requested signal removed - functionality moved to Export tab
            self.workbench._beat_frame_section.view_fullscreen_requested.connect(
                lambda: self.workbench._execute_operation(OperationType.VIEW_FULLSCREEN)
            )
            self.workbench._beat_frame_section.mirror_sequence_requested.connect(
                lambda: self.workbench._execute_operation(OperationType.MIRROR_SEQUENCE)
            )
            self.workbench._beat_frame_section.swap_colors_requested.connect(
                lambda: self.workbench._execute_operation(OperationType.SWAP_COLORS)
            )
            self.workbench._beat_frame_section.rotate_sequence_requested.connect(
                lambda: self.workbench._execute_operation(OperationType.ROTATE_SEQUENCE)
            )
            self.workbench._beat_frame_section.copy_json_requested.connect(
                lambda: self.workbench._execute_operation(OperationType.COPY_JSON)
            )
            self.workbench._beat_frame_section.delete_beat_requested.connect(
                self.workbench._handle_delete_beat
            )
            self.workbench._beat_frame_section.clear_sequence_requested.connect(
                self.workbench._handle_clear
            )
