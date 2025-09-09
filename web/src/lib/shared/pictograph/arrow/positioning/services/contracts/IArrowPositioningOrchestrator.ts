/**
 * Arrow Positioning Orchestrator Interface
 *
 * Main orchestrator for arrow positioning calculations.
 * Coordinates the entire arrow positioning pipeline.
 */

import type { ArrowPlacementData, MotionData, PictographData } from "$shared";

export interface IArrowPositioningOrchestrator {
  /**
   * Calculate complete arrow position using the positioning pipeline.
   */
  calculateArrowPoint(
    pictographData: PictographData,
    motionData?: MotionData
  ): Promise<[number, number, number]>;

  /**
   * Calculate positions for all arrows in the pictograph.
   */
  calculateAllArrowPoints(
    pictographData: PictographData
  ): Promise<PictographData>;

  /**
   * Determine if arrow should be mirrored based on motion type.
   */
  shouldMirrorArrow(
    arrowData: ArrowPlacementData,
    pictographData?: PictographData,
    motionData?: MotionData
  ): boolean;

  /**
   * Apply mirror transformation to arrow graphics item.
   */
  applyMirrorTransform(
    arrowItem: HTMLElement | SVGElement,
    shouldMirror: boolean
  ): void;
}
