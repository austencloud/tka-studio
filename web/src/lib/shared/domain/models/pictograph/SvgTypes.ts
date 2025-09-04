/**
 * SVG Domain Types
 *
 * Domain models for SVG data structures used in pictograph rendering.
 * These are pure data contracts without behavior.
 */

// ============================================================================
// SVG DATA MODELS
// ============================================================================

export interface ArrowSvgData {
  id: string;
  svgContent: string;
  dimensions: SVGDimensions;
  imageSrc?: string;
  viewBox?: string;
  center?: { x: number; y: number };
}

export interface SVGDimensions {
  width: number;
  height: number;
  viewBox?: string;
  center?: { x: number; y: number };
}
