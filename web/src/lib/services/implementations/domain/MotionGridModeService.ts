/**
 * MotionGridModeService - Ultimate Clean Architecture
 *
 * Derives grid mode directly from motion data - no need to pass gridData!
 * Cardinal locations (N, E, S, W) = Diamond grid
 * Intercardinal locations (NE, SE, SW, NW) = Box grid
 *
 * This enables the ultimate clean interface: renderArrow(motion) - that's it!
 */

import type { MotionData } from "../../../domain/MotionData";
import { GridMode, Location } from "../../../domain/enums";

export class MotionGridModeService {
  /**
   * ULTIMATE CLEAN ARCHITECTURE: Derive grid mode from motion data alone
   * No need to pass gridData - motion tells us everything!
   */
  deriveGridModeFromMotion(motion: MotionData): GridMode {
    const cardinalLocations = [
      Location.NORTH,
      Location.EAST,
      Location.SOUTH,
      Location.WEST,
    ];

    // If start OR end location is cardinal, it's diamond mode
    if (
      cardinalLocations.includes(motion.startLocation) ||
      cardinalLocations.includes(motion.endLocation)
    ) {
      return GridMode.DIAMOND;
    }

    // Otherwise it's box mode (intercardinal locations)
    return GridMode.BOX;
  }

  /**
   * Check if motion uses diamond grid (cardinal locations)
   */
  usesDiamondGrid(motion: MotionData): boolean {
    return this.deriveGridModeFromMotion(motion) === GridMode.DIAMOND;
  }

  /**
   * Check if motion uses box grid (intercardinal locations)
   */
  usesBoxGrid(motion: MotionData): boolean {
    return this.deriveGridModeFromMotion(motion) === GridMode.BOX;
  }

  /**
   * Get all grid-related information from motion data
   */
  getGridInfo(motion: MotionData) {
    const gridMode = this.deriveGridModeFromMotion(motion);
    return {
      gridMode,
      isDiamond: gridMode === GridMode.DIAMOND,
      isBox: gridMode === GridMode.BOX,
      startLocation: motion.startLocation,
      endLocation: motion.endLocation,
      arrowLocation: motion.arrowLocation,
    };
  }
}
