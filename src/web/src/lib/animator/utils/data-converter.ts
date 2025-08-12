/**
 * Data Converter - Web App Format to Standalone Format
 *
 * Converts web app sequence data to the format expected by the standalone engine.
 */

import type { StepDefinition, PropAttributes } from "./standalone-math.js";

// Web app data types
export interface WebAppSequenceData {
  id: string;
  name: string;
  word?: string;
  beats: WebAppBeatData[];
  metadata?: {
    author?: string;
    level?: number;
    [key: string]: any;
  };
  [key: string]: any;
}

export interface WebAppBeatData {
  pictograph_data?: {
    letter?: string;
    motions?: {
      blue?: WebAppMotionData;
      red?: WebAppMotionData;
    };
  };
  [key: string]: any;
}

export interface WebAppMotionData {
  motion_type: string;
  start_loc: string;
  end_loc: string;
  start_ori?: string;
  end_ori?: string;
  prop_rot_dir?: string;
  turns?: number;
  [key: string]: any;
}

/**
 * Convert web app sequence data to standalone format
 */
export function convertWebAppToStandalone(
  webAppData: WebAppSequenceData
): any[] {
  console.log("Converting web app data to standalone format:", webAppData);
  console.log("Number of beats:", webAppData.beats?.length || 0);
  console.log("Beats data structure:", webAppData.beats);

  // Check if we have beats
  if (!webAppData.beats || webAppData.beats.length === 0) {
    console.error("No beats found in sequence data");
    console.error("Full sequence data:", JSON.stringify(webAppData, null, 2));

    // Create a simple test sequence for demonstration
    console.log("Creating test sequence with 4 beats for demonstration...");
    return createTestSequence(webAppData);
  }

  // Log first beat structure for debugging
  const firstBeat = webAppData.beats[0];
  console.log("First beat structure:", firstBeat);
  console.log("First beat pictograph_data:", firstBeat?.pictograph_data);
  console.log("First beat motions:", firstBeat?.pictograph_data?.motions);

  // Create metadata object (index 0)
  const metadata = {
    word: webAppData.word || webAppData.name || "",
    author: webAppData.metadata?.author || "",
    level: webAppData.metadata?.level || 0,
    prop_type: "staff",
    grid_mode: "diamond",
    is_circular: false,
    can_be_CAP: false,
    is_strict_rotated_CAP: false,
    is_strict_mirrored_CAP: false,
    is_strict_swapped_CAP: false,
    is_mirrored_swapped_CAP: false,
    is_rotated_swapped_CAP: false,
  };

  // Create start position (index 1) - derive from first beat
  const startPosition = {
    beat: 0,
    sequence_start_position: "alpha",
    letter: "α",
    end_pos: "alpha1",
    timing: "none",
    direction: "none",
    blue_attributes: {
      start_loc: firstBeat?.pictograph_data?.motions?.blue?.start_loc || "s",
      end_loc: firstBeat?.pictograph_data?.motions?.blue?.start_loc || "s",
      start_ori: "in",
      end_ori: "in",
      prop_rot_dir: "no_rot",
      turns: 0,
      motion_type: "static",
    },
    red_attributes: {
      start_loc: firstBeat?.pictograph_data?.motions?.red?.start_loc || "n",
      end_loc: firstBeat?.pictograph_data?.motions?.red?.start_loc || "n",
      start_ori: "in",
      end_ori: "in",
      prop_rot_dir: "no_rot",
      turns: 0,
      motion_type: "static",
    },
  };

  // Convert beats to steps (index 2 onwards)
  const steps = webAppData.beats.map((beat, index) => {
    const motions = beat.pictograph_data?.motions;
    console.log(`Beat ${index + 1} motions:`, motions);

    return {
      beat: index + 1,
      letter: beat.pictograph_data?.letter || "",
      letter_type: "Type1",
      duration: 1,
      start_pos: `alpha${index}`,
      end_pos: `alpha${index + 1}`,
      timing: "split",
      direction: "same",
      blue_attributes: convertMotionToPropAttributes(motions?.blue),
      red_attributes: convertMotionToPropAttributes(motions?.red),
    };
  });

  // Combine into standalone format: [metadata, startPosition, ...steps]
  const standaloneData = [metadata, startPosition, ...steps];

  console.log("Converted to standalone format:", standaloneData);
  console.log("Standalone data length:", standaloneData.length);
  return standaloneData;
}

/**
 * Convert web app motion data to prop attributes
 */
function convertMotionToPropAttributes(
  motion?: WebAppMotionData
): PropAttributes {
  if (!motion) {
    // Default static motion
    return {
      start_loc: "s",
      end_loc: "s",
      start_ori: "in",
      end_ori: "in",
      prop_rot_dir: "no_rot",
      turns: 0,
      motion_type: "static",
    };
  }

  return {
    start_loc: motion.start_loc,
    end_loc: motion.end_loc,
    start_ori: motion.start_ori || "in",
    end_ori: motion.end_ori || "in",
    prop_rot_dir: motion.prop_rot_dir || "no_rot",
    turns: motion.turns || 0,
    motion_type: motion.motion_type,
  };
}

