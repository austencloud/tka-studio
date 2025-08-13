/**
 * Directionexport interface IDirectionalTupleService {
	calculateDirectionalTuple(_motion: MotionData, location: Location): [number, number];
	generateDirectionalTuples(
		_motion: MotionData,
		baseX: number,
		baseY: number
	): Array<[number, number]>;
} Processor
 *
 * Handles complex directional tuple processing for arrow positioning adjustments.
 * Direct TypeScript port of the Python DirectionalTupleProcessor.
 *
 * This service handles:
 * - Directional tuple generation based on motion data
 * - Quadrant index calculation for proper tuple selection
 * - Complex adjustment processing for different motion types
 */

import type { MotionData } from "$lib/domain";
import { Location } from "$lib/domain";
import type { Point } from "../../types";

export interface IDirectionalTupleCalculator {
  calculateDirectionalTuple(
    motion: MotionData,
    location: Location,
  ): [number, number];
  generateDirectionalTuples(
    motion: MotionData,
    baseX: number,
    baseY: number,
  ): Array<[number, number]>;
}

export interface IQuadrantIndexCalculator {
  calculateQuadrantIndex(location: Location): number;
}

export interface IDirectionalTupleProcessor {
  processDirectionalTuples(
    baseAdjustment: Point,
    _motion: MotionData,
    location: Location,
  ): Point;
}

export class DirectionalTupleCalculator implements IDirectionalTupleCalculator {
  /**
   * Calculator for directional tuples used in arrow positioning.
   */

  calculateDirectionalTuple(
    _motion: MotionData,
    _location: Location,
  ): [number, number] {
    /**
     * Legacy parity: Additional directional tuple is not separately added.
     * The selection is made directly from the generated 4-tuples.
     */
    return [0, 0];
  }

