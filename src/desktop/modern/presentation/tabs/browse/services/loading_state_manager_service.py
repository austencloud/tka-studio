"""
Loading State Manager Service

Service for managing loading states, progress, and loading UI components.
"""

from desktop.modern.core.interfaces.browse_services import ILoadingStateManager
from PyQt6.QtWidgets import QLabel, QProgressBar, QWidget


class LoadingStateManagerService(ILoadingStateManager):
    """Service for managing loading states and progress."""

    def __init__(
        self,
        loading_widget: QWidget,
        browsing_widget: QWidget,
        loading_progress_bar: QProgressBar,
        loading_label: QLabel,
        layout_manager,
    ):
        """Initialize with UI components."""
        self.loading_widget = loading_widget
        self.browsing_widget = browsing_widget
        self.loading_progress_bar = loading_progress_bar
        self.loading_label = loading_label
        self.layout_manager = layout_manager

        self._is_progressive_loading = False
        self._loading_cancelled = False

    def show_loading_state(self) -> None:
        """Show loading UI and hide main content."""
        self._is_progressive_loading = True
        self._loading_cancelled = False

        self.loading_widget.show()
        self.browsing_widget.hide()

        # Reset progress
        if self.loading_progress_bar:
            self.loading_progress_bar.setValue(0)
            self.loading_progress_bar.setMaximum(100)

        if self.loading_label:
            self.loading_label.setText("Preparing to load sequences...")

    def hide_loading_state(self) -> None:
        """Hide loading UI and show main content."""
        self._is_progressive_loading = False

        self.loading_widget.hide()
        self.browsing_widget.show()

    def update_progress(self, current: int, total: int, message: str = "") -> None:
        """Update loading progress."""
        if self._loading_cancelled:
            return

        if self.loading_progress_bar:
            self.loading_progress_bar.setMaximum(total)
            self.loading_progress_bar.setValue(current)

        if self.loading_label and message:
            self.loading_label.setText(message)

        progress_percent = (current / total * 100) if total > 0 else 0

    def show_empty_state(self) -> None:
        """Show empty state when no sequences are found."""
        self.hide_loading_state()
        self.layout_manager.clear_grid()
        self.layout_manager.add_empty_state()

    def show_loading_fallback(self) -> None:
        """Show basic loading message when progressive loading unavailable."""
        self.layout_manager.clear_grid()
        self.layout_manager.add_loading_fallback()

    def cancel_loading(self) -> None:
        """Cancel the current loading operation."""
        if self._is_progressive_loading:
            print("❌ User cancelled loading")
            self._loading_cancelled = True

    @property
    def is_loading(self) -> bool:
        """Check if currently loading."""
        return self._is_progressive_loading

    @property
    def is_cancelled(self) -> bool:
        """Check if loading was cancelled."""
        return self._loading_cancelled

    def set_loading_started(self, total_count: int) -> None:
        """Handle loading started."""

        if self.loading_progress_bar:
            self.loading_progress_bar.setMaximum(total_count)
            self.loading_progress_bar.setValue(0)

        if self.loading_label:
            self.loading_label.setText(f"Loading {total_count} sequences...")

    def set_loading_completed(self, total_loaded: int) -> None:
        """Handle loading completion."""
        if self._loading_cancelled:
            return
        self.hide_loading_state()

    def set_loading_cancelled(self) -> None:
        """Handle loading cancellation."""

        self.hide_loading_state()
        self._loading_cancelled = True
