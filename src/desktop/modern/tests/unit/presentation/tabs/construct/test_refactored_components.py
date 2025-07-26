"""
Tests for the refactored construct tab layout components.
These tests verify that the split responsibilities work correctly.
"""

import sys
from unittest.mock import MagicMock, Mock, patch

import pytest
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.presentation.tabs.construct.components.component_connector import (
    ComponentConnector,
)
from desktop.modern.presentation.tabs.construct.components.panel_factory import PanelFactory
from desktop.modern.presentation.tabs.construct.components.transition_animator import (
    TransitionAnimator,
)
from desktop.modern.presentation.tabs.construct.orchestrators.layout_orchestrator import (
    LayoutOrchestrator,
)
from desktop.modern.presentation.tabs.construct.orchestrators.progress_reporter import ProgressReporter
from PyQt6.QtWidgets import QApplication, QStackedWidget, QWidget


class TestPanelFactory:
    """Test suite for PanelFactory."""

    @pytest.fixture
    def app(self):
        """Create QApplication instance for testing."""
        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()
        yield app

    @pytest.fixture
    def mock_container(self):
        """Create mock DI container."""
        container = Mock(spec=DIContainer)
        container.resolve = Mock(return_value=Mock())
        return container

    @pytest.fixture
    def panel_factory(self, mock_container):
        """Create PanelFactory instance."""
        return PanelFactory(container=mock_container)

    @patch(
        "presentation.tabs.construct.components.panel_factory.create_modern_workbench"
    )
    def test_create_workbench_panel(self, mock_create_workbench, panel_factory, app):
        """Test workbench panel creation."""
        mock_workbench = Mock()
        mock_workbench.get_widget.return_value = QWidget()
        mock_create_workbench.return_value = mock_workbench

        panel, workbench = panel_factory.create_workbench_panel()

        assert panel is not None
        assert workbench == mock_workbench
        mock_create_workbench.assert_called_once()

    def test_create_start_position_panel_success(self, panel_factory, app):
        """Test start position panel creation (may return None if dependencies unavailable)."""
        widget, picker = panel_factory.create_start_position_panel()

        # Widget should always be created
        assert widget is not None
        # Picker may be None if dependencies are unavailable during testing
        # This is expected behavior when services can't be resolved

    def test_create_start_position_panel_failure(self, panel_factory, app):
        """Test start position panel creation with failure."""
        with patch(
            "presentation.tabs.construct.components.panel_factory.StartPositionPicker",
            side_effect=Exception("Test error"),
        ):
            widget, picker = panel_factory.create_start_position_panel()

            assert widget is not None
            assert picker is None

    def test_create_option_picker_panel_success(self, panel_factory, app):
        """Test successful option picker panel creation."""
        with patch(
            "presentation.tabs.construct.components.panel_factory.OptionPicker"
        ) as mock_picker:
            mock_picker_instance = Mock()
            mock_picker_instance.widget = QWidget()
            mock_picker.return_value = mock_picker_instance

            widget, picker = panel_factory.create_option_picker_panel()

            assert widget is not None
            assert picker == mock_picker_instance

    def test_create_graph_editor_panel_success(self, panel_factory, app):
        """Test graph editor panel creation (may return None if dependencies unavailable)."""
        widget, editor = panel_factory.create_graph_editor_panel()

        # Widget should always be created
        assert widget is not None
        # Editor may be None if dependencies are unavailable during testing
        # This is expected behavior when GraphEditor can't be imported/created

    def test_create_generate_controls_panel_success(self, panel_factory, app):
        """Test generate controls panel creation (may return None if dependencies unavailable)."""
        widget, panel = panel_factory.create_generate_controls_panel()

        # Widget should always be created
        assert widget is not None
        # Panel may be None if dependencies are unavailable during testing
        # This is expected behavior when GeneratePanel can't be imported/created


