from __future__ import annotations

from collections.abc import Callable
from typing import Any

from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtWidgets import QWidget

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.domain.models import SequenceData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.presentation.components.component_base import ViewableComponentBase
from desktop.modern.presentation.components.option_picker.components.option_picker_widget import (
    OptionPickerWidget,
)


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
        progress_callback: Callable[[str, float], None] | None = None,
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
        self._is_preparing_for_transition = False

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
        """Get size provider using WindowDiscoveryService - clean architecture."""
        try:
            # ✅ Use service from DI container instead of complex hierarchy walking
            from desktop.modern.application.services.ui.window_discovery_service import (
                IWindowDiscoveryService,
            )

            window_discovery_service = self.container.resolve(IWindowDiscoveryService)
            return window_discovery_service.create_size_provider()

        except Exception as e:
            # Fallback to simple size provider if service resolution fails
            print(f"⚠️ [OPTION_PICKER] Failed to resolve WindowDiscoveryService: {e}")
            return lambda: QSize(1200, 800)

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

    def prepare_for_transition(self) -> None:
        """Prepare option picker for widget transition by pre-loading content without fades."""
        self._is_preparing_for_transition = True
        try:
            # Pre-load content without fade animations
            if self.option_picker_widget and hasattr(
                self.option_picker_widget, "prepare_content_for_transition"
            ):
                self.option_picker_widget.prepare_content_for_transition()
        finally:
            self._is_preparing_for_transition = False

    def is_preparing_for_transition(self) -> bool:
        """Check if option picker is currently preparing for a widget transition."""
        return self._is_preparing_for_transition

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

    def load_motion_combinations(self, sequence_data: list[dict[str, Any]]) -> None:
        """Load motion combinations using simplified picker."""
        if self.option_picker_widget:
            self.option_picker_widget.load_motion_combinations(sequence_data)

    def get_pictograph_for_option(self, option_id: str) -> PictographData | None:
        """Get PictographData for a specific option ID - simplified stub."""
        # For now, return None - can be enhanced later if needed
        return None

    def refresh_options(self) -> None:
        """Refresh the option picker with latest beat options using simplified picker."""
        if self.option_picker_widget:
            self.option_picker_widget.refresh_options()

    def refresh_options_from_sequence(
        self, sequence_data: list[dict[str, Any]]
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
