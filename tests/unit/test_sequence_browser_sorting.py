"""
Sequence Browser Panel Sorting and Sectioning Tests

Test suite for the sorting and sectioning functionality in the sequence browser panel.
Ensures proper sorting, section creation, and navigation behavior.
"""

from datetime import date, datetime
from unittest.mock import Mock, patch

import pytest
from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.tabs.browse.components.sequence_browser_panel import (
    SequenceBrowserPanel,
)
from desktop.modern.presentation.tabs.browse.models import FilterType
from desktop.modern.presentation.tabs.browse.services.browse_service import BrowseService
from desktop.modern.presentation.tabs.browse.services.browse_state_service import BrowseStateService
from PyQt6.QtWidgets import QApplication


class TestSequenceBrowserSorting:
    """Test sorting functionality in the sequence browser panel."""

    @pytest.fixture
    def mock_browse_service(self):
        """Create a mock browse service."""
        return Mock(spec=BrowseService)

    @pytest.fixture
    def mock_state_service(self):
        """Create a mock state service."""
        mock_service = Mock(spec=BrowseStateService)
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
                word="Zebra",
                sequence_length=5,
                level=2,
                date_added=datetime(2023, 1, 15),
                thumbnails=["path1.jpg"],
            ),
            SequenceData(
                id="seq2",
                word="Apple",
                sequence_length=3,
                level=1,
                date_added=datetime(2023, 2, 20),
                thumbnails=["path2.jpg"],
            ),
            SequenceData(
                id="seq3",
                word="Banana",
                sequence_length=4,
                level=3,
                date_added=datetime(2023, 1, 10),
                thumbnails=["path3.jpg"],
            ),
            SequenceData(
                id="seq4",
                word="Cherry",
                sequence_length=3,
                level=1,
                date_added=datetime(2023, 3, 5),
                thumbnails=["path4.jpg"],
            ),
        ]

    def test_sort_sequences_alphabetical(
        self, sequence_browser_panel, sample_sequences
    ):
        """Test alphabetical sorting of sequences."""
        sorted_sequences = sequence_browser_panel._sort_sequences(
            sample_sequences, "alphabetical"
        )

        expected_order = ["Apple", "Banana", "Cherry", "Zebra"]
        actual_order = [seq.word for seq in sorted_sequences]

        assert actual_order == expected_order

    def test_sort_sequences_by_length(self, sequence_browser_panel, sample_sequences):
        """Test sorting sequences by length."""
        sorted_sequences = sequence_browser_panel._sort_sequences(
            sample_sequences, "length"
        )

        expected_lengths = [3, 3, 4, 5]  # Apple, Cherry, Banana, Zebra
        actual_lengths = [seq.sequence_length for seq in sorted_sequences]

        assert actual_lengths == expected_lengths

    def test_sort_sequences_by_level(self, sequence_browser_panel, sample_sequences):
        """Test sorting sequences by level."""
        sorted_sequences = sequence_browser_panel._sort_sequences(
            sample_sequences, "level"
        )

        expected_levels = [1, 1, 2, 3]  # Apple, Cherry, Zebra, Banana
        actual_levels = [seq.level for seq in sorted_sequences]

        assert actual_levels == expected_levels

    def test_sort_sequences_by_date_added(
        self, sequence_browser_panel, sample_sequences
    ):
        """Test sorting sequences by date added (newest first)."""
        sorted_sequences = sequence_browser_panel._sort_sequences(
            sample_sequences, "date_added"
        )

        # Should be newest first: Cherry (March 5), Apple (Feb 20), Zebra (Jan 15), Banana (Jan 10)
        expected_order = ["Cherry", "Apple", "Zebra", "Banana"]
        actual_order = [seq.word for seq in sorted_sequences]

        assert actual_order == expected_order

    def test_sort_sequences_default_fallback(
        self, sequence_browser_panel, sample_sequences
    ):
        """Test that unknown sort method falls back to alphabetical."""
        sorted_sequences = sequence_browser_panel._sort_sequences(
            sample_sequences, "unknown_method"
        )

        expected_order = ["Apple", "Banana", "Cherry", "Zebra"]
        actual_order = [seq.word for seq in sorted_sequences]

        assert actual_order == expected_order


