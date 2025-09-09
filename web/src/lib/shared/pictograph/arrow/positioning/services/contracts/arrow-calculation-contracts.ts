/**
 * Arrow Calculation Service Contracts
 *
 * Interfaces for various arrow calculation services.
 */

import type { 
  ArrowPlacementData,
  GridLocation, 
  MotionData, 
  MotionType,
  PictographData 
} from "$shared";
import type { Point } from "fabric";

export interface IArrowPointCalculator {
  calculatePoint(
    arrowData: ArrowPlacementData,
    motionData: MotionData,
    pictographData: PictographData
  ): Promise<{ x: number; y: number; rotation: number }>;
  
  shouldMirror(
    arrowData: ArrowPlacementData,
    motionData: MotionData,
    pictographData: PictographData
  ): boolean;
  
  renderArrowAtPoint(
    svg: SVGElement,
    arrowPoint: { x: number; y: number; rotation: number },
    motionData: MotionData
  ): Promise<void>;
}

export interface IArrowLocationService {
  calculateArrowLocation(input: {
    startLocation: string;
    endLocation: string;
    motionType: string;
  }): string;
}

export interface IArrowPathResolutionService {
  /**
   * Get arrow SVG path based on motion type and properties
   */
  getArrowPath(
    arrowData: ArrowPlacementData,
    motionData: MotionData
  ): string | null;

  /**
   * Get the correct arrow SVG path based on motion data (optimized version)
   */
  getArrowSvgPath(motionData: MotionData | undefined): string;
}

export interface IDashLocationCalculator {
  /**
   * Calculate dash arrow locations with comprehensive special case handling.
   */
  calculateDashLocationFromPictographData(
    pictographData: PictographData,
    motionData: MotionData,
    arrowColor: string
  ): GridLocation;
  
  calculateDashLocation(
    letter: string,
    startLocation: GridLocation,
    endLocation: GridLocation,
    motionType: MotionType,
    isLambda?: boolean,
    isLambdaDash?: boolean
  ): GridLocation;
}

export interface IDirectionalTupleCalculator {
  calculateDirectionalTuple(
    motion: MotionData,
    location: GridLocation
  ): [number, number];
  
  generateDirectionalTuples(
    motion: MotionData,
    baseX: number,
    baseY: number
  ): Array<[number, number]>;
}

export interface IQuadrantIndexCalculator {
  calculateQuadrantIndex(motion: MotionData, location: GridLocation): number;
}

export interface IDirectionalTupleProcessor {
  processDirectionalTuples(
    baseAdjustment: Point,
    motion: MotionData,
    location: GridLocation
  ): Point;
}
