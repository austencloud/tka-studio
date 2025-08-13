"""
Graph Editor State Manager - Qt Presentation Adapter

Thin adapter that delegates business logic to GraphEditorStateService
while handling Qt-specific concerns (signals, UI state).
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.application.services.graph_editor.graph_editor_state_manager import (
    GraphEditorStateManager as GraphEditorStateService,
)


if TYPE_CHECKING:
    from ..graph_editor import GraphEditor

logger = logging.getLogger(__name__)


class GraphEditorStateManager(QObject):
    """
    Qt presentation adapter for graph editor state management.

    Handles Qt signals and UI state while delegating all business logic
    to the GraphEditorStateService.
    """

    # Qt signals for state changes
    visibility_changed = pyqtSignal(bool)  # is_visible
    sequence_changed = pyqtSignal(object)  # SequenceData or None
    selected_beat_changed = pyqtSignal(object, int)  # BeatData or None, beat_index
    selected_arrow_changed = pyqtSignal(str)  # arrow_id

    def __init__(
        self,
        graph_editor: GraphEditor,
        state_service: GraphEditorStateService | None = None,
        parent: QObject | None = None,
    ):
        super().__init__(parent)
        self._graph_editor = graph_editor

        # Use injected service or create fallback for backward compatibility
        self._state_service = state_service or GraphEditorStateService()

        # Qt-specific state (presentation only)
        self._is_visible = False

        logger.info("Graph Editor State Manager initialized with service delegation")

    # Visibility management (pure Qt presentation concern)
