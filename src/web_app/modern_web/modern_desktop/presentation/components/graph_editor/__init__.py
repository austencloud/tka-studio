"""
Graph Editor Component Package

This package contains the refactored graph editor components following clean architecture patterns.

Main Components:
- GraphEditor: Main coordinator class (public API)
- GraphEditorAnimationController: Handles animations and height management
- GraphEditorSignalCoordinator: Manages signal connections and communication
- GraphEditorLayoutManager: Handles UI setup, styling, and positioning
- GraphEditorStateManager: Manages sequence, beat, arrow, and visibility state

Usage:
    from .graph_editor import GraphEditor

    # Create graph editor with service injection
    graph_editor = GraphEditor(
        graph_service=my_service,
        parent=my_parent,
        workbench_width=1200,
        workbench_height=800
    )
"""

# Main public API
from __future__ import annotations

from .components.adjustment_panel import AdjustmentPanel

# UI components (for compatibility)
from .components.pictograph_container import GraphEditorPictographContainer
from .graph_editor import GraphEditor
from .managers.layout_manager import GraphEditorLayoutManager

# Individual components (for advanced usage and testing)
from .managers.signal_coordinator import GraphEditorSignalCoordinator
from .managers.state_manager import GraphEditorStateManager


__all__ = [
    # Main public API
    "GraphEditor",
    # Component managers
    "GraphEditorSignalCoordinator",
    "GraphEditorLayoutManager",
    "GraphEditorStateManager",
    # UI components
    "GraphEditorPictographContainer",
    "AdjustmentPanel",
]
