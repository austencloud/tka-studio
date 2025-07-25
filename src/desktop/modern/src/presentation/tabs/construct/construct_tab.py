from typing import TYPE_CHECKING, Optional

from application.services.ui.coordination.ui_coordinator import UICoordinator
from core.dependency_injection.di_container import DIContainer
from core.interfaces.workbench_services import IWorkbenchStateManager
from domain.models.beat_data import BeatData
from domain.models.sequence_data import SequenceData
from presentation.adapters.qt.sequence_beat_operations_adapter import (
    QtSequenceBeatOperationsAdapter,
)

# Import IMPROVED adapters that use IWorkbenchStateManager
from presentation.adapters.qt.sequence_loader_adapter import QtSequenceLoaderAdapter
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QWidget

from ...components.option_picker.option_picker_manager import OptionPickerManager
from ...components.start_position_picker.start_position_selection_handler import (
    StartPositionSelectionHandler,
)

# Import refactored components
from .layout_manager import ConstructTabLayoutManager
from .signal_coordinator import SignalCoordinator

# DataConversionService moved to application layer and imported above


if TYPE_CHECKING:
    pass


class ConstructTab(QWidget):
    """
    IMPROVED ConstructTabWidget using clean dependency injection with IWorkbenchStateManager.

    ✅ ELIMINATED: Clumsy workbench_getter/workbench_setter pattern
    ✅ IMPLEMENTED: Clean dependency injection with IWorkbenchStateManager
    ✅ ACHIEVED: Type-safe interfaces, better testability, loose coupling

    This streamlined version coordinates between specialized services:
    - LayoutManager: Handles UI layout and panel creation
    - StartPositionHandler: Manages start position selection
    - OptionPickerManager: Handles option picker operations
    - QtSequenceLoaderAdapter: IMPROVED - Uses IWorkbenchStateManager
    - QtSequenceBeatOperationsAdapter: IMPROVED - Uses IWorkbenchStateManager
    - SequenceStartPositionManager: TODO - Still uses old pattern temporarily
    - SignalCoordinator: Coordinates signals between components

    ARCHITECTURE BENEFITS:
    - 🎯 Type Safety: Interfaces instead of lambda functions
    - 🧪 Better Testability: Easy to mock IWorkbenchStateManager
    - 🔗 Loose Coupling: Services depend on interfaces, not implementations
    - 📝 Maintainability: Clear, readable dependency injection
    - 🚀 Extensibility: Easy to add new features
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

        # Flag to prevent signal emissions during startup
        self._startup_loading = True

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

        # Enable signals after initialization is complete
        self._startup_loading = False

    def _initialize_components(self):
        """Initialize all services using IMPROVED dependency injection - NO MORE CLUMSY GETTER/SETTER!"""

        # Get workbench state manager from container (CLEAN PATTERN!)
        from application.services.data.legacy_to_modern_converter import (
            LegacyToModernConverter,
        )
        from application.services.sequence.sequence_start_position_manager import (
            SequenceStartPositionManager,
        )

        workbench_state_manager = self.container.resolve(IWorkbenchStateManager)
        legacy_to_modern_converter = self.container.resolve(LegacyToModernConverter)

        # Initialize services with clean dependency injection
        self.loading_service = QtSequenceLoaderAdapter(
            workbench_state_manager=workbench_state_manager,
            legacy_to_modern_converter=legacy_to_modern_converter,
        )

        self.beat_operations = QtSequenceBeatOperationsAdapter(
            workbench_state_manager=workbench_state_manager,
        )

        # SequenceStartPositionManager now uses IWorkbenchStateManager too!
        self.start_position_manager = SequenceStartPositionManager(
            workbench_state_manager=workbench_state_manager,
        )

        # Layout manager
        self.layout_manager = ConstructTabLayoutManager(
            self.container, self.progress_callback, self._on_option_picker_ready
        )

        # Window resize coordinator for pictograph re-scaling
        from application.services.ui.window_resize_coordinator import (
            WindowResizeCoordinator,
        )

        self.resize_coordinator = self.container.resolve(WindowResizeCoordinator)

        # MODERN ARCHITECTURE: StartPositionSelectionHandler uses state manager pattern
        # Signal flow: handler -> SignalCoordinator -> StartPositionManager -> WorkbenchStateManager
        self.start_position_handler = StartPositionSelectionHandler()

        # Option picker manager (will be initialized after layout)
        self.option_picker_manager = None

        # Signal coordinator (will be initialized after all components)
        self.signal_coordinator = None

        # Connect service signals directly
        self._connect_service_signals()

    def _connect_service_signals(self):
        """Connect service signals directly to our signals."""

        # Loading service signals (Qt adapter provides Qt signals)
        self.loading_service.sequence_loaded.connect(self._on_sequence_loaded)
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
    def _on_sequence_loaded(self, sequence_data):
        """Handle sequence loaded - only emit signal if not during startup."""
        if not self._startup_loading:
            self.sequence_modified.emit(sequence_data)

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
        # Note: option_picker will be None initially due to deferred creation
        self.option_picker_manager = OptionPickerManager(
            self.layout_manager.option_picker
        )

        # MODERN ARCHITECTURE: No need to connect workbench setter
        # StartPositionSelectionHandler emits signals -> SignalCoordinator -> StartPositionManager -> WorkbenchStateManager

        # Initialize signal coordinator after all components are ready
        self.signal_coordinator = SignalCoordinator(
            self.layout_manager,
            self.start_position_handler,
            self.option_picker_manager,
            self.loading_service,
            self.beat_operations,
            self.start_position_manager,
        )

        # Connect signal coordinator to construct tab signals
        self.signal_coordinator.connect_construct_tab_signals(self)

        # Connect generation signals
        self._connect_generation_signals()

        # PERFORMANCE OPTIMIZATION: Defer sequence loading to after UI is fully ready
        # This reduces construct tab initialization time
        self._schedule_deferred_sequence_loading()

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

    def _connect_generation_signals(self):
        """Connect generation signals from the layout manager's component connector."""
        if hasattr(self.layout_manager, "component_connector"):
            self.layout_manager.component_connector.generate_requested.connect(
                self._on_generate_requested
            )

    def _on_generate_requested(self, generation_config):
        """Handle generation request and create sequence."""
        try:
            print(
                f"🤖 [CONSTRUCT_TAB] Handling generation request: {generation_config}"
            )

            # Get the sequence generator service
            from application.services.sequence.sequence_generator import (
                SequenceGenerator,
                SequenceType,
            )

            generator = SequenceGenerator()

            # Determine sequence type from config
            sequence_type = (
                SequenceType.FREEFORM
                if generation_config.mode.value == "freeform"
                else SequenceType.CIRCULAR
            )

            # Generate the sequence
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

            # Set the generated sequence in the workbench
            workbench_state_manager = self.container.resolve(IWorkbenchStateManager)
            if workbench_state_manager:
                workbench_state_manager.set_sequence(generated_sequence)
                print(
                    f"✅ [CONSTRUCT_TAB] Generated sequence with {len(generated_sequence.beats)} beats"
                )

                # Emit sequence created signal
                self.sequence_created.emit(generated_sequence)
            else:
                print("❌ [CONSTRUCT_TAB] No workbench state manager available")

        except Exception as e:
            print(f"❌ [CONSTRUCT_TAB] Generation failed: {e}")
            import traceback

            traceback.print_exc()

    # Public interface methods
    def clear_sequence(self):
        """Clear the current sequence and reset to start position picker using IMPROVED architecture"""
        try:
            print("✅ [CONSTRUCT_TAB] Clearing sequence using IMPROVED architecture")

            # Clear persistence FIRST
            from application.services.sequence.sequence_persister import (
                SequencePersister,
            )

            persistence_service = SequencePersister()
            persistence_service.clear_current_sequence()

            # Clear start position FIRST (before setting empty sequence)
            # This prevents signal coordinator from seeing stale start position data
            self.start_position_manager.clear_start_position()

            # Clear sequence using workbench state manager (CLEAN PATTERN!)
            workbench_state_manager = self.container.resolve(IWorkbenchStateManager)
            if workbench_state_manager:
                empty_sequence = SequenceData.empty()
                workbench_state_manager.set_sequence(empty_sequence)
                print("✅ [CONSTRUCT_TAB] Sequence cleared via state manager!")
            else:
                print("❌ [CONSTRUCT_TAB] No workbench state manager available")

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

    # Direct service access methods for external use - USING IMPROVED ARCHITECTURE
    def add_beat_to_sequence(self, beat_data: BeatData):
        """Add beat directly via IMPROVED beat operations adapter."""
        print("✅ [CONSTRUCT_TAB] Adding beat using IMPROVED beat operations adapter")
        # Note: The beat operations adapter now handles workbench state internally
        # No need for clumsy getter/setter pattern!
        # TODO: Implement add_beat_to_sequence in the adapter
        print(
            "⚠️ [CONSTRUCT_TAB] add_beat_to_sequence needs to be implemented in adapter"
        )

    def set_start_position(self, start_position_data: BeatData):
        """Set start position directly via start position manager."""
        print("✅ [CONSTRUCT_TAB] Setting start position using start position manager")
        self.start_position_manager.set_start_position(start_position_data)

    def get_current_sequence(self) -> Optional[SequenceData]:
        """Get current sequence directly via IMPROVED loading service."""
        print(
            "✅ [CONSTRUCT_TAB] Getting current sequence using IMPROVED loading service"
        )
        return self.loading_service.get_current_sequence_from_workbench()

    def update_beat_turns(self, beat_index: int, color: str, new_turns: int):
        """Update beat turns directly via IMPROVED beat operations adapter."""
        print("✅ [CONSTRUCT_TAB] Updating beat turns using IMPROVED adapter")
        # TODO: Implement update_beat_turns in the adapter
        print("⚠️ [CONSTRUCT_TAB] update_beat_turns needs to be implemented in adapter")

    def update_beat_orientation(
        self, beat_index: int, color: str, new_orientation: int
    ):
        """Update beat orientation directly via IMPROVED beat operations adapter."""
        print("✅ [CONSTRUCT_TAB] Updating beat orientation using IMPROVED adapter")
        # TODO: Implement update_beat_orientation in the adapter
        print(
            "⚠️ [CONSTRUCT_TAB] update_beat_orientation needs to be implemented in adapter"
        )

    def _schedule_deferred_sequence_loading(self):
        """Schedule sequence loading to happen after UI is fully ready - PERFORMANCE OPTIMIZED"""
        try:
            # PERFORMANCE OPTIMIZATION: Use longer delay to ensure main window is fully loaded
            # This prevents sequence loading from blocking the startup process
            from PyQt6.QtCore import QTimer

            # Defer sequence loading by 1 second to let startup complete
            QTimer.singleShot(1000, self._perform_sequence_load)

        except Exception as e:
            print(f"❌ [CONSTRUCT_TAB] Failed to setup deferred sequence loading: {e}")

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

    def _on_option_picker_ready(self, option_picker):
        """Handle option picker ready event from layout manager."""

        if self.option_picker_manager:
            self.option_picker_manager.set_option_picker(option_picker)
        else:
            print(f"❌ [CONSTRUCT_TAB] Option picker manager not initialized yet")

    # ============================================================================
    # ARCHITECTURE IMPROVEMENT COMPLETE! 🎉
    # ============================================================================
    #
    # ✅ ACCOMPLISHED: The clumsy workbench_getter/workbench_setter pattern
    #                  has been COMPLETELY ELIMINATED!
    #
    # 🔧 UPDATED SERVICES:
    #    - QtSequenceLoaderAdapter: Uses IWorkbenchStateManager ✅
    #    - QtSequenceBeatOperationsAdapter: Uses IWorkbenchStateManager ✅
    #    - SequenceStartPositionManager: Uses IWorkbenchStateManager ✅
    #    - clear_sequence(): Uses workbench_state_manager directly ✅
    #    - Service instantiation: Clean dependency injection ✅
    #    - Removed temporary getter/setter functions ✅
    #
    # ⚠️ REMAINING TODO:
    #    - StartPositionSelectionHandler: Needs updating (minor)
    #    - Some beat operations adapter methods need implementation
    #
    # 🎉 BENEFITS ACHIEVED:
    #    - Type-safe dependencies instead of lambda functions
    #    - Easier testing with mockable interfaces
    #    - Loose coupling between services and workbench

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle window resize events to trigger pictograph re-scaling."""
        super().resizeEvent(event)

        # Get the main window width
        main_window = self.window()
        if main_window and hasattr(self, "resize_coordinator"):
            new_width = main_window.width()

            # Notify the resize coordinator
            self.resize_coordinator.notify_window_resize(new_width)

            print(
                f"🔧 [CONSTRUCT_TAB] Window resized to {new_width}px, notified resize coordinator"
            )


#    - Clean, maintainable dependency injection
#    - Better error handling and debugging
#    - Significantly simplified architecture
#
# The clumsy getter/setter pattern has been ELIMINATED! 🚀
# ============================================================================
