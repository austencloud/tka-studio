/**
 * Start Position Beta Detection Test
 *
 * Tests that the start position picker correctly detects beta positions
 */

import { StartPositionService } from "$lib/services/implementations/domain/StartPositionService";
import { GridMode } from "$lib/domain/enums";
import { endsWithBeta } from "$lib/utils/betaDetection";

// Test the start position service beta detection
async function testStartPositionBetaDetection() {
  console.log("🧪 Testing Start Position Beta Detection");

  const startPositionService = new StartPositionService();

  try {
    // Get the default start positions (should include the beta one)
    console.log("🔍 Getting default start positions for diamond mode...");
    const startPositions = await startPositionService.getDefaultStartPositions(
      GridMode.DIAMOND
    );

    console.log(`✅ Got ${startPositions.length} start positions`);

    // Find the beta position (should be the middle one - index 1)
    const betaPosition = startPositions[1]; // beta5_beta5 should be at index 1

    if (!betaPosition) {
      console.error("❌ No beta position found at index 1");
      return false;
    }

    console.log("🔍 Beta position data:", {
      letter: betaPosition.letter,
      endPosition: betaPosition.endPosition,
      motions: {
        blue: betaPosition.motions?.blue
          ? {
              startLocation: betaPosition.motions.blue.startLocation,
              endLocation: betaPosition.motions.blue.endLocation,
            }
          : null,
        red: betaPosition.motions?.red
          ? {
              startLocation: betaPosition.motions.red.startLocation,
              endLocation: betaPosition.motions.red.endLocation,
            }
          : null,
      },
    });

    // Test beta detection
    const isBeta = endsWithBeta(betaPosition);
    console.log(`🔍 endsWithBeta(betaPosition) = ${isBeta}`);

    if (isBeta) {
      console.log("✅ SUCCESS: Start position beta detection is working!");
      return true;
    } else {
      console.log("❌ FAILURE: Start position beta detection not working");
      return false;
    }
  } catch (error) {
    console.error("❌ ERROR in start position beta detection test:", error);
    return false;
  }
}

// Test all start positions
async function testAllStartPositions() {
  console.log("🧪 Testing All Start Positions");

  const startPositionService = new StartPositionService();

  try {
    const startPositions = await startPositionService.getDefaultStartPositions(
      GridMode.DIAMOND
    );

    console.log(`🔍 Testing ${startPositions.length} start positions:`);

    startPositions.forEach((position, index) => {
      const isBeta = endsWithBeta(position);
      console.log(
        `  ${index}: ${position.letter} - endsWithBeta: ${isBeta} - endPosition: ${position.endPosition}`
      );
    });

    return true;
  } catch (error) {
    console.error("❌ ERROR in all start positions test:", error);
    return false;
  }
}

// Run the tests
async function runTests() {
  console.log("🚀 Starting Start Position Beta Detection Tests\n");

  const test1Success = await testStartPositionBetaDetection();
  console.log("");

  const test2Success = await testAllStartPositions();
  console.log("");

  if (test1Success && test2Success) {
    console.log("🎉 All start position beta detection tests PASSED");
  } else {
    console.log("💥 Some start position beta detection tests FAILED");
  }
}

runTests();
