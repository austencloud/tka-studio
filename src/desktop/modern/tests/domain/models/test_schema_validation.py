"""
Schema Validation Tests

Tests that Pydantic domain models produce JSON that validates against
the v2 JSON schemas we created for cross-platform compatibility.
"""

import json
import pytest
from pathlib import Path
from jsonschema import validate, RefResolver, ValidationError

from domain.models.pydantic_models import (
    MotionData,
    BeatData,
    SequenceData,
    create_default_motion_data,
    create_default_beat_data,
    create_default_sequence_data,
)


class TestSchemaValidation:
    """Test that Python models validate against JSON schemas."""
    
    @pytest.fixture
    def schema_dir(self):
        """Get the schemas directory."""
        # Use relative path from current working directory to schemas
        # When tests run, cwd should be src/desktop/modern, so go up to TKA root
        return Path("../../../schemas").resolve()
    
    @pytest.fixture
    def motion_schema(self, schema_dir):
        """Load the motion data schema with reference resolution."""
        schema_path = schema_dir / "motion-data.json"
        with open(schema_path) as f:
            schema = json.load(f)

        # Load core-enums.json for reference resolution
        core_enums_path = schema_dir / "core-enums.json"
        with open(core_enums_path) as f:
            core_enums = json.load(f)

        # Create resolver with the core enums schema
        resolver = RefResolver(
            base_uri=schema["$id"],
            referrer=schema,
            store={
                "https://tka.dev/schemas/core-enums.json": core_enums
            }
        )

        return schema, resolver
    
    @pytest.fixture
    def beat_schema(self, schema_dir):
        """Load the beat data schema with reference resolution."""
        schema_path = schema_dir / "beat-data.json"
        with open(schema_path) as f:
            schema = json.load(f)

        # Load referenced schemas
        motion_schema_path = schema_dir / "motion-data.json"
        with open(motion_schema_path) as f:
            motion_schema = json.load(f)

        core_enums_path = schema_dir / "core-enums.json"
        with open(core_enums_path) as f:
            core_enums = json.load(f)

        glyph_data_path = schema_dir / "glyph-data.json"
        with open(glyph_data_path) as f:
            glyph_data = json.load(f)

        # Create resolver with all referenced schemas
        resolver = RefResolver(
            base_uri=schema["$id"],
            referrer=schema,
            store={
                "https://tka.dev/schemas/motion-data.json": motion_schema,
                "https://tka.dev/schemas/core-enums.json": core_enums,
                "https://tka.dev/schemas/glyph-data.json": glyph_data
            }
        )

        return schema, resolver
    
    @pytest.fixture
    def sequence_schema(self, schema_dir):
        """Load the sequence data schema with reference resolution."""
        schema_path = schema_dir / "sequence-data.json"
        with open(schema_path) as f:
            schema = json.load(f)

        # Load referenced schemas
        beat_schema_path = schema_dir / "beat-data.json"
        with open(beat_schema_path) as f:
            beat_schema = json.load(f)

        motion_schema_path = schema_dir / "motion-data.json"
        with open(motion_schema_path) as f:
            motion_schema = json.load(f)

        core_enums_path = schema_dir / "core-enums.json"
        with open(core_enums_path) as f:
            core_enums = json.load(f)

        # Create resolver with all referenced schemas
        resolver = RefResolver(
            base_uri=schema["$id"],
            referrer=schema,
            store={
                "https://tka.dev/schemas/beat-data.json": beat_schema,
                "https://tka.dev/schemas/motion-data.json": motion_schema,
                "https://tka.dev/schemas/core-enums.json": core_enums
            }
        )

        return schema, resolver
    
    def test_motion_data_validates_against_schema(self, motion_schema):
        """Test that MotionData JSON validates against motion-data-v2.json schema."""
        schema, resolver = motion_schema

        motion = create_default_motion_data(
            motion_type='pro',
            prop_rot_dir='cw',
            start_loc='n',
            end_loc='e',
            start_ori='in',
            end_ori='out'
        )

        json_data = motion.model_dump()

        # Should validate without errors
        validate(instance=json_data, schema=schema, resolver=resolver)
        
        # Verify structure matches schema expectations
        assert json_data['motionType'] == 'pro'
        assert json_data['propRotDir'] == 'cw'
        assert json_data['startLoc'] == 'n'
        assert json_data['endLoc'] == 'e'
        assert json_data['startOri'] == 'in'
        assert json_data['endOri'] == 'out'
    
    def test_beat_data_validates_against_schema(self, beat_schema):
        """Test that BeatData JSON validates against beat-data-v2.json schema."""
        schema, resolver = beat_schema

        blue_motion = create_default_motion_data(motion_type='pro')
        red_motion = create_default_motion_data(motion_type='anti')

        beat = BeatData(
            beat_number=1,
            letter='A',
            duration=1.5,
            blue_motion=blue_motion,
            red_motion=red_motion,
            filled=True
        )

        json_data = beat.model_dump()

        # Should validate without errors
        validate(instance=json_data, schema=schema, resolver=resolver)
        
        # Verify structure
        assert json_data['beatNumber'] == 1
        assert json_data['letter'] == 'A'
        assert json_data['duration'] == 1.5
        assert json_data['filled'] == True
        assert 'blueMotion' in json_data
        assert 'redMotion' in json_data
    
    def test_sequence_data_validates_against_schema(self, sequence_schema):
        """Test that SequenceData JSON validates against sequence-data-v2.json schema."""
        schema, resolver = sequence_schema

        sequence = create_default_sequence_data("Test Sequence", 4)
        beat1 = create_default_beat_data(1, 'A')
        beat2 = create_default_beat_data(2, 'B')

        sequence = sequence.add_beat(beat1)
        sequence = sequence.add_beat(beat2)

        json_data = sequence.model_dump()

        # Should validate without errors
        validate(instance=json_data, schema=schema, resolver=resolver)
        
        # Verify structure
        assert json_data['name'] == "Test Sequence"
        assert len(json_data['beats']) == 2
        assert json_data['beats'][0]['letter'] == 'A'
        assert json_data['beats'][1]['letter'] == 'B'
    
    def test_all_motion_types_validate(self, motion_schema):
        """Test that all motion types validate against schema."""
        schema, resolver = motion_schema
        motion_types = ['pro', 'anti', 'float', 'dash', 'static']

        for motion_type in motion_types:
            motion = create_default_motion_data(motion_type=motion_type)
            json_data = motion.model_dump()

            # Should validate without errors
            validate(instance=json_data, schema=schema, resolver=resolver)
            assert json_data['motionType'] == motion_type
    
    def test_all_orientations_validate(self, motion_schema):
        """Test that all orientations validate against schema."""
        schema, resolver = motion_schema
        orientations = ['in', 'out', 'clock', 'counter']

        for ori in orientations:
            motion = create_default_motion_data(start_ori=ori, end_ori=ori)
            json_data = motion.model_dump()

            # Should validate without errors
            validate(instance=json_data, schema=schema, resolver=resolver)
            assert json_data['startOri'] == ori
            assert json_data['endOri'] == ori
    
    def test_invalid_data_fails_validation(self, motion_schema):
        """Test that invalid data fails schema validation."""
        schema, resolver = motion_schema

        # Create motion with invalid motion_type
        motion = create_default_motion_data()
        json_data = motion.model_dump()

        # Manually corrupt the data
        json_data['motionType'] = 'invalid_type'

        # Should fail validation
        with pytest.raises(ValidationError):
            validate(instance=json_data, schema=schema, resolver=resolver)
    
    def test_round_trip_compatibility(self, motion_schema):
        """Test that data can round-trip through JSON and still validate."""
        schema, resolver = motion_schema

        original_motion = create_default_motion_data(
            motion_type='anti',
            prop_rot_dir='ccw',
            start_loc='ne',
            end_loc='sw'
        )

        # Serialize to JSON string
        json_str = original_motion.model_dump_json()

        # Parse back to dict
        json_data = json.loads(json_str)

        # Should still validate against schema
        validate(instance=json_data, schema=schema, resolver=resolver)
        
        # Should be able to recreate the object
        restored_motion = MotionData(**json_data)
        assert restored_motion == original_motion


