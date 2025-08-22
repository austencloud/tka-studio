/**
 * GridModeDerivationService - Microservice for determining grid mode from motion data
 *
 * CORRECTED LOGIC:
 * - Cardinal locations (N, E, S, W) in start/end positions = DIAMOND mode
 * - Intercardinal locations (NE, SE, SW, NW) in start/end positions = BOX mode
 */

import type { MotionData } from "../../../domain/MotionData";
import { GridMode, Location } from "../../../domain/enums";
import type { IGridModeDerivationService } from "../../interfaces/movement/IGridModeDerivationService";

export class GridModeDerivationService implements IGridModeDerivationService {
  /**
   * Determine grid mode from motion start/end locations
   *
   * CORRECTED: Cardinal locations = Diamond mode (not the other way around)
   */
  deriveGridMode(blueMotion: MotionData, redMotion: MotionData): GridMode {
    const cardinalLocations = [
      Location.NORTH,
      Location.EAST,
      Location.SOUTH,
      Location.WEST,
    ];

    const hasBlueStart = cardinalLocations.includes(blueMotion.startLocation);
    const hasBlueEnd = cardinalLocations.includes(blueMotion.endLocation);
    const hasRedStart = cardinalLocations.includes(redMotion.startLocation);
    const hasRedEnd = cardinalLocations.includes(redMotion.endLocation);

    // If any start/end location is cardinal, it's DIAMOND mode
    if (hasBlueStart || hasBlueEnd || hasRedStart || hasRedEnd) {
      return GridMode.DIAMOND;
    }

    // Otherwise it's BOX mode (intercardinal locations)
    return GridMode.BOX;
  }

  /**
   * Determine if motion uses cardinal locations
   */
  usesCardinalLocations(motion: MotionData): boolean {
    const cardinalLocations = [
      Location.NORTH,
      Location.EAST,
      Location.SOUTH,
      Location.WEST,
    ];
    return (
      cardinalLocations.includes(motion.startLocation) ||
      cardinalLocations.includes(motion.endLocation)
    );
  }

  /**
   * Determine if motion uses intercardinal locations
   */
  usesIntercardinalLocations(motion: MotionData): boolean {
    const intercardinalLocations = [
      Location.NORTHEAST,
      Location.SOUTHEAST,
      Location.SOUTHWEST,
      Location.NORTHWEST,
    ];
    return (
      intercardinalLocations.includes(motion.startLocation) ||
      intercardinalLocations.includes(motion.endLocation)
    );
  }
}
