/**
 * Arrow Positioning Service Contract
 *
 * Service for arrow positioning in Svelte components.
 * Thin wrapper around ArrowPositioningOrchestrator.
 */

import type {
    ArrowPlacementData,
    GridLocation,
    GridMode,
    Letter,
    MotionColor,
    MotionData,
    MotionType,
    Orientation,
    PictographData,
} from "$shared";

export interface ArrowPositionResult {
  x: number;
  y: number;
  rotation: number;
}

export interface ArrowPositioningInput {
  color: MotionColor;
  motionType: MotionType;
  location: GridLocation;
  gridMode: GridMode;
  turns: number;
  letter: Letter;
  startOrientation: Orientation;
  endOrientatio?: Orientation;
}

export interface IArrowPositioningService {
  calculatePosition(
    arrowData: ArrowPlacementData,
    motionData: MotionData,
    pictographData: PictographData
  ): Promise<ArrowPositionResult>;
  shouldMirror(
    arrowData: ArrowPlacementData,
    motionData: MotionData,
    pictographData: PictographData
  ): boolean;
}
