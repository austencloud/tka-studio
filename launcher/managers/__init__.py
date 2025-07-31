"""
TKA Launcher Managers
====================

Helper managers for dock, window, and component management.
"""

# Dock managers
from .dock_application_manager import DockApplicationManager
from .dock_components import DockApplicationIcon
from .dock_context_menu import DockContextMenuManager
from .dock_position_manager import DockPositionManager
from .dock_window_setup import DockWindowSetup

# Window managers
from .window_geometry_manager import WindowGeometryManager
from .window_mode_manager import WindowModeManager

__all__ = [
    "DockApplicationManager",
    "DockApplicationIcon",
    "DockContextMenuManager",
    "DockPositionManager",
    "DockWindowSetup",
    "WindowGeometryManager",
    "WindowModeManager",
]
