/**
 * Data Transformation Service
 *
 * Handles data transformation and adaptation between different formats.
 * Extracted from PictographRenderingService.
 */

import type { BeatData, MotionData, PictographData } from "$lib/domain";
import {
  ArrowType,
  createArrowData,
  createGridData as createDomainGridData,
  createPictographData,
  createPropData,
  GridMode,
  MotionColor,
  PropType,
} from "$lib/domain";
import { type GridData as RawGridData } from "../../../data/gridCoordinates.js";
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
      gridData: createDomainGridData(),
      arrows: {
        blue: createArrowData({
          arrowType: ArrowType.BLUE,
          color: MotionColor.BLUE,
        }),
        red: createArrowData({
          arrowType: ArrowType.RED,
          color: MotionColor.RED,
        }),
      },
      props: {
        blue: createPropData({
          propType: PropType.STAFF,
          color: MotionColor.BLUE,
        }),
        red: createPropData({
          propType: PropType.STAFF,
          color: MotionColor.RED,
        }),
      },
      motions,
      letter: beat.pictographData?.letter || null,
      beat: beat.beatNumber,
      isBlank: beat.isBlank,
      isMirrored: false,
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
