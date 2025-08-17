/**
 * Pictograph and Rendering Service Interfaces
 *
 * Interfaces for pictograph rendering, SVG generation, and visual representation
 * of sequences and beats.
 */

import type {
  ArrowData,
  BeatData,
  PictographData,
  MotionData,
} from "./domain-types";
import type { GridMode } from "../../domain";
import type { GridData as RawGridData } from "../../data/gridCoordinates.js";
import type { ArrowPosition, GridData } from "./core-types";

// ============================================================================
// SHARED TYPES (imported from core-types to avoid duplication)
// ============================================================================

export interface ISvgConfiguration {
  readonly SVG_SIZE: number;
  readonly CENTER_X: number;
  readonly CENTER_Y: number;
}

// ============================================================================
// PICTOGRAPH SERVICE INTERFACES
// ============================================================================

/**
 * Core pictograph service for managing pictograph data and updates
 */
export interface IPictographService {
  renderPictograph(data: PictographData): Promise<SVGElement>;
  updateArrow(
    pictographId: string,
    arrowData: ArrowData
  ): Promise<PictographData>;
}

/**
 * Specialized rendering service for pictographs and beats
 */
export interface IPictographRenderingService {
  renderPictograph(data: PictographData): Promise<SVGElement>;
  renderBeat(beat: BeatData): Promise<SVGElement>;
}

// ============================================================================
// MICROSERVICE INTERFACES
// ============================================================================

/**
 * SVG utility service for basic SVG creation and utilities
 */
export interface ISvgUtilityService {
  createBaseSVG(): SVGElement;
  createErrorSVG(errorMessage?: string): SVGElement;
}

/**
 * Grid rendering service for grid visualization
 */
export interface IGridRenderingService {
  renderGrid(svg: SVGElement, gridMode?: GridMode): Promise<void>;
}

/**
 * Arrow rendering service for arrow visualization
 */
export interface IArrowRenderingService {
  renderArrowAtPosition(
    svg: SVGElement,
    color: "blue" | "red",
    position: ArrowPosition,
    motionData: MotionData | undefined
  ): Promise<void>;
}

/**
 * Overlay rendering service for glyphs and metadata
 */
export interface IOverlayRenderingService {
  renderOverlays(svg: SVGElement, data: PictographData): Promise<void>;
  renderIdLabel(svg: SVGElement, data: PictographData): void;
  renderDebugInfo(
    svg: SVGElement,
    data: PictographData,
    positions: Map<string, ArrowPosition>
  ): void;
}

/**
 * Data transformation service for format conversion
 */
export interface IDataTransformationService {
  beatToPictographData(beat: BeatData): PictographData;
  adaptGridData(rawGridData: RawGridData, mode: GridMode): GridData;
}
