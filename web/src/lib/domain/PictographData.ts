/**
 * Pictograph Domain Model
 *
 * Immutable data for a complete pictograph.
 * Based on modern desktop app's pictographData.py
 */

import { GridModeDerivationService } from "../services/implementations/domain/GridModeDerivationService";
import type { ArrowPlacementData } from "./ArrowPlacementData";
import type { GridData } from "./GridData";
import { Letter, getLetterType } from "./Letter";
import type { MotionData } from "./MotionData";
import type { PropPlacementData } from "./PropPlacementData";
import {
  Direction,
  GridMode,
  GridPosition,
  LetterType,
  MotionColor,
  MotionType,
  Orientation,
  RotationDirection,
  Timing,
} from "./enums";

export interface PictographData {
  readonly id: string;

  readonly motions: Partial<Record<MotionColor, MotionData>>;
  readonly letter?: Letter | null;
  readonly startPosition?: GridPosition | null;
  readonly endPosition?: GridPosition | null;
  readonly gridMode?: GridMode | null;
  readonly timing?: Timing | null;
  readonly direction?: Direction | null;
  readonly letterType?: LetterType | null;

  // Additional properties that the codebase expects
  readonly arrows?: Partial<Record<MotionColor, ArrowPlacementData>>;
  readonly props?: Partial<Record<MotionColor, PropPlacementData>>;
  readonly gridData?: GridData;

  readonly isBlank: boolean;
  readonly metadata: Record<string, unknown>;
}

export function createPictographData(
  data: Partial<PictographData> = {}
): PictographData {
  const derivedData =
    data.motions?.blue && data.motions?.red ? deriveFromMotionData(data) : data;

  return {
    id: data.id || crypto.randomUUID(),
    motions: derivedData.motions || {},
    letter: derivedData.letter || null,
    startPosition: derivedData.startPosition || null,
    endPosition: derivedData.endPosition || null,
    timing: derivedData.timing || null,
    direction: derivedData.direction || null,
    letterType:
      derivedData.letterType ||
      (derivedData.letter ? getLetterType(derivedData.letter) : null),
    isBlank: derivedData.isBlank ?? false,
    metadata: derivedData.metadata || {},
  };
}

/**
 * Required motion data properties for derivation
 */
export interface RequiredMotionDataForDerivation {
  readonly startLocation: Location;
  readonly endLocation: Location;
  readonly startOrientation: Orientation;
  readonly turns: number | "fl";
  readonly motionType: MotionType;
  readonly rotationDirection: RotationDirection;
}

/**
 * Type guard to check if motion data has all required properties for derivation
 */
export function hasRequiredMotionDataForDerivation(
  motionData: Partial<MotionData>
): motionData is Partial<MotionData> & RequiredMotionDataForDerivation {
  return (
    motionData &&
    motionData.startLocation !== undefined &&
    motionData.endLocation !== undefined &&
    motionData.startOrientation !== undefined &&
    motionData.turns !== undefined &&
    motionData.motionType !== undefined &&
    motionData.rotationDirection !== undefined
  );
}
/**
 * Derive all pictograph properties from motion data
 */
function deriveFromMotionData(
  data: Partial<PictographData>
): Partial<PictographData> {
  const blueMotion = data.motions?.blue;
  const redMotion = data.motions?.red;

  if (!blueMotion || !redMotion) {
    return data;
  }

  const gridModeService = new GridModeDerivationService();
  const gridMode = gridModeService.deriveGridMode(blueMotion, redMotion);

  //  TODO: Derive all other values, like letter and positions and timing and direction adn letter type

  return {
    ...data,
    gridMode,
    metadata: {
      ...data.metadata,
      derivedFrom: "motion_data",
    },
  };
}
