"""
Progressive Loading Manager

Manages progressive image loading with immediate UI response and background loading.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import QCoreApplication, QTimer

from desktop.modern.presentation.views.sequence_card.image_loader import ImageLoader
from desktop.modern.presentation.views.sequence_card.sequence_card_page_widget import (
    SequenceCardPageWidget,
)


logger = logging.getLogger(__name__)


class ProgressiveLoadingManager:
    """Manages progressive loading of sequence card images."""

    def __init__(self, image_loader: ImageLoader, parent_component=None):
        self.image_loader = image_loader
        self.parent_component = parent_component
        self.page_widgets: list[SequenceCardPageWidget] = []

        # Progressive loading state
        self._progressive_timer: QTimer | None = None
        self._current_loading_cards = []
        self._current_loading_index = 0
        self._current_batch_name = ""
        self._is_priority_batch = False

    def set_page_widgets(self, page_widgets: list[SequenceCardPageWidget]):
        """Set the page widgets to manage loading for."""
        self.page_widgets = page_widgets

    def start_progressive_loading(self):
        """Start optimized progressive loading with immediate UI response."""
        if not self.page_widgets:
            return

        logger.info("Starting optimized progressive loading with immediate response")

        # Stage 1: Display placeholder cards immediately for instant response
        self._display_placeholder_cards()

        # Stage 2: Start background image loading
        self._start_background_image_loading()

    def stop_progressive_loading(self):
        """Stop any ongoing progressive loading."""
        if self._progressive_timer:
            self._progressive_timer.stop()
            self._progressive_timer.deleteLater()
            self._progressive_timer = None

        # Clear loading state
        self._current_loading_cards = []
        self._current_loading_index = 0
        self._current_batch_name = ""
        self._is_priority_batch = False

    def _display_placeholder_cards(self):
        """Display placeholder cards immediately for instant UI response."""
        total_cards = sum(len(page.card_widgets) for page in self.page_widgets)

        logger.info(f"Displaying {total_cards} placeholder cards instantly")

        for page_widget in self.page_widgets:
            for card_widget in page_widget.card_widgets:
                # Display placeholder immediately
                card_widget.show_placeholder()

        # Process events once to ensure immediate display
        QCoreApplication.processEvents()

        # Update header with immediate feedback
        if (
            self.parent_component
            and hasattr(self.parent_component, "parent")
            and hasattr(self.parent_component.parent(), "header")
            and hasattr(self.parent_component.parent().header, "set_description_text")
        ):
            self.parent_component.parent().header.set_description_text(
                f"Displaying {total_cards} sequence cards across {len(self.page_widgets)} pages"
            )

    def _start_background_image_loading(self):
        """Start background image loading with viewport priority."""
        # Get visible viewport first
        visible_cards = self._get_visible_cards()
        background_cards = self._get_background_cards()

        logger.info(
            f"Loading {len(visible_cards)} visible cards first, then {len(background_cards)} background cards"
        )

        # Load visible cards first with high priority
        self._load_cards_batch(visible_cards, is_priority=True)

        # Then load background cards
        self._load_cards_batch(background_cards, is_priority=False)

    def _get_visible_cards(self):
        """Get cards that are currently visible in the viewport."""
        visible_cards = []

        # Optimized: Load only first page immediately for instant response
        # This provides immediate visual feedback while background loads
        if self.page_widgets:
            # Load first page (6 cards) for immediate visual response
            first_page = self.page_widgets[0]
            visible_cards.extend(first_page.card_widgets)

            # Add second page if available for smooth scrolling
            if len(self.page_widgets) > 1:
                second_page = self.page_widgets[1]
                visible_cards.extend(second_page.card_widgets)

        return visible_cards

    def _get_background_cards(self):
        """Get cards that are not currently visible."""
        visible_cards = self._get_visible_cards()
        all_cards = []

        for page_widget in self.page_widgets:
            all_cards.extend(page_widget.card_widgets)

        return [card for card in all_cards if card not in visible_cards]

    def _load_cards_batch(self, cards, is_priority=True):
        """Load a batch of cards with progressive processing (legacy pattern)."""
        if not cards:
            return

        batch_name = "priority" if is_priority else "background"
        logger.info(f"Loading {len(cards)} {batch_name} cards progressively")

        # Use QTimer for truly progressive loading (one image at a time)
        self._current_loading_cards = cards.copy()
        self._current_loading_index = 0
        self._current_batch_name = batch_name
        self._is_priority_batch = is_priority

        # Start progressive loading with timer
        self._progressive_timer = QTimer()
        self._progressive_timer.timeout.connect(self._load_next_card)
        self._progressive_timer.start(1)  # Load one image every 1ms for maximum speed

    def _load_next_card(self):
        """Load the next card in the progressive loading sequence."""
        if not self._current_loading_cards or self._current_loading_index >= len(
            self._current_loading_cards
        ):
            # Finished loading this batch
            if self._progressive_timer:
                self._progressive_timer.stop()
                self._progressive_timer.deleteLater()
                self._progressive_timer = None

            logger.info(f"Completed loading {self._current_batch_name} cards")
            return

        # Load current card with safety checks
        card_widget = self._current_loading_cards[self._current_loading_index]

        # Safety check: ensure widget still exists and is valid
        try:
            if (
                card_widget and card_widget.isVisible() is not None
            ):  # Widget still exists
                card_widget.load_image_optimized()
        except RuntimeError:
            # Widget has been deleted, skip it
            logger.debug(
                f"Skipping deleted widget at index {self._current_loading_index}"
            )

        self._current_loading_index += 1
        loaded_count = self._current_loading_index
        total_cards = len(self._current_loading_cards)

        # LEGACY PATTERN: Process events after EVERY single image
        QCoreApplication.processEvents()

        # Update progress frequently for better user feedback
        if loaded_count % 3 == 0 or loaded_count == total_cards:
            if self._is_priority_batch:
                progress_text = (
                    f"Loading visible images... {loaded_count}/{total_cards}"
                )
            else:
                progress_text = (
                    f"Loading background images... {loaded_count}/{total_cards}"
                )

            try:
                if (
                    self.parent_component
                    and hasattr(self.parent_component, "parent")
                    and hasattr(self.parent_component.parent(), "header")
                    and hasattr(
                        self.parent_component.parent().header, "set_description_text"
                    )
                ):
                    self.parent_component.parent().header.set_description_text(
                        progress_text
                    )
            except RuntimeError:
                # Parent may have been deleted, ignore
                pass

        # Check if we've finished loading
        if loaded_count >= total_cards:
            if self._progressive_timer:
                self._progressive_timer.stop()
                self._progressive_timer.deleteLater()
                self._progressive_timer = None
