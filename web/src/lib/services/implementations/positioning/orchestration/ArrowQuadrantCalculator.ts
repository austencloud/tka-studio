/**
 * Arrow Quadrant Calculator
 *
 * Handles quadrant index calculations for different grid modes and motion types.
 * Implements sophisticated quadrant mapping logic from desktop implementations.
 */

import type { MotionData } from "$domain";
import { GridMode, Location, MotionType } from "$domain";

export class ArrowQuadrantCalculator {
  calculateQuadrantIndex(motion: MotionData, location: Location): number {
    /**
     * Calculate quadrant index for the given motion and arrow location.
     * Uses motion-type-specific and grid-mode-specific mappings.
     */
    const gridMode = this.determineGridMode(motion);
    const motionType = motion.motionType;

    // Apply sophisticated quadrant mapping based on grid mode and motion type
    if (gridMode === GridMode.DIAMOND) {
      if (this.isShiftMotion(motionType)) {
        return this.diamondShiftQuadrantIndex(location);
      } else {
        return this.diamondStaticDashQuadrantIndex(location);
      }
    } else {
      // Box grid mode
      if (this.isShiftMotion(motionType)) {
        return this.boxShiftQuadrantIndex(location);
      } else {
        return this.boxStaticDashQuadrantIndex(location);
      }
    }
  }

  private determineGridMode(motion: MotionData): GridMode {
    /**
     * Determine grid mode (diamond/box) based on motion start/end locations.
     * Diagonal locations (NE, SE, SW, NW) indicate diamond mode.
     * Cardinal locations (N, E, S, W) indicate box mode.
     */
    const diagonalLocations = [
      Location.NORTHEAST,
      Location.SOUTHEAST,
      Location.SOUTHWEST,
      Location.NORTHWEST,
    ];

    // Check both start and end locations for diagonal positions
    const startIsDiagonal = diagonalLocations.includes(motion.startLocation);
    const endIsDiagonal = diagonalLocations.includes(motion.endLocation);

    // If either start or end is diagonal, it's diamond mode
    if (startIsDiagonal || endIsDiagonal) {
      return GridMode.DIAMOND;
    }

    return GridMode.BOX;
  }

  private isShiftMotion(motionType: MotionType): boolean {
    /**
     * Check if motion type is a shift motion (PRO/ANTI/FLOAT).
     */
    return [MotionType.PRO, MotionType.ANTI, MotionType.FLOAT].includes(
      motionType
    );
  }

  private diamondShiftQuadrantIndex(location: Location): number {
    /**
     * Get quadrant index for shift motions (PRO/ANTI/FLOAT) in diamond grid.
     */
    const locationToIndex: Partial<Record<Location, number>> = {
      [Location.NORTHEAST]: 0,
      [Location.SOUTHEAST]: 1,
      [Location.SOUTHWEST]: 2,
      [Location.NORTHWEST]: 3,
    };
    return locationToIndex[location] || 0;
  }

  private diamondStaticDashQuadrantIndex(location: Location): number {
    /**
     * Get quadrant index for static/dash motions in diamond grid.
     */
    const locationToIndex: Partial<Record<Location, number>> = {
      [Location.NORTH]: 0,
      [Location.EAST]: 1,
      [Location.SOUTH]: 2,
      [Location.WEST]: 3,
    };
    return locationToIndex[location] || 0;
  }

  private boxShiftQuadrantIndex(location: Location): number {
    /**
     * Get quadrant index for shift motions (PRO/ANTI/FLOAT) in box grid.
     */
    const locationToIndex: Partial<Record<Location, number>> = {
      [Location.NORTH]: 0,
      [Location.EAST]: 1,
      [Location.SOUTH]: 2,
      [Location.WEST]: 3,
    };
    return locationToIndex[location] || 0;
  }

  private boxStaticDashQuadrantIndex(location: Location): number {
    /**
     * Get quadrant index for static/dash motions in box grid.
     */
    const locationToIndex: Partial<Record<Location, number>> = {
      [Location.NORTHEAST]: 0,
      [Location.SOUTHEAST]: 1,
      [Location.SOUTHWEST]: 2,
      [Location.NORTHWEST]: 3,
    };
    return locationToIndex[location] || 0;
  }
}
