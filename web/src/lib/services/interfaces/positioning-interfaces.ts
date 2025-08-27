/**
 * Positioning and Placement Service Interfaces
 *
 * Interfaces for arrow positioning, placement calculations, and coordinate systems.
 * This handles all spatial calculations and arrow placement logic.
 */

import type {
  ArrowPlacementData,
  MotionData,
  PictographData,
} from "./domain-types";
import type { GridMode } from "./core-types";
import type { MotionType } from "./domain-types";
import { MotionColor } from "../../domain/enums";
import type { Direction } from "../implementations/positioning/BetaPropDirectionCalculator";

// Import orchestrator interface from positioning services
export type { IArrowPositioningOrchestrator } from "../positioning/core-services";

// ============================================================================
// BETA OFFSET CALCULATOR
// ============================================================================

/**
 * Position interface for beta offset calculations
 */
export interface Position {
  x: number;
  y: number;
}

/**
 * Service interface for beta offset calculations
 * Converts direction values to pixel offsets for beta prop positioning
 */
export interface IBetaOffsetCalculator {
  /**
   * Calculate new position with offset based on direction
   */
  calculateNewPositionWithOffset(
    currentPosition: Position,
    direction: Direction
  ): Position;

  /**
   * Calculate beta separation offsets for both props
   * Returns offsets for blue and red props based on their calculated directions
   */
  calculateBetaSeparationOffsets(
    blueDirection: Direction | null,
    redDirection: Direction | null
  ): { blue: Position; red: Position };
}

// ============================================================================
// ARROW POSITIONING SERVICE
// ============================================================================

/**
 * Service interface for arrow positioning (thin wrapper around orchestrator)
 */
export interface IArrowPositioningService {
  calculatePosition(
    arrowData: ArrowPlacementData,
    motionData: MotionData,
    pictographData: PictographData
  ): Promise<{ x: number; y: number; rotation: number }>;
  shouldMirror(
    arrowData: ArrowPlacementData,
    motionData: MotionData,
    pictographData: PictographData
  ): boolean;
}

/**
 * Service interface for arrow location calculation
 */
export interface IArrowLocationService {
  calculateArrowLocation(input: {
    startLocation: string;
    endLocation: string;
    motionType: string;
  }): string;
}

// Note: IArrowPositioningOrchestrator provides the complete positioning pipeline

// ============================================================================
// ARROW PLACEMENT DATA SERVICE
// ============================================================================

/**
 * Service for managing arrow placement data and adjustments
 */
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

// ============================================================================
// ARROW PLACEMENT KEY SERVICE
// ============================================================================

/**
 * Service for generating and managing placement keys
 */
export interface IArrowPlacementKeyService {
  generatePlacementKey(
    motionData: MotionData,
    pictographData: PictographData,
    availableKeys: string[]
  ): string;

  generateBasicKey(motionType: MotionType): string;
}

// ============================================================================
// PROP RENDERING SERVICE
// ============================================================================

/**
 * Service for rendering and positioning props
 */
export interface IPropRenderingService {
  renderProp(
    propType: string,
    color: MotionColor,
    motionData: MotionData,
    gridMode: GridMode
  ): Promise<SVGElement>;

  calculatePropPosition(
    motionData: MotionData,
    color: MotionColor,
    gridMode: GridMode
  ): Promise<{ x: number; y: number; rotation: number }>;

  loadPropSVG(propType: string, color: MotionColor): Promise<string>;

  getSupportedPropTypes(): string[];
}
