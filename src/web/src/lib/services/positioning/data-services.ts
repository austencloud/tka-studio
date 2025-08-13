/**
 * Data processing and directional tuple service interfaces.
 */

import type {
  ArrowData,
  GridMode,
  Location,
  MotionData,
  PictographData,
} from "$lib/domain";
import type { ArrowPosition, GridData, MotionType, Point } from "./types";

// Directional tuple processing interfaces
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
    motion: MotionData,
    location: Location,
  ): Point;
}

// Key generation interfaces
export interface IPlacementKeyGenerator {
  generatePlacementKey(
    motionData: MotionData,
    pictographData: PictographData,
    defaultPlacements: Record<string, unknown>,
    gridMode?: string,
  ): string;
}

export interface IAttributeKeyGenerator {
  getKeyFromArrow(arrowData: ArrowData, pictographData: PictographData): string;
}

export interface ISpecialPlacementOriKeyGenerator {
  generateOrientationKey(
    motionData: MotionData,
    pictographData: PictographData,
  ): string;
}

export interface ITurnsTupleKeyGenerator {
  generateTurnsTuple(pictographData: PictographData): number[];
}

// Data service interfaces
export interface IArrowPlacementDataService {
  getDefaultAdjustment(
    motionType: MotionType,
    placementKey: string,
    turns: number | string,
    gridMode: GridMode,
  ): Promise<{ x: number; y: number }>;
  getAvailablePlacementKeys(
    motionType: MotionType,
    gridMode: GridMode,
  ): Promise<string[]>;
  isLoaded(): boolean;
  loadPlacementData(): Promise<void>;
}

export interface IArrowPlacementKeyService {
  generatePlacementKey(motionData: MotionData, letter: string): string;
}

export interface IArrowPositioningService {
  calculateArrowPosition(
    arrowData: ArrowData,
    pictographData: PictographData,
    gridData: GridData,
  ): Promise<ArrowPosition>;
  calculateAllArrowPositions(
    pictographData: PictographData,
    gridData: GridData,
  ): Promise<Map<string, ArrowPosition>>;
  calculateRotationAngle(
    motion: MotionData,
    location: Location,
    isMirrored: boolean,
  ): number;
  shouldMirrorArrow(motion: MotionData): boolean;
}
