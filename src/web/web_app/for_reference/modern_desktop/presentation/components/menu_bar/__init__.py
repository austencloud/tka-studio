"""
Menu Bar Components

Modern menu bar system for TKA desktop app with navigation and utility features.
"""

from __future__ import annotations

from .menu_bar_widget import MenuBarWidget
from .navigation.menu_bar_navigation_widget import MenuBarNavigationWidget


__all__ = [
    "MenuBarNavigationWidget",
    "MenuBarWidget",
]