/**
 * Type guard to check if data is web app format
 */
export function isWebAppFormat(data: any): data is WebAppSequenceData {
  return (
    data &&
    typeof data === "object" &&
    "beats" in data &&
    Array.isArray(data.beats) &&
    !Array.isArray(data)
  );
}

/**
 * Type guard to check if data is standalone format
 */
export function isStandaloneFormat(data: any): boolean {
  return (
    Array.isArray(data) &&
    data.length >= 3 &&
    typeof data[0] === "object" &&
    "word" in data[0]
  );
}

/**
 * Auto-detect format and convert if needed
 */
export function ensureStandaloneFormat(data: any): any[] {
  if (isStandaloneFormat(data)) {
    console.log("Data is already in standalone format");
    return data;
  }

  if (isWebAppFormat(data)) {
    console.log("Converting web app format to standalone format");
    return convertWebAppToStandalone(data);
  }

  throw new Error(
    "Unknown sequence data format - cannot convert to standalone format"
  );
}

/**
 * Create a test sequence for demonstration when no beats are found
 */
function createTestSequence(webAppData: WebAppSequenceData): any[] {
  const word = webAppData.word || webAppData.name || "TEST";

  // Create metadata (index 0)
  const metadata = {
    word: word,
    author: webAppData.metadata?.author || "Demo",
    level: webAppData.metadata?.level || 1,
    description: "Test sequence created for animation demonstration",
  };

  // Create start state (index 1)
  const startState = {
    beat: 0,
    letter: "",
    letter_type: "Type1",
    duration: 1,
    start_pos: "alpha0",
    end_pos: "alpha0",
    timing: "split",
    direction: "same",
    blue_attributes: {
      start_loc: "s",
      end_loc: "s",
      start_ori: "in",
      end_ori: "in",
      prop_rot_dir: "no_rot",
      turns: 0,
      motion_type: "static",
    },
    red_attributes: {
      start_loc: "n",
      end_loc: "n",
      start_ori: "in",
      end_ori: "in",
      prop_rot_dir: "no_rot",
      turns: 0,
      motion_type: "static",
    },
  };

  // Create 4 test beats with simple motions
  const testBeats = [
    // Beat 1: Blue moves from s to e, Red stays at n
    {
      beat: 1,
      letter: word[0] || "T",
      letter_type: "Type1",
      duration: 1,
      start_pos: "alpha0",
      end_pos: "alpha1",
      timing: "split",
      direction: "same",
      blue_attributes: {
        start_loc: "s",
        end_loc: "e",
        start_ori: "in",
        end_ori: "in",
        prop_rot_dir: "cw",
        turns: 1,
        motion_type: "linear",
      },
      red_attributes: {
        start_loc: "n",
        end_loc: "n",
        start_ori: "in",
        end_ori: "in",
        prop_rot_dir: "no_rot",
        turns: 0,
        motion_type: "static",
      },
    },
    // Beat 2: Blue moves from e to n, Red moves from n to w
    {
      beat: 2,
      letter: word[1] || "E",
      letter_type: "Type1",
      duration: 1,
      start_pos: "alpha1",
      end_pos: "alpha2",
      timing: "split",
      direction: "same",
      blue_attributes: {
        start_loc: "e",
        end_loc: "n",
        start_ori: "in",
        end_ori: "in",
        prop_rot_dir: "cw",
        turns: 1,
        motion_type: "linear",
      },
      red_attributes: {
        start_loc: "n",
        end_loc: "w",
        start_ori: "in",
        end_ori: "in",
        prop_rot_dir: "ccw",
        turns: 1,
        motion_type: "linear",
      },
    },
    // Beat 3: Blue moves from n to w, Red moves from w to s
    {
      beat: 3,
      letter: word[2] || "S",
      letter_type: "Type1",
      duration: 1,
      start_pos: "alpha2",
      end_pos: "alpha3",
      timing: "split",
      direction: "same",
      blue_attributes: {
        start_loc: "n",
        end_loc: "w",
        start_ori: "in",
        end_ori: "in",
        prop_rot_dir: "cw",
        turns: 1,
        motion_type: "linear",
      },
      red_attributes: {
        start_loc: "w",
        end_loc: "s",
        start_ori: "in",
        end_ori: "in",
        prop_rot_dir: "ccw",
        turns: 1,
        motion_type: "linear",
      },
    },
    // Beat 4: Both return to start positions
    {
      beat: 4,
      letter: word[3] || "T",
      letter_type: "Type1",
      duration: 1,
      start_pos: "alpha3",
      end_pos: "alpha4",
      timing: "split",
      direction: "same",
      blue_attributes: {
        start_loc: "w",
        end_loc: "s",
        start_ori: "in",
        end_ori: "in",
        prop_rot_dir: "cw",
        turns: 1,
        motion_type: "linear",
      },
      red_attributes: {
        start_loc: "s",
        end_loc: "n",
        start_ori: "in",
        end_ori: "in",
        prop_rot_dir: "ccw",
        turns: 1,
        motion_type: "linear",
      },
    },
  ];

  console.log("Created test sequence with", testBeats.length, "beats");
  return [metadata, startState, ...testBeats];
}
