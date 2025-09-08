/**
 * Data Transformation Service
 *
 * Handles data transformation and adaptation between different formats.
 * Extracted from PictographRenderingService.
 */

import {
  createPictographData,
  GridMode,
  type BeatData,
  type GridData,
  type MotionData,
  type PictographData,
  type GridPointData as RawGridData,
} from "$shared";
import { injectable } from "inversify";
import type { IDataTransformer } from "../contracts/IDataTransformer";

// Interface moved to contracts/IDataTransformer.ts

@injectable()
export class DataTransformer implements IDataTransformer {
  /**
   * Convert beat data to pictograph data
   */
  beatToPictographData(beat: BeatData): PictographData {
    const motions: Record<string, MotionData> = {};
    if (beat.pictographData?.motions?.blue)
      motions.blue = beat.pictographData.motions.blue;
    if (beat.pictographData?.motions?.red)
      motions.red = beat.pictographData.motions.red;
    return createPictographData({
      id: `beat-${beat.beatNumber}`,
      motions,
      letter: beat.pictographData?.letter || null,
    });
  }

  /**
   * Adapt raw grid data to match the interface requirements
   */
  adaptGridData(rawGridData: RawGridData, mode: GridMode): GridData {
    // Filter out null coordinates and adapt to interface
    const adaptPoints = (
      points: Record<string, { coordinates: { x: number; y: number } | null }>
    ) => {
      const adapted: Record<string, { coordinates: { x: number; y: number } }> =
        {};
      for (const [key, point] of Object.entries(points)) {
        if (point.coordinates) {
          adapted[key] = { coordinates: point.coordinates };
        }
      }
      return adapted;
    };

    return {
      gridMode: mode,
      centerX: 0.0,
      centerY: 0.0,
      radius: 100.0,
      gridPointData: {
        allLayer2PointsNormal: adaptPoints(
          rawGridData.allLayer2PointsNormal || {}
        ),
        allHandPointsNormal: adaptPoints(rawGridData.allHandPointsNormal || {}),
        allHandPointsStrict: {},
        allLayer2PointsStrict: {},
        allOuterPoints: {},
        centerPoint: { coordinates: { x: 475, y: 475 } },
      },
    };
  }
}
