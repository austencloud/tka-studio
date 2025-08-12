"""
Sequence Card Content Component

Modern implementation of the scrollable content display area.
Coordinates specialized helper components for layout and loading management.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import QCoreApplication, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.core.interfaces.sequence_card_services import (
    ISequenceCardCacheService,
    ISequenceCardLayoutService,
    SequenceCardData,
)
from desktop.modern.presentation.managers.sequence_card.page_layout_manager import (
    PageLayoutManager,
)
from desktop.modern.presentation.managers.sequence_card.progressive_loading_manager import (
    ProgressiveLoadingManager,
)
from desktop.modern.presentation.views.sequence_card.image_loader import ImageLoader


logger = logging.getLogger(__name__)


class SequenceCardContentComponent(QWidget):
    """Content component for displaying sequence cards."""

    sequences_displayed = pyqtSignal(int)  # Number of sequences displayed

    def __init__(
        self,
        display_adaptor,  # SequenceCardDisplayAdaptor
        cache_service: ISequenceCardCacheService,
        layout_service: ISequenceCardLayoutService,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.display_adaptor = display_adaptor
        self.cache_service = cache_service
        self.layout_service = layout_service

        self.current_sequences: list[SequenceCardData] = []
        self.current_column_count = 2

        # Create image loader for async loading
        self.image_loader = ImageLoader()

        # Create specialized helper managers
        self.progressive_loading_manager = ProgressiveLoadingManager(
            self.image_loader, parent_component=self
        )

        self._setup_ui()
        self._setup_connections()

        # Initialize page layout manager after UI setup
        self.page_layout_manager = PageLayoutManager(
            self.layout_service,
            self.content_layout,
            self.image_loader,
            self.cache_service,
        )

    def _setup_ui(self) -> None:
        """Setup content UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # Content widget for scroll area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(15)

        # Initial empty state
        self._show_empty_state()

        self.scroll_area.setWidget(self.content_widget)
        layout.addWidget(self.scroll_area)

        self._apply_styling()

    def _apply_styling(self) -> None:
        """Apply content area styling."""
        self.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background: transparent;
            }

            QScrollBar:vertical {
                background: rgba(0,0,0,0.1);
                width: 8px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical {
                background: rgba(0,0,0,0.3);
                border-radius: 4px;
                min-height: 20px;
            }

            QScrollBar::handle:vertical:hover {
                background: rgba(0,0,0,0.5);
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """
        )

    def _setup_connections(self) -> None:
        """Setup signal connections."""
        self.display_adaptor.sequences_loaded.connect(self._on_sequences_loaded)

    def _show_empty_state(self) -> None:
        """Show empty state message."""
        self._clear_content()

        empty_label = QLabel(
            "No sequences to display.\nSelect a sequence length from the sidebar."
        )
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_label.setStyleSheet(
            """
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                background: rgba(40, 40, 40, 0.3);
                border: 2px dashed rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                padding: 40px;
                margin: 20px;
                font-size: 14px;
                font-style: italic;
            }
        """
        )

        font = QFont()
        font.setPointSize(14)
        font.setItalic(True)
        empty_label.setFont(font)

        self.content_layout.addWidget(empty_label)

    def _clear_content(self) -> None:
        """Clear all content widgets and stop any ongoing loading (legacy behavior)."""
        # Stop progressive loading if active
        self._stop_progressive_loading()

        # CRITICAL: Clear page layout manager's internal state first (legacy pattern)
        # Check if page_layout_manager exists (it's created after _setup_ui)
        if hasattr(self, "page_layout_manager"):
            self.page_layout_manager.clear_all_pages()

        # Clear page widgets list
        self.page_widgets = []

        # Clear all widgets from content layout (only if content_layout exists)
        if hasattr(self, "content_layout"):
            while self.content_layout.count():
                child = self.content_layout.takeAt(0)
                if child and child.widget():
                    widget = child.widget()
                    widget.setParent(None)
                    widget.deleteLater()
                elif child and child.layout():
                    # Handle nested layouts (page row layouts)
                    nested_layout = child.layout()
                    while nested_layout.count():
                        subchild = nested_layout.takeAt(0)
                        if subchild and subchild.widget():
                            subwidget = subchild.widget()
                            subwidget.setParent(None)
                            subwidget.deleteLater()

    def _stop_progressive_loading(self) -> None:
        """Stop any ongoing progressive loading."""
        self.progressive_loading_manager.stop_progressive_loading()

    def _on_sequences_loaded(self, sequences: list[SequenceCardData]) -> None:
        """Handle sequences loaded signal with immediate UI response."""
        logger.info(f"Content component: {len(sequences)} sequences loaded")
        self.current_sequences = sequences

        # IMMEDIATE UI RESPONSE: Show structure instantly, then load progressively
        self.refresh_display_immediate()

    def refresh_display_immediate(self) -> None:
        """Refresh display with immediate UI response and progressive loading."""
        self._clear_content()

        if not self.current_sequences:
            self._show_empty_state()
            return

        try:
            # Check if page_layout_manager is available
            if not hasattr(self, "page_layout_manager"):
                logger.warning(
                    "PageLayoutManager not yet initialized, skipping display"
                )
                return

            # IMMEDIATE UI RESPONSE: Show page structure instantly with placeholders
            page_widgets = self.page_layout_manager.display_page_structure_immediately(
                self.current_sequences, self.current_column_count
            )

            # Process events to ensure immediate display
            QCoreApplication.processEvents()

            # Set up progressive loading manager with the page widgets
            self.progressive_loading_manager.set_page_widgets(page_widgets)

            # Assign image loaders to all widgets
            self.page_layout_manager.assign_image_loaders()

            # Start progressive image loading in background
            QTimer.singleShot(
                10, self.progressive_loading_manager.start_progressive_loading
            )

            self.sequences_displayed.emit(len(self.current_sequences))

        except Exception as e:
            logger.exception(f"Error refreshing display immediately: {e}")
            self._show_error_state(str(e))

    def refresh_display(self) -> None:
        """Refresh the display with current sequences (legacy method)."""
        self._clear_content()

        if not self.current_sequences:
            self._show_empty_state()
            return

        try:
            # Check if page_layout_manager is available
            if not hasattr(self, "page_layout_manager"):
                logger.warning(
                    "PageLayoutManager not yet initialized, skipping refresh"
                )
                return

            # Use page layout manager for display
            page_widgets = self.page_layout_manager.display_sequences_in_pages(
                self.current_sequences, self.current_column_count
            )

            # Set up progressive loading manager
            self.progressive_loading_manager.set_page_widgets(page_widgets)
            self.progressive_loading_manager.start_progressive_loading()

            self.sequences_displayed.emit(len(self.current_sequences))

        except Exception as e:
            logger.exception(f"Error refreshing display: {e}")
            self._show_error_state(str(e))

    def _show_error_state(self, error_message: str) -> None:
        """Show error state."""
        self._clear_content()

        error_label = QLabel(f"Error displaying sequences:\n{error_message}")
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setStyleSheet(
            """
            QLabel {
                color: #e74c3c;
                background: rgba(231, 76, 60, 0.1);
                border: 2px solid #e74c3c;
                border-radius: 10px;
                padding: 20px;
                margin: 20px;
                font-size: 12px;
            }
        """
        )

        self.content_layout.addWidget(error_label)

    def set_column_count(self, column_count: int) -> None:
        """Set the number of columns for page display."""
        self.current_column_count = column_count
        self.refresh_display()

    def get_scroll_position(self) -> int:
        """Get current scroll position."""
        return self.scroll_area.verticalScrollBar().value()

    def set_scroll_position(self, position: int) -> None:
        """Set scroll position."""
        self.scroll_area.verticalScrollBar().setValue(position)
