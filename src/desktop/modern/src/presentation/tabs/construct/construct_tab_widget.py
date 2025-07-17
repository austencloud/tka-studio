from typing import TYPE_CHECKING, Optional

from application.services.sequence.sequence_beat_operations import (
    SequenceBeatOperations,
)
from application.services.sequence.sequence_start_position_manager import (
    SequenceStartPositionManager,
)
from application.services.ui.coordination.ui_coordinator import UICoordinator
from core.dependency_injection.di_container import DIContainer
from domain.models.beat_data import BeatData
from domain.models.sequence_data import SequenceData

# Import services from application layer (moved from presentation)
from presentation.adapters.qt.sequence_loader_adapter import QtSequenceLoaderAdapter
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

# Import refactored components
from .layout_manager import ConstructTabLayoutManager
from .option_picker_manager import OptionPickerManager
from .signal_coordinator import SignalCoordinator
from .start_position_handler import StartPositionHandler

# DataConversionService moved to application layer and imported above


if TYPE_CHECKING:
    from presentation.components.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )


class ConstructTabWidget(QWidget):
    """
    Refactored ConstructTabWidget using direct service injection.

    This streamlined version coordinates between specialized services:
    - LayoutManager: Handles UI layout and panel creation
    - StartPositionHandler: Manages start position selection
    - OptionPickerManager: Handles option picker operations
    - SequenceLoadingService: Handles sequence loading from persistence
    - SequenceBeatOperations: Manages beat-level operations
    - SequenceStartPositionManager: Manages start position operations
    - SignalCoordinator: Coordinates signals between components
    - DataConversionService: Handles data conversions and caching
    """

    sequence_created = pyqtSignal(object)  # SequenceData object
    sequence_modified = pyqtSignal(object)  # SequenceData object
    start_position_set = pyqtSignal(
        str
    )  # Emits position key when start position is set
    start_position_loaded_from_persistence = pyqtSignal(
        str, object
    )  # position_key, BeatData

    def __init__(
        self,
        container: DIContainer,
        parent: Optional[QWidget] = None,
        progress_callback=None,
    ):
        super().__init__(parent)
        self.container = container
        self.progress_callback = progress_callback
        self.ui_coordinator = UICoordinator()

        # Report initialization start
        if self.progress_callback:
            self.progress_callback(84, "Initializing construct tab...")

        # Initialize component services
        self._initialize_components()

        # Report UI setup start
        if self.progress_callback:
            self.progress_callback(86, "Setting up UI components...")

        # Setup UI and connect signals
        self._setup_ui_with_progress()

        # Report signal connection
        if self.progress_callback:
            self.progress_callback(88, "Connecting signals...")

        self._connect_external_signals()

        # Report completion
        if self.progress_callback:
            self.progress_callback(90, "Construct tab ready")

    def _initialize_components(self):
        """Initialize all services directly via dependency injection"""

        # Get workbench references for services
        workbench_getter = self._get_workbench_getter()
        workbench_setter = self._get_workbench_setter()

        # Initialize sequence services directly
        self.loading_service = QtSequenceLoaderAdapter(
            workbench_getter=workbench_getter,
            workbench_setter=workbench_setter,
        )

        self.beat_operations = SequenceBeatOperations(
            workbench_getter=workbench_getter,
            workbench_setter=workbench_setter,
        )

        self.start_position_manager = SequenceStartPositionManager(
            workbench_getter=workbench_getter,
            workbench_setter=workbench_setter,
        )

        # Layout manager
        self.layout_manager = ConstructTabLayoutManager(
            self.container, self.progress_callback
        )

        self.start_position_handler = StartPositionHandler(
            workbench_setter=workbench_setter
        )

        # Option picker manager (will be initialized after layout)
        self.option_picker_manager = None

        # Signal coordinator (will be initialized after all components)
        self.signal_coordinator = None

        # Connect service signals directly
        self._connect_service_signals()

    def _connect_service_signals(self):
        """Connect service signals directly to our signals."""

        # Loading service signals
        self.loading_service.sequence_loaded.connect(self.sequence_modified.emit)
        self.loading_service.start_position_loaded.connect(
            self._on_start_position_loaded
        )

        # Beat operations signals
        self.beat_operations.beat_added.connect(self._on_beat_added)
        self.beat_operations.beat_removed.connect(self._on_beat_removed)
        self.beat_operations.beat_updated.connect(self._on_beat_updated)

        # Start position signals
        self.start_position_manager.start_position_set.connect(
            self._on_start_position_set
        )
        self.start_position_manager.start_position_updated.connect(
            self._on_start_position_updated
        )

    # Signal handlers (the real value that was in SequenceManager)
    def _on_start_position_loaded(
        self, start_position_data: BeatData, position_key: str
    ):
        """Handle start position loaded."""
        self.start_position_loaded_from_persistence.emit(
            position_key, start_position_data
        )

    def _on_beat_added(self, beat_data: BeatData, position: int):
        """Handle beat added."""
        current_sequence = self.loading_service.get_current_sequence_from_workbench()
        if current_sequence:
            self.sequence_modified.emit(current_sequence)

    def _on_beat_removed(self, position: int):
        """Handle beat removed."""
        current_sequence = self.loading_service.get_current_sequence_from_workbench()
        if current_sequence:
            self.sequence_modified.emit(current_sequence)

    def _on_beat_updated(self, beat_data: BeatData, position: int):
        """Handle beat updated."""
        current_sequence = self.loading_service.get_current_sequence_from_workbench()
        if current_sequence:
            self.sequence_modified.emit(current_sequence)

    def _on_start_position_set(self, start_position_data: BeatData):
        """Handle start position set."""
        print(f"🎯 Start position set: {start_position_data.letter}")
        self.start_position_set.emit(start_position_data.letter)

    def _on_start_position_updated(self, start_position_data: BeatData):
        """Handle start position updated."""
        print(f"🎯 Start position updated: {start_position_data.letter}")

    def _setup_ui_with_progress(self):
        """Setup UI using the layout manager"""
        # Delegate UI setup to layout manager
        self.layout_manager.setup_ui(self)

        # WINDOW MANAGEMENT FIX: Keep construct tab hidden during splash screen
        # It will be shown when the main window is displayed
        self.hide()
        self.setVisible(False)

        # Check construct tab visibility
        tab_visible = self.isVisible()
        parent_visible = self.parent().isVisible() if self.parent() else "No parent"

        # Initialize option picker manager after layout is created
        self.option_picker_manager = OptionPickerManager(
            self.layout_manager.option_picker
        )

        # Initialize signal coordinator after all components are ready
        self.signal_coordinator = SignalCoordinator(
            self.layout_manager,
            self.start_position_handler,
            self.option_picker_manager,
            self.loading_service,
            self.beat_operations,
            self.start_position_manager,
        )

        # Load sequence from current_sequence.json on startup if no session restoration
        # This mimics the legacy behavior of automatically loading the current sequence
        self._load_sequence_on_startup()

    def _connect_external_signals(self):
        """Connect external signals from the signal coordinator to this widget"""
        if (
            self.signal_coordinator
        ):  # Forward signals from signal coordinator to external listeners
            self.signal_coordinator.sequence_created.connect(self.sequence_created.emit)
            self.signal_coordinator.sequence_modified.connect(
                self.sequence_modified.emit
            )
            self.signal_coordinator.start_position_set.connect(
                self.start_position_set.emit
            )

            # NOTE: Workbench signals are already connected in signal_coordinator._setup_signal_connections()
            # No need for additional external connections here

    def _get_workbench_getter(self):
        """Get a function that returns the workbench"""

        def get_workbench():
            workbench = getattr(self.layout_manager, "workbench", None)
            if workbench is None:
                print("🚨 [WORKBENCH_GETTER] Layout manager has no workbench!")
                print(f"   Layout manager: {self.layout_manager}")
                print(
                    f"   Has workbench attr: {hasattr(self.layout_manager, 'workbench')}"
                )
            else:
                print(
                    f"✅ [WORKBENCH_GETTER] Workbench found: {type(workbench).__name__}"
                )
                if not hasattr(workbench, "get_sequence"):
                    print("🚨 [WORKBENCH_GETTER] Workbench has no get_sequence method!")
            return workbench

        return get_workbench

    def _get_workbench_setter(self):
        """Get a function that can set data on the workbench"""

        def set_workbench_data(data, pictograph_data=None):
            workbench: Optional[SequenceWorkbench] = getattr(
                self.layout_manager, "workbench", None
            )
            if workbench:
                if hasattr(data, "beats"):  # SequenceData
                    workbench.set_sequence(data)
                else:  # BeatData (start position)
                    # NEW: Pass both BeatData and optional PictographData
                    workbench.set_start_position(data, pictograph_data)

        return set_workbench_data

    # Public interface methods
    def clear_sequence(self):
        """Clear the current sequence and reset to start position picker"""
        try:

            # Clear persistence FIRST
            from application.services.sequence.sequence_persister import (
                SequencePersister,
            )

            persistence_service = SequencePersister()
            persistence_service.clear_current_sequence()

            # Clear start position FIRST (before setting empty sequence)
            # This prevents signal coordinator from seeing stale start position data
            self.start_position_manager.clear_start_position()

            # Clear sequence in workbench AFTER start position is cleared
            workbench_setter = self._get_workbench_setter()
            if workbench_setter:
                empty_sequence = SequenceData.empty()
                workbench_setter(empty_sequence)

            # NOTE: UI transition is handled automatically by signal coordinator
            # based on sequence state - no manual transition needed

        except Exception as e:
            print(f"❌ [CONSTRUCT_TAB] Failed to clear sequence: {e}")
            import traceback

            traceback.print_exc()

    def force_picker_update(self):
        """Force an update of the picker state based on current sequence state"""
        if self.signal_coordinator:
            self.signal_coordinator.force_picker_state_update()

    @property
    def workbench(self):
        """Access to the workbench component"""
        return getattr(self.layout_manager, "workbench", None)

    # Direct service access methods for external use
    def add_beat_to_sequence(self, beat_data: BeatData):
        """Add beat directly via beat operations service."""
        self.beat_operations.add_beat_to_sequence(beat_data)

    def set_start_position(self, start_position_data: BeatData):
        """Set start position directly via start position manager."""
        self.start_position_manager.set_start_position(start_position_data)

    def get_current_sequence(self) -> Optional[SequenceData]:
        """Get current sequence directly via loading service."""
        return self.loading_service.get_current_sequence_from_workbench()

    def update_beat_turns(self, beat_index: int, color: str, new_turns: int):
        """Update beat turns directly via beat operations service."""
        self.beat_operations.update_beat_turns(beat_index, color, new_turns)

    def update_beat_orientation(
        self, beat_index: int, color: str, new_orientation: int
    ):
        """Update beat orientation directly via beat operations service."""
        self.beat_operations.update_beat_orientation(beat_index, color, new_orientation)

    def _load_sequence_on_startup(self):
        """Load sequence from current_sequence.json on startup - exactly like legacy"""
        try:

            # Use a small delay to ensure UI is fully ready
            from PyQt6.QtCore import QTimer

            QTimer.singleShot(100, self._perform_sequence_load)

        except Exception as e:
            print(f"❌ [CONSTRUCT_TAB] Failed to setup sequence loading: {e}")

    def _perform_sequence_load(self):
        """Perform the actual sequence loading after UI is ready"""
        try:
            if self.loading_service:
                self.loading_service.load_sequence_on_startup()
            else:
                print("❌ [CONSTRUCT_TAB] No loading service available for loading")
        except Exception as e:
            print(f"❌ [CONSTRUCT_TAB] Failed to load sequence on startup: {e}")
