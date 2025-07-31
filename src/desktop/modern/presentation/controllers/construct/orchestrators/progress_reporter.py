"""
ProgressReporter

Manages initialization progress reporting across components.
This is Qt-agnostic and focuses on progress coordination.
"""

from collections.abc import Callable


class ProgressReporter:
    """
    Manages progress reporting during component initialization.

    Responsibilities:
    - Tracking initialization progress across components
    - Providing consistent progress updates
    - Managing progress callback coordination
    """

    def __init__(self, progress_callback: Callable[[int, str], None] | None = None):
        self.progress_callback = progress_callback
        self.progress_ranges = {
            "layout_setup": (84, 86),
            "workbench_creation": (86, 87),
            "start_position_creation": (87, 88),
            "option_picker_creation": (88, 89),
            "graph_editor_creation": (89, 90),
            "generate_controls_creation": (90, 91),
            "signal_connection": (91, 92),
            "finalization": (92, 100),
        }
        self.current_phase = None

    def start_phase(self, phase_name: str, message: str):
        """Start a new initialization phase."""
        if self.progress_callback and phase_name in self.progress_ranges:
            self.current_phase = phase_name
            start_progress = self.progress_ranges[phase_name][0]
            self.progress_callback(start_progress, message)

    def update_phase_progress(
        self, phase_name: str, progress_percent: float, message: str
    ):
        """Update progress within a phase."""
        if self.progress_callback and phase_name in self.progress_ranges:
            start_progress, end_progress = self.progress_ranges[phase_name]
            current_progress = (
                start_progress + (end_progress - start_progress) * progress_percent
            )
            self.progress_callback(int(current_progress), message)

    def complete_phase(self, phase_name: str, message: str):
        """Complete a phase."""
        if self.progress_callback and phase_name in self.progress_ranges:
            end_progress = self.progress_ranges[phase_name][1]
            self.progress_callback(end_progress, message)
            if phase_name == self.current_phase:
                self.current_phase = None

    def report_component_progress(
        self, component_name: str, progress_percent: float, message: str
    ):
        """Report progress for a specific component."""
        if component_name == "option_picker":
            # Special handling for option picker progress (76-82 range)
            mapped_progress = int(76 + (progress_percent * 6))
            if self.progress_callback:
                self.progress_callback(mapped_progress, f"Option picker: {message}")
        else:
            # Use current phase for other components
            if self.current_phase:
                self.update_phase_progress(
                    self.current_phase, progress_percent, message
                )

    def report_error(self, component_name: str, error_message: str):
        """Report an error during component initialization."""
        if self.progress_callback:
            message = f"Error in {component_name}: {error_message}"
            # Continue with current progress, just update message
            if self.current_phase and self.current_phase in self.progress_ranges:
                current_progress = self.progress_ranges[self.current_phase][0]
                self.progress_callback(current_progress, message)

    def get_overall_progress(self) -> int:
        """Get the overall progress percentage."""
        if self.current_phase and self.current_phase in self.progress_ranges:
            return self.progress_ranges[self.current_phase][0]
        return 0

    def get_phase_progress_ranges(self) -> dict:
        """Get all phase progress ranges."""
        return self.progress_ranges.copy()

    def is_phase_active(self, phase_name: str) -> bool:
        """Check if a phase is currently active."""
        return self.current_phase == phase_name

    def get_current_phase(self) -> str | None:
        """Get the current active phase."""
        return self.current_phase
