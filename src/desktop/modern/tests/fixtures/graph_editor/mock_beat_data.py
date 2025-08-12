#!/usr/bin/env python3
"""
Mock Beat Data Fixtures for Graph Editor Testing
===============================================

Provides comprehensive mock beat data fixtures following TKA immutable
domain model patterns for consistent testing.
"""

import sys
from pathlib import Path
from typing import List, Optional

# Add modern source to path
modern_src = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))

from domain.models import (
    ArrowData,
    BeatData,
    GridData,
    Location,
    MotionData,
    MotionType,
    PictographData,
    RotationDirection,
    SequenceData,
)

from application.services.sequence.beat_factory import BeatFactory


def create_sample_motion_data(
    motion_type: MotionType = MotionType.PRO,
    prop_rot_dir: RotationDirection = RotationDirection.CLOCKWISE,
    start_loc: Location = Location.NORTH,
    end_loc: Location = Location.SOUTH,
    turns: float = 1.0,
    start_ori: str = "in",
    end_ori: str = "out",
) -> MotionData:
    """Create sample motion data with customizable parameters."""
    return MotionData(
        motion_type=motion_type,
        prop_rot_dir=prop_rot_dir,
        start_loc=start_loc,
        end_loc=end_loc,
        turns=turns,
        start_ori=start_ori,
        end_ori=end_ori,
    )


def create_sample_beat_data(
    beat_number: int = 1,
    letter: str = "A",
    duration: float = 1.0,
    blue_motion: Optional[MotionData] = None,
    red_motion: Optional[MotionData] = None,
    metadata: Optional[dict] = None,
) -> BeatData:
    """Create sample beat data with embedded pictograph."""
    if blue_motion is None:
        blue_motion = create_sample_motion_data(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
        )

    if red_motion is None:
        red_motion = create_sample_motion_data(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.EAST,
            end_loc=Location.WEST,
            turns=0.5,
        )

    # Create pictograph data with motions
    pictograph_data = PictographData(
        grid_data=GridData(),
        arrows={"blue": ArrowData(color="blue"), "red": ArrowData(color="red")},
        motions={"blue": blue_motion, "red": red_motion},
        letter=letter,
        start_position="alpha1",
        end_position="beta5",
    )

    # Use factory to create beat with embedded pictograph
    return BeatFactory.create_from_pictograph(
        pictograph_data=pictograph_data,
        beat_number=beat_number,
        duration=duration,
        metadata=metadata,
    )


def create_start_position_beat() -> BeatData:
    """Create a start position beat for testing."""
    # Create pictograph data for start position
    pictograph_data = PictographData(
        grid_data=GridData(),
        arrows={"blue": ArrowData(color="blue"), "red": ArrowData(color="red")},
        motions={
            "blue": create_sample_motion_data(),
            "red": create_sample_motion_data(),
        },
        letter="A",
        start_position="alpha1",
        end_position="alpha1",  # Start position ends where it starts
    )

    # Use factory to create start position beat
    return BeatFactory.create_start_position_beat(pictograph_data)


def create_regular_beat(beat_number: int = 2, letter: str = "B") -> BeatData:
    """Create a regular beat for testing."""
    return create_sample_beat_data(
        beat_number=beat_number, letter=letter, metadata={"is_start_position": False}
    )


def create_complex_beat() -> BeatData:
    """Create a complex beat with varied motion data."""
    blue_motion = create_sample_motion_data(
        motion_type=MotionType.STATIC,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        start_loc=Location.NORTHEAST,
        end_loc=Location.SOUTHWEST,
        turns=2.5,
    )

    red_motion = create_sample_motion_data(
        motion_type=MotionType.DASH,
        prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
        start_loc=Location.NORTHWEST,
        end_loc=Location.SOUTHEAST,
        turns=1.5,
    )

    return create_sample_beat_data(
        beat_number=3,
        letter="C",
        blue_motion=blue_motion,
        red_motion=red_motion,
        metadata={"complexity": "high", "test_case": "complex_motions"},
    )


def create_sample_sequence_data(
    name: str = "Test Sequence",
    word: str = "ABC",
    beats: Optional[List[BeatData]] = None,
    start_position: str = "alpha1",
) -> SequenceData:
    """Create sample sequence data with customizable parameters."""
    if beats is None:
        beats = [
            create_start_position_beat(),
            create_regular_beat(2, "B"),
            create_complex_beat(),
        ]

    return SequenceData(
        name=name, word=word, beats=beats, start_position=start_position
    )


def create_empty_sequence() -> SequenceData:
    """Create an empty sequence for testing."""
    return SequenceData.empty()


def create_single_beat_sequence() -> SequenceData:
    """Create a sequence with a single beat."""
    return create_sample_sequence_data(
        name="Single Beat", word="A", beats=[create_start_position_beat()]
    )


def create_long_sequence(length: int = 8) -> SequenceData:
    """Create a longer sequence for performance testing."""
    beats = []
    for i in range(length):
        beat_number = i + 1
        letter = chr(ord("A") + (i % 26))  # Cycle through alphabet

        if i == 0:
            beats.append(create_start_position_beat())
        else:
            beats.append(create_regular_beat(beat_number, letter))

    return create_sample_sequence_data(
        name=f"Long Sequence ({length} beats)",
        word="".join(chr(ord("A") + (i % 26)) for i in range(length)),
        beats=beats,
    )


# Test data collections for different scenarios
class GraphEditorTestData:
    """Collection of test data for different graph editor scenarios."""

    @staticmethod
    def get_basic_test_data() -> dict:
        """Get basic test data for simple scenarios."""
        return {
            "beat": create_sample_beat_data(),
            "sequence": create_sample_sequence_data(),
            "start_beat": create_start_position_beat(),
            "regular_beat": create_regular_beat(),
        }

    @staticmethod
    def get_complex_test_data() -> dict:
        """Get complex test data for advanced scenarios."""
        return {
            "complex_beat": create_complex_beat(),
            "long_sequence": create_long_sequence(8),
            "empty_sequence": create_empty_sequence(),
            "single_beat_sequence": create_single_beat_sequence(),
        }

    @staticmethod
    def get_edge_case_data() -> dict:
        """Get edge case test data."""
        # Beat with no motions
        no_motion_beat = BeatData(
            beat_number=1, letter="X", duration=1.0, blue_motion=None, red_motion=None
        )

        # Beat with only blue motion
        blue_only_beat = create_sample_beat_data(red_motion=None)

        # Beat with only red motion
        red_only_beat = create_sample_beat_data(blue_motion=None)

        return {
            "no_motion_beat": no_motion_beat,
            "blue_only_beat": blue_only_beat,
            "red_only_beat": red_only_beat,
            "zero_turns_beat": create_sample_beat_data(
                blue_motion=create_sample_motion_data(turns=0.0),
                red_motion=create_sample_motion_data(turns=0.0),
            ),
        }


# Convenience functions for pytest fixtures
def pytest_sample_beat_data():
    """Pytest fixture function for sample beat data."""
    return create_sample_beat_data()


def pytest_sample_sequence_data():
    """Pytest fixture function for sample sequence data."""
    return create_sample_sequence_data()


def pytest_graph_editor_test_data():
    """Pytest fixture function for comprehensive test data."""
    return {
        **GraphEditorTestData.get_basic_test_data(),
        **GraphEditorTestData.get_complex_test_data(),
        **GraphEditorTestData.get_edge_case_data(),
    }
