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
from __future__ import annotations

from .layout_manager import GraphEditorLayoutManager
from .signal_coordinator import GraphEditorSignalCoordinator
from .state_manager import GraphEditorStateManager


__all__ = [
    "GraphEditorLayoutManager",
    "GraphEditorSignalCoordinator",
    "GraphEditorStateManager",
]
