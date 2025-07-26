"""
Unit tests for OptionPickerSectionCoordinationService.

Tests the platform-agnostic section coordination logic for managing
section updates, state caching, and coordination between sections.
"""

import unittest
from unittest.mock import Mock

from shared.application.services.option_picker.option_picker_section_coordination_service import (
    OptionPickerSectionCoordinationService,
)
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.components.option_picker.types.letter_types import LetterType


class TestOptionPickerSectionCoordinationService(unittest.TestCase):
    """Test suite for OptionPickerSectionCoordinationService."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.service = OptionPickerSectionCoordinationService()

        # Create sample beats for testing
        self.sample_beats = [
            BeatData(beat_number=1, duration=1.0),
            BeatData(beat_number=2, duration=1.0),
            BeatData(beat_number=3, duration=1.0),
        ]

        # Create a large sequence with proper sequential beat numbers
        self.large_beats = [BeatData(beat_number=i, duration=1.0) for i in range(1, 31)]

        # Create sample sequence data
        self.small_sequence = SequenceData(beats=self.sample_beats[:2])
        self.large_sequence = SequenceData(beats=self.large_beats)

        # Sample options by type
        self.small_options = {
            LetterType.TYPE1: ["option1", "option2"],
            LetterType.TYPE2: ["option3", "option4"],
        }

        self.large_options = {
            LetterType.TYPE1: ["option" + str(i) for i in range(30)],
            LetterType.TYPE2: ["option" + str(i) for i in range(30)],
        }

    def test_initial_state(self):
        """Test service starts in correct initial state."""
        self.assertTrue(self.service.can_start_update())
        self.assertEqual(self.service.get_pending_update_count(), 0)
        self.assertEqual(self.service.get_cached_section_state(LetterType.TYPE1), {})

    def test_update_lifecycle(self):
        """Test complete update lifecycle."""
        # Initially can start update
        self.assertTrue(self.service.can_start_update())

        # Start update
        self.service.start_update()
        self.assertFalse(self.service.can_start_update())

        # Finish update
        self.service.finish_update()
        self.assertTrue(self.service.can_start_update())

    def test_update_queue(self):
        """Test update queueing functionality."""
        # Initially no pending updates
        self.assertEqual(self.service.get_pending_update_count(), 0)

        # Queue an update
        self.service.queue_update(self.small_sequence, self.small_options)
        self.assertEqual(self.service.get_pending_update_count(), 1)

        # Queue another update
        self.service.queue_update(self.large_sequence, self.large_options)
        self.assertEqual(self.service.get_pending_update_count(), 2)

        # Clear pending updates
        self.service.clear_pending_updates()
        self.assertEqual(self.service.get_pending_update_count(), 0)

    def test_section_state_caching(self):
        """Test section state caching functionality."""
        # Test data
        test_state = {"active": True, "count": 5, "last_updated": "2024-01-01"}

        # Cache state
        self.service.cache_section_state(LetterType.TYPE1, test_state)

        # Retrieve cached state
        cached_state = self.service.get_cached_section_state(LetterType.TYPE1)
        self.assertEqual(cached_state, test_state)

        # Test different letter type returns empty dict
        empty_state = self.service.get_cached_section_state(LetterType.TYPE2)
        self.assertEqual(empty_state, {})

        # Clear cache
        self.service.clear_section_state_cache()
        cleared_state = self.service.get_cached_section_state(LetterType.TYPE1)
        self.assertEqual(cleared_state, {})

    def test_update_strategy_small_sequence(self):
        """Test update strategy for small sequences."""
        strategy = self.service.get_update_strategy(self.small_sequence)

        self.assertIsInstance(strategy, dict)
        self.assertIn("use_animation", strategy)
        self.assertIn("batch_size", strategy)
        self.assertIn("priority_order", strategy)
        self.assertIn("defer_heavy_operations", strategy)

        # Small sequence should enable animations
        self.assertTrue(strategy["use_animation"])
        self.assertFalse(strategy["defer_heavy_operations"])

    def test_update_strategy_large_sequence(self):
        """Test update strategy for large sequences."""
        strategy = self.service.get_update_strategy(self.large_sequence)

        # Large sequence should disable animations and defer heavy operations
        self.assertFalse(strategy["use_animation"])
        self.assertTrue(strategy["defer_heavy_operations"])

    def test_animation_disabling_logic(self):
        """Test animation disabling logic based on data size."""
        # Small dataset should not disable animations
        self.assertFalse(self.service.should_disable_animations(self.small_options))

        # Large dataset should disable animations
        self.assertTrue(self.service.should_disable_animations(self.large_options))

    def test_section_priorities(self):
        """Test section priority ordering."""
        priorities = self.service.get_section_priorities()

        self.assertIsInstance(priorities, list)
        self.assertIn(LetterType.TYPE1, priorities)
        self.assertIn(LetterType.TYPE2, priorities)

        # Should return consistent order
        priorities2 = self.service.get_section_priorities()
        self.assertEqual(priorities, priorities2)

    def test_data_validation_valid(self):
        """Test validation of valid section data."""
        validation_result = self.service.validate_section_data(self.small_options)

        self.assertIsInstance(validation_result, dict)
        self.assertIn("valid", validation_result)
        self.assertIn("errors", validation_result)
        self.assertIn("warnings", validation_result)
        self.assertIn("stats", validation_result)

        # Should be valid
        self.assertTrue(validation_result["valid"])
        self.assertEqual(len(validation_result["errors"]), 0)

    def test_data_validation_empty(self):
        """Test validation of empty section data."""
        empty_options = {}
        validation_result = self.service.validate_section_data(empty_options)

        # Should be invalid with errors
        self.assertFalse(validation_result["valid"])
        self.assertGreater(len(validation_result["errors"]), 0)

    def test_data_validation_large_dataset(self):
        """Test validation of large dataset."""
        # Create a dataset large enough to trigger warnings (100+ options per type)
        huge_options = {
            LetterType.TYPE1: ["option" + str(i) for i in range(150)],
            LetterType.TYPE2: ["option" + str(i) for i in range(150)],
        }

        validation_result = self.service.validate_section_data(huge_options)

        # Should be valid but with warnings
        self.assertTrue(validation_result["valid"])
        self.assertGreater(len(validation_result["warnings"]), 0)

        # Should have stats
        self.assertIn("stats", validation_result)
        self.assertIn("total_options", validation_result["stats"])

    def test_pending_updates_processing(self):
        """Test processing of pending updates."""
        # Queue multiple updates
        self.service.queue_update(self.small_sequence, self.small_options)
        self.service.queue_update(self.large_sequence, self.large_options)

        # Start update to block new ones
        self.service.start_update()

        # Finish update should process pending
        next_update = self.service.finish_update()

        # Should get the first queued update
        self.assertIsNotNone(next_update)
        self.assertEqual(len(next_update), 2)  # Should be tuple of (sequence, options)

        # Should have one less pending update
        self.assertEqual(self.service.get_pending_update_count(), 1)

    def test_state_cache_isolation(self):
        """Test that section state caches are isolated."""
        state1 = {"value": 1}
        state2 = {"value": 2}

        # Cache different states for different letter types
        self.service.cache_section_state(LetterType.TYPE1, state1)
        self.service.cache_section_state(LetterType.TYPE2, state2)

        # Retrieve and verify isolation
        cached1 = self.service.get_cached_section_state(LetterType.TYPE1)
        cached2 = self.service.get_cached_section_state(LetterType.TYPE2)

        self.assertEqual(cached1["value"], 1)
        self.assertEqual(cached2["value"], 2)
        self.assertNotEqual(cached1, cached2)

    def test_state_cache_copy_protection(self):
        """Test that cached states are protected from modification."""
        original_state = {"mutable": [1, 2, 3]}

        # Cache state
        self.service.cache_section_state(LetterType.TYPE1, original_state)

        # Modify original
        original_state["mutable"].append(4)

        # Cached state should not be affected
        cached_state = self.service.get_cached_section_state(LetterType.TYPE1)
        self.assertEqual(len(cached_state["mutable"]), 3)

    def test_validation_stats_accuracy(self):
        """Test accuracy of validation statistics."""
        test_options = {
            LetterType.TYPE1: ["a", "b", "c"],
            LetterType.TYPE2: ["d", "e"],
        }

        validation_result = self.service.validate_section_data(test_options)
        stats = validation_result["stats"]

        # Check individual counts
        self.assertEqual(stats[LetterType.TYPE1]["count"], 3)
        self.assertEqual(stats[LetterType.TYPE2]["count"], 2)

        # Check total count
        self.assertEqual(stats["total_options"], 5)

    def test_multiple_update_cycles(self):
        """Test multiple update cycles work correctly."""
        for i in range(5):
            # Should be able to start
            self.assertTrue(self.service.can_start_update())

            # Start update
            self.service.start_update()
            self.assertFalse(self.service.can_start_update())

            # Queue something during update
            self.service.queue_update(self.small_sequence, self.small_options)

            # Finish update
            self.service.finish_update()
            self.assertTrue(self.service.can_start_update())

    def test_priority_order_consistency(self):
        """Test that priority order is consistent and contains expected types."""
        priorities = self.service.get_section_priorities()

        # Should contain the main letter types
        expected_types = [
            LetterType.TYPE1,
            LetterType.TYPE2,
            LetterType.TYPE3,
            LetterType.TYPE4,
        ]

        for expected_type in expected_types:
            self.assertIn(expected_type, priorities)

        # Should be in the same order each time
        for _ in range(10):
            self.assertEqual(priorities, self.service.get_section_priorities())


if __name__ == "__main__":
    unittest.main()
