"""
Browse Components Module

Provides easy access to all filter selection components.
Use this as the main import point for the filter selection panel.

Example:
    from .components import FilterSelectionPanel
"""

from __future__ import annotations

from .components.categories_section import CategoriesSection
from .components.category_button import CategoryButton
from .components.category_group import CategoryGroup
from .components.filter_header import FilterHeader
from .components.filter_selection_panel import FilterSelectionPanel
from .components.prominent_button import ProminentButton
from .components.quick_access_section import QuickAccessSection
from .components.section_title import SectionTitle


__all__ = [
    "CategoriesSection",
    "CategoryButton",
    "CategoryGroup",
    "FilterHeader",
    "FilterSelectionPanel",
    "ProminentButton",
    "QuickAccessSection",
    "SectionTitle",
]
