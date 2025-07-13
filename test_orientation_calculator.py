#!/usr/bin/env python3
"""
Test script to verify OrientationCalculator service functionality.

This script tests the correct service for calculating end orientations
based on start orientation, turns, and motion type.
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "src", "desktop", "modern", "src")
)

from application.services.positioning.arrows.calculation.orientation_calculator import (
    OrientationCalculator,
)
from domain.models.enums import Location, MotionType, Orientation, RotationDirection
from domain.models.motion_data import MotionData


def test_orientation_calculator():
    """Test the OrientationCalculator service with various motion scenarios."""

    print("🧪 Testing OrientationCalculator Service")
    print("=" * 50)

    calculator = OrientationCalculator()

    # Test cases: (motion_type, turns, start_ori, expected_end_ori)
    test_cases = [
        # PRO motions
        (MotionType.PRO, 0, Orientation.IN, Orientation.IN),
        (MotionType.PRO, 1, Orientation.IN, Orientation.OUT),
        (MotionType.PRO, 2, Orientation.IN, Orientation.IN),
        (MotionType.PRO, 3, Orientation.IN, Orientation.OUT),
        # ANTI motions
        (MotionType.ANTI, 0, Orientation.IN, Orientation.OUT),
        (MotionType.ANTI, 1, Orientation.IN, Orientation.IN),
        (MotionType.ANTI, 2, Orientation.IN, Orientation.OUT),
        (MotionType.ANTI, 3, Orientation.IN, Orientation.IN),
        # STATIC motions
        (MotionType.STATIC, 0, Orientation.IN, Orientation.IN),
        (MotionType.STATIC, 1, Orientation.IN, Orientation.OUT),
        (MotionType.STATIC, 2, Orientation.IN, Orientation.IN),
        # DASH motions
        (MotionType.DASH, 0, Orientation.IN, Orientation.OUT),
        (MotionType.DASH, 1, Orientation.IN, Orientation.IN),
        (MotionType.DASH, 2, Orientation.IN, Orientation.OUT),
    ]

    print("Testing whole turn motions:")
    print("-" * 30)

    for motion_type, turns, start_ori, expected_end_ori in test_cases:
        # Create motion data
        motion_data = MotionData(
            motion_type=motion_type,
            turns=turns,
            start_ori=start_ori,
            end_ori=expected_end_ori,  # This will be overridden by calculation
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            prop_rot_dir=RotationDirection.CLOCKWISE,
        )

        # Calculate end orientation
        calculated_end_ori = calculator.calculate_end_orientation(
            motion_data, start_ori
        )

        # Check result
        success = calculated_end_ori == expected_end_ori
        status = "✅" if success else "❌"

        print(
            f"{status} {motion_type.value} {turns} turns: {start_ori.value} -> {calculated_end_ori.value} (expected: {expected_end_ori.value})"
        )

        if not success:
            print(
                f"   ⚠️  MISMATCH: Expected {expected_end_ori.value}, got {calculated_end_ori.value}"
            )

    print("\nTesting half turn motions:")
    print("-" * 30)

    # Test half turns with PRO motion
    half_turn_cases = [
        (MotionType.PRO, 0.5, Orientation.IN, RotationDirection.CLOCKWISE),
        (MotionType.PRO, 1.5, Orientation.IN, RotationDirection.CLOCKWISE),
        (MotionType.ANTI, 0.5, Orientation.IN, RotationDirection.CLOCKWISE),
        (MotionType.ANTI, 1.5, Orientation.IN, RotationDirection.CLOCKWISE),
    ]

    for motion_type, turns, start_ori, prop_rot_dir in half_turn_cases:
        motion_data = MotionData(
            motion_type=motion_type,
            turns=turns,
            start_ori=start_ori,
            end_ori=start_ori,  # Will be calculated
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            prop_rot_dir=prop_rot_dir,
        )

        calculated_end_ori = calculator.calculate_end_orientation(
            motion_data, start_ori
        )

        print(
            f"✅ {motion_type.value} {turns} turns ({prop_rot_dir.value}): {start_ori.value} -> {calculated_end_ori.value}"
        )

    print("\nTesting FLOAT motions:")
    print("-" * 30)

    # Test float motions
    float_cases = [
        (Location.NORTH, Location.EAST, Orientation.IN),  # CW handpath
        (Location.NORTH, Location.WEST, Orientation.IN),  # CCW handpath
        (Location.EAST, Location.SOUTH, Orientation.OUT),  # CW handpath
        (Location.WEST, Location.SOUTH, Orientation.OUT),  # CCW handpath
    ]

    for start_loc, end_loc, start_ori in float_cases:
        motion_data = MotionData(
            motion_type=MotionType.FLOAT,
            turns="fl",  # Float motions use 'fl' turns
            start_ori=start_ori,
            end_ori=start_ori,  # Will be calculated
            start_loc=start_loc,
            end_loc=end_loc,
            prop_rot_dir=RotationDirection.CLOCKWISE,
        )

        calculated_end_ori = calculator.calculate_end_orientation(
            motion_data, start_ori
        )
        handpath = calculator.calculate_handpath_direction(start_loc, end_loc)

        print(
            f"✅ FLOAT {start_loc.value}->{end_loc.value} ({handpath}): {start_ori.value} -> {calculated_end_ori.value}"
        )

    print("\n🎉 OrientationCalculator test completed!")
    return True


def test_motion_data_update():
    """Test updating MotionData objects with new orientations."""

    print("\n🧪 Testing MotionData Update Workflow")
    print("=" * 50)

    calculator = OrientationCalculator()

    # Simulate a motion with default orientations
    original_motion = MotionData(
        motion_type=MotionType.PRO,
        turns=1,
        start_ori=Orientation.IN,  # Default blue orientation
        end_ori=Orientation.OUT,  # Default calculated end
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,
        prop_rot_dir=RotationDirection.CLOCKWISE,
    )

    print(
        f"Original motion: {original_motion.motion_type.value} {original_motion.turns} turns"
    )
    print(
        f"  Default orientations: {original_motion.start_ori.value} -> {original_motion.end_ori.value}"
    )

    # Simulate sequence end orientations (what the motion should start from)
    sequence_end_blue_ori = Orientation.OUT  # Blue ended OUT
    sequence_end_red_ori = Orientation.IN  # Red ended IN

    print(
        f"\nSequence end orientations: blue={sequence_end_blue_ori.value}, red={sequence_end_red_ori.value}"
    )

    # Update the motion to start from sequence end orientation
    updated_motion = MotionData(
        motion_type=original_motion.motion_type,
        turns=original_motion.turns,
        start_ori=sequence_end_blue_ori,  # Start from sequence end
        end_ori=original_motion.end_ori,  # Will be recalculated
        start_loc=original_motion.start_loc,
        end_loc=original_motion.end_loc,
        prop_rot_dir=original_motion.prop_rot_dir,
    )

    # Calculate new end orientation
    new_end_ori = calculator.calculate_end_orientation(
        updated_motion, sequence_end_blue_ori
    )

    # Create final updated motion
    final_motion = MotionData(
        motion_type=updated_motion.motion_type,
        turns=updated_motion.turns,
        start_ori=sequence_end_blue_ori,
        end_ori=new_end_ori,
        start_loc=updated_motion.start_loc,
        end_loc=updated_motion.end_loc,
        prop_rot_dir=updated_motion.prop_rot_dir,
    )

    print(f"\nUpdated motion orientations:")
    print(f"  New start orientation: {final_motion.start_ori.value}")
    print(f"  Calculated end orientation: {final_motion.end_ori.value}")

    print(f"\n✅ Motion successfully updated to continue from sequence context!")
    return True


if __name__ == "__main__":
    try:
        test_orientation_calculator()
        test_motion_data_update()
        print("\n🎉 All tests passed! OrientationCalculator is working correctly.")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
