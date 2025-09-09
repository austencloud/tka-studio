/**
 * Arrow Placement Service Contracts
 *
 * Interfaces for arrow placement calculations and key generation.
 */

import type { 
  ArrowPlacementData, 
  GridLocation, 
  GridMode, 
  MotionData, 
  MotionType, 
  PictographData 
} from "$shared";
import type { Point } from "fabric";

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

export interface IArrowPlacementKeyService {
  generatePlacementKey(
    motionData: MotionData,
    pictographData: PictographData,
    availableKeys: string[]
  ): string;

  generateBasicKey(motionType: MotionType): string;
}

export interface ISpecialPlacementService {
  getSpecialAdjustment(
    motionData: MotionData,
    pictographData: PictographData,
    arrowColor?: string
  ): Promise<Point | null>;
}

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

export interface IArrowAdjustmentLookup {
  getBaseAdjustment(
    pictographData: PictographData,
    motionData: MotionData,
    letter: string,
    arrowColor?: string
  ): Promise<Point>;
}
