/**
 * Prop Lifecycle Manager Service
 *
 * Handles the complete lifecycle of prop rendering including asset loading and positioning.
 * Mirrors the ArrowLifecycleManager pattern for consistency.
 */

import { inject, injectable } from "inversify";
import { TYPES, type MotionData, type PictographData } from "$shared";
import type { IPropLifecycleManager } from "../contracts/IPropLifecycleManager";
import type { IPropSvgLoader } from "../contracts/IPropSvgLoader";
import type { IPropPlacementService } from "../contracts/IPropPlacementService";
import type { PropAssets, PropPosition } from "../../domain/models";

@injectable()
export class PropLifecycleManager implements IPropLifecycleManager {
  constructor(
    @inject(TYPES.IPropSvgLoader) private svgLoader: IPropSvgLoader,
    @inject(TYPES.IPropPlacementService) private placementService: IPropPlacementService
  ) {}

  /**
   * Load prop assets for a single motion
   */
  async loadPropAssets(motionData: MotionData): Promise<PropAssets> {
    try {
      if (!motionData.propPlacementData) {
        throw new Error('No prop placement data available');
      }

      const renderData = await this.svgLoader.loadPropSvg(
        motionData.propPlacementData,
        motionData
      );

      if (!renderData.svgData) {
        throw new Error('Failed to load prop SVG data');
      }

      return {
        imageSrc: renderData.svgData.svgContent,
        viewBox: `${renderData.svgData.viewBox.width} ${renderData.svgData.viewBox.height}`,
        center: renderData.svgData.center,
      };
    } catch (error) {
      console.error('Failed to load prop assets:', error);
      throw error;
    }
  }

  /**
   * Calculate position for a single prop
   */
  async calculatePropPosition(
    motionData: MotionData,
    pictographData: PictographData
  ): Promise<PropPosition> {
    try {
      const placementData = await this.placementService.calculatePlacement(
        pictographData,
        motionData
      );

      return {
        x: placementData.positionX,
        y: placementData.positionY,
        rotation: placementData.rotationAngle,
      };
    } catch (error) {
      console.error('Failed to calculate prop position:', error);
      throw error;
    }
  }

  /**
   * Coordinate complete prop state (assets + position)
   */
  async coordinatePropState(
    motionData: MotionData,
    pictographData: PictographData
  ): Promise<{
    assets: PropAssets;
    position: PropPosition;
    isVisible: boolean;
    isLoading: boolean;
    error: string | null;
  }> {
    try {
      // Load assets and calculate position in parallel
      const [assets, position] = await Promise.all([
        this.loadPropAssets(motionData),
        this.calculatePropPosition(motionData, pictographData),
      ]);

      return {
        assets,
        position,
        isVisible: true,
        isLoading: false,
        error: null,
      };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      
      // Return fallback state
      return {
        assets: {
          imageSrc: `<rect x="25" y="10" width="50" height="80" fill="${motionData.color === 'blue' ? '#2E3192' : '#ED1C24'}"/>`,
          viewBox: "100 100",
          center: { x: 50, y: 50 },
        },
        position: { x: 475, y: 475, rotation: 0 },
        isVisible: false,
        isLoading: false,
        error: errorMessage,
      };
    }
  }
}
