/**
 * Arrow Placement Service Contract
 *
 * Loads and manages arrow placement JSON data for positioning calculations.
 * Ports the exact functionality from desktop DefaultPlacementService.
 */

import { GridMode, type MotionType } from "$shared";

// Placement data structure from JSON files
export interface JsonPlacementData {
  [placementKey: string]: {
    [turns: string]: [number, number]; // [x, y] adjustment
  };
}

// Complete placement data for all motion types
export interface GridPlacementData {
  [motionType: string]: JsonPlacementData;
}

// All placement data for all grid modes
export interface AllPlacementData {
  [gridMode: string]: GridPlacementData;
}

export interface IArrowPlacementService {
  getDefaultAdjustment(
    motionType: MotionType,
    placementKey: string,
    turns: number | string,
    gridMode: GridMode
  ): Promise<{ x: number; y: number }>;

  getAvailablePlacementKeys(
    motionType: MotionType,
    gridMode: GridMode
  ): Promise<string[]>;

  isLoaded(): boolean;
  loadPlacementData(): Promise<void>;
}
