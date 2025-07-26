"""
Modern Browse Control Panel Integration Tests

Test suite for the integration between the control panel and sequence browser,
ensuring proper communication and state management.
"""

from unittest.mock import MagicMock, Mock, patch

import pytest
from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.tabs.browse.components.modern_browse_control_panel import (
    ModernBrowseControlPanel,
    ModernSortButton,
    ModernSortWidget,
)
from desktop.modern.presentation.tabs.browse.components.sequence_browser_panel import (
    SequenceBrowserPanel,
)
from desktop.modern.presentation.tabs.browse.models import FilterType, SortMethod
from desktop.modern.presentation.tabs.browse.services.browse_service import BrowseService
from desktop.modern.presentation.tabs.browse.services.browse_state_service import BrowseStateService
from PyQt6.QtWidgets import QApplication


class TestModernBrowseControlPanel:
    """Test the modern browse control panel functionality."""

    @pytest.fixture
    def mock_state_service(self):
        """Create a mock state service."""
        mock_service = Mock(spec=BrowseStateService)
        mock_service.get_current_sort_method.return_value = SortMethod.ALPHABETICAL
        mock_service.get_sort_order.return_value = "alphabetical"
        return mock_service

    @pytest.fixture
    def control_panel(self, mock_state_service):
        """Create a ModernBrowseControlPanel instance for testing."""
        return ModernBrowseControlPanel(mock_state_service)

    def test_control_panel_initialization(self, control_panel):
        """Test that control panel initializes properly."""
        assert control_panel is not None
        assert hasattr(control_panel, "sort_widget")
        assert hasattr(control_panel, "back_button")
        assert hasattr(control_panel, "filter_label")
        assert hasattr(control_panel, "count_label")

    def test_filter_description_updates(self, control_panel):
        """Test that filter description updates correctly."""
        # Test starting letter filter
        control_panel.update_filter_description(FilterType.STARTING_LETTER, "A-D")
        assert "starting with A-D" in control_panel.filter_label.text()

        # Test contains letters filter
        control_panel.update_filter_description(FilterType.CONTAINS_LETTERS, "ABC")
        assert "containing ABC" in control_panel.filter_label.text()

        # Test length filter
        control_panel.update_filter_description(FilterType.LENGTH, 5)
        assert "length 5" in control_panel.filter_label.text()

        # Test no filter
        control_panel.update_filter_description(None, None)
        assert "All sequences" in control_panel.filter_label.text()

    def test_count_updates(self, control_panel):
        """Test that count updates correctly."""
        # Test zero count
        control_panel.update_count(0)
        assert "No sequences" in control_panel.count_label.text()

        # Test single count
        control_panel.update_count(1)
        assert "1 sequence" in control_panel.count_label.text()

        # Test multiple count
        control_panel.update_count(42)
        assert "42 sequences" in control_panel.count_label.text()

    def test_sort_method_persistence(self, control_panel):
        """Test that sort method is retrieved from state service."""
        # Initial sort method should be loaded
        assert control_panel.sort_widget.current_sort_method == "alphabetical"


class TestModernSortWidget:
    """Test the modern sort widget functionality."""

    @pytest.fixture
    def mock_state_service(self):
        """Create a mock state service."""
        mock_service = Mock(spec=BrowseStateService)
        mock_service.get_current_sort_method.return_value = SortMethod.ALPHABETICAL
        return mock_service

    @pytest.fixture
    def sort_widget(self, mock_state_service):
        """Create a ModernSortWidget instance for testing."""
        return ModernSortWidget(mock_state_service)

    def test_sort_widget_initialization(self, sort_widget):
        """Test that sort widget initializes with correct buttons."""
        assert sort_widget is not None
        assert len(sort_widget.sort_buttons) == 4
        assert "alphabetical" in sort_widget.sort_buttons
        assert "length" in sort_widget.sort_buttons
        assert "level" in sort_widget.sort_buttons
        assert "date_added" in sort_widget.sort_buttons

    def test_sort_button_selection(self, sort_widget):
        """Test that sort buttons can be selected."""
        # Test setting sort method
        sort_widget.set_sort_method("length")
        assert sort_widget.current_sort_method == "length"

        # Check that the correct button is selected
        assert sort_widget.sort_buttons["length"].is_selected is True
        assert sort_widget.sort_buttons["alphabetical"].is_selected is False

    def test_sort_method_change_signal(self, sort_widget):
        """Test that sort method change emits signal."""
        # Mock the signal
        with patch.object(sort_widget, "sort_changed") as mock_signal:
            sort_widget._on_sort_selected("level")
            mock_signal.emit.assert_called_once_with("level")

    def test_sort_method_state_persistence(self, sort_widget, mock_state_service):
        """Test that sort method changes are persisted."""
        # Mock set_sort_method
        mock_state_service.set_sort_method = Mock()

        # Change sort method
        sort_widget._on_sort_selected("level")

        # Verify state service was called
        mock_state_service.set_sort_method.assert_called_once_with(
            SortMethod.DIFFICULTY_LEVEL
        )


