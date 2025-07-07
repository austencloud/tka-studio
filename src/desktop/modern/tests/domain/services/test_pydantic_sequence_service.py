"""
Tests for Pydantic Sequence Service

Validates:
1. Service operations work correctly
2. Immutability is preserved
3. camelCase JSON serialization
4. Type validation and error handling
5. Integration with Pydantic models
"""

import pytest
import json
from datetime import datetime

from src.domain.services.pydantic_sequence_service import PydanticSequenceService
from src.domain.models.pydantic_models import (
    create_default_motion_data,
    create_default_beat_data,
    create_default_sequence_data,
)


class TestPydanticSequenceService:
    """Test the Pydantic-based sequence service."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = PydanticSequenceService()
    
    def test_create_sequence(self):
        """Test sequence creation."""
        sequence = self.service.create_sequence("Test Sequence", length=4)
        
        assert sequence.name == "Test Sequence"
        assert sequence.length == 4
        assert len(sequence.beats) == 0
        assert sequence.created_at is not None
        assert sequence.updated_at is not None
        assert sequence.version == "1.0"
    
    def test_create_sequence_validation(self):
        """Test sequence creation validation."""
        # Empty name should fail
        with pytest.raises(ValueError, match="Sequence name cannot be empty"):
            self.service.create_sequence("")
        
        # Invalid length should fail
        with pytest.raises(ValueError, match="Sequence length must be at least 1"):
            self.service.create_sequence("Test", length=0)
    
    def test_get_sequence(self):
        """Test sequence retrieval."""
        # Create sequence
        original = self.service.create_sequence("Test")
        
        # Retrieve sequence
        retrieved = self.service.get_sequence("Test")
        
        assert retrieved is not None
        assert retrieved.name == "Test"
        assert retrieved == original
        
        # Non-existent sequence
        assert self.service.get_sequence("NonExistent") is None
    
    def test_list_sequences(self):
        """Test listing sequences."""
        # Initially empty
        assert len(self.service.list_sequences()) == 0
        
        # Create sequences
        seq1 = self.service.create_sequence("Sequence 1")
        seq2 = self.service.create_sequence("Sequence 2")
        
        sequences = self.service.list_sequences()
        assert len(sequences) == 2
        assert seq1 in sequences
        assert seq2 in sequences
    
    def test_update_sequence(self):
        """Test sequence updates."""
        import time

        # Create sequence
        original = self.service.create_sequence("Test")
        original_updated_at = original.updated_at

        # Small delay to ensure different timestamp
        time.sleep(0.001)

        # Update sequence
        updated = self.service.update_sequence("Test", difficulty="Hard", tags=["test"])

        assert updated is not None
        assert updated.difficulty == "Hard"
        assert updated.tags == ["test"]
        assert updated.updated_at != original_updated_at
        
        # Update non-existent sequence
        assert self.service.update_sequence("NonExistent", difficulty="Easy") is None
    
    def test_delete_sequence(self):
        """Test sequence deletion."""
        # Create sequence
        self.service.create_sequence("Test")
        assert self.service.get_sequence("Test") is not None
        
        # Delete sequence
        assert self.service.delete_sequence("Test") is True
        assert self.service.get_sequence("Test") is None
        
        # Delete non-existent sequence
        assert self.service.delete_sequence("NonExistent") is False
    
    def test_add_beat(self):
        """Test adding beats to sequence."""
        # Create sequence
        sequence = self.service.create_sequence("Test")
        
        # Create beat
        beat = create_default_beat_data(1, "A")
        
        # Add beat
        updated = self.service.add_beat("Test", beat)
        
        assert updated is not None
        assert len(updated.beats) == 1
        assert updated.beats[0].letter == "A"
        assert updated.beats[0].beat_number == 1
        
        # Add beat to non-existent sequence
        assert self.service.add_beat("NonExistent", beat) is None
    
    def test_add_beat_at_position(self):
        """Test adding beats at specific positions."""
        # Create sequence with one beat
        sequence = self.service.create_sequence("Test")
        beat1 = create_default_beat_data(1, "A")
        self.service.add_beat("Test", beat1)
        
        # Insert beat at beginning
        beat2 = create_default_beat_data(2, "B")
        updated = self.service.add_beat("Test", beat2, position=0)
        
        assert len(updated.beats) == 2
        assert updated.beats[0].letter == "B"
        assert updated.beats[1].letter == "A"
    
    def test_update_beat(self):
        """Test updating beats in sequence."""
        # Create sequence with beat
        sequence = self.service.create_sequence("Test")
        beat = create_default_beat_data(1, "A")
        self.service.add_beat("Test", beat)
        
        # Update beat
        new_beat = create_default_beat_data(1, "B")
        updated = self.service.update_beat("Test", 0, new_beat)
        
        assert updated is not None
        assert updated.beats[0].letter == "B"
        
        # Update non-existent beat
        assert self.service.update_beat("Test", 10, new_beat) is None
        
        # Update beat in non-existent sequence
        assert self.service.update_beat("NonExistent", 0, new_beat) is None
    
    def test_remove_beat(self):
        """Test removing beats from sequence."""
        # Create sequence with beats
        sequence = self.service.create_sequence("Test")
        beat1 = create_default_beat_data(1, "A")
        beat2 = create_default_beat_data(2, "B")
        self.service.add_beat("Test", beat1)
        self.service.add_beat("Test", beat2)
        
        # Remove first beat
        updated = self.service.remove_beat("Test", 0)
        
        assert updated is not None
        assert len(updated.beats) == 1
        assert updated.beats[0].letter == "B"
        
        # Remove non-existent beat
        assert self.service.remove_beat("Test", 10) is None
        
        # Remove beat from non-existent sequence
        assert self.service.remove_beat("NonExistent", 0) is None
    
    def test_sequence_to_json_camel_case(self):
        """Test sequence serialization to camelCase JSON."""
        sequence = self.service.create_sequence("Test Sequence")
        beat = create_default_beat_data(1, "A")
        sequence = self.service.add_beat("Test Sequence", beat)
        
        json_str = self.service.sequence_to_json(sequence)
        json_data = json.loads(json_str)
        
        # Check top-level camelCase
        assert 'createdAt' in json_data
        assert 'updatedAt' in json_data
        assert 'beatCount' not in json_data  # This would be snake_case
        
        # Check nested beat camelCase
        beat_data = json_data['beats'][0]
        assert 'beatNumber' in beat_data
        assert 'blueMotion' in beat_data
        assert 'redMotion' in beat_data
        
        # Check nested motion camelCase
        motion_data = beat_data['blueMotion']
        assert 'motionType' in motion_data
        assert 'propRotDir' in motion_data
        assert 'startLoc' in motion_data
    
    def test_sequence_from_json(self):
        """Test sequence deserialization from camelCase JSON."""
        # Create sequence and serialize
        original = self.service.create_sequence("Test")
        beat = create_default_beat_data(1, "A")
        original = self.service.add_beat("Test", beat)
        json_str = self.service.sequence_to_json(original)
        
        # Deserialize
        restored = self.service.sequence_from_json(json_str)
        
        assert restored.name == original.name
        assert len(restored.beats) == len(original.beats)
        assert restored.beats[0].letter == original.beats[0].letter
    
    def test_export_import_sequence(self):
        """Test sequence export/import functionality."""
        # Create and populate sequence
        sequence = self.service.create_sequence("Export Test")
        beat = create_default_beat_data(1, "A")
        self.service.add_beat("Export Test", beat)
        
        # Export sequence
        exported_json = self.service.export_sequence("Export Test")
        assert exported_json is not None
        
        # Clear service and import
        self.service.delete_sequence("Export Test")
        imported = self.service.import_sequence(exported_json)
        
        assert imported.name == "Export Test"
        assert len(imported.beats) == 1
        assert imported.beats[0].letter == "A"
        
        # Export non-existent sequence
        assert self.service.export_sequence("NonExistent") is None
    
    def test_create_sample_sequence(self):
        """Test sample sequence creation."""
        sequence = self.service.create_sample_sequence("Sample")
        
        assert sequence.name == "Sample"
        assert len(sequence.beats) == 4
        
        # Check that beats have different properties
        letters = [beat.letter for beat in sequence.beats]
        assert letters == ['A', 'B', 'C', 'D']
        
        # Check motion variety
        motion_types = [beat.blue_motion.motion_type for beat in sequence.beats]
        assert 'pro' in motion_types
        assert 'anti' in motion_types
    
    def test_get_sequence_stats(self):
        """Test sequence statistics."""
        # Create sample sequence
        sequence = self.service.create_sample_sequence("Stats Test")
        
        stats = self.service.get_sequence_stats("Stats Test")
        
        assert stats is not None
        assert stats['name'] == "Stats Test"
        assert stats['beatCount'] == 4
        assert stats['totalMotions'] == 8  # 4 beats * 2 motions each
        assert 'motionTypeDistribution' in stats
        assert 'createdAt' in stats
        assert 'updatedAt' in stats
        
        # Stats for non-existent sequence
        assert self.service.get_sequence_stats("NonExistent") is None
    
    def test_immutability(self):
        """Test that operations maintain immutability."""
        # Create sequence
        original = self.service.create_sequence("Immutable Test")
        original_id = id(original)
        
        # Add beat - should return new object
        beat = create_default_beat_data(1, "A")
        updated = self.service.add_beat("Immutable Test", beat)
        
        assert id(updated) != original_id
        assert len(original.beats) == 0  # Original unchanged
        assert len(updated.beats) == 1   # New object has beat
        
        # Update sequence - should return new object
        updated2 = self.service.update_sequence("Immutable Test", difficulty="Hard")
        
        assert id(updated2) != id(updated)
        assert updated.difficulty is None    # Previous object unchanged
        assert updated2.difficulty == "Hard" # New object has update
    
    def test_json_round_trip_compatibility(self):
        """Test that JSON can round-trip through the service."""
        # Create complex sequence
        sequence = self.service.create_sample_sequence("Round Trip Test")
        
        # Export to JSON
        json_str = self.service.export_sequence("Round Trip Test")
        
        # Delete original
        self.service.delete_sequence("Round Trip Test")
        
        # Import from JSON
        imported = self.service.import_sequence(json_str)
        
        # Export again
        json_str2 = self.service.export_sequence("Round Trip Test")
        
        # Should be identical
        assert json_str == json_str2
        
        # Verify data integrity
        assert imported.name == "Round Trip Test"
        assert len(imported.beats) == 4
