/**
 * Default Placement Service Contract
 */

import type { GridMode, MotionType } from "$shared";

export interface IDefaultPlacementService {
  getDefaultAdjustment(
    placementKey: string,
    turns: number | string,
    motionType: MotionType,
    gridMode: GridMode
  ): Promise<{ x: number; y: number }>;
  
  getAvailablePlacementKeys(
    motionType: MotionType,
    gridMode: GridMode
  ): Promise<string[]>;
  
  isLoaded(): boolean;
  
  getPlacementData(
    motionType: MotionType,
    placementKey: string,
    gridMode: GridMode
  ): Promise<{ [turns: string]: [number, number] }>;
  
  debugAvailableKeys(motionType: MotionType, gridMode: GridMode): Promise<void>;
}
