/**
 * Data Transformation Service
 *
 * Handles data transformation and adaptation between different formats.
 * Extracted from PictographRenderingService.
 */

import type { BeatData, MotionData, PictographData } from "$lib/domain";
import { createPictographData, GridMode } from "$lib/domain";
import { type GridPointData as RawGridData } from "../../../data/gridCoordinates.js";
export interface GridData {
  mode: GridMode;
  allLayer2PointsNormal: Record<
    string,
    { coordinates: { x: number; y: number } }
  >;
  allHandPointsNormal: Record<
    string,
    { coordinates: { x: number; y: number } }
  >;
}

export interface IDataTransformationService {
  beatToPictographData(beat: BeatData): PictographData;
  adaptGridData(rawGridData: RawGridData, mode: GridMode): GridData;
}

export class DataTransformationService implements IDataTransformationService {
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
      isBlank: beat.isBlank,
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
      mode,
      allLayer2PointsNormal: adaptPoints(
        rawGridData.allLayer2PointsNormal || {}
      ),
      allHandPointsNormal: adaptPoints(rawGridData.allHandPointsNormal || {}),
    };
  }
}
