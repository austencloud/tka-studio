"""
Core type definitions for the design system.
"""

from __future__ import annotations

from enum import Enum


class ComponentType(Enum):
    """Enumeration of all styleable component types in the application."""

    # Layout Components
    MENU_BAR = "menu_bar"
    TAB_CONTAINER = "tab_container"
    PANEL = "panel"
    DIALOG = "dialog"
    CONTAINER = "container"

    # Interactive Components
    BUTTON = "button"
    TAB_BUTTON = "tab_button"
    INPUT = "input"
    CHECKBOX = "checkbox"
    SLIDER = "slider"

    # Content Components
    LABEL = "label"
    CARD = "card"
    LIST_ITEM = "list_item"

    # Specialized Components
    OVERLAY = "overlay"
    TOOLTIP = "tooltip"
    SEQUENCE_VIEWER = "sequence_viewer"


class StyleVariant(Enum):
    """Standard style variants available across components."""

    DEFAULT = "default"
    ACCENT = "accent"
    SUBTLE = "subtle"
    PROMINENT = "prominent"
    MUTED = "muted"
    WARNING = "warning"
    SUCCESS = "success"
    ERROR = "error"
