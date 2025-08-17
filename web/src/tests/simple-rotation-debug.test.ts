/**
 * Simple test to debug arrow rotation calculations
 * Tests the core rotation logic directly without DI complexity
 */

import { describe, it } from "vitest";
import { ArrowRotationCalculator } from "$lib/services/positioning/arrows/calculation/ArrowRotationCalculator";

import {
  DirectionalTupleCalculator,
  QuadrantIndexCalculator,
} from "$lib/services/positioning/arrows/processors/DirectionalTupleProcessor";
import { createMotionData } from "$lib/domain";
import { MotionType, Location } from "$lib/domain/enums";

describe("Simple Arrow Rotation Debug", () => {
  it("should test pro arrow rotation calculation directly", () => {
    console.log("\n🧪 Testing Pro Arrow Rotation: N → E");

    // Create test data
    const motionData = createMotionData({
      motion_type: MotionType.PRO,
      start_loc: Location.NORTH,
      end_loc: Location.EAST,
      turns: 0,
    });

    console.log("📊 Input Data:");
    console.log("  Motion:", {
      motion_type: motionData.motion_type,
      start_loc: motionData.start_loc,
      end_loc: motionData.end_loc,
      turns: motionData.turns,
    });

    // Test the core rotation calculation components
    console.log("\n🔧 Testing Core Components:");

    // 1. Test DirectionalTupleCalculator
    const tupleCalculator = new DirectionalTupleCalculator();
    console.log("\n1️⃣ DirectionalTupleCalculator:");

    try {
      // Generate directional tuples for pro motion N→E
      const tuples = tupleCalculator.generateDirectionalTuples(
        motionData,
        10,
        40
      );
      console.log(
        `  Generated tuples: [${tuples.map((t) => `(${t[0]}, ${t[1]})`).join(", ")}]`
      );

      // Test quadrant selection
      const quadCalculator = new QuadrantIndexCalculator();
      const quadIndex = quadCalculator.calculateQuadrantIndex(
        motionData,
        Location.NORTHEAST
      );
      console.log(`  Quadrant index for NE: ${quadIndex}`);
      console.log(
        `  Selected tuple: (${tuples[quadIndex][0]}, ${tuples[quadIndex][1]})`
      );
    } catch (error) {
      console.error("  ❌ DirectionalTupleCalculator failed:", error);
    }

    // 2. Skip ArrowAdjustmentCalculator (complex dependencies)
    console.log(
      "\n2️⃣ ArrowAdjustmentCalculator: (skipped - complex dependencies)"
    );

    // 3. Test ArrowRotationCalculator
    console.log("\n3️⃣ ArrowRotationCalculator:");

    try {
      const rotationCalculator = new ArrowRotationCalculator();

      // IMPORTANT: For pro motion N→E, the arrow is positioned at NORTHEAST (not East!)
      // This is calculated by the shift location algorithm: N + E = NE
      const arrowLocation = Location.NORTHEAST;
      console.log(`  Arrow location for N→E pro motion: ${arrowLocation}`);

      const rotation = rotationCalculator.calculateRotation(
        motionData,
        arrowLocation
      );
      console.log(`  Calculated rotation: ${rotation}°`);

      // Analysis
      console.log("\n📋 Rotation Analysis:");
      console.log(
        `  Motion: ${motionData.start_loc} → ${motionData.end_loc} (${motionData.motion_type})`
      );
      console.log(`  Expected: 0° (arrow at northeast for N→E pro motion)`);
      console.log(`  Actual: ${rotation}°`);
      console.log(
        `  Difference: ${rotation - 0}° ${rotation > 0 ? "(too far clockwise)" : rotation < 0 ? "(too far counter-clockwise)" : "(PERFECT!)"}`
      );

      if (rotation === 0) {
        console.log("  🎯 SUCCESS: Rotation is now correct!");
      } else if (Math.abs(rotation - 0) === 90) {
        console.log("  🚨 Still 90° off from expected value");
      }
    } catch (error) {
      console.error("  ❌ ArrowRotationCalculator failed:", error);
    }

    console.log("\n✅ Core component testing complete");
  });

  it("should test multiple directions to identify pattern", () => {
    console.log("\n🧪 Testing Multiple Pro Arrow Directions");

    const testCases = [
      {
        start: Location.NORTH,
        end: Location.EAST,
        arrowLoc: Location.NORTHEAST,
        expected: 0,
        name: "N→E",
      },
      {
        start: Location.EAST,
        end: Location.SOUTH,
        arrowLoc: Location.SOUTHEAST,
        expected: 90,
        name: "E→S",
      },
      {
        start: Location.SOUTH,
        end: Location.WEST,
        arrowLoc: Location.SOUTHWEST,
        expected: 180,
        name: "S→W",
      },
      {
        start: Location.WEST,
        end: Location.NORTH,
        arrowLoc: Location.NORTHWEST,
        expected: 270,
        name: "W→N",
      },
    ];

    const rotationCalculator = new ArrowRotationCalculator();

    console.log("\n📐 Rotation Test Results:");
    console.log("Direction | Expected | Actual | Difference");
    console.log("----------|----------|--------|----------");

    for (const testCase of testCases) {
      try {
        const testMotion = createMotionData({
          motion_type: MotionType.PRO,
          start_loc: testCase.start,
          end_loc: testCase.end,
          turns: 0,
        });

        // For pro motion, arrow is positioned at the calculated arrow location (not end location!)
        const rotation = rotationCalculator.calculateRotation(
          testMotion,
          testCase.arrowLoc
        );

        const difference = rotation - testCase.expected;
        console.log(
          `${testCase.name.padEnd(9)} | ${testCase.expected.toString().padEnd(8)} | ${rotation.toString().padEnd(6)} | ${difference > 0 ? "+" : ""}${difference}°`
        );
      } catch (error) {
        console.log(
          `${testCase.name.padEnd(9)} | ${testCase.expected.toString().padEnd(8)} | ERROR  | -`
        );
      }
    }

    console.log("\n🔍 Pattern Analysis:");
    console.log("If all rotations are consistently off by the same amount,");
    console.log("then the issue is in the base calculation logic.");
    console.log(
      "If the pattern is inconsistent, the issue is in the directional logic."
    );
  });
});
