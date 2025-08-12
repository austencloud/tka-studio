"""
Qt Adapter for Graph Editor Auto Transform Service

This adapter wraps the pure GraphEditorAutoTransformService to provide Qt-specific signal coordination.
"""

from __future__ import annotations

from collections.abc import Callable
import logging
from typing import TYPE_CHECKING, Any

from PyQt6.QtCore import QObject, pyqtSignal
from shared.application.services.graph_editor.graph_editor_auto_transform_service import (
    GraphEditorAutoTransformService,
)


if TYPE_CHECKING:
    from desktop.modern.presentation.components.graph_editor.graph_editor import (
        GraphEditor,
    )

logger = logging.getLogger(__name__)


class QtGraphEditorAutoTransformAdapter(QObject):
    """
    Qt adapter for GraphEditorAutoTransformService.

    This adapter provides Qt signal coordination for the pure service.
    """

    # Qt signals for transform events
    transform_started = pyqtSignal(str, dict)  # transform_id, context
    transform_completed = pyqtSignal(str, dict)  # transform_id, context
    transform_progress = pyqtSignal(str, float, dict)  # transform_id, progress, context
    settings_changed = pyqtSignal(dict)  # settings

    # Qt signals for specific transform operations
    auto_align_requested = pyqtSignal(list, str)  # element_ids, alignment_type
    auto_distribute_requested = pyqtSignal(list, str)  # element_ids, distribution_type
    auto_resize_requested = pyqtSignal(list, dict)  # element_ids, target_size
    snap_to_grid_requested = pyqtSignal(list, int)  # element_ids, grid_size
    auto_layout_requested = pyqtSignal(str, list)  # layout_type, element_ids

    def __init__(
        self,
        graph_editor_getter: Callable[[], GraphEditor] | None = None,
    ):
        super().__init__()

        # Create the pure service
        self.service = GraphEditorAutoTransformService(graph_editor_getter)

        # Connect service callbacks to Qt signals
        self.service.add_transform_started_callback(self._on_transform_started)
        self.service.add_transform_completed_callback(self._on_transform_completed)
        self.service.add_transform_progress_callback(self._on_transform_progress)
        self.service.add_settings_changed_callback(self._on_settings_changed)

    def set_auto_transform_enabled(self, enabled: bool):
        """Enable or disable auto-transform."""
        self.service.set_auto_transform_enabled(enabled)

    def is_auto_transform_enabled(self) -> bool:
        """Check if auto-transform is enabled."""
        return self.service.is_auto_transform_enabled()

    def update_transform_settings(self, settings: dict[str, Any]):
        """Update transform settings."""
        self.service.update_transform_settings(settings)

    def get_transform_settings(self) -> dict[str, Any]:
        """Get current transform settings."""
        return self.service.get_transform_settings()

    def auto_align_elements(
        self,
        element_ids: list[str],
        alignment_type: str = "center",
        context: dict[str, Any] | None = None,
    ) -> bool:
        """
        Automatically align elements.

        Args:
            element_ids: List of element IDs to align
            alignment_type: Type of alignment ("left", "center", "right", "top", "middle", "bottom")
            context: Additional context for the operation

        Returns:
            True if alignment was successful, False otherwise
        """
        # Emit Qt signal for UI coordination
        self.auto_align_requested.emit(element_ids, alignment_type)

        # Delegate to service
        return self.service.auto_align_elements(element_ids, alignment_type, context)

    def auto_distribute_elements(
        self,
        element_ids: list[str],
        distribution_type: str = "horizontal",
        context: dict[str, Any] | None = None,
    ) -> bool:
        """
        Automatically distribute elements.

        Args:
            element_ids: List of element IDs to distribute
            distribution_type: Type of distribution ("horizontal", "vertical")
            context: Additional context for the operation

        Returns:
            True if distribution was successful, False otherwise
        """
        # Emit Qt signal for UI coordination
        self.auto_distribute_requested.emit(element_ids, distribution_type)

        # Delegate to service
        return self.service.auto_distribute_elements(
            element_ids, distribution_type, context
        )

    def auto_resize_elements(
        self,
        element_ids: list[str],
        target_size: dict[str, float] | None = None,
        context: dict[str, Any] | None = None,
    ) -> bool:
        """
        Automatically resize elements.

        Args:
            element_ids: List of element IDs to resize
            target_size: Target size dict with 'width' and 'height' keys
            context: Additional context for the operation

        Returns:
            True if resizing was successful, False otherwise
        """
        # Emit Qt signal for UI coordination
        self.auto_resize_requested.emit(element_ids, target_size or {})

        # Delegate to service
        return self.service.auto_resize_elements(element_ids, target_size, context)

    def snap_to_grid(
        self,
        element_ids: list[str],
        grid_size: int | None = None,
        context: dict[str, Any] | None = None,
    ) -> bool:
        """
        Snap elements to grid.

        Args:
            element_ids: List of element IDs to snap
            grid_size: Grid size (uses default if None)
            context: Additional context for the operation

        Returns:
            True if snapping was successful, False otherwise
        """
        grid_size = grid_size or self.service.get_transform_settings().get(
            "grid_size", 20
        )

        # Emit Qt signal for UI coordination
        self.snap_to_grid_requested.emit(element_ids, grid_size)

        # Delegate to service
        return self.service.snap_to_grid(element_ids, grid_size, context)

    def auto_layout(
        self,
        layout_type: str = "flow",
        element_ids: list[str] | None = None,
        context: dict[str, Any] | None = None,
    ) -> bool:
        """
        Apply automatic layout to elements.

        Args:
            layout_type: Type of layout ("flow", "grid", "circular", "tree")
            element_ids: List of element IDs (uses all if None)
            context: Additional context for the operation

        Returns:
            True if layout was successful, False otherwise
        """
        # Emit Qt signal for UI coordination
        self.auto_layout_requested.emit(layout_type, element_ids or [])

        # Delegate to service
        return self.service.auto_layout(layout_type, element_ids, context)

    def animate_transform(
        self,
        transform_id: str,
        duration: int | None = None,
        context: dict[str, Any] | None = None,
    ) -> bool:
        """
        Animate a transform operation.

        Args:
            transform_id: ID of the transform to animate
            duration: Animation duration in milliseconds
            context: Additional context for the operation

        Returns:
            True if animation was started, False otherwise
        """
        return self.service.animate_transform(transform_id, duration, context)

    def _on_transform_started(self, transform_id: str, context: dict[str, Any]):
        """Handle transform started callback from service."""
        self.transform_started.emit(transform_id, context)

    def _on_transform_completed(self, transform_id: str, context: dict[str, Any]):
        """Handle transform completed callback from service."""
        self.transform_completed.emit(transform_id, context)

    def _on_transform_progress(
        self, transform_id: str, progress: float, context: dict[str, Any]
    ):
        """Handle transform progress callback from service."""
        self.transform_progress.emit(transform_id, progress, context)

    def _on_settings_changed(self, settings: dict[str, Any]):
        """Handle settings changed callback from service."""
        self.settings_changed.emit(settings)

    # Pass-through methods for direct service access
    def add_transform_started_callback(
        self, callback: Callable[[str, dict[str, Any]], None]
    ):
        """Add callback for when a transform starts."""
        self.service.add_transform_started_callback(callback)

    def add_transform_completed_callback(
        self, callback: Callable[[str, dict[str, Any]], None]
    ):
        """Add callback for when a transform completes."""
        self.service.add_transform_completed_callback(callback)

    def add_transform_progress_callback(
        self, callback: Callable[[str, float, dict[str, Any]], None]
    ):
        """Add callback for transform progress updates."""
        self.service.add_transform_progress_callback(callback)

    def add_settings_changed_callback(self, callback: Callable[[dict[str, Any]], None]):
        """Add callback for when settings change."""
        self.service.add_settings_changed_callback(callback)
