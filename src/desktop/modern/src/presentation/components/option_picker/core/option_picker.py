from typing import Any, Callable, Dict, List, Optional

from core.dependency_injection.di_container import DIContainer
from domain.models import SequenceData
from domain.models.pictograph_data import PictographData
from presentation.components.component_base import ViewableComponentBase
from presentation.components.option_picker.core.option_picker_widget import (
    OptionPickerWidget,
)
from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtWidgets import QWidget


class OptionPicker(ViewableComponentBase):
    """
    Modern Option Picker - SIMPLIFIED Implementation using Legacy Success Pattern

    SIMPLIFIED: Now uses direct Legacy pattern instead of complex orchestration:
    - SimplifiedOptionPicker with direct Qt layout management
    - Simple factory-based object pool creation
    - Natural Qt sizing without business logic interference
    - Minimal dependency injection and service complexity

    This maintains compatibility with Modern data structures while using Legacy's proven approach.
    """

    option_selected = pyqtSignal(str)
    pictograph_selected = pyqtSignal(object)  # PictographData object

    def __init__(
        self,
        container: DIContainer,
        progress_callback: Optional[Callable[[str, float], None]] = None,
        parent=None,
    ):
        """
        Initialize the option picker with simplified pattern.

        Args:
            container: DI container for service resolution (minimal usage)
            progress_callback: Optional progress reporting callback
            parent: Parent widget
        """
        super().__init__(container, parent)

        # Component-specific properties
        self.progress_callback = progress_callback

        # Create option picker widget directly
        self.option_picker_widget = OptionPickerWidget(
            parent=parent,
            mw_size_provider=self._get_size_provider(),
            progress_callback=progress_callback,
            container=container,
        )

        # Connect widget's pictograph selection signal to our signal
        self.option_picker_widget.pictograph_selected.connect(
            self.pictograph_selected.emit
        )

    def _get_size_provider(self) -> Callable[[], QSize]:
        """Get size provider for the simplified picker that finds the main window."""

        def size_provider():
            # Try to find the main window by walking up the widget hierarchy
            widget = self
            while widget and widget.parent():
                widget = widget.parent()
                # Look for QMainWindow or a widget with "MainWindow" in its class name
                if hasattr(widget, "__class__"):
                    class_name = widget.__class__.__name__
                    if "MainWindow" in class_name or hasattr(widget, "menuBar"):
                        return widget.size()

            # Fallback: try to get from QApplication
            from PyQt6.QtWidgets import QApplication

            app: QApplication = QApplication.instance()
            if app:
                # Get the active window or primary screen size
                active_window = app.activeWindow()
                if active_window:
                    return active_window.size()

                # Use primary screen size as last resort
                screen = app.primaryScreen()
                if screen:
                    screen_size = screen.size()
                    # Return a reasonable portion of screen size
                    return QSize(
                        int(screen_size.width() * 0.8), int(screen_size.height() * 0.8)
                    )

            # Final fallback
            return QSize(1200, 800)

        return size_provider

    def initialize(self) -> None:
        """Initialize the option picker using simplified pattern."""
        try:
            # Simplified initialization - already done in constructor
            self.option_picker_widget.initialize()

            # Store widget reference for base class compatibility
            self._widget = self.option_picker_widget.get_widget()

            # Mark as initialized and emit signal
            self._initialized = True
            self.component_ready.emit()

        except Exception as e:
            # Use base class error handling
            self.emit_error(f"Failed to initialize option picker: {e}", e)
            raise

    def make_widgets_visible(self) -> None:
        """Make the option picker widgets visible after main window is shown."""
        if self._initialized and self.option_picker_widget:
            # Simplified - just show the widget
            self._widget.show()

    def get_widget(self) -> QWidget:
        """Get the main widget for this component."""
        if not self._widget:
            raise RuntimeError("OptionPicker not initialized - call initialize() first")
        return self._widget

    def cleanup(self) -> None:
        """Clean up option picker resources."""
        try:
            # Delegate cleanup to option picker widget
            if self.option_picker_widget:
                self.option_picker_widget.cleanup()

            # Call parent cleanup
            super().cleanup()

        except Exception as e:
            self.emit_error(f"Error during cleanup: {e}", e)

    def load_motion_combinations(self, sequence_data: List[Dict[str, Any]]) -> None:
        """Load motion combinations using simplified picker."""
        if self.option_picker_widget:
            self.option_picker_widget.load_motion_combinations(sequence_data)

    def get_pictograph_for_option(self, option_id: str) -> Optional["PictographData"]:
        """Get PictographData for a specific option ID - simplified stub."""
        # For now, return None - can be enhanced later if needed
        return None

    def refresh_options(self) -> None:
        """Refresh the option picker with latest beat options using simplified picker."""
        if self.option_picker_widget:
            self.option_picker_widget.refresh_options()

    def refresh_options_from_sequence(
        self, sequence_data: List[Dict[str, Any]]
    ) -> None:
        """Refresh options based on sequence state (DEPRECATED - compatibility)."""
        # Delegate to load_motion_combinations for compatibility
        self.load_motion_combinations(sequence_data)

    def refresh_options_from_modern_sequence(self, sequence: SequenceData) -> None:
        """PURE Modern: Refresh options based on Modern SequenceData using simplified picker."""
        if self.option_picker_widget:
            self.option_picker_widget.refresh_from_sequence(sequence)

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable the widget."""
        if self._widget:
            self._widget.setEnabled(enabled)

    def get_size(self) -> tuple[int, int]:
        """Get widget size."""
        if self._widget:
            return (self._widget.width(), self._widget.height())
        return (600, 800)

    def log_dimensions(self, phase: str) -> None:
        """Log comprehensive dimension analysis."""
        # This method is for debugging - simplified version
        print(f"Dimension logging for phase: {phase} (simplified pattern)")
