"""
Modern Browse Tab Package

Simplified browse tab implementation based on Legacy audit findings.
Focuses on real complexity: responsive UI, thumbnail management, and state persistence.
"""

from __future__ import annotations

from desktop.modern.presentation.views.browse.browse_tab import BrowseTab
from desktop.modern.presentation.views.browse.models import (
    BrowseTabSection,
    FilterType,
    NavigationMode,
    SortMethod,
)


__all__ = [
    "BrowseTab",
    "BrowseTabSection",
    "FilterType",
    "NavigationMode",
    "SortMethod",
]
