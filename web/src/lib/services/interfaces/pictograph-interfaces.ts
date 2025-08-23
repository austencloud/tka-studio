/**
 * Pictograph and Rendering Service Interfaces
 *
 * Interfaces for pictograph rendering, SVG generation, and visual representation
 * of sequences and beats.
 */

import type { GridPointData as RawGridData } from "../../data/gridCoordinates.js";
import type { GridMode } from "../../domain";
import { MotionColor } from "../../domain/enums";
import type { ArrowPosition } from "../positioning/types";
import type { GridData } from "./core-types";
import type {
  ArrowPlacementData,
  BeatData,
  MotionData,
  PictographData,
} from "./domain-types";

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
    arrowData: ArrowPlacementData
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
    color: MotionColor,
    position: ArrowPosition,
    motionData: MotionData | undefined
  ): Promise<void>;

  // Methods extracted from Arrow.svelte business logic
  getArrowPath(
    arrowData: ArrowPlacementData,
    motionData: MotionData
  ): string | null;
  loadArrowPlacementData(
    arrowData: ArrowPlacementData,
    motionData: MotionData
  ): Promise<{
    imageSrc: string;
    viewBox: { width: number; height: number };
    center: { x: number; y: number };
  }>;
  parseArrowSvg(svgText: string): {
    viewBox: { width: number; height: number };
    center: { x: number; y: number };
  };
  applyColorToSvg(svgText: string, color: MotionColor): string;
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

// ============================================================================
// ARROW RENDERING INTERFACES
// ============================================================================

/**
 * Arrow positioning service for rendering arrows in SVG containers
 */
export interface IArrowPositioningService {
  /**
   * Render arrow at sophisticated calculated position using real SVG assets
   */
  renderArrowAtPosition(
    svg: SVGElement,
    color: MotionColor,
    position: ArrowPosition,
    motionData: MotionData | undefined
  ): Promise<void>;
}

/**
 * Arrow path resolution service for determining correct SVG file paths
 */
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

/**
 * SVG color transformation service for applying colors to SVG elements
 */
export interface ISvgColorTransformationService {
  /**
   * Apply color transformation to SVG text content
   */
  applyColorToSvg(svgText: string, color: MotionColor): string;

  /**
   * Apply color transformation to arrow SVG element
   */
  applyArrowColorTransformation(
    svgElement: SVGElement,
    color: MotionColor
  ): void;

  /**
   * Get fill and stroke colors for a given motion color
   */
  getColorsForMotionColor(color: MotionColor): {
    fill: string;
    stroke: string;
  };
}

/**
 * Arrow SVG data structure
 */
export interface ArrowSvgData {
  imageSrc: string;
  viewBox: { width: number; height: number };
  center: { x: number; y: number };
}

/**
 * SVG loading service for fetching and caching arrow SVG files
 */
export interface ISvgLoadingService {
  /**
   * Load arrow SVG data with color transformation
   */
  loadArrowPlacementData(
    arrowData: ArrowPlacementData,
    motionData: MotionData
  ): Promise<ArrowSvgData>;

  /**
   * Fetch SVG content from a given path
   */
  fetchSvgContent(path: string): Promise<string>;
}

/**
 * Fallback arrow service for rendering when sophisticated positioning fails
 */
export interface IFallbackArrowService {
  /**
   * Render arrow using fallback positioning when main service fails
   */
  renderFallbackArrow(
    svg: SVGElement,
    color: MotionColor,
    position: ArrowPosition
  ): void;

  /**
   * Create enhanced arrow SVG path with sophisticated styling
   */
  createEnhancedArrowPath(color: MotionColor): SVGElement;
}

/**
 * SVG dimensions data structure
 */
export interface SVGDimensions {
  viewBox: { width: number; height: number };
  center: { x: number; y: number };
}

/**
 * SVG parsing service for extracting dimensions and processing SVG content
 */
export interface ISvgParsingService {
  /**
   * Parse SVG content and extract dimensions and center point
   */
  parseArrowSvg(svgText: string): SVGDimensions;

  /**
   * Extract SVG content (everything inside the <svg> tags)
   */
  extractSvgContent(svgText: string): string;
}
