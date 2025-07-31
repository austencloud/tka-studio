"""
Browse Tab Managers Package

This package contains the manager classes that handle different aspects
of the Browse tab functionality:

- BrowseDataManager: Handles data conversion and sequence operations
- BrowseActionHandler: Processes user actions (edit, save, delete, fullscreen)
- BrowseNavigationManager: Manages navigation between panels

Note: BrowseTabController moved to controllers package.
"""

from .browse_action_handler import BrowseActionHandler
from .browse_data_manager import BrowseDataManager
from .browse_navigation_manager import BrowseNavigationManager, BrowsePanel

__all__ = [
    "BrowseDataManager",
    "BrowseActionHandler",
    "BrowseNavigationManager",
    "BrowsePanel",
]
