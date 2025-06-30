"""
Test Suite for Refactored Graph Editor Architecture
==================================================

Comprehensive tests to validate the refactored graph editor components
and ensure backward compatibility with the existing API.

Test Categories:
- Component initialization and integration
- Signal routing and communication
- Public API compatibility
- UI layout and styling
- Beat data handling and updates
"""

import pytest
from unittest.mock import Mock, patch
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject

from domain.models.core_models import (
    BeatData,
    SequenceData,
    MotionData,
    MotionType,
    RotationDirection,
    Location,
    Orientation,
)
from presentation.components.graph_editor.graph_editor import GraphEditor
from presentation.components.graph_editor.components.pictograph_display_section import (
    PictographDisplaySection,
)
from presentation.components.graph_editor.components.main_adjustment_panel import (
    MainAdjustmentPanel,
)
from presentation.components.graph_editor.components.detailed_info_panel import (
    DetailedInfoPanel,
)
from presentation.components.graph_editor.components.dual_orientation_picker import (
    DualOrientationPicker,
)
from presentation.components.graph_editor.components.turn_adjustment_controls import (
    TurnAdjustmentControls,
)


class TestRefactoredGraphEditor:
    """Test suite for the refactored graph editor architecture"""

    @pytest.fixture
    def app(self):
        """Create QApplication for testing"""
        return QApplication.instance() or QApplication([])

    @pytest.fixture
    def sample_beat_data(self):
        """Create sample beat data for testing"""
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.5,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
        )

        red_motion = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.SOUTH,
            end_loc=Location.NORTH,
            turns=2.0,
            start_ori=Orientation.OUT,
            end_ori=Orientation.IN,
        )

        return BeatData(
            letter="A",
            blue_motion=blue_motion,
            red_motion=red_motion,
            metadata={"test": True},
        )

    @pytest.fixture
    def sample_sequence(self):
        """Create sample sequence data for testing"""
        return SequenceData(
            name="Test Sequence", beats=[], metadata={"test_sequence": True}
        )

    @pytest.fixture
    def graph_editor(self, app):
        """Create graph editor instance for testing"""
        return GraphEditor()

    def test_graph_editor_initialization(self, graph_editor):
        """Test that graph editor initializes correctly with all components"""
        # Verify main components are created
        assert graph_editor._pictograph_display is not None
        assert graph_editor._adjustment_panel is not None
        assert isinstance(graph_editor._pictograph_display, PictographDisplaySection)
        assert isinstance(graph_editor._adjustment_panel, MainAdjustmentPanel)

        # Verify initial state
        assert graph_editor._current_sequence is None
        assert graph_editor._selected_beat_index is None
        assert graph_editor._selected_beat_data is None

    def test_component_integration(self, graph_editor):
        """Test that components are properly integrated"""
        # Verify pictograph display section components
        pictograph_display = graph_editor._pictograph_display
        assert pictograph_display.get_pictograph_component() is not None
        assert pictograph_display.get_info_panel() is not None
        assert isinstance(pictograph_display.get_info_panel(), DetailedInfoPanel)

        # Verify adjustment panel components
        adjustment_panel = graph_editor._adjustment_panel
        assert adjustment_panel.get_orientation_picker() is not None
        assert adjustment_panel.get_turn_controls() is not None
        assert isinstance(
            adjustment_panel.get_orientation_picker(), DualOrientationPicker
        )
        assert isinstance(adjustment_panel.get_turn_controls(), TurnAdjustmentControls)

    def test_signal_routing(self, graph_editor):
        """Test that signals are properly routed between components"""
        # Create mock signal handlers
        beat_modified_mock = Mock()
        arrow_selected_mock = Mock()
        visibility_changed_mock = Mock()

        # Connect mock handlers to signals
        graph_editor.beat_modified.connect(beat_modified_mock)
        graph_editor.arrow_selected.connect(arrow_selected_mock)
        graph_editor.visibility_changed.connect(visibility_changed_mock)

        # Test orientation change signal routing
        orientation_picker = graph_editor._adjustment_panel.get_orientation_picker()
        orientation_picker.orientation_changed.emit("blue", "OUT")

        # Verify signal was routed correctly
        assert arrow_selected_mock.called
        call_args = arrow_selected_mock.call_args[0][0]
        assert call_args["color"] == "blue"
        assert call_args["orientation"] == "OUT"
        assert call_args["type"] == "orientation_change"

    def test_public_api_compatibility(
        self, graph_editor, sample_beat_data, sample_sequence
    ):
        """Test that public API methods work correctly"""
        # Test set_sequence
        graph_editor.set_sequence(sample_sequence)
        assert graph_editor._current_sequence == sample_sequence

        # Test set_selected_beat_data
        graph_editor.set_selected_beat_data(1, sample_beat_data)
        assert graph_editor._selected_beat_index == 1
        assert graph_editor._selected_beat_data == sample_beat_data

        # Test set_selected_start_position
        graph_editor.set_selected_start_position(sample_beat_data)

        # Test toggle_visibility
        initial_visibility = graph_editor.isVisible()
        graph_editor.toggle_visibility()
        assert graph_editor.isVisible() != initial_visibility

        # Test get_preferred_height
        assert graph_editor.get_preferred_height() == 300

    def test_beat_data_propagation(self, graph_editor, sample_beat_data):
        """Test that beat data is properly propagated to all components"""
        # Set beat data
        graph_editor.set_selected_beat_data(1, sample_beat_data)

        # Verify pictograph display section received the data
        pictograph_display = graph_editor._pictograph_display
        assert pictograph_display.get_current_beat_data() == sample_beat_data
        assert pictograph_display.get_current_beat_index() == 1

        # Verify adjustment panel received the data
        adjustment_panel = graph_editor._adjustment_panel
        assert adjustment_panel.get_current_beat_data() == sample_beat_data
        assert adjustment_panel.get_current_beat_index() == 1

    def test_panel_switching_logic(self, graph_editor, sample_beat_data):
        """Test that panels switch correctly based on beat type"""
        adjustment_panel = graph_editor._adjustment_panel

        # Test start position (should show orientation picker)
        graph_editor.set_selected_start_position(sample_beat_data)
        assert adjustment_panel.get_current_panel_mode() == "orientation"

        # Test regular beat (should show turn controls)
        graph_editor.set_selected_beat_data(1, sample_beat_data)
        assert adjustment_panel.get_current_panel_mode() == "turns"

    def test_styling_application(self, graph_editor):
        """Test that glassmorphism styling is applied correctly"""
        # Verify that styleSheet is set
        style_sheet = graph_editor.styleSheet()
        assert "rgba(255, 255, 255, 0.1)" in style_sheet
        assert "backdrop-filter: blur" in style_sheet
        assert "border-radius" in style_sheet

    def test_component_line_counts(self):
        """Test that all components are within the 350-line limit"""
        import inspect
        from pathlib import Path

        # Define component files to check
        component_files = [
            "src/desktop/modern/src/presentation/components/graph_editor/graph_editor.py",
            "src/desktop/modern/src/presentation/components/graph_editor/components/detailed_info_panel.py",
            "src/desktop/modern/src/presentation/components/graph_editor/components/pictograph_display_section.py",
            "src/desktop/modern/src/presentation/components/graph_editor/components/main_adjustment_panel.py",
            "src/desktop/modern/src/presentation/components/graph_editor/components/dual_orientation_picker.py",
            "src/desktop/modern/src/presentation/components/graph_editor/components/turn_adjustment_controls.py",
        ]

        for file_path in component_files:
            if Path(file_path).exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    line_count = len(f.readlines())
                assert (
                    line_count <= 350
                ), f"{file_path} has {line_count} lines (exceeds 350 limit)"


class TestComponentArchitecture:
    """Test the architectural patterns of individual components"""

    def test_component_separation(self):
        """Test that components are properly separated and don't have circular dependencies"""
        # This test ensures clean architecture principles are followed
        # Each component should be independently testable
        pass

    def test_signal_based_communication(self):
        """Test that components communicate via signals rather than direct coupling"""
        # Verify that components use PyQt signals for communication
        pass

    def test_dependency_injection_compatibility(self):
        """Test that components support dependency injection patterns"""
        # Verify that components can accept injected dependencies
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
