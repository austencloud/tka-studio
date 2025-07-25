"""
Comprehensive Tests for BetaPositioningDetector

Tests the beta positioning detection service in isolation.
"""

import pytest

from domain.models import BeatData
from domain.models.pictograph_data import PictographData

from application.services.positioning.props.detection.beta_positioning_detector import (
    BetaPositioningDetector,
)


class TestBetaPositioningDetector:
    """Comprehensive test suite for BetaPositioningDetector."""

    @pytest.fixture
    def detector(self):
        """Create detector instance for testing."""
        return BetaPositioningDetector()

    def test_initialization(self, detector):
        """Test that detector initializes correctly."""
        assert detector is not None
        beta_letters = detector.get_beta_ending_letters()
        assert len(beta_letters) == 13  # Expected number of beta-ending letters
        assert "G" in beta_letters
        assert "β" in beta_letters

    @pytest.mark.parametrize("letter", [
        "G", "H", "I", "J", "K", "L", "Y", "Z", "Y-", "Z-", "Ψ", "Ψ-", "β"
    ])
    def test_detects_all_beta_ending_letters(self, detector, letter):
        """Test detection of all beta-ending letters."""
        pictograph_data = PictographData(letter=letter)
        beat_data = BeatData(pictograph_data=pictograph_data)
        
        assert detector.should_apply_beta_positioning(beat_data) is True
        assert detector.is_beta_ending_letter(letter) is True

    @pytest.mark.parametrize("letter", [
        "A", "B", "C", "D", "E", "F", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X"
    ])
    def test_rejects_non_beta_letters(self, detector, letter):
        """Test rejection of non-beta letters."""
        pictograph_data = PictographData(letter=letter)
        beat_data = BeatData(pictograph_data=pictograph_data)
        
        assert detector.should_apply_beta_positioning(beat_data) is False
        assert detector.is_beta_ending_letter(letter) is False

    def test_handles_none_beat_data(self, detector):
        """Test handling of None beat data."""
        assert detector.should_apply_beta_positioning(None) is False

    def test_handles_beat_data_without_pictograph(self, detector):
        """Test handling of beat data without pictograph data."""
        beat_data = BeatData()
        assert detector.should_apply_beta_positioning(beat_data) is False

    def test_handles_pictograph_without_letter(self, detector):
        """Test handling of pictograph data without letter."""
        pictograph_data = PictographData()
        beat_data = BeatData(pictograph_data=pictograph_data)
        assert detector.should_apply_beta_positioning(beat_data) is False

    def test_handles_empty_string_letter(self, detector):
        """Test handling of empty string letter."""
        pictograph_data = PictographData(letter="")
        beat_data = BeatData(pictograph_data=pictograph_data)
        assert detector.should_apply_beta_positioning(beat_data) is False
        assert detector.is_beta_ending_letter("") is False

    def test_handles_none_letter(self, detector):
        """Test handling of None letter."""
        assert detector.is_beta_ending_letter(None) is False

    def test_case_sensitivity(self, detector):
        """Test that detection is case-sensitive."""
        # Lowercase should not match
        assert detector.is_beta_ending_letter("g") is False
        assert detector.is_beta_ending_letter("h") is False
        
        # Uppercase should match
        assert detector.is_beta_ending_letter("G") is True
        assert detector.is_beta_ending_letter("H") is True

    def test_get_beta_ending_letters_returns_copy(self, detector):
        """Test that get_beta_ending_letters returns a copy, not the original list."""
        letters1 = detector.get_beta_ending_letters()
        letters2 = detector.get_beta_ending_letters()
        
        # Should be equal but not the same object
        assert letters1 == letters2
        assert letters1 is not letters2
        
        # Modifying one should not affect the other
        letters1.append("TEST")
        assert "TEST" not in letters2
        assert "TEST" not in detector.get_beta_ending_letters()

    def test_special_characters_in_beta_letters(self, detector):
        """Test that special characters in beta letters are handled correctly."""
        special_letters = ["Y-", "Z-", "Ψ", "Ψ-", "β"]
        
        for letter in special_letters:
            pictograph_data = PictographData(letter=letter)
            beat_data = BeatData(pictograph_data=pictograph_data)
            assert detector.should_apply_beta_positioning(beat_data) is True

    def test_consistency_between_methods(self, detector):
        """Test that is_beta_ending_letter and should_apply_beta_positioning are consistent."""
        test_letters = ["G", "A", "I", "X", "β", "test"]
        
        for letter in test_letters:
            pictograph_data = PictographData(letter=letter)
            beat_data = BeatData(pictograph_data=pictograph_data)
            
            is_beta = detector.is_beta_ending_letter(letter)
            should_apply = detector.should_apply_beta_positioning(beat_data)
            
            assert is_beta == should_apply, f"Inconsistency for letter '{letter}'"

    def test_performance_with_many_calls(self, detector):
        """Test performance with many repeated calls."""
        import time
        
        pictograph_data = PictographData(letter="G")
        beat_data = BeatData(pictograph_data=pictograph_data)
        
        start_time = time.time()
        for _ in range(10000):
            detector.should_apply_beta_positioning(beat_data)
        end_time = time.time()
        
        # Should complete 10,000 calls in under 1 second
        assert (end_time - start_time) < 1.0

    def test_immutability_of_internal_state(self, detector):
        """Test that the detector's internal state cannot be modified externally."""
        original_letters = detector.get_beta_ending_letters()
        
        # Try to modify the returned list
        returned_letters = detector.get_beta_ending_letters()
        returned_letters.clear()
        
        # Original state should be unchanged
        assert detector.get_beta_ending_letters() == original_letters
        assert len(detector.get_beta_ending_letters()) == 13
