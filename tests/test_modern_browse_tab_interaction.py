"""
Browse Tab Integration Tests

Test suite to ensure the Modern Browse Tab works smoothly and consistently
without crashes when users interact with it.
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from domain.models.sequence_data import SequenceData
from presentation.tabs.browse.models import FilterType
from presentation.tabs.browse.modern_browse_tab import ModernBrowseTab
from presentation.tabs.browse.services.browse_service import BrowseService
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication


class TestModernBrowseTabInteraction:
    """Test user interactions with the Modern Browse Tab to prevent crashes."""

    @pytest.fixture
    def mock_sequences_dir(self, tmp_path):
        """Create a temporary sequences directory."""
        sequences_dir = tmp_path / "sequences"
        sequences_dir.mkdir()
        return sequences_dir

    @pytest.fixture
    def mock_settings_file(self, tmp_path):
        """Create a temporary settings file."""
        settings_file = tmp_path / "settings.json"
        settings_file.write_text('{"filter_type": null, "filter_value": null}')
        return settings_file

    @pytest.fixture
    def browse_tab(self, mock_sequences_dir, mock_settings_file):
        """Create a ModernBrowseTab instance for testing."""
        return ModernBrowseTab(mock_sequences_dir, mock_settings_file)

    def test_browse_tab_initialization(self, browse_tab):
        """Test that browse tab initializes without crashing."""
        assert browse_tab is not None
        assert hasattr(browse_tab, "internal_left_stack")
        assert hasattr(browse_tab, "filter_selection_panel")
        assert hasattr(browse_tab, "sequence_browser_panel")
        assert hasattr(browse_tab, "sequence_viewer_panel")

    def test_filter_selection_panel_creation(self, browse_tab):
        """Test that filter selection panel creates all buttons without crashing."""
        filter_panel = browse_tab.filter_selection_panel

        # Check that all expected filter buttons exist
        expected_filters = [
            FilterType.STARTING_LETTER,
            FilterType.CONTAINS_LETTERS,
            FilterType.SEQUENCE_LENGTH,
            FilterType.DIFFICULTY_LEVEL,
            FilterType.STARTING_POSITION,
            FilterType.AUTHOR,
            FilterType.FAVORITES,
            FilterType.MOST_RECENT,
            FilterType.GRID_MODE,
        ]

        for filter_type in expected_filters:
            assert filter_type in filter_panel.filter_buttons

        # Check Show All button exists
        assert hasattr(filter_panel, "show_all_button")
        assert filter_panel.show_all_button is not None

    def test_filter_button_clicks_no_crash(self, browse_tab):
        """Test that clicking filter buttons doesn't crash the application."""
        filter_panel = browse_tab.filter_selection_panel

        # Test each filter button click
        for filter_type in filter_panel.filter_buttons:
            # This should not crash
            filter_panel._on_filter_button_clicked(filter_type)

        # Test Show All button click
        filter_panel._on_filter_button_clicked(FilterType.ALL_SEQUENCES)

    def test_navigation_stack_switching(self, browse_tab):
        """Test that navigation stack switching works without crashing."""
        # Should start with filter selection (index 0)
        assert browse_tab.internal_left_stack.currentIndex() == 0

        # Switch to sequence browser (index 1)
        browse_tab._show_sequence_browser()
        assert browse_tab.internal_left_stack.currentIndex() == 1

        # Switch back to filter selection (index 0)
        browse_tab._show_filter_selection()
        assert browse_tab.internal_left_stack.currentIndex() == 0

    def test_filter_selection_signal_handling(self, browse_tab):
        """Test that filter selection signals are handled properly."""
        # Mock the signal connection
        with patch.object(browse_tab, "_on_filter_selected") as mock_handler:
            # Emit filter selected signal
            browse_tab.filter_selection_panel.filter_selected.emit(
                FilterType.ALL_SEQUENCES, None
            )

            # Verify handler was called
            mock_handler.assert_called_once_with(FilterType.ALL_SEQUENCES, None)

    def test_browse_service_filter_with_none_values(self, mock_sequences_dir):
        """Test that browse service handles None filter values without crashing."""
        service = BrowseService(mock_sequences_dir)

        # Test each filter type with None value
        filter_types = [
            FilterType.ALL_SEQUENCES,
            FilterType.STARTING_LETTER,
            FilterType.CONTAINS_LETTERS,
            FilterType.SEQUENCE_LENGTH,
            FilterType.DIFFICULTY_LEVEL,
            FilterType.STARTING_POSITION,
            FilterType.AUTHOR,
            FilterType.GRID_MODE,
            FilterType.FAVORITES,
            FilterType.MOST_RECENT,
        ]

        for filter_type in filter_types:
            # This should not crash
            result = service.apply_filter(filter_type, None)
            assert isinstance(result, list)

    def test_sequence_browser_back_navigation(self, browse_tab):
        """Test that back navigation from sequence browser works."""
        # Switch to sequence browser
        browse_tab._show_sequence_browser()
        assert browse_tab.internal_left_stack.currentIndex() == 1

        # Emit back to filters signal
        browse_tab.sequence_browser_panel.back_to_filters.emit()

        # Should switch back to filter selection
        assert browse_tab.internal_left_stack.currentIndex() == 0

    def test_responsive_grid_layout(self, browse_tab):
        """Test that responsive grid layout doesn't crash on resize."""
        filter_panel = browse_tab.filter_selection_panel

        # Simulate different window sizes
        test_widths = [400, 600, 800, 1200]

        for width in test_widths:
            # Simulate resize event
            filter_panel.resize(width, 600)

            # This should not crash
            filter_panel._finalize_layout_initialization()

    def test_sequence_viewer_operations(self, browse_tab):
        """Test that sequence viewer operations don't crash."""
        viewer = browse_tab.sequence_viewer_panel

        # Test showing a sequence
        test_sequence_data = {
            "word": "test_word",
            "length": 4,
            "difficulty": "beginner",
        }

        # This should not crash
        viewer.show_sequence("test_id", test_sequence_data)

        # Test clearing sequence
        viewer.clear_sequence()

    def test_filter_selection_to_browser_workflow(self, browse_tab):
        """Test the complete workflow from filter selection to browser."""
        # Start with filter selection
        assert browse_tab.internal_left_stack.currentIndex() == 0

        # Click a filter button
        browse_tab.filter_selection_panel._on_filter_button_clicked(
            FilterType.ALL_SEQUENCES
        )

        # Should switch to sequence browser
        assert browse_tab.internal_left_stack.currentIndex() == 1

        # Click back button
        browse_tab.sequence_browser_panel.back_to_filters.emit()

        # Should return to filter selection
        assert browse_tab.internal_left_stack.currentIndex() == 0