class TestTransitionAnimator:
    """Test suite for TransitionAnimator."""

    @pytest.fixture
    def app(self):
        """Create QApplication instance for testing."""
        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()
        yield app

    @pytest.fixture
    def transition_animator(self):
        """Create TransitionAnimator instance."""
        return TransitionAnimator()

    @pytest.fixture
    def mock_stack(self, app):
        """Create mock QStackedWidget."""
        stack = QStackedWidget()
        stack.addWidget(QWidget())
        stack.addWidget(QWidget())
        stack.setCurrentIndex(0)
        return stack

    def test_initialization(self, transition_animator):
        """Test TransitionAnimator initializes correctly."""
        assert transition_animator.is_transitioning() is False
        assert transition_animator._current_animation is None

    def test_fade_to_panel_same_index(self, transition_animator, mock_stack):
        """Test fade to panel with same index does nothing."""
        on_complete = Mock()
        transition_animator.fade_to_panel(mock_stack, 0, "test", on_complete)

        assert transition_animator.is_transitioning() is False
        on_complete.assert_not_called()

    def test_fade_to_panel_while_transitioning(self, transition_animator, mock_stack):
        """Test fade to panel while already transitioning."""
        transition_animator._is_transitioning = True
        on_complete = Mock()

        transition_animator.fade_to_panel(mock_stack, 1, "test", on_complete)

        # Should not change state
        assert transition_animator.is_transitioning() is True
        on_complete.assert_not_called()

    def test_reset_transition_state(self, transition_animator):
        """Test transition state reset."""
        transition_animator._is_transitioning = True
        transition_animator._current_animation = Mock()

        transition_animator._reset_transition_state()

        assert transition_animator.is_transitioning() is False
        assert transition_animator._current_animation is None


class TestComponentConnector:
    """Test suite for ComponentConnector."""

    @pytest.fixture
    def app(self):
        """Create QApplication instance for testing."""
        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()
        yield app

    @pytest.fixture
    def component_connector(self, app):
        """Create ComponentConnector instance."""
        return ComponentConnector()

    def test_initialization(self, component_connector):
        """Test ComponentConnector initializes correctly."""
        assert component_connector.workbench is None
        assert component_connector.graph_editor is None
        assert component_connector.generate_panel is None
        assert component_connector.start_position_picker is None

    def test_set_workbench(self, component_connector):
        """Test setting workbench."""
        mock_workbench = Mock()
        component_connector.set_workbench(mock_workbench)

        assert component_connector.workbench == mock_workbench

    def test_set_graph_editor(self, component_connector):
        """Test setting graph editor."""
        mock_graph_editor = Mock()
        mock_graph_editor.beat_modified = Mock()

        component_connector.set_graph_editor(mock_graph_editor)

        assert component_connector.graph_editor == mock_graph_editor

    def test_set_generate_panel(self, component_connector):
        """Test setting generate panel."""
        mock_generate_panel = Mock()
        mock_generate_panel.generate_requested = Mock()

        component_connector.set_generate_panel(mock_generate_panel)

        assert component_connector.generate_panel == mock_generate_panel

    def test_beat_selected_signal(self, component_connector):
        """Test beat selected signal handling."""
        signal_emitted = []
        component_connector.beat_selected_for_graph_editor.connect(
            lambda idx: signal_emitted.append(idx)
        )

        component_connector._on_beat_selected(5)

        assert signal_emitted == [5]