class TestSequenceBrowserSectioning:
    """Test sectioning functionality in the sequence browser panel."""

    @pytest.fixture
    def mock_browse_service(self):
        """Create a mock browse service."""
        return Mock(spec=BrowseService)

    @pytest.fixture
    def mock_state_service(self):
        """Create a mock state service."""
        mock_service = Mock(spec=BrowseStateService)
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
                date_added=datetime(2023, 1, 15),
                thumbnails=["path1.jpg"],
            ),
            SequenceData(
                id="seq2",
                word="Banana",
                sequence_length=4,
                level=2,
                date_added=datetime(2023, 2, 20),
                thumbnails=["path2.jpg"],
            ),
            SequenceData(
                id="seq3",
                word="Cherry",
                sequence_length=3,
                level=1,
                date_added=datetime(2023, 1, 10),
                thumbnails=["path3.jpg"],
            ),
            SequenceData(
                id="seq4",
                word="Zebra",
                sequence_length=5,
                level=3,
                date_added=datetime(2023, 3, 5),
                thumbnails=["path4.jpg"],
            ),
        ]

    def test_get_section_key_alphabetical(
        self, sequence_browser_panel, sample_sequences
    ):
        """Test section key generation for alphabetical sorting."""
        for seq in sample_sequences:
            section_key = sequence_browser_panel._get_section_key(seq, "alphabetical")
            expected_key = seq.word[0].upper()
            assert section_key == expected_key

    def test_get_section_key_length(self, sequence_browser_panel, sample_sequences):
        """Test section key generation for length sorting."""
        for seq in sample_sequences:
            section_key = sequence_browser_panel._get_section_key(seq, "length")
            expected_key = f"Length {seq.sequence_length}"
            assert section_key == expected_key

    def test_get_section_key_level(self, sequence_browser_panel, sample_sequences):
        """Test section key generation for level sorting."""
        for seq in sample_sequences:
            section_key = sequence_browser_panel._get_section_key(seq, "level")
            expected_key = f"Level {seq.level}"
            assert section_key == expected_key

    def test_get_section_key_date_added(self, sequence_browser_panel, sample_sequences):
        """Test section key generation for date added sorting."""
        for seq in sample_sequences:
            section_key = sequence_browser_panel._get_section_key(seq, "date_added")
            expected_key = seq.date_added.strftime("%Y-%m")
            assert section_key == expected_key

    def test_group_sequences_into_sections_alphabetical(
        self, sequence_browser_panel, sample_sequences
    ):
        """Test grouping sequences into alphabetical sections."""
        sections = sequence_browser_panel._group_sequences_into_sections(
            sample_sequences, "alphabetical"
        )

        # Should have sections: A, B, C, Z
        expected_sections = {"A", "B", "C", "Z"}
        assert set(sections.keys()) == expected_sections

        # Check sequence distribution
        assert len(sections["A"]) == 1  # Apple
        assert len(sections["B"]) == 1  # Banana
        assert len(sections["C"]) == 1  # Cherry
        assert len(sections["Z"]) == 1  # Zebra

    def test_group_sequences_into_sections_length(
        self, sequence_browser_panel, sample_sequences
    ):
        """Test grouping sequences into length sections."""
        sections = sequence_browser_panel._group_sequences_into_sections(
            sample_sequences, "length"
        )

        # Should have sections: Length 3, Length 4, Length 5
        expected_sections = {"Length 3", "Length 4", "Length 5"}
        assert set(sections.keys()) == expected_sections

        # Check sequence distribution
        assert len(sections["Length 3"]) == 2  # Apple, Cherry
        assert len(sections["Length 4"]) == 1  # Banana
        assert len(sections["Length 5"]) == 1  # Zebra

    def test_group_sequences_into_sections_level(
        self, sequence_browser_panel, sample_sequences
    ):
        """Test grouping sequences into level sections."""
        sections = sequence_browser_panel._group_sequences_into_sections(
            sample_sequences, "level"
        )

        # Should have sections: Level 1, Level 2, Level 3
        expected_sections = {"Level 1", "Level 2", "Level 3"}
        assert set(sections.keys()) == expected_sections

        # Check sequence distribution
        assert len(sections["Level 1"]) == 2  # Apple, Cherry
        assert len(sections["Level 2"]) == 1  # Banana
        assert len(sections["Level 3"]) == 1  # Zebra

    def test_group_sequences_into_sections_date_added(
        self, sequence_browser_panel, sample_sequences
    ):
        """Test grouping sequences into date sections."""
        sections = sequence_browser_panel._group_sequences_into_sections(
            sample_sequences, "date_added"
        )

        # Should have sections: 2023-01, 2023-02, 2023-03
        expected_sections = {"2023-01", "2023-02", "2023-03"}
        assert set(sections.keys()) == expected_sections

        # Check sequence distribution
        assert len(sections["2023-01"]) == 2  # Apple, Cherry
        assert len(sections["2023-02"]) == 1  # Banana
        assert len(sections["2023-03"]) == 1  # Zebra


