/**
 * Positioning and Placement Service Interfaces
 *
 * Interfaces for arrow positioning, placement calculations, and coordinate systems.
 * This handles all spatial calculations and arrow placement logic.
 */

import type { MotionData, PictographData } from "./domain-types";
import type { GridMode } from "./core-types";
import type { MotionType } from "./domain-types";

// Import orchestrator interface from positioning services
export type { IArrowPositioningOrchestrator } from "../positioning/core-services";

// ============================================================================
// ARROW POSITIONING SERVICE
// ============================================================================

// Note: IArrowPositioningService removed - use IArrowPositioningOrchestrator directly
// The orchestrator provides the complete positioning pipeline

// ============================================================================
// ARROW PLACEMENT DATA SERVICE
// ============================================================================

/**
 * Service for managing arrow placement data and adjustments
 */
export interface IArrowPlacementDataService {
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
    color: "blue" | "red",
    motionData: MotionData,
    gridMode: GridMode
  ): Promise<SVGElement>;

  calculatePropPosition(
    motionData: MotionData,
    color: "blue" | "red",
    gridMode: GridMode
  ): Promise<{ x: number; y: number; rotation: number }>;

  loadPropSVG(propType: string, color: "blue" | "red"): Promise<string>;

  getSupportedPropTypes(): string[];
}
