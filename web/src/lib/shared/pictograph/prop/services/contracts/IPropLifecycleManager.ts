/**
 * Prop Lifecycle Manager Interface
 *
 * Handles the complete lifecycle of prop rendering including asset loading and positioning
 */

import type { MotionData, PictographData } from "$shared";
import type { PropAssets, PropPosition } from "../../domain/models";

export interface IPropLifecycleManager {
  /**
   * Load prop assets for a single motion
   */
  loadPropAssets(motionData: MotionData): Promise<PropAssets>;

  /**
   * Calculate position for a single prop
   */
  calculatePropPosition(
    motionData: MotionData,
    pictographData: PictographData
  ): Promise<PropPosition>;

  /**
   * Coordinate complete prop state (assets + position)
   */
  coordinatePropState(
    motionData: MotionData,
    pictographData: PictographData
  ): Promise<{
    assets: PropAssets;
    position: PropPosition;
    isVisible: boolean;
    isLoading: boolean;
    error: string | null;
  }>;
}
