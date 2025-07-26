"""
ConstructTab - SIMPLIFIED UI WIDGET

The old ConstructTab was a 22KB god object handling 12+ responsibilities.
This version focuses ONLY on being a Qt widget with clean separation.

ELIMINATED:
- Complex service orchestration (moved to controller)
- Business logic (moved to controller) 
- Signal coordination (moved to controller)
- Progress reporting mixed with UI (separated)
- Manual dependency injection (simplified)
- Complex multi-phase initialization (linearized)

PROVIDES:
- Clean Qt widget with single responsibility
- Simple initialization without choreography
- Clear separation between UI and business logic
- Testable components
"""

from typing import Optional
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData

from .construct_tab_controller import ConstructTabController
from .construct_tab_view import ConstructTabView


class ConstructTab(QWidget):
    """
    SIMPLIFIED ConstructTab - Pure Qt widget with single responsibility.
    
    No longer a god object! Business logic moved to ConstructTabController.
    UI creation moved to ConstructTabView.
    
    This class now ONLY handles:
    - Qt widget lifecycle
    - Signal forwarding between view and controller
    - Public API for external interactions
    """

    # Public signals for external listeners
    sequence_created = pyqtSignal(object)  # SequenceData
    sequence_modified = pyqtSignal(object)  # SequenceData  
    start_position_set = pyqtSignal(str)   # position key
    start_position_loaded_from_persistence = pyqtSignal(str, object)  # key, BeatData

    def __init__(
        self,
        container: DIContainer,
        parent: Optional[QWidget] = None,
        progress_callback=None,
    ):
        """
        SIMPLIFIED initialization - no more complex choreography.
        """
        super().__init__(parent)
        
        # Create view (handles UI only)
        self._view = ConstructTabView(self)
        
        # Create controller (handles business logic)
        self._controller = ConstructTabController(container, progress_callback)
        
        # Setup the UI through the view
        self._view.setup_ui(
            container=container,
            progress_callback=progress_callback,
            option_picker_ready_callback=self._on_option_picker_ready
        )
        
        # Connect view and controller
        self._connect_view_controller()
        
        # Initialize the controller with view reference
        self._controller.initialize(self._view, self)
        
        # Hide during startup (will be shown by parent)
        self.hide()
        self.setVisible(False)

    def _on_option_picker_ready(self, option_picker):
        """Handle option picker ready callback from layout manager."""
        # Forward to controller for business logic handling
        if hasattr(self._controller, 'handle_option_picker_ready'):
            self._controller.handle_option_picker_ready(option_picker)

    def _connect_view_controller(self) -> None:
        """Connect view events to controller and controller events to external signals."""
        
        # Forward controller signals to our public signals
        self._controller.sequence_created.connect(self.sequence_created.emit)
        self._controller.sequence_modified.connect(self.sequence_modified.emit)
        self._controller.start_position_set.connect(self.start_position_set.emit)
        self._controller.start_position_loaded_from_persistence.connect(
            self.start_position_loaded_from_persistence.emit
        )

    # ============================================================================
    # PUBLIC API - Delegate to controller
    # ============================================================================

    def clear_sequence(self) -> None:
        """Clear the current sequence."""
        self._controller.clear_sequence()

    def force_picker_update(self) -> None:
        """Force an update of the picker state."""
        self._controller.force_picker_update()

    def add_beat_to_sequence(self, beat_data: BeatData) -> None:
        """Add beat to sequence."""
        self._controller.add_beat_to_sequence(beat_data)

    def set_start_position(self, start_position_data: BeatData) -> None:
        """Set start position."""
        self._controller.set_start_position(start_position_data)

    def get_current_sequence(self) -> Optional[SequenceData]:
        """Get current sequence."""
        return self._controller.get_current_sequence()

    def update_beat_turns(self, beat_index: int, color: str, new_turns: int) -> None:
        """Update beat turns."""
        self._controller.update_beat_turns(beat_index, color, new_turns)

    def update_beat_orientation(self, beat_index: int, color: str, new_orientation: int) -> None:
        """Update beat orientation."""
        self._controller.update_beat_orientation(beat_index, color, new_orientation)

    # ============================================================================
    # QT WIDGET EVENTS - Delegate to controller
    # ============================================================================

    def resizeEvent(self, event) -> None:
        """Handle resize events."""
        super().resizeEvent(event)
        self._controller.handle_resize(event, self.window())

    @property
    def workbench(self):
        """Access to workbench - for backward compatibility."""
        return self._controller.get_workbench()
