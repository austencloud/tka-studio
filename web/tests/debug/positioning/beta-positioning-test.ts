/**
 * Beta Positioning Test
 *
 * Tests the new simplified beta positioning architecture
 */

import {
  GridLocation,
  GridPosition,
  Letter,
  MotionColor,
  MotionType,
  Orientation,
  PropType,
  RotationDirection,
  createMotionData,
  createPictographData,
} from "$shared";

// Test the new simplified beta positioning
async function testBetaPositioning() {
  console.log("🧪 Testing Beta Positioning Architecture");

  // Create test pictograph data that should trigger beta positioning
  const pictographData = createPictographData({
    id: "beta-test",
    motions: {
      blue: createMotionData({
        motionType: MotionType.STATIC,
        startLocation: GridLocation.NORTH,
        endLocation: GridLocation.SOUTH, // Both props end at same location
        startOrientation: Orientation.OUT,
        endOrientation: Orientation.IN,
        rotationDirection: RotationDirection.NO_ROTATION,
        turns: 0,
        isVisible: true,
        color: MotionColor.BLUE,
        propType: PropType.STAFF,
        arrowLocation: GridLocation.NORTH, // Will be calculated by positioning system
      }),
      red: createMotionData({
        motionType: MotionType.STATIC,
        startLocation: GridLocation.NORTH,
        endLocation: GridLocation.SOUTH, // Both props end at same location
        startOrientation: Orientation.OUT,
        endOrientation: Orientation.IN,
        rotationDirection: RotationDirection.NO_ROTATION,
        turns: 0,
        isVisible: true,
        color: MotionColor.RED,
        propType: PropType.STAFF,
        arrowLocation: GridLocation.NORTH, // Will be calculated by positioning system
      }),
    },
    startPosition: GridPosition.BETA1,
    endPosition: GridPosition.BETA5, // This should trigger beta positioning
    letter: Letter.PSI_DASH,
  });

  // Use container to resolve service with proper dependencies
  const { resolve, TYPES } = await import("../../../src/lib/shared/inversify/container");
  const propPlacementService = resolve(TYPES.IPropPlacementService) as import("../../../src/lib/shared/pictograph/prop/services/contracts/IPropPlacementService").IPropPlacementService;

  try {
    console.log("🔍 Testing blue prop placement...");
    if (!pictographData.motions.blue || !pictographData.motions.red) {
      throw new Error("Missing motion data for test");
    }

    const bluePlacement = await propPlacementService.calculatePlacement(
      pictographData,
      pictographData.motions.blue
    );
    console.log("✅ Blue prop placement:", bluePlacement);

    console.log("🔍 Testing red prop placement...");
    const redPlacement = await propPlacementService.calculatePlacement(
      pictographData,
      pictographData.motions.red
    );
    console.log("✅ Red prop placement:", redPlacement);

    // Check if props are separated (beta positioning working)
    const xDifference = Math.abs(
      bluePlacement.positionX - redPlacement.positionX
    );
    const yDifference = Math.abs(
      bluePlacement.positionY - redPlacement.positionY
    );
    const totalSeparation = Math.sqrt(
      xDifference * xDifference + yDifference * yDifference
    );

    console.log(
      `📏 Prop separation: x=${xDifference}, y=${yDifference}, total=${totalSeparation}`
    );

    if (totalSeparation > 0) {
      console.log(
        "✅ SUCCESS: Props are separated - beta positioning is working!"
      );
      return true;
    } else {
      console.log(
        "❌ FAILURE: Props are not separated - beta positioning not working"
      );
      return false;
    }
  } catch (error) {
    console.error("❌ ERROR in beta positioning test:", error);
    return false;
  }
}

// Run the test
testBetaPositioning().then((success) => {
  if (success) {
    console.log("🎉 Beta positioning test PASSED");
  } else {
    console.log("💥 Beta positioning test FAILED");
  }
});
