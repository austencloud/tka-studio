/**
 * Directional Tuple Processor
 *
 * Handles complex directional tuple processing for arrow positioning adjustments.
 * Direct TypeScript port of the Python DirectionalTupleProcessor.
 *
 * This service handles:
 * - Directional tuple generation based on motion data
 * - Complex adjustment processing for different motion types
 *
 * Note: Uses ArrowQuadrantCalculator for quadrant index calculations to avoid duplication.
 */

import { GridLocation, type MotionData } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { Point } from "fabric";
import { inject, injectable } from "inversify";
import type {
  IDirectionalTupleCalculator,
  IDirectionalTupleProcessor,
} from "../contracts";

@injectable()
export class DirectionalTupleCalculator implements IDirectionalTupleCalculator {
  /**
   * Calculator for directional tuples used in arrow positioning.
   */

  calculateDirectionalTuple(
    _motion: MotionData,
    _location: GridLocation
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
    baseY: number
  ): Array<[number, number]> {
    /**
     * Generate directional tuples using legacy mappings by motion type, rotation, and inferred grid.
     * Tuple order: indices 0..3 correspond to NE, SE, SW, NW quadrant mapping.
     */

    const mt = String(motion.motionType).toLowerCase();
    const rot = String(motion.rotationDirection).toLowerCase();

    // Debug logging disabled to prevent console flooding
    // console.group(`🔢 [DirectionalTupleCalculator] generateDirectionalTuples`);
    // console.log(`   Motion: ${motion.startLocation}→${motion.endLocation}`);
    // console.log(`   Base: (${baseX}, ${baseY})`);
    // console.log(`   Motion Type (raw): "${motion.motionType}" → normalized: "${mt}"`);
    // console.log(`   Rotation (raw): "${motion.rotationDirection}" → normalized: "${rot}"`);

    const NE = GridLocation.NORTHEAST;
    const SE = GridLocation.SOUTHEAST;
    const SW = GridLocation.SOUTHWEST;
    const NW = GridLocation.NORTHWEST;
    const N = GridLocation.NORTH;
    const E = GridLocation.EAST;
    const S = GridLocation.SOUTH;
    const W = GridLocation.WEST;

    // Infer grid mode from motion locations (NOT arrow locations)
    // Diamond mode: motion uses cardinals (N, E, S, W) → arrows placed at diagonals
    // Box mode: motion uses diagonals (NE, SE, SW, NW) → arrows placed at cardinals
    const cardinalSet = new Set<GridLocation>([N, E, S, W]);
    const gridIsDiamond =
      cardinalSet.has(motion.startLocation) ||
      cardinalSet.has(motion.endLocation);

    // Helper to normalize rotation keys
    const isCW = rot === "clockwise" || rot === "cw";
    const isCCW = rot === "counter_clockwise" || rot === "ccw";
    const isNoRot = rot === "noRotation";

    // console.log(`   Grid Mode: ${gridIsDiamond ? "DIAMOND" : "BOX"}`);
    // console.log(`   Rotation Detection: CW=${isCW}, CCW=${isCCW}, NoRot=${isNoRot}`);

    // Mapping builders
    const tuple = (a: number, b: number) => [a, b] as [number, number];

    // SHIFT (pro/anti/float)
    const shiftDiamond = () => {
      if (mt === "float") {
        // Handpath-based mapping; approximate via start/end step direction
        const order = [NE, SE, SW, NW];
        const idxStart = order.indexOf(motion.startLocation as GridLocation);
        const idxEnd = order.indexOf(motion.endLocation as GridLocation);
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
        const idxStart = order.indexOf(motion.startLocation as GridLocation);
        const idxEnd = order.indexOf(motion.endLocation as GridLocation);
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
    let result: Array<[number, number]>;
    let branchTaken = "";

    if (mt === "dash") {
      if (gridIsDiamond) {
        branchTaken = "dashDiamond()";
        result = dashDiamond();
      } else {
        branchTaken = "dashBox()";
        result = dashBox();
      }
    } else if (mt === "static") {
      if (gridIsDiamond) {
        branchTaken = "staticDiamond()";
        result = staticDiamond();
      } else {
        branchTaken = "staticBox()";
        result = staticBox();
      }
    } else {
      // pro/anti/float
      if (gridIsDiamond) {
        branchTaken = "shiftDiamond()";
        result = shiftDiamond();
      } else {
        branchTaken = "shiftBox()";
        result = shiftBox();
      }
    }

    // console.log(`   🎯 Branch selected: ${branchTaken}`);
    // console.log(`   📊 Generated tuples:`);
    // result.forEach((tuple, index) => {
    //   const quadrant = ['NE (0)', 'SE (1)', 'SW (2)', 'NW (3)'][index];
    //   console.log(`      ${quadrant}: (${tuple[0]}, ${tuple[1]})`);
    // });

    // // Check if transformation was applied
    // const allSameAsBase = result.every(t => t[0] === baseX && t[1] === baseY);
    // if (allSameAsBase) {
    //   console.warn(`   ⚠️ WARNING: All tuples are IDENTICAL to base (${baseX}, ${baseY})`);
    //   console.warn(`   ⚠️ NO TRANSFORMATION was applied!`);
    // } else {
    //   console.log(`   ✅ Transformation applied (tuples differ from base)`);
    // }
    // console.groupEnd();

    return result;
  }
}

@injectable()
export class QuadrantIndexCalculator {
  /**
   * Wrapper around ArrowQuadrantCalculator to maintain interface compatibility.
   * Delegates to the centralized quadrant calculation logic.
   */
  constructor(
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    @inject(TYPES.IArrowQuadrantCalculator) private quadrantCalculator: any
  ) {}

  calculateQuadrantIndex(motion: MotionData, location: GridLocation): number {
    return this.quadrantCalculator.calculateQuadrantIndex(motion, location);
  }
}

@injectable()
export class DirectionalTupleProcessor implements IDirectionalTupleProcessor {
  /**
   * Processor for applying directional tuple adjustments to arrow positioning.
   */

  constructor(
    @inject(TYPES.IDirectionalTupleCalculator)
    private directionalTupleService: IDirectionalTupleCalculator,
    @inject(TYPES.IQuadrantIndexCalculator)
    private quadrantIndexService: QuadrantIndexCalculator
  ) {}

  processDirectionalTuples(
    baseAdjustment: Point,
    motion: MotionData,
    location: GridLocation
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
    // Debug logging disabled to prevent console flooding
    // console.group(`✨ [DirectionalTupleProcessor] processDirectionalTuples`);
    // console.log(`   Motion: ${motion.startLocation}→${motion.endLocation}`);
    // console.log(`   Arrow Location: ${location}`);
    // console.log(`   Base Adjustment: (${baseAdjustment.x}, ${baseAdjustment.y})`);

    try {
      // Generate directional tuples from base adjustment
      const directionalTuples =
        this.directionalTupleService.generateDirectionalTuples(
          motion,
          baseAdjustment.x,
          baseAdjustment.y
        );

      // Calculate quadrant index for tuple selection
      const quadrantIndex = this.quadrantIndexService.calculateQuadrantIndex(
        motion,
        location
      );

      // console.log(`   🎯 Quadrant Index: ${quadrantIndex} (${['NE', 'SE', 'SW', 'NW'][quadrantIndex]})`);

      // Select the appropriate tuple based on quadrant (legacy parity)
      const selectedTuple = directionalTuples[quadrantIndex] || [0, 0];

      // console.log(`   📍 Selected Tuple: (${selectedTuple[0]}, ${selectedTuple[1]})`);

      // // Check if final differs from base
      // if (selectedTuple[0] === baseAdjustment.x && selectedTuple[1] === baseAdjustment.y) {
      //   console.warn(`   ⚠️ WARNING: Selected tuple EQUALS base adjustment!`);
      //   console.warn(`   ⚠️ NO transformation was applied to final result!`);
      // } else {
      //   console.log(`   ✅ Final adjustment differs from base (transformation applied)`);
      // }

      // console.groupEnd();

      // Final adjustment = selected tuple only (baseAdjustment already used to build tuples)
      return new Point(selectedTuple[0], selectedTuple[1]);
    } catch (error) {
      console.warn(
        "Directional tuple processing failed, using base adjustment:",
        error
      );
      // console.groupEnd();
      return baseAdjustment;
    }
  }
}
