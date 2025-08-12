"""
Construct Tab Service Interfaces

Defines clean interfaces for construct tab services to enable proper dependency injection
and eliminate the None initialization anti-pattern.
"""

from __future__ import annotations

from typing import Any, Protocol

from PyQt6.QtWidgets import QWidget

from desktop.modern.domain.models import BeatData, SequenceData


class IConstructTabLayoutService(Protocol):
    """Interface for construct tab layout management."""

    def setup_layout(self, parent_widget: QWidget) -> None:
        """Set up the main UI layout."""
        ...

    def get_workbench_widget(self) -> QWidget:
        """Get the workbench widget."""
        ...

    def get_picker_widget(self) -> QWidget:
        """Get the picker panel widget."""
        ...

    def transition_to_start_position_picker(self) -> None:
        """Transition to start position picker."""
        ...

    def transition_to_option_picker(self) -> None:
        """Transition to option picker."""
        ...

    def transition_to_graph_editor(self) -> None:
        """Transition to graph editor."""
        ...

    def transition_to_generate_controls(self) -> None:
        """Transition to generate controls."""
        ...

    def transition_to_export_panel(self) -> None:
        """Transition to export panel."""
        ...


class IConstructTabComponentFactory(Protocol):
    """Interface for creating construct tab components."""

    def create_workbench(self) -> tuple[QWidget, Any]:
        """Create workbench component and return (widget, component)."""
        ...

    def create_start_position_picker(self) -> tuple[QWidget, Any]:
        """Create start position picker and return (widget, component)."""
        ...

    def create_option_picker(self) -> tuple[QWidget, Any]:
        """Create option picker and return (widget, component)."""
        ...

    def create_graph_editor(self) -> tuple[QWidget, Any]:
        """Create graph editor and return (widget, component)."""
        ...

    def create_generate_panel(self) -> tuple[QWidget, Any]:
        """Create generate panel and return (widget, component)."""
        ...

    def create_export_panel(self) -> tuple[QWidget, Any]:
        """Create export panel and return (widget, component)."""
        ...


class IConstructTabCoordinationService(Protocol):
    """Interface for coordinating construct tab components."""

    def setup_component_coordination(self, components: dict[str, Any]) -> None:
        """Set up coordination between components."""
        ...

    def handle_sequence_modified(self, sequence: SequenceData) -> None:
        """Handle sequence modification events."""
        ...

    def handle_start_position_set(self, start_position: BeatData) -> None:
        """Handle start position set events."""
        ...

    def handle_beat_added(self, beat_data: BeatData) -> None:
        """Handle beat added events."""
        ...

    def handle_generation_request(self, generation_config: dict[str, Any]) -> None:
        """Handle generation request events."""
        ...

    def handle_ui_transition_request(self, target_panel: str) -> None:
        """Handle UI transition requests."""
        ...


class IWorkbenchCoordinationService(Protocol):
    """Interface for workbench-specific coordination."""

    def setup_workbench_signals(self, workbench: Any) -> None:
        """Set up workbench signal connections."""
        ...

    def handle_workbench_operation(self, operation_type: str, **kwargs) -> None:
        """Handle workbench operations."""
        ...

    def update_workbench_state(self, sequence: SequenceData | None) -> None:
        """Update workbench state."""
        ...


class IWorkbenchUIService(Protocol):
    """Interface for workbench UI management."""

    def setup_workbench_ui(self, parent: QWidget) -> QWidget:
        """Set up workbench UI and return the main widget."""
        ...

    def update_sequence_display(self, sequence: SequenceData | None) -> None:
        """Update sequence display."""
        ...

    def update_beat_selection(self, beat_index: int | None) -> None:
        """Update beat selection display."""
        ...

    def show_operation_feedback(
        self, operation: str, message: str, duration: int = 3000
    ) -> None:
        """Show operation feedback to user."""
        ...


class IWorkbenchOperationService(Protocol):
    """Interface for workbench operations."""

    def execute_operation(self, operation_type: str, **kwargs) -> bool:
        """Execute a workbench operation."""
        ...

    def can_execute_operation(self, operation_type: str) -> bool:
        """Check if operation can be executed."""
        ...

    def get_available_operations(self) -> list[str]:
        """Get list of available operations."""
        ...
