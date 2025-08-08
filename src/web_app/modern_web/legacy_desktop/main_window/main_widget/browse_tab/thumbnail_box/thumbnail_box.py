from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QVBoxLayout, QWidget

from main_window.main_widget.browse_tab.thumbnail_box.thumbnail_box_favorites_manager import (
    ThumbnailBoxFavoritesManager,
)
from main_window.main_widget.browse_tab.thumbnail_box.thumbnail_box_nav_buttons_widget import (
    ThumbnailBoxNavButtonsWidget,
)
from main_window.main_widget.browse_tab.thumbnail_box.thumbnail_image_label import (
    ThumbnailImageLabel,
)

from .thumbnail_box_header import ThumbnailBoxHeader
from .thumbnail_box_state import ThumbnailBoxState
from .variation_number_label import VariationNumberLabel

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class ThumbnailBox(QWidget):
    margin = 10

    def __init__(
        self,
        browse_tab: BrowseTab,
        word: str,
        thumbnails: list[str],
        in_sequence_viewer=False,
    ) -> None:
        super().__init__(browse_tab)
        self.word = word
        self.main_widget = browse_tab.main_widget
        self.browse_tab = browse_tab
        self.sequence_picker = self.browse_tab.sequence_picker
        self.scroll_Area = self.sequence_picker.scroll_widget.scroll_area
        self.in_sequence_viewer = in_sequence_viewer
        self.state = ThumbnailBoxState(thumbnails)
        self.margin = 10  # Default margin
        self._preferred_width = 300  # Default preferred width
        self._is_resizing = False  # Prevent resize loops

        # Set up logging to track resize events
        import logging

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self._resize_count = 0  # Track how many times we've been resized

        self._setup_components()
        self._setup_layout()
        self._setup_size_constraints()

        self.logger.info(
            f"🔧 ThumbnailBox created: {word}, in_sequence_viewer={in_sequence_viewer}"
        )

    def _setup_components(self):
        self.favorites_manager = ThumbnailBoxFavoritesManager(self)
        self.header = ThumbnailBoxHeader(self)
        self.image_label = ThumbnailImageLabel(self)
        self.variation_number_label = VariationNumberLabel(self)
        self.nav_buttons_widget = ThumbnailBoxNavButtonsWidget(self)

    def _setup_layout(self):
        self.setContentsMargins(0, 0, 0, 0)
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.header)
        layout.addWidget(self.image_label)
        layout.addWidget(self.nav_buttons_widget)
        layout.addStretch()
        layout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)

    def _setup_size_constraints(self):
        """Set up proper size constraints to prevent inappropriate resizing."""
        from PyQt6.QtWidgets import QSizePolicy

        if self.in_sequence_viewer:
            # For sequence viewer, allow more flexibility
            self.setSizePolicy(
                QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
            )
        else:
            # For browse tab, calculate and enforce strict size constraints
            self._calculate_and_set_size_constraints()

    def _calculate_and_set_size_constraints(self):
        """Calculate and set size constraints based on parent layout."""
        try:
            # Get the sequence picker width (this should be stable)
            sequence_picker_width = self.sequence_picker.width()

            # If sequence picker width is not available yet, use a reasonable default
            if sequence_picker_width <= 1:
                sequence_picker_width = 800  # Default fallback

            # Calculate nav sidebar width (approximately 15% of sequence picker)
            nav_sidebar_width = int(sequence_picker_width * 0.15)

            # Calculate scroll widget width (remaining space)
            scroll_widget_width = sequence_picker_width - nav_sidebar_width

            # Calculate scrollbar width
            scrollbar_width = int(self.main_widget.width() * 0.01)

            # Calculate usable width for thumbnails
            total_margins = (3 * self.margin * 2) + 10  # 3 boxes * margins + buffer
            usable_width = scroll_widget_width - scrollbar_width - total_margins

            # Each thumbnail should be exactly 1/3 of usable width
            target_width = max(150, int(usable_width // 3))

            # Set both preferred width and maximum width to prevent expansion
            self._preferred_width = target_width
            self.setMinimumWidth(150)  # Reasonable minimum
            self.setMaximumWidth(target_width + 20)  # Small tolerance for layout

            self.logger.debug(
                f"Size constraints set for '{self.word}': "
                f"min=150, preferred={target_width}, max={target_width + 20}"
            )

        except Exception as e:
            self.logger.warning(f"Error setting size constraints: {e}")
            # Fallback to reasonable defaults
            self._preferred_width = 200
            self.setMinimumWidth(150)
            self.setMaximumWidth(250)

    def sizeHint(self):
        """Provide size hint to the layout system instead of forcing fixed width."""
        from PyQt6.QtCore import QSize

        return QSize(self._preferred_width, super().sizeHint().height())

    def resizeEvent(self, event):
        # Prevent resize loops
        if self._is_resizing:
            super().resizeEvent(event)
            return

        self._resize_count += 1
        old_size = event.oldSize()
        new_size = event.size()

        self.logger.debug(
            f"🚨 RESIZE EVENT #{self._resize_count} - ThumbnailBox '{self.word}':"
        )
        self.logger.debug(f"   📐 Old size: {old_size.width()}x{old_size.height()}")
        self.logger.debug(f"   📐 New size: {new_size.width()}x{new_size.height()}")
        self.logger.debug(f"   🔄 in_sequence_viewer: {self.in_sequence_viewer}")

        super().resizeEvent(event)

        # Only resize if not in sequence viewer and size change is significant
        if not self.in_sequence_viewer:
            width_change = (
                abs(old_size.width() - new_size.width()) if old_size.isValid() else 0
            )
            if width_change > 10:  # Only resize if significant change
                self._update_size_constraints_if_needed()

    def _update_size_constraints_if_needed(self):
        """Update size constraints only when necessary to prevent resize loops."""
        if self._is_resizing:
            return

        self._is_resizing = True
        try:
            old_preferred_width = self._preferred_width
            self._calculate_and_set_size_constraints()

            width_change = abs(old_preferred_width - self._preferred_width)
            if width_change >= 5:
                self.logger.debug(
                    f"Updating geometry for '{self.word}': {old_preferred_width} → {self._preferred_width}"
                )
                self.updateGeometry()
            else:
                self.logger.debug(
                    f"Width change too small ({width_change}px) - skipping updateGeometry()"
                )
        finally:
            self._is_resizing = False

    def resize_thumbnail_box(self):
        """Legacy method - now handled by _update_size_constraints_if_needed."""
        self.logger.debug(
            f"🔧 resize_thumbnail_box() called for '{self.word}' - delegating to size constraints"
        )
        if not self.in_sequence_viewer:
            self._update_size_constraints_if_needed()

    def recalculate_size_constraints(self):
        """Public method to recalculate size constraints when layout changes."""
        if not self.in_sequence_viewer:
            self.logger.debug(f"Recalculating size constraints for '{self.word}'")
            self._calculate_and_set_size_constraints()

    def _get_browse_tab_available_width(self) -> int:
        """Get the actual available width for the Browse Tab's left panel."""
        try:
            sequence_picker = self.browse_tab.sequence_picker
            return sequence_picker.width()
        except (AttributeError, TypeError):
            return 800

    def _get_sequence_viewer_available_width(self) -> int:
        """Get the actual available width for the sequence viewer (right panel)."""
        try:
            sequence_viewer = self.browse_tab.sequence_viewer
            return sequence_viewer.width()
        except (AttributeError, TypeError):
            return 400

    def update_thumbnails(self, thumbnails=[]):
        self.state.update_thumbnails(thumbnails)
        self.nav_buttons_widget.state.thumbnails = thumbnails

        if self == self.browse_tab.sequence_viewer.state.matching_thumbnail_box:
            self.browse_tab.sequence_viewer.update_thumbnails(self.state.thumbnails)

        # self.variation_number_label.update_index(self.state.current_index)
        self.header.difficulty_label.update_difficulty_label()  # 🆕 Update difficulty!
        self.image_label.update_thumbnail(self.state.current_index)
