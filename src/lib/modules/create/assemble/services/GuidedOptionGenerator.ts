/**
 * Guided Option Generator Service
 *
 * Generates the 6 valid options from any given position for Guided Construct mode.
 * Returns single-prop pictographs (blue OR red, not both) representing:
 * - STATIC (stay at position)
 * - DASH (move to opposite position)
 * - SHIFT to adjacent position 1 (PRO and ANTI)
 * - SHIFT to adjacent position 2 (PRO and ANTI)
 */

import type { MotionColor } from "$shared";
import {
  GridLocation,
  GridMode,
  MotionType,
  Orientation,
  PropType,
  RotationDirection,
  type PictographData,
} from "$shared";
import { createMotionData, createPictographData } from "$shared";
import { injectable } from "inversify";

export interface IGuidedOptionGenerator {
  /**
   * Generate 6 valid options from a given position
   * @param currentLocation - The current grid location
   * @param handColor - Which hand we're building (blue or red)
   * @param gridMode - Diamond or Box mode
   * @param propType - Type of prop (staff, fan, etc.)
   * @returns Array of 6 single-prop pictographs
   */
  generateOptions(
    currentLocation: GridLocation,
    handColor: MotionColor,
    gridMode: GridMode,
    propType?: PropType
  ): PictographData[];
}

@injectable()
export class GuidedOptionGenerator implements IGuidedOptionGenerator {
  // Opposite locations for DASH moves
  private readonly oppositeLocations: Record<GridLocation, GridLocation> = {
    [GridLocation.NORTH]: GridLocation.SOUTH,
    [GridLocation.SOUTH]: GridLocation.NORTH,
    [GridLocation.EAST]: GridLocation.WEST,
    [GridLocation.WEST]: GridLocation.EAST,
    [GridLocation.NORTHEAST]: GridLocation.SOUTHWEST,
    [GridLocation.SOUTHWEST]: GridLocation.NORTHEAST,
    [GridLocation.SOUTHEAST]: GridLocation.NORTHWEST,
    [GridLocation.NORTHWEST]: GridLocation.SOUTHEAST,
  };

  // Adjacent locations for SHIFT moves (clockwise and counter-clockwise)
  private readonly diamondAdjacent: Record<
    GridLocation,
    { cw: GridLocation; ccw: GridLocation }
  > = {
    [GridLocation.NORTH]: { cw: GridLocation.EAST, ccw: GridLocation.WEST },
    [GridLocation.EAST]: { cw: GridLocation.SOUTH, ccw: GridLocation.NORTH },
    [GridLocation.SOUTH]: { cw: GridLocation.WEST, ccw: GridLocation.EAST },
    [GridLocation.WEST]: { cw: GridLocation.NORTH, ccw: GridLocation.SOUTH },
    // Placeholders for corner positions (not used in Diamond mode)
    [GridLocation.NORTHEAST]: {
      cw: GridLocation.SOUTHEAST,
      ccw: GridLocation.NORTHWEST,
    },
    [GridLocation.SOUTHEAST]: {
      cw: GridLocation.SOUTHWEST,
      ccw: GridLocation.NORTHEAST,
    },
    [GridLocation.SOUTHWEST]: {
      cw: GridLocation.NORTHWEST,
      ccw: GridLocation.SOUTHEAST,
    },
    [GridLocation.NORTHWEST]: {
      cw: GridLocation.NORTHEAST,
      ccw: GridLocation.SOUTHWEST,
    },
  };