class TestSequenceBrowserIntegration:
    """Test integration between sorting and sectioning functionality."""

    @pytest.fixture
    def mock_browse_service(self):
        """Create a mock browse service."""
        return Mock(spec=BrowseService)

    @pytest.fixture
    def mock_state_service(self):
        """Create a mock state service."""
        mock_service = Mock(spec=BrowseStateService)
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
                word="Zebra",
                sequence_length=5,
                level=2,
                date_added=datetime(2023, 1, 15),
                thumbnails=["path1.jpg"],
            ),
            SequenceData(
                id="seq2",
                word="Apple",
                sequence_length=3,
                level=1,
                date_added=datetime(2023, 2, 20),
                thumbnails=["path2.jpg"],
            ),
            SequenceData(
                id="seq3",
                word="Banana",
                sequence_length=4,
                level=3,
                date_added=datetime(2023, 1, 10),
                thumbnails=["path3.jpg"],
            ),
        ]

    def test_sort_method_change_integration(
        self, sequence_browser_panel, sample_sequences
    ):
        """Test that sort method changes properly update the display."""
        # Set initial sequences
        sequence_browser_panel.current_sequences = sample_sequences

        # Mock the grid and navigation components
        with (
            patch.object(sequence_browser_panel, "_clear_grid"),
            patch.object(
                sequence_browser_panel, "_add_section_header"
            ) as mock_add_header,
            patch.object(
                sequence_browser_panel, "_create_sequence_thumbnail"
            ) as mock_create_thumbnail,
        ):

            # Test alphabetical sort
            sequence_browser_panel._on_sort_changed("alphabetical")

            # Verify that sections were created
            assert mock_add_header.call_count > 0
            assert mock_create_thumbnail.call_count == len(sample_sequences)

    def test_show_sequences_with_sort_method(
        self, sequence_browser_panel, sample_sequences
    ):
        """Test that show_sequences properly applies sorting."""
        # Mock the internal methods
        with patch.object(
            sequence_browser_panel, "_sort_and_display_sequences"
        ) as mock_sort_display:
            sequence_browser_panel.show_sequences(
                sample_sequences, FilterType.ALL_SEQUENCES
            )

            # Verify sort and display was called
            mock_sort_display.assert_called_once()
            args = mock_sort_display.call_args[0]
            assert args[0] == sample_sequences  # sequences
            assert args[1] == "alphabetical"  # sort method


