/**
 * Focused test for debugging arrow positioning issues
 * Tests both positioning systems to identify rotation calculation problems
 */

import { resolve, TYPES } from "$lib/services/bootstrap";
import type { IArrowPositioningOrchestrator } from "$lib/services/interfaces/positioning-interfaces";
import { describe, it } from "vitest";
// import type { GridData as ServiceGridData } from "$lib/services/interfaces/core-types";

import {
  createArrowPlacementData,
  createMotionData,
  createPictographData,
} from "$lib/domain";
import {
  Location,
  MotionColor,
  MotionType,
  Orientation,
  PropType,
  RotationDirection,
} from "$lib/domain/enums";

// Helper function to convert domain GridData to service GridData
// function convertGridData(domainGridData: unknown): ServiceGridData {
//   return {
//     mode: (domainGridData as { gridMode: string }).gridMode,
//     allLayer2PointsNormal: {},
//     allHandPointsNormal: {},
//   };
// }

describe("Arrow Positioning Debug Tests", () => {
  it("should test pro arrow rotation calculation - N to E motion", async () => {
    // Resolve orchestrator for this test
    const orchestrator = resolve(
      TYPES.IArrowPositioningOrchestrator
    ) as IArrowPositioningOrchestrator;

    console.log(
      "\n🧪 Testing Pro Arrow: N → E (should be clockwise, expect ~90° rotation)"
    );

    // ✅ FIXED: ArrowPlacementData now only contains arrow-specific properties
    const blueArrowData = createArrowPlacementData({
      positionX: 0,
      positionY: 0,
      rotationAngle: 0,
      coordinates: null,
      svgCenter: null,
      svgMirrored: false,
    });

    const blueMotionData = createMotionData({
      motionType: MotionType.PRO,
      startLocation: Location.NORTH,
      endLocation: Location.EAST,
      startOrientation: Orientation.IN,
      endOrientation: Orientation.IN,
      rotationDirection: RotationDirection.CLOCKWISE,
      turns: 0,
      color: MotionColor.BLUE,
      propType: PropType.STAFF,
      arrowLocation: Location.NORTH, // Will be calculated by positioning system
    });

    const redMotionData = createMotionData({
      motionType: MotionType.STATIC,
      startLocation: Location.SOUTH,
      endLocation: Location.SOUTH,
      startOrientation: Orientation.IN,
      endOrientation: Orientation.IN,
      rotationDirection: RotationDirection.NO_ROTATION,
      turns: 0,
      color: MotionColor.RED,
      propType: PropType.STAFF,
      arrowLocation: Location.SOUTH, // Will be calculated by positioning system
    });

    const pictographData = createPictographData({
      letter: null, // Test letter
      motions: {
        blue: blueMotionData,
        red: redMotionData,
      },
    });

    console.log("📊 Input Data:");
    console.log("  Blue Motion:", {
      motionType: blueMotionData.motionType,
      startLocation: blueMotionData.startLocation,
      endLocation: blueMotionData.endLocation,
      turns: blueMotionData.turns,
    });

    // Test 1: ArrowPositioningOrchestrator.calculateAllArrowPositions
    console.log(
      "\n🎯 Test 1: ArrowPositioningOrchestrator.calculateAllArrowPositions"
    );
    const orchestratorResult =
      await orchestrator.calculateAllArrowPositions(pictographData);
    const orchestratorBlueArrow =
      orchestratorResult.motions?.blue?.arrowPlacementData;

    console.log("  Orchestrator Result:");
    console.log(
      "    Position:",
      `(${orchestratorBlueArrow?.positionX}, ${orchestratorBlueArrow?.positionY})`
    );
    console.log("    Rotation:", `${orchestratorBlueArrow?.rotationAngle}°`);

    // Test 2: Direct orchestrator.calculateArrowPosition call
    console.log("\n🎯 Test 3: Direct orchestrator.calculateArrowPosition");
    const [x, y, rotation] = await orchestrator.calculateArrowPosition(
      pictographData,
      blueMotionData
    );

    console.log("  Direct Result:");
    console.log("    Position:", `(${x}, ${y})`);
    console.log("    Rotation:", `${rotation}°`);

    // Analysis
    console.log("\n📋 Analysis:");
    console.log("  Expected: Pro motion N→E should be ~90° (pointing east)");
    console.log("  User Report: Pro arrows are 90° too far clockwise");
    console.log(
      "  If correct rotation should be 90°, but we see 180°, then calculation is +90° off"
    );

    // Compare results
    const orchestratorRotation = orchestratorBlueArrow?.rotationAngle || 0;
    const directRotation = rotation;

    console.log("\n🔍 Rotation Comparison:");
    console.log(
      `  Orchestrator (calculateAllArrowPositions): ${orchestratorRotation}°`
    );
    console.log(`  Direct (calculateArrowPosition): ${directRotation}°`);

    if (orchestratorRotation === directRotation) {
      console.log(
        "  ✅ Both methods return same rotation - consistent calculation"
      );
    } else {
      console.log(
        "  ❌ Methods return different rotations - needs investigation"
      );
    }

    // Expected vs Actual
    const expectedRotation = 90; // N→E should point east (90°)
    const actualRotation = directRotation;
    const rotationDiff = actualRotation - expectedRotation;

    console.log("\n🎯 Rotation Analysis:");
    console.log(`  Expected rotation: ${expectedRotation}° (pointing east)`);
    console.log(`  Actual rotation: ${actualRotation}°`);
    console.log(
      `  Difference: ${rotationDiff}° ${rotationDiff > 0 ? "(too far clockwise)" : "(too far counter-clockwise)"}`
    );

    if (Math.abs(rotationDiff) === 90) {
      console.log("  🚨 CONFIRMED: Rotation is exactly 90° off!");
    }
  });

  it("should test multiple pro arrow directions", async () => {
    // Resolve orchestrator for this test
    const orchestrator = resolve(
      TYPES.IArrowPositioningOrchestrator
    ) as IArrowPositioningOrchestrator;

    console.log("\n🧪 Testing Multiple Pro Arrow Directions");

    const testCases = [
      { start: Location.NORTH, end: Location.EAST, expected: 90, name: "N→E" },
      { start: Location.EAST, end: Location.SOUTH, expected: 180, name: "E→S" },
      { start: Location.SOUTH, end: Location.WEST, expected: 270, name: "S→W" },
      { start: Location.WEST, end: Location.NORTH, expected: 0, name: "W→N" },
    ];

    for (const testCase of testCases) {
      console.log(`\n📐 Testing ${testCase.name}:`);

      const motionData = createMotionData({
        motionType: MotionType.PRO,
        startLocation: testCase.start,
        endLocation: testCase.end,
        turns: 0,
      });

      const pictographData = createPictographData({
        letter: null, // Test letter
        motions: { blue: motionData },
      });

      const [, , rotation] = await orchestrator.calculateArrowPosition(
        pictographData,
        motionData
      );

      console.log(`  Motion: ${testCase.start} → ${testCase.end}`);
      console.log(`  Expected rotation: ${testCase.expected}°`);
      console.log(`  Actual rotation: ${rotation}°`);
      console.log(`  Difference: ${rotation - testCase.expected}°`);
    }
  });
});
