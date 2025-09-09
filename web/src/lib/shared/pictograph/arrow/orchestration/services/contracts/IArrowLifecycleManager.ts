/**
 * Arrow Lifecycle Manager Contract
 *
 * Single responsibility service for coordinating all arrow lifecycle operations.
 * Separates concerns from components and provides clean coordination.
 */

import type { MotionData, PictographData } from "$shared";
import type {
  ArrowAssets,
  ArrowLifecycleResult,
  ArrowPosition,
  ArrowState,
} from "../../domain";

/**
 * Arrow Lifecycle Manager - Single point of coordination for all arrow operations
 */
export interface IArrowLifecycleManager {
  /**
   * Load arrow assets for a single motion
   */
  loadArrowAssets(motionData: MotionData): Promise<ArrowAssets>;

  /**
   * Calculate position for a single arrow
   */
  calculateArrowPosition(
    motionData: MotionData,
    pictographData: PictographData
  ): Promise<ArrowPosition>;

  /**
   * Determine if arrow should be mirrored
   */
  shouldMirrorArrow(
    motionData: MotionData,
    pictographData: PictographData
  ): boolean;

  /**
   * Get complete arrow state for a single motion
   */
  getArrowState(
    motionData: MotionData,
    pictographData: PictographData
  ): Promise<ArrowState>;

  /**
   * Coordinate complete arrow lifecycle for all motions in pictograph
   * This is the main coordination method that ensures proper loading order
   */
  coordinateArrowLifecycle(
    pictographData: PictographData
  ): Promise<ArrowLifecycleResult>;

  /**
   * Reset arrow state (for data changes)
   */
  resetArrowState(): void;
}
