/**
 * GridModeDeriver - Microservice for determining grid mode from motion data
 *
 * CORRECTED LOGIC:
 * - Cardinal locations (N, E, S, W) in start/end positions = DIAMOND mode
 * - Box locations (NE, SE, SW, NW) in start/end positions = BOX mode
 */

import { injectable } from "inversify";
import { GridLocation, GridMode } from "../../../../../domain/enums";
import type {
  GridData,
  MotionData,
} from "../../../../../pictograph/domain/models";
import { createGridData } from "../../../../../pictograph/domain/models/GridData";
// import type { IGridModeDeriver } from "../../../contracts";

// Temporary interface definition
interface IGridModeDeriver {
  deriveGridMode(blueMotion: any, redMotion: any): any;
}

@injectable()
export class GridModeDeriver implements IGridModeDeriver {
  private readonly cardinalLocations = [
    GridLocation.NORTH,
    GridLocation.EAST,
    GridLocation.SOUTH,
    GridLocation.WEST,
  ];
  private readonly intercardinalLocations = [
    GridLocation.NORTHEAST,
    GridLocation.SOUTHEAST,
    GridLocation.SOUTHWEST,
    GridLocation.NORTHWEST,
  ];

  /**
   * Determine grid mode from motion start/end locations
   *
   * CORRECTED: Cardinal locations = Diamond mode (not the other way around)
   */
  deriveGridMode(blueMotion: MotionData, redMotion: MotionData): GridMode {
    const blueIsDiamond = this.usesDiamondLocations(blueMotion);
    const redIsDiamond = this.usesDiamondLocations(redMotion);

    const blueIsBox = this.usesBoxLocations(blueMotion);
    const redIsBox = this.usesBoxLocations(redMotion);

    const blueIsSkewed = this.isSkewed(blueMotion);
    const redIsSkewed = this.isSkewed(redMotion);

    if (blueIsSkewed || redIsSkewed) {
      return GridMode.SKEWED;
    }

    if (blueIsDiamond && redIsDiamond) {
      return GridMode.DIAMOND;
    } else if (blueIsBox && redIsBox) {
      return GridMode.BOX;
    } else {
      // Fallback if motions don't match expected patterns
      console.warn(
        "GridModeDeriver: Unable to determine grid mode from motions. Defaulting to DIAMOND."
      );
      return GridMode.DIAMOND;
    }
  }
  /**
   * Determine if motion uses cardinal locations
   */
  usesDiamondLocations(motion: MotionData): boolean {
    return (
      this.cardinalLocations.includes(motion.startLocation) &&
      this.cardinalLocations.includes(motion.endLocation)
    );
  }

  /**
   * Determine if motion uses intercardinal locations
   */
  usesBoxLocations(motion: MotionData): boolean {
    return (
      this.intercardinalLocations.includes(motion.startLocation) &&
      this.intercardinalLocations.includes(motion.endLocation)
    );
  }

  /**
   * Determine if motion is skewed (starts in one mode and ends in another)
   */
  isSkewed(motion: MotionData): boolean {
    const startIsCardinal = this.cardinalLocations.includes(
      motion.startLocation
    );
    const endIsCardinal = this.cardinalLocations.includes(motion.endLocation);
    const startIsBox = this.intercardinalLocations.includes(
      motion.startLocation
    );
    const endIsBox = this.intercardinalLocations.includes(motion.endLocation);

    return (startIsCardinal && endIsBox) || (startIsBox && endIsCardinal);
  }

  /**
   * Compute complete GridData from motion data
   * Uses existing deriveGridMode logic and creates GridData with default positioning
   */
  computeGridData(blueMotion: MotionData, redMotion: MotionData): GridData {
    const gridMode = this.deriveGridMode(blueMotion, redMotion);
    return createGridData({
      gridMode,
      centerX: 0.0,
      centerY: 0.0,
      radius: 100.0,
    });
  }
}
