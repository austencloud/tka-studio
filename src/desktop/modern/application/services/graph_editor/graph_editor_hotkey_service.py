"""
Pure Graph Editor Hotkey Service - Platform Agnostic

This service handles graph editor hotkey operations without any Qt dependencies.
Qt-specific signal coordination is handled by adapters in the presentation layer.
"""

import logging
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from desktop.modern.domain.models.beat_data import BeatData

if TYPE_CHECKING:
    from desktop.modern.presentation.components.graph_editor.graph_editor import (
        GraphEditor,
    )

logger = logging.getLogger(__name__)


class GraphEditorHotkeyService:
    """
    Pure service for managing graph editor hotkey operations.

    This service is platform-agnostic and does not depend on Qt.
    Signal coordination is handled by Qt adapters in the presentation layer.

    Responsibilities:
    - Processing hotkey actions for graph editor
    - Managing arrow movements and modifications
    - Coordinating hotkey-based graph editor operations
    """

    def __init__(
        self,
        graph_editor_getter: Callable[[], "GraphEditor"] | None = None,
    ):
        self.graph_editor_getter = graph_editor_getter

        # Platform-agnostic event callbacks
        self._arrow_moved_callbacks: list[Callable[[str, int, int], None]] = []
        self._hotkey_processed_callbacks: list[
            Callable[[str, dict[str, Any]], None]
        ] = []

    def add_arrow_moved_callback(self, callback: Callable[[str, int, int], None]):
        """Add callback for when an arrow is moved."""
        self._arrow_moved_callbacks.append(callback)

    def add_hotkey_processed_callback(
        self, callback: Callable[[str, dict[str, Any]], None]
    ):
        """Add callback for when a hotkey is processed."""
        self._hotkey_processed_callbacks.append(callback)

    def process_hotkey(
        self,
        hotkey: str,
        beat_data: BeatData | None = None,
        context: dict[str, Any] | None = None,
    ) -> bool:
        """
        Process a hotkey action.

        Args:
            hotkey: The hotkey string (e.g., "Ctrl+A", "Shift+Left")
            beat_data: Current beat data (if available)
            context: Additional context for the hotkey

        Returns:
            True if hotkey was processed, False otherwise
        """
        try:
            context = context or {}

            # Process common hotkeys
            if hotkey == "Ctrl+A":
                return self._select_all(context)
            elif hotkey == "Ctrl+C":
                return self._copy(beat_data, context)
            elif hotkey == "Ctrl+V":
                return self._paste(context)
            elif hotkey == "Delete":
                return self._delete_selected(context)
            elif hotkey.startswith("Shift+"):
                return self._process_shift_hotkey(hotkey, beat_data, context)
            elif hotkey.startswith("Ctrl+"):
                return self._process_ctrl_hotkey(hotkey, beat_data, context)
            elif hotkey in ["Left", "Right", "Up", "Down"]:
                return self._process_arrow_key(hotkey, beat_data, context)
            else:
                return self._process_custom_hotkey(hotkey, beat_data, context)

        except Exception as e:
            logger.error(f"Failed to process hotkey {hotkey}: {e}")
            return False

    def move_arrow(
        self,
        arrow_id: str,
        delta_x: int,
        delta_y: int,
        beat_data: BeatData | None = None,
    ) -> bool:
        """
        Move an arrow by the specified delta.

        Args:
            arrow_id: Identifier for the arrow
            delta_x: X-axis movement delta
            delta_y: Y-axis movement delta
            beat_data: Current beat data (if available)

        Returns:
            True if arrow was moved, False otherwise
        """
        try:
            # Update graph editor if available
            if self.graph_editor_getter:
                try:
                    graph_editor = self.graph_editor_getter()
                    if graph_editor and hasattr(graph_editor, "move_arrow"):
                        graph_editor.move_arrow(arrow_id, delta_x, delta_y)
                except Exception as e:
                    logger.warning(f"Could not update graph editor: {e}")

            # Notify callbacks instead of emitting Qt signals
            for callback in self._arrow_moved_callbacks:
                callback(arrow_id, delta_x, delta_y)

            logger.info(f"Arrow {arrow_id} moved by ({delta_x}, {delta_y})")
            return True

        except Exception as e:
            logger.error(f"Failed to move arrow {arrow_id}: {e}")
            return False

    def _select_all(self, context: dict[str, Any]) -> bool:
        """Select all elements in the graph editor."""
        try:
            if self.graph_editor_getter:
                graph_editor = self.graph_editor_getter()
                if graph_editor and hasattr(graph_editor, "select_all"):
                    graph_editor.select_all()

            self._notify_hotkey_processed("select_all", context)
            return True
        except Exception as e:
            logger.error(f"Failed to select all: {e}")
            return False

    def _copy(self, beat_data: BeatData | None, context: dict[str, Any]) -> bool:
        """Copy selected elements."""
        try:
            if self.graph_editor_getter:
                graph_editor = self.graph_editor_getter()
                if graph_editor and hasattr(graph_editor, "copy_selected"):
                    graph_editor.copy_selected()

            self._notify_hotkey_processed("copy", context)
            return True
        except Exception as e:
            logger.error(f"Failed to copy: {e}")
            return False

    def _paste(self, context: dict[str, Any]) -> bool:
        """Paste copied elements."""
        try:
            if self.graph_editor_getter:
                graph_editor = self.graph_editor_getter()
                if graph_editor and hasattr(graph_editor, "paste"):
                    graph_editor.paste()

            self._notify_hotkey_processed("paste", context)
            return True
        except Exception as e:
            logger.error(f"Failed to paste: {e}")
            return False

    def _delete_selected(self, context: dict[str, Any]) -> bool:
        """Delete selected elements."""
        try:
            if self.graph_editor_getter:
                graph_editor = self.graph_editor_getter()
                if graph_editor and hasattr(graph_editor, "delete_selected"):
                    graph_editor.delete_selected()

            self._notify_hotkey_processed("delete", context)
            return True
        except Exception as e:
            logger.error(f"Failed to delete selected: {e}")
            return False

    def _process_shift_hotkey(
        self, hotkey: str, beat_data: BeatData | None, context: dict[str, Any]
    ) -> bool:
        """Process shift-based hotkeys."""
        try:
            shift_key = hotkey.replace("Shift+", "")

            if shift_key in ["Left", "Right", "Up", "Down"]:
                # Handle shift+arrow for selection
                return self._extend_selection(shift_key, context)
            else:
                # Handle other shift combinations
                return self._process_custom_shift_hotkey(shift_key, beat_data, context)

        except Exception as e:
            logger.error(f"Failed to process shift hotkey {hotkey}: {e}")
            return False

    def _process_ctrl_hotkey(
        self, hotkey: str, beat_data: BeatData | None, context: dict[str, Any]
    ) -> bool:
        """Process ctrl-based hotkeys."""
        try:
            ctrl_key = hotkey.replace("Ctrl+", "")

            if ctrl_key == "Z":
                return self._undo(context)
            elif ctrl_key == "Y":
                return self._redo(context)
            else:
                return self._process_custom_ctrl_hotkey(ctrl_key, beat_data, context)

        except Exception as e:
            logger.error(f"Failed to process ctrl hotkey {hotkey}: {e}")
            return False

    def _process_arrow_key(
        self, hotkey: str, beat_data: BeatData | None, context: dict[str, Any]
    ) -> bool:
        """Process arrow key movements."""
        try:
            # Define movement deltas
            deltas = {
                "Left": (-1, 0),
                "Right": (1, 0),
                "Up": (0, -1),
                "Down": (0, 1),
            }

            delta_x, delta_y = deltas.get(hotkey, (0, 0))

            # Move selected arrow or cursor
            selected_arrow = context.get("selected_arrow")
            if selected_arrow:
                return self.move_arrow(selected_arrow, delta_x, delta_y, beat_data)
            else:
                # Move cursor or perform other navigation
                return self._move_cursor(delta_x, delta_y, context)

        except Exception as e:
            logger.error(f"Failed to process arrow key {hotkey}: {e}")
            return False

    def _process_custom_hotkey(
        self, hotkey: str, beat_data: BeatData | None, context: dict[str, Any]
    ) -> bool:
        """Process custom hotkeys."""
        try:
            # This is where you would handle application-specific hotkeys
            # For now, just log and return False
            logger.info(f"Custom hotkey not implemented: {hotkey}")
            return False
        except Exception as e:
            logger.error(f"Failed to process custom hotkey {hotkey}: {e}")
            return False

    def _extend_selection(self, direction: str, context: dict[str, Any]) -> bool:
        """Extend selection in the specified direction."""
        try:
            if self.graph_editor_getter:
                graph_editor = self.graph_editor_getter()
                if graph_editor and hasattr(graph_editor, "extend_selection"):
                    graph_editor.extend_selection(direction)

            self._notify_hotkey_processed(f"extend_selection_{direction}", context)
            return True
        except Exception as e:
            logger.error(f"Failed to extend selection: {e}")
            return False

    def _move_cursor(self, delta_x: int, delta_y: int, context: dict[str, Any]) -> bool:
        """Move cursor by the specified delta."""
        try:
            if self.graph_editor_getter:
                graph_editor = self.graph_editor_getter()
                if graph_editor and hasattr(graph_editor, "move_cursor"):
                    graph_editor.move_cursor(delta_x, delta_y)

            self._notify_hotkey_processed("move_cursor", context)
            return True
        except Exception as e:
            logger.error(f"Failed to move cursor: {e}")
            return False

    def _undo(self, context: dict[str, Any]) -> bool:
        """Undo last action."""
        try:
            if self.graph_editor_getter:
                graph_editor = self.graph_editor_getter()
                if graph_editor and hasattr(graph_editor, "undo"):
                    graph_editor.undo()

            self._notify_hotkey_processed("undo", context)
            return True
        except Exception as e:
            logger.error(f"Failed to undo: {e}")
            return False

    def _redo(self, context: dict[str, Any]) -> bool:
        """Redo last undone action."""
        try:
            if self.graph_editor_getter:
                graph_editor = self.graph_editor_getter()
                if graph_editor and hasattr(graph_editor, "redo"):
                    graph_editor.redo()

            self._notify_hotkey_processed("redo", context)
            return True
        except Exception as e:
            logger.error(f"Failed to redo: {e}")
            return False

    def _process_custom_shift_hotkey(
        self, key: str, beat_data: BeatData | None, context: dict[str, Any]
    ) -> bool:
        """Process custom shift hotkeys."""
        logger.info(f"Custom shift hotkey not implemented: Shift+{key}")
        return False

    def _process_custom_ctrl_hotkey(
        self, key: str, beat_data: BeatData | None, context: dict[str, Any]
    ) -> bool:
        """Process custom ctrl hotkeys."""
        logger.info(f"Custom ctrl hotkey not implemented: Ctrl+{key}")
        return False

    def _notify_hotkey_processed(self, action: str, context: dict[str, Any]):
        """Notify callbacks that a hotkey was processed."""
        for callback in self._hotkey_processed_callbacks:
            callback(action, context)