class TestBrowseServiceRobustness:
    """Test browse service robustness to prevent crashes."""

    @pytest.fixture
    def browse_service(self, tmp_path):
        """Create a BrowseService instance for testing."""
        sequences_dir = tmp_path / "sequences"
        sequences_dir.mkdir()
        return BrowseService(sequences_dir)

    def test_load_sequences_empty_directory(self, browse_service):
        """Test loading sequences from empty directory doesn't crash."""
        sequences = browse_service.load_sequences()
        assert isinstance(sequences, list)
        # Should return test sequences when no real sequences exist
        assert len(sequences) > 0

    def test_apply_filter_edge_cases(self, browse_service):
        """Test edge cases in filter application."""
        # Test with None values
        result = browse_service.apply_filter(FilterType.STARTING_LETTER, None)
        assert isinstance(result, list)

        # Test with empty string
        result = browse_service.apply_filter(FilterType.STARTING_LETTER, "")
        assert isinstance(result, list)

        # Test with invalid filter type
        result = browse_service.apply_filter(FilterType.ALL_SEQUENCES, "invalid")
        assert isinstance(result, list)

    def test_sort_sequences_robustness(self, browse_service):
        """Test sequence sorting robustness."""
        from presentation.tabs.browse.models import SortMethod

        sequences = browse_service.load_sequences()

        # Test each sort method
        for sort_method in SortMethod:
            result = browse_service.sort_sequences(sequences, sort_method)
            assert isinstance(result, list)
            assert len(result) == len(sequences)


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
