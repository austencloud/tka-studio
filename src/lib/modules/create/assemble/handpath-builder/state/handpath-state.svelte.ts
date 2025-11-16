/**
 * Gestural Path Builder State Management
 *
 * Reactive state using Svelte 5 runes for hand path construction.
 * Implements fine-grained reactivity and immutable state updates.
 */

import type { GridMode, RotationDirection } from "$shared";
import {
  GridLocation,
  HandMotionType,
  type MotionColor,
  MotionColor as MC,
  type MotionData,
  PropType,
} from "$shared";
import { PathBuilderMode } from "../domain";
import type {
  AdvanceButtonState,
  GesturalSessionState,
  HandPath,
  HandPathSegment,
  PathBuilderConfig,
  PathBuildingState,
} from "../domain";

/**
 * Create a new gestural path builder state instance
 */
export function createGesturalPathState() {
  // ============================================================================
  // CORE STATE
  // ============================================================================

  /** Current builder mode (discrete vs continuous) */
  const mode = $state<PathBuilderMode>(PathBuilderMode.DISCRETE);

  /** Session configuration */
  let config = $state<PathBuilderConfig | null>(null);

  /** Which hand is currently being drawn (blue or red) */
  let currentHand = $state<MotionColor>(MC.BLUE);

  /** Blue hand path */
  let blueHandPath = $state<HandPath | null>(null);

  /** Red hand path */
  let redHandPath = $state<HandPath | null>(null);

  /** User-selected rotation direction */
  let selectedRotationDirection = $state<RotationDirection | null>(null);

  /** Current beat being drawn (1-indexed) */
  let currentBeatNumber = $state(1);

  /** Current hand location */
  let currentLocation = $state<GridLocation | null>(null);

  /** Completed segments for current hand */
  let completedSegments = $state<HandPathSegment[]>([]);

  /** Advance button state (for discrete mode) */
  let advanceButtonState = $state<AdvanceButtonState>({
    isPressed: false,
    pressStartTime: null,
    hasMovedSincePress: false,
  });

  /** Whether the user has started drawing */
  let hasStartedDrawing = $state(false);

  // ============================================================================
  // DERIVED STATE
  // ============================================================================

  /** Is the current hand complete? */
  const isCurrentHandComplete = $derived(
    config ? currentBeatNumber > config.sequenceLength : false
  );

  /** Are both hands complete? */
  const isSessionComplete = $derived(
    blueHandPath !== null && redHandPath !== null
  );

  /** Current building state */
  const currentBuildingState = $derived<PathBuildingState>({
    currentBeatNumber,
    currentLocation: currentLocation || GridLocation.NORTH,
    completedSegments: completedSegments as readonly HandPathSegment[],
    isComplete: isCurrentHandComplete,
  });

  /** Progress percentage for current hand */
  const progressPercentage = $derived(
    config ? (currentBeatNumber / config.sequenceLength) * 100 : 0
  );

  /** Can advance to next beat? */
  const canAdvance = $derived(
    currentLocation !== null && !isCurrentHandComplete
  );

  // ============================================================================
  // ACTIONS
  // ============================================================================

  /**
   * Initialize a new gestural path building session
   */
  function initializeSession(
    sequenceLength: number,
    gridMode: GridMode,
    startingLocation: GridLocation
  ): void {
    config = {
      sequenceLength,
      gridMode,
      startingLocation,
      allowedHandMotionTypes: [
        HandMotionType.SHIFT,
        HandMotionType.DASH,
        HandMotionType.STATIC,
      ],
    };

    currentHand = MC.BLUE;
    currentBeatNumber = 1;
    currentLocation = startingLocation;
    completedSegments = [];
    blueHandPath = null;
    redHandPath = null;
    selectedRotationDirection = null;
    hasStartedDrawing = false;
  }

  /**
   * Record a hand path segment
   */
  function recordSegment(
    startLocation: GridLocation,
    endLocation: GridLocation,
    handMotionType: HandMotionType
  ): void {
    const segment: HandPathSegment = {
      beatNumber: currentBeatNumber,
      startLocation,
      endLocation,
      handMotionType,
      timestamp: Date.now(),
    };

    completedSegments = [...completedSegments, segment];
    currentLocation = endLocation;
    currentBeatNumber++;
    hasStartedDrawing = true;
  }

  /**
   * Complete current hand and move to next hand
   */
  function completeCurrentHand(): void {
    if (!config || !currentLocation) return;

    const handPath: HandPath = {
      handColor: currentHand,
      segments: completedSegments as readonly HandPathSegment[],
      gridMode: config.gridMode,
      startingLocation: config.startingLocation,
    };

    if (currentHand === MC.BLUE) {
      blueHandPath = handPath;
      // Switch to red hand
      currentHand = MC.RED;
      currentBeatNumber = 1;
      currentLocation = config.startingLocation;
      completedSegments = [];
      hasStartedDrawing = false;
    } else {
      redHandPath = handPath;
      // Session complete
    }
  }

  /**
   * Delete a beat and all subsequent beats
   */
  function deleteBeatAndSubsequent(beatNumber: number): void {
    completedSegments = completedSegments.filter(
      (seg) => seg.beatNumber < beatNumber
    );
    currentBeatNumber = beatNumber;

    // Update current location to the end of the last remaining segment
    if (completedSegments.length > 0) {
      currentLocation =
        completedSegments[completedSegments.length - 1]!.endLocation;
    } else {
      currentLocation = config?.startingLocation || null;
    }
  }

  /**
   * Set rotation direction
   */
  function setRotationDirection(direction: RotationDirection): void {
    selectedRotationDirection = direction;
  }

  /**
   * Press advance button (discrete mode)
   */
  function pressAdvanceButton(): void {
    advanceButtonState = {
      isPressed: true,
      pressStartTime: Date.now(),
      hasMovedSincePress: false,
    };
  }

  /**
   * Release advance button (discrete mode)
   */
  function releaseAdvanceButton(): void {
    // If released without movement, record a static motion
    if (!advanceButtonState.hasMovedSincePress && currentLocation) {
      recordSegment(currentLocation, currentLocation, HandMotionType.STATIC);
    }

    advanceButtonState = {
      isPressed: false,
      pressStartTime: null,
      hasMovedSincePress: false,
    };
  }

  /**
   * Mark that movement occurred while button pressed
   */
  function markMovementOccurred(): void {
    advanceButtonState = {
      ...advanceButtonState,
      hasMovedSincePress: true,
    };
  }

  /**
   * Update current location (during drag)
   */
  function updateCurrentLocation(location: GridLocation): void {
    currentLocation = location;
  }

  /**
   * Reset session
   */
  function reset(): void {
    config = null;
    currentHand = MC.BLUE;
    currentBeatNumber = 1;
    currentLocation = null;
    completedSegments = [];
    blueHandPath = null;
    redHandPath = null;
    selectedRotationDirection = null;
    hasStartedDrawing = false;
    advanceButtonState = {
      isPressed: false,
      pressStartTime: null,
      hasMovedSincePress: false,
    };
  }

  /**
   * Go back to blue hand (restart from blue)
   */
  function backToBlueHand(): void {
    if (!config) return;

    currentHand = MC.BLUE;
    currentBeatNumber = 1;
    currentLocation = config.startingLocation;
    completedSegments = [];
    hasStartedDrawing = false;
  }

  // ============================================================================
  // PUBLIC API
  // ============================================================================

  return {
    // State (readonly access)
    get mode() {
      return mode;
    },
    get config() {
      return config;
    },
    get currentHand() {
      return currentHand;
    },
    get blueHandPath() {
      return blueHandPath;
    },
    get redHandPath() {
      return redHandPath;
    },
    get selectedRotationDirection() {
      return selectedRotationDirection;
    },
    get currentBeatNumber() {
      return currentBeatNumber;
    },
    get currentLocation() {
      return currentLocation;
    },
    get completedSegments() {
      return completedSegments as readonly HandPathSegment[];
    },
    get advanceButtonState() {
      return advanceButtonState;
    },
    get hasStartedDrawing() {
      return hasStartedDrawing;
    },

    // Derived state
    get isCurrentHandComplete() {
      return isCurrentHandComplete;
    },
    get isSessionComplete() {
      return isSessionComplete;
    },
    get currentBuildingState() {
      return currentBuildingState;
    },
    get progressPercentage() {
      return progressPercentage;
    },
    get canAdvance() {
      return canAdvance;
    },

    // Actions
    initializeSession,
    recordSegment,
    completeCurrentHand,
    deleteBeatAndSubsequent,
    setRotationDirection,
    pressAdvanceButton,
    releaseAdvanceButton,
    markMovementOccurred,
    updateCurrentLocation,
    reset,
    backToBlueHand,
  };
}

export type GesturalPathState = ReturnType<typeof createGesturalPathState>;
