/**
 * Beat Converter Service
 *
 * Handles conversion of PictographData to BeatData.
 * Single Responsibility: Transform pictograph data into beat format with proper initialization.
 */

import { injectable } from "inversify";
import type { PictographData, BeatData, MotionData, GridMode } from "$shared";
import { createMotionData } from "$shared";
import { GridLocation } from "$shared/pictograph/grid/domain/enums/grid-enums";
import {
  MotionType,
  RotationDirection,
  Orientation,
} from "$shared/pictograph/shared/domain/enums/pictograph-enums";

export interface IBeatConverterService {
  /**
   * Convert PictographData to BeatData - creates proper domain object
   */
  convertToBeat(
    pictograph: PictographData,
    beatNumber: number,
    gridMode: GridMode
  ): BeatData;
}

@injectable()
export class BeatConverterService implements IBeatConverterService {
  /**
   * Convert PictographData to BeatData - creates proper domain object
   */
  convertToBeat(
    pictograph: PictographData,
    beatNumber: number,
    gridMode: GridMode
  ): BeatData {
    // Ensure motions exist for blue and red with proper defaults
    const defaultMotion: MotionData = createMotionData({
      motionType: MotionType.STATIC,
      rotationDirection: RotationDirection.NO_ROTATION,
      startLocation: GridLocation.NORTH,
      endLocation: GridLocation.NORTH,
      turns: 0,
      startOrientation: Orientation.IN,
      endOrientation: Orientation.IN,
      gridMode: gridMode, // Add gridMode to default motion
    });

    // Add gridMode to the pictograph motions
    const motions = {
      blue: pictograph.motions.blue
        ? { ...pictograph.motions.blue, gridMode }
        : defaultMotion,
      red: pictograph.motions.red
        ? { ...pictograph.motions.red, gridMode }
        : defaultMotion,
    };

    return {
      ...pictograph, // Spread PictographData properties since BeatData extends PictographData
      id: crypto.randomUUID(),
      beatNumber: beatNumber,
      duration: 1.0,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
      motions, // Override motions with the enhanced version
    };
  }
}
