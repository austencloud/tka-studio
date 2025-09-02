/**
 * Pictograph and Rendering Service Interfaces
 *
 * Interfaces for pictograph rendering, SVG generation, and visual representation
 * of sequences and beats.
 */
// ============================================================================
// SHARED TYPES (imported from core-types to avoid duplication)
// ============================================================================
import type {
  ArrowPlacementData,
  ArrowSvgData,
  BeatData,
  GridData,
  GridMode,
  MotionData,
  PictographData,
  Position,
  GridPointData as RawGridData,
  SVGDimensions,
} from "$domain";
import { MotionColor } from "$domain";

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface ISvgConfiguration {
  readonly SVG_SIZE: number;
  readonly CENTER_X: number;
  readonly CENTER_Y: number;
}

export interface IPictographRenderingService {
  renderPictograph(data: PictographData): Promise<SVGElement>;
}

export interface ISvgUtilityService {
  createBaseSVG(): SVGElement;
  createErrorSVG(errorMessage?: string): SVGElement;
}

export interface IGridRenderingService {
  renderGrid(svg: SVGElement, gridMode?: GridMode): Promise<void>;
}

export interface IArrowRenderer {
  renderArrowAtPosition(
    svg: SVGElement,
    color: MotionColor,
    position: Position,
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

export interface IOverlayRenderer {
  renderOverlays(svg: SVGElement, data: PictographData): Promise<void>;
  renderIdLabel(svg: SVGElement, data: PictographData): void;
  renderDebugInfo(
    svg: SVGElement,
    data: PictographData,
    positions: Map<string, Position>
  ): void;
}

export interface IDataTransformer {
  beatToPictographData(beat: BeatData): PictographData;
  adaptGridData(rawGridData: RawGridData, mode: GridMode): GridData;
}

export interface IArrowPositioningService {
  /**
   * Render arrow at sophisticated calculated position using real SVG assets
   */
  renderArrowAtPosition(
    svg: SVGElement,
    color: MotionColor,
    position: Position,
    motionData: MotionData | undefined
  ): Promise<void>;
}

// MOVED TO positioning-interfaces.ts to avoid duplication
// export interface IArrowPathResolutionService {
//   /**
//    * Get arrow SVG path based on motion type and properties
//    */
//   getArrowPath(
//     arrowData: ArrowPlacementData,
//     motionData: MotionData
//   ): string | null;

//   /**
//    * Get the correct arrow SVG path based on motion data (optimized version)
//    */
//   getArrowSvgPath(motionData: MotionData | undefined): string;
// }

export interface ISvgColorTransformer {
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

export interface ISvgLoader {
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

export interface IFallbackArrowService {
  /**
   * Render arrow using fallback positioning when main service fails
   */
  renderFallbackArrow(
    svg: SVGElement,
    color: MotionColor,
    position: Position
  ): void;

  /**
   * Create enhanced arrow SVG path with sophisticated styling
   */
  createEnhancedArrowPath(color: MotionColor): SVGElement;
}

export interface ISvgParser {
  /**
   * Parse SVG content and extract dimensions and center point
   */
  parseArrowSvg(svgText: string): SVGDimensions;

  /**
   * Extract SVG content (everything inside the <svg> tags)
   */
  extractSvgContent(svgText: string): string;
}
