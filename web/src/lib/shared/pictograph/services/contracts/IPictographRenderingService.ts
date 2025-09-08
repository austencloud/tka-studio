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
  ArrowPosition,
  ArrowSvgData,
  MotionData,
  PictographData,
  SVGDimensions,
} from "$shared";
import { MotionColor } from "$shared";

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================


export interface IPictographRenderingService {
  renderPictograph(data: PictographData): Promise<SVGElement>;
}






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
    position: ArrowPosition
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
