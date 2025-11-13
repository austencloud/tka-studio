/**
 * Guided Construct State (Svelte 5 Runes)
 *
 * Two-phase state machine for Guided Construct mode:
 * 1. Blue Hand Phase - Build blue hand sequence
 * 2. Red Hand Phase - Build red hand sequence (same length)
 * 3. Merge - Combine blue + red into dual-prop sequence
 *
 * Similar to handpath-state.svelte.ts but works with pictographs instead of raw paths
 */

import {
  GridLocation,
  GridMode,
  MotionColor,
  PropType,
  type PictographData,
} from "$shared";
import { createPictographData } from "$shared";

type BuildPhase = "blue" | "red" | "complete";

export interface GuidedConstructConfig {
  startingLocation: GridLocation;
  gridMode: GridMode;
  propType: PropType;
}

export interface GuidedConstructState {
  // Phase tracking
  readonly currentPhase: BuildPhase;
  readonly currentHand: MotionColor;

  // Current build state
  readonly currentLocation: GridLocation;
  readonly currentBeatNumber: number; // 1-indexed (Beat 1, Beat 2, etc.)

  // Sequences
  readonly blueSequence: readonly PictographData[];
  readonly redSequence: readonly PictographData[];
  readonly mergedSequence: readonly PictographData[];

  // Computed states
  readonly blueSequenceLength: number;
  readonly isBlueHandComplete: boolean;
  readonly isRedHandComplete: boolean;
  readonly isComplete: boolean;

  // Configuration
  readonly config: GuidedConstructConfig;

  // Actions
  addBlueBeat: (pictograph: PictographData) => void;
  addRedBeat: (pictograph: PictographData) => void;
  completeBlueHand: () => void;
  reset: () => void;
  updateConfig: (config: Partial<GuidedConstructConfig>) => void;
}

export function createGuidedConstructState(
  initialConfig?: Partial<GuidedConstructConfig>
): GuidedConstructState {
  // Default configuration
  let config = $state<GuidedConstructConfig>({
    startingLocation: initialConfig?.startingLocation ?? GridLocation.NORTH,
    gridMode: initialConfig?.gridMode ?? GridMode.DIAMOND,
    propType: initialConfig?.propType ?? PropType.HAND,
  });

  // Phase tracking
  let currentPhase = $state<BuildPhase>("blue");

  // Current build state - use derived to reference config reactively
  let currentLocation = $state<GridLocation>(
    initialConfig?.startingLocation ?? GridLocation.NORTH
  );
  let currentBeatNumber = $state(1); // 1-indexed

  // Sequences (mutable arrays)
  let blueSequence = $state<PictographData[]>([]);
  let redSequence = $state<PictographData[]>([]);
  let mergedSequence = $state<PictographData[]>([]);

  // Computed: current hand color
  const currentHand = $derived<MotionColor>(
    currentPhase === "blue" ? MotionColor.BLUE : MotionColor.RED
  );

  // Computed: blue sequence length (locked when moving to red phase)
  const blueSequenceLength = $derived(blueSequence.length);

  // Computed: completion states
  const isBlueHandComplete = $derived(currentPhase !== "blue");
  const isRedHandComplete = $derived(
    currentPhase === "red" && redSequence.length >= blueSequenceLength
  );
  const isComplete = $derived(currentPhase === "complete");

  // Add beat to blue sequence
  function addBlueBeat(pictograph: PictographData): void {
    if (currentPhase !== "blue") {
      console.warn("Cannot add blue beat - not in blue phase");
      return;
    }

    blueSequence.push(pictograph);

    // Update current location to end location of the selected pictograph
    const blueMotion = pictograph.motions.blue;
    if (blueMotion?.endLocation) {
      currentLocation = blueMotion.endLocation;
    }

    currentBeatNumber++;
  }

  // Add beat to red sequence
  function addRedBeat(pictograph: PictographData): void {
    if (currentPhase !== "red") {
      console.warn("Cannot add red beat - not in red phase");
      return;
    }

    redSequence.push(pictograph);

    // Update current location to end location of the selected pictograph
    const redMotion = pictograph.motions.red;
    if (redMotion?.endLocation) {
      currentLocation = redMotion.endLocation;
    }

    currentBeatNumber++;

    // Auto-complete when red sequence matches blue length
    if (redSequence.length >= blueSequenceLength) {
      completeBuild();
    }
  }

  // Complete blue hand and transition to red hand
  function completeBlueHand(): void {
    if (currentPhase !== "blue") {
      console.warn("Cannot complete blue hand - not in blue phase");
      return;
    }

    if (blueSequence.length === 0) {
      console.warn("Cannot complete blue hand - no beats added");
      return;
    }

    // Transition to red phase
    currentPhase = "red";
    currentLocation = config.startingLocation; // Reset to start
    currentBeatNumber = 1; // Reset beat counter
  }

  // Complete entire build (merge sequences)
  function completeBuild(): void {
    currentPhase = "complete";
    mergedSequence = mergeBluAndRedSequences();
  }

  // Merge blue and red sequences into dual-prop pictographs
  function mergeBluAndRedSequences(): PictographData[] {
    if (blueSequence.length !== redSequence.length) {
      console.error("Cannot merge: sequences have different lengths");
      return [];
    }

    return blueSequence.map((blueBeat, index) => {
      const redBeat = redSequence[index];

      if (!blueBeat || !redBeat) {
        console.error(`Missing beat at index ${index}`);
        return createPictographData();
      }

      // Merge the two single-prop pictographs into one dual-prop pictograph
      return createPictographData({
        motions: {
          blue: blueBeat.motions.blue,
          red: redBeat.motions.red,
        },
      });
    });
  }

  // Reset to initial state
  function reset(): void {
    currentPhase = "blue";
    currentLocation = config.startingLocation;
    currentBeatNumber = 1;
    blueSequence = [];
    redSequence = [];
    mergedSequence = [];
  }

  // Update configuration
  function updateConfig(newConfig: Partial<GuidedConstructConfig>): void {
    config = { ...config, ...newConfig };

    // If starting location changed, update current location (only if no beats added yet)
    if (newConfig.startingLocation && blueSequence.length === 0) {
      currentLocation = newConfig.startingLocation;
    }
  }

  // Return readonly state + actions
  return {
    get currentPhase() {
      return currentPhase;
    },
    get currentHand() {
      return currentHand;
    },
    get currentLocation() {
      return currentLocation;
    },
    get currentBeatNumber() {
      return currentBeatNumber;
    },
    get blueSequence() {
      return blueSequence as readonly PictographData[];
    },
    get redSequence() {
      return redSequence as readonly PictographData[];
    },
    get mergedSequence() {
      return mergedSequence as readonly PictographData[];
    },
    get blueSequenceLength() {
      return blueSequenceLength;
    },
    get isBlueHandComplete() {
      return isBlueHandComplete;
    },
    get isRedHandComplete() {
      return isRedHandComplete;
    },
    get isComplete() {
      return isComplete;
    },
    get config() {
      return config;
    },

    addBlueBeat,
    addRedBeat,
    completeBlueHand,
    reset,
    updateConfig,
  };
}