class TestCrossPlatformCompatibility:
    """Test compatibility between Python models and expected web formats."""
    
    def test_motion_data_matches_web_expectations(self):
        """Test that MotionData JSON matches what web app expects."""
        motion = create_default_motion_data(
            motion_type='pro',
            prop_rot_dir='cw',
            start_loc='n',
            end_loc='e',
            start_ori='in',
            end_ori='out'
        )
        
        json_data = motion.model_dump()
        
        # Should match the web TypeScript interface exactly
        expected_keys = {
            'motionType', 'propRotDir', 'startLoc', 
            'endLoc', 'turns', 'startOri', 'endOri'
        }
        assert set(json_data.keys()) == expected_keys
        
        # All values should be JSON-serializable types
        assert isinstance(json_data['motionType'], str)
        assert isinstance(json_data['propRotDir'], str)
        assert isinstance(json_data['startLoc'], str)
        assert isinstance(json_data['endLoc'], str)
        assert isinstance(json_data['turns'], (int, float))
        assert isinstance(json_data['startOri'], str)
        assert isinstance(json_data['endOri'], str)
    
    def test_beat_data_matches_web_expectations(self):
        """Test that BeatData JSON matches what web app expects."""
        beat = create_default_beat_data(1, 'A')
        json_data = beat.model_dump()
        
        # Should have camelCase keys
        web_expected_keys = {
            'beatNumber', 'letter', 'duration', 'blueMotion', 
            'redMotion', 'blueReversal', 'redReversal', 'filled', 'tags'
        }
        
        # All expected keys should be present
        for key in web_expected_keys:
            assert key in json_data, f"Missing expected key: {key}"
        
        # Nested motion data should also be camelCase
        assert 'motionType' in json_data['blueMotion']
        assert 'propRotDir' in json_data['redMotion']
    
    def test_sequence_data_matches_web_expectations(self):
        """Test that SequenceData JSON matches what web app expects."""
        sequence = create_default_sequence_data("Test")
        beat = create_default_beat_data(1, 'A')
        sequence = sequence.add_beat(beat)
        
        json_data = sequence.model_dump()
        
        # Should have web-compatible structure
        assert 'name' in json_data
        assert 'beats' in json_data
        assert 'version' in json_data
        assert 'length' in json_data
        
        # Beats should be an array of properly formatted beat objects
        assert isinstance(json_data['beats'], list)
        assert len(json_data['beats']) == 1
        
        beat_data = json_data['beats'][0]
        assert 'beatNumber' in beat_data
        assert 'blueMotion' in beat_data
        assert 'redMotion' in beat_data
