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

// Import orchestrator interface from positioning services
export type { IArrowPositioningOrchestrator } from "../positioning/core-services";

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
