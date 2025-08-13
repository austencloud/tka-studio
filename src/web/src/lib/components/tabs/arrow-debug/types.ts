/**
 * Shared types for Arrow Debug components
 */

import type { PictographData, MotionData, ArrowData } from "$lib/domain";
import type { Point } from "$lib/services/positioning/types";

export interface DebugError {
  step: string;
  error: string;
  timestamp: number;
}

export interface DebugTiming {
  totalDuration: number;
  stepDurations: Record<string, number>;
}

export interface LocationDebugInfo {
  motionType: string;
  startOri: string;
  endOri: string;
  calculationMethod: string;
}

export interface CoordinateSystemDebugInfo {
  sceneCenter: Point;
  sceneDimensions: [number, number];
  handPoints: Record<string, Point>;
  layer2Points: Record<string, Point>;
  usedCoordinateSet: "hand_points" | "layer2_points" | "center";
  coordinateSystemType: string;
}

export interface AdjustmentDebugInfo {
  placementKey: string;
  turns: number | string;
  motionType: string;
  gridMode: string;
  adjustmentSource: "default_placement" | "calculated" | "fallback";
  rawPlacementData: unknown;
}

export interface SpecialAdjustmentDebugInfo {
  letter: string;
  oriKey: string;
  turnsTuple: string;
  arrowColor: string;
  specialPlacementFound: boolean;
  specialPlacementData: unknown;
  adjustmentSource: "special_placement" | "none";
}

export interface TupleProcessingDebugInfo {
  baseAdjustment: Point;
  quadrantIndex: number;
  directionalTuples: Array<[number, number]>;
  selectedTuple: [number, number];
  transformationMethod: string;
}

export interface DebugStepData {
  // Input data
  pictographData: PictographData | null;
  motionData: MotionData | null;
  arrowData: ArrowData | null;

  // Step results
  calculatedLocation: string | null;
  locationDebugInfo: LocationDebugInfo | null;
  initialPosition: Point | null;
  coordinateSystemDebugInfo: CoordinateSystemDebugInfo | null;
  defaultAdjustment: Point | null;
  defaultAdjustmentDebugInfo: AdjustmentDebugInfo | null;
  specialAdjustment: Point | null;
  specialAdjustmentDebugInfo: SpecialAdjustmentDebugInfo | null;
  tupleProcessedAdjustment: Point | null;
  tupleProcessingDebugInfo: TupleProcessingDebugInfo | null;
  finalPosition: Point | null;
  finalRotation: number;

  // Meta
  errors: DebugError[];
  timing: DebugTiming | null;
}
