"""
ConstructTab Controller - BUSINESS LOGIC COORDINATION

Extracted from the 22KB ConstructTab god object.
Handles all business logic, service coordination, and state management.

RESPONSIBILITIES:
- Service orchestration and dependency management
- Business logic for sequence operations
- Signal coordination between services
- State management and lifecycle
- Progress reporting coordination

DOES NOT HANDLE:
- Qt widget creation or management (that's the view)
- UI layout or styling (that's the view)
- Direct user interaction (that's the view)
"""

from typing import Optional

from PyQt6.QtCore import QObject, QTimer, pyqtSignal

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.workbench_services import IWorkbenchStateManager
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData


class ConstructTabController(QObject):
    """
    FOCUSED controller for construct tab business logic.

    Extracted from ConstructTab god object to separate concerns.
    Handles service coordination without UI responsibilities.
    """

    # Signals for communicating with the widget
    sequence_created = pyqtSignal(object)
    sequence_modified = pyqtSignal(object)
    start_position_set = pyqtSignal(str)
    start_position_loaded_from_persistence = pyqtSignal(str, object)

    def __init__(self, container: DIContainer, progress_callback=None):
        super().__init__()
        self._container = container
        self._progress_callback = progress_callback
        self._startup_loading = True

        # Services will be initialized in initialize()
        self._workbench_state_manager = None
        self._loading_service = None
        self._beat_operations = None
        self._start_position_manager = None
        self._resize_coordinator = None
        self._option_picker = None
        self._option_picker_manager = None
        self._signal_coordinator = None

    def initialize(self, view, widget) -> None:
        """
        Initialize the controller with view and widget references.

        SIMPLIFIED: Single initialization method instead of complex choreography.
        """
        try:
            self._view = view
            self._widget = widget

            if self._progress_callback:
                self._progress_callback(84, "Initializing construct tab controller...")

            # Initialize services
            self._initialize_services()

            if self._progress_callback:
                self._progress_callback(86, "Setting up business logic...")

            # Connect service signals
            self._connect_service_signals()

            # Create signal coordinator early (before option picker is ready)
            self._create_signal_coordinator_early()

            if self._progress_callback:
                self._progress_callback(88, "Starting sequence loading...")

            # Load sequence after short delay
            QTimer.singleShot(100, self._load_sequence_on_startup)

            # Enable signal processing
            self._startup_loading = False

        except Exception as e:
            print(f"❌ Controller initialization failed: {e}")

    def _initialize_services(self) -> None:
        """Initialize business services - FOCUSED on business logic only."""

        # Core state management
        self._workbench_state_manager = self._container.resolve(IWorkbenchStateManager)

        # Sequence operations
        from desktop.modern.application.services.sequence.sequence_start_position_manager import (
            SequenceStartPositionManager,
        )
        from desktop.modern.presentation.adapters.qt.sequence_beat_operations_adapter import (
            QtSequenceBeatOperationsAdapter,
        )
        from desktop.modern.presentation.adapters.qt.sequence_loader_adapter import (
            QtSequenceLoaderAdapter,
        )
        from shared.application.services.data.legacy_to_modern_converter import (
            LegacyToModernConverter,
        )

        legacy_converter = self._container.resolve(LegacyToModernConverter)

        self._loading_service = QtSequenceLoaderAdapter(
            workbench_state_manager=self._workbench_state_manager,
            legacy_to_modern_converter=legacy_converter,
        )

        self._beat_operations = QtSequenceBeatOperationsAdapter(
            workbench_state_manager=self._workbench_state_manager,
        )

        self._start_position_manager = SequenceStartPositionManager(
            workbench_state_manager=self._workbench_state_manager,
        )

        # Window resize handling
        from desktop.modern.application.services.ui.window_resize_coordinator import (
            WindowResizeCoordinator,
        )

        self._resize_coordinator = self._container.resolve(WindowResizeCoordinator)

    def _connect_service_signals(self) -> None:
        """Connect service signals to controller signals."""

        # Loading service signals
        self._loading_service.sequence_loaded.connect(self._on_sequence_loaded)
        self._loading_service.start_position_loaded.connect(
            self._on_start_position_loaded
        )

        # Beat operations signals
        self._beat_operations.beat_added.connect(self._on_beat_modified)
        self._beat_operations.beat_removed.connect(self._on_beat_modified)
        self._beat_operations.beat_updated.connect(self._on_beat_modified)

        # Start position signals
        self._start_position_manager.start_position_set.connect(
            self._on_start_position_set
        )
        self._start_position_manager.start_position_updated.connect(
            self._on_start_position_updated
        )

    # ============================================================================
    # SIGNAL HANDLERS - Business logic only
    # ============================================================================

    def _on_sequence_loaded(self, sequence_data) -> None:
        """Handle sequence loaded from persistence."""
        if not self._startup_loading:
            self.sequence_modified.emit(sequence_data)

    def _on_start_position_loaded(
        self, start_position_data: BeatData, position_key: str
    ) -> None:
        """Handle start position loaded from persistence."""
        self.start_position_loaded_from_persistence.emit(
            position_key, start_position_data
        )

    def _on_beat_modified(self, *args) -> None:
        """Handle any beat modification - emit current sequence."""
        current_sequence = self._loading_service.get_current_sequence_from_workbench()
        if current_sequence:
            self.sequence_modified.emit(current_sequence)

    def _on_start_position_set(self, start_position_data: BeatData) -> None:
        """Handle start position set."""
        self.start_position_set.emit(start_position_data.letter)

    def _on_start_position_updated(self, start_position_data: BeatData) -> None:
        """Handle start position updated."""
        pass

    def _load_sequence_on_startup(self) -> None:
        """Load sequence from persistence on startup."""
        try:
            if self._loading_service:
                self._loading_service.load_sequence_on_startup()
        except Exception as e:
            print(f"❌ Failed to load sequence on startup: {e}")

    # ============================================================================
    # PUBLIC BUSINESS LOGIC API
    # ============================================================================

    def clear_sequence(self) -> None:
        """Clear the current sequence and reset state."""
        try:
            # Clear persistence
            from shared.application.services.sequence.sequence_persister import (
                SequencePersister,
            )

            persistence_service = SequencePersister()
            persistence_service.clear_current_sequence()

            # Clear start position first
            self._start_position_manager.clear_start_position()

            # Clear sequence via state manager
            if self._workbench_state_manager:
                empty_sequence = SequenceData.empty()
                self._workbench_state_manager.set_sequence(empty_sequence)

        except Exception as e:
            print(f"❌ Failed to clear sequence: {e}")

    def force_picker_update(self) -> None:
        """Force picker state update - delegate to view."""
        if hasattr(self._view, "force_picker_update"):
            self._view.force_picker_update()

    def add_beat_to_sequence(self, beat_data: BeatData) -> None:
        """Add beat to sequence via beat operations service."""
        # TODO: Implement in beat operations adapter
        pass

    def set_start_position(self, start_position_data: BeatData) -> None:
        """Set start position via start position manager."""
        self._start_position_manager.set_start_position(start_position_data)

    def get_current_sequence(self) -> Optional[SequenceData]:
        """Get current sequence from workbench state."""
        return self._loading_service.get_current_sequence_from_workbench()

    def update_beat_turns(self, beat_index: int, color: str, new_turns: int) -> None:
        """Update beat turns via beat operations service."""
        # TODO: Implement in beat operations adapter
        pass

    def update_beat_orientation(
        self, beat_index: int, color: str, new_orientation: int
    ) -> None:
        """Update beat orientation via beat operations service."""
        # TODO: Implement in beat operations adapter
        pass

    def handle_resize(self, event, main_window) -> None:
        """Handle window resize events."""
        if main_window and self._resize_coordinator:
            new_width = main_window.width()
            self._resize_coordinator.notify_window_resize(new_width)

    def get_workbench(self):
        """Get workbench reference - for backward compatibility."""
        if hasattr(self._view, "get_workbench"):
            return self._view.get_workbench()
        return None

    def handle_generation_request(self, generation_config) -> None:
        """Handle sequence generation request."""
        try:
            from shared.application.services.sequence.sequence_generator import (
                SequenceGenerator,
                SequenceType,
            )

            generator = SequenceGenerator()

            # Determine sequence type
            sequence_type = (
                SequenceType.FREEFORM
                if generation_config.mode.value == "freeform"
                else SequenceType.CIRCULAR
            )

            # Generate sequence
            generated_sequence = generator.generate_sequence(
                sequence_type=sequence_type,
                name=f"Generated_{sequence_type.value}",
                length=generation_config.length,
                level=generation_config.level,
                turn_intensity=generation_config.turn_intensity,
                prop_continuity=generation_config.prop_continuity,
                letter_types=getattr(generation_config, "letter_types", []),
                cap_type=getattr(generation_config, "cap_type", None),
            )

            # Set generated sequence
            if self._workbench_state_manager:
                self._workbench_state_manager.set_sequence(generated_sequence)
                self.sequence_created.emit(generated_sequence)

        except Exception as e:
            print(f"❌ Generation failed: {e}")

    def handle_option_picker_ready(self, option_picker) -> None:
        """Handle option picker ready event from layout manager."""
        try:
            # Store reference for potential future use
            self._option_picker = option_picker

            # Create OptionPickerManager now that we have the option picker
            self._create_option_picker_manager()

            # Create SignalCoordinator now that all components are ready
            self._create_signal_coordinator()

        except Exception as e:
            print(f"❌ Failed to handle option picker ready: {e}")
            import traceback

            traceback.print_exc()

    def _create_option_picker_manager(self) -> None:
        """Create OptionPickerManager with the ready option picker."""
        try:
            from desktop.modern.presentation.components.option_picker.option_picker_manager import (
                OptionPickerManager,
            )

            self._option_picker_manager = OptionPickerManager(self._option_picker)

        except Exception as e:
            print(f"❌ Failed to create OptionPickerManager: {e}")
            import traceback

            traceback.print_exc()

    def _create_signal_coordinator_early(self) -> None:
        """Create SignalCoordinator early, before option picker is ready."""
        try:
            from desktop.modern.presentation.components.start_position_picker.start_position_selection_handler import (
                StartPositionSelectionHandler,
            )
            from desktop.modern.presentation.tabs.construct.signal_coordinator import (
                SignalCoordinator,
            )

            # Create start position selection handler
            start_position_handler = StartPositionSelectionHandler()

            # Create a placeholder option picker manager for now
            # This will be replaced when the real option picker is ready
            self._option_picker_manager = None

            # Create signal coordinator with available dependencies
            self._signal_coordinator = SignalCoordinator(
                layout_manager=self._view._layout_manager,
                start_position_handler=start_position_handler,
                option_picker_manager=self._option_picker_manager,  # Will be None initially
                loading_service=self._loading_service,
                beat_operations=self._beat_operations,
                start_position_manager=self._start_position_manager,
            )

            # Connect construct tab signals
            self._signal_coordinator.connect_construct_tab_signals(self._widget)

            print("✅ Signal coordinator created early")

        except Exception as e:
            print(f"❌ Failed to create early SignalCoordinator: {e}")
            import traceback

            traceback.print_exc()

    def _create_signal_coordinator(self) -> None:
        """Update SignalCoordinator with option picker manager when ready."""
        try:
            # If signal coordinator already exists, just update the option picker manager
            if self._signal_coordinator and self._option_picker_manager:
                self._signal_coordinator.set_option_picker_manager(
                    self._option_picker_manager
                )
                print("✅ Signal coordinator updated with option picker manager")
            else:
                # Fallback: create signal coordinator if it doesn't exist
                from desktop.modern.presentation.components.start_position_picker.start_position_selection_handler import (
                    StartPositionSelectionHandler,
                )
                from desktop.modern.presentation.tabs.construct.signal_coordinator import (
                    SignalCoordinator,
                )

                # Create start position selection handler
                start_position_handler = StartPositionSelectionHandler()

                # Create signal coordinator with all dependencies
                self._signal_coordinator = SignalCoordinator(
                    layout_manager=self._view._layout_manager,
                    start_position_handler=start_position_handler,
                    option_picker_manager=self._option_picker_manager,
                    loading_service=self._loading_service,
                    beat_operations=self._beat_operations,
                    start_position_manager=self._start_position_manager,
                )

                # Connect construct tab signals
                self._signal_coordinator.connect_construct_tab_signals(self._widget)

        except Exception as e:
            print(f"❌ Failed to update SignalCoordinator: {e}")
            import traceback

            traceback.print_exc()
