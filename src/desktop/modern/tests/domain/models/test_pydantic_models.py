"""
Tests for Pydantic Domain Models

Validates:
1. Python snake_case usage works correctly
2. JSON serialization produces camelCase
3. Both naming conventions are accepted (populate_by_name=True)
4. Immutability is preserved
5. Type validation works
6. Schema compatibility
"""

import pytest
import json
from typing import Dict, Any

from src.domain.models.pydantic_models import (
    MotionData,
    PictographData,
    BeatData,
    SequenceData,
    create_default_motion_data,
    create_default_beat_data,
    create_default_sequence_data,
)


class TestMotionData:
    """Test MotionData with camelCase serialization."""
    
    def test_snake_case_creation(self):
        """Test creating MotionData with snake_case (Python style)."""
        motion = MotionData(
            motion_type='pro',
            prop_rot_dir='cw',
            start_loc='n',
            end_loc='e',
            turns=1.5,
            start_ori='in',
            end_ori='out'
        )
        
        assert motion.motion_type == 'pro'
        assert motion.prop_rot_dir == 'cw'
        assert motion.start_loc == 'n'
        assert motion.end_loc == 'e'
        assert motion.turns == 1.5
        assert motion.start_ori == 'in'
        assert motion.end_ori == 'out'
    
    def test_camel_case_json_serialization(self):
        """Test that JSON output uses camelCase."""
        motion = create_default_motion_data()
        json_data = motion.model_dump()
        
        # Should have camelCase keys
        assert 'motionType' in json_data
        assert 'propRotDir' in json_data
        assert 'startLoc' in json_data
        assert 'endLoc' in json_data
        assert 'startOri' in json_data
        assert 'endOri' in json_data
        
        # Should NOT have snake_case keys
        assert 'motion_type' not in json_data
        assert 'prop_rot_dir' not in json_data
        assert 'start_loc' not in json_data
    
    def test_camel_case_json_string(self):
        """Test JSON string serialization."""
        motion = create_default_motion_data()
        json_str = motion.model_dump_json()
        json_data = json.loads(json_str)
        
        expected_keys = {
            'motionType', 'propRotDir', 'startLoc', 
            'endLoc', 'turns', 'startOri', 'endOri'
        }
        assert set(json_data.keys()) == expected_keys
    
    def test_populate_by_name_snake_case(self):
        """Test that snake_case input is accepted (populate_by_name=True)."""
        data = {
            'motion_type': 'anti',
            'prop_rot_dir': 'ccw',
            'start_loc': 's',
            'end_loc': 'w',
            'turns': 2.0,
            'start_ori': 'out',
            'end_ori': 'clock'
        }
        
        motion = MotionData(**data)
        assert motion.motion_type == 'anti'
        assert motion.prop_rot_dir == 'ccw'
    
    def test_populate_by_name_camel_case(self):
        """Test that camelCase input is accepted (populate_by_name=True)."""
        data = {
            'motionType': 'float',
            'propRotDir': 'no_rot',
            'startLoc': 'ne',
            'endLoc': 'sw',
            'turns': 0.5,
            'startOri': 'counter',
            'endOri': 'in'
        }
        
        motion = MotionData(**data)
        assert motion.motion_type == 'float'
        assert motion.prop_rot_dir == 'no_rot'
    
    def test_immutability(self):
        """Test that models are immutable (frozen=True)."""
        motion = create_default_motion_data()
        
        with pytest.raises(ValueError, match="Instance is frozen"):
            motion.motion_type = 'anti'
    
    def test_type_validation(self):
        """Test that invalid values are rejected."""
        with pytest.raises(ValueError):
            MotionData(
                motion_type='invalid_type',  # Invalid enum value
                prop_rot_dir='cw',
                start_loc='n',
                end_loc='e',
                turns=0,
                start_ori='in',
                end_ori='in'
            )


class TestBeatData:
    """Test BeatData with nested MotionData."""
    
    def test_beat_creation_with_motions(self):
        """Test creating BeatData with motion data."""
        blue_motion = create_default_motion_data(motion_type='pro')
        red_motion = create_default_motion_data(motion_type='anti')
        
        beat = BeatData(
            beat_number=1,
            letter='A',
            duration=1.5,
            blue_motion=blue_motion,
            red_motion=red_motion
        )
        
        assert beat.beat_number == 1
        assert beat.letter == 'A'
        assert beat.duration == 1.5
        assert beat.blue_motion.motion_type == 'pro'
        assert beat.red_motion.motion_type == 'anti'
    
    def test_beat_json_serialization(self):
        """Test that BeatData serializes with camelCase."""
        beat = create_default_beat_data(1, 'A')
        json_data = beat.model_dump()
        
        # Top-level should be camelCase
        assert 'beatNumber' in json_data
        assert 'blueMotion' in json_data
        assert 'redMotion' in json_data
        assert 'pictographData' in json_data
        
        # Nested motion should also be camelCase
        blue_motion = json_data['blueMotion']
        assert 'motionType' in blue_motion
        assert 'propRotDir' in blue_motion
    
    def test_beat_validation(self):
        """Test BeatData validation."""
        with pytest.raises(ValueError):
            BeatData(
                beat_number=-1,  # Should be >= 0
                letter='A',
                blue_motion=create_default_motion_data(),
                red_motion=create_default_motion_data()
            )


