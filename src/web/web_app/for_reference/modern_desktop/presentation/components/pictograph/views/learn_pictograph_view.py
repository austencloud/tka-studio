"""
Learn tab pictograph view - Direct view for learn tab contexts.

This provides auto-sizing to parent containers for learn tab questions
and answers without widget wrapper complexity.
"""

from __future__ import annotations

from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QSizePolicy

from .base_pictograph_view import BasePictographView


class LearnPictographView(BasePictographView):
    """
    Direct pictograph view for learn tab contexts.

    Features:
    - Auto-sizes to fill parent container
    - Maintains aspect ratio
    - Supports both question and answer contexts
    - Scales immediately on first display
    """

    def __init__(self, parent=None, context: str = "question"):
        # DEBUG: Log widget creation details
        import logging

        logger = logging.getLogger(__name__)
        logger.info("🎭 [LEARN_VIEW_DEBUG] Creating LearnPictographView")
        logger.info(f"   📱 Parent: {parent}")
        logger.info(f"   📱 Parent type: {type(parent) if parent else 'None'}")
        logger.info(f"   📱 Context: {context}")

        super().__init__(parent)

        # Store context for scaling adjustments
        self._context = context  # "question" or "answer"

        # CRITICAL FIX: Ensure widget flags are set correctly to prevent separate window
        from PyQt6.QtCore import Qt

        self.setWindowFlags(Qt.WindowType.Widget)

        # DEBUG: Log widget state after initialization
        logger.info(f"   📱 After init - Parent: {self.parent()}")
        logger.info(f"   📱 After init - Window flags: {self.windowFlags()}")
        logger.info(f"   📱 After init - Is window: {self.isWindow()}")

        # Set size policy to expand and fill available space
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Apply learn tab specific styling
        self._setup_learn_styling()

    def _setup_learn_styling(self):
        """Apply learn tab specific styling."""
        # Dark theme styling for learn tab display
        self.setStyleSheet(
            """
            LearnPictographView {
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 4px;
                background-color: rgba(255, 255, 255, 0.1);
            }
        """
        )

    def set_context(self, context: str):
        """Set the learn context (question or answer)."""
        self._context = context
        self._apply_view_specific_scaling()

    def _apply_view_specific_scaling(self):
        """Apply learn tab specific scaling to fill container."""
        # Get current widget size (this is our container)
        widget_size = self.size()

        if widget_size.width() <= 0 or widget_size.height() <= 0:
            return

        # Use the full container size for learn tab
        container_width = widget_size.width()
        container_height = widget_size.height()

        # Apply context-specific margin
        margin_factor = self._get_context_margin_factor()

        # Calculate effective size with margin
        effective_width = int(container_width * margin_factor)
        effective_height = int(container_height * margin_factor)

        # Use smaller dimension to maintain aspect ratio
        effective_size = min(effective_width, effective_height)

        # Apply legacy-style view scaling
        self._apply_legacy_view_scaling(effective_size)

    def _get_context_margin_factor(self) -> float:
        """Get margin factor based on context."""
        if self._context == "question":
            return 0.90  # Slightly smaller for questions
        if self._context == "answer":
            return 0.85  # Smaller for answer options
        return 0.90  # Default

    def _apply_legacy_view_scaling(self, target_size: int):
        """Apply legacy-style view scaling for learn tab."""
        if not self._scene:
            return

        # Get scene content bounds
        items_rect = self._scene.itemsBoundingRect()

        if items_rect.isEmpty():
            # Use scene rect as fallback
            items_rect = self._scene.sceneRect()

        if items_rect.isEmpty():
            return

        # Calculate scale to fit target size while maintaining aspect ratio
        scene_width = items_rect.width()
        scene_height = items_rect.height()

        if scene_width > 0 and scene_height > 0:
            # Calculate scale factors for both dimensions
            scale_x = target_size / scene_width
            scale_y = target_size / scene_height

            # Use minimum scale to ensure content fits
            scale_factor = min(scale_x, scale_y)

            # Apply the scaling
            self.resetTransform()
            self.scale(scale_factor, scale_factor)

            # Center the content
            self.centerOn(items_rect.center())

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize with learn tab specific logic."""
        super().resizeEvent(event)
        # Apply scaling immediately when container resizes
        self._apply_view_specific_scaling()

    def fit_to_container(
        self, container_width: int, container_height: int, maintain_square: bool = True
    ):
        """
        Fit the view to its container.

        Args:
            container_width: Available container width
            container_height: Available container height
            maintain_square: Whether to maintain square aspect ratio
        """
        if maintain_square:
            # Use smaller dimension to ensure square fits in container
            size = min(container_width, container_height)
            self.setFixedSize(size, size)
        else:
            self.setFixedSize(container_width, container_height)

    # === COMPATIBILITY METHODS ===

    def set_minimum_size(self, width: int, height: int):
        """Set minimum size for the view."""
        self.setMinimumSize(width, height)

    def set_maximum_size(self, width: int, height: int):
        """Set maximum size for the view."""
        self.setMaximumSize(width, height)