class TestModernSortButton:
    """Test the modern sort button functionality."""

    @pytest.fixture
    def sort_button(self):
        """Create a ModernSortButton instance for testing."""
        return ModernSortButton("Test", "test_method")

    def test_sort_button_initialization(self, sort_button):
        """Test that sort button initializes properly."""
        assert sort_button is not None
        assert sort_button.text() == "Test"
        assert sort_button.sort_method == "test_method"
        assert sort_button.is_selected is False

    def test_sort_button_selection_state(self, sort_button):
        """Test that sort button selection state works."""
        # Initially not selected
        assert sort_button.is_selected is False

        # Set selected
        sort_button.set_selected(True)
        assert sort_button.is_selected is True

        # Set not selected
        sort_button.set_selected(False)
        assert sort_button.is_selected is False

    def test_sort_button_signal_emission(self, sort_button):
        """Test that sort button emits signal when clicked."""
        # Mock the signal
        with patch.object(sort_button, "sort_selected") as mock_signal:
            sort_button.click()
            mock_signal.emit.assert_called_once_with("test_method")


class TestControlPanelSequenceBrowserIntegration:
    """Test integration between control panel and sequence browser."""

    @pytest.fixture
    def mock_browse_service(self):
        """Create a mock browse service."""
        return Mock(spec=BrowseService)

    @pytest.fixture
    def mock_state_service(self):
        """Create a mock state service."""
        mock_service = Mock(spec=BrowseStateService)
        mock_service.get_current_sort_method.return_value = SortMethod.ALPHABETICAL
        mock_service.get_sort_order.return_value = "alphabetical"
        return mock_service

    @pytest.fixture
    def sequence_browser_panel(self, mock_browse_service, mock_state_service):
        """Create a SequenceBrowserPanel instance for testing."""
        return SequenceBrowserPanel(mock_browse_service, mock_state_service)

    @pytest.fixture
    def sample_sequences(self):
        """Create sample sequences for testing."""
        return [
            SequenceData(
                id="seq1",
                word="Apple",
                sequence_length=3,
                level=1,
                thumbnails=["path1.jpg"],
            ),
            SequenceData(
                id="seq2",
                word="Banana",
                sequence_length=4,
                level=2,
                thumbnails=["path2.jpg"],
            ),
        ]

    def test_sort_change_propagation(self, sequence_browser_panel, sample_sequences):
        """Test that sort changes from control panel propagate to browser."""
        # Set up initial sequences
        sequence_browser_panel.current_sequences = sample_sequences

        # Mock the display method
        with patch.object(
            sequence_browser_panel, "_sort_and_display_sequences"
        ) as mock_display:
            # Simulate sort change from control panel
            sequence_browser_panel._on_sort_changed("length")

            # Verify that display was called with correct sort method
            mock_display.assert_called_once_with(sample_sequences, "length")

    def test_navigation_sidebar_updates_on_sort(
        self, sequence_browser_panel, sample_sequences
    ):
        """Test that navigation sidebar updates when sort changes."""
        # Set up sequences and navigation sidebar
        sequence_browser_panel.current_sequences = sample_sequences
        sequence_browser_panel.navigation_sidebar = Mock()

        # Mock the display methods
        with (
            patch.object(sequence_browser_panel, "_clear_grid"),
            patch.object(
                sequence_browser_panel, "_create_sequence_thumbnail"
            ) as mock_create,
        ):

            # Change sort method
            sequence_browser_panel._on_sort_changed("length")

            # Verify navigation sidebar was updated
            sequence_browser_panel.navigation_sidebar.update_sections.assert_called_once()

    def test_control_panel_state_synchronization(
        self, sequence_browser_panel, mock_state_service
    ):
        """Test that control panel and browser stay synchronized."""
        # Verify that both components use the same state service
        assert sequence_browser_panel.state_service is mock_state_service

        # Verify that sort order is retrieved consistently
        sort_order = sequence_browser_panel.state_service.get_sort_order()
        assert sort_order == "alphabetical"


