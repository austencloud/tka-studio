"""
Direct pictograph views - Legacy-style approach without widget wrappers.

This module provides direct QGraphicsView-based pictograph views that
eliminate the widget wrapper complexity and provide immediate, consistent
scaling like the legacy system.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Optional

from PyQt6.QtCore import QSize

from .base_pictograph_view import BasePictographView
from .beat_pictograph_view import BeatPictographView
from .learn_pictograph_view import LearnPictographView
from .option_pictograph_view import OptionPictographView
from .start_position_view import StartPositionView


def create_pictograph_view(context: str, parent=None, **kwargs) -> BasePictographView:
    """
    Factory function to create the appropriate pictograph view for each context.

    This replaces the complex widget wrapper approach with simple, direct
    view classes that handle their own scaling like the legacy system.

    Args:
        context: The context for the view ("option", "start_position", "learn", "base")
        parent: Parent widget
        **kwargs: Context-specific parameters

    Returns:
        Appropriate pictograph view instance

    Context-specific kwargs:
        option:
            - main_window_size_provider: Callable[[], QSize] for size calculations

        start_position:
            - is_advanced: bool for advanced mode

        learn:
            - context: str ("question" or "answer")
    """

    if context == "option":
        main_window_size_provider = kwargs.get("main_window_size_provider")
        return OptionPictographView(
            parent=parent, main_window_size_provider=main_window_size_provider
        )

    if context == "start_position":
        is_advanced = kwargs.get("is_advanced", False)
        return StartPositionView(parent=parent, is_advanced=is_advanced)

    if context == "learn":
        learn_context = kwargs.get("learn_context", "question")
        return LearnPictographView(parent=parent, context=learn_context)

    if context == "beat":
        return BeatPictographView(parent=parent)

    # Base view for other contexts
    return BasePictographView(parent=parent)


def create_option_view(
    parent=None,
    main_window_size_provider: Callable[[], QSize] | None = None,
    letter_type=None,
) -> OptionPictographView:
    """Create an option picker pictograph view."""
    view = OptionPictographView(
        parent=parent, main_window_size_provider=main_window_size_provider
    )
    if letter_type:
        view.set_letter_type(letter_type)
    return view


def create_start_position_view(
    parent=None, is_advanced: bool = False
) -> StartPositionView:
    """Create a start position picker pictograph view."""
    return StartPositionView(parent=parent, is_advanced=is_advanced)


def create_learn_view(parent=None, context: str = "question") -> LearnPictographView:
    """Create a learn tab pictograph view."""
    return LearnPictographView(parent=parent, context=context)


def create_beat_view(parent=None) -> BeatPictographView:
    """Create a beat frame pictograph view."""
    return BeatPictographView(parent=parent)


# Export all view classes
__all__ = [
    "BasePictographView",
    "LearnPictographView",
    "OptionPictographView",
    "StartPositionView",
    "create_learn_view",
    "create_option_view",
    "create_pictograph_view",
    "create_start_position_view",
]
