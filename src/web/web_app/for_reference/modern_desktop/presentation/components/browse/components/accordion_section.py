"""
Accordion Section Component

Individual collapsible section with header and content.
"""

from __future__ import annotations

from PyQt6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    pyqtSignal,
)
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QWidget

from desktop.modern.domain.models.browse_models import FilterType
from desktop.modern.presentation.styles.mixins import StyleMixin

from .accordion_content import AccordionContent
from .accordion_header import AccordionHeader
from .image_accordion_content import ImageAccordionContent


class AccordionSection(QFrame, StyleMixin):
    """Individual collapsible section with header and content."""

    # Signals
    filter_selected = pyqtSignal(FilterType, object)
    expansion_requested = pyqtSignal(object)  # Emits self when expansion is requested

    def __init__(
        self,
        title: str,
        filter_type: FilterType,
        options: list,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.title = title
        self.filter_type = filter_type
        self.options = options
        self.is_expanded = False

        self._setup_ui()
        self._setup_animation()
        self._apply_styling()

    def _setup_ui(self) -> None:
        """Setup the section layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        self.header = AccordionHeader(self.title, self.is_expanded)
        self.header.clicked.connect(self._on_header_clicked)
        layout.addWidget(self.header)

        # Content - use image-based for certain types
        if self.filter_type.value in ["starting_position", "difficulty", "grid_mode"]:
            self.content = ImageAccordionContent(self.filter_type, self.options)
        else:
            self.content = AccordionContent(self.filter_type, self.options)

        self.content.filter_selected.connect(self.filter_selected.emit)
        layout.addWidget(self.content)

        # Initially hide content
        self.content.setMaximumHeight(0)
        self.content.setVisible(False)

    def _setup_animation(self) -> None:
        """Setup the expand/collapse animation with opacity effects."""
        # Height animation
        self.height_animation = QPropertyAnimation(self.content, b"maximumHeight")
        self.height_animation.setDuration(
            250
        )  # 250ms for smooth but responsive animation
        self.height_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        # Opacity effect and animation
        from PyQt6.QtCore import QParallelAnimationGroup
        from PyQt6.QtWidgets import QGraphicsOpacityEffect

        self.opacity_effect = QGraphicsOpacityEffect()
        self.content.setGraphicsEffect(self.opacity_effect)

        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(200)  # Slightly faster for opacity
        self.opacity_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        # Group animations to run in parallel
        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(self.height_animation)
        self.animation_group.addAnimation(self.opacity_animation)

        # Connect animation finished signal
        self.animation_group.finished.connect(self._on_animation_finished)

    def _on_header_clicked(self) -> None:
        """Handle header click to request expansion."""
        print(f"🔄 [ACCORDION SECTION] Header clicked: {self.title}")
        self.expansion_requested.emit(self)

    def _on_animation_finished(self) -> None:
        """Handle animation completion."""
        if not self.is_expanded:
            # Hide content completely when collapsed
            self.content.setVisible(False)

    def expand(self) -> None:
        """Expand this section to fill available space."""
        if self.is_expanded:
            return

        print(f"📖 [ACCORDION SECTION] Expanding: {self.title}")
        self.is_expanded = True
        self.header.set_expanded(True)

        # Show content and animate to full height and opacity
        self.content.setVisible(True)

        # Calculate available space dynamically
        target_height = self._calculate_available_space()

        # Setup height animation
        self.height_animation.setStartValue(0)
        self.height_animation.setEndValue(target_height)

        # Setup opacity animation
        self.opacity_animation.setStartValue(0.0)
        self.opacity_animation.setEndValue(1.0)

        # Start both animations
        self.animation_group.start()

    def _calculate_available_space(self) -> int:
        """Calculate available space for this section to expand into."""
        # Get parent container (accordion panel)
        parent = self.parent()
        if not parent:
            return self.content.content_height

        # Get total available height
        parent_height = parent.height()
        if parent_height <= 0:
            return self.content.content_height

        # Calculate space used by other sections (headers only, since content is collapsed)
        used_space = 0

        # Add space for all section headers
        for child in parent.children():
            if hasattr(child, "header") and child != self:
                used_space += child.header.height()

        # Add space for our own header
        used_space += self.header.height()

        # Add space for margins and spacing
        if hasattr(parent, "layout") and parent.layout():
            layout = parent.layout()
            margins = layout.contentsMargins()
            used_space += margins.top() + margins.bottom()
            # Add spacing between sections (number of sections - 1) * spacing
            section_count = len([c for c in parent.children() if hasattr(c, "header")])
            used_space += (section_count - 1) * layout.spacing()

        # Calculate available space for content
        available_space = parent_height - used_space

        # Ensure minimum space and don't exceed natural content height
        min_space = max(200, self.content.content_height)
        return max(min_space, available_space)

    def collapse(self) -> None:
        """Collapse this section."""
        if not self.is_expanded:
            return

        print(f"📕 [ACCORDION SECTION] Collapsing: {self.title}")
        self.is_expanded = False
        self.header.set_expanded(False)

        # Animate to zero height and opacity
        current_height = self.content.height()

        # Setup height animation
        self.height_animation.setStartValue(current_height)
        self.height_animation.setEndValue(0)

        # Setup opacity animation
        self.opacity_animation.setStartValue(1.0)
        self.opacity_animation.setEndValue(0.0)

        # Start both animations
        self.animation_group.start()

    def _apply_styling(self) -> None:
        """Apply glassmorphism styling to the section using standard patterns."""
        self.setStyleSheet(
            """
            AccordionSection {
                background: transparent;
                border: none;
                margin: 8px 0px;
                padding: 0px;
            }
        """
        )

    def get_buttons(self) -> dict:
        """Get all buttons from the content for external access."""
        return self.content.get_buttons()
