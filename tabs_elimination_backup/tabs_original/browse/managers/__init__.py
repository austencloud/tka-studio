"""
Browse Tab Managers Package

This package contains the manager classes that handle different aspects
of the Browse tab functionality:

- BrowseTabController: Main coordinator for all browse tab operations
- BrowseDataManager: Handles data conversion and sequence operations
- BrowseActionHandler: Processes user actions (edit, save, delete, fullscreen)
- BrowseNavigationManager: Manages navigation between panels
"""

from .browse_action_handler import BrowseActionHandler
from .browse_data_manager import BrowseDataManager
from .browse_navigation_manager import BrowseNavigationManager, BrowsePanel
from .browse_tab_controller import BrowseTabController

__all__ = [
    "BrowseTabController",
    "BrowseDataManager",
    "BrowseActionHandler",
    "BrowseNavigationManager",
    "BrowsePanel",
]
