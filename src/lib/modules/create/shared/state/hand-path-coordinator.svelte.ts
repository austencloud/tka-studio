/**
 * Hand Path Coordinator State
 *
 * Manages state coordination between HandPathWorkspace and HandPathToolPanel.
 * Provides a single source of truth for hand path drawing state.
 */

import { GridLocation, GridMode, PropType, resolve, TYPES } from "$shared";
import type {
  IHandPathDirectionDetector,
  IPathToMotionConverter,
} from "../../construct/handpath-builder/services/contracts";
import {
  createGesturalPathState,
  type GesturalPathState,
} from "../../construct/handpath-builder/state";

export function createHandPathCoordinator() {
  // Services
  let handPathDirectionDetector: IHandPathDirectionDetector | null = null;
  let pathToMotionConverter: IPathToMotionConverter | null = null;

  // State
  const pathState: GesturalPathState = createGesturalPathState();
  let sequenceLength = $state(16);
  let gridMode = $state<GridMode>(GridMode.DIAMOND);
  let isStarted = $state(false);

  // Initialize services
  function initializeServices() {
    if (!handPathDirectionDetector) {
      handPathDirectionDetector = resolve<IHandPathDirectionDetector>(
        TYPES.IHandPathDirectionDetector
      );
    }
    if (!pathToMotionConverter) {
      pathToMotionConverter = resolve<IPathToMotionConverter>(
        TYPES.IPathToMotionConverter
      );
    }
  }

  // Start or restart drawing
  function startDrawing(): void {
    const startLocation =
      gridMode === GridMode.DIAMOND
        ? GridLocation.NORTH
        : GridLocation.NORTHEAST;
    pathState.initializeSession(sequenceLength, gridMode, startLocation);
    isStarted = true;
  }

  // Handle segment complete
  function handleSegmentComplete(start: GridLocation, end: GridLocation): void {
    if (!handPathDirectionDetector || !pathState.config) return;

    const handMotionType = handPathDirectionDetector.getHandMotionType(
      start,
      end,
      pathState.config.gridMode
    );

    pathState.recordSegment(start, end, handMotionType);

    // Auto-complete hand if all beats drawn
    if (pathState.isCurrentHandComplete) {
      pathState.completeCurrentHand();
    }
  }

  // Handle advance button press
  function handleAdvancePressed(): void {
    pathState.pressAdvanceButton();
  }

  // Handle advance button release
  function handleAdvanceReleased(): void {
    pathState.releaseAdvanceButton();
  }

  // Handle hand complete
  function handleHandComplete(): void {
    pathState.completeCurrentHand();
  }

  // Handle restart - reset current drawing session
  function handleRestart(): void {
    pathState.reset();
  }

  // Handle back to settings - reset and return to pre-flight view
  function handleBackToSettings(): void {
    pathState.reset();
    isStarted = false;
  }

  // Handle finish
  function handleFinish(
    onSequenceComplete?: (motions: { blue: any[]; red: any[] }) => void
  ): void {
    if (!pathToMotionConverter || !pathState.selectedRotationDirection) {
      alert("Please select a rotation direction before finishing.");
      return;
    }

    const blueMotions = pathState.blueHandPath
      ? pathToMotionConverter.convertHandPathToMotions(
          pathState.blueHandPath,
          pathState.selectedRotationDirection,
          PropType.HAND
        )
      : [];

    const redMotions = pathState.redHandPath
      ? pathToMotionConverter.convertHandPathToMotions(
          pathState.redHandPath,
          pathState.selectedRotationDirection,
          PropType.HAND
        )
      : [];

    onSequenceComplete?.({ blue: blueMotions, red: redMotions });

    // Reset state and return to settings after completion
    handleBackToSettings();
  }

  // Handle back to blue
  function handleBackToBlue(): void {
    pathState.backToBlueHand();
  }

  return {
    // State (read-only getters)
    get pathState() {
      return pathState;
    },
    get sequenceLength() {
      return sequenceLength;
    },
    set sequenceLength(value: number) {
      sequenceLength = value;
    },
    get gridMode() {
      return gridMode;
    },
    set gridMode(value: GridMode) {
      gridMode = value;
    },
    get isStarted() {
      return isStarted;
    },

    // Actions
    initializeServices,
    startDrawing,
    handleSegmentComplete,
    handleAdvancePressed,
    handleAdvanceReleased,
    handleHandComplete,
    handleRestart,
    handleBackToSettings,
    handleFinish,
    handleBackToBlue,
  };
}

export type HandPathCoordinator = ReturnType<typeof createHandPathCoordinator>;
