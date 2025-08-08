/**
 * Example usage of the manual rotation system
 * This file shows how to manually specify staff rotations instead of using dynamic calculations
 */

import type {
  SequenceData,
  SequenceStep,
  PropAttributes,
} from "../src/lib/animator/types/core.js";
import {
  setManualRotationDegrees,
  // setCustomRotation, // Not used in this example
  clearManualRotation,
  hasManualRotation,
  getManualRotationDegrees,
} from "../src/lib/animator/utils/manual-rotation.js";
import {
  // ROTATION_PRESETS, // Not used in this example
  MOTION_TYPE_PRESETS,
  // applyRotationPreset, // Not used in this example
  createStepWithManualRotation,
  applyManualRotationsToSteps,
} from "../src/lib/animator/utils/rotation-presets.js";

// Example 1: Basic manual rotation setup
function example1_BasicManualRotation() {
  console.log("=== Example 1: Basic Manual Rotation ===");

  // Start with a basic step
  const step: SequenceStep = {
    beat: 1,
    blue_attributes: {
      start_loc: "s",
      end_loc: "w",
      start_ori: "in",
      end_ori: "in",
      prop_rot_dir: "cw",
      turns: 0,
      motion_type: "pro",
    },
    red_attributes: {
      start_loc: "n",
      end_loc: "e",
      start_ori: "in",
      end_ori: "in",
      prop_rot_dir: "cw",
      turns: 0,
      motion_type: "pro",
    },
  };

  // Add manual rotation to blue prop: 0° to 90° clockwise
  step.blue_attributes = setManualRotationDegrees(
    step.blue_attributes,
    0, // start at 0 degrees
    90, // end at 90 degrees
    "cw", // force clockwise direction
  );

  // Add manual rotation to red prop: 0° to -90° counter-clockwise
  step.red_attributes = setManualRotationDegrees(
    step.red_attributes,
    0, // start at 0 degrees
    -90, // end at -90 degrees
    "ccw", // force counter-clockwise direction
  );

  console.log("Step with manual rotations:", JSON.stringify(step, null, 2));
}

// Example 2: Using presets
function example2_UsingPresets() {
  console.log("\n=== Example 2: Using Rotation Presets ===");

  const step: SequenceStep = {
    beat: 2,
    blue_attributes: {
      start_loc: "w",
      end_loc: "n",
      motion_type: "pro",
      start_ori: "in",
      end_ori: "in",
      prop_rot_dir: "cw",
      turns: 0,
    },
    red_attributes: {
      start_loc: "e",
      end_loc: "s",
      motion_type: "fl",
      start_ori: "in",
      end_ori: "in",
      prop_rot_dir: "no_rot",
      turns: 0,
    },
  };

  // Apply pro isolation preset to blue prop
  step.blue_attributes = MOTION_TYPE_PRESETS.pro_isolation_cw(
    step.blue_attributes,
  );

  // Apply float preset to red prop (no rotation)
  step.red_attributes = MOTION_TYPE_PRESETS.float_no_rotation(
    step.red_attributes,
  );

  console.log("Step with preset rotations:", JSON.stringify(step, null, 2));
}

