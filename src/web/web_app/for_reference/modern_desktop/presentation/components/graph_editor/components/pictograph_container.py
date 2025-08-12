from __future__ import annotations

import logging
from typing import Optional

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from shared.application.services.pictograph.pictograph_csv_manager import (
    PictographCSVManager,
)

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.presentation.components.pictograph.views import (
    create_pictograph_view,
)

from ..config import ColorConfig, LayoutConfig, SizeConfig, StateConfig, UIConfig


logger = logging.getLogger(__name__)


class GraphEditorPictographContainer(QWidget):
    arrow_selected = pyqtSignal(str)
    beat_modified = pyqtSignal(BeatData)

    def __init__(self, parent):
        super().__init__(parent)
        self._graph_editor = parent
        self._current_beat: Optional[BeatData] = None
        self._selected_arrow_id: Optional[str] = None
        self._selected_arrow_items = {}  # Track selected arrow visual items
        self._selection_highlight_color = ColorConfig.SELECTION_HIGHLIGHT_COLOR

        # Get layout service from parent's container
        container = getattr(parent, "container", None)
        if container:
            self._pictograph_service = PictographCSVManager()
        else:
            self._pictograph_service = None

        self._current_pictograph: Optional[PictographData] = None

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        # Match legacy: no margins and no spacing like legacy container
        layout.setContentsMargins(
            LayoutConfig.CONTAINER_MARGINS,
            LayoutConfig.CONTAINER_MARGINS,
            LayoutConfig.CONTAINER_MARGINS,
            LayoutConfig.CONTAINER_MARGINS,
        )
        layout.setSpacing(LayoutConfig.CONTAINER_SPACING)

        self._pictograph_widget = create_pictograph_view("base", parent=self)
        # Connect arrow selection signal from the scene
        if hasattr(self._pictograph_widget.scene, "arrow_selected"):
            self._pictograph_widget.scene.arrow_selected.connect(self._on_arrow_clicked)

        layout.addWidget(self._pictograph_widget)

        # Set reasonable initial size - will be updated in resizeEvent to maintain square aspect ratio
        self.setFixedSize(
            UIConfig.INITIAL_PICTOGRAPH_SIZE, UIConfig.INITIAL_PICTOGRAPH_SIZE
        )

        # Set size policy to Fixed to match legacy behavior
        from PyQt6.QtWidgets import QSizePolicy

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Web-inspired styling with gold border like web version
        self.setStyleSheet(
            f"""
            GraphEditorPictographContainer {{
                border: {LayoutConfig.PICTOGRAPH_BORDER_WIDTH}px solid {ColorConfig.SELECTION_HIGHLIGHT_COLOR};
                border-radius: {LayoutConfig.PANEL_BORDER_RADIUS}px;
                background-color: {ColorConfig.PICTOGRAPH_BACKGROUND};
            }}
        """
        )

    def set_beat(self, beat_data: Optional[BeatData]):
        self._current_beat = beat_data
        if beat_data and beat_data.pictograph_data:
            self._pictograph_widget.update_from_pictograph_data(
                beat_data.pictograph_data
            )
        else:
            self._pictograph_widget.clear_pictograph()

    def refresh_display(self, beat_data: BeatData):
        """Refresh pictograph display with new beat data"""
        self.set_beat(beat_data)

        # Maintain selection if we had one
        if self._selected_arrow_id:
            self._apply_arrow_selection_visual(self._selected_arrow_id)

    def set_selected_arrow(self, arrow_id: str):
        """Set selected arrow and update visual feedback"""
        # Clear previous selection
        self._clear_arrow_selection()

        # Set new selection
        self._selected_arrow_id = arrow_id
        self._apply_arrow_selection_visual(arrow_id)

        self.arrow_selected.emit(arrow_id)

    def _clear_arrow_selection(self):
        """Clear all arrow selection visual feedback"""
        if hasattr(self._pictograph_widget, "scene") and self._pictograph_widget.scene:
            for item in self._pictograph_widget.scene.items():
                if hasattr(item, "setSelected"):
                    item.setSelected(False)
                if hasattr(item, "clear_selection_highlight"):
                    item.clear_selection_highlight()

    def _apply_arrow_selection_visual(self, arrow_id: str):
        """Apply visual feedback for selected arrow"""
        if (
            not hasattr(self._pictograph_widget, "scene")
            or not self._pictograph_widget.scene
        ):
            return

        for item in self._pictograph_widget.scene.items():
            if hasattr(item, "arrow_color") and item.arrow_color == arrow_id:
                # Add gold border highlighting
                if hasattr(item, "add_selection_highlight"):
                    item.add_selection_highlight(self._selection_highlight_color)
                elif hasattr(item, "setSelected"):
                    item.setSelected(True)
                break

    def _on_arrow_clicked(self, arrow_id: str):
        self._selected_arrow_id = arrow_id
        self.arrow_selected.emit(arrow_id)

    def resizeEvent(self, event):
        """Handle resize events with responsive sizing based on graph editor height"""
        super().resizeEvent(event)

        # CRITICAL FIX: Prevent resize loops during animation and initialization
        if self._graph_editor and hasattr(self._graph_editor, "_animation_controller"):
            if self._graph_editor._animation_controller.is_animating():
                logger.debug("Blocking pictograph resize during animation")
                return

        # CRITICAL FIX: Don't resize pictograph when graph editor is collapsed or very small
        # This prevents pictograph from shrinking when graph editor collapses
        if self._graph_editor and hasattr(self._graph_editor, "height"):
            graph_editor_height = self._graph_editor.height()

            # Check if graph editor is collapsed or in transition
            if graph_editor_height < StateConfig.MINIMUM_GRAPH_HEIGHT:
                logger.debug(
                    "Skipping pictograph resize - graph editor too small: %dpx",
                    graph_editor_height,
                )
                return

            if graph_editor_height > 0:
                # Calculate content size as percentage of graph editor height
                content_size = int(
                    graph_editor_height * LayoutConfig.PICTOGRAPH_SIZE_RATIO
                )

                # Ensure minimum size for usability
                content_size = max(content_size, LayoutConfig.PICTOGRAPH_MIN_SIZE)

                # CRITICAL FIX: Only resize if there's a significant change to prevent flashing
                current_size = self.width()
                if abs(current_size - content_size) < StateConfig.RESIZE_TOLERANCE:
                    return  # Skip micro-adjustments that cause flashing

                # Apply responsive sizing
                self.setFixedSize(content_size, content_size)

                # The pictograph widget should fill most of the content area
                if self._pictograph_widget:
                    view_size = int(content_size * LayoutConfig.PICTOGRAPH_VIEW_RATIO)
                    self._pictograph_widget.setFixedSize(view_size, view_size)

                logger.debug(
                    "Pictograph responsive resize: graph_editor=%dpx, content=%dpx",
                    graph_editor_height,
                    content_size,
                )

    def handle_width_change(self, new_width: int) -> None:
        """Handle graph editor width changes and recalculate pictograph size"""
        if new_width <= 0:
            return

        # Prevent resize loops during animation
        if self._graph_editor and hasattr(self._graph_editor, "_animation_controller"):
            if self._graph_editor._animation_controller.is_animating():
                logger.debug("Blocking pictograph width update during animation")
                return

        # Use both width and height for better sizing calculation
        graph_editor_height = self._graph_editor.height() if self._graph_editor else 0

        # CRITICAL FIX: Don't resize pictograph when graph editor is collapsed or very small
        if graph_editor_height < StateConfig.MINIMUM_GRAPH_HEIGHT:
            logger.debug(
                "Skipping pictograph width update - graph editor too small: %dpx",
                graph_editor_height,
            )
            return

        if graph_editor_height > 0:
            # Calculate size based on both dimensions for better proportions
            # Use the smaller dimension to ensure square pictograph fits properly
            available_width = int(new_width * SizeConfig.PICTOGRAPH_WIDTH_RATIO)
            available_height = int(
                graph_editor_height * SizeConfig.PICTOGRAPH_HEIGHT_RATIO
            )

            # Choose the smaller dimension to ensure it fits in both directions
            content_size = min(available_width, available_height)

            # Ensure minimum size for usability
            content_size = max(content_size, LayoutConfig.PICTOGRAPH_MIN_SIZE)

            # Only resize if there's a significant change to prevent flashing
            current_size = self.width()
            if abs(current_size - content_size) < StateConfig.RESIZE_TOLERANCE:
                return  # Skip micro-adjustments that cause flashing

            # Apply responsive sizing
            self.setFixedSize(content_size, content_size)

            # The pictograph widget should fill most of the content area
            if self._pictograph_widget:
                view_size = int(content_size * LayoutConfig.PICTOGRAPH_VIEW_RATIO)
                self._pictograph_widget.setFixedSize(view_size, view_size)

            logger.debug(
                "Pictograph resized: width=%dpx, height=%dpx, content=%dpx",
                new_width,
                graph_editor_height,
                content_size,
            )
