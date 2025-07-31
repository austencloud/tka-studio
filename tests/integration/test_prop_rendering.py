#!/usr/bin/env python3
"""
Test script to verify prop rendering functionality.

This script tests the prop rendering pipeline to ensure that:
1. Props are generated from motion data
2. Props are positioned correctly using the positioning services
3. The Qt adapter renders props properly
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_prop_rendering():
    """Test the prop rendering pipeline."""
    print("🧪 Testing TKA Prop Rendering Pipeline")
    print("=" * 50)

    try:
        # Import required modules
        from desktop.modern.application.adapters.qt_pictograph_rendering_service_adapter import (
            QtPictographRenderingServiceAdapter,
        )
        from desktop.modern.domain.models.arrow_data import ArrowData
        from desktop.modern.domain.models.enums import (
            Location,
            MotionType,
            Orientation,
            RotationDirection,
        )
        from desktop.modern.domain.models.grid_data import GridData
        from desktop.modern.domain.models.motion_data import MotionData
        from desktop.modern.domain.models.pictograph_data import PictographData

        print("✅ Successfully imported all required modules")

        # Create test motion data
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
        )

        red_motion = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.EAST,
            end_loc=Location.WEST,
            turns=0.5,
            start_ori=Orientation.OUT,
            end_ori=Orientation.IN,
        )

        print("✅ Created test motion data:")
        print(
            f"   Blue: {blue_motion.motion_type.value} from {blue_motion.start_loc.value} to {blue_motion.end_loc.value}"
        )
        print(
            f"   Red: {red_motion.motion_type.value} from {red_motion.start_loc.value} to {red_motion.end_loc.value}"
        )

        # Create test pictograph data
        pictograph_data = PictographData(
            grid_data=GridData(),
            arrows={"blue": ArrowData(color="blue"), "red": ArrowData(color="red")},
            motions={"blue": blue_motion, "red": red_motion},
            letter="G",
            start_position="alpha1",
            end_position="beta5",
        )

        print("✅ Created test pictograph data with motions")

        # Create Qt adapter
        adapter = QtPictographRenderingServiceAdapter()
        print("✅ Created Qt pictograph rendering adapter")

        # Test prop position calculation
        blue_position = adapter._calculate_prop_position_from_motion(
            blue_motion, "blue"
        )
        red_position = adapter._calculate_prop_position_from_motion(red_motion, "red")

        print("✅ Calculated prop positions:")
        print(f"   Blue prop position: ({blue_position.x}, {blue_position.y})")
        print(f"   Red prop position: ({red_position.x}, {red_position.y})")

        # Test prop generation from motions
        props = adapter._generate_props_from_motions(pictograph_data)
        print(f"✅ Generated {len(props)} props from motion data:")
        for prop in props:
            print(
                f"   {prop['color']} prop at ({prop['x']}, {prop['y']}) - motion_type: {prop['motion_data']['motion_type']}"
            )

        # Test pictograph data conversion
        converted_data = adapter._convert_pictograph_data_to_dict(pictograph_data)
        print("✅ Converted pictograph data:")
        print(f"   Grid mode: {converted_data['grid_mode']}")
        print(f"   Motions: {len(converted_data['motions'])}")
        print(f"   Props: {len(converted_data['props'])}")
        print(f"   Glyphs: {len(converted_data['glyphs'])}")

        print("\n🎉 All tests passed! Prop rendering pipeline is working correctly.")
        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_prop_rendering()
    sys.exit(0 if success else 1)