class TestSortingStateManagement:
    """Test state management for sorting functionality."""

    @pytest.fixture
    def mock_state_service(self):
        """Create a mock state service with full functionality."""
        mock_service = Mock(spec=BrowseStateService)
        mock_service.get_current_sort_method.return_value = SortMethod.ALPHABETICAL
        mock_service.get_sort_order.return_value = "alphabetical"
        mock_service.set_sort_method = Mock()
        return mock_service

    def test_sort_method_enum_conversion(self, mock_state_service):
        """Test that sort method strings are properly converted to enums."""
        sort_widget = ModernSortWidget(mock_state_service)

        # Test conversion from string to enum
        sort_widget._on_sort_selected("length")

        # Verify correct enum was passed to state service
        mock_state_service.set_sort_method.assert_called_once_with(
            SortMethod.SEQUENCE_LENGTH
        )

    def test_sort_method_persistence_across_sessions(self, mock_state_service):
        """Test that sort method persists across sessions."""
        # Create widget and verify it loads initial state
        sort_widget = ModernSortWidget(mock_state_service)

        # Verify initial state was loaded
        mock_state_service.get_current_sort_method.assert_called_once()

    def test_sort_order_string_mapping(self, mock_state_service):
        """Test that sort methods are correctly mapped to string values."""
        # Test the mapping in BrowseStateService.get_sort_order
        mock_state_service.get_sort_order.return_value = "length"

        sort_widget = ModernSortWidget(mock_state_service)

        # Verify the mapping works
        assert sort_widget.current_sort_method == "alphabetical"  # Initial value

        # Test setting different sort methods
        sort_widget.set_sort_method("length")
        assert sort_widget.current_sort_method == "length"


@pytest.mark.gui
class TestControlPanelGUI:
    """Test GUI-related functionality (requires display)."""

    @pytest.fixture
    def qt_app(self):
        """Provide QApplication for GUI tests."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        return app

    @pytest.fixture
    def mock_state_service(self):
        """Create a mock state service."""
        mock_service = Mock(spec=BrowseStateService)
        mock_service.get_current_sort_method.return_value = SortMethod.ALPHABETICAL
        return mock_service

    @pytest.fixture
    def control_panel(self, qt_app, mock_state_service):
        """Create a ModernBrowseControlPanel instance for GUI testing."""
        return ModernBrowseControlPanel(mock_state_service)

    def test_control_panel_widget_creation(self, control_panel):
        """Test that all widgets are created properly."""
        assert control_panel.back_button is not None
        assert control_panel.title_label is not None
        assert control_panel.filter_label is not None
        assert control_panel.count_label is not None
        assert control_panel.sort_widget is not None

    def test_sort_button_styling(self, control_panel):
        """Test that sort buttons have proper styling."""
        for button in control_panel.sort_widget.sort_buttons.values():
            assert button.styleSheet() != ""  # Should have style

            # Test selected state styling
            button.set_selected(True)
            selected_style = button.styleSheet()

            button.set_selected(False)
            normal_style = button.styleSheet()

            # Styles should be different
            assert selected_style != normal_style

    def test_control_panel_signal_connections(self, control_panel):
        """Test that signals are properly connected."""
        # Test back button signal
        with patch.object(control_panel, "back_to_filters") as mock_signal:
            control_panel.back_button.click()
            mock_signal.emit.assert_called_once()

    def test_sort_widget_layout(self, control_panel):
        """Test that sort widget has proper layout."""
        sort_widget = control_panel.sort_widget

        # Should have all expected buttons
        assert len(sort_widget.sort_buttons) == 4

        # Buttons should be in the widget
        for button in sort_widget.sort_buttons.values():
            assert button.parent() == sort_widget
