/**
 * Arrow Lifecycle Manager Implementation
 *
 * Single responsibility service for coordinating all arrow lifecycle operations.
 * Orchestrates loading, positioning, and state management for arrows.
 */

import { inject, injectable } from "inversify";
import { TYPES } from "../../../../../inversify";
import type { MotionData, PictographData } from "../../../../shared";
import type { IArrowPositioningOrchestrator } from "../../../positioning/services";
import type { IArrowRenderer } from "../../../rendering";
import {
  type ArrowAssets,
  type ArrowLifecycleResult,
  type ArrowPosition,
  type ArrowState,
  createArrowAssets,
  createArrowLifecycleResult,
  createArrowPosition,
  createArrowState,
} from "../../domain";
import type { IArrowLifecycleManager } from "../contracts";

@injectable()
export class ArrowLifecycleManager implements IArrowLifecycleManager {
  constructor(
    @inject(TYPES.IArrowRenderer) private arrowRenderer: IArrowRenderer,
    @inject(TYPES.IArrowPositioningOrchestrator)
    private positioningOrchestrator: IArrowPositioningOrchestrator
  ) {}

  /**
   * Load arrow assets for a single motion
   */
  async loadArrowAssets(motionData: MotionData): Promise<ArrowAssets> {
    if (!motionData.arrowPlacementData) {
      throw new Error("No arrow placement data available");
    }

    const svgData = await this.arrowRenderer.loadArrowSvg(
      motionData.arrowPlacementData,
      motionData
    );

    return createArrowAssets({
      imageSrc: svgData.imageSrc,
      viewBox: svgData.viewBox,
      center: svgData.center,
    });
  }

  /**
   * Calculate position for a single arrow
   */
  async calculateArrowPosition(
    motionData: MotionData,
    pictographData: PictographData
  ): Promise<ArrowPosition> {
    const [x, y, rotation] =
      await this.positioningOrchestrator.calculateArrowPoint(
        pictographData,
        motionData
      );

    // Apply manual adjustments from keyboard controls (WASD)
    const manualAdjustX =
      motionData.arrowPlacementData?.manualAdjustmentX || 0;
    const manualAdjustY =
      motionData.arrowPlacementData?.manualAdjustmentY || 0;

    return createArrowPosition({
      x: x + manualAdjustX,
      y: y + manualAdjustY,
      rotation,
    });
  }

  /**
   * Determine if arrow should be mirrored
   */
  shouldMirrorArrow(
    motionData: MotionData,
    pictographData: PictographData
  ): boolean {
    if (!motionData.arrowPlacementData) {
      return false;
    }

    return this.positioningOrchestrator.shouldMirrorArrow(
      motionData.arrowPlacementData,
      pictographData,
      motionData
    );
  }

  /**
   * Get complete arrow state for a single motion
   */
  async getArrowState(
    motionData: MotionData,
    pictographData: PictographData
  ): Promise<ArrowState> {
    try {
      // Load assets and calculate position in parallel
      const [assets, position] = await Promise.all([
        this.loadArrowAssets(motionData),
        this.calculateArrowPosition(motionData, pictographData),
      ]);

      const shouldMirror = this.shouldMirrorArrow(motionData, pictographData);

      return createArrowState({
        assets,
        position,
        shouldMirror,
        isVisible: true,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Unknown error";
      return createArrowState({
        assets: null,
        position: null,
        shouldMirror: false,
        isVisible: false,
        isLoading: false,
        error: errorMessage,
      });
    }
  }

  /**
   * Coordinate complete arrow lifecycle for all motions in pictograph
   * This is the main coordination method that ensures proper loading order
   */
  async coordinateArrowLifecycle(
    pictographData: PictographData
  ): Promise<ArrowLifecycleResult> {
    if (!pictographData.motions) {
      return createArrowLifecycleResult({ allReady: true });
    }

    const positions: Record<string, ArrowPosition> = {};
    const mirroring: Record<string, boolean> = {};
    const assets: Record<string, ArrowAssets> = {};
    const errors: Record<string, string> = {};

    // Process all motions in parallel for better performance
    const motionPromises = Object.entries(pictographData.motions).map(
      async ([color, motionData]) => {
        try {
          const arrowState = await this.getArrowState(
            motionData!,
            pictographData
          );

          if (arrowState.error) {
            errors[color] = arrowState.error;
          } else if (arrowState.assets && arrowState.position) {
            positions[color] = arrowState.position;
            mirroring[color] = arrowState.shouldMirror;
            assets[color] = arrowState.assets;
          }
        } catch (error) {
          const errorMessage =
            error instanceof Error ? error.message : "Unknown error";
          errors[color] = errorMessage;
        }
      }
    );

    await Promise.all(motionPromises);

    const allReady =
      Object.keys(errors).length === 0 && Object.keys(positions).length > 0;

    return createArrowLifecycleResult({
      positions,
      mirroring,
      assets,
      allReady,
      errors,
    });
  }

  /**
   * Reset arrow state (for data changes)
   */
  resetArrowState(): void {
    // This method can be used to clear any internal caches or state
    // Currently no internal state to reset, but provides extension point
  }
}