class TestSequenceData:
    """Test SequenceData with immutable operations."""
    
    def test_sequence_creation(self):
        """Test creating a sequence."""
        sequence = create_default_sequence_data("Test Sequence", 4)
        
        assert sequence.name == "Test Sequence"
        assert sequence.length == 4
        assert len(sequence.beats) == 0
    
    def test_add_beat_immutable(self):
        """Test that add_beat returns a new sequence."""
        sequence = create_default_sequence_data("Test", 2)
        beat = create_default_beat_data(1, 'A')
        
        new_sequence = sequence.add_beat(beat)
        
        # Original sequence unchanged
        assert len(sequence.beats) == 0
        
        # New sequence has the beat
        assert len(new_sequence.beats) == 1
        assert new_sequence.beats[0].letter == 'A'
        
        # Different objects
        assert sequence is not new_sequence
    
    def test_update_beat_immutable(self):
        """Test that update_beat returns a new sequence."""
        sequence = create_default_sequence_data("Test", 2)
        beat1 = create_default_beat_data(1, 'A')
        beat2 = create_default_beat_data(2, 'B')
        
        sequence = sequence.add_beat(beat1)
        new_sequence = sequence.update_beat(0, beat2)
        
        # Original sequence unchanged
        assert sequence.beats[0].letter == 'A'
        
        # New sequence has updated beat
        assert new_sequence.beats[0].letter == 'B'
    
    def test_sequence_json_serialization(self):
        """Test sequence JSON serialization."""
        sequence = create_default_sequence_data("Test Sequence")
        beat = create_default_beat_data(1, 'A')
        sequence = sequence.add_beat(beat)
        
        json_data = sequence.model_dump()
        
        # Top-level camelCase
        assert 'createdAt' in json_data
        assert 'updatedAt' in json_data
        
        # Nested beats should be camelCase
        beat_data = json_data['beats'][0]
        assert 'beatNumber' in beat_data
        assert 'blueMotion' in beat_data


class TestSchemaCompatibility:
    """Test compatibility with @tka/domain TypeScript schemas."""
    
    def test_motion_data_schema_compatibility(self):
        """Test that MotionData JSON matches TypeScript schema."""
        motion = create_default_motion_data(
            motion_type='pro',
            prop_rot_dir='cw',
            start_loc='n',
            end_loc='e',
            start_ori='in',
            end_ori='in'
        )
        
        json_data = motion.model_dump()
        
        # Should match TypeScript MotionData interface exactly
        expected_structure = {
            'motionType': str,
            'propRotDir': str,
            'startLoc': str,
            'endLoc': str,
            'turns': (int, float),
            'startOri': str,
            'endOri': str
        }
        
        for key, expected_type in expected_structure.items():
            assert key in json_data
            assert isinstance(json_data[key], expected_type)
    
    def test_round_trip_compatibility(self):
        """Test that data can round-trip through JSON."""
        original_motion = create_default_motion_data()
        
        # Serialize to JSON (camelCase)
        json_str = original_motion.model_dump_json()
        json_data = json.loads(json_str)
        
        # Deserialize back (should accept camelCase due to populate_by_name)
        restored_motion = MotionData(**json_data)
        
        assert restored_motion == original_motion


class TestFactoryFunctions:
    """Test factory functions for easy object creation."""
    
    def test_create_default_motion_data(self):
        """Test default motion data creation."""
        motion = create_default_motion_data()
        
        assert motion.motion_type == 'pro'
        assert motion.prop_rot_dir == 'cw'
        assert motion.start_loc == 'n'
        assert motion.end_loc == 'e'
        assert motion.turns == 0.0
    
    def test_create_default_beat_data(self):
        """Test default beat data creation."""
        beat = create_default_beat_data(1, 'A')
        
        assert beat.beat_number == 1
        assert beat.letter == 'A'
        assert beat.duration == 1.0
        assert beat.blue_motion.motion_type == 'pro'
        assert beat.red_motion.motion_type == 'pro'
    
    def test_create_default_sequence_data(self):
        """Test default sequence data creation."""
        sequence = create_default_sequence_data("Test", 8)
        
        assert sequence.name == "Test"
        assert sequence.length == 8
        assert len(sequence.beats) == 0