// Example 3: Batch applying rotations to multiple steps
function example3_BatchRotations() {
  console.log("\n=== Example 3: Batch Applying Rotations ===");

  // Start with some basic steps
  const steps = [
    {
      beat: 1,
      blue_attributes: {
        start_loc: "s",
        end_loc: "w",
        motion_type: "pro",
        start_ori: "in",
        end_ori: "in",
        prop_rot_dir: "cw",
        turns: 0,
      },
      red_attributes: {
        start_loc: "n",
        end_loc: "e",
        motion_type: "pro",
        start_ori: "in",
        end_ori: "in",
        prop_rot_dir: "cw",
        turns: 0,
      },
    },
    {
      beat: 2,
      blue_attributes: {
        start_loc: "w",
        end_loc: "n",
        motion_type: "anti",
        start_ori: "in",
        end_ori: "in",
        prop_rot_dir: "ccw",
        turns: 1,
      },
      red_attributes: {
        start_loc: "e",
        end_loc: "s",
        motion_type: "fl",
        start_ori: "in",
        end_ori: "in",
        prop_rot_dir: "no_rot",
        turns: 0,
      },
    },
    {
      beat: 3,
      blue_attributes: {
        start_loc: "n",
        end_loc: "e",
        motion_type: "static",
        start_ori: "in",
        end_ori: "in",
        prop_rot_dir: "no_rot",
        turns: 0,
      },
      red_attributes: {
        start_loc: "s",
        end_loc: "w",
        motion_type: "dash",
        start_ori: "in",
        end_ori: "out",
        prop_rot_dir: "cw",
        turns: 0,
      },
    },
  ];

  // Define manual rotations for specific beats
  const rotationMap = {
    1: {
      blue: { start: 0, end: 90, direction: "cw" as const },
      red: { start: 0, end: -90, direction: "ccw" as const },
    },
    2: {
      blue: { start: 90, end: 450, direction: "cw" as const }, // 1 full turn + 90°
      red: { start: -90, end: -90, direction: "shortest" as const }, // no rotation
    },
    3: {
      blue: { start: 450, end: 450, direction: "shortest" as const }, // static
      red: { start: -90, end: 180, direction: "shortest" as const }, // flip to opposite
    },
  };

  const stepsWithManualRotations = applyManualRotationsToSteps(
    steps,
    rotationMap,
  );

  console.log("Steps with batch-applied rotations:");
  stepsWithManualRotations.forEach((step, index) => {
    console.log(`Step ${index + 1}:`, JSON.stringify(step, null, 2));
  });
}

// Example 4: Creating a complete sequence with manual rotations
function example4_CompleteSequence() {
  console.log("\n=== Example 4: Complete Sequence with Manual Rotations ===");

  const sequenceData: SequenceData = [
    // Metadata
    {
      word: "Manual Rotation Example",
      author: "Manual Input",
      level: 1,
      prop_type: "staff",
      grid_mode: "standard",
    },
    // Start position (beat 0)
    {
      beat: 0,
      blue_attributes: setManualRotationDegrees(
        {
          start_loc: "s",
          end_loc: "s",
          start_ori: "in",
          end_ori: "in",
          prop_rot_dir: "no_rot",
          turns: 0,
          motion_type: "static",
        },
        0,
        0,
        "shortest",
      ),
      red_attributes: setManualRotationDegrees(
        {
          start_loc: "n",
          end_loc: "n",
          start_ori: "in",
          end_ori: "in",
          prop_rot_dir: "no_rot",
          turns: 0,
          motion_type: "static",
        },
        0,
        0,
        "shortest",
      ),
    },
    // Beat 1: Pro isolation movements
    createStepWithManualRotation(
      1,
      { start: 0, end: 90, direction: "cw" }, // Blue: 90° clockwise
      { start: 0, end: -90, direction: "ccw" }, // Red: 90° counter-clockwise
      { start_loc: "s", end_loc: "w", motion_type: "pro" },
      { start_loc: "n", end_loc: "e", motion_type: "pro" },
    ),
    // Beat 2: Full turn movements
    createStepWithManualRotation(
      2,
      { start: 90, end: 450, direction: "cw" }, // Blue: 1 full turn + 90°
      { start: -90, end: 270, direction: "cw" }, // Red: 1 full turn
      { start_loc: "w", end_loc: "n", motion_type: "anti" },
      { start_loc: "e", end_loc: "s", motion_type: "anti" },
    ),
    // Beat 3: Return to start
    createStepWithManualRotation(
      3,
      { start: 450, end: 0, direction: "shortest" }, // Blue: shortest path back to 0°
      { start: 270, end: 0, direction: "shortest" }, // Red: shortest path back to 0°
      { start_loc: "n", end_loc: "s", motion_type: "dash" },
      { start_loc: "s", end_loc: "n", motion_type: "dash" },
    ),
  ];

  console.log("Complete sequence with manual rotations:");
  console.log(JSON.stringify(sequenceData, null, 2));
}