class TestSequenceBrowserEdgeCases:
    """Test edge cases and error conditions."""

    @pytest.fixture
    def mock_browse_service(self):
        """Create a mock browse service."""
        return Mock(spec=BrowseService)

    @pytest.fixture
    def mock_state_service(self):
        """Create a mock state service."""
        mock_service = Mock(spec=BrowseStateService)
        mock_service.get_sort_order.return_value = "alphabetical"
        return mock_service

    @pytest.fixture
    def sequence_browser_panel(self, mock_browse_service, mock_state_service):
        """Create a SequenceBrowserPanel instance for testing."""
        return SequenceBrowserPanel(mock_browse_service, mock_state_service)

    def test_sort_empty_sequences(self, sequence_browser_panel):
        """Test sorting empty sequence list."""
        sorted_sequences = sequence_browser_panel._sort_sequences([], "alphabetical")
        assert sorted_sequences == []

    def test_sort_sequences_with_none_values(self, sequence_browser_panel):
        """Test sorting sequences with None values."""
        sequences = [
            SequenceData(
                id="seq1", word=None, sequence_length=None, level=None, date_added=None
            ),
            SequenceData(
                id="seq2",
                word="Apple",
                sequence_length=3,
                level=1,
                date_added=datetime(2023, 1, 15),
            ),
        ]

        # Should not crash with None values
        sorted_sequences = sequence_browser_panel._sort_sequences(
            sequences, "alphabetical"
        )
        assert len(sorted_sequences) == 2

        # None values should be handled gracefully
        sorted_sequences = sequence_browser_panel._sort_sequences(sequences, "length")
        assert len(sorted_sequences) == 2

    def test_get_section_key_with_none_values(self, sequence_browser_panel):
        """Test section key generation with None values."""
        seq = SequenceData(
            id="seq1", word=None, sequence_length=None, level=None, date_added=None
        )

        # Should return fallback values
        assert sequence_browser_panel._get_section_key(seq, "alphabetical") == "?"
        assert (
            sequence_browser_panel._get_section_key(seq, "length") == "Unknown Length"
        )
        assert sequence_browser_panel._get_section_key(seq, "level") == "Unknown Level"
        assert (
            sequence_browser_panel._get_section_key(seq, "date_added") == "Unknown Date"
        )

    def test_group_empty_sequences(self, sequence_browser_panel):
        """Test grouping empty sequence list."""
        sections = sequence_browser_panel._group_sequences_into_sections(
            [], "alphabetical"
        )
        assert sections == {}

    def test_section_navigation_with_no_sections(self, sequence_browser_panel):
        """Test section navigation when no sections exist."""
        # Should not crash when trying to navigate to non-existent section
        sequence_browser_panel._on_section_selected("NonExistentSection")
        # If we get here without exception, the test passes


@pytest.mark.gui
class TestSequenceBrowserGUI:
    """Test GUI-related functionality (requires display)."""

    @pytest.fixture
    def qt_app(self):
        """Provide QApplication for GUI tests."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        return app

    @pytest.fixture
    def mock_browse_service(self):
        """Create a mock browse service."""
        return Mock(spec=BrowseService)

    @pytest.fixture
    def mock_state_service(self):
        """Create a mock state service."""
        mock_service = Mock(spec=BrowseStateService)
        mock_service.get_sort_order.return_value = "alphabetical"
        return mock_service

    @pytest.fixture
    def sequence_browser_panel(self, qt_app, mock_browse_service, mock_state_service):
        """Create a SequenceBrowserPanel instance for GUI testing."""
        return SequenceBrowserPanel(mock_browse_service, mock_state_service)

    def test_section_header_creation(self, sequence_browser_panel):
        """Test that section headers are properly created."""
        # Test header creation
        current_row = sequence_browser_panel._add_section_header("Test Section", 0)

        # Should return the next row number
        assert current_row == 1

        # Check that a widget was added to the grid
        assert sequence_browser_panel.grid_layout.count() > 0

    def test_thumbnail_creation_with_sections(self, sequence_browser_panel):
        """Test that thumbnails are created properly with sections."""
        sample_seq = SequenceData(
            id="seq1", word="Test", sequence_length=3, level=1, thumbnails=["test.jpg"]
        )

        # Should not crash when creating thumbnail
        thumbnail = sequence_browser_panel._create_sequence_thumbnail(sample_seq)
        assert thumbnail is not None
