/**
 * Example usage of the finalized orientation mapping system
 * This demonstrates how to use the precise, manually-validated rotation angles
 */

import type {
  SequenceData /* SequenceStep */,
} from "../src/lib/animator/types/core.js";
import {
  processSequenceWithOrientationMappings,
  validateSequenceOrientationIntegrity,
  generateOrientationProcessingReport,
  exportFinalizedOrientationMappings,
} from "../src/lib/animator/utils/sequence-orientation-processor.js";
import {
  getOrientationAngle,
  getOrientationAngleRadians,
} from "../src/lib/animator/utils/orientation-mapping.js";

// Example 1: Basic orientation mapping lookup
function example1_BasicOrientationLookup() {
  console.log("=== Example 1: Basic Orientation Mapping Lookup ===");

  // Get specific orientation angles
  const nHandIn = getOrientationAngle("n_hand", "in");
  const nHandOut = getOrientationAngle("n_hand", "out");
  const neClockwise = getOrientationAngle("ne", "clock");

  console.log(`n_hand 'in' orientation: ${nHandIn}°`);
  console.log(`n_hand 'out' orientation: ${nHandOut}°`);
  console.log(`ne 'clockwise' orientation: ${neClockwise}°`);

  // Get angles in radians for calculations
  const nHandInRadians = getOrientationAngleRadians("n_hand", "in");
  console.log(`n_hand 'in' in radians: ${nHandInRadians.toFixed(3)}`);
}

// Example 2: Process a complete sequence with orientation mappings
function example2_ProcessSequence() {
  console.log(
    "\n=== Example 2: Process Sequence with Orientation Mappings ===",
  );

  // Sample sequence data
  const originalSequence: SequenceData = [
    // Metadata
    {
      word: "Orientation Test",
      author: "System",
      level: 1,
      prop_type: "staff",
      grid_mode: "standard",
    },
    // Start position (beat 0)
    {
      beat: 0,
      blue_attributes: {
        start_loc: "s_hand",
        end_loc: "s_hand",
        start_ori: "in",
        end_ori: "in",
        prop_rot_dir: "no_rot",
        turns: 0,
        motion_type: "static",
      },
      red_attributes: {
        start_loc: "n_hand",
        end_loc: "n_hand",
        start_ori: "in",
        end_ori: "in",
        prop_rot_dir: "no_rot",
        turns: 0,
        motion_type: "static",
      },
    },
    // Beat 1: Move with orientation change
    {
      beat: 1,
      blue_attributes: {
        start_loc: "s_hand",
        end_loc: "w_hand",
        start_ori: "in",
        end_ori: "out",
        prop_rot_dir: "cw",
        turns: 0,
        motion_type: "pro",
      },
      red_attributes: {
        start_loc: "n_hand",
        end_loc: "e_hand",
        start_ori: "in",
        end_ori: "clock",
        prop_rot_dir: "cw",
        turns: 0,
        motion_type: "pro",
      },
    },
    // Beat 2: Continue movement
    {
      beat: 2,
      blue_attributes: {
        start_loc: "w_hand",
        end_loc: "ne",
        start_ori: "out",
        end_ori: "counter",
        prop_rot_dir: "ccw",
        turns: 0,
        motion_type: "dash",
      },
      red_attributes: {
        start_loc: "e_hand",
        end_loc: "sw",
        start_ori: "clock",
        end_ori: "in",
        prop_rot_dir: "ccw",
        turns: 0,
        motion_type: "dash",
      },
    },
  ];

  // Validate sequence integrity first
  const validation = validateSequenceOrientationIntegrity(originalSequence);
  console.log("Sequence validation:", validation);

  if (validation.isValid) {
    // Process the sequence with orientation mappings
    const processedSequence =
      processSequenceWithOrientationMappings(originalSequence);

    // Generate a report
    const report = generateOrientationProcessingReport(
      originalSequence,
      processedSequence,
    );
    console.log("Processing report:");
    console.log(report);

    // Show the processed sequence
    console.log("Processed sequence with manual rotations:");
    console.log(JSON.stringify(processedSequence, null, 2));
  } else {
    console.error("Sequence validation failed:", validation.errors);
  }
}

// Example 3: Demonstrate orientation continuity validation
function example3_OrientationContinuityValidation() {
  console.log("\n=== Example 3: Orientation Continuity Validation ===");

  // Example with broken continuity (end_ori doesn't match next start_ori)
  const brokenSequence: SequenceData = [
    {
      word: "Broken Continuity Test",
      author: "System",
      level: 1,
      prop_type: "staff",
      grid_mode: "standard",
    },
    {
      beat: 1,
      blue_attributes: {
        start_loc: "n_hand",
        end_loc: "e_hand",
        start_ori: "in",
        end_ori: "out", // This should match the next beat's start_ori
        motion_type: "pro",
        prop_rot_dir: "cw",
        turns: 0,
      },
      red_attributes: {
        start_loc: "s_hand",
        end_loc: "w_hand",
        start_ori: "in",
        end_ori: "clock",
        motion_type: "pro",
        prop_rot_dir: "cw",
        turns: 0,
      },
    },
    {
      beat: 2,
      blue_attributes: {
        start_loc: "e_hand",
        end_loc: "se",
        start_ori: "clock", // BROKEN: doesn't match previous end_ori 'out'
        end_ori: "counter",
        motion_type: "dash",
        prop_rot_dir: "ccw",
        turns: 0,
      },
      red_attributes: {
        start_loc: "w_hand",
        end_loc: "nw",
        start_ori: "clock", // This matches correctly
        end_ori: "in",
        motion_type: "dash",
        prop_rot_dir: "ccw",
        turns: 0,
      },
    },
  ];

  const validation = validateSequenceOrientationIntegrity(brokenSequence);
  console.log("Broken sequence validation:");
  console.log("Valid:", validation.isValid);
  console.log("Errors:", validation.errors);
  console.log("Warnings:", validation.warnings);
}

// Example 4: Export finalized orientation mappings
function example4_ExportOrientationMappings() {
  console.log("\n=== Example 4: Export Finalized Orientation Mappings ===");

  const mappings = exportFinalizedOrientationMappings();
  console.log("Finalized orientation mappings:");
  console.log(mappings);
}

// Example 5: Compare all orientations for a position
function example5_CompareOrientationsForPosition() {
  console.log("\n=== Example 5: Compare All Orientations for Position ===");

  const position = "e_hand";
  const orientations = ["in", "out", "clockwise", "counter"] as const;

  console.log(`All orientations for ${position}:`);
  orientations.forEach((orientation) => {
    const angle = getOrientationAngle(position, orientation);
    console.log(`  ${orientation}: ${angle}°`);
  });
}

// Run all examples
if (typeof window === "undefined") {
  // Only run in Node.js environment
  example1_BasicOrientationLookup();
  example2_ProcessSequence();
  example3_OrientationContinuityValidation();
  example4_ExportOrientationMappings();
  example5_CompareOrientationsForPosition();
}

export {
  example1_BasicOrientationLookup,
  example2_ProcessSequence,
  example3_OrientationContinuityValidation,
  example4_ExportOrientationMappings,
  example5_CompareOrientationsForPosition,
};
