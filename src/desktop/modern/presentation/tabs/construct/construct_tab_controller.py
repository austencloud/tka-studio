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
    generation_completed = pyqtSignal(bool, str)  # success, error_message

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

    def set_start_position(self, start_position_data: BeatData) -> None:
        """Set start position via start position manager."""
        self._start_position_manager.set_start_position(start_position_data)

    def get_current_sequence(self) -> Optional[SequenceData]:
        """Get current sequence from workbench state."""
        return self._loading_service.get_current_sequence_from_workbench()

    def update_beat_turns(self, beat_index: int, color: str, new_turns: int) -> None:
        """Update beat turns via beat operations service."""
        # TODO: Implement in beat operations adapter

    def update_beat_orientation(
        self, beat_index: int, color: str, new_orientation: int
    ) -> None:
        """Update beat orientation via beat operations service."""
        # TODO: Implement in beat operations adapter

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
        """Handle sequence generation request using modern generation services."""
        try:
            print(
                f"🎯 [CONSTRUCT_TAB_CONTROLLER] ===== GENERATION REQUESTED ===== {generation_config.mode.value}"
            )
            print(
                f"🔍 [CONSTRUCT_TAB_CONTROLLER] RECEIVED LENGTH: {generation_config.length}"
            )
            print(
                "🔍 [CONSTRUCT_TAB_CONTROLLER] This is the REAL execution path from Generate button click"
            )

            # Get the unified modern generation service
            from desktop.modern.core.interfaces.generation_services import (
                IGenerationService,
            )

            generation_service = self._container.resolve(IGenerationService)
            if not generation_service:
                raise RuntimeError("Generation service not available")

            # Use the appropriate method based on mode
            if generation_config.mode.value == "freeform":
                result = generation_service.generate_freeform_sequence(
                    generation_config
                )
            elif generation_config.mode.value == "circular":
                result = generation_service.generate_circular_sequence(
                    generation_config
                )
            else:
                raise ValueError(
                    f"Unknown generation mode: {generation_config.mode.value}"
                )

            # Check result
            if not result or not result.success:
                error_msg = (
                    result.error_message
                    if result
                    else "Generation failed with no result"
                )
                raise RuntimeError(error_msg)

            print(
                f"✅ [CONSTRUCT_TAB_CONTROLLER] Modern generation successful: {len(result.sequence_data or [])} beats"
            )

            # CRITICAL FIX: Process generated sequence using legacy-style incremental approach
            if result.sequence_data:
                print(
                    f"🔧 [CONSTRUCT_TAB_CONTROLLER] Starting incremental beat processing (legacy-style): {len(result.sequence_data)} beats"
                )

                # Clear existing sequence first
                self._workbench_state_manager.set_sequence(None)

                # Import required modules
                from PyQt6.QtWidgets import QApplication

                from desktop.modern.domain.models.beat_data import BeatData

                # Process each pictograph individually like legacy system
                for i, pictograph_data in enumerate(result.sequence_data):
                    print(
                        f"� [CONSTRUCT_TAB_CONTROLLER] Processing beat {i + 1}/{len(result.sequence_data)} incrementally"
                    )

                    # Apply arrow positioning to this individual pictograph
                    positioned_pictograph_data = (
                        self._apply_arrow_positioning_to_pictograph(pictograph_data)
                    )

                    # Create BeatData for this individual beat
                    beat_data = BeatData(
                        beat_number=i + 1,
                        pictograph_data=positioned_pictograph_data,
                    )

                    # Add this beat to the sequence incrementally (like legacy)
                    self._add_beat_to_sequence_incrementally(beat_data)

                    # Process UI events like legacy system for visual feedback
                    QApplication.processEvents()

                    print(
                        f"✅ [CONSTRUCT_TAB_CONTROLLER] Beat {i + 1} added incrementally with correct arrow positioning"
                    )

                print(
                    "✅ [CONSTRUCT_TAB_CONTROLLER] All beats processed incrementally using legacy-style approach"
                )

            # Notify generation completion
            self.generation_completed.emit(True, "")
            print("✅ Generation completed successfully using modern services")

        except Exception as e:
            print(f"❌ Generation failed: {e}")
            import traceback

            traceback.print_exc()
            # Notify generation failure
            self.generation_completed.emit(False, str(e))

    def _add_beat_to_sequence_incrementally(self, beat_data: BeatData) -> None:
        """
        Add a single beat to the sequence incrementally, following legacy pattern.

        This mimics the legacy approach where each beat is added individually
        and immediately visible in the UI, ensuring proper arrow positioning.
        """
        try:
            # Get current sequence or create empty one
            current_sequence = self._workbench_state_manager.get_current_sequence()

            if current_sequence is None:
                # Create new sequence with this beat
                import uuid

                from desktop.modern.domain.models.sequence_data import SequenceData

                new_sequence = SequenceData(
                    id=str(uuid.uuid4()),
                    name="Generated Sequence",
                    beats=[beat_data],
                    sequence_length=1,
                )
            else:
                # Add beat to existing sequence
                new_sequence = current_sequence.add_beat(beat_data)

            # Update workbench state with the new sequence
            self._workbench_state_manager.set_sequence(new_sequence)

            # Emit signal for UI updates (like legacy system)
            self.sequence_created.emit(new_sequence)

            print(
                f"🔧 [CONSTRUCT_TAB_CONTROLLER] Beat {beat_data.beat_number} added incrementally"
            )

        except Exception as e:
            print(
                f"❌ [CONSTRUCT_TAB_CONTROLLER] Failed to add beat incrementally: {e}"
            )
            raise

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
                construct_tab_controller=self,
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
                    construct_tab_controller=self,
                )

                # Connect construct tab signals
                self._signal_coordinator.connect_construct_tab_signals(self._widget)

        except Exception as e:
            print(f"❌ Failed to update SignalCoordinator: {e}")
            import traceback

            traceback.print_exc()

    def _apply_arrow_positioning_to_pictograph(self, pictograph_data):
        """
        Apply proper arrow positioning to a generated pictograph.

        This is the CRITICAL FIX that ensures generated sequences have correctly
        positioned arrows just like manually created sequences.
        """
        try:
            # DIRECT FIX: Create arrow positioning orchestrator directly
            print(
                f"🔧 [CONSTRUCT_TAB_CONTROLLER] Creating arrow positioning orchestrator directly for {pictograph_data.letter}"
            )

            from desktop.modern.application.services.positioning.arrows.orchestration.arrow_positioning_orchestrator import (
                ArrowPositioningOrchestrator,
            )
            from shared.application.services.positioning.arrows.calculation.arrow_location_calculator import (
                ArrowLocationCalculatorService,
            )
            from shared.application.services.positioning.arrows.calculation.arrow_rotation_calculator import (
                ArrowRotationCalculatorService,
            )
            from shared.application.services.positioning.arrows.coordinate_system.arrow_coordinate_system_service import (
                ArrowCoordinateSystemService,
            )
            from shared.application.services.positioning.arrows.orchestration.arrow_adjustment_calculator import (
                ArrowAdjustmentCalculator,
            )

            # Create dependencies directly
            coordinate_system = ArrowCoordinateSystemService()
            location_calculator = ArrowLocationCalculatorService()
            rotation_calculator = ArrowRotationCalculatorService()
            adjustment_calculator = ArrowAdjustmentCalculator()

            # Create orchestrator
            orchestrator = ArrowPositioningOrchestrator(
                location_calculator=location_calculator,
                rotation_calculator=rotation_calculator,
                adjustment_calculator=adjustment_calculator,
                coordinate_system=coordinate_system,
            )

            # Apply arrow positioning
            positioned_pictograph = orchestrator.calculate_all_arrow_positions(
                pictograph_data
            )
            print(
                f"✅ [CONSTRUCT_TAB_CONTROLLER] Applied direct arrow positioning to {pictograph_data.letter}"
            )
            return positioned_pictograph

        except Exception as e:
            print(
                f"❌ [CONSTRUCT_TAB_CONTROLLER] Direct arrow positioning failed for {pictograph_data.letter}: {e}"
            )
            import traceback

            traceback.print_exc()
            # Return original pictograph if positioning fails
            return pictograph_data

    def _apply_fallback_arrow_positioning(self, pictograph_data):
        """Fallback arrow positioning when DI container fails."""
        try:
            # Try to get services from DI container first
            from desktop.modern.core.dependency_injection.di_container import (
                get_container,
            )
            from desktop.modern.core.interfaces.positioning_services import (
                IArrowAdjustmentCalculator,
                IArrowCoordinateSystemService,
                IArrowLocationCalculator,
                IArrowPositioningOrchestrator,
                IArrowRotationCalculator,
            )

            container = get_container()

            # Try to resolve from container
            try:
                orchestrator = container.resolve(IArrowPositioningOrchestrator)
                positioned_pictograph = orchestrator.calculate_all_arrow_positions(
                    pictograph_data
                )
                print(
                    f"✅ [CONSTRUCT_TAB_CONTROLLER] Applied container arrow positioning to {pictograph_data.letter}"
                )
                return positioned_pictograph
            except Exception:
                # Fallback to manual creation
                location_calculator = container.resolve(IArrowLocationCalculator)
                rotation_calculator = container.resolve(IArrowRotationCalculator)
                adjustment_calculator = container.resolve(IArrowAdjustmentCalculator)
                coordinate_system = container.resolve(IArrowCoordinateSystemService)

                from desktop.modern.application.services.positioning.arrows.orchestration.arrow_positioning_orchestrator import (
                    ArrowPositioningOrchestrator,
                )

                orchestrator = ArrowPositioningOrchestrator(
                    location_calculator=location_calculator,
                    rotation_calculator=rotation_calculator,
                    adjustment_calculator=adjustment_calculator,
                    coordinate_system=coordinate_system,
                )

                positioned_pictograph = orchestrator.calculate_all_arrow_positions(
                    pictograph_data
                )
                print(
                    f"✅ [CONSTRUCT_TAB_CONTROLLER] Applied fallback arrow positioning to {pictograph_data.letter}"
                )
                return positioned_pictograph

        except Exception as e:
            print(
                f"❌ [CONSTRUCT_TAB_CONTROLLER] Fallback arrow positioning failed for {pictograph_data.letter}: {e}"
            )
            # Return original pictograph if all positioning fails
            return pictograph_data
