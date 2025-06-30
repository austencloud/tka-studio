"""
Graph Editor Managers Package
============================

Essential coordination components for the graph editor.

This package contains only the core managers needed for:
- Layout management and calculations
- State management and synchronization
- Signal coordination between components
"""

# Essential manager imports only
from .layout_manager import GraphEditorLayoutManager
from .state_manager import GraphEditorStateManager
from .signal_coordinator import GraphEditorSignalCoordinator

__all__ = [
    "GraphEditorLayoutManager",
    "GraphEditorStateManager",
    "GraphEditorSignalCoordinator",
]