// Example 5: Utility functions
function example5_UtilityFunctions() {
  console.log("\n=== Example 5: Utility Functions ===");

  let attributes: PropAttributes = {
    start_loc: "s",
    end_loc: "w",
    motion_type: "pro",
    start_ori: "in",
    end_ori: "in",
    prop_rot_dir: "cw",
    turns: 0,
  };

  console.log("Original attributes:", attributes);
  console.log("Has manual rotation:", hasManualRotation(attributes));

  // Add manual rotation
  attributes = setManualRotationDegrees(attributes, 45, 135, "cw");
  console.log("After adding manual rotation:", attributes);
  console.log("Has manual rotation:", hasManualRotation(attributes));

  // Get rotation values in degrees
  const rotationDegrees = getManualRotationDegrees(attributes);
  console.log("Rotation in degrees:", rotationDegrees);

  // Clear manual rotation
  attributes = clearManualRotation(attributes);
  console.log("After clearing manual rotation:", attributes);
  console.log("Has manual rotation:", hasManualRotation(attributes));
}

// Run all examples
if (typeof window === "undefined") {
  // Only run in Node.js environment
  example1_BasicManualRotation();
  example2_UsingPresets();
  example3_BatchRotations();
  example4_CompleteSequence();
  example5_UtilityFunctions();
}

// Example 6: Using orientation test data
function example6_OrientationBasedRotations() {
  console.log("\n=== Example 6: Orientation-Based Rotations ===");

  // This example shows how to use data from the staff orientation test interface

  // Sample test data (this would come from your test interface export)
  const sampleOrientationData = {
    n: {
      in: 270, // pointing toward center (down)
      out: 90, // pointing away from center (up)
      n: 90, // pointing north
      e: 0, // pointing east
      s: 270, // pointing south
      w: 180, // pointing west
    },
    s: {
      in: 90, // pointing toward center (up)
      out: 270, // pointing away from center (down)
      n: 90,
      e: 0,
      s: 270,
      w: 180,
    },
    e: {
      in: 180, // pointing toward center (left)
      out: 0, // pointing away from center (right)
      n: 90,
      e: 0,
      s: 270,
      w: 180,
    },
    w: {
      in: 0, // pointing toward center (right)
      out: 180, // pointing away from center (left)
      n: 90,
      e: 0,
      s: 270,
      w: 180,
    },
  };

  console.log("Sample orientation test data:");
  console.log(JSON.stringify(sampleOrientationData, null, 2));

  // Example of how this data would be used to create manual rotations
  const stepWithOrientationBasedRotations = {
    beat: 1,
    blue_attributes: setManualRotationDegrees(
      {
        start_loc: "s",
        end_loc: "n",
        start_ori: "in",
        end_ori: "out",
        motion_type: "pro",
        prop_rot_dir: "cw",
        turns: 0,
      },
      sampleOrientationData.s.in, // 90° (pointing up toward center)
      sampleOrientationData.n.out, // 90° (pointing up away from center)
      "shortest",
    ),
    red_attributes: setManualRotationDegrees(
      {
        start_loc: "n",
        end_loc: "s",
        start_ori: "in",
        end_ori: "out",
        motion_type: "pro",
        prop_rot_dir: "cw",
        turns: 0,
      },
      sampleOrientationData.n.in, // 270° (pointing down toward center)
      sampleOrientationData.s.out, // 270° (pointing down away from center)
      "shortest",
    ),
  };

  console.log("Step with orientation-based manual rotations:");
  console.log(JSON.stringify(stepWithOrientationBasedRotations, null, 2));
}

export {
  example1_BasicManualRotation,
  example2_UsingPresets,
  example3_BatchRotations,
  example4_CompleteSequence,
  example5_UtilityFunctions,
  example6_OrientationBasedRotations,
};