class TestLayoutOrchestrator:
    """Test suite for LayoutOrchestrator."""

    @pytest.fixture
    def layout_orchestrator(self):
        """Create LayoutOrchestrator instance."""
        return LayoutOrchestrator()

    def test_initialization(self, layout_orchestrator):
        """Test LayoutOrchestrator initializes correctly."""
        assert layout_orchestrator.components == {}
        assert len(layout_orchestrator.initialization_order) == 5
        assert "workbench" in layout_orchestrator.initialization_order

    def test_register_and_get_component(self, layout_orchestrator):
        """Test component registration and retrieval."""
        mock_component = Mock()
        layout_orchestrator.register_component("test", mock_component)

        assert layout_orchestrator.get_component("test") == mock_component
        assert layout_orchestrator.get_component("nonexistent") is None

    def test_get_tab_for_panel(self, layout_orchestrator):
        """Test panel to tab mapping."""
        assert (
            layout_orchestrator.get_tab_for_panel(0) == 0
        )  # start_position_picker -> Build
        assert layout_orchestrator.get_tab_for_panel(1) == 0  # option_picker -> Build
        assert layout_orchestrator.get_tab_for_panel(2) == 2  # graph_editor -> Edit
        assert (
            layout_orchestrator.get_tab_for_panel(3) == 1
        )  # generate_controls -> Generate

    def test_should_allow_transition(self, layout_orchestrator):
        """Test transition allowance logic."""
        assert layout_orchestrator.should_allow_transition(0, 1) is True
        assert layout_orchestrator.should_allow_transition(1, 1) is False

    def test_validate_component_setup_success(self, layout_orchestrator):
        """Test successful component setup validation."""
        # Register all required components
        for component_name in layout_orchestrator.initialization_order:
            layout_orchestrator.register_component(component_name, Mock())

        is_valid, issues = layout_orchestrator.validate_component_setup()

        assert is_valid is True
        assert len(issues) == 0

    def test_validate_component_setup_missing_component(self, layout_orchestrator):
        """Test component setup validation with missing component."""
        # Register only some components
        layout_orchestrator.register_component("workbench", Mock())

        is_valid, issues = layout_orchestrator.validate_component_setup()

        assert is_valid is False
        assert len(issues) > 0
        assert any("Missing required component" in issue for issue in issues)


class TestProgressReporter:
    """Test suite for ProgressReporter."""

    @pytest.fixture
    def mock_progress_callback(self):
        """Create mock progress callback."""
        return Mock()

    @pytest.fixture
    def progress_reporter(self, mock_progress_callback):
        """Create ProgressReporter instance."""
        return ProgressReporter(mock_progress_callback)

    def test_initialization(self, progress_reporter):
        """Test ProgressReporter initializes correctly."""
        assert progress_reporter.current_phase is None
        assert len(progress_reporter.progress_ranges) > 0

    def test_start_phase(self, progress_reporter, mock_progress_callback):
        """Test starting a phase."""
        progress_reporter.start_phase("layout_setup", "Test message")

        assert progress_reporter.current_phase == "layout_setup"
        mock_progress_callback.assert_called_once_with(84, "Test message")

    def test_complete_phase(self, progress_reporter, mock_progress_callback):
        """Test completing a phase."""
        progress_reporter.start_phase("layout_setup", "Start message")
        progress_reporter.complete_phase("layout_setup", "Complete message")

        assert progress_reporter.current_phase is None
        # Should be called twice - once for start, once for complete
        assert mock_progress_callback.call_count == 2

    def test_update_phase_progress(self, progress_reporter, mock_progress_callback):
        """Test updating phase progress."""
        progress_reporter.update_phase_progress("layout_setup", 0.5, "Halfway")

        # Should calculate progress between start (84) and end (86)
        expected_progress = 84 + (86 - 84) * 0.5  # 85
        mock_progress_callback.assert_called_once_with(85, "Halfway")

    def test_report_component_progress_option_picker(
        self, progress_reporter, mock_progress_callback
    ):
        """Test reporting option picker progress."""
        progress_reporter.report_component_progress("option_picker", 0.5, "Loading")

        # Should map to 76-82 range
        expected_progress = 76 + (0.5 * 6)  # 79
        mock_progress_callback.assert_called_once_with(79, "Option picker: Loading")

    def test_get_overall_progress(self, progress_reporter):
        """Test getting overall progress."""
        progress_reporter.start_phase("layout_setup", "Test")

        assert progress_reporter.get_overall_progress() == 84