  generateDirectionalTuples(
    motion: MotionData,
    baseX: number,
    baseY: number,
  ): Array<[number, number]> {
    /**
     * Generate directional tuples using legacy mappings by motion type, rotation, and inferred grid.
     * Tuple order: indices 0..3 correspond to NE, SE, SW, NW quadrant mapping.
     */
    const mt = String(motion.motion_type).toLowerCase();
    const rot = String(motion.prop_rot_dir).toLowerCase();

    const NE = Location.NORTHEAST;
    const SE = Location.SOUTHEAST;
    const SW = Location.SOUTHWEST;
    const NW = Location.NORTHWEST;
    const N = Location.NORTH;
    const E = Location.EAST;
    const S = Location.SOUTH;
    const W = Location.WEST;

    // Infer grid mode from start/end locations (diagonals => diamond; cardinals => box)
    const diagonalSet = new Set<Location>([NE, SE, SW, NW]);
    const gridIsDiamond =
      diagonalSet.has(motion.start_loc) || diagonalSet.has(motion.end_loc);

    // Helper to normalize rotation keys
    const isCW = rot === "clockwise" || rot === "cw";
    const isCCW = rot === "counter_clockwise" || rot === "ccw";
    const isNoRot = rot === "no_rot";

    // Mapping builders
    const tuple = (a: number, b: number) => [a, b] as [number, number];

    // SHIFT (pro/anti/float)
    const shiftDiamond = () => {
      if (mt === "float") {
        // Handpath-based mapping; approximate via start/end step direction
        const order = [NE, SE, SW, NW];
        const idxStart = order.indexOf(motion.start_loc as Location);
        const idxEnd = order.indexOf(motion.end_loc as Location);
        // Determine cw vs ccw step (1 step cw => cw; else ccw)
        const cwStep = (idxStart + 1) % 4 === idxEnd;
        if (cwStep) {
          return [
            tuple(baseX, baseY),
            tuple(-baseY, baseX),
            tuple(-baseX, -baseY),
            tuple(baseY, -baseX),
          ];
        } else {
          return [
            tuple(-baseY, -baseX),
            tuple(baseX, -baseY),
            tuple(baseY, baseX),
            tuple(-baseX, baseY),
          ];
        }
      }
      if (mt === "pro" && isCW)
        return [
          tuple(baseX, baseY),
          tuple(-baseY, baseX),
          tuple(-baseX, -baseY),
          tuple(baseY, -baseX),
        ];
      if (mt === "pro" && isCCW)
        return [
          tuple(-baseY, -baseX),
          tuple(baseX, -baseY),
          tuple(baseY, baseX),
          tuple(-baseX, baseY),
        ];
      if (mt === "anti" && isCW)
        return [
          tuple(-baseY, -baseX),
          tuple(baseX, -baseY),
          tuple(baseY, baseX),
          tuple(-baseX, baseY),
        ];
      if (mt === "anti" && isCCW)
        return [
          tuple(baseX, baseY),
          tuple(-baseY, baseX),
          tuple(-baseX, -baseY),
          tuple(baseY, -baseX),
        ];
      return [
        tuple(baseX, baseY),
        tuple(baseX, baseY),
        tuple(baseX, baseY),
        tuple(baseX, baseY),
      ];
    };

    const shiftBox = () => {
      if (mt === "float") {
        // Use box cw/ccw from start->end around N,E,S,W order
        const order = [N, E, S, W];
        const idxStart = order.indexOf(motion.start_loc as Location);
        const idxEnd = order.indexOf(motion.end_loc as Location);
        const cwStep = (idxStart + 1) % 4 === idxEnd;
        if (cwStep) {
          return [
            tuple(baseX, baseY),
            tuple(-baseY, baseX),
            tuple(-baseX, -baseY),
            tuple(baseY, -baseX),
          ];
        } else {
          return [
            tuple(-baseY, -baseX),
            tuple(baseX, -baseY),
            tuple(baseY, baseX),
            tuple(-baseX, baseY),
          ];
        }
      }
      if (mt === "pro" && isCW)
        return [
          tuple(-baseX, baseY),
          tuple(-baseY, -baseX),
          tuple(baseX, -baseY),
          tuple(baseY, baseX),
        ];
      if (mt === "pro" && isCCW)
        return [
          tuple(baseX, baseY),
          tuple(-baseY, baseX),
          tuple(-baseX, -baseY),
          tuple(baseY, -baseX),
        ];
      if (mt === "anti" && isCW)
        return [
          tuple(-baseX, baseY),
          tuple(-baseY, -baseX),
          tuple(baseX, -baseY),
          tuple(baseY, baseX),
        ];
      if (mt === "anti" && isCCW)
        return [
          tuple(baseX, baseY),
          tuple(-baseY, baseX),
          tuple(-baseX, -baseY),
          tuple(baseY, -baseX),
        ];
      return [
        tuple(baseX, baseY),
        tuple(baseX, baseY),
        tuple(baseX, baseY),
        tuple(baseX, baseY),
      ];
    };

    // DASH
    const dashDiamond = () => {
      if (isCW)
        return [
          tuple(baseX, -baseY),
          tuple(baseY, baseX),
          tuple(-baseX, baseY),
          tuple(-baseY, -baseX),
        ];
      if (isCCW)
        return [
          tuple(-baseX, -baseY),
          tuple(baseY, -baseX),
          tuple(baseX, baseY),
          tuple(-baseY, baseX),
        ];
      if (isNoRot)
        return [
          tuple(baseX, baseY),
          tuple(-baseY, -baseX),
          tuple(baseX, -baseY),
          tuple(baseY, baseX),
        ];
      return [
        tuple(baseX, baseY),
        tuple(baseX, baseY),
        tuple(baseX, baseY),
        tuple(baseX, baseY),
      ];
    };

    const dashBox = () => {
      if (isCW)
        return [
          tuple(-baseY, baseX),
          tuple(-baseX, -baseY),
          tuple(baseY, -baseX),
          tuple(baseX, baseY),
        ];
      if (isCCW)
        return [
          tuple(-baseX, baseY),
          tuple(-baseY, -baseX),
          tuple(baseX, -baseY),
          tuple(baseY, baseX),
        ];
      if (isNoRot)
        return [
          tuple(baseX, baseY),
          tuple(-baseY, baseX),
          tuple(-baseX, -baseY),
          tuple(baseY, -baseX),
        ];
      return [
        tuple(baseX, baseY),
        tuple(baseX, baseY),
        tuple(baseX, baseY),
        tuple(baseX, baseY),
      ];
    };

    // STATIC
    const staticDiamond = () => {
      if (isCW)
        return [
          tuple(baseX, -baseY),
          tuple(baseY, baseX),
          tuple(-baseX, baseY),
          tuple(-baseY, -baseX),
        ];
      if (isCCW)
        return [
          tuple(-baseX, -baseY),
          tuple(baseY, -baseX),
          tuple(baseX, baseY),
          tuple(-baseY, baseX),
        ];
      return [
        tuple(baseX, baseY),
        tuple(-baseX, -baseY),
        tuple(-baseY, baseX),
        tuple(baseY, -baseX),
      ];
    };

    const staticBox = () => {
      if (isCW)
        return [
          tuple(baseX, baseY),
          tuple(-baseY, baseX),
          tuple(-baseX, -baseY),
          tuple(baseY, -baseX),
        ];
      if (isCCW)
        return [
          tuple(-baseY, -baseX),
          tuple(baseX, -baseY),
          tuple(baseY, baseX),
          tuple(-baseX, baseY),
        ];
      return [
        tuple(baseX, baseY),
        tuple(-baseY, baseX),
        tuple(-baseX, -baseY),
        tuple(baseY, -baseX),
      ];
    };

    // Dispatch by motion type and grid
    if (mt === "dash") return gridIsDiamond ? dashDiamond() : dashBox();
    if (mt === "static") return gridIsDiamond ? staticDiamond() : staticBox();
    // pro/anti/float
    return gridIsDiamond ? shiftDiamond() : shiftBox();
  }
}