  private readonly boxAdjacent: Record<
    GridLocation,
    { cw: GridLocation; ccw: GridLocation }
  > = {
    [GridLocation.NORTHEAST]: {
      cw: GridLocation.SOUTHEAST,
      ccw: GridLocation.NORTHWEST,
    },
    [GridLocation.SOUTHEAST]: {
      cw: GridLocation.SOUTHWEST,
      ccw: GridLocation.NORTHEAST,
    },
    [GridLocation.SOUTHWEST]: {
      cw: GridLocation.NORTHWEST,
      ccw: GridLocation.SOUTHEAST,
    },
    [GridLocation.NORTHWEST]: {
      cw: GridLocation.NORTHEAST,
      ccw: GridLocation.SOUTHWEST,
    },
    // Placeholders for cardinal positions (not used in Box mode)
    [GridLocation.NORTH]: { cw: GridLocation.EAST, ccw: GridLocation.WEST },
    [GridLocation.EAST]: { cw: GridLocation.SOUTH, ccw: GridLocation.NORTH },
    [GridLocation.SOUTH]: { cw: GridLocation.WEST, ccw: GridLocation.EAST },
    [GridLocation.WEST]: { cw: GridLocation.NORTH, ccw: GridLocation.SOUTH },
  };

  generateOptions(
    currentLocation: GridLocation,
    handColor: MotionColor,
    gridMode: GridMode,
    propType: PropType = PropType.HAND
  ): PictographData[] {
    const adjacent =
      gridMode === GridMode.DIAMOND ? this.diamondAdjacent : this.boxAdjacent;
    const adjacentLocations = adjacent[currentLocation];
    const oppositeLocation = this.oppositeLocations[currentLocation];

    const options: PictographData[] = [];

    // 1. STATIC (stay at current position)
    options.push(
      this.createSinglePropPictograph(
        handColor,
        currentLocation,
        currentLocation,
        MotionType.STATIC,
        RotationDirection.NO_ROTATION,
        gridMode,
        propType
      )
    );

    // 2. DASH (move to opposite position)
    options.push(
      this.createSinglePropPictograph(
        handColor,
        currentLocation,
        oppositeLocation,
        MotionType.DASH,
        RotationDirection.NO_ROTATION,
        gridMode,
        propType
      )
    );

    // 3. SHIFT to CW adjacent + PRO
    options.push(
      this.createSinglePropPictograph(
        handColor,
        currentLocation,
        adjacentLocations.cw,
        MotionType.PRO,
        RotationDirection.CLOCKWISE,
        gridMode,
        propType
      )
    );

    // 4. SHIFT to CW adjacent + ANTI
    options.push(
      this.createSinglePropPictograph(
        handColor,
        currentLocation,
        adjacentLocations.cw,
        MotionType.ANTI,
        RotationDirection.COUNTER_CLOCKWISE,
        gridMode,
        propType
      )
    );

    // 5. SHIFT to CCW adjacent + PRO
    options.push(
      this.createSinglePropPictograph(
        handColor,
        currentLocation,
        adjacentLocations.ccw,
        MotionType.PRO,
        RotationDirection.CLOCKWISE,
        gridMode,
        propType
      )
    );

    // 6. SHIFT to CCW adjacent + ANTI
    options.push(
      this.createSinglePropPictograph(
        handColor,
        currentLocation,
        adjacentLocations.ccw,
        MotionType.ANTI,
        RotationDirection.COUNTER_CLOCKWISE,
        gridMode,
        propType
      )
    );

    return options;
  }

  /**
   * Create a single-prop pictograph (only blue OR red motion, not both)
   */
  private createSinglePropPictograph(
    handColor: MotionColor,
    startLocation: GridLocation,
    endLocation: GridLocation,
    motionType: MotionType,
    rotationDirection: RotationDirection,
    gridMode: GridMode,
    propType: PropType
  ): PictographData {
    const motion = createMotionData({
      color: handColor,
      startLocation,
      endLocation,
      motionType,
      rotationDirection,
      gridMode,
      propType,
      startOrientation: Orientation.IN,
      endOrientation: Orientation.IN,
      turns: 0, // Default to 0 turns for guided building
      arrowLocation: startLocation, // Will be calculated by arrow services
      isVisible: true,
    });

    return createPictographData({
      motions: {
        [handColor]: motion,
      },
    });
  }
}
