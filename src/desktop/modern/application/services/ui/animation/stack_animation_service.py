"""
Stack animation service for QStackedWidget transitions.
Handles single and parallel stack fade operations.
"""

from __future__ import annotations

from PyQt6.QtWidgets import QStackedWidget

from desktop.modern.core.interfaces.animation_interfaces import (
    IAnimationService,
    IStackAnimationService,
    ParallelStackOperation,
    StackFadeOptions,
)
from desktop.modern.core.interfaces.core_services import ILayoutService


class StackAnimationService(IStackAnimationService):
    """Service for animating QStackedWidget transitions."""

    def __init__(
        self,
        animation_service: IAnimationService,
        layout_service: ILayoutService | None = None,
    ):
        self._animation_service = animation_service
        self._layout_service = layout_service

    async def fade_stack(
        self,
        stack: QStackedWidget,
        new_index: int,
        options: StackFadeOptions | None = None,
    ) -> None:
        """Fade transition between stack widgets."""
        if not stack:
            return

        current_widget = stack.currentWidget()
        next_widget = stack.widget(new_index)

        # Validate transition
        if not current_widget or not next_widget or stack.currentIndex() == new_index:
            return

        options = options or StackFadeOptions()

        # Phase 1: Fade out current widget
        await self._animation_service.fade_widget(current_widget, False, options)

        # Phase 2: Switch stack index
        stack.setCurrentIndex(new_index)

        # Phase 3: Apply layout changes if requested
        if options.resize_layout and options.layout_ratio and self._layout_service:
            self._layout_service.set_layout_ratio(options.layout_ratio)

        # Phase 4: Fade in next widget
        await self._animation_service.fade_widget(next_widget, True, options)

    async def fade_parallel_stacks(self, operation: ParallelStackOperation) -> None:
        """Fade transition for parallel stacks with layout changes."""
        # Validate operation
        if not self._validate_parallel_operation(operation):
            return

        # Get widgets for animation
        left_old = operation.left_stack.currentWidget()
        left_new = operation.left_stack.widget(operation.left_new_index)
        right_old = operation.right_stack.currentWidget()
        right_new = operation.right_stack.widget(operation.right_new_index)

        # Phase 1: Fade out both current widgets simultaneously
        await self._animation_service.fade_widgets(
            [left_old, right_old], fade_in=False, options=operation.options
        )

        # Phase 2: Switch both stacks and apply layout changes
        operation.left_stack.setCurrentIndex(operation.left_new_index)
        operation.right_stack.setCurrentIndex(operation.right_new_index)

        if self._layout_service:
            self._apply_parallel_layout_changes(operation)

        # Phase 3: Fade in both new widgets simultaneously
        await self._animation_service.fade_widgets(
            [left_new, right_new], fade_in=True, options=operation.options
        )

    def _validate_parallel_operation(self, operation: ParallelStackOperation) -> bool:
        """Validate that parallel operation has all required components."""
        return all(
            [
                operation.left_stack,
                operation.right_stack,
                operation.left_stack.widget(operation.left_new_index),
                operation.right_stack.widget(operation.right_new_index),
                operation.layout_ratio,
            ]
        )

    def _apply_parallel_layout_changes(self, operation: ParallelStackOperation) -> None:
        """Apply layout changes for parallel stack operation."""
        if not self._layout_service:
            return

        # Set the layout ratio
        self._layout_service.set_layout_ratio(operation.layout_ratio)

        # Reset any fixed dimensions that might interfere
        # This logic mirrors the legacy implementation
        left_stack = operation.left_stack
        right_stack = operation.right_stack

        # Qt's QWIDGETSIZE_MAX equivalent
        max_size = 16777215

        left_stack.setMaximumWidth(max_size)
        right_stack.setMaximumWidth(max_size)
        left_stack.setMinimumWidth(0)
        right_stack.setMinimumWidth(0)
