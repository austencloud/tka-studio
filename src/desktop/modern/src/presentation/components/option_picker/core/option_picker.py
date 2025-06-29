from typing import Any, Callable, Dict, List, Optional

from core.dependency_injection.di_container import DIContainer
from core.interfaces.option_picker_services import (
    IOptionPickerOrchestrator,
)
from domain.models.core_models import BeatData, SequenceData
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

# Import the new base class
from ..component_base import ViewableComponentBase


class OptionPicker(ViewableComponentBase):
    """
    Modern Option Picker - REFACTORED Component Implementation

    REFACTORED: Now uses orchestrator pattern with specialized services:
    - OptionPickerOrchestrator for coordination
    - Clean separation of concerns
    - Pure dependency injection
    - Event-driven communication
    - Proper lifecycle management

    This works directly with Modern data structures (BeatData, SequenceData).
    """

    option_selected = pyqtSignal(str)
    beat_data_selected = pyqtSignal(object)  # New signal for actual BeatData

    def __init__(
        self,
        container: DIContainer,
        progress_callback: Optional[Callable[[str, float], None]] = None,
        parent=None,
    ):
        """
        Initialize the option picker with orchestrator pattern.

        Args:
            container: DI container for service resolution
            progress_callback: Optional progress reporting callback
            parent: Parent widget
        """
        super().__init__(container, parent)

        # Component-specific properties
        self.progress_callback = progress_callback

        # Initialize orchestrator with dependency injection
        from application.services.option_picker.option_picker_orchestrator import (
            OptionPickerOrchestrator,
        )

        self.orchestrator = OptionPickerOrchestrator(
            container=container, progress_callback=progress_callback
        )

        # Connect orchestrator signals to our signals
        self.orchestrator.option_selected.connect(self.option_selected.emit)
        self.orchestrator.beat_data_selected.connect(self.beat_data_selected.emit)

    def initialize(self) -> None:
        """Initialize the option picker using orchestrator pattern."""
        try:
            # Delegate initialization to orchestrator
            self.orchestrator.initialize(self.progress_callback)

            # Store widget reference for base class compatibility
            self._widget = self.orchestrator.get_widget()

            # Mark as initialized and emit signal
            self._initialized = True
            self.component_ready.emit()

        except Exception as e:
            # Use base class error handling
            self.emit_error(f"Failed to initialize option picker: {e}", e)
            raise

    def get_widget(self) -> QWidget:
        """Get the main widget for this component."""
        if not self._widget:
            raise RuntimeError("OptionPicker not initialized - call initialize() first")
        return self._widget

    def cleanup(self) -> None:
        """Clean up option picker resources."""
        try:
            # Delegate cleanup to orchestrator
            if self.orchestrator:
                self.orchestrator.cleanup()

            # Call parent cleanup
            super().cleanup()

        except Exception as e:
            self.emit_error(f"Error during cleanup: {e}", e)

    def load_motion_combinations(self, sequence_data: List[Dict[str, Any]]) -> None:
        """Load motion combinations using orchestrator."""
        if self.orchestrator:
            self.orchestrator.load_motion_combinations(sequence_data)

    def get_beat_data_for_option(self, option_id: str) -> Optional[BeatData]:
        """Get BeatData for a specific option ID using orchestrator."""
        if self.orchestrator:
            return self.orchestrator.get_beat_data_for_option(option_id)
        return None

    def refresh_options(self) -> None:
        """Refresh the option picker with latest beat options using orchestrator."""
        if self.orchestrator:
            self.orchestrator.refresh_options()

    def refresh_options_from_sequence(
        self, sequence_data: List[Dict[str, Any]]
    ) -> None:
        """Refresh options based on sequence state (DEPRECATED - compatibility)."""
        # Delegate to load_motion_combinations for compatibility
        self.load_motion_combinations(sequence_data)

    def refresh_options_from_modern_sequence(self, sequence: SequenceData) -> None:
        """PURE Modern: Refresh options based on Modern SequenceData using orchestrator."""
        if self.orchestrator:
            self.orchestrator.refresh_from_sequence(sequence)

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
        # This method is for debugging - could be implemented if needed
        print(f"Dimension logging for phase: {phase} (orchestrator pattern)")
