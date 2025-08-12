"""
Loading State Controller

Controls the loading and browsing state transitions for the sequence browser panel.
Manages visibility of loading widgets, progress updates, and state coordination.
"""

from __future__ import annotations

import logging

from PyQt6.QtWidgets import QLabel, QProgressBar, QWidget


logger = logging.getLogger(__name__)


class LoadingStateController:
    """
    Controller for managing loading state transitions.

    Handles:
    - Loading/browsing widget visibility
    - Progress bar updates
    - Loading state coordination
    - Cancel button management
    """

    def __init__(
        self,
        loading_widget: QWidget | None = None,
        browsing_widget: QWidget | None = None,
        loading_progress_bar: QProgressBar | None = None,
        loading_label: QLabel | None = None,
    ):
        """
        Initialize the loading state controller.

        Args:
            loading_widget: Widget to show during loading
            browsing_widget: Widget to show during browsing
            loading_progress_bar: Progress bar for loading updates
            loading_label: Label for loading messages
        """
        self.loading_widget = loading_widget
        self.browsing_widget = browsing_widget
        self.loading_progress_bar = loading_progress_bar
        self.loading_label = loading_label

        # State tracking
        self._is_loading = False
        self._loading_cancelled = False

    def show_loading_state(
        self, message: str = "Preparing to load sequences..."
    ) -> None:
        """
        Show loading UI and hide main content.

        Args:
            message: Loading message to display
        """
        logger.info(f"🔄 [LOADING_STATE] Showing loading state: {message}")

        self._is_loading = True
        self._loading_cancelled = False

        if self.loading_widget:
            self.loading_widget.show()
        if self.browsing_widget:
            self.browsing_widget.hide()

        # Reset progress
        if self.loading_progress_bar:
            self.loading_progress_bar.setValue(0)
            self.loading_progress_bar.setMaximum(100)

        if self.loading_label:
            self.loading_label.setText(message)

    def hide_loading_state(self) -> None:
        """Hide loading UI and show main content."""
        logger.info("✅ [LOADING_STATE] Hiding loading state")

        self._is_loading = False

        if self.loading_widget:
            self.loading_widget.hide()
        if self.browsing_widget:
            self.browsing_widget.show()

    def update_loading_progress(
        self, current: int, total: int, message: str = ""
    ) -> None:
        """
        Update loading progress.

        Args:
            current: Current progress value
            total: Total progress value
            message: Optional progress message
        """
        if self._loading_cancelled:
            return

        if self.loading_progress_bar:
            self.loading_progress_bar.setMaximum(total)
            self.loading_progress_bar.setValue(current)

        if self.loading_label and message:
            self.loading_label.setText(message)

        # Log progress at key milestones
        if total > 0:
            percentage = (current / total) * 100
            if percentage % 25 == 0:  # Log at 25%, 50%, 75%, 100%
                logger.info(
                    f"📊 [LOADING_STATE] Progress: {current}/{total} ({percentage:.0f}%)"
                )

    def set_loading_message(self, message: str) -> None:
        """
        Set the loading message.

        Args:
            message: Message to display
        """
        if self.loading_label:
            self.loading_label.setText(message)

    def cancel_loading(self) -> None:
        """Cancel the current loading operation."""
        logger.info("⛔ [LOADING_STATE] Loading cancelled")
        self._loading_cancelled = True

        if self.loading_label:
            self.loading_label.setText("Cancelling...")

    def is_loading(self) -> bool:
        """Check if currently in loading state."""
        return self._is_loading

    def is_loading_cancelled(self) -> bool:
        """Check if loading was cancelled."""
        return self._loading_cancelled

    def reset_state(self) -> None:
        """Reset the loading state."""
        self._is_loading = False
        self._loading_cancelled = False

        if self.loading_progress_bar:
            self.loading_progress_bar.setValue(0)

        if self.loading_label:
            self.loading_label.setText("")

    def set_widgets(
        self,
        loading_widget: QWidget | None = None,
        browsing_widget: QWidget | None = None,
        loading_progress_bar: QProgressBar | None = None,
        loading_label: QLabel | None = None,
    ) -> None:
        """
        Update the widget references.

        Args:
            loading_widget: Widget to show during loading
            browsing_widget: Widget to show during browsing
            loading_progress_bar: Progress bar for loading updates
            loading_label: Label for loading messages
        """
        if loading_widget is not None:
            self.loading_widget = loading_widget
        if browsing_widget is not None:
            self.browsing_widget = browsing_widget
        if loading_progress_bar is not None:
            self.loading_progress_bar = loading_progress_bar
        if loading_label is not None:
            self.loading_label = loading_label

    def prepare_for_progressive_loading(self) -> None:
        """Prepare state for progressive loading (keep browsing area visible)."""
        logger.info("🎨 [LOADING_STATE] Preparing for progressive loading")

        # For progressive loading, we want to keep the browsing widget visible
        # and just clear the content, rather than showing a loading screen
        self._is_loading = True
        self._loading_cancelled = False

        # Ensure browsing widget is visible
        if self.browsing_widget:
            self.browsing_widget.show()

        # Hide loading widget since we're doing progressive loading
        if self.loading_widget:
            self.loading_widget.hide()

    def finalize_progressive_loading(self, total_loaded: int) -> None:
        """
        Finalize progressive loading state.

        Args:
            total_loaded: Total number of items loaded
        """
        logger.info(
            f"✅ [LOADING_STATE] Progressive loading completed: {total_loaded} items"
        )

        self._is_loading = False

        # Ensure browsing widget is visible
        if self.browsing_widget:
            self.browsing_widget.show()

        # Hide loading widget
        if self.loading_widget:
            self.loading_widget.hide()
