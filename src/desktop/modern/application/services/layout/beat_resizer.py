"""
Enhanced Beat Resizer Service

Implements sophisticated beat sizing logic with precise
dimension calculations and intelligent responsive behavior.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QScrollArea, QWidget

from desktop.modern.core.interfaces.core_services import IBeatResizer


if TYPE_CHECKING:
    from desktop.modern.presentation.components.graph_editor.graph_editor import (
        GraphEditor,
    )
    from desktop.modern.presentation.components.sequence_workbench.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
    )


def ensure_positive_size(size: int, min_value: int = 1) -> int:
    """Ensure a size value is positive to avoid Qt warnings"""
    return max(size, min_value)


class BeatResizer(IBeatResizer):
    """
    Enhanced beat frame resizer with validated sizing algorithms.

    Provides intelligent beat sizing that considers:
    - Available container space    - Number of columns in current layout
    - Fixed height ratio for optimal display
    - Dynamic scroll bar management
    """

    def __init__(self):
        self._last_calculated_size = None
        self._size_cache = {}

        # Graph editor reference for accurate height calculations
        self._graph_editor_ref: GraphEditor | None = None

    def set_graph_editor_reference(self, graph_editor: GraphEditor):
        """Set reference to graph editor for accurate height calculations"""
        self._graph_editor_ref = graph_editor

    def resize_beat_frame(
        self, beat_frame: SequenceBeatFrame, num_rows: int, num_columns: int
    ) -> int:
        """
        Complete beat frame resize using validated algorithm.

        Args:
            beat_frame: The beat frame widget
            num_rows: Number of rows in current layout
            num_columns: Number of columns in current layout

        Returns:
            Calculated beat size in pixels
        """
        width, height = self.calculate_dimensions(beat_frame)
        beat_size = self.calculate_beat_size(width, height, num_columns)
        self.resize_beats(beat_frame, beat_size)
        self.configure_scroll_behavior(beat_frame, num_rows)
        return beat_size

    def calculate_dimensions(self, beat_frame: SequenceBeatFrame) -> tuple[int, int]:
        """
        Calculate available container dimensions using validated logic.

        Algorithm:
        - Takes half the main widget width
        - Subtracts button panel and scrollbar widths
        - Applies 0.8 factor for padding
        - Subtracts graph editor height from available height
        """
        # Find the main widget and related components
        main_window = self._find_main_window(beat_frame)
        # Validated calculation
        scrollbar_width = beat_frame.verticalScrollBar().width() if beat_frame else 0

        # Main widget width divided by 2 (workbench takes half the screen)
        half_main_width = main_window.width() // 2

        # Find button panel width (or estimate if not found)
        button_panel_width = self._get_button_panel_width(main_window)

        # Calculate available width with validated formula
        available_width = half_main_width - button_panel_width - scrollbar_width
        width = int(available_width * 0.8)

        # Calculate available height (subtract graph editor space)
        graph_editor_height = self._get_graph_editor_height(main_window)
        available_height = main_window.height() - int(graph_editor_height * 0.8)

        return width, available_height

    def calculate_beat_size(self, width: int, height: int, num_columns: int) -> int:
        """
        Calculate optimal beat size using validated algorithm.

        Algorithm:
        - Width constraint: available_width // num_columns
        - Height constraint: available_height // 6 (fixed ratio!)
        - Final size: min(width_constraint, height_constraint)
        - Special case: When num_columns == 1 (cleared sequence), use width // 6 instead
          to maintain consistent sizing with when options are present
        """
        # Caching for performance
        cache_key = (width, height, num_columns)
        if cache_key in self._size_cache:
            return self._size_cache[cache_key]

        if num_columns == 0:
            beat_size = 0
        elif num_columns == 1:
            width_constraint = int(width // 6)
            height_constraint = int(height // 6)  # Fixed ratio of 6!
            beat_size = min(width_constraint, height_constraint)
        else:
            width_constraint = int(width // num_columns)
            height_constraint = int(height // 6)  # Fixed ratio of 6!
            beat_size = min(width_constraint, height_constraint)

        # Ensure positive size (safety check)
        beat_size = ensure_positive_size(beat_size)

        self._size_cache[cache_key] = beat_size
        return beat_size

    def resize_beats(self, beat_frame: SequenceBeatFrame, beat_size: int):
        """
        Resize beat views using validated logic.

        Algorithm:
        - Sets fixed size to calculated beat_size
        - Sets minimum size to beat_size - 48 for inner content
        - Applies same sizing to start position view
        """
        # Safety check
        safe_size = ensure_positive_size(beat_size)
        min_size = ensure_positive_size(safe_size - 48)

        # Resize all beat views
        beat_views = getattr(beat_frame, "_beat_views", [])
        for beat_view in beat_views:
            beat_view.setFixedSize(safe_size, safe_size)
            if hasattr(beat_view, "setMinimumSize"):
                beat_view.setMinimumSize(min_size, min_size)

        # Also resize start position view (consistent behavior)
        start_position_view = getattr(beat_frame, "_start_position_view", None)
        if start_position_view:
            start_position_view.setFixedSize(safe_size, safe_size)
            if hasattr(start_position_view, "setMinimumSize"):
                start_position_view.setMinimumSize(min_size, min_size)

    def configure_scroll_behavior(self, beat_frame: SequenceBeatFrame, num_rows: int):
        """
        Configure scroll bar behavior using validated logic.

        Algorithm:
        - Show scrollbar if rows > 4
        - Hide scrollbar if rows <= 4
        """
        # The beat frame itself might be a scroll area (SequenceBeatFrame inherits from QScrollArea)
        scroll_area = self._find_scroll_area_parent(beat_frame)
        if not scroll_area and isinstance(beat_frame, QScrollArea):
            scroll_area = beat_frame

        if scroll_area:
            if num_rows > 4:
                scroll_area.setVerticalScrollBarPolicy(
                    Qt.ScrollBarPolicy.ScrollBarAlwaysOn
                )
            else:
                scroll_area.setVerticalScrollBarPolicy(
                    Qt.ScrollBarPolicy.ScrollBarAlwaysOff
                )

    def _find_main_window(self, widget: QWidget) -> QWidget | None:
        """Find the main widget by traversing up to the top-level window"""
        # Get the top-level widget (main window)
        top_level = widget.window()

        # Ensure it's actually a top-level window
        if top_level and top_level.isWindow():
            return top_level

        return None

    def _find_scroll_area_parent(self, widget: QWidget) -> QScrollArea | None:
        """Find QScrollArea parent widget"""
        parent = widget.parent()
        while parent:
            if isinstance(parent, QScrollArea):
                return parent
            parent = parent.parent()
        return None

    def _get_button_panel_width(self, main_widget: QWidget) -> int:
        """Get button panel width or reasonable estimate"""
        # Try to find button panel, otherwise use reasonable default
        button_panel = self._find_child_by_name(main_widget, "button_panel")
        if button_panel and hasattr(button_panel, "width"):
            return button_panel.width()
        return 200  # Reasonable default

    def _get_graph_editor_height(self, main_widget: QWidget) -> int:
        """Get actual graph editor height, not a guess"""
        # Use direct reference if available and visible
        if self._graph_editor_ref and self._graph_editor_ref.is_visible():
            return self._graph_editor_ref.height()

        # Fallback: try to find graph editor by name
        graph_editor = self._find_child_by_name(main_widget, "graph_editor")
        if (
            graph_editor
            and hasattr(graph_editor, "height")
            and hasattr(graph_editor, "is_visible")
        ) and graph_editor.is_visible():
            return graph_editor.height()

        # If not visible, don't subtract any height
        return 0

    def _find_child_by_name(self, widget: QWidget, name: str) -> QWidget | None:
        """Find child widget by object name"""
        for child in widget.findChildren(QWidget):
            if child.objectName() == name:
                return child
        return None

    def clear_cache(self):
        """Clear size calculation cache"""
        self._size_cache.clear()
        self._last_calculated_size = None

    # Interface implementation methods
    def resize_beat(self, beat_data: Any, new_size: tuple[int, int]) -> Any:
        """Resize beat to new dimensions (interface implementation)."""
        # For Qt-based implementation, this would resize the actual widget
        # For web implementation, this would update CSS dimensions
        width, height = new_size

        # Ensure positive sizes
        width = ensure_positive_size(width)
        height = ensure_positive_size(height)

        # Return updated beat data with new size
        if hasattr(beat_data, "update"):
            return beat_data.update(width=width, height=height)
        # For dict-like beat data
        updated_data = dict(beat_data) if hasattr(beat_data, "items") else {}
        updated_data.update({"width": width, "height": height})
        return updated_data

    def calculate_optimal_size(
        self,
        beat_data: Any,
        container_size: tuple[int, int],
    ) -> tuple[int, int]:
        """Calculate optimal size for beat within container (interface implementation)."""
        # Note: beat_data parameter is part of interface but not used in this implementation
        container_width, container_height = container_size

        # Use existing calculation logic - fallback to simple calculation
        calculated_size = min(container_width, container_height) // 6

        # Ensure it fits within container
        optimal_width = min(calculated_size, container_width)
        optimal_height = min(calculated_size, container_height)

        return (
            ensure_positive_size(optimal_width),
            ensure_positive_size(optimal_height),
        )

    def validate_size_constraints(self, size: tuple[int, int]) -> bool:
        """Validate size constraints (interface implementation)."""
        width, height = size

        # Basic validation
        if width <= 0 or height <= 0:
            return False

        # Check reasonable bounds (not too large or too small)
        min_size = 50
        max_size = 2000

        if width < min_size or height < min_size:
            return False
        return not (width > max_size or height > max_size)
