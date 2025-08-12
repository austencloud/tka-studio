"""Test domain model serialization."""
from __future__ import annotations

import json

from src.domain.models import (
    ArrowData,
    ArrowType,
    BeatData,
    GridData,
    GridMode,
    Location,
    MotionData,
    MotionType,
    Orientation,
    PictographData,
    PropData,
    PropType,
    RotationDirection,
    SequenceData,
)


class TestMotionDataSerialization:
    """Test MotionData serialization."""

    def test_motion_data_camel_case_serialization(self):
        """Test MotionData serialization to camelCase JSON."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
            turns=1.5,
        )

        # Serialize to camelCase
        json_str = motion.to_json()
        data = json.loads(json_str)

        # Verify camelCase keys
        assert "motionType" in data
        assert "propRotDir" in data
        assert "startLoc" in data
        assert "endLoc" in data
        assert "startOri" in data
        assert "endOri" in data

        # Verify values
        assert data["motionType"] == "pro"
        assert data["propRotDir"] == "cw"
        assert data["startLoc"] == "n"
        assert data["endLoc"] == "e"
        assert data["startOri"] == "in"
        assert data["endOri"] == "out"
        assert data["turns"] == 1.5

    def test_motion_data_round_trip_serialization(self):
        """Test complete round-trip serialization."""
        original = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.SOUTH,
            end_loc=Location.WEST,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
            turns=0.0,
        )

        # Round trip
        json_str = original.to_json()
        restored = MotionData.from_json(json_str)

        assert original == restored

    def test_motion_data_snake_case_serialization(self):
        """Test snake_case serialization still works."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,
            start_ori=Orientation.IN,
            end_ori=Orientation.IN,
        )

        json_str = motion.to_json(camel_case=False)
        data = json.loads(json_str)

        assert "motion_type" in data
        assert "prop_rot_dir" in data
        assert "start_loc" in data


class TestBeatDataSerialization:
    """Test BeatData serialization."""

    def test_beat_data_camel_case_serialization(self):
        """Test BeatData serialization to camelCase JSON."""
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,
            start_ori=Orientation.IN,
            end_ori=Orientation.IN,
        )

        red_motion = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.SOUTH,
            end_loc=Location.WEST,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
        )

        beat = BeatData(
            beat_number=1,
            letter="A",
            blue_motion=blue_motion,
            red_motion=red_motion,
            blue_reversal=True,
            is_blank=False,
        )

        # Serialize to camelCase
        json_str = beat.to_json()
        data = json.loads(json_str)

        # Verify camelCase keys
        assert "beatNumber" in data
        assert "blueMotion" in data
        assert "redMotion" in data
        assert "blueReversal" in data
        assert "isBlank" in data

        # Verify nested motion data has camelCase
        assert "motionType" in data["blueMotion"]
        assert "propRotDir" in data["blueMotion"]

        # Verify values
        assert data["beatNumber"] == 1
        assert data["letter"] == "A"
        assert data["blueReversal"]
        assert not data["isBlank"]

    def test_beat_data_round_trip_serialization(self):
        """Test complete round-trip serialization."""
        original = BeatData(beat_number=2, letter="B", is_blank=True)

        # Round trip
        json_str = original.to_json()
        restored = BeatData.from_json(json_str)

        assert original.beat_number == restored.beat_number
        assert original.letter == restored.letter
        assert original.is_blank == restored.is_blank


class TestSequenceDataSerialization:
    """Test SequenceData serialization."""

    def test_sequence_data_camel_case_serialization(self):
        """Test SequenceData serialization to camelCase JSON."""
        beat1 = BeatData(beat_number=1, letter="A")
        beat2 = BeatData(beat_number=2, letter="B")

        sequence = SequenceData(
            name="Test Sequence",
            word="AB",
            beats=[beat1, beat2],
            start_position="north",
        )

        # Serialize to camelCase
        json_str = sequence.to_json()
        data = json.loads(json_str)

        # Verify camelCase keys
        assert "startPosition" in data
        assert "beats" in data

        # Verify nested beat data has camelCase
        assert len(data["beats"]) == 2
        assert "beatNumber" in data["beats"][0]

        # Verify values
        assert data["name"] == "Test Sequence"
        assert data["word"] == "AB"
        assert data["startPosition"] == "north"

    def test_sequence_data_round_trip_serialization(self):
        """Test complete round-trip serialization."""
        original = SequenceData(name="Test", word="TEST", beats=[])

        # Round trip
        json_str = original.to_json()
        restored = SequenceData.from_json(json_str)

        assert original.name == restored.name
        assert original.word == restored.word
        assert len(original.beats) == len(restored.beats)


class TestPictographDataSerialization:
    """Test PictographData serialization."""

    def test_pictograph_data_camel_case_serialization(self):
        """Test PictographData serialization to camelCase JSON."""
        grid_data = GridData(grid_mode=GridMode.DIAMOND)
        arrow_data = ArrowData(arrow_type=ArrowType.BLUE, color="blue")
        prop_data = PropData(prop_type=PropType.STAFF, color="blue")

        pictograph = PictographData(
            grid_data=grid_data,
            arrows={"blue": arrow_data},
            props={"blue": prop_data},
            start_position="north",
            end_position="south",
            is_blank=False,
            is_mirrored=True,
        )

        # Serialize to camelCase
        json_str = pictograph.to_json()
        data = json.loads(json_str)

        # Verify camelCase keys
        assert "gridData" in data
        assert "startPosition" in data
        assert "endPosition" in data
        assert "isBlank" in data
        assert "isMirrored" in data

        # Verify nested data has camelCase
        assert "gridMode" in data["gridData"]

        # Verify values
        assert data["startPosition"] == "north"
        assert data["endPosition"] == "south"
        assert not data["isBlank"]
        assert data["isMirrored"]

    def test_pictograph_data_round_trip_serialization(self):
        """Test complete round-trip serialization."""
        original = PictographData(is_blank=True, is_mirrored=False)

        # Round trip
        json_str = original.to_json()
        restored = PictographData.from_json(json_str)

        assert original.is_blank == restored.is_blank
        assert original.is_mirrored == restored.is_mirrored
