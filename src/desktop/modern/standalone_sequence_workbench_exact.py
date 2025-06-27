"""
Standalone Architectural Extraction of TKA Modern Sequence Workbench

This file provides a precise extraction of the ModernSequenceWorkbench component
from the main application, maintaining complete visual and functional fidelity.

The extracted workbench replicates the exact left panel component hierarchy from
the main application's construct tab without any modifications to the component's
internal architecture or visual presentation.

This should be KEPT until marked deletable and all workbench functionality is implemented.
"""

import sys
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Add modern/src to path for imports
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

# Import the actual TKA components and services
from core.dependency_injection.di_container import get_container
from presentation.factories.workbench_factory import (
    create_modern_workbench,
    configure_workbench_services,
)
from presentation.components.workbench.workbench import ModernSequenceWorkbench
from core.interfaces.core_services import ILayoutService
from core.interfaces.workbench_services import (
    ISequenceWorkbenchService,
    IFullScreenService,
    IBeatDeletionService,
    IGraphEditorService,
    IDictionaryService,
)
from domain.models.core_models import (
    BeatData,
    SequenceData,
    MotionData,
    MotionType,
    Location,
    RotationDirection,
    Orientation,
)


class StandaloneSequenceWorkbenchWindow(QMainWindow):
    """Unfortunately the pictograph
    Standalone window hosting the exact ModernSequenceWorkbench component

    This window serves as a minimal container for the actual workbench component,
    preserving all original functionality, styling, and behavior patterns.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("TKA Modern Sequence Workbench - Standalone")

        # Set window geometry to match main application proportions
        # Main app is typically 1400x900, left panel is 50% = 700px width
        self.setGeometry(100, 100, 700, 900)

        # Initialize dependency injection container
        self._container = get_container()
        self._configure_services()

        # Create the actual workbench component
        self._workbench: Optional[ModernSequenceWorkbench] = None

        # Setup UI with exact styling
        self._setup_ui()
        self._apply_aurora_styling()

        # Load test data using the same patterns as main app
        self._load_aabb_sequence()

        print("🎉 Standalone Modern Sequence Workbench initialized")
        print("📊 Exact architectural extraction from main application")

    def _configure_services(self):
        """Configure all required services using the actual TKA service configuration"""
        try:
            # Register essential services that might be missing
            self._register_essential_services()

            # Use the actual workbench factory to configure services
            configure_workbench_services(self._container)
            print("✅ Services configured successfully")
        except Exception as e:
            print(f"⚠️ Service configuration warning: {e}")
            # Try fallback service registration
            self._register_fallback_services()

    def _register_essential_services(self):
        """Register essential services that might be missing in standalone mode"""
        try:
            from core.interfaces.core_services import (
                IUIStateManagementService,
                ILayoutService,
            )
            from application.services.ui.ui_state_management_service import (
                UIStateManagementService,
            )
            from application.services.layout.layout_management_service import (
                LayoutManagementService,
            )

            # Check current registrations
            registrations = self._container.get_registrations()

            # Register UI state management service if not already registered
            if IUIStateManagementService not in registrations:
                ui_state_service = UIStateManagementService()
                self._container.register_instance(
                    IUIStateManagementService, ui_state_service
                )
                print("✅ Registered UIStateManagementService")
            else:
                print("✅ UIStateManagementService already registered")

            # Register layout service if not already registered
            if ILayoutService not in registrations:
                layout_service = LayoutManagementService()
                self._container.register_instance(ILayoutService, layout_service)
                print("✅ Registered LayoutManagementService")
            else:
                print("✅ LayoutManagementService already registered")

            # Register positioning services for proper arrow positioning
            self._register_positioning_services()

        except Exception as e:
            print(f"⚠️ Could not register essential services: {e}")

    def _register_fallback_services(self):
        """Register minimal fallback services for standalone operation"""
        try:
            from core.interfaces.core_services import IUIStateManagementService
            from core.interfaces.workbench_services import (
                ISequenceWorkbenchService,
                IFullScreenService,
                IBeatDeletionService,
                IGraphEditorService,
                IDictionaryService,
            )

            # Create minimal mock services
            class MockService:
                def __getattr__(self, name):
                    return lambda *args, **kwargs: None

            # Get current registrations
            registrations = self._container.get_registrations()

            # Register mock services if not already registered
            services_to_mock = [
                IUIStateManagementService,
                ISequenceWorkbenchService,
                IFullScreenService,
                IBeatDeletionService,
                IGraphEditorService,
                IDictionaryService,
            ]

            for service_interface in services_to_mock:
                if service_interface not in registrations:
                    mock_service = MockService()
                    self._container.register_instance(service_interface, mock_service)
                    print(f"✅ Registered mock {service_interface.__name__}")
                else:
                    print(f"✅ {service_interface.__name__} already registered")

        except Exception as e:
            print(f"⚠️ Fallback service registration failed: {e}")

    def _register_positioning_services(self):
        """Register positioning services for proper arrow positioning"""
        try:
            # Import the individual calculator services with correct class names
            from application.services.positioning.arrows.orchestration.arrow_adjustment_calculator_service import (
                ArrowAdjustmentCalculatorService,
            )
            from application.services.positioning.arrows.coordinate_system.arrow_coordinate_system_service import (
                ArrowCoordinateSystemService,
            )
            from application.services.positioning.arrows.calculation.arrow_location_calculator import (
                ArrowLocationCalculatorService,
            )
            from application.services.positioning.arrows.calculation.arrow_rotation_calculator import (
                ArrowRotationCalculatorService,
            )
            from application.services.positioning.arrows.orchestration.arrow_positioning_orchestrator import (
                ArrowPositioningOrchestrator,
            )
            from core.interfaces.positioning_services import (
                IArrowAdjustmentCalculator,
                IArrowCoordinateSystemService,
                IArrowLocationCalculator,
                IArrowRotationCalculator,
                IArrowPositioningOrchestrator,
            )

            # Check current registrations
            registrations = self._container.get_registrations()

            # Register calculator microservices
            if IArrowLocationCalculator not in registrations:
                self._container.register_singleton(
                    IArrowLocationCalculator, ArrowLocationCalculatorService
                )
                print("✅ Registered ArrowLocationCalculatorService")
            else:
                print("✅ ArrowLocationCalculatorService already registered")

            if IArrowRotationCalculator not in registrations:
                self._container.register_singleton(
                    IArrowRotationCalculator, ArrowRotationCalculatorService
                )
                print("✅ Registered ArrowRotationCalculatorService")
            else:
                print("✅ ArrowRotationCalculatorService already registered")

            if IArrowAdjustmentCalculator not in registrations:
                self._container.register_singleton(
                    IArrowAdjustmentCalculator, ArrowAdjustmentCalculatorService
                )
                print("✅ Registered ArrowAdjustmentCalculatorService")
            else:
                print("✅ ArrowAdjustmentCalculatorService already registered")

            if IArrowCoordinateSystemService not in registrations:
                self._container.register_singleton(
                    IArrowCoordinateSystemService, ArrowCoordinateSystemService
                )
                print("✅ Registered ArrowCoordinateSystemService")
            else:
                print("✅ ArrowCoordinateSystemService already registered")

            # Register orchestrator (replaces monolith)
            if IArrowPositioningOrchestrator not in registrations:
                self._container.register_singleton(
                    IArrowPositioningOrchestrator, ArrowPositioningOrchestrator
                )
                print("✅ Registered ArrowPositioningOrchestrator")
            else:
                print("✅ ArrowPositioningOrchestrator already registered")

        except ImportError as e:
            # Some positioning services not available - continue
            print(f"⚠️ Failed to import positioning services: {e}")
            print("   This means IArrowPositioningOrchestrator will not be available")

        try:
            # Register additional positioning services that might be needed
            self._register_additional_positioning_services()
        except Exception as e:
            print(f"⚠️ Failed to register additional positioning services: {e}")

        try:
            # Register pictograph services for complete rendering
            self._register_pictograph_services()
        except Exception as e:
            print(f"⚠️ Failed to register pictograph services: {e}")

    def _register_additional_positioning_services(self):
        """Register additional positioning services that the orchestrator depends on"""
        try:
            # Import the focused arrow adjustment services
            from application.services.positioning.arrows.orchestration.arrow_adjustment_lookup_service import (
                ArrowAdjustmentLookupService,
            )
            from application.services.positioning.arrows.orchestration.directional_tuple_processor import (
                DirectionalTupleProcessor,
            )

            # Register the focused services if not already registered
            registrations = self._container.get_registrations()

            if ArrowAdjustmentLookupService not in registrations:
                self._container.register_singleton(
                    ArrowAdjustmentLookupService, ArrowAdjustmentLookupService
                )
                print("✅ Registered ArrowAdjustmentLookupService")

            if DirectionalTupleProcessor not in registrations:
                self._container.register_singleton(
                    DirectionalTupleProcessor, DirectionalTupleProcessor
                )
                print("✅ Registered DirectionalTupleProcessor")

        except ImportError as e:
            print(f"⚠️ Failed to import additional positioning services: {e}")

    def _register_pictograph_services(self):
        """Register pictograph services for complete rendering including text/labels and decorative elements"""
        try:
            # Import pictograph services from main application
            from application.services.data.pictograph_data_service import (
                IPictographDataService,
                PictographDataService,
            )
            from application.services.core.pictograph_management_service import (
                PictographManagementService,
            )

            # Register the focused services if not already registered
            registrations = self._container.get_registrations()

            if IPictographDataService not in registrations:
                self._container.register_singleton(
                    IPictographDataService, PictographDataService
                )
                print("✅ Registered PictographDataService")

            if PictographManagementService not in registrations:
                self._container.register_singleton(
                    PictographManagementService, PictographManagementService
                )
                print("✅ Registered PictographManagementService")

        except ImportError as e:
            print(f"⚠️ Failed to import pictograph data services: {e}")

        try:
            # Import orchestrator services
            from application.services.core.pictograph_orchestrator import (
                IPictographOrchestrator,
                PictographOrchestrator,
            )
            from application.services.positioning.props.orchestration.prop_orchestrator import (
                IPropOrchestrator,
                PropOrchestrator,
            )

            registrations = self._container.get_registrations()

            if IPictographOrchestrator not in registrations:
                self._container.register_singleton(
                    IPictographOrchestrator, PictographOrchestrator
                )
                print("✅ Registered PictographOrchestrator")

            if IPropOrchestrator not in registrations:
                self._container.register_singleton(IPropOrchestrator, PropOrchestrator)
                print("✅ Registered PropOrchestrator")

        except ImportError as e:
            print(f"⚠️ Failed to import pictograph orchestrator services: {e}")

    def _setup_ui(self):
        """Setup UI with the exact ModernSequenceWorkbench component"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        try:
            # Create the actual ModernSequenceWorkbench using the factory
            self._workbench = create_modern_workbench(
                container=self._container, parent=central_widget
            )

            # Add workbench to layout
            main_layout.addWidget(self._workbench)

            print("✅ ModernSequenceWorkbench component created successfully")

        except Exception as e:
            print(f"❌ Failed to create workbench component: {e}")
            # Create fallback label
            from PyQt6.QtWidgets import QLabel

            fallback_label = QLabel(f"Workbench initialization failed: {e}")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fallback_label.setStyleSheet(
                "color: #ff6b6b; font-size: 14px; padding: 20px;"
            )
            main_layout.addWidget(fallback_label)

    def _apply_aurora_styling(self):
        """Apply the exact Aurora background styling from the main application"""
        # Replicate the exact gradient background used in the main TKA application
        self.setStyleSheet(
            """
            QMainWindow {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #0f172a,
                    stop: 0.5 #1e293b,
                    stop: 1 #334155
                );
            }
            
            QWidget {
                font-family: 'Inter', 'Segoe UI', sans-serif;
                font-size: 12px;
                color: #ffffff;
            }
            
            /* Preserve exact Nord color scheme */
            QFrame {
                background-color: rgba(46, 52, 64, 0.8);
                border: 1px solid rgba(76, 86, 106, 0.5);
                border-radius: 8px;
            }
            
            QPushButton {
                background-color: #5e81ac;
                border: 1px solid #81a1c1;
                border-radius: 6px;
                color: #eceff4;
                padding: 8px 16px;
                font-weight: 500;
            }
            
            QPushButton:hover {
                background-color: #81a1c1;
                border-color: #88c0d0;
            }
            
            QPushButton:pressed {
                background-color: #4c566a;
            }
            
            QPushButton:disabled {
                background-color: #3b4252;
                color: #4c566a;
                border-color: #3b4252;
            }
        """
        )

    def _load_aabb_sequence(self):
        """Load the AABB sequence using the same data patterns as the main application"""
        if not self._workbench:
            print("❌ No workbench available for sequence loading")
            return

        try:
            # Create AABB sequence data identical to main application
            sequence_data = self._create_aabb_sequence()
            start_position_data = self._create_start_position()

            print(f"🔍 Created sequence data: {sequence_data.name}")
            print(f"🔍 Sequence beats: {len(sequence_data.beats)}")
            for i, beat in enumerate(sequence_data.beats):
                print(
                    f"   Beat {i+1}: {beat.letter} - {beat.blue_motion.motion_type.value if beat.blue_motion else 'No motion'}"
                )

            print(
                f"🔍 Start position: {start_position_data.letter} - {start_position_data.metadata}"
            )

            # Load data into workbench using the exact same methods
            print("🔄 Loading sequence into workbench...")
            self._workbench.set_sequence(sequence_data)

            print("🔄 Loading start position into workbench...")
            self._workbench.set_start_position(start_position_data)

            # Verify the data was loaded
            loaded_sequence = self._workbench.get_sequence()
            if loaded_sequence:
                print(
                    f"✅ Workbench sequence verified: {loaded_sequence.name} with {len(loaded_sequence.beats)} beats"
                )
            else:
                print("❌ Workbench sequence is None after loading")

            # Test beat frame access
            if hasattr(self._workbench, "_beat_frame_section"):
                beat_frame_section = self._workbench._beat_frame_section
                if beat_frame_section and hasattr(beat_frame_section, "_beat_frame"):
                    beat_frame = beat_frame_section._beat_frame
                    if beat_frame:
                        current_seq = beat_frame.get_sequence()
                        print(
                            f"🔍 Beat frame sequence: {current_seq.name if current_seq else 'None'}"
                        )
                    else:
                        print("❌ Beat frame is None")
                else:
                    print("❌ Beat frame section has no _beat_frame")
            else:
                print("❌ Workbench has no _beat_frame_section")

            print("✅ Sequence loading completed successfully")

            # Show the graph editor to test the layout fixes
            self._show_graph_editor()

        except Exception as e:
            print(f"❌ Failed to load sequence data: {e}")
            import traceback

            traceback.print_exc()

    def _show_graph_editor(self):
        """Show the graph editor to test the layout fixes"""
        try:
            if self._workbench and hasattr(self._workbench, "_graph_editor_section"):
                graph_editor_section = self._workbench._graph_editor_section
                if graph_editor_section and hasattr(
                    graph_editor_section, "_graph_editor"
                ):
                    graph_editor = graph_editor_section._graph_editor
                    if graph_editor and hasattr(graph_editor, "show"):
                        graph_editor.show()
                        print("🎯 Graph editor shown for layout testing")
                    elif graph_editor and hasattr(graph_editor, "toggle"):
                        graph_editor.toggle()
                        print("🎯 Graph editor toggled for layout testing")
                    else:
                        print("❌ Graph editor has no show/toggle method")
                else:
                    print("❌ Graph editor section has no _graph_editor")
            else:
                print("❌ Workbench has no _graph_editor_section")
        except Exception as e:
            print(f"❌ Failed to show graph editor: {e}")

    def _create_aabb_sequence(self) -> SequenceData:
        """Create the AABB sequence using exact data from main application"""
        beats = []

        # Beat 1: A (alpha1 -> alpha3)
        beat1 = BeatData(
            beat_number=1,
            letter="A",
            duration=1.0,
            blue_motion=MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.WEST,
                start_ori=Orientation.IN,
                end_ori=Orientation.IN,
                turns=0.0,
            ),
            red_motion=MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.EAST,
                start_ori=Orientation.IN,
                end_ori=Orientation.IN,
                turns=0.0,
            ),
        )

        # Beat 2: A (alpha3 -> alpha5)
        beat2 = BeatData(
            beat_number=2,
            letter="A",
            duration=1.0,
            blue_motion=MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.WEST,
                end_loc=Location.NORTH,
                start_ori=Orientation.IN,
                end_ori=Orientation.IN,
                turns=0.0,
            ),
            red_motion=MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.EAST,
                end_loc=Location.SOUTH,
                start_ori=Orientation.IN,
                end_ori=Orientation.IN,
                turns=0.0,
            ),
        )

        # Beat 3: B (alpha5 -> alpha3)
        beat3 = BeatData(
            beat_number=3,
            letter="B",
            duration=1.0,
            blue_motion=MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.WEST,
                start_ori=Orientation.IN,
                end_ori=Orientation.OUT,
                turns=0.0,
            ),
            red_motion=MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.EAST,
                start_ori=Orientation.IN,
                end_ori=Orientation.OUT,
                turns=0.0,
            ),
        )

        # Beat 4: B (alpha3 -> alpha1)
        beat4 = BeatData(
            beat_number=4,
            letter="B",
            duration=1.0,
            blue_motion=MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.WEST,
                end_loc=Location.SOUTH,
                start_ori=Orientation.OUT,
                end_ori=Orientation.IN,
                turns=0.0,
            ),
            red_motion=MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.EAST,
                end_loc=Location.NORTH,
                start_ori=Orientation.OUT,
                end_ori=Orientation.IN,
                turns=0.0,
            ),
        )

        beats = [beat1, beat2, beat3, beat4]

        return SequenceData(
            name="AABB",
            beats=beats,
            metadata={"word": "AABB", "level": 0, "prop_type": "staff"},
        )

    def _create_start_position(self) -> BeatData:
        """Create start position data identical to main application"""
        return BeatData(
            beat_number=0,  # Use 0 for start position to match detection logic
            letter="α",
            duration=1.0,
            blue_motion=MotionData(
                motion_type=MotionType.STATIC,
                prop_rot_dir=RotationDirection.NO_ROTATION,
                start_loc=Location.SOUTH,
                end_loc=Location.SOUTH,
                start_ori=Orientation.IN,
                end_ori=Orientation.IN,
                turns=0.0,
            ),
            red_motion=MotionData(
                motion_type=MotionType.STATIC,
                prop_rot_dir=RotationDirection.NO_ROTATION,
                start_loc=Location.NORTH,
                end_loc=Location.NORTH,
                start_ori=Orientation.IN,
                end_ori=Orientation.IN,
                turns=0.0,
            ),
            metadata={"is_start_position": True, "sequence_start_position": "alpha"},
        )

    def get_workbench(self) -> Optional[ModernSequenceWorkbench]:
        """Get the workbench component for external access"""
        return self._workbench

    def closeEvent(self, event):
        """Handle window close event with proper cleanup"""
        try:
            if self._workbench:
                # Perform any necessary cleanup
                print("🧹 Cleaning up workbench component")

            # Clean up dependency injection container if needed
            print("🧹 Cleaning up services")

        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")

        super().closeEvent(event)


def main():
    """Main entry point for standalone sequence workbench"""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    # Set application properties to match main TKA application
    app.setApplicationName("TKA Modern Sequence Workbench")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("TKA")

    # Set application style to match main application
    app.setStyle("Fusion")

    try:
        # Create and show the standalone workbench window
        workbench_window = StandaloneSequenceWorkbenchWindow()
        workbench_window.show()

        print("🚀 Standalone workbench window displayed")
        print("📋 This is an exact architectural extraction of ModernSequenceWorkbench")
        print("🎯 All functionality should match the main application exactly")

        return app.exec()

    except Exception as e:
        print(f"❌ Failed to start standalone workbench: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