export class QuadrantIndexCalculator implements IQuadrantIndexCalculator {
  /**
   * Calculator for quadrant indices used in directional tuple selection.
   */

  calculateQuadrantIndex(location: Location): number {
    /**
     * Calculate quadrant index for the given location.
     *
     * Args:
     *     location: Arrow location
     *
     * Returns:
     *     Quadrant index (0-3)
     */
    const quadrantMap: Record<Location, number> = {
      [Location.NORTHEAST]: 0,
      [Location.SOUTHEAST]: 1,
      [Location.SOUTHWEST]: 2,
      [Location.NORTHWEST]: 3,
      // Cardinal directions map to nearest quadrant
      [Location.NORTH]: 0, // Maps to NE quadrant
      [Location.EAST]: 1, // Maps to SE quadrant
      [Location.SOUTH]: 2, // Maps to SW quadrant
      [Location.WEST]: 3, // Maps to NW quadrant
    };

    return quadrantMap[location] || 0;
  }
}

export class DirectionalTupleProcessor implements IDirectionalTupleProcessor {
  /**
   * Processor for applying directional tuple adjustments to arrow positioning.
   */

  constructor(
    private directionalTupleService: IDirectionalTupleCalculator,
    private quadrantIndexService: IQuadrantIndexCalculator,
  ) {}

  processDirectionalTuples(
    baseAdjustment: Point,
    _motion: MotionData,
    location: Location,
  ): Point {
    /**
     * Process directional tuples to calculate final adjustment.
     *
     * Args:
     *     baseAdjustment: Base adjustment from placement services
     *     motion: Motion data for directional calculations
     *     location: Arrow location for quadrant selection
     *
     * Returns:
     *     Final adjustment point after directional processing
     */
    try {
      // Generate directional tuples from base adjustment
      const directionalTuples =
        this.directionalTupleService.generateDirectionalTuples(
          _motion,
          baseAdjustment.x,
          baseAdjustment.y,
        );

      // Calculate quadrant index for tuple selection
      const quadrantIndex =
        this.quadrantIndexService.calculateQuadrantIndex(location);

      // Select the appropriate tuple based on quadrant (legacy parity)
      const selectedTuple = directionalTuples[quadrantIndex] || [0, 0];

      // Final adjustment = selected tuple only (baseAdjustment already used to build tuples)
      return { x: selectedTuple[0], y: selectedTuple[1] };
    } catch (error) {
      console.warn(
        "Directional tuple processing failed, using base adjustment:",
        error,
      );
      return baseAdjustment;
    }
  }
}
