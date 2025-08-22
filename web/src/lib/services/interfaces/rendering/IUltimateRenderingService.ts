/**
 * IUltimateRenderingService - The Ultimate Clean Architecture Interface
 *
 * REVOLUTIONARY: Rendering services take ONLY motion data!
 * Everything else is derived:
 * - Grid mode from motion locations (cardinal = diamond, intercardinal = box)
 * - Arrow placement from motion.arrowLocation
 * - Prop placement from motion.endLocation + motion.endOrientation
 * - Visibility from motion.isVisible
 * - Prop type from motion.propType
 *
 * This is the cleanest possible interface - single parameter, zero redundancy!
 */

import type { MotionData } from "../../../domain/MotionData";

export interface IUltimateArrowRenderingService {
  /**
   * ULTIMATE CLEAN INTERFACE: Render arrow from motion data alone!
   *
   * Derives everything needed:
   * - Grid mode from motion.startLocation/endLocation
   * - Arrow location from motion.arrowLocation
   * - Visibility from motion.isVisible
   * - Positioning calculated on-demand
   */
  renderArrow(motion: MotionData): Promise<{
    svgContent: string;
    placement: {
      positionX: number;
      positionY: number;
      rotationAngle: number;
      coordinates: { x: number; y: number } | null;
      svgCenter: { x: number; y: number } | null;
      svgMirrored: boolean;
    };
  }>;

  /**
   * Check if arrow should be visible based on motion data
   */
  isArrowVisible(motion: MotionData): boolean;

  /**
   * Calculate arrow placement from motion data
   */
  calculateArrowPlacement(motion: MotionData): {
    positionX: number;
    positionY: number;
    rotationAngle: number;
    coordinates: { x: number; y: number } | null;
    svgCenter: { x: number; y: number } | null;
    svgMirrored: boolean;
  };
}

export interface IUltimatePropRenderingService {
  /**
   * ULTIMATE CLEAN INTERFACE: Render prop from motion data alone!
   *
   * Derives everything needed:
   * - Grid mode from motion.startLocation/endLocation
   * - Prop type from motion.propType
   * - Prop orientation from motion.endOrientation
   * - Prop location from motion.endLocation
   * - Visibility from motion.isVisible
   * - Positioning calculated on-demand
   */
  renderProp(motion: MotionData): Promise<{
    svgContent: string;
    placement: {
      positionX: number;
      positionY: number;
      rotationAngle: number;
    };
  }>;

  /**
   * Check if prop should be visible based on motion data
   */
  isPropVisible(motion: MotionData): boolean;

  /**
   * Calculate prop placement from motion data
   */
  calculatePropPlacement(motion: MotionData): {
    positionX: number;
    positionY: number;
    rotationAngle: number;
  };
}

export interface IUltimatePictographRenderingService {
  /**
   * ULTIMATE CLEAN INTERFACE: Render entire pictograph from motion data!
   *
   * Takes blue and red motion data, renders complete pictograph
   */
  renderPictograph(
    blueMotion: MotionData,
    redMotion: MotionData
  ): Promise<{
    svgContent: string;
    arrows: {
      blue: ReturnType<IUltimateArrowRenderingService["renderArrow"]>;
      red: ReturnType<IUltimateArrowRenderingService["renderArrow"]>;
    };
    props: {
      blue: ReturnType<IUltimatePropRenderingService["renderProp"]>;
      red: ReturnType<IUltimatePropRenderingService["renderProp"]>;
    };
  }>;
}
